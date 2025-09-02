#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to extract remaining workkeys from english.xml
"""

import re
import xml.etree.ElementTree as ET
import os
import sys
from datetime import datetime

def extract_workkeys_from_xml(input_file, output_file):
    """Extract entries containing workkeys and save to separate file"""
    
    # Define workkey patterns to search for
    workkey_patterns = [
        r'PortraitClick',
		r'PortraitClickSpam',
        r'HelpGeneral Combat',
        r'HelpGeneral Normal',
        r'HelpGeneral Sneaking',
        r'HelpImmobilized Combat',
        r'HelpImmobilized Normal',
        r'HelpImmobilized Sneaking',
        r'BuffTarget Combat',
        r'BuffTarget Normal',
        r'BuffTarget Sneaking',
        r'SpeakTo Combat' ,
        r'SpeakTo Normal',
        r'SpeakTo Sneaking',
        r'SpeakTo Shadowheart',
        r'MoveTo Combat',
        r'MoveTo Normal',
        r'MoveTo Sneaking',
        r'MoveTo Shadowheart',
        r'HirelingName',
        r'IE_ToggleInventory',
        r'IE_PanelSelect',
        r'IE_ContextMenu',
        r'IE_ToggleSpells',
        r'IE_PartyManagement',
        r'IE_',
        r'GEN_CheckMagicPocketGold',
        r'GEN_PlayerName',
        r'SpellSlot',
        r'Tooltip'
    ]

    
    # Compile regex patterns
    compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in workkey_patterns]
    
    workkey_entries = []
    total_lines = 0
    
    print("Đang đọc file XML...", flush=True)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            total_lines = len(lines)
            
        print(f"Tổng số dòng: {total_lines}", flush=True)
        print("Đang tìm kiếm workkeys...", flush=True)
        
        for line_num, line in enumerate(lines, 1):
            # Check if line contains any workkey pattern
            for pattern in compiled_patterns:
                if pattern.search(line):
                    # Extract the content element
                    if '<content contentuid=' in line:
                        workkey_entries.append({
                            'line_number': line_num,
                            'content': line.strip(),
                            'pattern_found': pattern.pattern
                        })
                        break
            
            # Progress indicator
            if line_num % 10000 == 0:
                print(f"Đã xử lý: {line_num}/{total_lines} dòng", flush=True)
    
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}", flush=True)
        return
    
    print(f"\nTìm thấy {len(workkey_entries)} entries chứa workkeys", flush=True)
    
    # Create XML structure for workkey entries
    if workkey_entries:
        print("Đang tạo file XML cho workkeys...", flush=True)
        
        # Create XML content
        xml_content = ['<?xml version="1.0" encoding="utf-8"?>']
        xml_content.append('<!-- Extracted Workkeys from BG3 English.xml -->')
        xml_content.append(f'<!-- Extracted on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} -->')
        xml_content.append(f'<!-- Total entries found: {len(workkey_entries)} -->')
        xml_content.append('<contentList>')
        
        # Group by pattern for better organization
        pattern_groups = {}
        for entry in workkey_entries:
            pattern = entry['pattern_found']
            if pattern not in pattern_groups:
                pattern_groups[pattern] = []
            pattern_groups[pattern].append(entry)
        
        # Add entries grouped by pattern
        for pattern, entries in pattern_groups.items():
            xml_content.append(f'\t<!-- Pattern: {pattern} - {len(entries)} entries -->')
            for entry in entries:
                # Extract just the content element
                content_line = entry['content']
                if content_line.startswith('\t'):
                    xml_content.append(content_line)
                else:
                    xml_content.append(f'\t{content_line}')
            xml_content.append('')
        
        xml_content.append('</contentList>')
        
        # Write to output file
        try:
            # Ensure the output filename is valid for Windows
            invalid_chars = '<>:"|?*'
            clean_filename = output_filename
            for char in invalid_chars:
                clean_filename = clean_filename.replace(char, '_')
            
            # Recreate the full output path with cleaned filename
            clean_output_file = os.path.join(output_dir, clean_filename)
            
            with open(clean_output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(xml_content))
            
            print(f"✅ Đã tạo file: {clean_output_file}", flush=True)
            print(f"📊 Thống kê:", flush=True)
            for pattern, entries in pattern_groups.items():
                print(f"   - {pattern}: {len(entries)} entries", flush=True)
                
        except Exception as e:
            print(f"❌ Lỗi khi ghi file: {e}", flush=True)
    
    else:
        print("❌ Không tìm thấy workkeys nào!", flush=True)

if __name__ == "__main__":
    # Set UTF-8 encoding for console
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    
    print("🔍 BG3 Workkeys Extractor", flush=True)
    print("=" * 50, flush=True)
    
    # Check if running with command line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1].strip().strip('"')
        print(f"Sử dụng file từ command line: {input_file}", flush=True)
        
        # Auto-generate output filename for command line mode
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_filename = f"workkeys_extracted_{base_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
        print(f"Tự động tạo tên file output: {output_filename}", flush=True)
        
    else:
        # Get input file path from user
        print("\n📁 Nhập đường dẫn file English.xml (Enter để dùng mặc định):", flush=True)
        try:
            input_file = input("Input file: ").strip().strip('"')
        except (EOFError, KeyboardInterrupt):
            input_file = ""
        
        if not input_file:
            # Default path if no input
            input_file = r"d:\Games\Baldurt's Gate VH\baldurts-gate-3\data\wip\Package English Path8_4.116897358\english.xml"
            print(f"Sử dụng đường dẫn mặc định: {input_file}", flush=True)
    
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"❌ Không tìm thấy file: {input_file}", flush=True)
            print("Nhấn Enter để thoát...", flush=True)
            try:
                input()
            except:
                pass
            sys.exit(1)
    
        # Get output file path from user
        print("\n💾 Nhập tên file output (Enter để tạo tên tự động):", flush=True)
        try:
            output_filename = input("Output filename: ").strip().strip('"')
        except (EOFError, KeyboardInterrupt):
            output_filename = ""
        
        if not output_filename:
            # Generate default output filename based on input
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_filename = f"workkeys_extracted_{base_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"
            print(f"Sử dụng tên file: {output_filename}", flush=True)
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Không tìm thấy file: {input_file}", flush=True)
        if len(sys.argv) <= 1:  # Only wait for input in interactive mode
            print("Nhấn Enter để thoát...", flush=True)
            try:
                input()
            except:
                pass
        sys.exit(1)
    
    # Ensure output directory exists
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output", "filtered")
    os.makedirs(output_dir, exist_ok=True)
    
    # Full path to output file
    output_file = os.path.join(output_dir, output_filename)
    
    print(f"\n📂 Input:  {input_file}", flush=True)
    print(f"📄 Output: {output_file}", flush=True)
    print("\nBắt đầu xử lý...", flush=True)
    
    extract_workkeys_from_xml(input_file, output_file)
    
    print("\n✨ Hoàn thành!", flush=True)
    if len(sys.argv) <= 1:  # Only wait for input in interactive mode
        print("Nhấn Enter để thoát...", flush=True)
        try:
            input()
        except:
            pass
