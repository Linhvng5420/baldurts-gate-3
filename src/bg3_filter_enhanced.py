#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BG3 Enhanced Filter Tool
Công cụ lọc nâng cao cho Baldur's Gate 3 XML files
Bao gồm: UI Text Filter, English Filter, Context Filter, và nhiều tính năng khác
"""

import xml.etree.ElementTree as ET
import re
import os
import sys
import logging
import html
import argparse
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Set, Tuple, Optional
from xml.dom import minidom

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('src/bg3_filter_enhanced.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class BG3EnhancedFilter:
    """Bộ lọc nâng cao cho BG3 XML files"""
    
    def __init__(self, config_file: str = "src/filter_config.json"):
        """Khởi tạo bộ lọc nâng cao"""
        self.config_file = config_file
        self.load_config()
        self.stats = {
            'total_entries': 0,
            'ui_text_found': 0,
            'english_only_found': 0,
            'context_filtered': 0,
            'dialogue_found': 0,
            'technical_found': 0,
            'errors': 0
        }
        
        # Vietnamese diacritics for English detection
        self.VIET_DIACRITICS = set("ăâđêôơưáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ")
        
        # Initialize filter components
        self._init_ui_patterns()
        self._init_ui_keywords()
        self._init_dialogue_patterns()
        self._init_technical_patterns()
        self._init_context_keywords()
    
    def load_config(self):
        """Load configuration from JSON file"""
        default_config = {
            "ui_filter": {
                "enabled": True,
                "max_length": 200,
                "min_ui_keywords": 1,
                "short_text_threshold": 50
            },
            "english_filter": {
                "enabled": True,
                "preserve_system_markers": True,
                "min_alpha_chars": 1
            },
            "dialogue_filter": {
                "enabled": True,
                "min_dialogue_length": 10,
                "max_dialogue_length": 500
            },
            "technical_filter": {
                "enabled": True,
                "preserve_debug": False
            },
            "context_filter": {
                "enabled": True,
                "categories": ["combat", "inventory", "menu", "quest", "character"]
            },
            "output_settings": {
                "base_dir": "output/filtered",
                "create_subfolders": True,
                "backup_original": False
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                    # Merge with defaults for missing keys
                    for key, value in default_config.items():
                        if key not in self.config:
                            self.config[key] = value
            else:
                self.config = default_config
                self.save_config()
        except Exception as e:
            logger.warning(f"Could not load config: {e}. Using defaults.")
            self.config = default_config
    
    def save_config(self):
        """Save current configuration to JSON file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Could not save config: {e}")
    
    def _init_ui_patterns(self) -> None:
        """Khởi tạo các pattern để nhận diện UI text"""
        self.ui_patterns = [
            # LSTag với Tooltip hoặc Type
            re.compile(r'&lt;LSTag\s+(?:Type="[^"]*"\s+)?Tooltip="[^"]*"[^&]*&gt;[^&]*&lt;/LSTag&gt;', re.IGNORECASE),
            
            # LSTag với Type
            re.compile(r'&lt;LSTag\s+Type="[^"]*"[^&]*&gt;[^&]*&lt;/LSTag&gt;', re.IGNORECASE),
            
            # Text có chứa placeholder số [1], [2], etc.
            re.compile(r'\[[0-9]+\]'),
            
            # Text có chứa &lt;br&gt;
            re.compile(r'&lt;br&gt;'),
            
            # Text có chứa các ký hiệu markup khác
            re.compile(r'&lt;[bi]&gt;.*?&lt;/[bi]&gt;'),
            
            # Text chứa tooltip keywords
            re.compile(r'\b(?:tooltip|interface|menu|button|panel|dialog|window)\b', re.IGNORECASE),
            
            # Text có format đặc biệt với dấu :
            re.compile(r'^[^:]{1,50}:\s*\[[0-9]+\]'),
            
            # Text có chứa instruction keys như [IE_PanelSelect]
            re.compile(r'\[IE_[A-Za-z0-9_]+\]'),
            
            # Hotkey patterns
            re.compile(r'\b(?:Ctrl|Alt|Shift|Tab|Enter|Esc)\b', re.IGNORECASE),
            
            # Status indicators
            re.compile(r'\b(?:enabled|disabled|selected|active|inactive)\b', re.IGNORECASE),
        ]
    
    def _init_ui_keywords(self) -> None:
        """Khởi tạo danh sách từ khóa UI"""
        self.ui_keywords = {
            # Menu và Navigation
            'save', 'load', 'options', 'settings', 'menu', 'exit', 'quit', 'close', 'cancel',
            'confirm', 'yes', 'no', 'ok', 'continue', 'start', 'new game', 'credits', 'help',
            'tutorial', 'back', 'next', 'previous', 'home', 'main menu',
            
            # Game UI
            'inventory', 'character', 'skills', 'abilities', 'spells', 'equipment', 'journal',
            'map', 'quest', 'party', 'combat', 'dialogue', 'trade', 'shop', 'vendor',
            
            # Actions
            'attack', 'defend', 'cast', 'use', 'equip', 'unequip', 'drop', 'pickup',
            'examine', 'talk', 'interact', 'move', 'rest', 'camp',
            
            # Stats và Game Mechanics
            'health', 'mana', 'stamina', 'strength', 'dexterity', 'constitution', 'intelligence',
            'wisdom', 'charisma', 'level', 'experience', 'gold', 'damage', 'armor', 'speed',
            'advantage', 'disadvantage', 'critical hit', 'saving throw', 'ability check',
            
            # Status Effects
            'poisoned', 'charmed', 'frightened', 'stunned', 'paralyzed', 'unconscious',
            'incapacitated', 'restrained', 'grappled', 'prone', 'blinded', 'deafened',
            
            # Tooltips
            'tooltip', 'description', 'effect', 'duration', 'range', 'target', 'components',
            'concentration', 'ritual', 'bonus action', 'reaction', 'legendary action',
            
            # Interface Elements
            'button', 'panel', 'window', 'dialog', 'dropdown', 'checkbox', 'slider',
            'tab', 'toolbar', 'statusbar', 'minimap', 'hotbar', 'quickslot'
        }
    
    def _init_dialogue_patterns(self) -> None:
        """Khởi tạo các pattern để nhận diện dialogue"""
        self.dialogue_patterns = [
            # Quoted speech
            re.compile(r'^[""\'"].*[""\'"]$'),
            
            # Character names followed by colon
            re.compile(r'^[A-Z][a-zA-Z\s]+:\s*'),
            
            # Common dialogue starters
            re.compile(r'^\b(?:I|You|We|They|He|She|Let|Please|Thank|Sorry|Excuse)\b', re.IGNORECASE),
            
            # Questions
            re.compile(r'.*\?$'),
            
            # Exclamations
            re.compile(r'.*!$'),
            
            # Stage directions in brackets
            re.compile(r'\[.*\]'),
        ]
    
    def _init_technical_patterns(self) -> None:
        """Khởi tạo các pattern để nhận diện technical text"""
        self.technical_patterns = [
            # System messages
            re.compile(r'^%%%.*'),
            
            # Debug messages
            re.compile(r'\b(?:debug|error|warning|info|trace)\b', re.IGNORECASE),
            
            # File paths
            re.compile(r'[a-zA-Z]:\\[\\a-zA-Z0-9\._\-]+'),
            
            # UUIDs/GUIDs
            re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.IGNORECASE),
            
            # Version numbers
            re.compile(r'\bv?\d+\.\d+(?:\.\d+)*\b'),
            
            # URLs
            re.compile(r'https?://[^\s]+'),
            
            # Code-like patterns
            re.compile(r'\b(?:function|class|method|variable|return|if|else|for|while)\b'),
        ]
    
    def _init_context_keywords(self) -> None:
        """Khởi tạo từ khóa theo context"""
        self.context_keywords = {
            'combat': {
                'attack', 'damage', 'critical', 'hit', 'miss', 'dodge', 'block', 'parry',
                'weapon', 'armor', 'shield', 'spell', 'magic', 'heal', 'poison', 'fire',
                'ice', 'lightning', 'death', 'kill', 'defeat', 'victory', 'battle', 'fight'
            },
            'inventory': {
                'item', 'inventory', 'equipment', 'weapon', 'armor', 'potion', 'scroll',
                'ring', 'amulet', 'boots', 'helmet', 'gloves', 'robe', 'sword', 'axe',
                'bow', 'staff', 'shield', 'gold', 'coin', 'sell', 'buy', 'trade'
            },
            'menu': {
                'menu', 'option', 'setting', 'config', 'preference', 'save', 'load',
                'exit', 'quit', 'start', 'new', 'continue', 'back', 'next', 'cancel',
                'confirm', 'yes', 'no', 'ok', 'apply', 'reset', 'default'
            },
            'quest': {
                'quest', 'mission', 'objective', 'goal', 'task', 'complete', 'finish',
                'progress', 'journal', 'log', 'update', 'reward', 'experience', 'xp',
                'level', 'advance', 'unlock', 'discover', 'explore', 'find', 'search'
            },
            'character': {
                'character', 'hero', 'player', 'party', 'companion', 'ally', 'friend',
                'enemy', 'npc', 'villain', 'boss', 'leader', 'follower', 'member',
                'skill', 'ability', 'talent', 'feat', 'trait', 'attribute', 'stat'
            }
        }
    
    def strip_tags(self, text: str) -> str:
        """Remove XML-like tags & unescape HTML entities"""
        if not text:
            return ""
        # Unescape basic entities first
        unescaped = html.unescape(text)
        # Remove angle-bracket tags
        no_tags = re.sub(r'<[^>]+>', '', unescaped)
        return no_tags.strip()
    
    def is_ui_text(self, content: str) -> bool:
        """
        Kiểm tra xem content có phải là UI text không
        """
        if not content or len(content.strip()) == 0:
            return False
        
        content_lower = content.lower()
        content_clean = self.strip_tags(content)
        
        # Kiểm tra độ dài
        max_length = self.config['ui_filter']['max_length']
        if len(content_clean) > max_length:
            # Nếu dài nhưng có LSTag hoặc các pattern đặc biệt thì vẫn có thể là UI
            has_special_patterns = any(pattern.search(content) for pattern in self.ui_patterns[:4])
            if not has_special_patterns:
                return False
        
        # Kiểm tra các pattern đặc biệt
        for pattern in self.ui_patterns:
            if pattern.search(content):
                logger.debug(f"UI pattern matched: {pattern.pattern[:50]}...")
                return True
        
        # Kiểm tra từ khóa UI
        words = re.findall(r'\b\w+\b', content_lower)
        ui_word_count = sum(1 for word in words if word in self.ui_keywords)
        
        min_keywords = self.config['ui_filter']['min_ui_keywords']
        short_threshold = self.config['ui_filter']['short_text_threshold']
        
        # Nếu có ít nhất min_keywords từ UI và text ngắn
        if ui_word_count >= min_keywords and len(content_clean) < short_threshold:
            logger.debug(f"UI keyword matched in short text: {ui_word_count} keywords")
            return True
        
        # Nếu có nhiều từ UI trong text dài hơn
        if ui_word_count >= 2:
            logger.debug(f"Multiple UI keywords matched: {ui_word_count} keywords")
            return True
        
        # Text ngắn không có dấu câu phức tạp
        if len(words) <= 3 and not re.search(r'[.!?;,]{2,}', content):
            # Loại trừ những câu thoại rõ ràng
            if not re.search(r'["\']|(\bI\b)|(\byou\b)|(\bhe\b)|(\bshe\b)|(\bthey\b)', content_lower):
                logger.debug(f"Short text without dialogue indicators: {content[:30]}...")
                return True
        
        return False
    
    def is_english_only(self, text: str) -> bool:
        """
        Kiểm tra xem text có phải chỉ tiếng Anh không
        """
        if not text:
            return False
        
        if not self.config['english_filter']['enabled']:
            return False
        
        clean_text = self.strip_tags(text).lower()
        # Remove bracketed placeholders
        clean_text = re.sub(r'\[[^\]]*\]', ' ', clean_text)
        
        # Check for Vietnamese diacritics
        for ch in clean_text:
            if ch in self.VIET_DIACRITICS:
                return False
        
        # Must have at least one ASCII letter
        min_alpha = self.config['english_filter']['min_alpha_chars']
        if len(re.findall(r'[a-z]', clean_text)) < min_alpha:
            return False
        
        # Preserve system markers if configured
        if self.config['english_filter']['preserve_system_markers']:
            if clean_text.strip().startswith('%%%'):
                return False
        
        return True
    
    def is_dialogue(self, text: str) -> bool:
        """
        Kiểm tra xem text có phải là dialogue không
        """
        if not text or not self.config['dialogue_filter']['enabled']:
            return False
        
        clean_text = self.strip_tags(text).strip()
        min_length = self.config['dialogue_filter']['min_dialogue_length']
        max_length = self.config['dialogue_filter']['max_dialogue_length']
        
        if len(clean_text) < min_length or len(clean_text) > max_length:
            return False
        
        # Check dialogue patterns
        for pattern in self.dialogue_patterns:
            if pattern.search(clean_text):
                return True
        
        return False
    
    def is_technical(self, text: str) -> bool:
        """
        Kiểm tra xem text có phải là technical text không
        """
        if not text or not self.config['technical_filter']['enabled']:
            return False
        
        clean_text = self.strip_tags(text)
        
        # Check technical patterns
        for pattern in self.technical_patterns:
            if pattern.search(clean_text):
                return True
        
        return False
    
    def get_content_context(self, text: str) -> List[str]:
        """
        Xác định context của content
        """
        if not text or not self.config['context_filter']['enabled']:
            return []
        
        clean_text = self.strip_tags(text).lower()
        words = set(re.findall(r'\b\w+\b', clean_text))
        contexts = []
        
        enabled_categories = self.config['context_filter']['categories']
        
        for category, keywords in self.context_keywords.items():
            if category in enabled_categories:
                if words.intersection(keywords):
                    contexts.append(category)
        
        return contexts
    
    def filter_xml_file(self, input_file: str, output_options: Dict[str, str]) -> Dict[str, any]:
        """
        Lọc file XML với nhiều tiêu chí
        """
        logger.info(f"Bắt đầu lọc file: {input_file}")
        
        try:
            tree = ET.parse(input_file)
            root = tree.getroot()
            
            # Tạo các cấu trúc XML riêng cho từng loại
            filter_results = {}
            
            if output_options.get('ui_text'):
                filter_results['ui_text'] = ET.Element("contentList")
            if output_options.get('english_only'):
                filter_results['english_only'] = ET.Element("contentList")
            if output_options.get('dialogue'):
                filter_results['dialogue'] = ET.Element("contentList")
            if output_options.get('technical'):
                filter_results['technical'] = ET.Element("contentList")
            if output_options.get('by_context'):
                filter_results['by_context'] = {}
                for context in self.config['context_filter']['categories']:
                    filter_results['by_context'][context] = ET.Element("contentList")
            if output_options.get('non_english'):
                filter_results['non_english'] = ET.Element("contentList")
            
            # Xử lý từng content entry
            for content_elem in root.findall('content'):
                self.stats['total_entries'] += 1
                
                content_text = content_elem.text if content_elem.text else ""
                contentuid = content_elem.get('contentuid', '')
                version = content_elem.get('version', '1')
                
                # Tạo element copy
                def create_content_copy():
                    new_elem = ET.Element('content')
                    new_elem.set('contentuid', contentuid)
                    new_elem.set('version', version)
                    new_elem.text = content_text
                    return new_elem
                
                # Kiểm tra và phân loại
                if self.is_ui_text(content_text) and 'ui_text' in filter_results:
                    filter_results['ui_text'].append(create_content_copy())
                    self.stats['ui_text_found'] += 1
                
                if self.is_english_only(content_text) and 'english_only' in filter_results:
                    filter_results['english_only'].append(create_content_copy())
                    self.stats['english_only_found'] += 1
                elif 'non_english' in filter_results and content_text.strip():
                    # Non-English (có nội dung và không phải English-only)
                    filter_results['non_english'].append(create_content_copy())
                
                if self.is_dialogue(content_text) and 'dialogue' in filter_results:
                    filter_results['dialogue'].append(create_content_copy())
                    self.stats['dialogue_found'] += 1
                
                if self.is_technical(content_text) and 'technical' in filter_results:
                    filter_results['technical'].append(create_content_copy())
                    self.stats['technical_found'] += 1
                
                # Context filtering
                if 'by_context' in filter_results:
                    contexts = self.get_content_context(content_text)
                    for context in contexts:
                        if context in filter_results['by_context']:
                            filter_results['by_context'][context].append(create_content_copy())
                            self.stats['context_filtered'] += 1
            
            # Lưu các file kết quả
            output_files = {}
            base_dir = Path(self.config['output_settings']['base_dir'])
            
            if self.config['output_settings']['create_subfolders']:
                base_dir = base_dir / Path(input_file).stem
            
            base_dir.mkdir(parents=True, exist_ok=True)
            
            for filter_type, xml_root in filter_results.items():
                if filter_type == 'by_context':
                    context_dir = base_dir / 'by_context'
                    context_dir.mkdir(exist_ok=True)
                    for context, context_root in xml_root.items():
                        if len(context_root) > 0:  # Only save if has content
                            output_file = context_dir / f"{context}.xml"
                            self._save_xml_file(context_root, str(output_file))
                            output_files[f'context_{context}'] = str(output_file)
                else:
                    if len(xml_root) > 0:  # Only save if has content
                        output_file = base_dir / f"{filter_type}.xml"
                        self._save_xml_file(xml_root, str(output_file))
                        output_files[filter_type] = str(output_file)
            
            # Tạo báo cáo thống kê
            report_file = base_dir / "filter_report.txt"
            self._create_report(str(report_file), input_file, output_files)
            
            logger.info(f"Hoàn thành lọc file. Kết quả lưu trong: {base_dir}")
            logger.info(f"Tổng entries: {self.stats['total_entries']}")
            logger.info(f"UI text: {self.stats['ui_text_found']}")
            logger.info(f"English-only: {self.stats['english_only_found']}")
            logger.info(f"Dialogue: {self.stats['dialogue_found']}")
            logger.info(f"Technical: {self.stats['technical_found']}")
            
            return {
                'stats': self.stats.copy(),
                'output_files': output_files,
                'output_dir': str(base_dir)
            }
            
        except Exception as e:
            self.stats['errors'] += 1
            logger.error(f"Lỗi khi xử lý file {input_file}: {str(e)}")
            raise
    
    def _save_xml_file(self, xml_root: ET.Element, output_file: str) -> None:
        """Lưu XML file với format đẹp"""
        rough_string = ET.tostring(xml_root, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ", encoding='utf-8')
        
        with open(output_file, 'wb') as f:
            f.write(pretty_xml)
    
    def _create_report(self, report_file: str, input_file: str, output_files: Dict[str, str]) -> None:
        """Tạo báo cáo thống kê chi tiết"""
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("BG3 ENHANCED FILTER REPORT\n")
            f.write("=" * 50 + "\n")
            f.write(f"Input file: {input_file}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("FILTER STATISTICS:\n")
            f.write(f"Total entries processed: {self.stats['total_entries']:,}\n")
            f.write(f"UI text found: {self.stats['ui_text_found']:,}\n")
            f.write(f"English-only found: {self.stats['english_only_found']:,}\n")
            f.write(f"Dialogue found: {self.stats['dialogue_found']:,}\n")
            f.write(f"Technical found: {self.stats['technical_found']:,}\n")
            f.write(f"Context filtered: {self.stats['context_filtered']:,}\n")
            f.write(f"Processing errors: {self.stats['errors']}\n\n")
            
            f.write("OUTPUT FILES:\n")
            for filter_type, file_path in output_files.items():
                f.write(f"- {filter_type}: {file_path}\n")
            
            f.write("\nFILTER CONFIGURATION:\n")
            f.write(json.dumps(self.config, indent=2, ensure_ascii=False))
    
    def analyze_xml_file(self, input_file: str) -> Dict[str, any]:
        """
        Phân tích file XML không tạo output, chỉ thống kê
        """
        logger.info(f"Bắt đầu phân tích file: {input_file}")
        
        analysis = {
            'total_entries': 0,
            'empty_entries': 0,
            'ui_candidates': 0,
            'english_only_candidates': 0,
            'dialogue_candidates': 0,
            'technical_candidates': 0,
            'context_distribution': defaultdict(int),
            'length_distribution': defaultdict(int),
            'sample_entries': {
                'ui': [],
                'english_only': [],
                'dialogue': [],
                'technical': []
            }
        }
        
        try:
            tree = ET.parse(input_file)
            root = tree.getroot()
            
            all_content = root.findall('content')
            total_content = len(all_content)
            
            logger.info(f"Tìm thấy {total_content} entries để phân tích")
            
            for i, content_elem in enumerate(all_content):
                if i % 10000 == 0 and i > 0:
                    logger.info(f"Đã xử lý {i}/{total_content} entries ({i/total_content*100:.1f}%)")
                
                analysis['total_entries'] += 1
                content_text = content_elem.text if content_elem.text else ""
                
                if not content_text.strip():
                    analysis['empty_entries'] += 1
                    continue
                
                # Length distribution
                length_category = self._get_length_category(len(content_text))
                analysis['length_distribution'][length_category] += 1
                
                # Filter analysis
                if self.is_ui_text(content_text):
                    analysis['ui_candidates'] += 1
                    if len(analysis['sample_entries']['ui']) < 5:
                        analysis['sample_entries']['ui'].append({
                            'uid': content_elem.get('contentuid', ''),
                            'text': content_text[:100] + '...' if len(content_text) > 100 else content_text
                        })
                
                if self.is_english_only(content_text):
                    analysis['english_only_candidates'] += 1
                    if len(analysis['sample_entries']['english_only']) < 5:
                        analysis['sample_entries']['english_only'].append({
                            'uid': content_elem.get('contentuid', ''),
                            'text': content_text[:100] + '...' if len(content_text) > 100 else content_text
                        })
                
                if self.is_dialogue(content_text):
                    analysis['dialogue_candidates'] += 1
                    if len(analysis['sample_entries']['dialogue']) < 5:
                        analysis['sample_entries']['dialogue'].append({
                            'uid': content_elem.get('contentuid', ''),
                            'text': content_text[:100] + '...' if len(content_text) > 100 else content_text
                        })
                
                if self.is_technical(content_text):
                    analysis['technical_candidates'] += 1
                    if len(analysis['sample_entries']['technical']) < 5:
                        analysis['sample_entries']['technical'].append({
                            'uid': content_elem.get('contentuid', ''),
                            'text': content_text[:100] + '...' if len(content_text) > 100 else content_text
                        })
                
                # Context distribution
                contexts = self.get_content_context(content_text)
                for context in contexts:
                    analysis['context_distribution'][context] += 1
            
            logger.info(f"Hoàn thành phân tích file: {analysis['total_entries']} entries")
            return analysis
            
        except Exception as e:
            logger.error(f"Lỗi khi phân tích file {input_file}: {str(e)}")
            raise
    
    def _get_length_category(self, length: int) -> str:
        """Phân loại độ dài text"""
        if length == 0:
            return "empty"
        elif length <= 20:
            return "very_short"
        elif length <= 50:
            return "short"
        elif length <= 100:
            return "medium"
        elif length <= 200:
            return "long"
        else:
            return "very_long"


def create_cli_parser():
    """Tạo command line parser"""
    parser = argparse.ArgumentParser(
        description="BG3 Enhanced Filter Tool - Công cụ lọc nâng cao cho Baldur's Gate 3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  # Lọc UI text
  python bg3_filter_enhanced.py input.xml --ui-text
  
  # Lọc English-only content
  python bg3_filter_enhanced.py input.xml --english-only
  
  # Lọc tất cả loại
  python bg3_filter_enhanced.py input.xml --all
  
  # Chỉ phân tích không tạo output
  python bg3_filter_enhanced.py input.xml --analyze-only
  
  # Sử dụng config file khác
  python bg3_filter_enhanced.py input.xml --config custom_config.json --ui-text
        """
    )
    
    parser.add_argument('input_file', help='File XML cần lọc')
    parser.add_argument('--config', default='src/filter_config.json', help='File cấu hình JSON')
    parser.add_argument('--output-dir', help='Thư mục output (ghi đè config)')
    
    # Filter options
    parser.add_argument('--ui-text', action='store_true', help='Lọc UI text')
    parser.add_argument('--english-only', action='store_true', help='Lọc English-only content')
    parser.add_argument('--non-english', action='store_true', help='Lọc non-English content') 
    parser.add_argument('--dialogue', action='store_true', help='Lọc dialogue')
    parser.add_argument('--technical', action='store_true', help='Lọc technical text')
    parser.add_argument('--by-context', action='store_true', help='Lọc theo context')
    parser.add_argument('--all', action='store_true', help='Lọc tất cả loại')
    
    # Analysis only
    parser.add_argument('--analyze-only', action='store_true', help='Chỉ phân tích, không tạo output')
    
    # Debug options
    parser.add_argument('--verbose', '-v', action='store_true', help='Hiển thị log chi tiết')
    parser.add_argument('--debug', action='store_true', help='Bật debug mode')
    
    return parser


def main():
    """Hàm chính"""
    parser = create_cli_parser()
    args = parser.parse_args()
    
    # Setup logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    
    logger.info("Bắt đầu BG3 Enhanced Filter Tool")
    
    # Kiểm tra file input
    if not os.path.exists(args.input_file):
        logger.error(f"File input không tồn tại: {args.input_file}")
        return 1
    
    try:
        # Khởi tạo filter
        filter_tool = BG3EnhancedFilter(args.config)
        
        # Override output dir if provided
        if args.output_dir:
            filter_tool.config['output_settings']['base_dir'] = args.output_dir
        
        if args.analyze_only:
            # Chỉ phân tích
            analysis = filter_tool.analyze_xml_file(args.input_file)
            
            print("\n" + "=" * 50)
            print("PHÂN TÍCH FILE XML")
            print("=" * 50)
            print(f"Tổng entries: {analysis['total_entries']:,}")
            print(f"Entries trống: {analysis['empty_entries']:,}")
            print(f"UI candidates: {analysis['ui_candidates']:,}")
            print(f"English-only candidates: {analysis['english_only_candidates']:,}")
            print(f"Dialogue candidates: {analysis['dialogue_candidates']:,}")
            print(f"Technical candidates: {analysis['technical_candidates']:,}")
            
            print(f"\nPhân bố độ dài:")
            for length_cat, count in analysis['length_distribution'].items():
                print(f"  {length_cat}: {count:,}")
            
            print(f"\nPhân bố context:")
            for context, count in analysis['context_distribution'].items():
                print(f"  {context}: {count:,}")
            
            # Save analysis to file
            analysis_file = f"src/{Path(args.input_file).stem}_analysis.json"
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump(dict(analysis), f, indent=2, ensure_ascii=False, default=str)
            print(f"\nPhân tích chi tiết lưu tại: {analysis_file}")
            
        else:
            # Xác định output options
            output_options = {}
            if args.all:
                output_options = {
                    'ui_text': True,
                    'english_only': True,
                    'non_english': True,
                    'dialogue': True,
                    'technical': True,
                    'by_context': True
                }
            else:
                if args.ui_text:
                    output_options['ui_text'] = True
                if args.english_only:
                    output_options['english_only'] = True
                if args.non_english:
                    output_options['non_english'] = True
                if args.dialogue:
                    output_options['dialogue'] = True
                if args.technical:
                    output_options['technical'] = True
                if args.by_context:
                    output_options['by_context'] = True
            
            if not output_options:
                logger.error("Vui lòng chọn ít nhất một loại filter hoặc sử dụng --all")
                return 1
            
            # Lọc file
            results = filter_tool.filter_xml_file(args.input_file, output_options)
            
            print("\n" + "=" * 50)
            print("KẾT QUẢ LỌC")
            print("=" * 50)
            print(f"Thư mục output: {results['output_dir']}")
            print(f"Tổng entries: {results['stats']['total_entries']:,}")
            
            for filter_type in output_options.keys():
                if filter_type in results['output_files']:
                    print(f"✓ {filter_type}: {results['output_files'][filter_type]}")
            
            print("\nThống kê chi tiết:")
            for key, value in results['stats'].items():
                if key != 'total_entries':
                    print(f"  {key}: {value:,}")
        
        logger.info("Hoàn thành thành công!")
        return 0
        
    except KeyboardInterrupt:
        logger.info("Đã hủy thao tác bởi người dùng")
        return 1
    except Exception as e:
        logger.error(f"Lỗi chung: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
