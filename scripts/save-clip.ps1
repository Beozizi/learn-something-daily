param([string]$Out)
Add-Type -AssemblyName System.Windows.Forms, System.Drawing
$img = [System.Windows.Forms.Clipboard]::GetImage()
if (-not $img) { "no image in clipboard"; exit 1 }
New-Item -ItemType Directory -Force (Split-Path $Out) | Out-Null
$img.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
"$($img.Width)x$($img.Height) -> $Out"
