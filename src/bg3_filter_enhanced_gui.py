#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BG3 Enhanced Filter GUI Application
Ứng dụng GUI cho BG3 Enhanced Filter với hướng dẫn trực quan
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import json
import threading
from datetime import datetime
from pathlib import Path
import subprocess

class BG3FilterGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.create_interface()
        self.load_settings()
        
    def setup_window(self):
        """Thiết lập cửa sổ chính"""
        self.root.title("BG3 Enhanced Filter - Công cụ lọc nâng cao v2.0")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2b2b2b")
        
        # Icon và style
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
            
        # Style
        self.setup_styles()
        
    def setup_styles(self):
        """Thiết lập theme và styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colors
        bg_color = "#2b2b2b"
        fg_color = "#ffffff"
        accent_color = "#4CAF50"
        button_color = "#3f3f3f"
        
        # Configure styles
        style.configure('Title.TLabel', 
                       background=bg_color, 
                       foreground=accent_color, 
                       font=('Arial', 16, 'bold'))
        
        style.configure('Header.TLabel', 
                       background=bg_color, 
                       foreground=fg_color, 
                       font=('Arial', 12, 'bold'))
        
        style.configure('Custom.TButton',
                       background=button_color,
                       foreground=fg_color,
                       font=('Arial', 10))
        
        style.configure('Success.TButton',
                       background=accent_color,
                       foreground=fg_color,
                       font=('Arial', 10, 'bold'))
        
    def setup_variables(self):
        """Thiết lập biến"""
        self.input_file = tk.StringVar()
        self.output_dir = tk.StringVar(value="output/filtered")
        self.current_filter = tk.StringVar(value="ui_text")
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Sẵn sàng")
        
        # Filter options
        self.filter_options = {
            'ui_text': tk.BooleanVar(value=True),
            'english_only': tk.BooleanVar(),
            'non_english': tk.BooleanVar(),
            'dialogue': tk.BooleanVar(),
            'technical': tk.BooleanVar(),
            'context': tk.BooleanVar(),
            'analyze_only': tk.BooleanVar()
        }
        
    def create_interface(self):
        """Tạo giao diện chính"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(title_frame, text="🎮 BG3 Enhanced Filter", style='Title.TLabel').pack(side=tk.LEFT)
        ttk.Label(title_frame, text="v2.0", style='Header.TLabel').pack(side=tk.RIGHT)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_filter_tab()
        self.create_guide_tab()
        self.create_examples_tab()
        self.create_settings_tab()
        self.create_log_tab()
        
        # Status bar
        self.create_status_bar(main_frame)
        
    def create_filter_tab(self):
        """Tab lọc chính"""
        filter_frame = ttk.Frame(self.notebook)
        self.notebook.add(filter_frame, text="🔍 Lọc File")
        
        # File selection section
        file_section = ttk.LabelFrame(filter_frame, text="📁 Chọn File XML")
        file_section.pack(fill=tk.X, padx=10, pady=5)
        
        file_frame = ttk.Frame(file_section)
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(file_frame, text="File XML:").pack(side=tk.LEFT)
        ttk.Entry(file_frame, textvariable=self.input_file, width=60).pack(side=tk.LEFT, padx=(10, 5))
        ttk.Button(file_frame, text="Chọn File", command=self.select_input_file).pack(side=tk.LEFT)
        
        # Output directory
        output_frame = ttk.Frame(file_section)
        output_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Label(output_frame, text="Thư mục đầu ra:").pack(side=tk.LEFT)
        ttk.Entry(output_frame, textvariable=self.output_dir, width=50).pack(side=tk.LEFT, padx=(10, 5))
        ttk.Button(output_frame, text="Chọn", command=self.select_output_dir).pack(side=tk.LEFT)
        
        # Filter options section
        filter_section = ttk.LabelFrame(filter_frame, text="⚙️ Tùy chọn lọc")
        filter_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create filter options grid
        options_frame = ttk.Frame(filter_section)
        options_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left column
        left_col = ttk.Frame(options_frame)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_filter_option(left_col, 'ui_text', "🎨 UI Text Filter", 
                                 "Tách giao diện người dùng")
        self.create_filter_option(left_col, 'english_only', "🔤 English Only", 
                                 "Chỉ giữ lại text tiếng Anh")
        self.create_filter_option(left_col, 'non_english', "🌍 Non-English", 
                                 "Loại bỏ text tiếng Anh")
        self.create_filter_option(left_col, 'dialogue', "💬 Dialogue Filter", 
                                 "Tách đối thoại trong game")
        
        # Right column
        right_col = ttk.Frame(options_frame)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        self.create_filter_option(right_col, 'technical', "⚙️ Technical Filter", 
                                 "Tách text kỹ thuật")
        self.create_filter_option(right_col, 'context', "📝 Context Filter", 
                                 "Phân loại theo nội dung")
        self.create_filter_option(right_col, 'analyze_only', "📊 Analyze Only", 
                                 "Chỉ phân tích không tạo file")
        
        # Action buttons
        action_frame = ttk.Frame(filter_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="🚀 Bắt đầu lọc", 
                  command=self.start_filtering, style='Success.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="🔍 Xem trước", 
                  command=self.preview_filter).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="📂 Mở thư mục kết quả", 
                  command=self.open_output_folder).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="🔄 Reset", 
                  command=self.reset_filters).pack(side=tk.RIGHT)
        
        # Progress bar
        progress_frame = ttk.Frame(filter_frame)
        progress_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.progress_label = ttk.Label(progress_frame, text="0%")
        self.progress_label.pack(side=tk.RIGHT, padx=(10, 0))
        
    def create_filter_option(self, parent, key, title, description):
        """Tạo option cho filter"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        
        cb = ttk.Checkbutton(frame, text=title, variable=self.filter_options[key])
        cb.pack(anchor=tk.W)
        
        desc_label = ttk.Label(frame, text=description, font=('Arial', 9), foreground='gray')
        desc_label.pack(anchor=tk.W, padx=(20, 0))
        
    def create_guide_tab(self):
        """Tab hướng dẫn"""
        guide_frame = ttk.Frame(self.notebook)
        self.notebook.add(guide_frame, text="📖 Hướng dẫn")
        
        # Scroll frame for guide
        canvas = tk.Canvas(guide_frame, bg="#2b2b2b")
        scrollbar = ttk.Scrollbar(guide_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Guide content
        self.create_guide_content(scrollable_frame)
        
    def create_guide_content(self, parent):
        """Tạo nội dung hướng dẫn"""
        # Title
        title_frame = ttk.Frame(parent)
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Label(title_frame, text="📖 Hướng dẫn sử dụng BG3 Enhanced Filter", 
                 style='Title.TLabel').pack()
        
        # Filter descriptions
        filters_info = [
            {
                'title': '🎨 UI Text Filter',
                'description': 'Tách các text giao diện người dùng',
                'features': [
                    '• Lọc button, menu, tooltip',
                    '• Phát hiện tag LSTag',
                    '• Text ngắn (<200 ký tự)',
                    '• Keyword UI patterns'
                ],
                'example': 'Ví dụ: "Health", "Inventory", "Save Game"'
            },
            {
                'title': '🔤 English Only Filter',
                'description': 'Chỉ giữ lại text hoàn toàn bằng tiếng Anh',
                'features': [
                    '• Loại bỏ text có ký tự đặc biệt',
                    '• Giữ text ASCII chuẩn',
                    '• Bảo vệ system markers',
                    '• Kiểm tra ký tự alphabet'
                ],
                'example': 'Giữ: "Hello World" | Loại: "Xin chào"'
            },
            {
                'title': '🌍 Non-English Filter',
                'description': 'Loại bỏ text tiếng Anh, giữ lại text khác',
                'features': [
                    '• Phát hiện text đã dịch',
                    '• Giữ ký tự Unicode',
                    '• Lọc text hỗn hợp',
                    '• Bảo vệ markup'
                ],
                'example': 'Giữ: "Xin chào" | Loại: "Hello World"'
            },
            {
                'title': '💬 Dialogue Filter',
                'description': 'Tách đối thoại và narration',
                'features': [
                    '• Phát hiện dialogue patterns',
                    '• Tách narrator text',
                    '• Character speech',
                    '• Story elements'
                ],
                'example': 'Ví dụ: "Hello there, traveler!"'
            },
            {
                'title': '⚙️ Technical Filter',
                'description': 'Tách text kỹ thuật và debug',
                'features': [
                    '• System messages',
                    '• Debug information',
                    '• Error messages',
                    '• Technical terms'
                ],
                'example': 'Ví dụ: "ERROR_CODE_001", "DEBUG_MODE"'
            },
            {
                'title': '📝 Context Filter',
                'description': 'Phân loại theo ngữ cảnh',
                'features': [
                    '• Combat context',
                    '• Menu context', 
                    '• Inventory context',
                    '• Quest context',
                    '• Character context'
                ],
                'example': 'Phân loại: Combat, Menu, Quest, etc.'
            }
        ]
        
        for filter_info in filters_info:
            self.create_filter_guide_section(parent, filter_info)
            
    def create_filter_guide_section(self, parent, filter_info):
        """Tạo section hướng dẫn cho từng filter"""
        section_frame = ttk.LabelFrame(parent, text=filter_info['title'])
        section_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Description
        desc_label = ttk.Label(section_frame, text=filter_info['description'], 
                              font=('Arial', 11, 'bold'))
        desc_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        # Features
        features_frame = ttk.Frame(section_frame)
        features_frame.pack(fill=tk.X, padx=15, pady=5)
        
        ttk.Label(features_frame, text="Tính năng:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        for feature in filter_info['features']:
            ttk.Label(features_frame, text=feature, font=('Arial', 9)).pack(anchor=tk.W, padx=(10, 0))
            
        # Example
        if 'example' in filter_info:
            example_frame = ttk.Frame(section_frame)
            example_frame.pack(fill=tk.X, padx=15, pady=(5, 15))
            
            ttk.Label(example_frame, text="Ví dụ:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
            ttk.Label(example_frame, text=filter_info['example'], 
                     font=('Arial', 9, 'italic'), foreground='blue').pack(anchor=tk.W, padx=(10, 0))
        
    def create_examples_tab(self):
        """Tab ví dụ thực tế"""
        examples_frame = ttk.Frame(self.notebook)
        self.notebook.add(examples_frame, text="💡 Ví dụ")
        
        # Examples notebook
        examples_notebook = ttk.Notebook(examples_frame)
        examples_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create example tabs
        self.create_ui_examples_tab(examples_notebook)
        self.create_dialogue_examples_tab(examples_notebook) 
        self.create_context_examples_tab(examples_notebook)
        self.create_workflow_examples_tab(examples_notebook)
        
    def create_ui_examples_tab(self, parent):
        """Tab ví dụ UI Filter"""
        ui_frame = ttk.Frame(parent)
        parent.add(ui_frame, text="🎨 UI Examples")
        
        # Create scrolled text
        text_widget = scrolledtext.ScrolledText(ui_frame, wrap=tk.WORD, height=25)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ui_examples = """
