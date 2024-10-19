import os
import re
import gzip
import shutil
from tqdm import tqdm

quite_mode = False

filedir_pattern = re.compile(r'^rfMRI_REST.*$')
filename_pattern = re.compile(r'^\d+_3T_rfMRI_REST(1|2)_(LR|RL)\.nii\.gz$')

# 要搜索的目录路径, 目录下仅有sub文件夹
directory = r'F:\hcp\HCP'
# 遍历目录中的所有文件并筛选符合正则表达式的文件
matching_files = []
for sub in os.listdir(directory):
    sub_dir = directory + os.sep + sub + os.sep + r'unprocessed\3T'
    for filename in os.listdir(sub_dir):
        # 检查文件名是否匹配正则表达式
        mri_files = os.listdir(sub_dir)
        for mri_file in mri_files:
            if filedir_pattern.match(mri_file):
                rs_fmris = os.listdir(sub_dir+os.sep+mri_file)
                for rs_fmri in rs_fmris:
                    if filename_pattern.match(rs_fmri):
                        matching_files.append(sub_dir+os.sep+mri_file + os.sep + rs_fmri)

# 输出匹配的文件
# for f in matching_files:
#     print(f)

for gzip_file in tqdm(matching_files, desc="解压进度", unit="file"):
    output_file = gzip_file[:-3]
    if(quite_mode):
        print(f'extracting {gzip_file}')
    with gzip.open(gzip_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)