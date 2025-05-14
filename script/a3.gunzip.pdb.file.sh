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










