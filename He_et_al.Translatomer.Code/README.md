# Using translatomer to predict ribo-seq signal from rna seq.

```py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
data = pd.read_csv("results/bigmodel_h512_l12_lr1e-5_metrics.csv")
val = data.dropna(subset = ['val_loss'])
train = data.dropna(subset = ['train_loss'])
epoch = train["epoch"]  
train_loss = train["train_loss"]
val_loss = val["val_loss"]
train_acc = train["train_acc"]
val_acc = val["val_acc"]

fig = plt.figure(figsize = (7,6)) 
p1 = pl.plot(epoch, train_loss,'r-', label = u'train_loss')
p2 = pl.plot(epoch,val_loss, 'b-', label = u'val_loss')
pl.legend()
pl.xlabel(u'Epoch')
pl.ylabel(u'MSE loss')
# ✅ 保存图片
plt.savefig("loss_curve.png", dpi=300, bbox_inches='tight')
plt.close()  # 可选：避免在某些IDE中自动弹窗

fig = plt.figure(figsize = (7,6)) 
p3 = pl.plot(epoch, train_acc,'r-', label = u'train_acc')
p4 = pl.plot(epoch,val_acc, 'b-', label = u'val_acc')
pl.legend()
pl.xlabel(u'Epoch')
pl.ylabel(u'PCC')
# ✅ 保存图片
plt.savefig("pcc_curve.png", dpi=300, bbox_inches='tight')
plt.close()  # 可选：避免在某些IDE中自动弹窗
```
## De novo prediction


