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
这段内容是 PDB 中晶体学信息文件的一部分，通常称作 crystal.idx 或 unit_cell_parameters.idx，记录的是：

蛋白质晶体结构的晶胞参数（unit cell parameters）和空间群（space group）

用于描述晶体在三维空间中的几何结构和对称性。
```sh
(base) dell@dell-PowerEdge-R750xa:~/model/data/b1.pdbs/pdb_information$ head crystal.idx
```
PROTEIN DATA BANK LIST OF CRYSTAL UNIT CELL PARAMETERS
Fri Apr 11 10:58:54 EDT 2025
idcode | x  |    a   |      b  |       c   |    alpha  |   beta   |  gamma  |  sp.gp.   |    Z
------ | ------|--    |  -----  |   -----   |    -----  |   -----  |   -----  |  -----   |  ------ 
100D   | CRYST1   | 23.980  |  40.770  |  44.840  |  90.000  |  90.000   | 90.000 | P 21 21 21  | 8
101D   | CRYST1   | 24.270  |  39.620  |  63.570  |  90.000  |  90.000  |  90.000  |P 21 21 21  | 8
101M   | CRYST1   | 91.670  |  91.670  |  45.970 |   90.000  |  90.000   |120.000 | P 6         | 6
102D   | CRYST1   |  24.780 |  41.160  |  65.510  |  90.000  |  90.000  |  90.000 | P 21 21 21  | 8
102L   | CRYST1   | 60.900  |  60.900   | 96.100  |  90.000   | 90.000  | 120.000 | P 32 2 1    | 6

100D
晶胞边长 a/b/c：23.980 / 40.770 / 44.840 Å

三角度 α/β/γ：90.000 / 90.000 / 90.000 度 → 正交晶系（Orthorhombic）

空间群：P 21 21 21 → 表示晶体对称性是最常见的 P212121

Z = 8 → 晶胞中有 8 个不对称单元

### 3.4 entries.idx 
| 最全的信息，含 PDB ID、标题、作者、解析度、实验方法等
编号、标题、提交日期、复合物名称、来源、作者、分辨率、实验类型等。

字段名	|示例值	|含义说明
-- | -- | -- 
IDCODE	|100D	|PDB 编号，结构的唯一标识符
HEADER|	DNA-RNA HYBRID	|简要的结构类别（通常是功能分类）
ACCESSION DATE	|12/05/94	|数据入库日期（提交到 PDB 的时间）
COMPOUND	|CRYSTAL STRUCTURE OF...	|结构名称、研究对象的详细说明
SOURCE|	Physeter catodon 或 Enterobacteria phage T4	|生物来源（物种或系统）
AUTHOR LIST|	Smith, R.D., Olson, J.S., ...	|发表该结构的研究作者
RESOLUTION	|1.9, 2.25, NOT	|分辨率（仅适用于 X-ray 结构；NMR为"NOT"）
EXPERIMENT TYPE|	X-RAY DIFFRACTION, SOLUTION NMR	|实验方法，用于解析蛋白质三维结构的技术

项目 | 内容
-- | -- 
ID | 101M
类型 | OXYGEN TRANSPORT（氧运输蛋白）
来源 | 抹香鲸 (Physeter catodon)
名称 | 抹香鲸肌红蛋白 F46V 突变体与正丁基异氰化物结合结构（pH 9.0）
分辨率 | 2.07 Å
方法 | X-RAY DIFFRACTION

### 3.5 resolu.idx 
| PDB ID 与解析度（补充精确数据）
💡 PDB ID 与结构解析度的对应表

```sh
(base) dell@dell-PowerEdge-R750xa:~/model/data/b1.pdbs/pdb_information$ head resolu.idx
```

PROTEIN DATA BANK LIST OF IDCODES AND DATA RESOLUTION VALUES
Fri Apr 11 10:59:11 EDT 2025
RESOLUTION VALUE IS -1.00 FOR ENTRIES DERIVED FROM NMR AND OTHER EXPERIMENT METHODS (NOT INCLUDING X-RAY) IN WHICH THE FIELD REFINE.LS_D_RES_HIGH IS EMPTY

IDCODE |      RESOLUTION
------  |    ----------
100D    ;|       1.9
101D    ;|       2.25
101M    ;|       2.07
102D    ;|       2.2

字段 | 示例 | 含义
--   |  -- |  --
IDCODE | 100D | 蛋白质结构的 PDB 编号（唯一标识）
RESOLUTION | 1.9 | 该结构的解析度，单位为埃（Å）

PDB ID | Resolution (Å) | 说明
--    | ----            | ---
100D | 1.90 Å | 解析度非常高，结构清晰可靠
101D | 2.25 Å | 中等精度结构
101M | 2.07 Å | 好的结构质量（常用于建模）

### 3.6 source.idx 
| 生物来源信息

