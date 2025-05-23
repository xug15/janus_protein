import json
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from Bio.Seq import Seq
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# ===================== 用户配置 =====================
input_jsonl = "k562_rna_ribo_features.jsonl"
output_image_dir = "/home/dell/model/script/Translatomer-main/k562_rna_images"
output_matrix_dir = "k562_rna_encoded/"
output_jsonl = output_matrix_dir + "/train_K562_rna_ribo_train.jsonl"
json_image_dir = output_image_dir
max_transcripts = None  # 限制处理数量
num_threads = 12  # 线程数，根据CPU核心数设置
# ===================================================

os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_matrix_dir, exist_ok=True)

# RNAfold 预测结构
def predict_structure(seq):
    result = subprocess.run(['RNAfold'], input=seq, capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    structure = lines[1].split()[0]
    return structure

# One-hot 编码
def one_hot_base(base):
    return {'A':[1,0,0,0],'a':[1,0,0,0], 'C':[0,1,0,0],'c':[0,1,0,0], 'G':[0,0,1,0], 'g':[0,0,1,0],'U':[0,0,0,1],'u':[0,0,0,1],'T':[0,0,0,1],'t':[0,0,0,1]}.get(base, [0,0,0,0])

def one_hot_structure(dot):
    return {'.':[1,0,0], '(': [0,1,0], ')':[0,0,1]}.get(dot, [0,0,0])

def normalize(arr):
    return np.log1p(np.array(arr))

def encode_rna(seq, struct, rna_expr, ribo_expr):
    assert len(seq) == len(struct) == len(rna_expr) == len(ribo_expr)
    rna_norm = normalize(rna_expr)
    ribo_norm = normalize(ribo_expr)
    return np.array([
        one_hot_base(seq[i]) + one_hot_structure(struct[i]) + [rna_norm[i]] + [ribo_norm[i]]
        for i in range(len(seq))
    ])

def encode_rna_noribo(seq, struct, rna_expr):
    assert len(seq) == len(struct) == len(rna_expr)
    rna_norm = normalize(rna_expr)
    return np.array([
        one_hot_base(seq[i]) + one_hot_structure(struct[i]) + [rna_norm[i]]
        for i in range(len(seq))
    ])

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

# 单个转录本处理函数
def process_transcript(line):
    try:
        data = json.loads(line)
        rna_signal = data["rnaseq_signal"]
        ribo_signal = data["riboseq_signal"]
        transcript_id = data["transcript_id"]
        utr5, cds, utr3 = data["utr5"], data["cds"], data["utr3"]
        transcript_seq = utr5 + cds + utr3

        if all(v == 0.0 for v in rna_signal) and all(v == 0.0 for v in ribo_signal):
            print(f"⚠️ 跳过：{transcript_id} — 全部信号为 0")
            return None

        L = min(len(transcript_seq), len(rna_signal), len(ribo_signal))
        transcript_seq = transcript_seq[:L].replace('T', 'U')
        rna_signal, ribo_signal = rna_signal[:L], ribo_signal[:L]

        structure = predict_structure(transcript_seq)
        if len(structure) != len(transcript_seq):
            print(f"❌ 长度不一致，跳过 {transcript_id}")
            return None

        encoded = encode_rna(transcript_seq, structure, rna_signal, ribo_signal)
        encoded_predict = encode_rna_noribo(transcript_seq, structure, rna_signal)

        # protein one-hot 编码
        utr5_len, cds_len, utr3_len = len(utr5), len(cds), len(utr3)
        protein_one_hot = [[0]*23] * utr5_len
        protein_seq = Seq(cds).translate(to_stop=False)

        for aa in protein_seq:
            one_hot = one_hot_amino23(aa)
            protein_one_hot += [one_hot] * 3

        extra = cds_len - 3 * len(protein_seq)
        protein_one_hot += [one_hot_amino23('0')] * extra
        protein_one_hot += [[0]*23] * utr3_len
        protein_one_hot = np.array(protein_one_hot[:L])

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


        # 构造 JSON 条目
        image_path = os.path.join(json_image_dir, f"{transcript_id}.png")
        json_item = {
            "images": image_path,
            "instruction": f"图片是根据下面内容进行one-hot编码... \n基因序列：{transcript_seq}\n预测结构：{structure}",
            "output": ribo_signal
        }
        return json_item

    except Exception as e:
        print(f"❗ 错误 {e}")
        return None

# 主线程：读取数据并多线程处理
results = []
with open(input_jsonl, "r") as f:
    lines = f.readlines()
    if max_transcripts:
        lines = lines[:max_transcripts]

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(process_transcript, line) for line in lines]
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

# 写入最终 JSONL 输出
with open(output_jsonl, "w") as out_f:
    for item in results:
        out_f.write(json.dumps(item) + "\n")

print(f"✅ 处理完成，总计生成 {len(results)} 条数据。")