🎨 UI TEXT FILTER - VÍ DỤ THỰC TẾ

═══════════════════════════════════════════════════════════════

📌 1. BUTTON VÀ MENU

Input XML:
<content contentuid="h123">Save Game</content>
<content contentuid="h124">Load Game</content> 
<content contentuid="h125">Options</content>
<content contentuid="h126">Exit</content>

➤ Kết quả: Tất cả được lọc vào ui_text.xml

═══════════════════════════════════════════════════════════════

📌 2. TOOLTIP VÀ HINT

Input XML:
<content contentuid="h200"><LSTag Tooltip="MovementSpeed">Movement Speed</LSTag>: [1]/[2]</content>
<content contentuid="h201">Press [E] to interact</content>
<content contentuid="h202">Hold [Shift] to run</content>

➤ Kết quả: Phát hiện LSTag và control hints → ui_text.xml

═══════════════════════════════════════════════════════════════

📌 3. STATUS VÀ INDICATOR

Input XML:
<content contentuid="h300">Health: 100/100</content>
<content contentuid="h301">Mana: 50/80</content>
<content contentuid="h302">Level Up!</content>
<content contentuid="h303">Quest Complete</content>

➤ Kết quả: Status indicators và notifications → ui_text.xml

═══════════════════════════════════════════════════════════════

