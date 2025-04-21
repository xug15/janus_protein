## 1. Download PDB files from PDB websites.

```sh
rsync -avz rsync.rcsb.org::ftp/data/structures/divided/pdb/ ./pdb/
```

## 2. Download the PDB protein informations.

(base) dell@dell-PowerEdge-R750xa:~/model/data/b1.pdbs/pdb_information$ cat a2.download.sh
```sh
#wget https://files.rcsb.org/pub/pdb/derived_data/pdb_seqres.txt.gz
#wget https://files.rcsb.org/pub/pdb/derived_data/pdb_entry_type.txt

#wget -r -np -nH --cut-dirs=5 -R "index.html*" https://files.rcsb.org/pub/pdb/derived_data/SG/
#wget -r -np -nH --cut-dirs=5 -R "index.html*" https://files.rcsb.org/pub/pdb/derived_data/index/
wget https://files.rcsb.org/pub/pdb/derived_data/SG/SgTargetsInPdb.txt

wget https://files.rcsb.org/pub/pdb/derived_data/index/author.idx
wget https://files.rcsb.org/pub/pdb/derived_data/index/cmpd_res.idx
wget https://files.rcsb.org/pub/pdb/derived_data/index/compound.idx
wget https://files.rcsb.org/pub/pdb/derived_data/index/crystal.idx
wget https://files.rcsb.org/pub/pdb/derived_data/index/entries.idx
wget https://files.rcsb.org/pub/pdb/derived_data/index/on_hold.list
wget https://files.rcsb.org/pub/pdb/derived_data/index/pending_waiting.list
wget https://files.rcsb.org/pub/pdb/derived_data/index/resolu.idx
wget https://files.rcsb.org/pub/pdb/derived_data/index/source.idx
wget https://files.rcsb.org/pub/pdb/derived_data/index/status_query.csv
wget https://files.rcsb.org/pub/pdb/derived_data/index/status_query.seq

```

## 3. The meaning of files of PDB files.

文件名 | 作用
--  |  --
author.idx | 每个 PDB 编号的第一作者
compound.idx / cmpd_res.idx | 每个结构的标题和复合物注释，有些含解析度
crystal.idx | 晶体学单位胞参数、空间群
entries.idx | 最全的信息，含 PDB ID、标题、作者、解析度、实验方法等
resolu.idx | PDB ID 与解析度（补充精确数据）
source.idx | 生物来源信息
pdb_seqres.txt | 含有序列信息（FASTA 格式），用于提取蛋白序列
status_query.csv/seq | 待发布结构，可能含功能、序列等补充注释

### 3.1 compound.idx

PROTEIN DATA BANK LIST OF IDCODE AND COMPOUND NAMES AS FOUND IN THE COMPOUND RECORDS
Fri Apr 11 10:58:43 EDT 2025
IDCODE |  COMPOUND
------  |-------------------------------------------------------------------------
7RWG   | ""Crystal structure of human methionine adenosyltransferase 2A (MAT2A) in complex with SAM and allosteric inhibitor AGI-43192
9DVJ  |  ""Structure of the phosphate exporter XPR1/SLC53A1
2QPS  |  ""Sugar tongs"" mutant Y380A in complex with acarbose

这段是来自 PDB（Protein Data Bank） 的 compound.idx 文件的一部分，用于记录每个结构条目（PDB ID）对应的复合物名称（Compound）或结构标题，它反映了结构研究的对象和功能背景。

列名 | 含义
--|--
IDCODE | PDB 编号，如 7RWG, 9DVJ，表示某个结构的唯一 ID。
COMPOUND | 对该结构的文字说明，通常是该蛋白结构、复合物、突变体的功能或实验描述。

🔹 7RWG：
中文翻译：人类甲硫氨酸腺苷转移酶 2A（MAT2A）与 SAM 及别构抑制剂 AGI-43192 的晶体结构

生物背景：MAT2A 是一类重要的甲基供体 SAM 的合成酶，在肿瘤代谢中有研究价值。

🔹 9DVJ：
中文翻译：磷酸盐输出蛋白 XPR1/SLC53A1 的结构

功能：XPR1 是一种磷酸盐跨膜转运蛋白，参与细胞内外磷酸平衡调控。

🔹 2QPS：
中文翻译：“糖钳”突变体 Y380A 与阿卡波糖的复合物结构

说明：Y380A 是一种定点突变，研究其与阿卡波糖（一种α-葡萄糖苷酶抑制剂）结合方式。

### 3.2 cmpd_res.idx

PROTEIN DATA BANK LIST OF IDCODE, RESOLUTION, AND COMPOUND NAMES
Fri Apr 11 10:58:47 EDT 2025

IDCODE  |     RESOLUTION    |     COMPOUND 
------|  ----------   | --------------------------------------
7RWG    ;|       0.97    ; |      ""Crystal structure of human methionine adenosyltransferase 2A (MAT2A) in complex with SAM and allosteric inhibitor AGI-43192
9DVJ    ; |      2.52    ; |      ""Structure of the phosphate exporter XPR1/SLC53A1
2QPS    ; |      2.2     ; |      ""Sugar tongs"" mutant Y380A in complex with acarbose
6F4G    ; |      1.9     ; |      'Crystal structure of the Drosophila melanogaster SNF/U2A'/U2-SL4 complex
7W7V    ;  |     3.0     ; |      'late' E2P of SERCA2b
5NQ2    ;  |     1.54    ; |      'Porcine (Sus scrofa) Major Histocompatibility Complex, class I, presenting IAYERMCNI

字段名 | 示例 | 含义
--     |   --|-- 
IDCODE | 7RWG | PDB 的结构编号，是一个 4 位或更多位的代码，用于唯一标识一个蛋白质或复合物结构
RESOLUTION | 0.97 | 结构解析度（单位是 Å），数值越低，表示结构越精细、质量越好（仅适用于 X-ray）
COMPOUND | "Crystal structure of..." | 对该结构的简要描述，包括研究对象（蛋白名、复合物、突变、配体等）


7RWG
解析度：0.97 Å（非常高精度）

结构名称：Crystal structure of human methionine adenosyltransferase 2A (MAT2A) in complex with SAM and allosteric inhibitor AGI-43192

中文：人甲硫氨酸腺苷转移酶2A（MAT2A）与 SAM 及别构抑制剂 AGI-43192 的晶体结构

🔹 9DVJ
解析度：2.52 Å

结构名称：Structure of the phosphate exporter XPR1/SLC53A1

中文：磷酸盐输出转运蛋白 XPR1/SLC53A1 的结构

🔹 2QPS
解析度：2.2 Å

结构名称：“Sugar tongs” mutant Y380A in complex with acarbose

中文：“糖钳”样突变体 Y380A 与阿卡波糖的复合物结构（阿卡波糖是一种抗糖尿病药物）

🔹 6F4G
解析度：1.9 Å

结构名称：Crystal structure of the Drosophila melanogaster SNF/U2A'/U2-SL4 complex

中文：果蝇 SNF/U2A'/U2-SL4 RNA 结合复合物的晶体结构

🔹 7W7V
解析度：3.0 Å

结构名称："late" E2P of SERCA2b

中文：SERCA2b 的 E2P 状态结构（钙泵的后期磷酸化状态）

🔹 5NQ2
解析度：1.54 Å

结构名称：Porcine (Sus scrofa) Major Histocompatibility Complex, class I, presenting IAYERMCNI

中文：猪 MHC-I（主要组织相容性复合物 I 类）呈递 IAYERMCNI 肽段的结构

### 3.3 crystal.idx
crystal.idx | 晶体学单位胞参数、空间群


