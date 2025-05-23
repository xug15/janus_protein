
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
SEQUENCE_LENGTH = 65536
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









