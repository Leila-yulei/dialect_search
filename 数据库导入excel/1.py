import pandas as pd

# 读取原始 Excel 文件
file_path = 'output.xlsx'  # 替换为你的文件路径
df = pd.read_excel(file_path)

# 假设数据在第 1 列（第一列索引为 0），第二列和第三列需要重复
# 如果你的列名不同，请替换为实际列名
column_to_split = df.columns[0]  # 第一列需要拆分
repeat_columns = df.columns[1:]  # 后面的列需要重复

# 将逗号分隔的字符串拆分为列表
df[column_to_split] = df[column_to_split].str.split('、')

# 将拆分后的列展开为多行
df_exploded = df.explode(column_to_split).reset_index(drop=True)

# 保存为新的 Excel 文件
output_file_path = 'output.xlsx'  # 输出文件路径
df_exploded.to_excel(output_file_path, index=False, engine='openpyxl')

print(f"数据已成功拆分为多行并保存到 {output_file_path}")