[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

$installerDir = $PSScriptRoot
$siteRoot = Split-Path -Parent $installerDir
$uploadsRoot = Split-Path -Parent $siteRoot
$downloadsDir = Join-Path $siteRoot "downloads"
$privateBuildDir = Join-Path $uploadsRoot "private-build"
$sourceExe = Join-Path $privateBuildDir "Lernreich.exe"
$sourceLogo = Join-Path $siteRoot "logo.png"
$outputExe = Join-Path $downloadsDir "Lernreich-Setup.exe"
$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) "LernreichInstallerBuild"
$stagingDir = Join-Path $tempRoot "build-staging"
$iexpressOutputExe = Join-Path $stagingDir "Lernreich-Setup.exe"
$sedFile = Join-Path $stagingDir "Lernreich-Setup.sed"

if (-not (Test-Path -LiteralPath $sourceExe)) {
  throw "Lernreich.exe wurde nicht gefunden: $sourceExe. Lege die private App-Datei in diesen Ordner, damit nur der Setup-Installer oeffentlich im Website-Download liegt."
}

if (Test-Path -LiteralPath $stagingDir) {
  $resolvedStaging = (Resolve-Path -LiteralPath $stagingDir).Path
  $resolvedTempRoot = if (Test-Path -LiteralPath $tempRoot) {
    (Resolve-Path -LiteralPath $tempRoot).Path
  } else {
    $tempRoot
  }
  if (-not $resolvedStaging.StartsWith($resolvedTempRoot, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Sicherheitsstopp: Unerwarteter Staging-Ordner '$resolvedStaging'."
  }
  Remove-Item -LiteralPath $stagingDir -Recurse -Force
}

New-Item -ItemType Directory -Path $stagingDir -Force | Out-Null

function Copy-Utf8BomFile {
  param(
    [Parameter(Mandatory = $true)][string]$Source,
    [Parameter(Mandatory = $true)][string]$Destination
  )

  $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
  $utf8Bom = New-Object System.Text.UTF8Encoding($true)
  $content = [System.IO.File]::ReadAllText($Source, $utf8NoBom)
  [System.IO.File]::WriteAllText($Destination, $content, $utf8Bom)
}

Copy-Item -LiteralPath $sourceExe -Destination (Join-Path $stagingDir "Lernreich.exe") -Force
Copy-Utf8BomFile -Source (Join-Path $installerDir "Install-Lernreich.ps1") -Destination (Join-Path $stagingDir "Install-Lernreich.ps1")
Copy-Utf8BomFile -Source (Join-Path $installerDir "Uninstall-Lernreich.ps1") -Destination (Join-Path $stagingDir "Uninstall-Lernreich.ps1")

$payloadFiles = @(
  "Install-Lernreich.ps1",
  "Uninstall-Lernreich.ps1",
  "Lernreich.exe"
)

if (Test-Path -LiteralPath $sourceLogo) {
  Copy-Item -LiteralPath $sourceLogo -Destination (Join-Path $stagingDir "logo.png") -Force
  $payloadFiles += "logo.png"
}

$stringLines = for ($i = 0; $i -lt $payloadFiles.Count; $i++) {
  "FILE$i=""$($payloadFiles[$i])"""
}

$sourceFileLines = for ($i = 0; $i -lt $payloadFiles.Count; $i++) {
  "%FILE$i%="
}

$sedContent = @"
[Version]
Class=IEXPRESS
SEDVersion=3
[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=0
HideExtractAnimation=1
UseLongFileName=1
InsideCompressed=0
CAB_FixedSize=0
CAB_ResvCodeSigning=0
RebootMode=N
InstallPrompt=
DisplayLicense=
FinishMessage=
TargetName=$iexpressOutputExe
FriendlyName=Lernreich Setup
AppLaunched=powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File Install-Lernreich.ps1
PostInstallCmd=<None>
AdminQuietInstCmd=
UserQuietInstCmd=
SourceFiles=SourceFiles
[Strings]
$($stringLines -join "`r`n")
[SourceFiles]
SourceFiles0=$stagingDir\
[SourceFiles0]
$($sourceFileLines -join "`r`n")
"@

Set-Content -LiteralPath $sedFile -Value $sedContent -Encoding ASCII

$iexpress = Join-Path $env:SystemRoot "System32\iexpress.exe"
if (-not (Test-Path -LiteralPath $iexpress)) {
  throw "IExpress wurde auf diesem Windows-System nicht gefunden."
}

& $iexpress /N /Q $sedFile | Out-Null

for ($i = 0; $i -lt 120 -and -not (Test-Path -LiteralPath $iexpressOutputExe); $i++) {
  Start-Sleep -Seconds 1
}

if (-not (Test-Path -LiteralPath $iexpressOutputExe)) {
  throw "Der Installer wurde nicht erstellt: $iexpressOutputExe"
}

$lastSize = -1
$stableSeconds = 0
for ($i = 0; $i -lt 120; $i++) {
  $currentSize = (Get-Item -LiteralPath $iexpressOutputExe).Length
  if ($currentSize -eq $lastSize -and $currentSize -gt 5MB) {
    $stableSeconds++
  } else {
    $stableSeconds = 0
    $lastSize = $currentSize
  }

  if ($stableSeconds -ge 3) {
    break
  }

  Start-Sleep -Seconds 1
}

$finalSize = (Get-Item -LiteralPath $iexpressOutputExe).Length
if ($finalSize -le 5MB) {
  throw "Der Installer ist unerwartet klein ($finalSize Bytes)."
}

for ($i = 0; $i -lt 30; $i++) {
  try {
    Copy-Item -LiteralPath $iexpressOutputExe -Destination $outputExe -Force
    break
  } catch {
    if ($i -eq 29) {
      throw
    }
    Start-Sleep -Seconds 1
  }
}

$cert = Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert |
  Where-Object { $_.Subject -eq "CN=Hijratullah Haqmal" -and $_.HasPrivateKey } |
  Select-Object -First 1

if ($cert) {
  $signatureResult = Set-AuthenticodeSignature -FilePath $outputExe -Certificate $cert
  if ($signatureResult.Status -ne "Valid") {
    Write-Warning "Signaturstatus nach dem Signieren: $($signatureResult.Status) - $($signatureResult.StatusMessage)"
  }
}

Get-Item -LiteralPath $outputExe | Select-Object FullName, Length, LastWriteTime
Get-AuthenticodeSignature -LiteralPath $outputExe | Select-Object Status, StatusMessage

exit 0
