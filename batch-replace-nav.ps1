# 批量替换导航链接脚本

Get-ChildItem "D:\socienceAI\agentskills\download\*.html" | ForEach-Object {
    $file = $_.FullName
    Write-Host "处理：$file"
    
    # 读取文件
    $content = Get-Content $file -Encoding UTF8 -Raw
    
    # 替换导航链接
    $content = $content -replace 'ai-agents\.html','skills.html'
    $content = $content -replace 'Agent 服务','方法论技能'
    $content = $content -replace '社科智能体','社科技能'
    $content = $content -replace '智能体','技能'
    
    # 保存文件
    $content | Set-Content $file -Encoding UTF8
    
    Write-Host "✅ 完成：$file"
}

Write-Host "`n✅ 批量替换完成！"
