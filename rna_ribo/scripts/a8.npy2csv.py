import numpy as np
import pandas as pd
import sys
import os

def npy_to_csv(npy_path, sep=','):
    # 检查文件是否存在
    if not os.path.isfile(npy_path):
        print(f"文件不存在: {npy_path}")
        return

    # 加载 .npy 数据
    try:
        data = np.load(npy_path, allow_pickle=True)
    except Exception as e:
        print(f"读取失败: {e}")
        return

    # 如果是字典，遍历保存
    if isinstance(data.item() if data.shape == () else data, dict):
        data = data.item()
        for key, value in data.items():
            df = pd.DataFrame(value)
            out_path = f"{key}.csv"
            df.to_csv(out_path, index=False, sep=sep)
            print(f"已保存 {out_path}")
    else:
        # 常规数组或矩阵
        df = pd.DataFrame(data)
        out_path = os.path.splitext(npy_path)[0] + ".csv"
        df.to_csv(out_path, index=False, sep=sep)
        print(f"已保存 {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python npy2csv.py your_file.npy")
    else:
        npy_path = sys.argv[1]
        npy_to_csv(npy_path)



