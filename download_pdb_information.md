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

```txt
PROTEIN DATA BANK LIST OF IDCODE AND COMPOUND NAMES AS FOUND IN THE COMPOUND RECORDS
Fri Apr 11 10:58:43 EDT 2025
IDCODE  COMPOUND
------  -------------------------------------------------------------------------
7RWG    ""Crystal structure of human methionine adenosyltransferase 2A (MAT2A) in complex with SAM and allosteric inhibitor AGI-43192
9DVJ    ""Structure of the phosphate exporter XPR1/SLC53A1
2QPS    ""Sugar tongs"" mutant Y380A in complex with acarbose
6F4G    'Crystal structure of the Drosophila melanogaster SNF/U2A'/U2-SL4 complex
7W7V    'late' E2P of SERCA2b
5NQ2    'Porcine (Sus scrofa) Major Histocompatibility Complex, class I, presenting IAYERMCNI

```

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

```txt
PROTEIN DATA BANK LIST OF IDCODE, RESOLUTION, AND COMPOUND NAMES
Fri Apr 11 10:58:47 EDT 2025
IDCODE       RESOLUTION         COMPOUND
------  -    ---------- -       --------------------------------------
7RWG    ;       0.97    ;       ""Crystal structure of human methionine adenosyltransferase 2A (MAT2A) in complex with SAM and allosteric inhibitor AGI-43192
9DVJ    ;       2.52    ;       ""Structure of the phosphate exporter XPR1/SLC53A1
2QPS    ;       2.2     ;       ""Sugar tongs"" mutant Y380A in complex with acarbose
6F4G    ;       1.9     ;       'Crystal structure of the Drosophila melanogaster SNF/U2A'/U2-SL4 complex
7W7V    ;       3.0     ;       'late' E2P of SERCA2b
5NQ2    ;       1.54    ;       'Porcine (Sus scrofa) Major Histocompatibility Complex, class I, presenting IAYERMCNI
```

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
```txt
PROTEIN DATA BANK LIST OF CRYSTAL UNIT CELL PARAMETERS
Fri Apr 11 10:58:54 EDT 2025
idcode              a         b         c       alpha     beta     gamma    sp.gp.       Z
------  ------    -----     -----     -----     -----     -----    -----    ------       -
100D    CRYST1    23.980    40.770    44.840    90.000    90.000    90.000  P 21 21 21   8
101D    CRYST1    24.270    39.620    63.570    90.000    90.000    90.000  P 21 21 21   8
101M    CRYST1    91.670    91.670    45.970    90.000    90.000   120.000  P 6          6
102D    CRYST1    24.780    41.160    65.510    90.000    90.000    90.000  P 21 21 21   8
102L    CRYST1    60.900    60.900    96.100    90.000    90.000   120.000  P 32 2 1     6
102M    CRYST1    91.433    91.433    45.949    90.000    90.000   120.000  P 6          6
```
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
```txt
IDCODE, HEADER, ACCESSION DATE, COMPOUND, SOURCE, AUTHOR LIST, RESOLUTION, EXPERIMENT TYPE (IF NOT X-RAY)
------- ------- --------------- --------- ------- ------------ ----------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
100D    DNA-RNA HYBRID  12/05/94        CRYSTAL STRUCTURE OF THE HIGHLY DISTORTED CHIMERIC DECAMER R(C)D(CGGCGCCG)R(G)-SPERMINE COMPLEX-SPERMINE BINDING TO PHOSPHATE ONLY AND MINOR GROOVE TERTIARY BASE-PAIRING               Ban, C., Ramakrishnan, B., Sundaralingam, M.    1.9     X-RAY DIFFRACTION
101D    DNA     12/14/94        REFINEMENT OF NETROPSIN BOUND TO DNA: BIAS AND FEEDBACK IN ELECTRON DENSITY MAP INTERPRETATION          Goodsell, D.S., Kopka, M.L., Dickerson, R.E.    2.25    X-RAY DIFFRACTION
101M    OXYGEN TRANSPORT        12/13/97        SPERM WHALE MYOGLOBIN F46V N-BUTYL ISOCYANIDE AT PH 9.0 Physeter catodonSmith, R.D., Olson, J.S., Phillips Jr., G.N.    2.07    X-RAY DIFFRACTION
102D    DNA     12/15/94        SEQUENCE-DEPENDENT DRUG BINDING TO THE MINOR GROOVE OF DNA: THE CRYSTAL STRUCTURE OF THE DNA DODECAMER D(CGCAAATTTGCG)2 COMPLEXED WITH PROPAMIDINE              Nunn, C.M., Neidle, S.  2.2     X-RAY DIFFRACTION
102L    HYDROLASE(O-GLYCOSYL)   09/29/92        HOW AMINO-ACID INSERTIONS ARE ALLOWED IN AN ALPHA-HELIX OF T4 LYSOZYME Enterobacteria phage T4  Heinz, D.W., Matthews, B.W.     1.74    X-RAY DIFFRACTION
102M    OXYGEN TRANSPORT        12/15/97        SPERM WHALE MYOGLOBIN H64A AQUOMET AT PH 9.0    Physeter catodon       Smith, R.D., Olson, J.S., Phillips Jr., G.N.     1.84    X-RAY DIFFRACTION
103D    DNA     12/16/94        THE UNUSUAL STRUCTURE OF THE HUMAN CENTROMERE (GGA)2 MOTIF: UNPAIRED GUANOSINE RESIDUES STACKED BETWEEN SHEARED G(DOT)A PAIRS           Chou, S.-H., Zhu, L., Reid, B.R.        NOT     SOLUTION NMR
103L    HYDROLASE(O-GLYCOSYL)   09/29/92        HOW AMINO-ACID INSERTIONS ARE ALLOWED IN AN ALPHA-HELIX OF T4 LYSOZYME Enterobacteria phage T4  Heinz, D.W., Matthews, B.W.     1.9     X-RAY DIFFRACTION
```
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
```txt
PROTEIN DATA BANK LIST OF IDCODES AND DATA RESOLUTION VALUES
Fri Apr 11 10:59:11 EDT 2025
RESOLUTION VALUE IS -1.00 FOR ENTRIES DERIVED FROM NMR AND OTHER EXPERIMENT METHODS (NOT INCLUDING X-RAY) IN WHICH THE FIELD REFINE.LS_D_RES_HIGH IS EMPTY

IDCODE       RESOLUTION
------  -    ----------
100D    ;       1.9
101D    ;       2.25
101M    ;       2.07
102D    ;       2.2
```
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

