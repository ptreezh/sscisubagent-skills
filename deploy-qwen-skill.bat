@echo off
REM Qwen CLI 自动化系统部署脚本

echo ========================================
echo Qwen CLI 自动化系统部署
echo ========================================
echo.

REM 步骤 1: 创建 Qwen skill 目录
echo [1/4] 创建 Qwen skill 目录...
if not exist "%USERPROFILE%\.qwen\skills\autonomous-execution" (
    mkdir "%USERPROFILE%\.qwen\skills\autonomous-execution"
    echo ✅ 目录创建成功
) else (
    echo ✅ 目录已存在
)
echo.

REM 步骤 2: 复制 skill 文件
echo [2/4] 复制 skill 文件...
copy "%~dp0qwen-skill.yaml" "%USERPROFILE%\.qwen\skills\autonomous-execution\" >nul
copy "%~dp0qwen-auto-executor.py" "%USERPROFILE%\.qwen\skills\autonomous-execution\" >nul
echo ✅ 文件复制完成
echo.

REM 步骤 3: 创建 skill 索引
echo [3/4] 创建 skill 索引...
echo {
echo   "name": "autonomous-execution",
echo   "version": "1.0.0",
echo   "enabled": true,
echo   "triggers": ["启动自动化", "执行任务", "继续执行"]
echo } > "%USERPROFILE%\.qwen\skills\autonomous-execution\index.json"
echo ✅ skill 索引创建完成
echo.

REM 步骤 4: 验证安装
echo [4/4] 验证安装...
if exist "%USERPROFILE%\.qwen\skills\autonomous-execution\qwen-skill.yaml" (
    echo ✅ skill 配置存在
) else (
    echo ❌ skill 配置缺失
)

if exist "%USERPROFILE%\.qwen\skills\autonomous-execution\qwen-auto-executor.py" (
    echo ✅ 执行器存在
) else (
    echo ❌ 执行器缺失
)

echo.
echo ========================================
echo 部署完成！
echo ========================================
echo.
echo 使用方法:
echo   1. 打开 Qwen CLI
echo   2. 输入：启动自动化任务执行
echo   3. 或输入：qwen "启动自动化"
echo.
echo 可用命令:
echo   - 启动自动化
echo   - 执行任务
echo   - 继续执行
echo   - 查看状态
echo   - 停止
echo.

pause