```py

import kipoiseq
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from train_all_11fold import TrainModule, FastaStringExtractor

import matplotlib.pyplot as plt
import seaborn as sns

import pyBigWig
from kipoiseq import Interval
import math
import random
#############part1
def one_hot_encode(sequence):
    en_dict = {'A' : 0, 'T' : 1, 'C' : 2, 'G' : 3, 'N' : 4}
    en_seq = [en_dict[ch] for ch in sequence]
    np_seq = np.array(en_seq, dtype = int)
    seq_emb = np.zeros((len(np_seq), 5))
    seq_emb[np.arange(len(np_seq)), np_seq] = 1
    return seq_emb.astype(np.float32)
    
def get_cds_interval(gff_df, gene_name):
    # filter by gene_name
    gff_df = gff_df[gff_df[8].str.split(';').str[5].str.split('=').str[1] == gene_name]
    # generate dict
    gene_dict = {row[8].split(';')[0].split('=')[1]: {'chrom': row[0],'start': row[3], 'end': row[4], 'name':row[8].split(';')[7].split('=')[1], 
                                                      'cds_intervals': []} for _, row in gff_df.iterrows() if row[2] == 'transcript'}
    cds_df = gff_df[gff_df[2] == 'CDS']
    for _, row in cds_df.iterrows():
        gene_name = row[8].split(';')[3].split('=')[1]
        gene_dict[gene_name]['cds_intervals'].append((row[3], row[4]))
    target_gene = next((gene_info for gene_info in gene_dict.values()
                      ), None)
    if target_gene:
        cds_intervals = target_gene['cds_intervals']
        return {
            'chrom': target_gene['chrom'],
            'gene_start': target_gene['start'],
            'gene_end': target_gene['end'],
            'cds_intervals': cds_intervals,
            'gene_name': target_gene['name']
        }
    
def generate_inputs(region, fasta_file, bw_file, region_len=SEQUENCE_LENGTH):
    bw = pyBigWig.open(bw_file)
    target = []
    chrom = region.chrom
    start = region.start
    end = region.end
    chromosome_length = bw.chroms(chrom)
    interval = Interval(chrom, start, end).resize(region_len)
    trimmed_interval = Interval(interval.chrom,
                                max(interval.start, 0),
                                min(interval.end, chromosome_length),
                                )
    signals = np.array(bw.values(chrom, trimmed_interval.start, trimmed_interval.end)).astype(np.float32).tolist()
    pad_upstream = np.array([0] * max(-interval.start, 0)).astype(np.float32).tolist()
    pad_downstream = np.array([0] * max(interval.end - chromosome_length, 0)).astype(np.float32).tolist()
    tmp = pad_upstream + signals + pad_downstream
    arr = np.array(tmp).astype(np.float32)
    target.append(arr)

    target = np.array(target).astype(np.float32)
    target = np.nan_to_num(target,0)
    target = np.log(target + 1)
    bw.close()
    return target

def generate_outputs(region, fasta_file, bw_file, nBins=1024, region_len=65536):
    bw = pyBigWig.open(bw_file)
    target = []
    chrom = region.chrom
    start = region.start
    end = region.end
    chromosome_length = bw.chroms(chrom)
    interval = Interval(chrom, start, end).resize(region_len)
    trimmed_interval = Interval(interval.chrom,
                                max(interval.start, 0),
                                min(interval.end, chromosome_length),
                               )
    signals = np.array(bw.values(chrom, trimmed_interval.start, trimmed_interval.end)).astype(np.float32).tolist()
    pad_upstream = np.array([0] * max(-interval.start, 0)).astype(np.float32).tolist()
    pad_downstream = np.array([0] * max(interval.end - chromosome_length, 0)).astype(np.float32).tolist()
    tmp = pad_upstream + signals + pad_downstream
    arr = np.array(tmp).astype(np.float32)
    reshaped_arr = arr.reshape(-1, 64)
    averages = np.mean(reshaped_arr, axis=1)
    target.append(averages)

    target = np.array(target).astype(np.float32)
    target = np.nan_to_num(target,0)
    target = np.log(target + 1)
    bw.close()
    return target
###############part2
random.seed(2077)
SEQUENCE_LENGTH = 65536

device = 'cuda:3'
checkpoint = 'results/bigmodel_h512_l12_lr1e-5_epoch=38-step=746889.ckpt'
model = TrainModule.load_from_checkpoint(checkpoint).to(device)
model = model.eval()

fasta_file = 'data/hg38/hg38.fa'
fasta_extractor = FastaStringExtractor(fasta_file)
gff_file = 'data/hg38/gencode.v43.annotation.gff3'
rna_bw_file = 'data/hg38/K562/GSE153597/input_features/K562_GSE153597_rnaseq.bw'
ribo_bw_file = 'data/hg38/K562/GSE153597/input_features/K562_GSE153597_riboseq.bw'

gene_name = 'SYT6' #target gene

gff_df = pd.read_csv(gff_file, sep='\t', comment='#', header=None)
gene_info = get_cds_interval(gff_df, gene_name)

gene_interval =kipoiseq.Interval(gene_info['chrom'], gene_info['gene_start'], gene_info['gene_end'])
target_interval = Interval(gene_interval.chrom, gene_interval.start, gene_interval.end).resize(SEQUENCE_LENGTH)
ref_seq = fasta_extractor.extract(target_interval)
ref_emb = torch.Tensor(one_hot_encode(ref_seq)).to(device)

epi = torch.Tensor(generate_inputs(gene_interval, fasta_file, rna_bw_file)[0]).unsqueeze(1).to(device)
reference_input = torch.cat([ref_emb, epi], dim = 1).unsqueeze(0)
pred = model(reference_input)[0].detach().cpu().numpy()
#########part3
print(pred)
print(pred.shape)

```

## extract signal from bw. 
```py
import pyBigWig

bw = pyBigWig.open("rna_seq_sample.bw")
signal = bw.values("chr1", 100000, 100100)  # 获取 chr1:100000-100100 的值
print(signal)
bw.close()

```
如何生成jsonl文件,从gff3注释文件,提取hg38基因组数据转录序列,以及riboseq与rnaseq bw文件的信号.
/home/dell/model/script/Translatomer-main/data/hg38/K562/GSE153597/input_features/K562_GSE153597_riboseq.bw
/home/dell/model/script/Translatomer-main/data/hg38/K562/GSE153597/input_features/K562_GSE153597_rnaseq.bw
/home/dell/model/script/Translatomer-main/data/hg38/hg38.fa
/home/dell/model/script/Translatomer-main/data/hg38/gencode.v43.annotation.gff3

