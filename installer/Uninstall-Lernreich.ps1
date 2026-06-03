[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Windows.Forms

$installDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$resolvedInstallDir = (Resolve-Path -LiteralPath $installDir).Path
$installLeaf = [System.IO.Path]::GetFileName($resolvedInstallDir.TrimEnd("\"))
$installRoot = [System.IO.Path]::GetPathRoot($resolvedInstallDir)
$markerPath = Join-Path $resolvedInstallDir ".lernreich-install.json"
$exePath = Join-Path $resolvedInstallDir "Lernreich.exe"

if ($resolvedInstallDir.TrimEnd("\") -ieq $installRoot.TrimEnd("\")) {
  throw "Sicherheitsstopp: Der Installationsordner ist ein Laufwerksstamm."
}

if ($installLeaf -notlike "Lernreich*") {
  throw "Sicherheitsstopp: Unerwarteter Installationsordner '$resolvedInstallDir'."
}

if (-not (Test-Path -LiteralPath $markerPath) -or -not (Test-Path -LiteralPath $exePath)) {
  throw "Sicherheitsstopp: Lernreich-Installationsdaten wurden nicht gefunden."
}

$language = "de"
try {
  $marker = Get-Content -LiteralPath $markerPath -Raw | ConvertFrom-Json
  if ($marker.language -eq "en") {
    $language = "en"
  }
} catch {}

$Text = @{
  de = @{
    Title = "Lernreich deinstallieren"
    DataQuestion = "M$([char]246)chtest du auch Lernfortschritt, Statistikdaten und gespeicherte Lernreich-Daten entfernen?`r`n`r`nBetroffene Ordner:`r`n{0}`r`n`r`nJa = alles l$([char]246)schen`r`nNein = pers$([char]246)nliche Lerndaten behalten"
    DoneRemoved = "Lernreich wurde deinstalliert. Lernfortschritt und Statistikdaten wurden entfernt."
    DoneKept = "Lernreich wurde deinstalliert. Lernfortschritt und Statistikdaten bleiben erhalten."
  }
  en = @{
    Title = "Uninstall Lernreich"
    DataQuestion = "Do you also want to remove learning progress, statistics, and saved Lernreich data?`r`n`r`nAffected folders:`r`n{0}`r`n`r`nYes = delete everything`r`nNo = keep personal learning data"
    DoneRemoved = "Lernreich was uninstalled. Learning progress and statistics were removed."
    DoneKept = "Lernreich was uninstalled. Learning progress and statistics were kept."
  }
}

$text = $Text[$language]

function Get-LernreichDataFolders {
  $candidates = @(
    (Join-Path $env:APPDATA "Lernreich"),
    (Join-Path $env:LOCALAPPDATA "Lernreich")
  ) | Select-Object -Unique

  foreach ($candidate in $candidates) {
    if (Test-Path -LiteralPath $candidate) {
      $resolved = (Resolve-Path -LiteralPath $candidate).Path
      $leaf = [System.IO.Path]::GetFileName($resolved.TrimEnd("\"))
      if ($leaf -eq "Lernreich") {
        $resolved
      }
    }
  }
}

$dataFolders = @(Get-LernreichDataFolders)
$removeData = $false

if ($dataFolders.Count -gt 0) {
  $folderList = $dataFolders -join "`r`n"
  $answer = [System.Windows.Forms.MessageBox]::Show(
    [string]::Format($text.DataQuestion, $folderList),
    $text.Title,
    [System.Windows.Forms.MessageBoxButtons]::YesNo,
    [System.Windows.Forms.MessageBoxIcon]::Question
  )
  $removeData = ($answer -eq [System.Windows.Forms.DialogResult]::Yes)
}

Get-Process -Name "Lernreich" -ErrorAction SilentlyContinue | Stop-Process -Force

$desktopShortcut = Join-Path ([Environment]::GetFolderPath("DesktopDirectory")) "Lernreich.lnk"
$startMenuFolder = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Lernreich"
$registryPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\Lernreich"

Remove-Item -LiteralPath $desktopShortcut -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $startMenuFolder -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $registryPath -Recurse -Force -ErrorAction SilentlyContinue

if ($removeData) {
  foreach ($folder in $dataFolders) {
    Remove-Item -LiteralPath $folder -Recurse -Force -ErrorAction SilentlyContinue
  }
}

Remove-Item -LiteralPath $resolvedInstallDir -Recurse -Force -ErrorAction SilentlyContinue

$doneMessage = if ($removeData) { $text.DoneRemoved } else { $text.DoneKept }
[System.Windows.Forms.MessageBox]::Show(
  $doneMessage,
  $text.Title,
  [System.Windows.Forms.MessageBoxButtons]::OK,
  [System.Windows.Forms.MessageBoxIcon]::Information
) | Out-Null
