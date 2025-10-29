"""
批量清理现有歌词文件
提取规则：从 "下载txt文档" 到 "更多" 之间的内容
"""

import os
import shutil

def extract_clean_lyrics(file_path):
    """
    从文件中提取 "下载txt文档" 到 "更多" 之间的内容
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        start_idx = None
        end_idx = None
        
        # 查找起始和结束位置
        for i, line in enumerate(lines):
            if '下载txt文档' in line or 'txt 文档' in line:
                start_idx = i + 1  # 从下一行开始
            elif '更多' in line and start_idx is not None:
                end_idx = i
                break
        
        if start_idx is not None and end_idx is not None and start_idx < end_idx:
            # 提取内容
            extracted_lines = lines[start_idx:end_idx]
            # 移除空行
            clean_lines = [line for line in extracted_lines if line.strip()]
            return ''.join(clean_lines), True
        else:
            print(f"    ⚠️  未找到提取标记")
            return None, False
            
    except Exception as e:
        print(f"    ✗ 错误: {e}")
        return None, False

def process_directory(root_dir, backup_dir='backup_original'):
    """
    批量处理目录中的所有txt文件
    """
    # 创建备份目录
    backup_path = os.path.join(os.path.dirname(root_dir), backup_dir)
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)
        print(f"✓ 创建备份目录: {backup_path}\n")
    
    stats = {
        'total': 0,
        'success': 0,
        'failed': 0
    }
    
    # 遍历所有txt文件
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.txt'):
                stats['total'] += 1
                file_path = os.path.join(root, file)
                
                # 显示进度
                rel_path = os.path.relpath(file_path, root_dir)
                print(f"[{stats['total']}] 处理: {rel_path}")
                
                # 提取内容
                clean_content, success = extract_clean_lyrics(file_path)
                
                if success and clean_content:
                    # 备份原文件
                    backup_file = os.path.join(backup_path, f"backup_{stats['total']}_{file}")
                    shutil.copy2(file_path, backup_file)
                    
                    # 写入清理后的内容
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(clean_content)
                    
                    # 统计
                    original_size = os.path.getsize(backup_file)
                    new_size = os.path.getsize(file_path)
                    reduction = (original_size - new_size) / original_size * 100
                    
                    print(f"    ✓ 已清理 (减少 {reduction:.1f}%)")
                    stats['success'] += 1
                else:
                    stats['failed'] += 1
                
                print()
    
    return stats

def main():
    print("="*60)
    print("🎵 批量清理歌词文件")
    print("="*60)
    print("提取规则：从 '下载txt文档' 到 '更多' 之间的内容\n")
    
    # 要处理的目录
    target_dir = "test_lyrics/page_1"
    
    if not os.path.exists(target_dir):
        print(f"✗ 目录不存在: {target_dir}")
        return
    
    print(f"处理目录: {target_dir}\n")
    print("="*60 + "\n")
    
    # 处理文件
    stats = process_directory(target_dir)
    
    # 显示统计
    print("="*60)
    print("✅ 处理完成！")
    print("="*60)
    print(f"总文件数: {stats['total']}")
    print(f"成功: {stats['success']}")
    print(f"失败: {stats['failed']}")
    print("="*60)
    print(f"\n原始文件已备份到: backup_original/")

if __name__ == '__main__':
    main()

