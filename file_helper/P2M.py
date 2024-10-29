# 将pyhton变量转为matlab的格式，即保存为mat文件
import numpy as np
from scipy.io import savemat

class P2M:
    def __init__(self) -> None:
        pass

    def save_mat(self,variables:dict,filename='save.mat'):
        # mat_dict = {}
        # for key, value in variables.items():
        #     max_len = max(len(s)for s in value)
        #     char_matrix = np.array([list(s.ljust(max_len)) for s in value])
        #     mat_dict[key] = char_matrix
        # savemat(filename,mat_dict)
        savemat(filename, variables)
