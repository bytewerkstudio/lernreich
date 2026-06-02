$ErrorActionPreference = "Stop"

python -m pip show pyinstaller *> $null
if ($LASTEXITCODE -ne 0) {
    python -m pip install pyinstaller
}

python -m pip show pystray *> $null
if ($LASTEXITCODE -ne 0) {
    python -m pip install pystray
}

python -m pip show pillow *> $null
if ($LASTEXITCODE -ne 0) {
    python -m pip install pillow
}

python -m PyInstaller `
    --noconfirm `
    --windowed `
    --onefile `
    --icon ".\assets\lernreich.ico" `
    --add-data ".\assets\lernreich.ico;assets" `
    --version-file ".\version_info.txt" `
    --name "Lernreich" `
    ".\study_city.py"

Write-Host "Fertig: dist\Lernreich.exe"