```txt
PROTEIN DATA BANK LIST OF IDCODE AND SOURCE NAMES AS FOUND IN THE COMPOUND RECORDS
Fri Apr 11 10:56:35 EDT 2025
IDCODE  SOURCE
------  -----------------------------------------------------------------
100D
101D
101M    Physeter catodon
102D
102L    Enterobacteria phage T4
102M    Physeter catodon
```
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
```
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
### 3.8 status_query.csv
| 待发布结构，可能含功能、序列等补充注释
```txt
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
```txt
>8G7Z Entity 1
MALPRCMWPNYVWRAMMACVVHRGSGAPLTLCLLGCLLQTFHVLSQKYPYDVPDYAQRGGGGPGGGAPGGPGLGLGSLGE
ERFPVVNTAYGRVRGVRRELNNEILGPVVQFLGVPYATPPLGARRFQPPEAPASWPGVRNATTLPPACPQNLHGALPAIM
LPVWFTDNLEAAATYVQNQSEDCLYLNLYVPTEDDIRDSGKKPVMLFLHGGSYMEGTGNMFDGSVLAAYGNVIVVTLNYR
LGVLGFLSTGDQAAKGNYGLLDQIQALRWLSENIAHFGGDPERITIFGSGAGASCVNLLILSHHSEGLFQKAIAQSGTAI
SSWSVNYQPLKYTRLLAAKVGCDREDSTEAVECLRRKSSRELVDQDVQPARYHIAFGPVVDGDVVPDDPEILMQQGEFLN
YDMLIGVNQGEGLKFVEDSAESEDGVSASAFDFTVSNFVDNLYGYPEGKDVLRETIKFMYTDWADRDNGEMRRKTLLALF
TDHQWVAPAVATAKLHADYQSPVYFYTFYHHCQAEGRPEWADAAHGDELPYVFGVPMVGATDLFPCNFSKNDVMLSAVVM
TYWTNFAKTGDPNQPVPQDTKFIHTKPNRFEEVVWSKFNSKEKQYLHIGLKPRVRDNYRANKVAFWLELVPHLHNLHTEL
FTTTTRLPPYATRWPPRTPGPGTSGTRRPPPPATLPPESDIDLGPRAYDRFPGDSRDYSTELSVTVAVGASLLFLNILAF
```
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