PROTEIN DATA BANK LIST OF IDCODE AND SOURCE NAMES AS FOUND IN THE COMPOUND RECORDS
Fri Apr 11 10:56:35 EDT 2025


IDCODE | SOURCE
------ | -----------------------------------------------------------------
100D|
101D|
101M|  Physeter catodon
102D|
102L |   Enterobacteria phage T4
102M |   Physeter catodon


### 3.7 pdb_seqres.txt 
| 含有序列信息（FASTA 格式），用于提取蛋白序列
```sh
(base) dell@dell-PowerEdge-R750xa:~/model/data/b1.pdbs/pdb_information$ head -n 20 pdb_seqres.txt
```
```txt
>100d_A mol:na length:10  DNA/RNA (5'-R(*CP*)-D(*CP*GP*GP*CP*GP*CP*CP*GP*)-R(*G)-3')
CCGGCGCCGG
>100d_B mol:na length:10  DNA/RNA (5'-R(*CP*)-D(*CP*GP*GP*CP*GP*CP*CP*GP*)-R(*G)-3')
CCGGCGCCGG
>101d_A mol:na length:12  DNA (5'-D(*CP*GP*CP*GP*AP*AP*TP*TP*(CBR)P*GP*CP*G)-3')
CGCGAATTCGCG
>101d_B mol:na length:12  DNA (5'-D(*CP*GP*CP*GP*AP*AP*TP*TP*(CBR)P*GP*CP*G)-3')
CGCGAATTCGCG
>101m_A mol:protein length:154  MYOGLOBIN
MVLSEGEWQLVLHVWAKVEADVAGHGQDILIRLFKSHPETLEKFDRVKHLKTEAEMKASEDLKKHGVTVLTALGAILKKKGHHEAELKPLAQSHATKHKIPIKYLEFISEAIIHVLHSRHPGNFGADAQGAMNKALELFRKDIAAKYKELGYQG
>102d_A mol:na length:12  DNA (5'-D(*CP*GP*CP*AP*AP*AP*TP*TP*TP*GP*CP*G)-3')
CGCAAATTTGCG
>102d_B mol:na length:12  DNA (5'-D(*CP*GP*CP*AP*AP*AP*TP*TP*TP*GP*CP*G)-3')
CGCAAATTTGCG
>102l_A mol:protein length:165  T4 LYSOZYME
MNIFEMLRIDEGLRLKIYKDTEGYYTIGIGHLLTKSPSLNAAAKSELDKAIGRNTNGVITKDEAEKLFNQDVDAAVRGILRNAKLKPVYDSLDAVRRAALINMVFQMGETGVAGFTNSLRMLQQKRWDEAAVNLAKSRWYNQTPNRAKRVITTFRTGTWDAYKNL
>102m_A mol:protein length:154  MYOGLOBIN
MVLSEGEWQLVLHVWAKVEADVAGHGQDILIRLFKSHPETLEKFDRFKHLKTEAEMKASEDLKKAGVTVLTALGAILKKKGHHEAELKPLAQSHATKHKIPIKYLEFISEAIIHVLHSRHPGNFGADAQGAMNKALELFRKDIAAKYKELGYQG
>103d_A mol:na length:12  DNA (5'-D(*GP*TP*GP*GP*AP*AP*TP*GP*GP*AP*AP*C)-3')
GTGGAATGGAAC
```
### 3.8 status_query.csv/seq 
| 待发布结构，可能含功能、序列等补充注释
```sh
(base) dell@dell-PowerEdge-R750xa:~/model/data/b1.pdbs/pdb_information$ head status_query.csv
```
```csv
'Structure_ID','pdb_id','status_code','initial_deposition_date','date_hold_coordinates','date_struct_fact','date_hold_struct_fact','date_nmr_constraints','date_hold_nmr_constraints','date_of_RCSB_release','author_list','title','author_release_sequence'
'PDB2CX2','2CX2','WDRN','1998-04-24','n/a','n/a','n/a','n/a','n/a','n/a','McKeever, B.M., Pandya, S.R., Percival, M.D., Ouellet, M., Bayly, C., O''Neill, G.P., Bastien, L., Kennedy, B.P., Adam, M., Cromlish, W., Roy, P., Black, W.C., Guay, D., Leblanc, Y.','CYCLOOXYGENASE-2 (PROSTAGLANDIN SYNTHASE-2) COMPLEXED WITH A BENZYL-INDOLE INHIBITOR, L-758048','n/a'
'PDB1BJS','1BJS','WDRN','1998-06-29','n/a','n/a','n/a','n/a','n/a','n/a','Liang, J., Kongsaeree, P., Guo, W., Clardy, J.','CRYSTAL STRUCTURE OF CYCLOHEXADIENYL DEHYDRATASE','n/a'
'PDB2DIH','2DIH','WDRN','1998-08-25','n/a','n/a','n/a','n/a','n/a','n/a','Scapin, G., Zheng, R., Blanchard, J.S.','M. TUBERCULOSIS DIHYDRODIPICOLINATE REDUCTASE IN COMPLEX WITH NADH AND THE INHIBITOR 2,6 PYRIDINE DICARBOXYLATE','n/a'
'PDB2NP4','2NP4','WDRN','1998-09-14','n/a','1998-09-14','n/a','n/a','n/a','n/a','Weichsel, A., Andersen, J.F., Roberts, S.A., Montfort, W.R.','CRYSTAL STRUCTURE OF NITROPHORIN 4 FROM RHODNIUS PROLIXUS','n/a'
'PDB2ERU','2ERU','WDRN','1998-10-21','n/a','n/a','n/a','n/a','n/a','n/a','Sotelo-Mundo, R.R., Montfort, W.R.','HUMAN THIOREDOXIN (OXIDIZED FORM)','n/a'
'PDB1B2Q','1B2Q','WDRN','1998-12-02','n/a','1998-12-02','n/a','n/a','n/a','n/a','Silvian, L.F., Wang, J., Steitz, T.A.','ISOLEUCINYL TRNA SYNTHETASE/TRNA COMPLEX','n/a'
'PDB450D','450D','WDRN','1999-01-20','n/a','1999-01-20','n/a','n/a','n/a','n/a','Clark, G.R., Squire, C.J., Martin, R.F., White, J., Kelly, D., Reum, M., Sy, D., Sptheim- Maurizot, M.','5''-D(*CP*GP*CP*GP*AP*AP*TP*TP*CP*GP*CP*G)-3''','n/a'
'PDB451D','451D','WDRN','1999-01-20','n/a','1999-01-20','n/a','n/a','n/a','n/a','Clark, G.R., Squire, C.J., Martin, R.F., White, J., Kelly, D., Reum, M., Sy, D., Sptheim- Maurizot, M.','5''-D(*CP*GP*CP*GP*AP*AP*TP*TP*CP*GP*CP*G)-3''','n/a'
'PDB1B7W','1B7W','WDRN','1999-01-26','n/a','n/a','n/a','n/a','n/a','n/a','Ha, Y., Shi, D., Allewell, N.M.','CRYSTAL STRUCTURE OF M FERRITIN','n/a'
```
字段名 | 示例 | 含义
--    |  --  | --
Structure_ID | PDB2CX2 | 内部结构编号（有时带有数据库前缀）
pdb_id | 2CX2 | PDB ID，结构的唯一标识符
status_code | WDRN | 状态码，如 WDRN 表示“Withdrawn”（已撤回）或未发布
initial_deposition_date | 1998-04-24 | 初次提交时间
date_hold_coordinates 等 | n/a | 各类“延迟公开”的时间控制字段
date_of_RCSB_release | n/a | 真正发布到 RCSB 的时间（如未发布则为 n/a）
author_list | McKeever, B.M., ... | 作者信息
title | 结构名称（功能或复合物描述） | 
author_release_sequence | n/a | 是否作者提交了序列并允许公开（可为空）

