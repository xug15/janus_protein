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


# run bacterial AMPs to predict structure.
inputfasta='2024_bacterial_AMPs_with_known_activity.fasta'
outputname='structure_bacterial'
inputpath='/home/dell/model/data/rawdata/AMPs/APD3/'
outputpath='/home/dell/model/data/rawdata/AMPs/APD3/'
[[ -d ${outputpath}/${outputname} ]] || mkdir -p ${outputpath}/${outputname}

echo  "docker run --rm --gpus device=0 -v ${inputpath}:/root/input -v ${outputpath}/${outputname}:/root/output biochunan/esmfold-image -i /root/input/${inputfasta} -o /root/output > /root/output/pred-root-devel.log 2>/root/output/pred-root-devel.err "

docker run --rm --gpus device=0 \
-v ${inputpath}:/root/input \
-v ${outputpath}/${outputname}:/root/output \
biochunan/esmfold-image \
-i /root/input/${inputfasta} \
-o /root/output \
> /root/output/pred-root-devel.log 2>/root/output/pred-root-devel.err



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