📌 4. ERROR VÀ WARNING

Input XML:
<content contentuid="h400">File not found</content>
<content contentuid="h401">Connection lost</content>
<content contentuid="h402">Invalid input</content>

➤ Kết quả: System messages → ui_text.xml

═══════════════════════════════════════════════════════════════

📌 5. KHÔNG PHẢI UI TEXT

Input XML:
<content contentuid="h500">Once upon a time, in a distant land, there lived a brave adventurer who sought to save the world from an ancient evil that threatened all living beings.</content>

➤ Kết quả: Quá dài (>200 chars) → KHÔNG lọc vào ui_text.xml

═══════════════════════════════════════════════════════════════

🔧 CẤU HÌNH UI FILTER

Max length: 200 characters
UI keywords: Save, Load, Options, Menu, Button, etc.
LSTag detection: Automatic
Short text priority: <50 chars
        """
        
        text_widget.insert(tk.END, ui_examples)
        text_widget.config(state=tk.DISABLED)
        
    def create_dialogue_examples_tab(self, parent):
        """Tab ví dụ Dialogue Filter"""
        dialogue_frame = ttk.Frame(parent)
        parent.add(dialogue_frame, text="💬 Dialogue Examples")
        
        text_widget = scrolledtext.ScrolledText(dialogue_frame, wrap=tk.WORD, height=25)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        dialogue_examples = """
💬 DIALOGUE FILTER - VÍ DỤ THỰC TẾ

═══════════════════════════════════════════════════════════════

📌 1. CHARACTER SPEECH

