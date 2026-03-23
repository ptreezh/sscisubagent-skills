@echo off
REM 初始化 Git 仓库并推送到 GitHub 和 Gitee
REM 执行日期：2026-03-23

echo ========================================
echo 初始化 Git 仓库
echo ========================================
echo.

cd /d D:\socienceAI\agentskills

REM 初始化 Git
echo 初始化 Git...
git init

REM 添加所有文件
echo 添加文件...
git add .

REM 提交
echo 提交文件...
git commit -m "Initial commit: 60 个社会科学方法论技能包"

REM 添加 GitHub 远程仓库
echo.
echo 添加 GitHub 远程仓库...
git remote add origin https://github.com/socienceai/agentskills.git

REM 添加 Gitee 远程仓库
echo 添加 Gitee 远程仓库...
git remote add gitee https://gitee.com/socienceai/agentskills.git

REM 推送到 GitHub
echo.
echo 推送到 GitHub...
echo 请手动执行：git push -u origin main

REM 推送到 Gitee
echo.
echo 推送到 Gitee...
echo 请手动执行：git push -u gitee main

echo.
echo ========================================
echo Git 仓库初始化完成！
echo ========================================
echo.
echo 下一步:
echo 1. 创建 GitHub 仓库：https://github.com/new
echo 2. 创建 Gitee 仓库：https://gitee.com/new
echo 3. 执行推送命令
echo.
pause
