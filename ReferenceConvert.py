import re
from collections import OrderedDict

# 示例输入数据（可替换为实际文件读取）
reference_data = """""".split("\n") # 把原文参考文献的字符串按行转换成列表（复制粘贴到引号中间即可）

# 1. 按原有顺序提取旧标号并生成新序号
old_labels = []
content_list = []
for line in reference_data:
    # 分割标号与内容（处理可能的格式差异）
    match = re.match(r'^(\w+)\s*-\s*(.*)$', line.strip())
    if match:
        old_label, content = match.groups()
        old_labels.append(old_label)
        content_list.append(content)
    else:
        print(f"警告：无法解析行 - {line}")
        old_labels.append(None)
        content_list.append(line.strip())

# 2. 生成连续新标号（1, 2, 3...）
new_labels = list(range(1, len(old_labels)+1))

# 3. 建立旧标号到新标号的映射（保留原始顺序，处理重复标号）
mapping = OrderedDict()
for old, new in zip(old_labels, new_labels):
    if old:
        if old in mapping:
            print(f"警告：重复标号 {old}，新标号为 {new}（原映射为 {mapping[old]}）")
        mapping[old] = new

# 4. 生成新参考文献列表
new_references = [f"{new}. {content}" for new, content in zip(new_labels, content_list)]

# 5. 导出结果（示例输出到控制台，可修改为文件写入）
print("=== 新参考文献列表 ===")
for line in new_references:
    print(line)

print("\n=== 标号映射表 ===")
for old, new in mapping.items():
    print(f"旧标号：{old} → 新标号：{new}")

# 扩展：保存到文件
with open("new_references.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(new_references))

with open("label_mapping.txt", "w", encoding="utf-8") as f:
    f.write("旧标号,新标号\n")
    for old, new in mapping.items():
        f.write(f"{old},{new}\n")
        



# 定义旧标号到新标号的映射表（与之前生成的标号映射表一致）
reference_mapping = mapping

# 原始文本以字符串形式直接定义（支持多行文本，用三重引号包裹）
original_text = """ """
# 原文参考文献的字符串（复制粘贴过来即可）


# 定义正则表达式匹配旧标号格式（支持逗号分隔的多个标号，如(mar25f, apr25i)）
pattern = r'[（\(]([a-z]{3}\d{2}[a-z](?:,\s*[a-z]{3}\d{2}[a-z])*)[）\)]'

# 替换函数：将旧标号转换为新标号，支持多标号批量处理
def replace_labels(match):
    old_labels = match.group(1).split(', ')  # 拆分多个标号
    new_labels = []
    for label in old_labels:
        new_label = reference_mapping.get(label.lower())  # 兼容大小写
        if new_label is not None:
            new_labels.append(f'[{new_label}]')
        else:
            new_labels.append(label)  # 未匹配的标号保留原格式
    return '(' + ', '.join(new_labels) + ')' if len(new_labels) > 1 else new_labels[0]

# 执行替换（忽略大小写匹配，确保jan24A与JAN24a都能识别）
updated_text = re.sub(pattern, replace_labels, original_text, flags=re.IGNORECASE)

# 输出修正后的文本
print("=== 修正后的文本 ===")
print(updated_text)