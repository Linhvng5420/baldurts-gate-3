#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced XML Cleaner - Công cụ làm sạch file XML nâng cao
Xóa comment, dòng trống và tối ưu format XML
"""

import re
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

class XMLCleaner:
    def __init__(self, remove_comments=True, remove_empty_lines=True, 
                 preserve_indent=True, backup=True):
        """
        Khởi tạo XML Cleaner
        
        Args:
            remove_comments (bool): Xóa comment XML
            remove_empty_lines (bool): Xóa dòng trống
            preserve_indent (bool): Giữ nguyên indentation
            backup (bool): Tạo backup file gốc
        """
        self.remove_comments = remove_comments
        self.remove_empty_lines = remove_empty_lines
        self.preserve_indent = preserve_indent
        self.backup = backup
        
        # Thống kê
        self.stats = {
            'files_processed': 0,
            'files_success': 0,
            'files_failed': 0,
            'total_lines_removed': 0,
            'total_comments_removed': 0,
            'total_empty_lines_removed': 0
        }
    
    def create_backup(self, file_path):
        """Tạo backup file gốc"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{file_path}.backup_{timestamp}"
            
            with open(file_path, 'r', encoding='utf-8') as src:
                content = src.read()
            
            with open(backup_path, 'w', encoding='utf-8') as dst:
                dst.write(content)
            
            print(f"📦 Backup tạo tại: {backup_path}")
            return backup_path
            
        except Exception as e:
            print(f"⚠️  Không thể tạo backup: {str(e)}")
            return None
    
    def clean_xml_content(self, content):
        """
        Làm sạch nội dung XML
        
        Args:
            content (str): Nội dung XML gốc
            
        Returns:
            tuple: (cleaned_content, stats_dict)
        """
        original_lines = content.splitlines()
        original_line_count = len(original_lines)
        
        # Thống kê cho file này
        file_stats = {
            'comments_removed': 0,
            'empty_lines_removed': 0,
            'lines_removed': 0
        }
        
        # Xóa comment XML nếu được yêu cầu
        if self.remove_comments:
            # Đếm số comment trước khi xóa
            comment_matches = re.findall(r'<!--.*?-->', content, flags=re.DOTALL)
            file_stats['comments_removed'] = len(comment_matches)
            
            # Xóa comment
            content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        
        # Xử lý từng dòng
        lines = content.splitlines()
        cleaned_lines = []
        
        for line in lines:
            # Nếu xóa dòng trống
            if self.remove_empty_lines:
                # Bỏ qua dòng trống hoàn toàn
                if not line.strip():
                    file_stats['empty_lines_removed'] += 1
                    continue
            
            # Giữ nguyên indentation nếu được yêu cầu
            if self.preserve_indent:
                cleaned_lines.append(line)
            else:
                # Loại bỏ khoảng trắng đầu và cuối (có thể phá vỡ XML structure)
                cleaned_lines.append(line.strip())
        
        # Tính toán thống kê
        final_line_count = len(cleaned_lines)
        file_stats['lines_removed'] = original_line_count - final_line_count
        
        # Ghép lại thành nội dung
        cleaned_content = '\n'.join(cleaned_lines)
        
        # Đảm bảo file kết thúc bằng newline
        if cleaned_content and not cleaned_content.endswith('\n'):
            cleaned_content += '\n'
        
        return cleaned_content, file_stats
    
    def clean_file(self, input_path, output_path=None):
        """
        Làm sạch một file XML
        
        Args:
            input_path (str): Đường dẫn file đầu vào
            output_path (str, optional): Đường dẫn file đầu ra
            
        Returns:
            bool: True nếu thành công
        """
        try:
            # Kiểm tra file đầu vào
            if not os.path.exists(input_path):
                print(f"❌ File không tồn tại: {input_path}")
                self.stats['files_failed'] += 1
                return False
            
            self.stats['files_processed'] += 1
            print(f"🔄 Đang xử lý: {input_path}")
            
            # Tạo backup nếu được yêu cầu
            if self.backup and output_path != input_path:
                self.create_backup(input_path)
            
            # Đọc nội dung file
            with open(input_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Làm sạch nội dung
            cleaned_content, file_stats = self.clean_xml_content(content)
            
            # Xác định đường dẫn output
            if output_path is None:
                output_path = input_path
            
            # Tạo thư mục output nếu chưa tồn tại
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            
            # Ghi file đã làm sạch
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_content)
            
            # Cập nhật thống kê tổng
            self.stats['files_success'] += 1
            self.stats['total_lines_removed'] += file_stats['lines_removed']
            self.stats['total_comments_removed'] += file_stats['comments_removed']
            self.stats['total_empty_lines_removed'] += file_stats['empty_lines_removed']
            
            # In thống kê file
            print(f"✅ Hoàn thành: {output_path}")
            print(f"   📊 Comment đã xóa: {file_stats['comments_removed']}")
            print(f"   📊 Dòng trống đã xóa: {file_stats['empty_lines_removed']}")
            print(f"   📊 Tổng dòng đã xóa: {file_stats['lines_removed']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Lỗi khi xử lý {input_path}: {str(e)}")
            self.stats['files_failed'] += 1
            return False
    
    def clean_directory(self, input_dir, output_dir=None, pattern="*.xml", recursive=False):
        """
        Làm sạch tất cả file XML trong thư mục
        
        Args:
            input_dir (str): Thư mục đầu vào
            output_dir (str, optional): Thư mục đầu ra
            pattern (str): Pattern file để tìm
            recursive (bool): Tìm kiếm đệ quy
            
        Returns:
            bool: True nếu có ít nhất 1 file được xử lý thành công
        """
        input_path = Path(input_dir)
        
        if not input_path.exists():
            print(f"❌ Thư mục không tồn tại: {input_dir}")
            return False
        
        # Tìm file
        if recursive:
            files = list(input_path.rglob(pattern))
        else:
            files = list(input_path.glob(pattern))
        
        if not files:
            print(f"❌ Không tìm thấy file nào với pattern '{pattern}' trong: {input_dir}")
            return False
        
        print(f"🔍 Tìm thấy {len(files)} file(s)")
        print("=" * 60)
        
        for file_path in files:
            # Xác định đường dẫn output
            if output_dir:
                # Giữ cấu trúc thư mục
                rel_path = file_path.relative_to(input_path)
                output_file = Path(output_dir) / rel_path
            else:
                output_file = file_path
            
            self.clean_file(str(file_path), str(output_file))
            print("-" * 40)
        
        return self.stats['files_success'] > 0
    
    def print_summary(self):
        """In tổng kết"""
        print("\n" + "=" * 60)
        print("🎉 TỔNG KẾT")
        print("=" * 60)
        print(f"📁 File đã xử lý: {self.stats['files_processed']}")
        print(f"✅ File thành công: {self.stats['files_success']}")
        print(f"❌ File lỗi: {self.stats['files_failed']}")
        print(f"💬 Tổng comment đã xóa: {self.stats['total_comments_removed']:,}")
        print(f"📄 Tổng dòng trống đã xóa: {self.stats['total_empty_lines_removed']:,}")
        print(f"🗑️  Tổng dòng đã xóa: {self.stats['total_lines_removed']:,}")

