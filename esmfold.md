## Download ESMFold docker images to predict protein structure.

```sh
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
# 添加 NVIDIA 源（自动识别系统版本）
distribution=$(. /etc/os-release; echo $ID$VERSION_ID)   && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list   | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g'   | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
docker info | grep -A3 Runtimes
docker run --rm --gpus device=0 --entrypoint nvidia-smi biochunan/esmfold-image
```

```sh
docker run --rm biochunan/esmfold-image --help
#run test samples.
docker run --rm --gpus device=0 \
-v /home/dell/esm:/root/input \
-v /home/dell/esm/esm_structure:/root/output \
biochunan/esmfold-image \
-i /root/input/input.fasta \
-o /root/output \
> ./pred-root-devel.log 2>./pred-root-devel.err

```
## run in guida local
设置4个变量。
1. 蛋白的fasta
2. 输出蛋白结构的名字，用于新建并保存结果
3. 蛋白的路径
4. 输出蛋白结构的路径
```sh
# run bacterial AMPs to predict structure.

inputfasta='2024_amphibian_AMPs_with_known_activity.fasta'
outputname='structure_amphibian'

inputfasta='2024_bacterial_AMPs_with_known_activity.fasta'  
outputname='structure_bacterial'

inputfasta='2024_plant_AMPs_with_known_activity.fasta'
outputname='structure_plant'

inputfasta='2024_animal_AMPs_with_known_activity.fasta'
outputname='structure_animal'

inputfasta='2024_human_AMPs_with_known_activity.fasta'  
outputname='structure_human'

inputfasta='2024_insect_AMPs_with_known_activity.fasta' 
outputname='structure_insect'

inputfasta='2024_natural_AMPs_with_known_activity.fasta'
outputname='structure_natural'

inputpath='/home/dell/model/data/rawdata/AMPs/APD3/'
outputpath='/home/dell/model/data/rawdata/AMPs/APD3/'


[[ -d ${outputpath}/${outputname} ]] || mkdir -p ${outputpath}/${outputname}

echo  "docker run --rm --gpus device=0 -v ${inputpath}:/root/input -v ${outputpath}/${outputname}:/root/output biochunan/esmfold-image -i /root/input/${inputfasta} -o /root/output > ${outputpath}/${outputname}/pred-root-devel.log 2>${outputpath}/${outputname}/pred-root-devel.err "

docker run --rm --gpus device=0 \
-v ${inputpath}:/root/input \
-v ${outputpath}/${outputname}:/root/output \
biochunan/esmfold-image \
-i /root/input/${inputfasta} \
-o /root/output \
> ${outputpath}/${outputname}/pred-root-devel.log 2>${outputpath}/${outputname}/pred-root-devel.err

```

···sh
#!/bin/bash

# 输入文件名数组（与 outputname 一一对应）
input_files=(
    "2024_amphibian_AMPs_with_known_activity.fasta"
    "2024_bacterial_AMPs_with_known_activity.fasta"
    "2024_plant_AMPs_with_known_activity.fasta"
    "2024_animal_AMPs_with_known_activity.fasta"
    "2024_human_AMPs_with_known_activity.fasta"
    "2024_insect_AMPs_with_known_activity.fasta"
    "2024_natural_AMPs_with_known_activity.fasta"
)

output_names=(
    "structure_amphibian"
    "structure_bacterial"
    "structure_plant"
    "structure_animal"
    "structure_human"
    "structure_insect"
    "structure_natural"
)

# 输入输出路径（通用）
inputpath='/home/dell/model/data/rawdata/AMPs/APD3'
outputpath='/home/dell/model/data/rawdata/AMPs/APD3'

# 遍历输入序列
for i in "${!input_files[@]}"; do
    inputfasta="${input_files[$i]}"
    outputname="${output_names[$i]}"

    # 创建输出目录
    outdir="${outputpath}/${outputname}"
    [[ -d "$outdir" ]] || mkdir -p "$outdir"

    echo "🚀 预测中: $inputfasta → 输出目录: $outputname"

    # 执行 docker 预测命令
    docker run --rm --gpus device=0 \
        -v "${inputpath}:/root/input" \
        -v "${outdir}:/root/output" \
        biochunan/esmfold-image \
        -i "/root/input/${inputfasta}" \
        -o "/root/output" \
        > "${outdir}/pred-root-devel.log" \
        2> "${outdir}/pred-root-devel.err"

    echo "✅ 预测完成: $inputfasta → $outdir"
done

echo "🎉 所有序列批量预测完成！"

```

item| 说明
-- | --
pLDDT（Predicted LDDT）| 预测局部距离差异得分，范围 0–100，≥70 表示可信，≥90 非常可靠；
pTM（predicted TM-score） |  预测拓扑得分，类似 RMSD 全局比对质量指标，越接近 1 越好；
batch size| 模型每次并行处理的序列数，这里是一次预测 2 条序列。

标准选择pLDDT 大于70.

25/05/06 08:27:13 | INFO | root | Predicted structure for AP01651 with length 60, pLDDT 76.4, pTM 0.669 in 0.4s (amortized, batch size 16). 370 / 410 completed.  
25/05/06 08:27:13 | INFO | root | Predicted structure for AP01652 with length 61, pLDDT 88.1, pTM 0.814 in 0.4s (amortized, batch size 16). 371 / 410 completed.  
25/05/06 08:27:13 | INFO | root | Predicted structure for AP01767 with length 61, pLDDT 82.5, pTM 0.762 in 0.4s (amortized, batch size 16). 372 / 410 completed.  
25/05/06 08:27:13 | INFO | root | Predicted structure for AP03289 with length 61, pLDDT 82.0, pTM 0.763 in 0.4s (amortized, batch size 16). 373 / 410 completed.  
25/05/06 08:27:13 | INFO | root | Predicted structure for AP00807 with length 62, pLDDT 34.0, pTM 0.122 in 0.4s (amortized, batch size 16). 374 / 410 completed.  
25/05/06 08:27:13 | INFO | root | Predicted structure for AP01171 with length 62, pLDDT 40.4, pTM 0.166 in 0.4s (amortized, batch size 16). 375 / 410 completed.  
25/05/06 08:27:13 | INFO | root | Predicted structure for AP01232 with length 62, pLDDT 48.1, pTM 0.155 in 0.4s (amortized, batch size 16). 376 / 410 completed.  
25/05/06 08:27:13 | INFO | root | Predicted structure for AP01600 with length 64, pLDDT 57.5, pTM 0.423 in 0.4s (amortized, batch size 16). 377 / 410 completed.  
25/05/06 08:27:13 | INFO | root | Predicted structure for AP02396 with length 64, pLDDT 83.4, pTM 0.770 in 0.4s (amortized, batch size 16). 378 / 410 completed.  
25/05/06 08:27:13 | INFO | root | Predicted structure for AP02584 with length 64, pLDDT 91.8, pTM 0.841 in 0.4s (amortized, batch size 16). 379 / 410 completed.  