## 4. Transfer PDB into png

Unzip pdb files.

```sh

dbpath='/home/dell/model/data/b1.pdbs/pdb'
output='/home/dell/model/data/b1.pdbs/pdb_list'

for folder in `ls ${dbpath}`;
do
echo ${folder}
    for pdb in `ls ${dbpath}/${folder}|grep gz`;
        do
        echo "${dbpath}/${folder}/${pdb}"
        filename=${pdb}
        id=${filename#pdb}             # 去除前缀pdb → 100d.ent.gz
        id=${id%.ent.gz}               # 去除后缀.ent.gz → 100d
        id_upper=$(echo "$id" | tr 'a-z' 'A-Z')  # 转换为大写 → 100D

        echo "$id_upper"
        echo "gunzip -c ${dbpath}/${folder}/${pdb} > ${output}/${id_upper}.pdb "
        gunzip -c ${dbpath}/${folder}/${pdb} > ${output}/${id_upper}.pdb
        done
done
```
convert pdb into 6 angle pictures into one image
```sh
conda activate pymol_env 
#or
conda activate /home/dell/.conda/envs/pymol_env

```
```py
import os
import glob
from PIL import Image, ImageDraw, ImageFont
import pymol2  # 使用 pymol-open-source

input_dir = "/home/dell/model/data/b1.pdbs/pdb_list"
single_output_dir = "/home/dell/model/data/b2.pdb_all_single"
merged_output_dir = "/home/dell/model/data/b3.pdb_all_merge_images/"
os.makedirs(single_output_dir, exist_ok=True)
os.makedirs(merged_output_dir, exist_ok=True)

# 定义6个角度的旋转操作
rotations = {
    "front":  (0, 0),
    "back":   (180, 0),
    "left":   (-90, 0),
    "right":  (180, 0),
    "top":    (90, 90),
    "bottom": (0, 180),
}


# 加载字体
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font = ImageFont.truetype(font_path, 20)

with pymol2.PyMOL() as pymol:
    pymol.cmd.bg_color("white")
    pdb_files = glob.glob(os.path.join(input_dir, "*.pdb"))

    for pdb_file in pdb_files:
        name = os.path.splitext(os.path.basename(pdb_file))[0]
        pymol.cmd.reinitialize()
        pymol.cmd.load(pdb_file, name)
        pymol.cmd.hide("everything", name)
        pymol.cmd.show("cartoon", name)
        pymol.cmd.color("blue", name)
        pymol.cmd.orient(name)
        pymol.cmd.zoom(name, 2.0)

        img_paths = []
        for view_name, (yaw, pitch) in rotations.items():
            pymol.cmd.turn("y", yaw)
            pymol.cmd.turn("x", pitch)
            img_path = os.path.join(single_output_dir, f"{name}_{view_name}.png")
            pymol.cmd.png(img_path, width=512, height=512, dpi=300, ray=0)
            img_paths.append((img_path, view_name))
            print(f"✅ Rendered: {img_path}")

        # 拼接图片（每行2张，3行，共6张）
        width, height = 512, 512
        spacing = 10
        merged_img = Image.new("RGB", (2 * width + spacing, 3 * height + 2 * spacing), color="white")

        for idx, (img_path, view_name) in enumerate(img_paths):
            img = Image.open(img_path).convert("RGBA")
            bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
            bg.paste(img, mask=img)
            final_img = bg.convert("RGB")

            # 添加标注文字
            draw = ImageDraw.Draw(final_img)
            draw.text((10, 10), view_name, font=font, fill="black")

            row, col = divmod(idx, 2)
            x = col * (width + spacing)
            y = row * (height + spacing)
            merged_img.paste(final_img, (x, y))

        merged_path = os.path.join(merged_output_dir, f"{name}_merged.png")
        merged_img.save(merged_path)
        print(f"🧩 Merged image saved: {merged_path}")

```
多进程
```sh
conda activate pymol_env 
#or
conda activate /home/dell/.conda/envs/pymol_env
```
```py
import os
import glob
import multiprocessing as mp
from PIL import Image, ImageDraw, ImageFont

# 配置路径
input_dir = "/home/dell/model/data/b1.pdbs/pdb_list"
single_output_dir = "/home/dell/model/data/b2.pdb_all_single"
merged_output_dir = "/home/dell/model/data/b3.pdb_all_merge_images"
os.makedirs(single_output_dir, exist_ok=True)
os.makedirs(merged_output_dir, exist_ok=True)

# 加载字体
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font = ImageFont.truetype(font_path, 20)

# 六视角
rotations = {
    "front": (0, 0),
    "back": (180, 0),
    "left": (-90, 0),
    "right": (180, 0),
    "top": (90, 90),
    "bottom": (0, 180),
}

def render_pdb(pdb_file):
    import pymol2  # 必须在子进程内部导入
    name = os.path.splitext(os.path.basename(pdb_file))[0]

    with pymol2.PyMOL() as pymol:
        pymol.cmd.bg_color("white")
        pymol.cmd.reinitialize()
        pymol.cmd.load(pdb_file, name)
        pymol.cmd.hide("everything", name)
        pymol.cmd.show("cartoon", name)
        pymol.cmd.color("blue", name)
        pymol.cmd.orient(name)
        pymol.cmd.zoom(name, 2.0)

        img_paths = []
        for view_name, (yaw, pitch) in rotations.items():
            pymol.cmd.turn("y", yaw)
            pymol.cmd.turn("x", pitch)
            img_path = os.path.join(single_output_dir, f"{name}_{view_name}.png")
            pymol.cmd.png(img_path, width=512, height=512, dpi=300, ray=0)
            img_paths.append((img_path, view_name))
            print(f"✅ {name} - {view_name}")

    # 拼图（主图合成不依赖 PyMOL）
    width, height = 512, 512
    spacing = 10
    merged_img = Image.new("RGB", (2 * width + spacing, 3 * height + 2 * spacing), color="white")

    for idx, (img_path, view_name) in enumerate(img_paths):
        img = Image.open(img_path).convert("RGBA")
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        bg.paste(img, mask=img)
        final_img = bg.convert("RGB")

        draw = ImageDraw.Draw(final_img)
        draw.text((10, 10), view_name, font=font, fill="black")

        row, col = divmod(idx, 2)
        x = col * (width + spacing)
        y = row * (height + spacing)
        merged_img.paste(final_img, (x, y))

    merged_path = os.path.join(merged_output_dir, f"{name}_merged.png")
    merged_img.save(merged_path)
    print(f"🧩 {name} 合图完成 → {merged_path}")

# 主程序入口
if __name__ == "__main__":
    pdb_files = glob.glob(os.path.join(input_dir, "*.pdb"))
    print(f"📦 共检测到 {len(pdb_files)} 个 PDB 文件，开始并行渲染...")

    # 开启多进程（可根据显卡或CPU线程调节数量）
    with mp.Pool(processes=36) as pool:
        pool.map(render_pdb, pdb_files)

```


