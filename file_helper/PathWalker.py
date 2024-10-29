# 根据正则表达式获取路径,并生成命令

import os
import re
import shutil
from tqdm import tqdm
import gzip

##
# d 搜索的根目录
# patterns 一个正则表达式列表，每一级目录的正则匹配，只支持搜索到最后一级目录再查找文件
# file_pattern 文件名的正则表达式
# is_collected 是否捕获正则表达式中的组
# is_one2one 是否一个目录下只有一个匹配的文件（用于减少搜索时间）
class PathWalker():
    def __init__(self,d,patterns,file_pattern,is_collected=False,is_one2one=False) -> None:
        # 正则匹配路径符号\\，pattern需要是\\\\
        # 由于py输出(os.getcwd())的win路径以及os.sep都是使用'\\'
        # 因此使用re匹配'\\'的话，需要将dir_path原来的'\'改为'\\'，使用replace也就是'\\'to'\\\\'
        sep = os.sep
        if sep == '\\':
            dir_path_re = d.replace('\\','\\\\')
            sep = sep*2
        # 要遍历的根目录路径
        self.d = d
        # 根目录下的目录pattern,每一级目录pattern都是list一个元素
        patterns.insert(0,dir_path_re)
        self.patterns = []
        for i in range(len(patterns)):
            pattern = sep.join(patterns[0:i+1])
            pattern = '^'+pattern+'$'
            self.patterns.append(re.compile(pattern))
        self.file_pattern = re.compile(file_pattern)
        self.h = 1
        self.res = []
        self.is_collected = is_collected
        self.collected = []
        self.is_one2one = is_one2one

    # the recursive function helper
    def __recursive_helper(self,d,h):
        files = os.listdir(d)
        for file in files:
            if self.file_pattern.match(file):
                self.res.append(os.sep.join([d,file]))
                if self.is_collected:
                    group = re.findall(self.patterns[h-1],d)
                    group.append(re.findall(self.file_pattern,file)[0])
                    self.collected.append(group)
                if self.is_one2one:
                    break
            if h < len(self.patterns):
                if self.patterns[h].match(os.sep.join([d,file])):
                    self.__recursive_helper(os.sep.join([d,file]),h+1)
        
    # obtain the matched file path
    def get_path(self):
        self.res = []
        self.__recursive_helper(self.d,self.h)
        return self.res


# generate commands

# unzip_gzip
# unzip the end with .gz file
# 
def unzip_gzip(matching_files,out=-3):
    ## use gzip unzip files
    for gzip_file in tqdm(matching_files, desc="解压进度", unit="file"):
        output_file = gzip_file[:out]
        with gzip.open(gzip_file, 'rb') as f_in:
            with open(output_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

# 用于将搜索到的的文件名生成命令
def move_to(matching_files,output_dirs):
    ## move files
    for i,file in tqdm(enumerate(matching_files),total=len(matching_files)):
        if not os.path.isdir(output_dirs[i]):
            os.mkdir(output_dirs[i])
        if not os.path.isfile(output_dirs[i] + os.sep + file.split(os.sep)[-1]):
            shutil.move(file,output_dirs[i])
