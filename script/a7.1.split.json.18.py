import sys
import os
import json
from math import ceil

def clean_newlines(obj):
    """递归去除字符串中的换行符"""
    if isinstance(obj, dict):
        return {k: clean_newlines(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_newlines(item) for item in obj]
    elif isinstance(obj, str):
        return obj.replace('\n', ' ').strip()
    else:
        return obj

def split_jsonl(input_path, output_dir, num_parts=18):
    os.makedirs(output_dir, exist_ok=True)

    with open(input_path, 'r', encoding='utf-8') as f:
        lines = [json.loads(line) for line in f if line.strip()]

    # 清洗每条记录
    lines = [clean_newlines(line) for line in lines]

    total = len(lines)
    part_size = ceil(total / num_parts)

    for i in range(num_parts):
        start = i * part_size
        end = min(start + part_size, total)
        part_data = lines[start:end]

        output_path = os.path.join(output_dir, f"split_{i+1}.json")
        with open(output_path, 'w', encoding='utf-8') as out_f:
            for record in part_data:
                out_f.write(json.dumps(record, ensure_ascii=False) + '\n')

        print(f"写入文件：{output_path}（共 {len(part_data)} 条）")

def main():
    if len(sys.argv) != 3:
        print("用法: python split_jsonl.py input.jsonl output_dir/")
        sys.exit(1)

    input_jsonl = sys.argv[1]
    output_directory = sys.argv[2]

    if not os.path.exists(input_jsonl):
        print(f"输入文件不存在: {input_jsonl}")
        sys.exit(1)

    split_jsonl(input_jsonl, output_directory)

if __name__ == "__main__":
    main()
