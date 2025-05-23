
##第一步：解析 GFF3，提取转录本结构（UTR/CDS）
import gffutils
from itertools import chain

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

def sort_features(features):
    if not features:
        return features
    reverse = features[0].strand == '-'
    return sorted(features, key=lambda f: f.start, reverse=reverse)

## 第三步：提取 Ribo-seq & RNA-seq 信号（pyBigWig）
import pyBigWig

#bw_rna = pyBigWig.open("/home/dell/model/script/Translatomer-main/data/hg38/K562/GSE153597/input_features/K562_GSE153597_rnaseq.bw")
#bw_ribo = pyBigWig.open("/home/dell/model/script/Translatomer-main/data/hg38/K562/GSE153597/input_features/K562_GSE153597_riboseq.bw")


bw_rna = pyBigWig.open("/home/dell/model/script/Translatomer-main/data/hg38/HepG2/GSE174419/input_features/HepG2_GSE174419_rnaseq.bw")
bw_ribo = pyBigWig.open("/home/dell/model/script/Translatomer-main/data/hg38/HepG2/GSE174419/output_features/HepG2_GSE174419_riboseq.bw")

def extract_signal(bw, chrom, start, end, strand):
    return bw.values(chrom, start, end, numpy=True).tolist()
def extract_signal(bw, chrom, start, end, strand):
    if strand == '+':
        return bw.values(chrom, start, end, numpy=True).tolist()
    elif strand == '-':
        # 反向链：起始和终止位置顺序调换 + 翻转值方向
        values = bw.values(chrom, start, end, numpy=True).tolist()
        return values[::-1]
    else:
        raise ValueError(f"Invalid strand: {strand}")



## 第四步：生成 JSONL 文件
import json
from tqdm import tqdm

output_jsonl = "HepG2_rna_ribo_features.jsonl"
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

        #if tid != 'ENST00000327044.7':
        #    continue

        #print("tid",tid)
        #print("transcript",transcript)
        # 取序列
        cds_seq = ''.join([extract_sequence(f.chrom, f.start - 1, f.end, f.strand) for f in sort_features(cds)])
        utr5_seq = ''.join([extract_sequence(f.chrom, f.start - 1, f.end, f.strand) for f in sort_features(utr5)])
        utr3_seq = ''.join([extract_sequence(f.chrom, f.start - 1, f.end, f.strand) for f in sort_features(utr3)])

        # 提取信号
        

        start = transcript.start - 1
        end = transcript.end
        rnaseq_signal_cds = list(chain.from_iterable([extract_signal(bw_rna,f.chrom,f.start-1,f.end, f.strand) for f in sort_features(cds)]))
        rnaseq_signal_utr5 =list(chain.from_iterable([extract_signal(bw_rna,f.chrom,f.start-1,f.end, f.strand) for f in sort_features(utr5) ]))
        rnaseq_signal_utr3 =list(chain.from_iterable([extract_signal(bw_rna,f.chrom,f.start-1,f.end, f.strand) for f in sort_features(utr3) ]))
        rnaseq_signal=list(chain(rnaseq_signal_utr5,  rnaseq_signal_cds, rnaseq_signal_utr3))

        #print("rnaseq_signal_utr5",rnaseq_signal_utr5)
        #print("rnaseq_signal_utr3",rnaseq_signal_utr3)
        #print("rnaseq_signal_cds",rnaseq_signal_cds)
        #print("rnaseq_signal",rnaseq_signal)

        riboseq_signal_cds = list(chain.from_iterable([extract_signal(bw_ribo,f.chrom,f.start-1,f.end, f.strand) for f in sort_features(cds)]))
        riboseq_signal_utr5 =list(chain.from_iterable([extract_signal(bw_ribo,f.chrom,f.start-1,f.end, f.strand) for f in sort_features(utr5) ]))
        riboseq_signal_utr3 =list(chain.from_iterable([extract_signal(bw_ribo,f.chrom,f.start-1,f.end, f.strand) for f in sort_features(utr3) ]))
        riboseq_signal=list(chain(riboseq_signal_utr5,  riboseq_signal_cds, riboseq_signal_utr3))
        #print("riboseq_signal_utr5",riboseq_signal_utr5)
        #print("riboseq_signal_utr3",riboseq_signal_utr3)
        #print("riboseq_signal_cds",riboseq_signal_cds)
        #print("riboseq_signal",riboseq_signal)


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







