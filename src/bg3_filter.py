#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BG3 Enhanced Filter Tool
Công cụ lọc nâng cao cho Baldur's Gate 3 XML files
Bao gồm: UI Text Filter, English Filter, Context Filter, và GUI
"""

import xml.etree.ElementTree as ET
import re
import os
import sys
import logging
import html
import argparse
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
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

# Import các class từ hai file gốc
from bg3_filter_enhanced import BG3EnhancedFilter
from bg3_filter_enhanced_gui import BG3FilterGUI

def show_gui():
    """Khởi chạy giao diện đồ họa"""
    root = tk.Tk()
    app = BG3FilterGUI(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

def main():
    """Hàm main chính"""
    parser = argparse.ArgumentParser(
        description="BG3 Enhanced Filter Tool - Công cụ lọc nâng cao cho Baldur's Gate 3",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--gui', action='store_true', help='Chạy với giao diện đồ họa')
    parser.add_argument('--cli', action='store_true', help='Chạy với giao diện dòng lệnh')
    
    args = parser.parse_args()
    
    # Mặc định chạy GUI nếu không có tham số
    if not (args.gui or args.cli):
        args.gui = True
    
    if args.gui:
        show_gui()
    else:
        # Import và chạy CLI
        from bg3_filter_enhanced import create_cli_parser, main as cli_main
        sys.exit(cli_main())

if __name__ == "__main__":
    main()
