# AI 美学升级报告 Windows 安装器（作者：谭代坤（老谭出品））
# 用法：powershell -ExecutionPolicy Bypass -File install.ps1 [-Full] [-Claude]
param(
    [switch]$Full,
    [switch]$Claude
)
$ErrorActionPreference = "Stop"

$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if ($Claude) { $SkillsHome = Join-Path $env:USERPROFILE ".claude\skills"; $Tool = "claude" }
else {
    $CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE ".codex" }
    $SkillsHome = Join-Path $CodexHome "skills"; $Tool = "codex"
}
$TargetDir = Join-Path $SkillsHome "face-consultation-report"
$BinDir = Join-Path $env:USERPROFILE ".local\bin"

Write-Host "AI 美学升级报告安装器（Windows）"
Write-Host "仓库目录: $RootDir"
Write-Host "安装目录: $TargetDir"

# 查找 Python 3.10+
$Python = $null; $PyArgs = @()
foreach ($cand in @(@("py", "-3"), @("python"), @("python3"))) {
    try {
        $exe = $cand[0]; $pre = @($cand | Select-Object -Skip 1)
        $ver = & $exe @pre -c "import sys;print('%d.%d'%sys.version_info[:2])" 2>$null
        if ($LASTEXITCODE -eq 0 -and $ver -and ([version]$ver -ge [version]"3.10")) { $Python = $exe; $PyArgs = $pre; break }
    } catch {}
}
if (-not $Python) {
    Write-Host "【错误】未找到 Python 3.10 或以上版本。" -ForegroundColor Red
    Write-Host "请到 https://www.python.org/downloads/ 下载安装，安装时勾选 'Add Python to PATH'，然后重新运行本脚本。"
    exit 1
}

$BackupDir = $null
if (Test-Path $TargetDir) {
    $BackupDir = "$TargetDir.backup.$(Get-Date -Format yyyyMMdd-HHmmss)"
    Write-Host "发现已存在安装目录，备份到: $BackupDir"
    Move-Item $TargetDir $BackupDir
}
New-Item -ItemType Directory -Force -Path $TargetDir, $BinDir | Out-Null

Copy-Item "$RootDir\skill\SKILL.md" "$TargetDir\SKILL.md"
foreach ($d in @("agents", "references")) { Copy-Item -Recurse "$RootDir\skill\$d" "$TargetDir\$d" }
foreach ($d in @("scripts", "legacy", "templates")) { Copy-Item -Recurse "$RootDir\$d" "$TargetDir\$d" }
foreach ($f in @("requirements.txt", "README.md", "PRIVACY.md", "LICENSE")) { Copy-Item "$RootDir\$f" "$TargetDir\$f" }
New-Item -ItemType Directory -Force -Path "$TargetDir\knowledge" | Out-Null
Copy-Item "$RootDir\knowledge\README.md" "$TargetDir\knowledge\README.md"
if ($BackupDir -and (Test-Path "$BackupDir\knowledge")) {
    Copy-Item -Recurse -Force "$BackupDir\knowledge\*" "$TargetDir\knowledge\"
    Write-Host "已保留你之前放在 knowledge\ 里的资料"
}
Remove-Item -Recurse -Force "$TargetDir\scripts\__pycache__" -ErrorAction SilentlyContinue

Write-Host "创建 Python 虚拟环境..."
& $Python @PyArgs -m venv "$TargetDir\.venv"
$VenvPy = Join-Path $TargetDir ".venv\Scripts\python.exe"
& $VenvPy -m pip install --upgrade pip | Out-Null
& $VenvPy -m pip install -r "$TargetDir\requirements.txt"
if ($LASTEXITCODE -ne 0) { Write-Host "【错误】依赖安装失败，请检查网络后重试。" -ForegroundColor Red; exit 1 }

$cmds = @{
    "face-report-v2"      = "scripts\render_sales_v2.py";
    "face-report-handoff" = "scripts\build_handoff_sheet.py";
    "face-report-basic"   = "legacy\render_report.py"
}
foreach ($name in $cmds.Keys) {
    Set-Content -Encoding ASCII -Path (Join-Path $BinDir "$name.cmd") -Value "@echo off`r`n`"$VenvPy`" `"$TargetDir\$($cmds[$name])`" %*"
}

& $VenvPy "$RootDir\scripts\validate_install.py" --target $TargetDir
if ($LASTEXITCODE -ne 0) { Write-Host "【错误】安装校验未通过，请把上面的报错截图发给作者。" -ForegroundColor Red; exit 1 }

if ($Full) {
    Write-Host "安装 PNG 截图组件（Playwright + Chromium）..."
    & $VenvPy -m pip install "playwright>=1.40,<2" "python-docx>=1.0,<2" "openpyxl>=3.1,<4"
    if ($LASTEXITCODE -eq 0) { & $VenvPy -m playwright install chromium }
    if ($LASTEXITCODE -eq 0) { Write-Host "截图组件安装完成，可以导出 report-v2.png。" }
    else { Write-Host "【提示】截图组件安装失败（常见原因：网络无法下载 Chromium）。不影响生成 HTML 报告；网络正常后重新运行：install.ps1 -Full" -ForegroundColor Yellow }
} else {
    Write-Host "提示：未安装 PNG 截图组件。需要导出 report-v2.png 时运行：powershell -ExecutionPolicy Bypass -File install.ps1 -Full"
}

Write-Host ""
Write-Host "安装完成。技能目录（$Tool）: $TargetDir"
Write-Host "命令行入口: $BinDir\face-report-v2.cmd"
if (-not (($env:PATH -split ";") -contains $BinDir)) {
    Write-Host "如果提示找不到 face-report-v2，请把 $BinDir 加入 PATH，或直接用完整路径运行。"
}
