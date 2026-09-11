@echo off
REM 批量测试所有 13 个 skill

cd /d "%~dp0"

echo ======================================================================
echo Skill 批量自动化测试
echo ======================================================================
echo.

set SKILLS=grounded-theory-expert social-network-analysis-expert bourdieu-field-analysis-expert msqca-analysis-expert did-analysis-expert data-analysis-expert business-ecosystem-analysis-expert business-model-analysis-expert actor-network-analysis-expert digital-marx-expert digital-durkheim-expert digital-weber-expert survey-design-expert

echo 开始测试所有 13 个 skill...
echo.

for %%S in (%SKILLS%) do (
    echo ======================================================================
    echo 测试：%%S
    echo ======================================================================
    echo.
    
    python auto-test-runner.py %%S
    
    echo.
    echo 完成：%%S
    echo.
)

echo ======================================================================
echo 所有 skill 测试完成！
echo ======================================================================
echo.
echo 测试报告位置：test-records\
echo.

pause
