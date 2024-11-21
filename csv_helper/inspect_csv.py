# 用于查看csv文件每一列的情况，方便进行接下来的数据补全和丢弃
import numpy as np
import pandas as pd
import json
from prettytable import PrettyTable

def set_column_types(file_path,output_path, is_select=True):
    """
    通过用户的输入，设置每一列的类型，并将每一列的类型对应存储，存储类型被改变的csv副本
    :param file_path:
    :param output_path: 将保存为csv和hdf5(key='df')两种格式的文件，同时保存datatype对应关系到json. 文件名是output_path + '.csv' 和output_path + '.h5'
    """
    try:
        # 读取 CSV 文件
        df = pd.read_csv(file_path)

        # 初始化变量
        column_types = {}
        is_selected_list = []

        print(f"文件包含 {df.shape[1]} 列，以下是每列的信息：\n")

        # 遍历每列
        for column in df.columns:
            ## ABIDE 中部分缺失数据使用-9999代替
            df.loc[df[column]==-9999,column] = np.nan
            nan_percentage = df[column].count() / df.shape[0]
            print(f"列名: '{column}'")
            print(f'数据缺失率：{(1-nan_percentage) * 100}%')
            print(f"示例数据: {df[column].head(5).to_list()}")

            # 提示用户输入类型
            print('如果不选择这一列，输入"x"')
            user_input = input(f"请输入该列的数据类型编号（例如 int64(1), float64(2), category(3)，object(4)）：\n"
                               f"直接按 Enter 表示不改变列的类型 [{df[column].dtype}]: ").strip()

            # 如果用户按 Enter，使用上一列的类型
            if not user_input:
                print(f"默认使用类型: {df[column].dtype}\n")
            else:
                # 更新列类型
                column_types[column] = user_input
                if user_input == 'x':
                    is_selected_list.append(False)
                    print(f'没有选择列{column}\n')
                else:
                    is_selected_list.append(True)
                    if user_input == '1':
                        df[column] = df[column].astype('int64')
                    if user_input == '2':
                        df[column] = df[column].astype('float64')
                    if user_input == '3':
                        df[column] = df[column].astype('category')
                    if user_input == '3':
                        df[column] = df[column].astype('category')
                    if user_input == '4':
                        df[column] = df[column].astype('object')
                    print(f"已将类型设置为: {df[column].dtype}\n")

        # 输出用户指定的类型
        print("\n最终的列类型如下：")
        for col, dtype in column_types.items():
            print(f"列 '{col}': {dtype}")

        with open('data_type.json','w') as f:
            json.dump(column_types,f,indent=4)
            print('数据类型对应关系已保存到 data_type.json')

        df = df.loc[:,is_selected_list]
        # save to csv and hdf5
        df.to_csv(output_path+'.csv',index=False)
        df.to_hdf(output_path+'.h5',key='df',mode='w')

    except Exception as e:
        print(f"发生错误: {e}")


def check_column_types(file_path):
    """
    检查 CSV 文件中每列的数据类型。
    如果某列不是数值类型，显示列名及其非数值类型。

    :param file_path: CSV 文件路径
    """
    try:
        # 读取 CSV 文件
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        if file_path.endswith('.h5'):
            df = pd.read_hdf(file_path, key='df')

        print(f"样本有{df.shape[0]}个\n")
        print(f"文件包含 {df.shape[1]} 列。检查数据类型：\n")


        # 遍历每列
        for column in df.columns:
            # 判断列的类型
            if pd.api.types.is_numeric_dtype(df[column]):
                print(f"列 '{column}': 数值类型 （{df[column].dtype})")
            else:
                print(f"列 '{column}': 非数值类型 ({df[column].dtype})")

    except Exception as e:
        print(f"发生错误: {e}")

def load_datatype(csv_file,data_type,output = 'output'):
    df = pd.read_csv(csv_file)
    with open(data_type,'r') as f:
        dt = json.load(f)
    is_selected_list = []
    for column in df.columns:
        try:
            d_type = dt[column]
        except Exception as e:
            is_selected_list.append(True)
            continue

        if d_type == 'x':
            is_selected_list.append(False)
        else:
            is_selected_list.append(True)
            if d_type == '1':
                df[column] = df[column].astype('int64')
            if d_type == '2':
                df[column] = df[column].astype('float64')
            if d_type == '3':
                df[column] = df[column].astype('category')
            if d_type == '4':
                df[column] = df[column].astype('object')

    df = df.loc[:,is_selected_list]
    df.to_hdf(output + '.h5',key='df',mode='w',format='table')
    df.to_csv(output + '.csv')

if __name__ == '__main__':
    # 使用需要inspect的csv文件
    file_path = "example.csv"
    data_type = 'data_type.json'
    output = 'output'
    check_column_types(file_path)
    load_datatype(file_path,data_type,output)
    check_column_types('output.h5')