```sh
conda activate pytorch3916
```
extract signal from k562 
```py

##第一步：解析 GFF3，提取转录本结构（UTR/CDS）
import gffutils

db_path = "hg38.db"
gff_file = "/home/dell/model/script/Translatomer-main/data/hg38/gencode.v43.annotation.gff3"

# 构建数据库（只做一次）
gffutils.create_db(gff_file, dbfn=db_path, force=True, keep_order=True, merge_strategy='merge', sort_attribute_values=True)

db = gffutils.FeatureDB(db_path)
## 第二步：提取转录本序列（基于 hg38）
from Bio import SeqIO

fasta_path = "/home/dell/model/script/Translatomer-main/data/hg38/hg38.fa"
genome = SeqIO.to_dict(SeqIO.parse(fasta_path, "fasta"))

def extract_sequence(chrom, start, end, strand):
    seq = genome[chrom].seq[start:end]
    return str(seq if strand == "+" else seq.reverse_complement())
## 第三步：提取 Ribo-seq & RNA-seq 信号（pyBigWig）
import pyBigWig

bw_rna = pyBigWig.open("/home/dell/model/script/Translatomer-main/data/hg38/K562/GSE153597/input_features/K562_GSE153597_rnaseq.bw")
bw_ribo = pyBigWig.open("/home/dell/model/script/Translatomer-main/data/hg38/K562/GSE153597/input_features/K562_GSE153597_riboseq.bw")

def extract_signal(bw, chrom, start, end):
    return bw.values(chrom, start, end, numpy=True).tolist()
## 第四步：生成 JSONL 文件
import json
from tqdm import tqdm

output_jsonl = "k562_rna_ribo_features.jsonl"
with open(output_jsonl, "w") as fout:
    for transcript in tqdm(db.features_of_type('transcript')):
        chrom = transcript.chrom
        strand = transcript.strand
        tid = transcript.attributes.get('transcript_id', [None])[0]
        gid = transcript.attributes.get('gene_id', [None])[0]

        # 提取所有子结构
        exons = list(db.children(transcript, featuretype='exon', order_by='start'))
        cds = list(db.children(transcript, featuretype='CDS', order_by='start'))
        utr5 = [f for f in db.children(transcript, featuretype='five_prime_UTR', order_by='start')]
        utr3 = [f for f in db.children(transcript, featuretype='three_prime_UTR', order_by='start')]

        if not cds or not utr5 or not utr3:
            continue  # 必须包含完整结构

        # 取序列
        cds_seq = ''.join([extract_sequence(f.chrom, f.start - 1, f.end, f.strand) for f in cds])
        utr5_seq = ''.join([extract_sequence(f.chrom, f.start - 1, f.end, f.strand) for f in utr5])
        utr3_seq = ''.join([extract_sequence(f.chrom, f.start - 1, f.end, f.strand) for f in utr3])

        # 提取信号
        start = transcript.start - 1
        end = transcript.end
        rnaseq_signal = extract_signal(bw_rna, chrom, start, end)
        riboseq_signal = extract_signal(bw_ribo, chrom, start, end)

        fout.write(json.dumps({
            "transcript_id": tid,
            "gene_id": gid,
            "chrom": chrom,
            "strand": strand,
            "utr5": utr5_seq,
            "cds": cds_seq,
            "utr3": utr3_seq,
            "rnaseq_signal": rnaseq_signal,
            "riboseq_signal": riboseq_signal
        }) + "\n")

```
extract data signal from hepG2