## 5. Generate jsonl fils for janus training
###########


entries.idx:
```txt
IDCODE, HEADER, ACCESSION DATE, COMPOUND, SOURCE, AUTHOR LIST, RESOLUTION, EXPERIMENT TYPE (IF NOT X-RAY)
------- ------- --------------- --------- ------- ------------ ----------- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
100D    DNA-RNA HYBRID  12/05/94        CRYSTAL STRUCTURE OF THE HIGHLY DISTORTED CHIMERIC DECAMER R(C)D(CGGCGCCG)R(G)-SPERMINE COMPLEX-SPERMINE BINDING TO PHOSPHATE ONLY AND MINOR GROOVE TERTIARY BASE-PAIRING               Ban, C., Ramakrishnan, B., Sundaralingam, M.    1.9     X-RAY DIFFRACTION
101D    DNA     12/14/94        REFINEMENT OF NETROPSIN BOUND TO DNA: BIAS AND FEEDBACK IN ELECTRON DENSITY MAP INTERPRETATION          Goodsell, D.S., Kopka, M.L., Dickerson, R.E.    2.25    X-RAY DIFFRACTION
101M    OXYGEN TRANSPORT        12/13/97        SPERM WHALE MYOGLOBIN F46V N-BUTYL ISOCYANIDE AT PH 9.0 Physeter catodonSmith, R.D., Olson, J.S., Phillips Jr., G.N.    2.07    X-RAY DIFFRACTION
102D    DNA     12/15/94        SEQUENCE-DEPENDENT DRUG BINDING TO THE MINOR GROOVE OF DNA: THE CRYSTAL STRUCTURE OF THE DNA DODECAMER D(CGCAAATTTGCG)2 COMPLEXED WITH PROPAMIDINE              Nunn, C.M., Neidle, S.  2.2     X-RAY DIFFRACTION
102L    HYDROLASE(O-GLYCOSYL)   09/29/92        HOW AMINO-ACID INSERTIONS ARE ALLOWED IN AN ALPHA-HELIX OF T4 LYSOZYME Enterobacteria phage T4  Heinz, D.W., Matthews, B.W.     1.74    X-RAY DIFFRACTION
102M    OXYGEN TRANSPORT        12/15/97        SPERM WHALE MYOGLOBIN H64A AQUOMET AT PH 9.0    Physeter catodon       Smith, R.D., Olson, J.S., Phillips Jr., G.N.     1.84    X-RAY DIFFRACTION
103D    DNA     12/16/94        THE UNUSUAL STRUCTURE OF THE HUMAN CENTROMERE (GGA)2 MOTIF: UNPAIRED GUANOSINE RESIDUES STACKED BETWEEN SHEARED G(DOT)A PAIRS           Chou, S.-H., Zhu, L., Reid, B.R.        NOT     SOLUTION NMR
103L    HYDROLASE(O-GLYCOSYL)   09/29/92        HOW AMINO-ACID INSERTIONS ARE ALLOWED IN AN ALPHA-HELIX OF T4 LYSOZYME Enterobacteria phage T4  Heinz, D.W., Matthews, B.W.     1.9     X-RAY DIFFRACTION
```

