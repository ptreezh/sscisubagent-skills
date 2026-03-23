@echo off
REM 部署验证脚本
REM 验证社会科学方法论 skill 进化系统的部署

echo ============================================================
echo 社会科学方法论 Skill 进化系统 - 部署验证
echo ============================================================
echo.

REM 设置路径
set QWEN_HOME=%USERPROFILE%\.qwen
set SKILLS_SOURCE=D:\socienceAI\agentskills

echo [1/6] 检查 Qwen CLI 主目录...
if exist "%QWEN_HOME%" (
    echo   [OK] Qwen CLI 主目录存在：%QWEN_HOME%
) else (
    echo   [ERROR] Qwen CLI 主目录不存在！
    echo   请先安装 Qwen CLI
    goto :end
)

echo.
echo [2/6] 检查扩展目录...
if exist "%QWEN_HOME%\extensions\skill-evolution\index.js" (
    echo   [OK] 进化引擎扩展已安装
) else (
    echo   [WARNING] 进化引擎扩展未安装
    echo   请运行：xcopy /E /I "%SKILLS_SOURCE%\extensions\skill-evolution" "%QWEN_HOME%\extensions\skill-evolution"
)

echo.
echo [3/6] 检查 skills 目录...
if exist "%QWEN_HOME%\skills" (
    echo   [OK] skills 目录存在
) else (
    echo   [ERROR] skills 目录不存在！
    goto :end
)

echo.
echo [4/6] 检查已安装的 skill...
set SKILL_COUNT=0

if exist "%QWEN_HOME%\skills\grounded-theory-expert\soul.md" (
    echo   [OK] grounded-theory-expert 已安装
    set /a SKILL_COUNT+=1
) else (
    echo   [WARNING] grounded-theory-expert 未安装
)

if exist "%QWEN_HOME%\skills\social-network-analysis-expert\soul.md" (
    echo   [OK] social-network-analysis-expert 已安装
    set /a SKILL_COUNT+=1
) else (
    echo   [WARNING] social-network-analysis-expert 未安装
)

echo   已安装 skill 数量：%SKILL_COUNT%

echo.
echo [5/6] 检查 skill 核心文件...

for %%S in (grounded-theory-expert social-network-analysis-expert) do (
    if exist "%QWEN_HOME%\skills\%%S" (
        if exist "%QWEN_HOME%\skills\%%S\soul.md" (
            echo   [OK] %%S\soul.md 存在
        ) else (
            echo   [WARNING] %%S\soul.md 不存在
        )
        
        if exist "%QWEN_HOME%\skills\%%S\lesson-memory.md" (
            echo   [OK] %%S\lesson-memory.md 存在
        ) else (
            echo   [WARNING] %%S\lesson-memory.md 不存在
        )
        
        if exist "%QWEN_HOME%\skills\%%S\case-library" (
            echo   [OK] %%S\case-library\ 目录存在
        ) else (
            echo   [WARNING] %%S\case-library\ 目录不存在
        )
        
        if exist "%QWEN_HOME%\skills\%%S\skill-hooks.yaml" (
            echo   [OK] %%S\skill-hooks.yaml 存在
        ) else (
            echo   [WARNING] %%S\skill-hooks.yaml 不存在
        )
    )
)

echo.
echo [6/6] 检查 Qwen CLI config.yaml...
if exist "%QWEN_HOME%\config.yaml" (
    findstr /C:"skill-evolution" "%QWEN_HOME%\config.yaml" >nul
    if errorlevel 1 (
        echo   [WARNING] config.yaml 未配置 skill-evolution 扩展
        echo   请编辑 config.yaml 添加：
        echo   extensions:
        echo     enabled:
        echo       - skill-evolution
    ) else (
        echo   [OK] config.yaml 已配置 skill-evolution 扩展
    )
) else (
    echo   [WARNING] config.yaml 不存在
)

echo.
echo ============================================================
echo 验证完成！
echo ============================================================
echo.
echo 已安装 skill 数量：%SKILL_COUNT%
echo.

if %SKILL_COUNT% GEQ 1 (
    echo [SUCCESS] 部署成功！可以启动 Qwen CLI 测试
    echo.
    echo 下一步：
    echo   1. 启动 Qwen CLI: qwen
    echo   2. 测试 skill: 使用扎根理论分析以下访谈数据...
    echo   3. 查看教训：type "%QWEN_HOME%\skills\grounded-theory-expert\lesson-memory.md"
) else (
    echo [ERROR] 部署失败！请先安装 skill
    echo.
    echo 请运行：
    echo   xcopy /E /I "%SKILLS_SOURCE%\grounded-theory-expert" "%QWEN_HOME%\skills\grounded-theory-expert"
    echo   xcopy /E /I "%SKILLS_SOURCE%\social-network-analysis-expert" "%QWEN_HOME%\skills\social-network-analysis-expert"
)

:end
echo.
pause