```py

##第一步：解析 GFF3，提取转录本结构（UTR/CDS）
import gffutils

db_path = "hg38.db"
gff_file = "/home/dell/model/script/Translatomer-main/data/hg38/gencode.v43.annotation.gff3"

# 构建数据库（只做一次）
#gffutils.create_db(gff_file, dbfn=db_path, force=True, keep_order=True, merge_strategy='merge', sort_attribute_values=True)

db = gffutils.FeatureDB(db_path)
## 第二步：提取转录本序列（基于 hg38）
from Bio import SeqIO

fasta_path = "/home/dell/model/script/Translatomer-main/data/hg38/hg38.fa"
genome = SeqIO.to_dict(SeqIO.parse(fasta_path, "fasta"))

def extract_sequence(chrom, start, end, strand):
    seq = genome[chrom].seq[start:end]
    return str(seq if strand == "+" else seq.reverse_complement())
## 第三步：提取 Ribo-seq & RNA-seq 信号（pyBigWig）
import pyBigWig

bw_rna = pyBigWig.open("/home/dell/model/script/Translatomer-main/data/hg38/HepG2/GSE174419/input_features/HepG2_GSE174419_rnaseq.bw")
bw_ribo = pyBigWig.open("/home/dell/model/script/Translatomer-main/data/hg38/HepG2/GSE174419/output_features/HepG2_GSE174419_riboseq.bw")

def extract_signal(bw, chrom, start, end):
    return bw.values(chrom, start, end, numpy=True).tolist()
## 第四步：生成 JSONL 文件
import json
from tqdm import tqdm

output_jsonl = "hepG2_rna_ribo_features.jsonl"
with open(output_jsonl, "w") as fout:
    for transcript in tqdm(db.features_of_type('transcript')):
        chrom = transcript.chrom
        strand = transcript.strand
        tid = transcript.attributes.get('transcript_id', [None])[0]
        gid = transcript.attributes.get('gene_id', [None])[0]

        # 提取所有子结构
        exons = list(db.children(transcript, featuretype='exon', order_by='start'))
        cds = list(db.children(transcript, featuretype='CDS', order_by='start'))
        utr5 = [f for f in db.children(transcript, featuretype='five_prime_UTR', order_by='start')]
        utr3 = [f for f in db.children(transcript, featuretype='three_prime_UTR', order_by='start')]

        if not cds or not utr5 or not utr3:
            continue  # 必须包含完整结构

        # 取序列
        cds_seq = ''.join([extract_sequence(f.chrom, f.start - 1, f.end, f.strand) for f in cds])
        utr5_seq = ''.join([extract_sequence(f.chrom, f.start - 1, f.end, f.strand) for f in utr5])
        utr3_seq = ''.join([extract_sequence(f.chrom, f.start - 1, f.end, f.strand) for f in utr3])

        # 提取信号
        start = transcript.start - 1
        end = transcript.end
        rnaseq_signal = extract_signal(bw_rna, chrom, start, end)
        riboseq_signal = extract_signal(bw_ribo, chrom, start, end)

        fout.write(json.dumps({
            "transcript_id": tid,
            "gene_id": gid,
            "chrom": chrom,
            "strand": strand,
            "utr5": utr5_seq,
            "cds": cds_seq,
            "utr3": utr3_seq,
            "rnaseq_signal": rnaseq_signal,
            "riboseq_signal": riboseq_signal
        }) + "\n")

```

GCGGAUUUAGCUCAGUUGGGAGAGCGCCAGACUGAAGAUCUGCCAUGGUAG
RNA fold预测出来的结果,
((((((((...((((((.((......)).))))))))))))))........
U,A,C,G进行编码,
rna的表达量2,6,10,9,1,7,0,...
ribo-seq的表达了9,7,2,1,0,...

是否可以生成编码生成图片

```py
import subprocess

def predict_structure(seq):
    result = subprocess.run(['RNAfold'], input=seq.encode(), capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    structure = lines[1].split()[0]  # dot-bracket
    return structure

```

```py
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
rna_exp=

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

```
create image.

```py
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

```

