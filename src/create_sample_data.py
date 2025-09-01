#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo script cho BG3 Enhanced Filter GUI
Tạo file XML mẫu để test các tính năng
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

def create_sample_xml():
    """Tạo file XML mẫu với nhiều loại content"""
    
    # Tạo root element
    root = ET.Element("contentList")
    
    # Sample data với nhiều loại khác nhau
    samples = [
        # UI Text samples
        ("h001", "Save Game", "1"),
        ("h002", "Load Game", "1"),
        ("h003", "Options", "1"),
        ("h004", "Health: [1]/[2]", "1"),
        ("h005", "Press [E] to interact", "1"),
        ("h006", "<LSTag Tooltip=\"MovementSpeed\">Movement Speed</LSTag>: [1]/[2]", "1"),
        ("h007", "Inventory", "1"),
        ("h008", "Character", "1"),
        ("h009", "Quest Complete", "1"),
        ("h010", "Level Up!", "1"),
        
        # Dialogue samples
        ("h101", "\"Hello there, traveler! What brings you to our village?\"", "1"),
        ("h102", "\"I'm looking for the ancient temple. Have you seen it?\"", "1"), 
        ("h103", "The wind howls through the abandoned ruins.", "1"),
        ("h104", "You hear footsteps approaching from behind.", "1"),
        ("h105", "*This place gives me the creeps...*", "1"),
        ("h106", "(I should be more careful here.)", "1"),
        ("h107", "Something doesn't feel right about this place.", "1"),
        ("h108", "\"Ah yes, it's just beyond the forest. But beware!\"", "1"),
        
        # Combat context
        ("h201", "Attack of Opportunity", "1"),
        ("h202", "Critical Hit!", "1"),
        ("h203", "You take 15 damage", "1"),
        ("h204", "Spell Resistance", "1"),
        ("h205", "Fire Bolt", "1"),
        ("h206", "Lightning Strike", "1"),
        ("h207", "Healing Potion", "1"),
        
        # Inventory context  
        ("h301", "Leather Armor", "1"),
        ("h302", "Health Potion", "1"),
        ("h303", "Weight: 2.5 kg", "1"),
        ("h304", "Rarity: Common", "1"),
        ("h305", "Sword of Power", "1"),
        ("h306", "Shield of Protection", "1"),
        
        # Quest context
        ("h401", "Find the Lost Artifact", "1"),
        ("h402", "Quest Complete", "1"),
        ("h403", "Objective: Talk to the Elder", "1"),
        ("h404", "Reward: 500 Gold", "1"),
        ("h405", "Explore the Ancient Ruins", "1"),
        
        # Character context
        ("h501", "Astarion", "1"),
        ("h502", "Level 5 Rogue", "1"),
        ("h503", "Strength: 12", "1"),
        ("h504", "Background: Noble", "1"),
        ("h505", "Charisma: 17", "1"),
        
        # Technical samples
        ("h601", "ERROR_CODE_001", "1"),
        ("h602", "DEBUG_MODE_ENABLED", "1"),
        ("h603", "C:\\Game\\Data\\file.pak", "1"),
        ("h604", "Version 4.1.1.3622062", "1"),
        
        # Mixed content
        ("h701", "Once upon a time, in a distant land far away, there lived a brave adventurer who sought to save the world from an ancient evil that threatened all living beings with destruction and chaos.", "1"),
        ("h702", "The ancient magic flows through your veins.", "1"),
        ("h703", "Menu Settings Configuration", "1"),
        ("h704", "Combat Victory Achievement Unlocked", "1"),
        
        # Vietnamese samples (for Non-English testing)
        ("h801", "Xin chào, hỡi người lữ hành!", "50"),
        ("h802", "Tôi đang tìm kiếm ngôi đền cổ.", "50"),
        ("h803", "Nhiệm vụ hoàn thành", "50"),
        ("h804", "Kinh nghiệm: 1000 điểm", "50"),
        
        # Empty and short samples
        ("h901", "", "1"),
        ("h902", "OK", "1"),
        ("h903", "Yes", "1"),
        ("h904", "No", "1"),
        ("h905", "Cancel", "1"),
    ]
    
    # Tạo content elements
    for contentuid, text, version in samples:
        content = ET.SubElement(root, "content")
        content.set("contentuid", contentuid)
        content.set("version", version)
        content.text = text
    
    return root

def save_pretty_xml(root, filename):
    """Lưu XML với format đẹp"""
    rough_string = ET.tostring(root, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty = reparsed.toprettyxml(indent="  ", encoding='utf-8')
    
    with open(filename, 'wb') as f:
        f.write(pretty)

def main():
    """Tạo các file XML mẫu"""
    
    # Tạo thư mục data/input nếu chưa có
    os.makedirs("data/input", exist_ok=True)
    
    # Tạo file XML mẫu
    print("🔨 Tạo file XML mẫu...")
    
    root = create_sample_xml()
    
    # Lưu file mẫu
    sample_file = "data/input/sample_english.xml"
    save_pretty_xml(root, sample_file)
    
    print(f"✅ Đã tạo file mẫu: {sample_file}")
    print(f"📊 Tổng cộng: {len(root)} entries")
    
    # Thống kê nội dung
    print("\n📋 Nội dung file mẫu:")
    print("- UI text samples: 10 entries")
    print("- Dialogue samples: 8 entries") 
    print("- Combat context: 7 entries")
    print("- Inventory context: 6 entries")
    print("- Quest context: 5 entries")
    print("- Character context: 5 entries")
    print("- Technical samples: 4 entries")
    print("- Mixed content: 4 entries")
    print("- Vietnamese samples: 4 entries")
    print("- Short samples: 5 entries")
    
    print(f"\n🎯 Cách sử dụng:")
    print(f"1. Chạy: run_bg3_filter_gui.bat")
    print(f"2. Chọn file: {sample_file}")
    print(f"3. Test các tính năng filter khác nhau")
    print(f"4. Xem kết quả trong output/filtered/")

if __name__ == "__main__":
    main()
