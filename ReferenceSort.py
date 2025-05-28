import re
from collections import OrderedDict

def generate_letter_label(index):
    """生成两位字母标号（aa=0, ab=1, ..., ba=26, bb=27...）"""
    first = index // 26
    second = index % 26
    return f"{chr(ord('a') + first)}{chr(ord('a') + second)}"

def process_references(text, references):
    # ====================== 步骤1：提取正文引用标号并生成字母映射 ======================
    # 提取正文中所有引用标号（如[12]）并去重，保留首次出现顺序
    citation_matches = re.findall(r'\[(\d+)\]', text)
    unique_citations = OrderedDict.fromkeys(citation_matches).keys()  # 保留顺序去重
    citation_numbers = [int(num) for num in unique_citations]
    
    # 生成字母标号映射（数字→字母）
    letter_map = {num: generate_letter_label(idx) for idx, num in enumerate(citation_numbers)}
    
    # 替换正文中的数字标号为字母
    for num, letter in letter_map.items():
        text = re.sub(rf'\[{num}\]', f'[{letter}]', text)
    
    # ====================== 步骤2：处理参考文献列表 ======================
    # 解析参考文献为字典（标号: 内容）
    ref_dict = {}
    for line in references:
        line = line.strip()
        if not line:
            continue
        match = re.match(r'^(\d+)\.\s(.*)', line)
        if match:
            ref_num = int(match.group(1))
            ref_content = match.group(2)
            ref_dict[ref_num] = ref_content
    
    # 分离已引用和未引用的参考文献
    cited_refs = {num: content for num, content in ref_dict.items() if num in letter_map}
    uncited_refs = {num: content for num, content in ref_dict.items() if num not in letter_map}
    
    # 为未引用的参考文献分配后续字母标号
    total_cited = len(citation_numbers)
    for num in uncited_refs.keys():
        idx = total_cited + list(uncited_refs.keys()).index(num)
        letter_map[num] = generate_letter_label(idx)
    
    # 合并并按字母标号排序
    all_refs = {**cited_refs, **uncited_refs}
    sorted_refs = sorted(all_refs.items(), key=lambda x: letter_map[x[0]])
    
    # ====================== 步骤3：生成最终数字映射并替换 ======================
    # 按字母顺序生成新数字标号（aa→1, ab→2, ...）
    sorted_letters = sorted(letter_map.values(), key=lambda x: (ord(x[0]), ord(x[1])))
    new_number_map = {letter: str(i+1) for i, letter in enumerate(sorted_letters)}
    
    # 替换正文中的字母标号为新数字
    for letter, new_num in new_number_map.items():
        text = re.sub(rf'\[{letter}\]', f'[{new_num}]', text)
    
    # 处理参考文献为最终格式
    final_references = []
    for num, content in sorted_refs:
        letter = letter_map[num]
        new_num = new_number_map[letter]
        final_references.append(f"{new_num}. {content}")
    
    return text, final_references

# ====================== 示例运行 ======================
if __name__ == "__main__":
    # 读取正文（请替换为实际文本）
    text = """ """
    
    
    # 读取参考文献（请替换为实际参考文献字符串，每行格式为“数字. 内容”）
    references = """ """.split("\n")
    
    # 处理文本和参考文献
    processed_text, processed_references = process_references(text, references)
    
    # 输出结果
    print("==== 最终正文 ====")
    print(processed_text)
    print("\n==== 最终参考文献 ====")
    for ref in processed_references:
        print(ref)