```json

{"transcript_id": "ENST00000616016.5", 
"gene_id": "ENSG00000187634.13", 
"chrom": "chr1", 
"strand": "+",
"utr5":"ggcggcggAGTCTCCCAAGTCCCCGCCGGGCGGGCGCGCGCCAGTGGACGCGGGTGCACGACTGACGCGGCCCGGGCGGCGGGGCGGGGGCTTGGGACCCCCGAGAGGGGCGGGGACTCCGCGACTCCTCGCTGCCGGGCTCGGCCTGGCGGGTGGGTCGGCGAGCCGGGCGTGGGACTGCCCCGGGCGCGGGCGCTGGTGGCCGGGGCGCGGGACTCCAGACGCCCCGGGGAGCCCCGAGGCCCTGGAACTGCGGCGCTCGGCGAGTCGATCCGGGATCGATAGCAGCTCCATGTCTCCGGCCTCTGAGGCCCCGCCGGCCGGCTGGGCAGTCCGGGGAGGCCTGGCGGGCGGCGCGTAGGCGGCGGCTGCGGGCGCCGGGGCGCACTAGCGGACGGCGTGGGCGCGCGGCCAGGCGCCTCCCCGGCCCCCGCGACCCAACTCCAGCCCGGGCCGGAATAAGTTGCTGCCGCCGGCGGAGAGCGGGGCTGCGGAGCCACCGGGGCGCC", 
"cds":"ATGCCGGCGGTCAAGAAGGAGTTCCCGGGCCTGCAGCGGCGCGTGGGGAGGAGGCCCCAGCCCCTGAGGACGTCACCAAGTGGACCGTGGATGACGTCTGCAGCTTCGTGGGGGGCCTGTCTGGCTGTGGAGAGTACACTCGGGTCTTCAGGGAGCAGGGGATCGACGGGGAGACCCTGCCACTGCTGACGGAGGAGCACCTGCTGACCAACATGGGGCTGAAGCTGGGGCCCGCCCTCAAGATCCGGGCCCAGGTGGCCAGGCGCCTGGGCCGAGTTTTCTACGTGGCCAGCTTCCCCGTGGCTCTGCCACTGCAGCCACCAACCCTGCGGGCCCCGGAGCGAGAACTCGGCACAGGAGAGCAGCCCTTGTCCCCCACGACGGCCACGTCCCCCTATGGAGGGGGCCACGCCCTTGCCGGTCAAACTTCACCCAAGCAGGAGAATGGGACCTTGGCTCTACTTCCAGGGGCCCCCGACCCTTCCCAGCCTCTGTGTTGA", 
"utr3":"GGTTGCCGGGGGTAGGGGTGGGGCCACACAAATCTCCAGGAGCCACCACTCAACACAATGGCCGACTGGTCTCGGTCTGCTGACGTCAGGGTCAGCTCCCCCGCGGAGCTGACTTCAGCAGCCCACAGCTGTGGGGCTTCAGcagccacaccagcccagcccagcccagcTCTCGATACGTTTGGTCTTTCATGCTGAAAAATAAATAATAAAGCCTG", 
"rnaseq_signal": [14.548399925231934,  0.0, 0.0, 0.0, 0.0, 0.0, 0.0,203.67799377441406, 683.7760009765625, 698.3250122070312, 698.3250122070312, 712.8729858398438, 945.6480102539062, 945.6480102539062, 960.197021484375, 974.7449951171875, 974.7449951171875, 974.7449951171875, 989.2930297851562, 989.2930297851562, 989.2930297851562, 989.2930297851562, 960.197021484375, 960.197021484375, 872.906005859375, 872.906005859375, 872.906005859375, 872.906005859375, 872.906005859375, 858.3579711914062, 843.8090209960938, 829.260986328125, 829.260986328125, 829.260986328125, 829.260986328125, 829.260986328125, 872.906005859375, 887.4539794921875, 887.4539794921875, 887.4539794921875, 887.4539794921875, 887.4539794921875, 916.551025390625, 916.551025390625, 931.0999755859375, 1018.3900146484375, 1207.52001953125, 1309.3599853515625, 1396.6500244140625, 1411.199951171875, 1483.93994140625, 1600.3299560546875, 1600.3299560546875, 1600.3299560546875, 1614.8800048828125, 1614.8800048828125, 1687.6199951171875, 1687.6199951171875, 1192.969970703125, ], 

"riboseq_signal": [5.284999847412109, 5.284999847412109, 5.284999847412109, 3.5233399868011475, 3.5233399868011475, 3.5233399868011475, 3.5233399868011475, 3.5233399868011475, 3.5233399868011475, 3.5233399868011475, 3.5233399868011475, 3.5233399868011475, 3.5233399868011475, 3.5233399868011475, 1.7616699934005737, 1.7616699934005737, 1.7616699934005737, 1.7616699934005737, 1.7616699934005737, 1.7616699934005737, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}

```
对json进行格式处理.
```py
import json
import subprocess

def predict_structure(seq):
    """调用 RNAfold 预测 RNA 二级结构"""
    result = subprocess.run(['RNAfold'], input=seq.encode(), capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    structure = lines[1].split()[0]  # 第二行是 dot-bracket 表达式
    return structure

# 读取 JSON 输入
with open("input.json", "r") as f:
    data = json.load(f)

# 获取信号
rna_signal = data["rnaseq_signal"]
ribo_signal = data["riboseq_signal"]

# 判断是否全部为 0（跳过输出）
if all(v == 0.0 for v in rna_signal) and all(v == 0.0 for v in ribo_signal):
    print(f"Skip {data['transcript_id']} — RNA-seq and Ribo-seq signals all zero")
else:
    # 构建 transcript_seq
    transcript_seq = data["utr5"] + data["cds"] + data["utr3"]

    # 预测结构
    structure = predict_structure(transcript_seq)

    # 构建输出
    output = {
        "transcript_id": data["transcript_id"],
        "transcript_seq": transcript_seq,
        "structure": structure,
        "rnaseq_signal": rna_signal,
        "riboseq_signal": ribo_signal
    }

    # 输出为 JSONL
    with open("output.jsonl", "w") as f_out:
        f_out.write(json.dumps(output) + "\n")

```
# k562