Input XML:
<content contentuid="h600">"Hello there, traveler! What brings you to our village?"</content>
<content contentuid="h601">"I'm looking for the ancient temple. Have you seen it?"</content>
<content contentuid="h602">"Ah yes, it's just beyond the forest. But beware of the dangers!"</content>

➤ Kết quả: Direct speech → dialogue.xml

═══════════════════════════════════════════════════════════════

📌 2. NARRATOR TEXT

Input XML:
<content contentuid="h700">The wind howls through the abandoned ruins.</content>
<content contentuid="h701">You hear footsteps approaching from behind.</content>
<content contentuid="h702">A mysterious figure emerges from the shadows.</content>

➤ Kết quả: Narrative descriptions → dialogue.xml

═══════════════════════════════════════════════════════════════

📌 3. THOUGHT VÀ INNER MONOLOGUE

Input XML:
<content contentuid="h800">*This place gives me the creeps...*</content>
<content contentuid="h801">(I should be more careful here.)</content>
<content contentuid="h802">Something doesn't feel right about this.</content>

➤ Kết quả: Internal thoughts → dialogue.xml

═══════════════════════════════════════════════════════════════

📌 4. ACTION DESCRIPTIONS

Input XML:
<content contentuid="h900">*Draws sword cautiously*</content>
<content contentuid="h901">*Looks around nervously*</content>
<content contentuid="h902">*Casts a protective spell*</content>

➤ Kết quả: Action descriptions → dialogue.xml

═══════════════════════════════════════════════════════════════

📌 5. KHÔNG PHẢI DIALOGUE

Input XML:
<content contentuid="h950">Inventory</content>
<content contentuid="h951">Health Potion</content>
<content contentuid="h952">+5 Attack</content>

➤ Kết quả: UI elements → KHÔNG vào dialogue.xml

═══════════════════════════════════════════════════════════════

🔧 CẤU HÌNH DIALOGUE FILTER

Min length: 10 characters
Max length: 500 characters
Patterns: Quotes, parentheses, narrative markers
Context: Conversation, story, narration
        """
        
        text_widget.insert(tk.END, dialogue_examples)
        text_widget.config(state=tk.DISABLED)
        
    def create_context_examples_tab(self, parent):
        """Tab ví dụ Context Filter"""
        context_frame = ttk.Frame(parent)
        parent.add(context_frame, text="📝 Context Examples")
        
        text_widget = scrolledtext.ScrolledText(context_frame, wrap=tk.WORD, height=25)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        context_examples = """
📝 CONTEXT FILTER - VÍ DỤ PHÂN LOẠI

═══════════════════════════════════════════════════════════════

🗡️ COMBAT CONTEXT

Input XML:
<content contentuid="h1000">Attack of Opportunity</content>
<content contentuid="h1001">Critical Hit!</content>
<content contentuid="h1002">You take 15 damage</content>
<content contentuid="h1003">Spell Resistance</content>

➤ Kết quả: by_context/combat.xml

Keywords: attack, damage, spell, critical, hit, combat, fight, weapon

═══════════════════════════════════════════════════════════════

📦 INVENTORY CONTEXT

Input XML:
<content contentuid="h1100">Leather Armor</content>
<content contentuid="h1101">Health Potion</content>
<content contentuid="h1102">Weight: 2.5 kg</content>
<content contentuid="h1103">Rarity: Common</content>

➤ Kết quả: by_context/inventory.xml

Keywords: armor, potion, weight, item, equipment, inventory

═══════════════════════════════════════════════════════════════

📋 MENU CONTEXT

Input XML:
<content contentuid="h1200">Main Menu</content>
<content contentuid="h1201">Settings</content>
<content contentuid="h1202">Video Options</content>
<content contentuid="h1203">Key Bindings</content>

➤ Kết quả: by_context/menu.xml

Keywords: menu, options, settings, configure, preferences

═══════════════════════════════════════════════════════════════

🗂️ QUEST CONTEXT

Input XML:
<content contentuid="h1300">Find the Lost Artifact</content>
<content contentuid="h1301">Quest Complete</content>
<content contentuid="h1302">Objective: Talk to the Elder</content>
<content contentuid="h1303">Reward: 500 Gold</content>

➤ Kết quả: by_context/quest.xml

Keywords: quest, objective, reward, complete, mission, task

═══════════════════════════════════════════════════════════════

👤 CHARACTER CONTEXT

Input XML:
<content contentuid="h1400">Astarion</content>
<content contentuid="h1401">Level 5 Rogue</content>
<content contentuid="h1402">Strength: 12</content>
<content contentuid="h1403">Background: Noble</content>

➤ Kết quả: by_context/character.xml

Keywords: level, strength, rogue, background, character, class

═══════════════════════════════════════════════════════════════