字段 | 含义
--  | --
2CX2 | 结构编号
WDRN | 状态为 Withdrawn，即该结构未正式发布或被撤回
初次提交时间 | 1998-04-24
title | 该结构是：环氧合酶-2（COX-2）与一种苄基吲哚类抑制剂 L-758048 的复合物结构
author_list | 多位作者

### 3.9 status_query.seq  
```sh
(base) dell@dell-PowerEdge-R750xa:~/model/data/b1.pdbs/pdb_information$ grep -A 1 ">" status_query.seq |head -n 18
``` 
```fa
>8G7Z Entity 1
MALPRCMWPNYVWRAMMACVVHRGSGAPLTLCLLGCLLQTFHVLSQKYPYDVPDYAQRGGGGPGGGAPGGPGLGLGSLGE
>8G7Z Entity 2
MYQRMLRCGADLGSPGGGSGGGAGGRLALIWIVPLTLGGLLGVAWGASSLGAHHIHHFHGSSKEFEQKLISEEDLGFEID
>8RZZ Entity 1
MDLAKLGLKEVMPTKINLEGLVGDHAFSMEGVGEGNILEGTQEVKISVTKGAPLPFAFDIVSVAF(CRO)NRAYTGYPEE
>8RZZ Entity 2
MTSKVYDPEQRKRMITGPQWWARCKQMNVLDSFINYYDSEKHAENAVIFLHGNATSSYLWRHVVPHIEPVARCIIPDLIG
>8VRP Entity 1
PIVQNLQGQMVHQCISPRTLNAWVKVVEEKAFSPEVIPMFSALSCGATPQDLNTMLNTVGGHQAAMQMLKETINEEAAEW
>8XJT Entity 1
MGSSHHHHHHSSGLVPRGSHMASMTGGQQMGRGSEFELRRQALEYASEMNGMEIAIIGMAVRFPQSRTLHEFWHNIVQGK
```


































