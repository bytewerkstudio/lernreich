[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[System.Windows.Forms.Application]::EnableVisualStyles()

$appName = "Lernreich"
$publisher = "Bytewerk Studio"
$version = "1.2.0"
$sourceExe = Join-Path $PSScriptRoot "Lernreich.exe"
$sourceUninstaller = Join-Path $PSScriptRoot "Uninstall-Lernreich.ps1"
$sourceLogo = Join-Path $PSScriptRoot "logo.png"
$defaultInstallDir = Join-Path $env:LOCALAPPDATA "Programs\Lernreich"

$SetupText = @{
  de = @{
    WindowTitle = "Lernreich Setup"
    HeaderTitle = "Lernreich installieren"
    HeaderSubtitle = "Einmal einrichten, danach bequem aus dem Startmenü oder vom Desktop starten."
    Language = "Sprache"
    Folder = "Installationsordner"
    FolderHint = "Wenn du einen Hauptordner wählst, wird darin automatisch ein Unterordner 'Lernreich' erstellt."
    Browse = "Auswählen"
    Options = "Optionen"
    DesktopShortcut = "Desktop-Verknüpfung erstellen"
    StartMenuShortcut = "Startmenü-Verknüpfung erstellen"
    LaunchAfterInstall = "Nach der Installation starten"
    Install = "Installieren"
    Cancel = "Abbrechen"
    BrowseDialog = "Installationsordner auswählen"
    InvalidFolder = "Bitte wähle einen gültigen Installationsordner."
    MissingApp = "Lernreich.exe wurde im Setup-Paket nicht gefunden."
    ProgressTitle = "Installation läuft"
    ProgressSubtitle = "Lernreich wird eingerichtet."
    StepPrepare = "Installation wird vorbereitet..."
    StepCopy = "Programmdateien werden kopiert..."
    StepShortcuts = "Verknüpfungen werden erstellt..."
    StepRegistry = "Windows-Eintrag wird angelegt..."
    StepFinish = "Installation wird abgeschlossen..."
    ErrorTitle = "Installation fehlgeschlagen"
    ErrorMessage = "Die Installation konnte nicht abgeschlossen werden:"
  }
  en = @{
    WindowTitle = "Lernreich Setup"
    HeaderTitle = "Install Lernreich"
    HeaderSubtitle = "Set it up once, then start it from the Start menu or desktop."
    Language = "Language"
    Folder = "Installation folder"
    FolderHint = "If you choose a parent folder, a 'Lernreich' subfolder will be created automatically."
    Browse = "Choose"
    Options = "Options"
    DesktopShortcut = "Create desktop shortcut"
    StartMenuShortcut = "Create Start menu shortcut"
    LaunchAfterInstall = "Launch after installation"
    Install = "Install"
    Cancel = "Cancel"
    BrowseDialog = "Choose installation folder"
    InvalidFolder = "Please choose a valid installation folder."
    MissingApp = "Lernreich.exe was not found in the setup package."
    ProgressTitle = "Installing"
    ProgressSubtitle = "Lernreich is being set up."
    StepPrepare = "Preparing installation..."
    StepCopy = "Copying program files..."
    StepShortcuts = "Creating shortcuts..."
    StepRegistry = "Adding Windows entry..."
    StepFinish = "Finishing installation..."
    ErrorTitle = "Installation failed"
    ErrorMessage = "The installation could not be completed:"
  }
}

function Get-UiFont {
  param([float]$Size = 9.0, [System.Drawing.FontStyle]$Style = [System.Drawing.FontStyle]::Regular)
  New-Object System.Drawing.Font("Segoe UI", $Size, $Style)
}

function Get-Color {
  param([string]$Html)
  [System.Drawing.ColorTranslator]::FromHtml($Html)
}

function Resolve-InstallDirectory {
  param([Parameter(Mandatory = $true)][string]$RequestedPath)

  if ([string]::IsNullOrWhiteSpace($RequestedPath)) {
    throw "Empty path"
  }

  $expandedPath = [Environment]::ExpandEnvironmentVariables($RequestedPath.Trim())
  if (-not [System.IO.Path]::IsPathRooted($expandedPath)) {
    throw "Path is not rooted"
  }

  $fullPath = [System.IO.Path]::GetFullPath($expandedPath)
  $fullPath = $fullPath.TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)
  $leaf = [System.IO.Path]::GetFileName($fullPath)

  if ($leaf -notlike "Lernreich*") {
    $fullPath = Join-Path $fullPath "Lernreich"
    $leaf = "Lernreich"
  }

  $root = [System.IO.Path]::GetPathRoot($fullPath)
  if ($fullPath.TrimEnd("\") -ieq $root.TrimEnd("\")) {
    throw "Path points to a drive root"
  }

  if ([string]::IsNullOrWhiteSpace($leaf) -or $leaf -notlike "Lernreich*") {
    throw "Path must be a Lernreich folder"
  }

  $fullPath
}

function Show-SetupForm {
  $state = @{
    Result = $null
    Language = "de"
  }

  $form = New-Object System.Windows.Forms.Form
  $form.Text = $SetupText.de.WindowTitle
  $form.StartPosition = "CenterScreen"
  $form.FormBorderStyle = "FixedSingle"
  $form.MaximizeBox = $false
  $form.MinimizeBox = $true
  $form.ClientSize = New-Object System.Drawing.Size(700, 560)
  $form.BackColor = Get-Color "#f7f7f5"
  $form.Font = Get-UiFont 9

  if (Test-Path -LiteralPath $sourceExe) {
    try { $form.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($sourceExe) } catch {}
  }

  $header = New-Object System.Windows.Forms.Panel
  $header.Location = New-Object System.Drawing.Point(0, 0)
  $header.Size = New-Object System.Drawing.Size(700, 132)
  $header.BackColor = Get-Color "#18191c"
  $form.Controls.Add($header)

  if (Test-Path -LiteralPath $sourceLogo) {
    try {
      $logo = New-Object System.Windows.Forms.PictureBox
      $logo.Location = New-Object System.Drawing.Point(38, 36)
      $logo.Size = New-Object System.Drawing.Size(54, 54)
      $logo.SizeMode = "Zoom"
      $logo.Image = [System.Drawing.Image]::FromFile($sourceLogo)
      $header.Controls.Add($logo)
    } catch {}
  }

  $titleLabel = New-Object System.Windows.Forms.Label
  $titleLabel.Location = New-Object System.Drawing.Point(112, 34)
  $titleLabel.Size = New-Object System.Drawing.Size(540, 34)
  $titleLabel.ForeColor = [System.Drawing.Color]::White
  $titleLabel.BackColor = Get-Color "#18191c"
  $titleLabel.Font = Get-UiFont 18 ([System.Drawing.FontStyle]::Bold)
  $header.Controls.Add($titleLabel)

  $subtitleLabel = New-Object System.Windows.Forms.Label
  $subtitleLabel.Location = New-Object System.Drawing.Point(115, 72)
  $subtitleLabel.Size = New-Object System.Drawing.Size(530, 40)
  $subtitleLabel.ForeColor = Get-Color "#d7dae0"
  $subtitleLabel.BackColor = Get-Color "#18191c"
  $subtitleLabel.Font = Get-UiFont 10
  $header.Controls.Add($subtitleLabel)

  $languageLabel = New-Object System.Windows.Forms.Label
  $languageLabel.Location = New-Object System.Drawing.Point(42, 166)
  $languageLabel.Size = New-Object System.Drawing.Size(180, 24)
  $languageLabel.Font = Get-UiFont 10 ([System.Drawing.FontStyle]::Bold)
  $form.Controls.Add($languageLabel)

  $languageCombo = New-Object System.Windows.Forms.ComboBox
  $languageCombo.Location = New-Object System.Drawing.Point(42, 194)
  $languageCombo.Size = New-Object System.Drawing.Size(236, 28)
  $languageCombo.DropDownStyle = "DropDownList"
  [void]$languageCombo.Items.Add("Deutsch")
  [void]$languageCombo.Items.Add("English")
  $languageCombo.SelectedIndex = 0
  $form.Controls.Add($languageCombo)

  $folderLabel = New-Object System.Windows.Forms.Label
  $folderLabel.Location = New-Object System.Drawing.Point(42, 248)
  $folderLabel.Size = New-Object System.Drawing.Size(220, 24)
  $folderLabel.Font = Get-UiFont 10 ([System.Drawing.FontStyle]::Bold)
  $form.Controls.Add($folderLabel)

  $folderBox = New-Object System.Windows.Forms.TextBox
  $folderBox.Location = New-Object System.Drawing.Point(42, 278)
  $folderBox.Size = New-Object System.Drawing.Size(470, 28)
  $folderBox.Text = $defaultInstallDir
  $form.Controls.Add($folderBox)

  $browseButton = New-Object System.Windows.Forms.Button
  $browseButton.Location = New-Object System.Drawing.Point(526, 276)
  $browseButton.Size = New-Object System.Drawing.Size(126, 32)
  $browseButton.FlatStyle = "Flat"
  $browseButton.BackColor = [System.Drawing.Color]::White
  $browseButton.ForeColor = Get-Color "#18191c"
  $browseButton.Font = Get-UiFont 9 ([System.Drawing.FontStyle]::Bold)
  $form.Controls.Add($browseButton)

  $folderHintLabel = New-Object System.Windows.Forms.Label
  $folderHintLabel.Location = New-Object System.Drawing.Point(42, 314)
  $folderHintLabel.Size = New-Object System.Drawing.Size(610, 34)
  $folderHintLabel.ForeColor = Get-Color "#71747c"
  $folderHintLabel.Font = Get-UiFont 8.5
  $form.Controls.Add($folderHintLabel)

  $optionsLabel = New-Object System.Windows.Forms.Label
  $optionsLabel.Location = New-Object System.Drawing.Point(42, 368)
  $optionsLabel.Size = New-Object System.Drawing.Size(180, 24)
  $optionsLabel.Font = Get-UiFont 10 ([System.Drawing.FontStyle]::Bold)
  $form.Controls.Add($optionsLabel)

  $desktopCheck = New-Object System.Windows.Forms.CheckBox
  $desktopCheck.Location = New-Object System.Drawing.Point(45, 400)
  $desktopCheck.Size = New-Object System.Drawing.Size(280, 28)
  $desktopCheck.Checked = $true
  $desktopCheck.Font = Get-UiFont 9.5
  $desktopCheck.BackColor = Get-Color "#f7f7f5"
  $form.Controls.Add($desktopCheck)

  $startMenuCheck = New-Object System.Windows.Forms.CheckBox
  $startMenuCheck.Location = New-Object System.Drawing.Point(356, 400)
  $startMenuCheck.Size = New-Object System.Drawing.Size(292, 28)
  $startMenuCheck.Checked = $true
  $startMenuCheck.Font = Get-UiFont 9.5
  $startMenuCheck.BackColor = Get-Color "#f7f7f5"
  $form.Controls.Add($startMenuCheck)

  $launchCheck = New-Object System.Windows.Forms.CheckBox
  $launchCheck.Location = New-Object System.Drawing.Point(45, 436)
  $launchCheck.Size = New-Object System.Drawing.Size(320, 28)
  $launchCheck.Checked = $true
  $launchCheck.Font = Get-UiFont 9.5
  $launchCheck.BackColor = Get-Color "#f7f7f5"
  $form.Controls.Add($launchCheck)

  $installButton = New-Object System.Windows.Forms.Button
  $installButton.Location = New-Object System.Drawing.Point(458, 498)
  $installButton.Size = New-Object System.Drawing.Size(194, 40)
  $installButton.FlatStyle = "Flat"
  $installButton.BackColor = Get-Color "#18191c"
  $installButton.ForeColor = [System.Drawing.Color]::White
  $installButton.Font = Get-UiFont 10 ([System.Drawing.FontStyle]::Bold)
  $form.Controls.Add($installButton)

  $cancelButton = New-Object System.Windows.Forms.Button
  $cancelButton.Location = New-Object System.Drawing.Point(326, 498)
  $cancelButton.Size = New-Object System.Drawing.Size(116, 40)
  $cancelButton.FlatStyle = "Flat"
  $cancelButton.BackColor = [System.Drawing.Color]::White
  $cancelButton.ForeColor = Get-Color "#18191c"
  $cancelButton.Font = Get-UiFont 9 ([System.Drawing.FontStyle]::Bold)
  $form.Controls.Add($cancelButton)

  function Apply-SetupLanguage {
    param([string]$LanguageKey)
    $text = $SetupText[$LanguageKey]
    $form.Text = $text.WindowTitle
    $titleLabel.Text = $text.HeaderTitle
    $subtitleLabel.Text = $text.HeaderSubtitle
    $languageLabel.Text = $text.Language
    $folderLabel.Text = $text.Folder
    $folderHintLabel.Text = $text.FolderHint
    $browseButton.Text = $text.Browse
    $optionsLabel.Text = $text.Options
    $desktopCheck.Text = $text.DesktopShortcut
    $startMenuCheck.Text = $text.StartMenuShortcut
    $launchCheck.Text = $text.LaunchAfterInstall
    $installButton.Text = $text.Install
    $cancelButton.Text = $text.Cancel
  }

  $languageCombo.Add_SelectedIndexChanged({
    $state.Language = if ($languageCombo.SelectedIndex -eq 1) { "en" } else { "de" }
    Apply-SetupLanguage $state.Language
  })

  $browseButton.Add_Click({
    $text = $SetupText[$state.Language]
    $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
    $dialog.Description = $text.BrowseDialog
    $dialog.ShowNewFolderButton = $true
    if (Test-Path -LiteralPath $folderBox.Text) {
      $dialog.SelectedPath = $folderBox.Text
    }

    if ($dialog.ShowDialog($form) -eq [System.Windows.Forms.DialogResult]::OK) {
      try {
        $folderBox.Text = Resolve-InstallDirectory $dialog.SelectedPath
      } catch {
        $folderBox.Text = Join-Path $dialog.SelectedPath "Lernreich"
      }
    }
  })

  $installButton.Add_Click({
    $text = $SetupText[$state.Language]
    try {
      $installDir = Resolve-InstallDirectory $folderBox.Text
    } catch {
      [System.Windows.Forms.MessageBox]::Show($text.InvalidFolder, $text.WindowTitle, "OK", "Warning") | Out-Null
      return
    }

    $state.Result = [pscustomobject]@{
      Language = $state.Language
      InstallDir = $installDir
      DesktopShortcut = [bool]$desktopCheck.Checked
      StartMenuShortcut = [bool]$startMenuCheck.Checked
      LaunchAfterInstall = [bool]$launchCheck.Checked
    }

    $form.DialogResult = [System.Windows.Forms.DialogResult]::OK
    $form.Close()
  })

  $cancelButton.Add_Click({
    $state.Result = $null
    $form.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
    $form.Close()
  })

  Apply-SetupLanguage "de"
  [void]$form.ShowDialog()
  $state.Result
}

function New-AppShortcut {
  param(
    [Parameter(Mandatory = $true)][string]$ShortcutPath,
    [Parameter(Mandatory = $true)][string]$TargetPath,
    [string]$Arguments = "",
    [string]$Description = "Lernreich starten",
    [Parameter(Mandatory = $true)][string]$IconPath
  )

  $shortcutFolder = Split-Path -Parent $ShortcutPath
  New-Item -ItemType Directory -Path $shortcutFolder -Force | Out-Null

  $shell = New-Object -ComObject WScript.Shell
  $shortcut = $shell.CreateShortcut($ShortcutPath)
  $shortcut.TargetPath = $TargetPath
  $shortcut.Arguments = $Arguments
  $shortcut.WorkingDirectory = Split-Path -Parent $TargetPath
  $shortcut.IconLocation = "$IconPath,0"
  $shortcut.Description = $Description
  $shortcut.Save()
}

function New-ProgressWindow {
  param([hashtable]$Text)

  $form = New-Object System.Windows.Forms.Form
  $form.Text = $Text.WindowTitle
  $form.StartPosition = "CenterScreen"
  $form.FormBorderStyle = "FixedSingle"
  $form.MaximizeBox = $false
  $form.MinimizeBox = $false
  $form.ClientSize = New-Object System.Drawing.Size(560, 255)
  $form.BackColor = Get-Color "#f7f7f5"
  $form.Font = Get-UiFont 9

  if (Test-Path -LiteralPath $sourceExe) {
    try { $form.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($sourceExe) } catch {}
  }

  $title = New-Object System.Windows.Forms.Label
  $title.Location = New-Object System.Drawing.Point(36, 34)
  $title.Size = New-Object System.Drawing.Size(490, 36)
  $title.Font = Get-UiFont 17 ([System.Drawing.FontStyle]::Bold)
  $title.Text = $Text.ProgressTitle
  $form.Controls.Add($title)

  $subtitle = New-Object System.Windows.Forms.Label
  $subtitle.Location = New-Object System.Drawing.Point(39, 76)
  $subtitle.Size = New-Object System.Drawing.Size(490, 28)
  $subtitle.Font = Get-UiFont 10
  $subtitle.ForeColor = Get-Color "#71747c"
  $subtitle.Text = $Text.ProgressSubtitle
  $form.Controls.Add($subtitle)

  $status = New-Object System.Windows.Forms.Label
  $status.Location = New-Object System.Drawing.Point(39, 126)
  $status.Size = New-Object System.Drawing.Size(490, 26)
  $status.Font = Get-UiFont 9.5
  $status.ForeColor = Get-Color "#3c3f46"
  $form.Controls.Add($status)

  $bar = New-Object System.Windows.Forms.ProgressBar
  $bar.Location = New-Object System.Drawing.Point(42, 162)
  $bar.Size = New-Object System.Drawing.Size(478, 20)
  $bar.Minimum = 0
  $bar.Maximum = 100
  $bar.Value = 0
  $form.Controls.Add($bar)

  [pscustomobject]@{
    Form = $form
    Bar = $bar
    Status = $status
    Value = 0
  }
}

function Update-SetupProgress {
  param(
    [Parameter(Mandatory = $true)]$Ui,
    [Parameter(Mandatory = $true)][int]$Target,
    [Parameter(Mandatory = $true)][string]$Message,
    [int]$DelayMs = 18
  )

  $Ui.Status.Text = $Message
  for ($i = [int]$Ui.Value; $i -le $Target; $i++) {
    $Ui.Bar.Value = [Math]::Min($i, 100)
    $Ui.Value = $i
    [System.Windows.Forms.Application]::DoEvents()
    Start-Sleep -Milliseconds $DelayMs
  }
}

function Show-InstallError {
  param(
    [hashtable]$Text,
    [string]$Message
  )

  [System.Windows.Forms.MessageBox]::Show(
    "$($Text.ErrorMessage)`r`n`r`n$Message",
    $Text.ErrorTitle,
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Error
  ) | Out-Null
}

$options = Show-SetupForm
if (-not $options) {
  exit 0
}

$text = $SetupText[$options.Language]

if (-not (Test-Path -LiteralPath $sourceExe)) {
  Show-InstallError $text $text.MissingApp
  exit 1
}

$installDir = $options.InstallDir
$installedExe = Join-Path $installDir "Lernreich.exe"
$installedUninstaller = Join-Path $installDir "Uninstall-Lernreich.ps1"
$installMarker = Join-Path $installDir ".lernreich-install.json"
$startMenuFolder = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Lernreich"
$desktopShortcut = Join-Path ([Environment]::GetFolderPath("DesktopDirectory")) "Lernreich.lnk"
$powershellExe = Join-Path $env:SystemRoot "System32\WindowsPowerShell\v1.0\powershell.exe"
$registryPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\Lernreich"

$progress = New-ProgressWindow $text
$progress.Form.Show()
[System.Windows.Forms.Application]::DoEvents()

try {
  Update-SetupProgress $progress 10 $text.StepPrepare
  Get-Process -Name "Lernreich" -ErrorAction SilentlyContinue | Stop-Process -Force
  New-Item -ItemType Directory -Path $installDir -Force | Out-Null

  Update-SetupProgress $progress 35 $text.StepCopy
  Copy-Item -LiteralPath $sourceExe -Destination $installedExe -Force
  if (Test-Path -LiteralPath $sourceUninstaller) {
    Copy-Item -LiteralPath $sourceUninstaller -Destination $installedUninstaller -Force
  }

  Update-SetupProgress $progress 58 $text.StepShortcuts
  if ($options.StartMenuShortcut) {
    New-AppShortcut `
      -ShortcutPath (Join-Path $startMenuFolder "Lernreich.lnk") `
      -TargetPath $installedExe `
      -IconPath $installedExe

    if (Test-Path -LiteralPath $installedUninstaller) {
      New-AppShortcut `
        -ShortcutPath (Join-Path $startMenuFolder "Lernreich deinstallieren.lnk") `
        -TargetPath $powershellExe `
        -Arguments "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$installedUninstaller`"" `
        -Description "Lernreich deinstallieren" `
        -IconPath $installedExe
    }
  } elseif (Test-Path -LiteralPath $startMenuFolder) {
    Remove-Item -LiteralPath $startMenuFolder -Recurse -Force
  }

  if ($options.DesktopShortcut) {
    New-AppShortcut -ShortcutPath $desktopShortcut -TargetPath $installedExe -IconPath $installedExe
  } else {
    Remove-Item -LiteralPath $desktopShortcut -Force -ErrorAction SilentlyContinue
  }

  Update-SetupProgress $progress 78 $text.StepRegistry
  $estimatedSizeKb = [Math]::Ceiling((Get-Item -LiteralPath $installedExe).Length / 1KB)
  $uninstallCommand = "`"$powershellExe`" -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$installedUninstaller`""

  New-Item -Path $registryPath -Force | Out-Null
  New-ItemProperty -Path $registryPath -Name "DisplayName" -Value $appName -PropertyType String -Force | Out-Null
  New-ItemProperty -Path $registryPath -Name "DisplayVersion" -Value $version -PropertyType String -Force | Out-Null
  New-ItemProperty -Path $registryPath -Name "Publisher" -Value $publisher -PropertyType String -Force | Out-Null
  New-ItemProperty -Path $registryPath -Name "InstallLocation" -Value $installDir -PropertyType String -Force | Out-Null
  New-ItemProperty -Path $registryPath -Name "DisplayIcon" -Value "$installedExe,0" -PropertyType String -Force | Out-Null
  New-ItemProperty -Path $registryPath -Name "UninstallString" -Value $uninstallCommand -PropertyType String -Force | Out-Null
  New-ItemProperty -Path $registryPath -Name "QuietUninstallString" -Value $uninstallCommand -PropertyType String -Force | Out-Null
  New-ItemProperty -Path $registryPath -Name "EstimatedSize" -Value $estimatedSizeKb -PropertyType DWord -Force | Out-Null
  New-ItemProperty -Path $registryPath -Name "NoModify" -Value 1 -PropertyType DWord -Force | Out-Null
  New-ItemProperty -Path $registryPath -Name "NoRepair" -Value 1 -PropertyType DWord -Force | Out-Null
  New-ItemProperty -Path $registryPath -Name "InstallLanguage" -Value $options.Language -PropertyType String -Force | Out-Null

  Update-SetupProgress $progress 92 $text.StepFinish
  $installInfo = [ordered]@{
    appName = $appName
    publisher = $publisher
    version = $version
    installDir = $installDir
    language = $options.Language
    desktopShortcut = [bool]$options.DesktopShortcut
    startMenuShortcut = [bool]$options.StartMenuShortcut
    installedAt = (Get-Date).ToString("o")
  }
  $installInfo | ConvertTo-Json | Set-Content -LiteralPath $installMarker -Encoding UTF8
  Update-SetupProgress $progress 100 $text.StepFinish
}
catch {
  $progress.Form.Close()
  Show-InstallError $text $_.Exception.Message
  exit 1
}

$progress.Form.Close()

if ($options.LaunchAfterInstall) {
  Start-Process -FilePath $installedExe
}