```py

import json
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os
from Bio.Seq import Seq

# ===================== 用户自定义配置 =====================
input_jsonl = "k562_rna_ribo_features.jsonl"  # ✅ 输入 JSONL 文件
output_image_dir = "k562_rna_images"          # ✅ 图像输出目录
output_matrix_dir = "k562_rna_encoded"        # ✅ 编码矩阵输出目录
max_transcripts = None  # ✅ 限制处理的转录本数量，例如设为 100，仅处理前 100 个；为 None 表示处理全部
# =========================================================

# 创建输出目录
os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_matrix_dir, exist_ok=True)


def predict_structure(seq):
    """调用 RNAfold 预测 RNA 二级结构"""
    result = subprocess.run(['RNAfold'], input=seq, capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    structure = lines[1].split()[0]
    return structure

def predict_protein(seq):
    # 转换为 Biopython 序列对象并翻译
    dna_seq = Seq(seq)
    protein_seq = dna_seq.translate(to_stop=True)
    return protein_seq

def one_hot_base(base):
    return {'A':[1,0,0,0], 'C':[0,1,0,0], 'G':[0,0,1,0], 'U':[0,0,0,1]}.get(base, [0,0,0,0])

def one_hot_structure(dot):
    return {'.':[1,0,0], '(': [0,1,0], ')':[0,0,1]}.get(dot, [0,0,0])


def one_hot_amino23(acid):
    aa_dict = {
        'A': 0, 'R': 1, 'N': 2, 'D': 3, 'C': 4,
        'Q': 5, 'E': 6, 'G': 7, 'H': 8, 'I': 9,
        'L': 10, 'K': 11, 'M': 12, 'F': 13, 'P': 14,
        'S': 15, 'T': 16, 'W': 17, 'Y': 18, 'V': 19,
        '*': 20,  # stop codon
        '0': 21   # 非翻译区：UTR 标识
        # 可选扩展: '-' 可为22
    }
    vec = [0] * 23
    idx = aa_dict.get(acid.upper(), None)
    if idx is not None:
        vec[idx] = 1
    return vec

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



# 主循环：逐行读取 JSONL 文件
with open(input_jsonl, "r") as f:
    for idx, line in enumerate(f):
        if max_transcripts is not None and idx >= max_transcripts:
            break
        try:
            data = json.loads(line)
            rna_signal = data["rnaseq_signal"]
            ribo_signal = data["riboseq_signal"]
            transcript_id = data["transcript_id"]
            transcript_seq = data["utr5"] + data["cds"] + data["utr3"]

            # 跳过全为 0 的情况
            if all(v == 0.0 for v in rna_signal) and all(v == 0.0 for v in ribo_signal):
                print(f"⚠️ 跳过：{transcript_id} — 全部信号为 0")
                continue

            # 裁剪长度一致
            L = min(len(transcript_seq), len(rna_signal), len(ribo_signal))
            transcript_seq_dna=transcript_seq[:L]
            transcript_seq = transcript_seq[:L].replace('T', 'U')  # RNAfold 需要U
            rna_signal = rna_signal[:L]
            ribo_signal = ribo_signal[:L]

            # RNAfold 预测结构
            structure = predict_structure(transcript_seq)
            if len(structure) != len(transcript_seq):
                print(f"❌ 长度不一致，跳过 {transcript_id}")
                continue
            # protein sequence 预测
            protein_seq=predict_protein(data["cds"])
            # 编码
            encoded = encode_rna(transcript_seq, structure, rna_signal, ribo_signal)
            print("transcript_seq:"+transcript_seq+"\n")
            print("structure:"+structure+"\n")
            print("protein:"+protein_seq+"\n")
            print("rna_signal:",rna_signal)
            print("ribo_signal:",ribo_signal)

            # 保存图像
            image_path = os.path.join(output_image_dir, f"{transcript_id}.png")
            plt.figure(figsize=(10, 3))
            plt.imshow(encoded.T, aspect='auto', cmap='viridis')
            plt.xlabel("Position")
            plt.ylabel("Features: [A,C,G,U], [.,(,)], RNA, Ribo")
            plt.title(f"Transcript: {transcript_id}")
            plt.colorbar()
            plt.tight_layout()
            plt.savefig(image_path, dpi=300)
            plt.close()

            # 保存编码矩阵
            np.save(os.path.join(output_matrix_dir, f"{transcript_id}.npy"), encoded)

            print(f"✅ 已保存 {transcript_id}: 图像 -> {image_path}")
        except Exception as e:
            print(f"❗ 出错跳过：{data.get('transcript_id', 'unknown')} — {e}")


```
#

