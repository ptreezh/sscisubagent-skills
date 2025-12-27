# PowerShell script to verify all skill files compliance with agentskills.io standard

$dirs = Get-ChildItem 'D:\stigmergy-CLI-Multi-Agents\sscisubagent-skills\skills' -Directory
$compliant = 0
$nonCompliant = 0
$totalCount = 0

foreach ($dir in $dirs) {
    $skillFile = Join-Path $dir.FullName 'SKILL.md'
    if (Test-Path $skillFile) {
        $totalCount++
        $lines = Get-Content $skillFile
        
        # Check if first line is ---
        if ($lines.Count -ge 1 -and $lines[0] -eq '---') {
            # Check if second line contains name field
            if ($lines.Count -ge 2) {
                $secondLine = $lines[1].Trim()
                if ($secondLine -match '^name:\s*(.+)$') {
                    Write-Host "$($dir.Name): COMPLIANT" -ForegroundColor Green
                    $compliant++
                } else {
                    Write-Host "$($dir.Name): MISSING name field in second line" -ForegroundColor Red
                    $nonCompliant++
                }
            } else {
                Write-Host "$($dir.Name): TOO FEW LINES" -ForegroundColor Red
                $nonCompliant++
            }
        } else {
            Write-Host "$($dir.Name): MISSING YAML frontmatter separator" -ForegroundColor Red
            $nonCompliant++
        }
    }
}

Write-Host ""
Write-Host "Total skills checked: $totalCount" -ForegroundColor Yellow
Write-Host "Compliant skills: $compliant" -ForegroundColor Yellow
Write-Host "Non-compliant skills: $nonCompliant" -ForegroundColor Yellow