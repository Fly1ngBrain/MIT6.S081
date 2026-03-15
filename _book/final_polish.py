import os
import re
from pathlib import Path

def final_polish():
    # 匹配破碎的 Markdown 语法：![](<../路径.png
    # 提取括号内的 alt 文本和实际路径，重新拼装为标准的 ![alt](path)
    pattern = re.compile(r'!\[(.*?)\]\(<([^>)\s]+\.png)[^)]*\)?')

    for root, _, files in os.walk("."):
        if "_book" in root or ".git" in root:
            continue
        for file in files:
            if file.endswith(".md"):
                filepath = Path(root) / file
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 执行替换并记录替换次数
                new_content, count = pattern.subn(r'![\1](\2)', content)

                if count > 0:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"✨ 缝合修复了 {filepath.name} 中的 {count} 处破碎链接")

if __name__ == "__main__":
    print("🧹 正在进行最后的语法清理...")
    final_polish()
    print("✅ 清理完成！")