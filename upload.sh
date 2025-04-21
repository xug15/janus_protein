#!/bin/bash

# 设置提交信息（当前时间）
label=$(date '+%Y-%m-%d_%H:%M')
echo "提交信息: ${label}"

# 添加并提交
git add *



if git diff --cached --quiet; then
    echo "⚠️ 暂无更改需要提交"
else
    git commit -m "${label}"
# 设置 main 分支
git branch -M main

# 如果 remote 已存在则先删除
git remote remove origin 2>/dev/null
git remote add origin git@github.com:xug15/janus_protein.git

# 推送到远程
git push -u origin main
fi







