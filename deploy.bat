@echo off
REM 一键部署脚本
REM 自动部署社会科学方法论 skill 进化系统到 Qwen CLI

echo ============================================================
echo 社会科学方法论 Skill 进化系统 - 一键部署
echo ============================================================
echo.

REM 设置路径
set QWEN_HOME=%USERPROFILE%\.qwen
set SKILLS_SOURCE=D:\socienceAI\agentskills

echo [部署中] 请稍候...
echo.

REM 步骤 1: 创建目录
echo [1/5] 创建目录结构...
if not exist "%QWEN_HOME%\extensions" mkdir "%QWEN_HOME%\extensions"
if not exist "%QWEN_HOME%\skills" mkdir "%QWEN_HOME%\skills"
echo   [OK] 目录创建完成

REM 步骤 2: 安装扩展
echo.
echo [2/5] 安装进化引擎扩展...
xcopy /E /I /Y "%SKILLS_SOURCE%\extensions\skill-evolution" "%QWEN_HOME%\extensions\skill-evolution" >nul
if errorlevel 1 (
    echo   [ERROR] 扩展安装失败
) else (
    echo   [OK] 扩展安装成功
)

REM 步骤 3: 配置 Qwen CLI
echo.
echo [3/5] 配置 Qwen CLI...
findstr /C:"skill-evolution" "%QWEN_HOME%\config.yaml" >nul
if errorlevel 1 (
    echo.
    echo extensions: >> "%QWEN_HOME%\config.yaml"
    echo   enabled: >> "%QWEN_HOME%\config.yaml"
    echo     - skill-evolution >> "%QWEN_HOME%\config.yaml"
    echo   [OK] 已添加扩展配置到 config.yaml
) else (
    echo   [OK] 扩展配置已存在
)

REM 步骤 4: 复制 skill
echo.
echo [4/5] 复制 skill 到 Qwen CLI...

xcopy /E /I /Y "%SKILLS_SOURCE%\grounded-theory-expert" "%QWEN_HOME%\skills\grounded-theory-expert" >nul
if errorlevel 1 (
    echo   [ERROR] grounded-theory-expert 复制失败
) else (
    echo   [OK] grounded-theory-expert 复制成功
)

xcopy /E /I /Y "%SKILLS_SOURCE%\social-network-analysis-expert" "%QWEN_HOME%\skills\social-network-analysis-expert" >nul
if errorlevel 1 (
    echo   [ERROR] social-network-analysis-expert 复制失败
) else (
    echo   [OK] social-network-analysis-expert 复制成功
)

REM 步骤 5: 验证
echo.
echo [5/5] 验证部署...

set VERIFIED=1

if not exist "%QWEN_HOME%\extensions\skill-evolution\index.js" (
    echo   [ERROR] 扩展文件缺失
    set VERIFIED=0
)

if not exist "%QWEN_HOME%\skills\grounded-theory-expert\soul.md" (
    echo   [ERROR] grounded-theory-expert\soul.md 缺失
    set VERIFIED=0
)

if not exist "%QWEN_HOME%\skills\social-network-analysis-expert\soul.md" (
    echo   [ERROR] social-network-analysis-expert\soul.md 缺失
    set VERIFIED=0
)

if %VERIFIED%==1 (
    echo   [OK] 所有文件验证通过
)

echo.
echo ============================================================
echo 部署完成！
echo ============================================================
echo.

if %VERIFIED%==1 (
    echo [SUCCESS] 部署成功！
    echo.
    echo 下一步：
    echo   1. 启动 Qwen CLI: qwen
    echo   2. 应该看到 [SkillEvolution] 日志
    echo   3. 测试：使用扎根理论分析以下访谈数据...
    echo.
    echo 查看文件位置：
    echo   - soul.md: %QWEN_HOME%\skills\grounded-theory-expert\soul.md
    echo   - lesson-memory.md: %QWEN_HOME%\skills\grounded-theory-expert\lesson-memory.md
    echo   - case-library: %QWEN_HOME%\skills\grounded-theory-expert\case-library\
) else (
    echo [ERROR] 部署失败！请检查错误信息
)

echo.
pause