def main():
    """Hàm main với argparse"""
    parser = argparse.ArgumentParser(
        description="XML Cleaner - Công cụ làm sạch file XML nâng cao",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  python xml_cleaner_advanced.py file.xml
  python xml_cleaner_advanced.py file.xml -o cleaned.xml
  python xml_cleaner_advanced.py -d ./input/ -o ./output/
  python xml_cleaner_advanced.py -d ./data/ --recursive
  python xml_cleaner_advanced.py file.xml --no-comments --no-empty-lines
  python xml_cleaner_advanced.py file.xml --no-backup
        """
    )
    
    # Input arguments
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('file', nargs='?', help='File XML cần làm sạch')
    group.add_argument('-d', '--directory', help='Thư mục chứa file XML')
    
    # Output arguments  
    parser.add_argument('-o', '--output', help='File/thư mục đầu ra (mặc định: ghi đè file gốc)')
    
    # Options
    parser.add_argument('--no-comments', action='store_true', 
                       help='KHÔNG xóa comment XML')
    parser.add_argument('--no-empty-lines', action='store_true',
                       help='KHÔNG xóa dòng trống')
    parser.add_argument('--no-backup', action='store_true',
                       help='KHÔNG tạo backup')
    parser.add_argument('--no-indent', action='store_true',
                       help='KHÔNG giữ nguyên indentation (cẩn thận!)')
    
    # Directory options
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='Tìm kiếm đệ quy trong thư mục con')
    parser.add_argument('-p', '--pattern', default='*.xml',
                       help='Pattern file để tìm (mặc định: *.xml)')
    
    args = parser.parse_args()
    
    # Hiển thị header
    print("🧹 XML Cleaner Advanced - Công cụ làm sạch XML nâng cao")
    print("=" * 60)
    
    # Tạo cleaner với các options
    cleaner = XMLCleaner(
        remove_comments=not args.no_comments,
        remove_empty_lines=not args.no_empty_lines,
        preserve_indent=not args.no_indent,
        backup=not args.no_backup
    )
    
    # Hiển thị cấu hình
    print("⚙️  Cấu hình:")
    print(f"   🗨️  Xóa comment: {'✅' if cleaner.remove_comments else '❌'}")
    print(f"   📄 Xóa dòng trống: {'✅' if cleaner.remove_empty_lines else '❌'}")
    print(f"   📐 Giữ indentation: {'✅' if cleaner.preserve_indent else '❌'}")
    print(f"   💾 Tạo backup: {'✅' if cleaner.backup else '❌'}")
    print()
    
    # Xử lý
    success = False
    
    if args.file:
        # Xử lý file đơn lẻ
        success = cleaner.clean_file(args.file, args.output)
    elif args.directory:
        # Xử lý thư mục
        success = cleaner.clean_directory(
            args.directory, 
            args.output, 
            args.pattern, 
            args.recursive
        )
    
    # In tổng kết
    cleaner.print_summary()
    
    # Exit code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
