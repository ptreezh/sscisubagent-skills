@echo off
REM 部署 Skill 和扩展到 Qwen CLI
REM 用于真实环境测试

echo ============================================================
echo 部署 Skill 和扩展到 Qwen CLI
echo ============================================================
echo.

set QWEN_HOME=%USERPROFILE%\.qwen
set SKILLS_SOURCE=D:\socienceAI\agentskills

echo [1/4] 创建目录结构...
if not exist "%QWEN_HOME%\skills" mkdir "%QWEN_HOME%\skills"
if not exist "%QWEN_HOME%\extensions" mkdir "%QWEN_HOME%\extensions"
echo   [OK] 目录创建完成

echo.
echo [2/4] 部署扩展...
xcopy /E /I /Y "%SKILLS_SOURCE%\extensions\skill-evolution" "%QWEN_HOME%\extensions\skill-evolution" >nul
xcopy /E /I /Y "%SKILLS_SOURCE%\extensions\skill-task-integration" "%QWEN_HOME%\extensions\skill-task-integration" >nul
echo   [OK] 扩展部署完成

echo.
echo [3/4] 部署 skill...
set DEPLOYED=0

for %%D in (
  grounded-theory-expert
  social-network-analysis-expert
  bourdieu-field-analysis-expert
  msqca-analysis-expert
  did-analysis-expert
  data-analysis-expert
  business-ecosystem-analysis-expert
  business-model-analysis-expert
  actor-network-analysis-expert
  digital-marx-expert
  digital-durkheim-expert
  digital-weber-expert
  survey-design-expert
) do (
  if exist "%SKILLS_SOURCE%\%%D" (
    xcopy /E /I /Y "%SKILLS_SOURCE%\%%D" "%QWEN_HOME%\skills\%%D" >nul
    echo   [OK] %%D
    set /a DEPLOYED+=1
  )
)

echo.
echo [4/4] 配置 Qwen CLI...
findstr /C:"skill-evolution" "%QWEN_HOME%\config.yaml" >nul
if errorlevel 1 (
  echo.
  echo extensions: >> "%QWEN_HOME%\config.yaml"
  echo   enabled: >> "%QWEN_HOME%\config.yaml"
  echo     - skill-evolution >> "%QWEN_HOME%\config.yaml"
  echo     - skill-task-integration >> "%QWEN_HOME%\config.yaml"
  echo   [OK] 已添加扩展配置
) else (
  echo   [OK] 扩展配置已存在
)

echo.
echo ============================================================
echo 部署完成！
echo ============================================================
echo.
echo 部署统计:
echo   - 扩展：2 个
echo   - skill: %DEPLOYED% 个
echo.
echo 下一步:
echo   1. 重启 Qwen CLI（如果需要）
echo   2. 启动测试：qwen
echo   3. 开始测试 grounded-theory-expert
echo.

pause
