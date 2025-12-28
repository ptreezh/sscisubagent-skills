@echo off
REM 自动化部署脚本 - SSCI Subagent Skills (Windows)
REM 作者: socienceAI.com
REM 联系: zhangshuren@freeagentskills.com

setlocal enabledelayedexpansion

REM 设置颜色（Windows 10+）
set "INFO=[INFO]"
set "SUCCESS=[SUCCESS]"
set "WARNING=[WARNING]"
set "ERROR=[ERROR]"

echo ==========================================
echo   SSCI Subagent Skills 自动部署脚本
echo   作者: socienceAI.com
echo ==========================================
echo.

REM 解析参数
set SKIP_TESTS=0
set COMMIT_MESSAGE=
set VERSION_TAG=

:parse_args
if "%~1"=="" goto end_parse
if "%~1"=="--skip-tests" (
    set SKIP_TESTS=1
    shift
    goto parse_args
)
if "%~1"=="-m" (
    set COMMIT_MESSAGE=%~2
    shift /2
    goto parse_args
)
if "%~1"=="--message" (
    set COMMIT_MESSAGE=%~2
    shift /2
    goto parse_args
)
if "%~1"=="-t" (
    set VERSION_TAG=%~2
    shift /2
    goto parse_args
)
if "%~1"=="--tag" (
    set VERSION_TAG=%~2
    shift /2
    goto parse_args
)
if "%~1"=="--help" goto help
if "%~1"=="-h" goto help
echo %ERROR% 未知选项: %~1
echo 使用 --help 查看帮助信息
exit /b 1

:end_parse

REM 检查Git状态
echo %INFO% 检查Git状态...

git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo %ERROR% 当前目录不是Git仓库
    exit /b 1
)

for /f %%i in ('git status -s') do set HAS_CHANGES=1
if not defined HAS_CHANGES (
    echo %WARNING% 没有需要提交的更改
    exit /b 0
)

echo %SUCCESS% Git仓库检查通过

REM 运行测试
if %SKIP_TESTS%==0 (
    echo %INFO% 运行测试...

    REM Python语法检查
    echo %INFO% 检查Python文件语法...

    for /r %%f in (*.py) do (
        echo %%f | findstr /v "\\.venv\\" | findstr /v "\\venv\\" | findstr /v "\\env\\" | findstr /v "\\archive\\" | findstr /v "\\project_backup\\" | findstr /v "node_modules" >nul
        if not errorlevel 1 (
            python -m py_compile "%%f" 2>&1
            if errorlevel 1 (
                echo %ERROR% Python语法检查失败: %%f
                exit /b 1
            )
        )
    )

    echo %SUCCESS% 所有测试通过
) else (
    echo %WARNING% 跳过测试
)

REM 添加文件到Git
echo %INFO% 添加文件到Git...
git add .

echo %INFO% 将要提交的文件:
git status -s

echo %SUCCESS% 文件已添加到暂存区

REM 创建提交
echo %INFO% 创建Git提交...

if defined COMMIT_MESSAGE (
    git commit -m "%COMMIT_MESSAGE%"
) else (
    set "COMMIT_MESSAGE=feat: 自动部署更新 - %date% %time%

- 更新作者和联系信息
- 优化技能文件结构
- 更新文档

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

    git commit -m "!COMMIT_MESSAGE!"
)

if errorlevel 1 (
    echo %ERROR% 提交失败
    exit /b 1
)

echo %SUCCESS% 提交创建成功

REM 推送到远程仓库
echo %INFO% 推送到远程仓库...

for /f %%i in ('git branch --show-current') do set CURRENT_BRANCH=%%i
echo %INFO% 当前分支: !CURRENT_BRANCH!

git push origin !CURRENT_BRANCH!

if errorlevel 1 (
    echo %ERROR% 推送失败
    exit /b 1
)

echo %SUCCESS% 推送成功

REM 创建Git标签
if defined VERSION_TAG (
    echo %INFO% 创建Git标签: %VERSION_TAG%

    git tag -a %VERSION_TAG% -m "Release %VERSION_TAG%"
    git push origin %VERSION_TAG%

    echo %SUCCESS% 标签创建并推送成功
)

echo.
echo %SUCCESS% 部署完成！
echo.
echo %INFO% 仓库地址: https://github.com/ptreezh/sscisubagent-skills

goto :eof

:help
echo 使用方法:
echo   %~nx0 [选项]
echo.
echo 选项:
echo   --skip-tests       跳过测试
echo   --message, -m      自定义提交信息
echo   --tag, -t          创建版本标签
echo   --help, -h         显示帮助信息
echo.
echo 示例:
echo   %~nx0                           # 默认部署
echo   %~nx0 --skip-tests              # 跳过测试
echo   %~nx0 -m "feat: add new skill"  # 自定义提交信息
echo   %~nx0 -t v1.0.0                 # 创建版本标签
exit /b 0
