# Using Deepseek-Janus-Pro-7b to learn protein structure to predict novel antimicrobial peptide and cellulolytic enzyme.

##  1. Structure of protein was necessary information for the project.
** There are 2 ways for getting the structure of protein.
The first one is obtaining from PDB database.
The second way is predicting from deep learning models.

### 1.1 processing the pdb files.

* 1.1.1 Using PyMOL software convert PDB files into 6 images from front, back, left, right, top, bottom side views.
* please refer the script a1.2.pdb_to_png.6.direct.one.py

* 1.1.2 The basic information of protein is also vital important for fine-tuning the deepseek-janus-pro-7b model.
New the three basic information tables were used to help generate  training json.   
For example:  

rcsb_pdb_structure_20250413193700.csv  
```txt
Identifier,StructureData,,,,,,,,,,
Entry ID,Structure Title,Structure Determination Methodology,Refinement Resolution (Å),Molecular Weight per Deposited Model,Total Number of Polymer Residues per Deposited Model,Number of Non-Hydrogen Atoms per Deposited Model,Experimental Method,Release Date,Stucture Keywords,Structure Author,
"1C01","SOLUTION STRUCTURE OF MIAMP1, A PLANT ANTIMICROBIAL PROTEIN","experimental",,8.15,76,571,"SOLUTION NMR","2000-07-19","ANTIMICROBIAL PROTEIN","McManus, A.M., Nielsen, K.J., Marcus, J.P., Harrison, S.J., Green, J.L., Manners, J.M., Craik, D.J."
```
rcsb_pdb_biological_details_20250413193803.csv  
```txt
Identifier,Polymer EntityData,,,,,,,,,,,,
Entry ID,Entity ID,Asym ID,Auth Asym ID,Macromolecule Name,EC Number,Source Organism,Taxonomy ID,Expression Host,Biological Process,Cellular Component,Molecular Function,Plasmid Name,
"1C01","1","A","A","ANTIMICROBIAL PEPTIDE 1",,"Macadamia integrifolia",60698,,"GO:0045926, GO:0042742, GO:0050832, GO:0031640","GO:0005576"

```
rcsb_pdb_sequence_20250413193719.csv  
```txt
Identifier,Polymer EntityData,,,,,,,,,
Entry ID,Entity ID,Asym ID,Auth Asym ID,Database Name,Accession Code(s),Sequence,Polymer Entity Sequence Length,Entity Macromolecule Type,Molecular Weight (Entity),
"1C01","1","A","A","UniProt","P80915","SAFTVWSGPGCNNRAERYSKCGCSAIHQKGGYDFSYTGQTAALYNQAGCSGVAHTRFGSSARACNPFGWKSIFIQC",76,"polypeptide(L)",8.147
"1D9J","1","A","A","UniProt","P01507","KWKLFKKIGIGKFLHSAKKFX",21,"polypeptide(L)",2.411
,,,,"UniProt","P11006"
```
* 1.1.3 Generate the data into the jsonl formate.   
refering script: a2.4.createjson.pdbinfor.py  
train_entitygroup_level.jsonl:
```js
{"image": "/home/dell/model/data/b3.mergeimages/8t3h_merged.png", "instruction": "这个是蛋白的结构从前,后,左,右,上,下,6个角度观察结构的图像,请根据该蛋白结构6个角度的图片,预测该蛋白的整体功能。目标蛋白的第 1.0 条肽段，序列为IINVLTSIVTPIKNQLDKYQX,序列长度为 21 个氨基酸，分子量约为 2.301 kDa，分子类型为 polypeptide(L)。", "output": "该蛋白结构功能是ANTIMICROBIAL PROTEIN,该蛋白结构编号为 8T3H，名称为 Solution NMR structure alpha-helix 3 of Cry10Aa protein，使用 SOLUTION NMR 方法解析，关键词是ANTIMICROBIAL PROTEIN。其分子量约为 2.3 kDa，共含 21 个残基。以下是蛋白每个肽链的功能与序列信息:目标蛋白的第1.0 条肽段，蛋白名称为 Pesticidal crystal protein Cry10Aa peptide，来源于 Bacillus thuringiensis。该链的 EC 编号为 nan，GO 注释包括：生物过程：GO:0001907, GO:0030435；细胞组分：nan；序列同源性功能：GO:0005102, GO:0090729。"}
```
## 2 Fine turning the DeepSeek-Janus-Pro-7b model.
### 2.1 Fine turning

a3.1.train-deepseek-janus.amp.sh
```bash
CUDA_VISIBLE_DEVICES=1,2,3 \
swift sft \
    --model /home/dell/model/deepseek-janus-pro-7b \
    --model_type deepseek_janus_pro \
    --dataset /home/dell/model/data/b5.json/train_entitygroup_level.jsonl \
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
    --save_total_limit 2 \
    --logging_steps 5 \
    --max_length 4048 \
    --output_dir /home/dell/model/train_deepseek_janus_7b_pro \
    --warmup_ratio 0.05 \
    --dataloader_num_workers 4 \
    --dataset_num_proc 4

```
**--freeze_vit false**  

