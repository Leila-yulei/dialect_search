import pandas as pd

def auto_fill_word_id(input_file, output_file):
    """
    读取 Excel 文件，自动填充 word_id 列
    :param input_file: 输入的 Excel 文件路径
    :param output_file: 输出的 Excel 文件路径
    """
    # 读取 Excel 文件
    df = pd.read_excel(input_file, engine='openpyxl')

    # 初始化当前 word_id
    current_word_id = 1

    # 遍历每一行
    for index in range(len(df)):
        # 检查当前行是否为被释词
        if pd.notna(df.at[index, '被释词']):
            # 填充 word_id，并更新 current_word_id
            df.at[index, 'word_id'] = current_word_id
            current_word_id += 1
        else:
            # 继续使用前一次的 current_word_id
            df.at[index, 'word_id'] = current_word_id - 1

    # 保存结果到新的 Excel 文件
    df.to_excel(output_file, index=False)
    print(f"处理完成！结果已保存到 {output_file}")

# 使用示例
input_file = 'dialect.xlsx'  # 输入 Excel 文件路径
output_file = 'meaning_filled.xlsx'  # 输出 Excel 文件路径
auto_fill_word_id(input_file, output_file)