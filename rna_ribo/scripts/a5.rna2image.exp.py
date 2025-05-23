import numpy as np
import matplotlib.pyplot as plt
import matplotlib

def one_hot_base(base):
    return {'A':[1,0,0,0], 'C':[0,1,0,0], 'G':[0,0,1,0], 'U':[0,0,0,1]}.get(base, [0,0,0,0])

def one_hot_structure(dot):
    return {'.':[1,0,0], '(': [0,1,0], ')':[0,0,1]}.get(dot, [0,0,0])

def normalize(arr):
    arr = np.array(arr)
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr) + 1e-6)

def encode_rna(seq, struct, rna_expr, ribo_expr):
    assert len(seq) == len(struct) == len(rna_expr) == len(ribo_expr)
    matrix = []
    rna_norm = normalize(rna_expr)
    ribo_norm = normalize(ribo_expr)
    for i in range(len(seq)):
        row = one_hot_base(seq[i]) + one_hot_structure(struct[i]) + [rna_norm[i]] + [ribo_norm[i]]
        matrix.append(row)
    return np.array(matrix)

# 示例数据
seq = "GCGGAUUUAGCUCAGUUGGGAGAGCGCCAGACUGAAGAUCUGCCAUGGUAG"
struct = "((((((((...((((((.((......)).))))))))))))))........"
rna_expr =  [2,6,9,9,1,7,0,5,8,4,7,3,6,7,4,8,7,5,3,6,7,6,6,4,4,4,2,3,2,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,8,2]
ribo_expr = [9,7,2,1,0,5,3,2,4,2,2,1,1,2,2,3,4,5,4,3,2,2,2,3,3,2,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,3]

# 编码
encoded = encode_rna(seq, struct, rna_expr, ribo_expr)  # shape: (L, 10)

# 转置后作为图像显示
plt.figure(figsize=(10, 3))
plt.imshow(encoded.T, aspect='auto', cmap='viridis')
plt.xlabel("Position")
plt.ylabel("Features: [A,C,G,U], [.,(,)], RNA, Ribo")
plt.title("RNA Structure + Expression Encoding")
plt.colorbar()
plt.tight_layout()
plt.savefig("rna_encoded_image2.png", dpi=300)
plt.show()

# 可保存 numpy 格式
np.save("rna_encoded2.npy", encoded)




