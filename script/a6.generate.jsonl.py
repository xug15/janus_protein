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



