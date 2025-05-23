import json
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from Bio.Seq import Seq
import os

# ===================== 用户配置 =====================
input_jsonl = "k562_rna_ribo_features.jsonl"
output_image_dir = "/home/dell/model/script/Translatomer-main/k562_rna_images"
output_matrix_dir = "k562_rna_encoded/"
output_jsonl = output_matrix_dir +"/train_K562_rna_ribo_train.jsonl"
json_image_dir = output_image_dir
max_transcripts = None  # 设置为整数可限制最大处理数
# ===================================================

os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_matrix_dir, exist_ok=True)

# RNAfold 预测结构
def predict_structure(seq):
    result = subprocess.run(['RNAfold'], input=seq, capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    structure = lines[1].split()[0]
    return structure

# one-hot 编码：碱基
def one_hot_base(base):
    return {'A':[1,0,0,0],'a':[1,0,0,0], 'C':[0,1,0,0],'c':[0,1,0,0], 'G':[0,0,1,0], 'g':[0,0,1,0],'U':[0,0,0,1],'u':[0,0,0,1],'T':[0,0,0,1],'t':[0,0,0,1]}.get(base, [0,0,0,0])

# one-hot 编码：结构
def one_hot_structure(dot):
    return {'.':[1,0,0], '(': [0,1,0], ')':[0,0,1]}.get(dot, [0,0,0])

# 归一化表达量
def normalize(arr):
    arr = np.array(arr)
    return np.log1p(arr)

# RNA 综合编码：base + structure + RNA + Ribo
def encode_rna(seq, struct, rna_expr, ribo_expr):
    assert len(seq) == len(struct) == len(rna_expr) == len(ribo_expr)
    matrix = []
    rna_norm = normalize(rna_expr)
    ribo_norm = normalize(ribo_expr)
    for i in range(len(seq)):
        row = one_hot_base(seq[i]) + one_hot_structure(struct[i]) + [rna_norm[i]] + [ribo_norm[i]]
        matrix.append(row)
    return np.array(matrix)

# RNA 综合编码：base + structure + RNA + Ribo
def encode_rna_noribo(seq, struct, rna_expr):
    assert len(seq) == len(struct) == len(rna_expr) 
    matrix = []
    rna_norm = normalize(rna_expr)
    for i in range(len(seq)):
        row = one_hot_base(seq[i]) + one_hot_structure(struct[i]) + [rna_norm[i]] 
        matrix.append(row)
    return np.array(matrix)

# one-hot 编码：氨基酸，含 stop、UTR（共23类）
def one_hot_amino23(acid):
    aa_dict = {
        'A': 0, 'R': 1, 'N': 2, 'D': 3, 'C': 4,
        'Q': 5, 'E': 6, 'G': 7, 'H': 8, 'I': 9,
        'L': 10, 'K': 11, 'M': 12, 'F': 13, 'P': 14,
        'S': 15, 'T': 16, 'W': 17, 'Y': 18, 'V': 19,
        '*': 20, '0': 21
    }
    vec = [0] * 23
    idx = aa_dict.get(acid.upper(), None)
    if idx is not None:
        vec[idx] = 1
    return vec

# 主程序
with open(output_jsonl, "w") as f:
    pass
#
with open(input_jsonl, "r") as f:
    for idx, line in enumerate(f):
        if max_transcripts is not None and idx >= max_transcripts:
            break
        try:
            data = json.loads(line)
            rna_signal = data["rnaseq_signal"]
            ribo_signal = data["riboseq_signal"]
            transcript_id = data["transcript_id"]
            utr5 = data["utr5"]
            cds = data["cds"]
            utr3 = data["utr3"]
            transcript_seq = utr5 + cds + utr3

            if all(v == 0.0 for v in rna_signal) and all(v == 0.0 for v in ribo_signal):
                print(f"⚠️ 跳过：{transcript_id} — 全部信号为 0")
                continue

            L = min(len(transcript_seq), len(rna_signal), len(ribo_signal))
            transcript_seq = transcript_seq[:L].replace('T', 'U')
            rna_signal = rna_signal[:L]
            ribo_signal = ribo_signal[:L]

            structure = predict_structure(transcript_seq)
            if len(structure) != len(transcript_seq):
                print(f"❌ 长度不一致，跳过 {transcript_id}")
                continue

            encoded = encode_rna(transcript_seq, structure, rna_signal, ribo_signal)
            encoded_predict = encode_rna_noribo(transcript_seq, structure, rna_signal)
            # === 氨基酸 one-hot 编码 ===
            utr5_len = len(utr5)
            cds_len = len(cds)
            utr3_len = len(utr3)

            protein_one_hot = []

            for _ in range(utr5_len):
                protein_one_hot.append([0]*23)

            protein_seq = Seq(cds).translate(to_stop=False)
            for aa in protein_seq:
                one_hot = one_hot_amino23(aa)
                for _ in range(3):
                    protein_one_hot.append(one_hot)

            extra = cds_len - 3 * len(protein_seq)
            for _ in range(extra):
                protein_one_hot.append(one_hot_amino23('0'))

            for _ in range(utr3_len):
                protein_one_hot.append([0]*23)

            protein_one_hot = np.array(protein_one_hot[:L])

            # === 图像输出 ===
            image_path = os.path.join(output_image_dir, f"{transcript_id}.full.png")
            fig, axs = plt.subplots(2, 1, figsize=(12, 5), sharex=True)

            axs[0].imshow(encoded.T, aspect='auto', cmap='viridis')
            axs[0].set_ylabel("RNA Features\n[A,C,G,U], [.,(,)], RNA, Ribo")
            axs[0].set_title(f"Transcript: {transcript_id}")

            #print(f"{transcript_id} protein_one_hot shape: {protein_one_hot.shape}")
            axs[1].imshow(protein_one_hot.T, aspect='auto', cmap='plasma')
            axs[1].set_xlabel("Nucleotide Position")
            axs[1].set_ylabel("Protein One-Hot\n(23 classes)")

            plt.tight_layout()
            plt.savefig(image_path, dpi=300)
            plt.close()

            # === 图像输出 ===
            image_path = os.path.join(output_image_dir, f"{transcript_id}.png")
            fig, axs = plt.subplots(2, 1, figsize=(12, 5), sharex=True)

            axs[0].imshow(encoded_predict.T, aspect='auto', cmap='viridis')
            axs[0].set_ylabel("RNA Features\n[A,C,G,U], [.,(,)], RNA")
            axs[0].set_title(f"Transcript: {transcript_id}")

            #print(f"{transcript_id} protein_one_hot shape: {protein_one_hot.shape}")
            axs[1].imshow(protein_one_hot.T, aspect='auto', cmap='plasma')
            axs[1].set_xlabel("Nucleotide Position")
            axs[1].set_ylabel("Protein One-Hot\n(23 classes)")

            plt.tight_layout()
            plt.savefig(image_path, dpi=300)
            plt.close()

            # 保存矩阵
            new_image_path = os.path.join(json_image_dir, f"{transcript_id}.png")
            json_item = {
                "images": f"{new_image_path}",
                "instruction": f"图片是根据下面内容进行one-hot编码.第一幅图分别表示'A','C','G','U','.','(',')','RNA log+1表达量',第二副图对应翻译的蛋白序列图,从上到下表示'A','R','N','D','C','Q', 'E', 'G', 'H', 'I','L', 'K', 'M', 'F', 'P','S', 'T', 'W', 'Y', 'V','*', '0'\n"
                                f"根据基因的转录组数据预测该基因的翻译组数据生物计算任务。\n"
                               f"基因序列包含AUCG四种碱基，序列为：{transcript_seq}\n"
                               f"预测其形成RNA的二级结构，'.' 表示单链，'(' 表示左配对，')' 表示右配对，预测结果为：{structure}\n"
                               f"基因的转录UTR5长度:{utr5_len},CDS长度:{cds_len},UTR3长度:{utr3_len}\n"
                               f"CDS翻译为氨基酸序列:{protein_seq}\n"
                               f"基因的转录水平表达量:{rna_signal}",
                "output": f"{ribo_signal}"
            }
            with open(output_jsonl, "a") as fout:
                fout.write(json.dumps(json_item, ensure_ascii=False) + "\n")
            print(f"✅ 已保存 {transcript_id}: 图像 -> {image_path}")

        except Exception as e:
            print(f"❗ 出错跳过：{data.get('transcript_id', 'unknown')} — {e}")













