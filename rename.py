import os
import re

# 读取文件名对应的英文名称
en_names = {}
with open('en_names.txt', 'r', encoding='utf-8') as f:
    for line in f:
        english, chinese = re.match(r'(.+)《(.+?)》', line.strip()).groups()
        en_names[chinese] = english

# 遍历 source 目录下的文件
source_dir = 'source'
for filename in os.listdir(source_dir):
    # 提取文件名中的期数和中文标题
    match = re.match(r'第(\d+)期:(.+)\.md', filename)
    if match:
        num, chinese_title = match.groups()
        num = num.zfill(3)  # 转换为3位数字，不足补0
        # 查找对应的英文标题
        english_title = en_names.get(chinese_title, chinese_title)
        # 构建新的文件名
        new_filename = f'{num}-{english_title} 《{chinese_title}》.md'
        # 重命名文件
        os.rename(os.path.join(source_dir, filename), os.path.join(source_dir, new_filename))
    else:
        print(f"No match found for file: {filename}")