# HepG2


```py

import json
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os

# ===================== 用户自定义配置 =====================
input_jsonl = "hepG2_rna_ribo_features.jsonl"  # ✅ 输入 JSONL 文件
output_image_dir = "hepG2_rna_images"          # ✅ 图像输出目录
output_matrix_dir = "hepG2_rna_encoded"        # ✅ 编码矩阵输出目录
max_transcripts = None  # ✅ 限制处理的转录本数量，例如设为 100，仅处理前 100 个；为 None 表示处理全部
# =========================================================

# 创建输出目录
os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_matrix_dir, exist_ok=True)

def predict_structure(seq):
    """调用 RNAfold 预测 RNA 二级结构"""
    result = subprocess.run(['RNAfold'], input=seq, capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")
    structure = lines[1].split()[0]
    return structure

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

# 主循环：逐行读取 JSONL 文件
with open(input_jsonl, "r") as f:
    for idx, line in enumerate(f):
        if max_transcripts is not None and idx >= max_transcripts:
            break
        try:
            data = json.loads(line)
            rna_signal = data["rnaseq_signal"]
            ribo_signal = data["riboseq_signal"]
            transcript_id = data["transcript_id"]
            transcript_seq = data["utr5"] + data["cds"] + data["utr3"]

            # 跳过全为 0 的情况
            if all(v == 0.0 for v in rna_signal) and all(v == 0.0 for v in ribo_signal):
                print(f"⚠️ 跳过：{transcript_id} — 全部信号为 0")
                continue

            # 裁剪长度一致
            L = min(len(transcript_seq), len(rna_signal), len(ribo_signal))
            transcript_seq = transcript_seq[:L].replace('T', 'U')  # RNAfold 需要U
            rna_signal = rna_signal[:L]
            ribo_signal = ribo_signal[:L]

            # RNAfold 预测结构
            structure = predict_structure(transcript_seq)
            if len(structure) != len(transcript_seq):
                print(f"❌ 长度不一致，跳过 {transcript_id}")
                continue

            # 编码
            encoded = encode_rna(transcript_seq, structure, rna_signal, ribo_signal)

            # 保存图像
            image_path = os.path.join(output_image_dir, f"{transcript_id}.png")
            plt.figure(figsize=(10, 3))
            plt.imshow(encoded.T, aspect='auto', cmap='viridis')
            plt.xlabel("Position")
            plt.ylabel("Features: [A,C,G,U], [.,(,)], RNA, Ribo")
            plt.title(f"Transcript: {transcript_id}")
            plt.colorbar()
            plt.tight_layout()
            plt.savefig(image_path, dpi=300)
            plt.close()

            # 保存编码矩阵
            np.save(os.path.join(output_matrix_dir, f"{transcript_id}.npy"), encoded)

            print(f"✅ 已保存 {transcript_id}: 图像 -> {image_path}")
        except Exception as e:
            print(f"❗ 出错跳过：{data.get('transcript_id', 'unknown')} — {e}")

```

```py
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
```