pdb_seqres.txt:
```txt
>100d_A mol:na length:10  DNA/RNA (5'-R(*CP*)-D(*CP*GP*GP*CP*GP*CP*CP*GP*)-R(*G)-3')
CCGGCGCCGG
>100d_B mol:na length:10  DNA/RNA (5'-R(*CP*)-D(*CP*GP*GP*CP*GP*CP*CP*GP*)-R(*G)-3')
CCGGCGCCGG
>101m_A mol:protein length:154  MYOGLOBIN
MVLSEGEWQLVLHVWAKVEADVAGHGQDILIRLFKSHPETLEKFDRVKHLKTEAEMKASEDLKKHGVTVLTALGAILKKKGHHEAELKPLAQSHATKHKIPIKYLEFISEAIIHVLHSRHPGNFGADAQGAMNKALELFRKDIAAKYKELGYQG
```

##########
读取entries.idx,读取IDCODE,为蛋白的id.
```js
{
"image": "/home/dell/model/data/b3.mergeimages/{id}_merged.png", 
"instruction": "这个是蛋白的结构从前,后,左,右,上,下,6个角度观察结构的图像,请根据该蛋白结构6个角度的图片,预测该蛋白的整体功能。
目标蛋白的第{pdb_seqres.txt_id}条肽段，序列为{pdb_seqres.txt_id_A},序列长度为 {length}，类型为{pdb_seqres.txt_id_protein/na}。(可能包括多条链需要分别显示)", 
"output":"该蛋白结构功能是{entries.id_HEADER},该蛋白结构编号为 {id}. compound 是{entries.id_COMPOUND},来源是{entries.id_SOURCE}"
"label":"{entries.id_HEADER}"
}
```

