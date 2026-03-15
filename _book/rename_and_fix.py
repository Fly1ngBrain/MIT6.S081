import os
import re
from pathlib import Path

def fix_all():
    assets_dir = Path(".gitbook/assets")

    # 1. 批量重命名物理文件
    if assets_dir.exists():
        for filename in os.listdir(assets_dir):
            if filename.startswith("image (") and filename.endswith(".png"):
                # 提取数字，例如从 "image (190).png" 提取 "190"
                match = re.search(r'image \(([0-9]+)\)\.png', filename)
                if match:
                    num = match.group(1)
                    new_name = f"image_{num}.png"
                    
                    old_path = assets_dir / filename
                    new_path = assets_dir / new_name
                    
                    # 为了防止重复运行报错，先检查目标文件是否已存在
                    if not new_path.exists():
                        os.rename(old_path, new_path)
                        print(f"✅ 文件重命名: {filename} -> {new_name}")

    # 2. 批量修改 Markdown 文件中的链接
    # 正则解释：匹配 "image (数字).png" 以及它后面可能跟着的脏数据 ">" 或 ")"
    # 将它们全部替换为 "image_数字.png"
    pattern = re.compile(r'image \(([0-9]+)\)\.png[>\)]*')

    for root, _, files in os.walk("."):
        if "_book" in root or ".git" in root:
            continue
        for file in files:
            if file.endswith(".md"):
                filepath = Path(root) / file
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 执行替换并记录替换次数
                new_content, count = pattern.subn(r'image_\1.png', content)

                if count > 0:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"📝 修复了 {filepath} 中的 {count} 处图片链接")

if __name__ == "__main__":
    print("🚀 开始修复文件名和 Markdown 链接...")
    fix_all()
    print("🎉 全部修复完成！")