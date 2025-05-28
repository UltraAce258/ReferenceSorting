import re

def clean_text_spacing(text):
    """
    处理文本空格问题：
    - 去除中英文/数字间的空格（如"AI 手机"→"AI手机"）
    - 去除中文字符间的异常空格（如"电 池"→"电池"）
    - 保留段落开头的四个空格
    - 保留英文/数字字符间的原有空格
    """
    # 按段落分割文本（保留换行符）
    paragraphs = text.split('\n')
    processed_paras = []
    
    for para in paragraphs:
        # 匹配段落开头的四个空格（支持全角/半角混合，实际应用中建议统一为半角空格）
        # ^表示行首，\s{4}匹配四个空白字符（包括空格、制表符等，可根据实际情况调整为'    '纯空格）
        # 使用非贪婪匹配避免匹配过多内容
        match = re.match(r'^(\s{4})(.*)', para)
        
        if match:
            # 提取开头的四个空格和正文内容
            prefix = match.group(1)
            body = match.group(2)
        else:
            # 无开头空格的段落直接处理正文
            prefix = ''
            body = para
        
        # 第一阶段：处理中英文/数字间的空格（两种方向）
        # 中文在前，英文/数字在后（如"AI 手机"→"AI手机"）
        body = re.sub(r'([\u4e00-\u9fa5])\s+([a-zA-Z0-9])', r'\1\2', body)
        # 英文/数字在前，中文在后（如"2024 年"→"2024年"）
        body = re.sub(r'([a-zA-Z0-9])\s+([\u4e00-\u9fa5])', r'\1\2', body)
        # 第二阶段：处理中文字符间的异常空格（如"电 池"→"电池"）
        body = re.sub(r'([\u4e00-\u9fa5])\s+([\u4e00-\u9fa5])', r'\1\2', body)
        #第三阶段：去除引用符号与中文字符、其他字符，以及连续的引用符号之间的空格（如 "中文字符 [1] [2]"→“中文字符[1][2]"）
        # 去除中文字符与引用符号间的空格
        body = re.sub(r'([\u4e00-\u9fa5])\s*(\[[0-9]+])', r'\1\2', body)
        # 去除引用符号与其他字符间的空格（除了行首缩进）
        body = re.sub(r'(?<!^\s{4})(\[[0-9]+])\s+', r'\1', body)
        # 合并连续的引用符号
        body = re.sub(r'(\[[0-9]+])\s+(\[[0-9]+])', r'\1\2', body)
        # 组合处理后的段落
        processed_paras.append(prefix + body)
    
    # 合并段落并返回
    return '\n'.join(processed_paras)

# 示例用法（实际使用时替换为你的文本）
if __name__ == "__main__":
    sample_text = """ """
    cleaned_text = clean_text_spacing(sample_text)
    print(cleaned_text)