```sh
conda activate pymol_env
pip install biopython

```
```py
import os
import re
import json
from Bio import SeqIO

# 文件路径
entries_path = "entries.idx"
seqres_path = "pdb_seqres.txt"
output_jsonl = "deepseek_janus_training_data.jsonl"

# 读取 entries.idx 数据
entries_info = {}
with open(entries_path, "r", encoding="utf-8") as f:
    lines = f.readlines()[2:]  # 从第3行开始
    for line in lines:
        if re.match(r"^\s*\w{4}\s", line):
            fields = line.strip().split("\t")
            if len(fields) < 5:
                continue  # 跳过字段不足的行
            pdb_id = fields[0].strip().upper()
            header = fields[1].strip()
            accession_date = fields[2].strip()
            compound = fields[3].strip()
            source = fields[4].strip() if fields[4].strip() else "Unknown"
            entries_info[pdb_id.upper()] = {
                "header": header,
                "compound": compound,
                "source": source
            }
            #print(pdb_id.upper())
            #print(entries_info[pdb_id.upper()])

# 读取序列信息
seqres_info = {}
for record in SeqIO.parse(seqres_path, "fasta"):
    desc = record.description
    #print(desc)
    match = re.match(r"(\w+)_(\w+) mol:(\w+) length:(\d+)", desc)
    #print(match)
    if match:
        pdb_id, chain, mol_type, length = match.groups()
        pdb_id = pdb_id.upper()
        if pdb_id not in seqres_info:
            seqres_info[pdb_id] = []
        seqres_info[pdb_id].append({
            "chain": chain,
            "mol_type": mol_type,
            "length": int(length),
            "sequence": str(record.seq)
        })
        #print(pdb_id)
        #print(seqres_info[pdb_id])

# 构建训练数据
with open(output_jsonl, "w", encoding="utf-8") as fout:
    for pdb_id in entries_info:
        if pdb_id not in seqres_info:
            continue
        image_path = f"/home/dell/model/data/b3.pdb_all_merge_images/{pdb_id}_merged.png"
        if not os.path.exists(image_path):
            print(f"❌ 文件不存在：{image_path}")
            continue
        peptide_info = seqres_info[pdb_id]
        count = len(peptide_info)
        #print(peptide_info)
        instruction = (
            f"这个是蛋白的结构从前,后,左,右,上,下,6个角度观察结构的图像,请根据该蛋白结构6个角度的图片,预测该蛋白的整体功能。\n"
            f"目标共有{count}条链，"
        )
        for i, pep in enumerate(peptide_info):
            instruction += (
                f"链 {pep['chain']} 的序列为 {pep['sequence']}，"
                f"序列长度为 {pep['length']}，类型为 {pep['mol_type']}。"
            )
            if i != len(peptide_info) - 1:
                instruction += "\n"

        output_text = (
            f"该蛋白结构功能是 {entries_info[pdb_id]['header']}，"
            f"该蛋白结构编号为 {pdb_id}。compound 是 {entries_info[pdb_id]['compound']}，"
            f"来源是 {entries_info[pdb_id]['source']}。"
        )

        json.dump({
            "image": image_path,
            "instruction": instruction,
            "output": output_text,
            "label": entries_info[pdb_id]['header']
        }, fout, ensure_ascii=False)
        fout.write("\n")

```


## 6. model train
```sh
CUDA_VISIBLE_DEVICES=1,2,3 \
swift sft \
    --model /home/dell/model/deepseek-janus-pro-7b \
    --model_type deepseek_janus_pro \
    --dataset /home/dell/model/data/b5.pdb_all.jsonl/deepseek_janus_training_data.jsonl \
    --train_type lora \
    --torch_dtype bfloat16 \
    --num_train_epochs 5 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --learning_rate 1e-5 \
    --lora_rank 8 \
    --lora_alpha 32 \
    --target_modules all-linear \
    --freeze_vit false \
    --gradient_accumulation_steps 16 \
    --eval_steps 100 \
    --save_steps 100 \
    --save_total_limit 20 \
    --logging_steps 5 \
    --max_length 4048 \
    --output_dir /home/dell/model/train_deepseek_janus_7b_pro \
    --warmup_ratio 0.05 \
    --dataloader_num_workers 4 \
    --dataset_num_proc 4
```

output in /home/dell/model/train_deepseek_janus_7b_pro/v9-20250416-120003

### Load the trained model.

```sh
CUDA_VISIBLE_DEVICES=2 \
swift infer \
    --adapters /home/dell/model/train_deepseek_janus_7b_pro/v16-20250416-160133/checkpoint-270 \
    --stream false \
    --max_batch_size 1 \
    --load_data_args true \
    --max_new_tokens 2048 \
   --val_dataset test.jsonl \
   --result_path test.result.jsonl
```
### 

```sh
CUDA_VISIBLE_DEVICES=2 \
swift infer \
    --model /home/dell/model/deepseek-janus-pro-7b \
    --model_type deepseek_janus_pro \
    --stream false \
    --max_batch_size 1 \
    --load_data_args true \
    --max_new_tokens 2048 \
   --val_dataset dataset.jsonl \
   --result_path result_origin.jsonl

```