output
```sh
[INFO:swift] Saving model checkpoint to /home/dell/model/train_deepseek_janus_7b_pro/v16-20250416-160133/checkpoint-200
{'loss': 1.00927935, 'token_acc': 0.74503353, 'grad_norm': 1.37748516, 'learning_rate': 1.51e-06, 'memory(GiB)': 43.21, 'train_speed(iter/s)': 0.063233, 'epoch': 3.73, 'global_step/max_steps': '205/270', 'percentage': '75.93%', 'elapsed_time': '54m 1s', 'remaining_time': '17m 7s'}
{'loss': 1.0359683, 'token_acc': 0.75277993, 'grad_norm': 1.35974193, 'learning_rate': 1.3e-06, 'memory(GiB)': 43.25, 'train_speed(iter/s)': 0.063164, 'epoch': 3.83, 'global_step/max_steps': '210/270', 'percentage': '77.78%', 'elapsed_time': '55m 24s', 'remaining_time': '15m 49s'}
{'loss': 1.00502844, 'token_acc': 0.74949345, 'grad_norm': 1.58470118, 'learning_rate': 1.1e-06, 'memory(GiB)': 43.25, 'train_speed(iter/s)': 0.063161, 'epoch': 3.92, 'global_step/max_steps': '215/270', 'percentage': '79.63%', 'elapsed_time': '56m 43s', 'remaining_time': '14m 30s'}
{'loss': 0.99238052, 'token_acc': 0.75366466, 'grad_norm': 3.70276713, 'learning_rate': 9.1e-07, 'memory(GiB)': 43.25, 'train_speed(iter/s)': 0.063329, 'epoch': 4.0, 'global_step/max_steps': '220/270', 'percentage': '81.48%', 'elapsed_time': '57m 53s', 'remaining_time': '13m 9s'}
{'loss': 1.00049133, 'token_acc': 0.75182625, 'grad_norm': 1.5559634, 'learning_rate': 7.4e-07, 'memory(GiB)': 43.25, 'train_speed(iter/s)': 0.063252, 'epoch': 4.09, 'global_step/max_steps': '225/270', 'percentage': '83.33%', 'elapsed_time': '59m 16s', 'remaining_time': '11m 51s'}
{'loss': 1.00520859, 'token_acc': 0.74781248, 'grad_norm': 1.73655367, 'learning_rate': 5.9e-07, 'memory(GiB)': 43.25, 'train_speed(iter/s)': 0.063231, 'epoch': 4.18, 'global_step/max_steps': '230/270', 'percentage': '85.19%', 'elapsed_time': '1h 0m 37s', 'remaining_time': '10m 32s'}
{'loss': 0.99729557, 'token_acc': 0.75651402, 'grad_norm': 2.69448423, 'learning_rate': 4.5e-07, 'memory(GiB)': 43.25, 'train_speed(iter/s)': 0.063222, 'epoch': 4.28, 'global_step/max_steps': '235/270', 'percentage': '87.04%', 'elapsed_time': '1h 1m 56s', 'remaining_time': '9m 13s'}
{'loss': 0.98616228, 'token_acc': 0.76397545, 'grad_norm': 1.70558536, 'learning_rate': 3.4e-07, 'memory(GiB)': 43.25, 'train_speed(iter/s)': 0.063171, 'epoch': 4.37, 'global_step/max_steps': '240/270', 'percentage': '88.89%', 'elapsed_time': '1h 3m 18s', 'remaining_time': '7m 54s'}
{'loss': 0.98212757, 'token_acc': 0.75718187, 'grad_norm': 1.79198229, 'learning_rate': 2.3e-07, 'memory(GiB)': 43.25, 'train_speed(iter/s)': 0.063164, 'epoch': 4.46, 'global_step/max_steps': '245/270', 'percentage': '90.74%', 'elapsed_time': '1h 4m 38s', 'remaining_time': '6m 35s'}
{'loss': 0.99518023, 'token_acc': 0.75466653, 'grad_norm': 1.64945257, 'learning_rate': 1.5e-07, 'memory(GiB)': 43.25, 'train_speed(iter/s)': 0.063144, 'epoch': 4.55, 'global_step/max_steps': '250/270', 'percentage': '92.59%', 'elapsed_time': '1h 5m 58s', 'remaining_time': '5m 16s'}
{'loss': 0.98563643, 'token_acc': 0.75255864, 'grad_norm': 1.49578714, 'learning_rate': 8e-08, 'memory(GiB)': 43.25, 'train_speed(iter/s)': 0.063147, 'epoch': 4.64, 'global_step/max_steps': '255/270', 'percentage': '94.44%', 'elapsed_time': '1h 7m 17s', 'remaining_time': '3m 57s'}
{'loss': 0.97417698, 'token_acc': 0.76579193, 'grad_norm': 1.20739162, 'learning_rate': 4e-08, 'memory(GiB)': 43.25, 'train_speed(iter/s)': 0.063139, 'epoch': 4.73, 'global_step/max_steps': '260/270', 'percentage': '96.30%', 'elapsed_time': '1h 8m 37s', 'remaining_time': '2m 38s'}
{'loss': 0.9867487, 'token_acc': 0.75098923, 'grad_norm': 1.7396512, 'learning_rate': 1e-08, 'memory(GiB)': 43.25, 'train_speed(iter/s)': 0.063117, 'epoch': 4.83, 'global_step/max_steps': '265/270', 'percentage': '98.15%', 'elapsed_time': '1h 9m 58s', 'remaining_time': '1m 19s'}
{'loss': 0.98493128, 'token_acc': 0.76092613, 'grad_norm': 1.76163006, 'learning_rate': 0.0, 'memory(GiB)': 43.25, 'train_speed(iter/s)': 0.063139, 'epoch': 4.92, 'global_step/max_steps': '270/270', 'percentage': '100.00%', 'elapsed_time': '1h 11m 15s', 'remaining_time': '0s'}
Train: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 270/270 [1:11:15<00:00, 15.65s/it]
{'eval_loss': 1.02031076, 'eval_token_acc': 0.75162095, 'eval_runtime': 3.5645, 'eval_samples_per_second': 2.244, 'eval_steps_per_second': 2.244, 'epoch': 4.92, 'global_step/max_steps': '270/270', 'percentage': '100.00%', 'elapsed_time': '1h 11m 19s', 'remaining_time': '0s'}
Val: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 8/8 [00:02<00:00,  3.65it/s]
/home/dell/.conda/envs/deepseek-janus-train-swift/lib/python3.10/site-packages/peft/utils/save_and_load.py:230: UserWarning: Setting `save_embedding_layers` to `True` as embedding layers found in `target_modules`.
  warnings.warn("Setting `save_embedding_layers` to `True` as embedding layers found in `target_modules`.")
[INFO:swift] Saving model checkpoint to /home/dell/model/train_deepseek_janus_7b_pro/v16-20250416-160133/checkpoint-270
{'train_runtime': 4283.441, 'train_samples_per_second': 1.017, 'train_steps_per_second': 0.063, 'train_loss': 1.5100154, 'epoch': 4.92, 'global_step/max_steps': '270/270', 'percentage': '100.00%', 'elapsed_time': '1h 11m 23s', 'remaining_time': '0s'}
Train: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 270/270 [1:11:23<00:00, 15.86s/it]
[INFO:swift] last_model_checkpoint: /home/dell/model/train_deepseek_janus_7b_pro/v16-20250416-160133/checkpoint-270
[INFO:swift] best_model_checkpoint: /home/dell/model/train_deepseek_janus_7b_pro/v16-20250416-160133/checkpoint-270
[INFO:swift] images_dir: /home/dell/model/train_deepseek_janus_7b_pro/v16-20250416-160133/images
```

