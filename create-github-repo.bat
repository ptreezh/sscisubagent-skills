@echo off
REM 一键创建 GitHub 仓库并推送
REM 执行日期：2026-03-23

echo ========================================
echo 创建 GitHub 仓库并推送
echo ========================================
echo.

cd /d D:\socienceAI\agentskills

REM 检查 Git 是否已初始化
if not exist ".git" (
    echo 初始化 Git...
    git init
)

REM 添加所有文件
echo.
echo 添加文件...
git add .

REM 提交
echo.
echo 提交文件...
git commit -m "Initial commit: 60 种社会科学方法论技能包"

REM 重命名分支为 main
echo.
echo 重命名分支为 main...
git branch -M main

REM 添加远程仓库
echo.
echo 添加远程仓库...
git remote remove origin 2>nul
git remote add origin https://github.com/ptreezh/superpower-socialscience-skills.git

echo.
echo ========================================
echo Git 配置完成！
echo ========================================
echo.
echo 下一步（手动执行）:
echo.
echo 1. 打开浏览器访问：https://github.com/new
echo 2. 填写仓库信息:
echo    - Repository name: superpower-socialscience-skills
echo    - Description: 60 种社会科学方法论技能包
echo    - Visibility: Public
echo    - 不勾选 Initialize this repository
echo 3. 点击 Create repository
echo 4. 返回本窗口，执行推送:
echo.
echo    git push -u origin main
echo.
echo ========================================
pause
