import os
import re
from pathlib import Path

# 匹配复杂的 Markdown 图片引用，包括带空格和括号的情况
# 目标：提取出 image (数字)
img_pattern = re.compile(r'!\[.*?\]\((.*?(image\s*\(\d+\)).*?)\)')

def find_all_assets():
    """扫描全仓库，建立图片文件名到实际路径的映射"""
    asset_map = {}
    for root, _, files in os.walk("."):
        if "_book" in root or ".git" in root:
            continue
        for f in files:
            if f.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                # 统一存为小写键，防止大小写坑
                asset_map[f.lower()] = Path(root).absolute()
    return asset_map

def fix_markdown_files(asset_map):
    for root, _, files in os.walk("."):
        if "_book" in root or ".git" in root:
            continue
        for file in files:
            if file.endswith(".md"):
                md_path = Path(root) / file
                with open(md_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                def replace_func(match):
                    full_old_path = match.group(1)
                    img_name_part = match.group(2) # 获取像 "image (586)" 这样的部分
                    
                    # 尝试匹配文件名
                    target_file = None
                    for actual_name in asset_map:
                        if img_name_part.lower() in actual_name:
                            target_file = actual_name
                            break
                    
                    if target_file:
                        target_full_path = asset_map[target_file] / target_file
                        # 计算当前 md 文件到图片文件的相对路径
                        rel_path = os.path.relpath(target_full_path, start=Path(root).absolute())
                        # Windows 路径转转为 Web 通用的 /
                        rel_path = rel_path.replace('\\', '/')
                        print(f"✅ 修复: {md_path.name} -> {rel_path}")
                        return f"![image]({rel_path})"
                    
                    return match.group(0) # 没找到就不动

                new_content = img_pattern.sub(replace_func, content)
                
                if new_content != content:
                    with open(md_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

if __name__ == "__main__":
    print("🔍 正在扫描全仓库资源文件...")
    assets = find_all_assets()
    print(f"找到 {len(assets)} 个图片资源。开始修复 Markdown...")
    fix_markdown_files(assets)
    print("✨ 修复完成！请尝试重新编译构建。")