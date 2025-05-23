import numpy as np
import matplotlib.pyplot as plt

def one_hot_base(base):
    mapping = {'A': [1,0,0,0], 'C': [0,1,0,0], 'G': [0,0,1,0], 'U': [0,0,0,1]}
    return mapping.get(base, [0,0,0,0])

def encode_structure(dot):
    if dot == '.':
        return [1,0,0]
    elif dot == '(':
        return [0,1,0]
    elif dot == ')':
        return [0,0,1]
    else:
        return [0,0,0]

def encode_sequence_structure(seq, struct):
    encoded = []
    for b, s in zip(seq, struct):
        encoded.append(one_hot_base(b) + encode_structure(s))
    return np.array(encoded)

# 示例数据
seq = "GCGGAUUUAGCUCAGUUGGGAGAGCGCCAGACUGAAGAUCUGCCAUGGUAG"
struct = "((((((((...((((((.((......)).))))))))))))))........"

encoded = encode_sequence_structure(seq, struct)

# 显示为图像
plt.imshow(encoded.T, aspect='auto', cmap='viridis')
plt.xlabel("Position")
plt.ylabel("Features (A,C,G,U,.,(,))")
plt.title("RNA sequence + structure encoding")
plt.colorbar()
plt.tight_layout()
plt.savefig("rna_structure_encoding.png", dpi=300)
plt.show()

# ✅ 保存图片
plt.savefig("seq.structure.png", dpi=300, bbox_inches='tight')
plt.close()  # 可选：避免在某些IDE中自动弹窗