🔧 CẤU HÌNH CONTEXT FILTER

Categories: combat, inventory, menu, quest, character
Multi-context: Một text có thể thuộc nhiều context
Priority: Thứ tự ưu tiên khi phân loại
Threshold: Số lượng keyword tối thiểu
        """
        
        text_widget.insert(tk.END, context_examples)
        text_widget.config(state=tk.DISABLED)
        
    def create_workflow_examples_tab(self, parent):
        """Tab ví dụ workflow"""
        workflow_frame = ttk.Frame(parent)
        parent.add(workflow_frame, text="🔄 Workflow")
        
        text_widget = scrolledtext.ScrolledText(workflow_frame, wrap=tk.WORD, height=25)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        workflow_examples = """
🔄 WORKFLOW VÀ QUY TRÌNH SỬ DỤNG

═══════════════════════════════════════════════════════════════

📋 1. QUY TRÌNH CƠ BẢN

Bước 1: Chọn file XML input
├── File english.xml từ game BG3
├── Hoặc file đã gộp từ nhiều nguồn
└── Đảm bảo format XML hợp lệ

Bước 2: Chọn loại filter
├── UI Text: Cho translator UI
├── Dialogue: Cho translator nội dung
├── Context: Để phân chia công việc
└── Analyze Only: Để kiểm tra trước

Bước 3: Thiết lập output
├── Chọn thư mục đầu ra
├── Kiểm tra quyền ghi
└── Đảm bảo đủ dung lượng

Bước 4: Chạy filter và kiểm tra kết quả

═══════════════════════════════════════════════════════════════

🎯 2. CÁC TRƯỜNG HỢP SỬ DỤNG THỰC TẾ

🔸 Trường hợp 1: Dịch UI đầu tiên
├── Chọn: UI Text Filter
├── Kết quả: ui_text.xml (khoảng 60k entries)
├── Translator tập trung vào menu, button, tooltip
└── Ưu tiên: Text ngắn, quan trọng

🔸 Trường hợp 2: Dịch nội dung game
├── Chọn: Dialogue Filter
├── Kết quả: dialogue.xml (khoảng 75k entries)  
├── Translator tập trung vào câu chuyện
└── Ưu tiên: Đối thoại, narration

🔸 Trường hợp 3: Chia việc theo team
├── Chọn: Context Filter
├── Kết quả: combat.xml, quest.xml, character.xml
├── Mỗi team nhận một loại context
└── Tránh xung đột, dễ quản lý

🔸 Trường hợp 4: Kiểm tra file lớn
├── Chọn: Analyze Only
├── Kết quả: Báo cáo thống kê (JSON)
├── Xem trước mà không tạo file
└── Quyết định chiến lược filter

═══════════════════════════════════════════════════════════════

⚙️ 3. TIPS VÀ TRICKS

💡 Tip 1: Combine Filters
├── English Only + UI Text → Chỉ UI tiếng Anh
├── Non-English + Dialogue → Dialogue đã dịch
└── Context + UI → UI theo từng loại

💡 Tip 2: Analyze First
├── Luôn chạy Analyze Only trước
├── Xem distribution và sample
├── Quyết định filter phù hợp
└── Tránh lãng phí thời gian

💡 Tip 3: Batch Processing
├── Xử lý nhiều file cùng lúc
├── Sử dụng script automation
├── Thiết lập config template
└── Tiết kiệm thời gian

💡 Tip 4: Quality Check
├── Kiểm tra filter_report.txt
├── Verify sample entries
├── So sánh với mong đợi
└── Adjust config nếu cần

═══════════════════════════════════════════════════════════════

📊 4. HIỂU KẾT QUẢ

📁 Cấu trúc output:
output/filtered/[filename]/
├── ui_text.xml           # UI elements
├── english_only.xml      # English text only
├── non_english.xml       # Non-English text
├── dialogue.xml          # Dialogues & narration
├── technical.xml         # Technical text
├── by_context/           # Context-based
│   ├── combat.xml
│   ├── menu.xml
│   ├── inventory.xml
│   ├── quest.xml
│   └── character.xml
└── filter_report.txt     # Detailed report

