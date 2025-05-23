import json
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os
from multiprocessing import Pool
from Bio.Seq import Seq

# ========== 用户配置 ==========
input_jsonl = "k562_rna_ribo_features.jsonl"
output_image_dir = "k562_rna_images"
output_matrix_dir = "k562_rna_encoded"
output_json = "k562_rna_outputs.json"
max_transcripts = None
num_workers = 8
show_aa = True
# ==============================

os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_matrix_dir, exist_ok=True)

# 氨基酸 one-hot 编码表
AA_LIST = list("ACDEFGHIKLMNPQRSTVWY*")
AA_TO_ONEHOT = {aa: [1 if i == idx else 0 for i in range(len(AA_LIST))] for idx, aa in enumerate(AA_LIST)}

def encode_protein(seq):
    return np.array([AA_TO_ONEHOT.get(aa, [0]*len(AA_LIST)) for aa in seq])

def predict_structure(seq):
    result = subprocess.run(['RNAfold'], input=seq, capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    return lines[1].split()[0]

def one_hot_base(base):
    return {'A':[1,0,0,0], 'C':[0,1,0,0], 'G':[0,0,1,0], 'U':[0,0,0,1]}.get(base, [0,0,0,0])

def one_hot_structure(dot):
    return {'.':[1,0,0], '(': [0,1,0], ')':[0,0,1]}.get(dot, [0,0,0])

def normalize(arr):
    arr = np.array(arr)
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr) + 1e-6)

def encode_rna(seq, struct, rna_expr, ribo_expr):
    assert len(seq) == len(struct) == len(rna_expr) == len(ribo_expr)
    rna_norm = normalize(rna_expr)
    ribo_norm = normalize(ribo_expr)
    return np.array([
        one_hot_base(seq[i]) + one_hot_structure(struct[i]) + [rna_norm[i]] + [ribo_norm[i]]
        for i in range(len(seq))
    ])

def process_sample(data):
    try:
        rna_signal = data["rnaseq_signal"]
        ribo_signal = data["riboseq_signal"]
        transcript_id = data["transcript_id"]
        transcript_seq = data["utr5"] + data["cds"] + data["utr3"]

        if all(v == 0.0 for v in rna_signal) and all(v == 0.0 for v in ribo_signal):
            return None

        L = min(len(transcript_seq), len(rna_signal), len(ribo_signal))
        transcript_seq = transcript_seq[:L].replace('T', 'U')
        rna_signal = rna_signal[:L]
        ribo_signal = ribo_signal[:L]

        structure = predict_structure(transcript_seq)
        if len(structure) != len(transcript_seq):
            return None

        encoded = encode_rna(transcript_seq, structure, rna_signal, ribo_signal)

        image_path = os.path.join(output_image_dir, f"{transcript_id}.png")
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.imshow(encoded.T, aspect='auto', cmap='viridis')
        ax.set_xlabel("Position")
        ax.set_ylabel("Features")

        # 氨基酸标注和编码
        protein_seq = ""
        if show_aa and "cds" in data:
            cds_rna = data["cds"].replace("U", "T")
            if len(cds_rna) % 3 != 0:
                cds_rna = cds_rna[:len(cds_rna) - (len(cds_rna) % 3)]
            protein_seq = str(Seq(cds_rna).translate(to_stop=False))
            protein_matrix = encode_protein(protein_seq)
            np.save(os.path.join(output_matrix_dir, f"{transcript_id}_protein.npy"), protein_matrix)

            cds_start = len(data["utr5"])
            for i, aa in enumerate(protein_seq):
                base_idx = cds_start + i * 3 + 1
                if base_idx >= len(transcript_seq):
                    break
                ax.text(base_idx, encoded.shape[1] + 0.5, aa, fontsize=6, ha='center', va='bottom', color='black')

        ax.set_title(f"{transcript_id}")
        plt.tight_layout()
        plt.savefig(image_path, dpi=300)
        plt.close()

        np.save(os.path.join(output_matrix_dir, f"{transcript_id}.npy"), encoded)

        return {
            "transcript_id": transcript_id,
            "image": image_path,
            "protein_length": len(protein_seq),
            "has_protein": bool(protein_seq)
        }
    except Exception as e:
        return None

with open(input_jsonl, "r") as f:
    all_data = [json.loads(line) for line in f if line.strip()]
    if max_transcripts:
        all_data = all_data[:max_transcripts]

with Pool(processes=num_workers) as pool:
    results = list(pool.map(process_sample, all_data))

results = [r for r in results if r]
with open(output_json, "w") as fout:
    json.dump(results, fout, indent=2)




