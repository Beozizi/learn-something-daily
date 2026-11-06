# Cài công cụ cho dự án Learn Something Daily trên một máy Windows mới.
#
#   powershell -ExecutionPolicy Bypass -File scripts\cai-dat.ps1 [-Tools D:\lsd-tools] [-CPU]
#
#   -Tools  thư mục chứa venv + model (mặc định <dự án>\.tools). Chọn ổ còn ≥ 15 GB trống.
#   -CPU    máy không có card NVIDIA: cài torch/onnxruntime bản CPU (chậm hơn nhưng chạy được).
#
# Cài: Python 3.12 (py), uv, ffmpeg, Node.js LTS, Git (qua winget) → venv-chung (lồng tiếng GenMax,
# tách nền, dò bảng trống, ảnh) + venv-align (WhisperX) → ghi cau-hinh.json → chạy kiem-tra-may.py.
# Không đụng tới API key: tự tạo .genmax_key.txt (và .chatgpt_key.txt nếu dùng) ở gốc dự án.
param(
    [string]$Tools = "",
    [switch]$CPU
)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
if (-not $Tools) { $Tools = Join-Path $Root ".tools" }
New-Item -ItemType Directory -Force $Tools, (Join-Path $Tools "models") | Out-Null

function Buoc($msg) { Write-Host "`n== $msg" -ForegroundColor Cyan }
function Co($cmd) { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }
function LamMoiPath {
    $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
                [Environment]::GetEnvironmentVariable("Path", "User")
}

Buoc "1/5 Phần mềm nền (winget)"
if (-not (Co "winget")) { throw "Thiếu winget (App Installer). Cài từ Microsoft Store rồi chạy lại." }
$goi = @(
    @{ id = "Python.Python.3.12"; lenh = "py" },
    @{ id = "astral-sh.uv";       lenh = "uv" },
    @{ id = "Gyan.FFmpeg";        lenh = "ffmpeg" },
    @{ id = "OpenJS.NodeJS.LTS";  lenh = "node" },
    @{ id = "Git.Git";            lenh = "git" }
)
foreach ($g in $goi) {
    if (Co $g.lenh) { Write-Host "  có sẵn: $($g.lenh)"; continue }
    Write-Host "  cài $($g.id)…"
    winget install --id $g.id -e --silent --accept-package-agreements --accept-source-agreements
    LamMoiPath
}
LamMoiPath
$ffmpegBin = ""
if (Co "ffmpeg") { $ffmpegBin = Split-Path -Parent (Get-Command ffmpeg).Source }
else {
    $f = Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Recurse -Filter ffmpeg.exe -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($f) { $ffmpegBin = $f.DirectoryName } else { throw "Không tìm thấy ffmpeg sau khi cài." }
}

$env:UV_CACHE_DIR = Join-Path $Tools "uv-cache"
$env:UV_PYTHON_INSTALL_DIR = Join-Path $Tools "python"
$chung = Join-Path $Tools "venv-chung"
$align = Join-Path $Tools "venv-align"

Buoc "2/5 venv-chung (GenMax, rembg, OpenCV, ảnh)"
if (-not (Test-Path "$chung\Scripts\python.exe")) { uv venv $chung --python 3.12 }
$onnx = if ($CPU) { "onnxruntime" } else { "onnxruntime-gpu" }
uv pip install --python "$chung\Scripts\python.exe" numpy soundfile requests opencv-python-headless pillow pypdf pyyaml rembg $onnx

Buoc "3/5 venv-align (WhisperX, torch)"
if (-not (Test-Path "$align\Scripts\python.exe")) { uv venv $align --python 3.12 }
$idx = if ($CPU) { "https://download.pytorch.org/whl/cpu" } else { "https://download.pytorch.org/whl/cu128" }
uv pip install --python "$align\Scripts\python.exe" "torch==2.8.0" "torchaudio==2.8.0" --index-url $idx
uv pip install --python "$align\Scripts\python.exe" "whisperx==3.8.6" "torch==2.8.0" "torchaudio==2.8.0" --extra-index-url $idx --index-strategy unsafe-best-match

Buoc "4/5 HyperFrames (Node)"
Push-Location (Join-Path $Root "tap\2026-11-06-why-cant-you-focus\video")
npx --yes hyperframes@0.9.10 --version
Pop-Location

Buoc "5/5 Ghi cau-hinh.json"
$cfgPath = Join-Path $Root "cau-hinh.json"
if (Test-Path $cfgPath) { Copy-Item $cfgPath "$cfgPath.cu" -Force; Write-Host "  bản cũ lưu ở cau-hinh.json.cu" }
$cfg = [ordered]@{
    tools      = $Tools
    models     = (Join-Path $Tools "models")
    ffmpeg_bin = $ffmpegBin
    venv       = [ordered]@{ tts = $chung; align = $align; media = $chung; chung = $chung }
}
$json = $cfg | ConvertTo-Json -Depth 4
[IO.File]::WriteAllText($cfgPath, $json, (New-Object Text.UTF8Encoding $false))
Write-Host "  $cfgPath"

Write-Host "`nKiểm tra máy:" -ForegroundColor Cyan
py (Join-Path $Root "scripts\kiem-tra-may.py")