📈 Metrics trong report:
├── Total entries processed
├── Each filter count
├── Processing time
├── Sample entries
└── Distribution statistics
        """
        
        text_widget.insert(tk.END, workflow_examples)
        text_widget.config(state=tk.DISABLED)
        
    def create_settings_tab(self):
        """Tab cài đặt"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Cài đặt")
        
        # Filter settings
        filter_settings_frame = ttk.LabelFrame(settings_frame, text="🔧 Cài đặt Filter")
        filter_settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # UI Filter settings
        ui_frame = ttk.LabelFrame(filter_settings_frame, text="UI Text Filter")
        ui_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(ui_frame, text="Max length:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.ui_max_length = tk.StringVar(value="200")
        ttk.Entry(ui_frame, textvariable=self.ui_max_length, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(ui_frame, text="Short text threshold:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.ui_short_threshold = tk.StringVar(value="50")
        ttk.Entry(ui_frame, textvariable=self.ui_short_threshold, width=10).grid(row=0, column=3, padx=5)
        
        # Dialogue Filter settings
        dialogue_frame = ttk.LabelFrame(filter_settings_frame, text="Dialogue Filter")
        dialogue_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(dialogue_frame, text="Min length:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.dialogue_min_length = tk.StringVar(value="10")
        ttk.Entry(dialogue_frame, textvariable=self.dialogue_min_length, width=10).grid(row=0, column=1, padx=5)
        
        ttk.Label(dialogue_frame, text="Max length:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.dialogue_max_length = tk.StringVar(value="500")
        ttk.Entry(dialogue_frame, textvariable=self.dialogue_max_length, width=10).grid(row=0, column=3, padx=5)
        
        # Output settings
        output_settings_frame = ttk.LabelFrame(settings_frame, text="📁 Cài đặt Output")
        output_settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_subfolders = tk.BooleanVar(value=True)
        ttk.Checkbutton(output_settings_frame, text="Tạo thư mục con cho từng loại filter", 
                       variable=self.create_subfolders).pack(anchor=tk.W, padx=10, pady=5)
        
        self.backup_original = tk.BooleanVar(value=False)
        ttk.Checkbutton(output_settings_frame, text="Backup file gốc", 
                       variable=self.backup_original).pack(anchor=tk.W, padx=10, pady=5)
        
        self.verbose_logging = tk.BooleanVar(value=True)
        ttk.Checkbutton(output_settings_frame, text="Logging chi tiết", 
                       variable=self.verbose_logging).pack(anchor=tk.W, padx=10, pady=5)
        
        # Buttons
        buttons_frame = ttk.Frame(settings_frame)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(buttons_frame, text="💾 Lưu cài đặt", 
                  command=self.save_settings).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="🔄 Reset về mặc định", 
                  command=self.reset_settings).pack(side=tk.LEFT)
        ttk.Button(buttons_frame, text="📂 Mở file config", 
                  command=self.open_config_file).pack(side=tk.RIGHT)
        
    def create_log_tab(self):
        """Tab log"""
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text="📋 Log")
        
        # Log controls
        log_controls = ttk.Frame(log_frame)
        log_controls.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(log_controls, text="🔄 Làm mới", 
                  command=self.refresh_log).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(log_controls, text="🗑️ Xóa log", 
                  command=self.clear_log).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(log_controls, text="💾 Lưu log", 
                  command=self.save_log).pack(side=tk.LEFT)
        
        # Log display
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=25, 
                                                 font=('Consolas', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        
        # Load initial log
        self.refresh_log()
        
    def create_status_bar(self, parent):
        """Tạo status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Status label
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Clock
        self.clock_label = ttk.Label(status_frame, text="")
        self.clock_label.pack(side=tk.RIGHT, padx=5)
        
        # Update clock
        self.update_clock()
        
    def update_clock(self):
        """Cập nhật đồng hồ"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)
        
    # Event handlers
    def select_input_file(self):
        """Chọn file input"""
        file_path = filedialog.askopenfilename(
            title="Chọn file XML",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
        )
        if file_path:
            self.input_file.set(file_path)
            self.update_status(f"Đã chọn file: {os.path.basename(file_path)}")
            
    def select_output_dir(self):
        """Chọn thư mục output"""
        dir_path = filedialog.askdirectory(title="Chọn thư mục đầu ra")
        if dir_path:
            self.output_dir.set(dir_path)
            self.update_status(f"Thư mục đầu ra: {dir_path}")
            
    def start_filtering(self):
        """Bắt đầu quá trình lọc"""
        if not self.input_file.get():
            messagebox.showerror("Lỗi", "Vui lòng chọn file XML input!")
            return
            
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("Lỗi", "File input không tồn tại!")
            return
            
        # Check if any filter is selected
        if not any(var.get() for var in self.filter_options.values()):
            messagebox.showerror("Lỗi", "Vui lòng chọn ít nhất một loại filter!")
            return
            
        # Confirm start
        if messagebox.askyesno("Xác nhận", "Bắt đầu quá trình lọc?"):
            # Start filtering in separate thread
            threading.Thread(target=self.run_filter, daemon=True).start()
            
    def run_filter(self):
        """Chạy filter trong thread riêng"""
        try:
            self.update_status("Đang chuẩn bị...")
            self.progress_var.set(0)
            
            # Build command
            cmd = [sys.executable, "src/bg3_filter_enhanced.py", self.input_file.get()]
            
            # Add filter options
            if self.filter_options['ui_text'].get():
                cmd.append("--ui-text")
            if self.filter_options['english_only'].get():
                cmd.append("--english-only")
            if self.filter_options['non_english'].get():
                cmd.append("--non-english")
            if self.filter_options['dialogue'].get():
                cmd.append("--dialogue")
            if self.filter_options['technical'].get():
                cmd.append("--technical")
            if self.filter_options['context'].get():
                cmd.append("--by-context")
            if self.filter_options['analyze_only'].get():
                cmd.append("--analyze-only")
                
            cmd.extend(["--output-dir", self.output_dir.get()])
            cmd.append("--verbose")
            
            self.update_status("Đang chạy filter...")
            self.progress_var.set(25)
            
            # Run command
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            self.progress_var.set(75)
            
            if result.returncode == 0:
                self.progress_var.set(100)
                self.update_status("Hoàn thành!")
                messagebox.showinfo("Thành công", "Đã hoàn thành quá trình lọc!")
                self.refresh_log()
            else:
                self.update_status("Có lỗi xảy ra!")
                messagebox.showerror("Lỗi", f"Có lỗi trong quá trình lọc:\n{result.stderr}")
                
        except Exception as e:
            self.update_status("Lỗi nghiêm trọng!")
            messagebox.showerror("Lỗi", f"Lỗi nghiêm trọng: {str(e)}")
            
    def preview_filter(self):
        """Xem trước kết quả filter"""
        if not self.input_file.get():
            messagebox.showerror("Lỗi", "Vui lòng chọn file XML input!")
            return
            
        # Run analyze only
        try:
            cmd = [sys.executable, "src/bg3_filter_enhanced.py", 
                   self.input_file.get(), "--analyze-only"]
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                # Show analysis result
                self.show_analysis_result()
            else:
                messagebox.showerror("Lỗi", f"Không thể phân tích file:\n{result.stderr}")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xem trước: {str(e)}")
            
    def show_analysis_result(self):
        """Hiển thị kết quả phân tích"""
        try:
            # Load analysis result
            analysis_file = "src/english_analysis.json"
            if os.path.exists(analysis_file):
                with open(analysis_file, 'r', encoding='utf-8') as f:
                    analysis = json.load(f)
                    
                # Create preview window
                preview_window = tk.Toplevel(self.root)
                preview_window.title("🔍 Kết quả phân tích")
                preview_window.geometry("800x600")
                preview_window.configure(bg="#2b2b2b")
                
                # Create text widget
                text_widget = scrolledtext.ScrolledText(preview_window, wrap=tk.WORD, font=('Consolas', 10))
                text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                # Format analysis result
                result_text = self.format_analysis_result(analysis)
                text_widget.insert(tk.END, result_text)
                text_widget.config(state=tk.DISABLED)
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể hiển thị kết quả: {str(e)}")
            
    def format_analysis_result(self, analysis):
        """Format kết quả phân tích"""
        text = "🔍 KẾT QUẢ PHÂN TÍCH FILE XML\n"
        text += "=" * 50 + "\n\n"
        
        text += f"📊 THỐNG KÊ TỔNG QUAN\n"
        text += f"Total entries: {analysis.get('total_entries', 0):,}\n"
        text += f"Empty entries: {analysis.get('empty_entries', 0):,}\n\n"
        
        text += f"🎨 UI CANDIDATES: {analysis.get('ui_candidates', 0):,}\n"
        text += f"🔤 English only: {analysis.get('english_only_candidates', 0):,}\n"
        text += f"💬 Dialogue: {analysis.get('dialogue_candidates', 0):,}\n"
        text += f"⚙️ Technical: {analysis.get('technical_candidates', 0):,}\n\n"
        
        if 'context_distribution' in analysis:
            text += f"📝 PHÂN BỐ CONTEXT\n"
            for context, count in analysis['context_distribution'].items():
                text += f"  {context}: {count:,}\n"
            text += "\n"
            
        if 'length_distribution' in analysis:
            text += f"📏 PHÂN BỐ ĐỘ DÀI\n"
            for length_cat, count in analysis['length_distribution'].items():
                text += f"  {length_cat}: {count:,}\n"
            text += "\n"
            
        # Add samples
        if 'sample_entries' in analysis:
            text += f"💡 VÍ DỤ ENTRIES\n"
            for category, samples in analysis['sample_entries'].items():
                text += f"\n📌 {category.upper()}:\n"
                for i, sample in enumerate(samples[:3], 1):
                    sample_text = sample.get('text', '')[:100]
                    if len(sample_text) == 100:
                        sample_text += "..."
                    text += f"  {i}. {sample_text}\n"
                    
        return text
        
    def open_output_folder(self):
        """Mở thư mục kết quả"""
        output_path = self.output_dir.get()
        if os.path.exists(output_path):
            os.startfile(output_path)
        else:
            messagebox.showwarning("Cảnh báo", "Thư mục output chưa tồn tại!")
            
    def reset_filters(self):
        """Reset tất cả filter options"""
        for var in self.filter_options.values():
            var.set(False)
        self.filter_options['ui_text'].set(True)
        self.update_status("Đã reset filter options")
        
    def refresh_log(self):
        """Làm mới log"""
        log_file = "src/bg3_filter_enhanced.log"
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                self.log_text.config(state=tk.NORMAL)
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(tk.END, content)
                self.log_text.config(state=tk.DISABLED)
                self.log_text.see(tk.END)
                
            except Exception as e:
                self.log_text.config(state=tk.NORMAL)
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(tk.END, f"Không thể đọc log file: {str(e)}")
                self.log_text.config(state=tk.DISABLED)
        else:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, "Log file không tồn tại")
            self.log_text.config(state=tk.DISABLED)
            
    def clear_log(self):
        """Xóa log"""
        if messagebox.askyesno("Xác nhận", "Xóa tất cả log?"):
            log_file = "src/bg3_filter_enhanced.log"
            try:
                if os.path.exists(log_file):
                    os.remove(log_file)
                self.refresh_log()
                self.update_status("Đã xóa log")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa log: {str(e)}")
                
    def save_log(self):
        """Lưu log"""
        file_path = filedialog.asksaveasfilename(
            title="Lưu log",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                content = self.log_text.get(1.0, tk.END)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.update_status(f"Đã lưu log: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu log: {str(e)}")
                
    def save_settings(self):
        """Lưu cài đặt"""
        try:
            settings = {
                "ui_filter": {
                    "max_length": int(self.ui_max_length.get()),
                    "short_text_threshold": int(self.ui_short_threshold.get())
                },
                "dialogue_filter": {
                    "min_length": int(self.dialogue_min_length.get()),
                    "max_length": int(self.dialogue_max_length.get())
                },
                "output_settings": {
                    "create_subfolders": self.create_subfolders.get(),
                    "backup_original": self.backup_original.get(),
                    "verbose_logging": self.verbose_logging.get()
                }
            }
            
            with open("src/filter_config.json", 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
                
            self.update_status("Đã lưu cài đặt")
            messagebox.showinfo("Thành công", "Đã lưu cài đặt!")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu cài đặt: {str(e)}")
            
    def reset_settings(self):
        """Reset cài đặt về mặc định"""
        if messagebox.askyesno("Xác nhận", "Reset tất cả cài đặt về mặc định?"):
            self.ui_max_length.set("200")
            self.ui_short_threshold.set("50")
            self.dialogue_min_length.set("10")
            self.dialogue_max_length.set("500")
            self.create_subfolders.set(True)
            self.backup_original.set(False)
            self.verbose_logging.set(True)
            self.update_status("Đã reset cài đặt")
            
    def open_config_file(self):
        """Mở file config"""
        config_file = "src/filter_config.json"
        if os.path.exists(config_file):
            try:
                os.startfile(config_file)
            except:
                messagebox.showinfo("Thông tin", f"Mở file: {config_file}")
        else:
            messagebox.showwarning("Cảnh báo", "File config không tồn tại!")
            
    def load_settings(self):
        """Load cài đặt từ file"""
        try:
            config_file = "src/filter_config.json"
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    
                # Load UI settings
                ui_settings = settings.get("ui_filter", {})
                self.ui_max_length.set(str(ui_settings.get("max_length", 200)))
                self.ui_short_threshold.set(str(ui_settings.get("short_text_threshold", 50)))
                
                # Load dialogue settings
                dialogue_settings = settings.get("dialogue_filter", {})
                self.dialogue_min_length.set(str(dialogue_settings.get("min_length", 10)))
                self.dialogue_max_length.set(str(dialogue_settings.get("max_length", 500)))
                
                # Load output settings
                output_settings = settings.get("output_settings", {})
                self.create_subfolders.set(output_settings.get("create_subfolders", True))
                self.backup_original.set(output_settings.get("backup_original", False))
                self.verbose_logging.set(output_settings.get("verbose_logging", True))
                
        except Exception as e:
            print(f"Không thể load cài đặt: {str(e)}")
            
    def update_status(self, message):
        """Cập nhật status"""
        self.status_var.set(message)
        self.root.update_idletasks()
        

def main():
    """Hàm main"""
    root = tk.Tk()
    app = BG3FilterGUI(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()
