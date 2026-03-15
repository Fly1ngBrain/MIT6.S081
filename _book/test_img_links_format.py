import os
import re

# 匹配 Markdown 图片语法: ![alt](path)
img_regex = re.compile(r'!\[.*?\]\((.*?)\)')

def check_and_fix_images():
    for root, dirs, files in os.walk("."):
        # 忽略构建目录和隐藏目录
        if '_book' in root or '.git' in root:
            continue
            
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                matches = img_regex.findall(content)
                for img_path in matches:
                    # 1. 检查是否存在 HTML 特殊字符
                    if '>' in img_path or ')' in img_path:
                        print(f"⚠️ 发现可疑路径: {img_path} 在文件 {path}")
                    
                    # 2. 检查绝对路径 (以 / 开头在 GitHub Pages 会失效)
                    if img_path.startswith('/'):
                        print(f"🚩 发现绝对路径: {img_path}，建议改为相对路径。")

                    # 3. 检查文件物理是否存在
                    # 获取图片相对于当前 md 文件的绝对物理路径
                    real_img_path = os.path.normpath(os.path.join(root, img_path))
                    if not os.path.exists(real_img_path):
                        print(f"❌ 图片文件不存在: {real_img_path} (引用自 {path})")

if __name__ == "__main__":
    check_and_fix_images()