|项目|	结果|	解读|
|-- |--    |--     |
|训练轮次	|epoch ≈ 4.92（共设定 5 轮）	|完整完成，覆盖率高 👍|
|训练 Loss	|train_loss: 1.51 → final loss: ~0.98	|明显下降，收敛良好 👍|
|Token Accuracy	|token_acc: 0.76	|对于结构+生物功能任务，非常优秀 💯|
|Eval Accuracy	|eval_token_acc: 0.75+	|模型泛化能力好，未过拟合 👍|
|Gradient Norm	|< 2~3，稳定	|无震荡或爆炸 👍|
|显存使用	|43.25 GiB / 多卡（合理）	|资源利用良好，未溢出|

training from last version.
```sh
CUDA_VISIBLE_DEVICES=1,2,3 \
swift sft \
    --model /home/dell/model/deepseek-janus-pro-7b \
    --model_type deepseek_janus_pro \
    --dataset /home/dell/model/data/b5.json/train_entitygroup_level.jsonl \
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
    --save_total_limit 2 \
    --logging_steps 5 \
    --max_length 2048 \
    --output_dir /home/dell/model/train_deepseek_janus_7b_pro \
    --warmup_ratio 0.05 \
    --dataloader_num_workers 4 \
    --dataset_num_proc 4 \
    --resume_from_checkpoint /home/dell/model/train_deepseek_janus_7b_pro/v5-20250414-142451/checkpoint-162

```

## 2.2 Using model to infer the function of protein by images of structure.


```sh
CUDA_VISIBLE_DEVICES=2 \
swift infer \
    --adapters /home/dell/model/train_deepseek_janus_7b_pro/v16-20250416-160133/checkpoint-270 \
    --stream false \
    --max_batch_size 1 \
    --load_data_args true \
    --max_new_tokens 2048 \
   --val_dataset dataset.jsonl \
   --result_path result.jsonl
```
Using the native deepseek-janus-pro-7b model to infer the function of protein by strucrue of images.
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



