[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[System.Windows.Forms.Application]::EnableVisualStyles()

$appName = "Lernreich"
$publisher = "Bytewerk Studio"
$version = "1.3.0"
$sourceExe = Join-Path $PSScriptRoot "Lernreich.exe"
$sourceUninstaller = Join-Path $PSScriptRoot "Uninstall-Lernreich.ps1"
$sourceLogo = Join-Path $PSScriptRoot "logo.png"
$defaultInstallDir = Join-Path $env:LOCALAPPDATA "Programs\Lernreich"

$SetupText = @{
  de = @{
    WindowTitle = "Lernreich Setup"
    HeaderTitle = "Lernreich installieren"
    HeaderSubtitle = "Einmal einrichten, danach bequem aus dem Startmen$([char]252) oder vom Desktop starten."
    Language = "Sprache"
    Username = "Benutzername"
    Folder = "Installationsordner"
    FolderHint = "Wenn du einen Hauptordner w$([char]228)hlst, wird darin automatisch ein Unterordner 'Lernreich' erstellt."
    Browse = "Ausw$([char]228)hlen"
    Options = "Optionen"
    DesktopShortcut = "Desktop-Verkn$([char]252)pfung erstellen"
    StartMenuShortcut = "Startmen$([char]252)-Verkn$([char]252)pfung erstellen"
    LaunchAfterInstall = "Nach der Installation starten"
    Install = "Installieren"
    Cancel = "Abbrechen"
    BrowseDialog = "Installationsordner ausw$([char]228)hlen"
    InvalidFolder = "Bitte w$([char]228)hle einen g$([char]252)ltigen Installationsordner."
    MissingApp = "Lernreich.exe wurde im Setup-Paket nicht gefunden."
    ProgressTitle = "Installation l$([char]228)uft"
    ProgressSubtitle = "Lernreich wird eingerichtet."
    StepPrepare = "Installation wird vorbereitet..."
    StepCopy = "Programmdateien werden kopiert..."
    StepShortcuts = "Verkn$([char]252)pfungen werden erstellt..."
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
    Username = "Username"
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
  $form.ClientSize = New-Object System.Drawing.Size(560, 410)
  $form.BackColor = Get-Color "#ffffff"
  $form.Font = Get-UiFont 9

  if (Test-Path -LiteralPath $sourceExe) {
    try { $form.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($sourceExe) } catch {}
  }

  if (Test-Path -LiteralPath $sourceLogo) {
    try {
      $logo = New-Object System.Windows.Forms.PictureBox
      $logo.Location = New-Object System.Drawing.Point(30, 20)
      $logo.Size = New-Object System.Drawing.Size(44, 44)
      $logo.SizeMode = "Zoom"
      $logo.Image = [System.Drawing.Image]::FromFile($sourceLogo)
      $form.Controls.Add($logo)
    } catch {}
  }

  $titleLabel = New-Object System.Windows.Forms.Label
  $titleLabel.Location = New-Object System.Drawing.Point(90, 18)
  $titleLabel.Size = New-Object System.Drawing.Size(440, 28)
  $titleLabel.ForeColor = Get-Color "#111215"
  $titleLabel.BackColor = [System.Drawing.Color]::White
  $titleLabel.Font = Get-UiFont 14 ([System.Drawing.FontStyle]::Bold)
  $form.Controls.Add($titleLabel)

  $subtitleLabel = New-Object System.Windows.Forms.Label
  $subtitleLabel.Location = New-Object System.Drawing.Point(90, 46)
  $subtitleLabel.Size = New-Object System.Drawing.Size(440, 36)
  $subtitleLabel.ForeColor = Get-Color "#71747c"
  $subtitleLabel.BackColor = [System.Drawing.Color]::White
  $subtitleLabel.Font = Get-UiFont 9
  $form.Controls.Add($subtitleLabel)

  $topDivider = New-Object System.Windows.Forms.Panel
  $topDivider.Location = New-Object System.Drawing.Point(0, 84)
  $topDivider.Size = New-Object System.Drawing.Size(560, 1)
  $topDivider.BackColor = Get-Color "#e6e6e2"
  $form.Controls.Add($topDivider)

  $languageLabel = New-Object System.Windows.Forms.Label
  $languageLabel.Location = New-Object System.Drawing.Point(30, 105)
  $languageLabel.Size = New-Object System.Drawing.Size(180, 20)
  $languageLabel.Font = Get-UiFont 9 ([System.Drawing.FontStyle]::Bold)
  $languageLabel.BackColor = [System.Drawing.Color]::White
  $languageLabel.ForeColor = Get-Color "#111215"
  $form.Controls.Add($languageLabel)

  $languageCombo = New-Object System.Windows.Forms.ComboBox
  $languageCombo.Location = New-Object System.Drawing.Point(30, 128)
  $languageCombo.Size = New-Object System.Drawing.Size(180, 24)
  $languageCombo.DropDownStyle = "DropDownList"
  $languageCombo.FlatStyle = "Flat"
  [void]$languageCombo.Items.Add("Deutsch")
  [void]$languageCombo.Items.Add("English")
  $languageCombo.SelectedIndex = 0
  $form.Controls.Add($languageCombo)

  $usernameLabel = New-Object System.Windows.Forms.Label
  $usernameLabel.Location = New-Object System.Drawing.Point(280, 105)
  $usernameLabel.Size = New-Object System.Drawing.Size(250, 20)
  $usernameLabel.Font = Get-UiFont 9 ([System.Drawing.FontStyle]::Bold)
  $usernameLabel.BackColor = [System.Drawing.Color]::White
  $usernameLabel.ForeColor = Get-Color "#111215"
  $form.Controls.Add($usernameLabel)

  $usernameBox = New-Object System.Windows.Forms.TextBox
  $usernameBox.Location = New-Object System.Drawing.Point(280, 128)
  $usernameBox.Size = New-Object System.Drawing.Size(250, 24)
  $usernameBox.BorderStyle = [System.Windows.Forms.BorderStyle]::FixedSingle
  $usernameBox.BackColor = Get-Color "#ffffff"
  $usernameBox.ForeColor = Get-Color "#111215"
  
  $defaultUser = "Hijrat"
  if ($env:USERNAME) {
    try {
      $rawUser = $env:USERNAME.Trim()
      if ($rawUser) {
        $defaultUser = (Get-Culture).TextInfo.ToTitleCase($rawUser.ToLower())
      }
    } catch {
      $defaultUser = "Hijrat"
    }
  }
  $usernameBox.Text = $defaultUser
  $form.Controls.Add($usernameBox)

  $folderLabel = New-Object System.Windows.Forms.Label
  $folderLabel.Location = New-Object System.Drawing.Point(30, 172)
  $folderLabel.Size = New-Object System.Drawing.Size(220, 20)
  $folderLabel.Font = Get-UiFont 9 ([System.Drawing.FontStyle]::Bold)
  $folderLabel.BackColor = [System.Drawing.Color]::White
  $folderLabel.ForeColor = Get-Color "#111215"
  $form.Controls.Add($folderLabel)

  $folderBox = New-Object System.Windows.Forms.TextBox
  $folderBox.Location = New-Object System.Drawing.Point(30, 195)
  $folderBox.Size = New-Object System.Drawing.Size(360, 24)
  $folderBox.Text = $defaultInstallDir
  $folderBox.BorderStyle = [System.Windows.Forms.BorderStyle]::FixedSingle
  $folderBox.BackColor = Get-Color "#ffffff"
  $folderBox.ForeColor = Get-Color "#111215"
  $form.Controls.Add($folderBox)

  $browseButton = New-Object System.Windows.Forms.Button
  $browseButton.Location = New-Object System.Drawing.Point(404, 192)
  $browseButton.Size = New-Object System.Drawing.Size(126, 28)
  $browseButton.FlatStyle = "Flat"
  $browseButton.FlatAppearance.BorderSize = 0
  $browseButton.BackColor = Get-Color "#f1f1ed"
  $browseButton.ForeColor = Get-Color "#111215"
  $browseButton.Font = Get-UiFont 8.5 ([System.Drawing.FontStyle]::Bold)
  $browseButton.Cursor = [System.Windows.Forms.Cursors]::Hand
  $form.Controls.Add($browseButton)

  $folderHintLabel = New-Object System.Windows.Forms.Label
  $folderHintLabel.Location = New-Object System.Drawing.Point(30, 226)
  $folderHintLabel.Size = New-Object System.Drawing.Size(500, 20)
  $folderHintLabel.ForeColor = Get-Color "#71747c"
  $folderHintLabel.BackColor = [System.Drawing.Color]::White
  $folderHintLabel.Font = Get-UiFont 8
  $form.Controls.Add($folderHintLabel)

  $optionsLabel = New-Object System.Windows.Forms.Label
  $optionsLabel.Location = New-Object System.Drawing.Point(30, 260)
  $optionsLabel.Size = New-Object System.Drawing.Size(180, 20)
  $optionsLabel.Font = Get-UiFont 9 ([System.Drawing.FontStyle]::Bold)
  $optionsLabel.BackColor = [System.Drawing.Color]::White
  $optionsLabel.ForeColor = Get-Color "#111215"
  $form.Controls.Add($optionsLabel)

  $desktopCheck = New-Object System.Windows.Forms.CheckBox
  $desktopCheck.Location = New-Object System.Drawing.Point(32, 283)
  $desktopCheck.Size = New-Object System.Drawing.Size(230, 24)
  $desktopCheck.Checked = $true
  $desktopCheck.Font = Get-UiFont 9
  $desktopCheck.BackColor = [System.Drawing.Color]::White
  $desktopCheck.ForeColor = Get-Color "#111215"
  $desktopCheck.Cursor = [System.Windows.Forms.Cursors]::Hand
  $form.Controls.Add($desktopCheck)

  $startMenuCheck = New-Object System.Windows.Forms.CheckBox
  $startMenuCheck.Location = New-Object System.Drawing.Point(280, 283)
  $startMenuCheck.Size = New-Object System.Drawing.Size(250, 24)
  $startMenuCheck.Checked = $true
  $startMenuCheck.Font = Get-UiFont 9
  $startMenuCheck.BackColor = [System.Drawing.Color]::White
  $startMenuCheck.ForeColor = Get-Color "#111215"
  $startMenuCheck.Cursor = [System.Windows.Forms.Cursors]::Hand
  $form.Controls.Add($startMenuCheck)

  $launchCheck = New-Object System.Windows.Forms.CheckBox
  $launchCheck.Location = New-Object System.Drawing.Point(32, 310)
  $launchCheck.Size = New-Object System.Drawing.Size(230, 24)
  $launchCheck.Checked = $true
  $launchCheck.Font = Get-UiFont 9
  $launchCheck.BackColor = [System.Drawing.Color]::White
  $launchCheck.ForeColor = Get-Color "#111215"
  $launchCheck.Cursor = [System.Windows.Forms.Cursors]::Hand
  $form.Controls.Add($launchCheck)

  $bottomDivider = New-Object System.Windows.Forms.Panel
  $bottomDivider.Location = New-Object System.Drawing.Point(0, 350)
  $bottomDivider.Size = New-Object System.Drawing.Size(560, 1)
  $bottomDivider.BackColor = Get-Color "#e6e6e2"
  $form.Controls.Add($bottomDivider)

  $installButton = New-Object System.Windows.Forms.Button
  $installButton.Location = New-Object System.Drawing.Point(394, 362)
  $installButton.Size = New-Object System.Drawing.Size(136, 32)
  $installButton.FlatStyle = "Flat"
  $installButton.FlatAppearance.BorderSize = 0
  $installButton.BackColor = Get-Color "#3b52e2"
  $installButton.ForeColor = [System.Drawing.Color]::White
  $installButton.Font = Get-UiFont 9.5 ([System.Drawing.FontStyle]::Bold)
  $installButton.Cursor = [System.Windows.Forms.Cursors]::Hand
  $form.Controls.Add($installButton)

  $cancelButton = New-Object System.Windows.Forms.Button
  $cancelButton.Location = New-Object System.Drawing.Point(260, 362)
  $cancelButton.Size = New-Object System.Drawing.Size(120, 32)
  $cancelButton.FlatStyle = "Flat"
  $cancelButton.FlatAppearance.BorderSize = 0
  $cancelButton.BackColor = Get-Color "#f1f1ed"
  $cancelButton.ForeColor = Get-Color "#111215"
  $cancelButton.Font = Get-UiFont 8.5 ([System.Drawing.FontStyle]::Bold)
  $cancelButton.Cursor = [System.Windows.Forms.Cursors]::Hand
  $form.Controls.Add($cancelButton)

  function Apply-SetupLanguage {
    param([string]$LanguageKey)
    $text = $SetupText[$LanguageKey]
    $form.Text = $text.WindowTitle
    $titleLabel.Text = $text.HeaderTitle
    $subtitleLabel.Text = $text.HeaderSubtitle
    $languageLabel.Text = $text.Language
    $usernameLabel.Text = $text.Username
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

    $finalUsername = $usernameBox.Text.Trim()
    if ([string]::IsNullOrEmpty($finalUsername)) {
      $finalUsername = "Hijrat"
    }

    $state.Result = [pscustomobject]@{
      Language = $state.Language
      InstallDir = $installDir
      Username = $finalUsername
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
  $form.BackColor = Get-Color "#ffffff"
  $form.Font = Get-UiFont 9

  if (Test-Path -LiteralPath $sourceExe) {
    try { $form.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($sourceExe) } catch {}
  }

  $title = New-Object System.Windows.Forms.Label
  $title.Location = New-Object System.Drawing.Point(36, 34)
  $title.Size = New-Object System.Drawing.Size(490, 36)
  $title.Font = Get-UiFont 17 ([System.Drawing.FontStyle]::Bold)
  $title.ForeColor = Get-Color "#3b52e2"
  $title.BackColor = [System.Drawing.Color]::White
  $title.Text = $Text.ProgressTitle
  $form.Controls.Add($title)

  $subtitle = New-Object System.Windows.Forms.Label
  $subtitle.Location = New-Object System.Drawing.Point(39, 76)
  $subtitle.Size = New-Object System.Drawing.Size(490, 28)
  $subtitle.Font = Get-UiFont 10
  $subtitle.ForeColor = Get-Color "#71747c"
  $subtitle.BackColor = [System.Drawing.Color]::White
  $subtitle.Text = $Text.ProgressSubtitle
  $form.Controls.Add($subtitle)

  $status = New-Object System.Windows.Forms.Label
  $status.Location = New-Object System.Drawing.Point(39, 126)
  $status.Size = New-Object System.Drawing.Size(490, 26)
  $status.Font = Get-UiFont 9.5
  $status.ForeColor = Get-Color "#3c3f46"
  $status.BackColor = [System.Drawing.Color]::White
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

  # Write username to progress.json safely (compatible with PowerShell 5.1 PSCustomObjects)
  $lernreichAppData = Join-Path $env:APPDATA "Lernreich"
  if (-not (Test-Path -Path $lernreichAppData)) {
    New-Item -ItemType Directory -Path $lernreichAppData -Force | Out-Null
  }
  $progressJsonPath = Join-Path $lernreichAppData "progress.json"
  $progressData = @{}
  if (Test-Path -Path $progressJsonPath) {
    try {
      $content = Get-Content -LiteralPath $progressJsonPath -Raw -ErrorAction SilentlyContinue
      if ($content) {
        $obj = ConvertFrom-Json $content
        if ($null -ne $obj) {
          foreach ($prop in $obj.PSObject.Properties) {
            $progressData[$prop.Name] = $prop.Value
          }
        }
      }
    } catch {}
  }
  $progressData["username"] = $options.Username
  if (-not $progressData.ContainsKey("total_seconds")) { $progressData["total_seconds"] = 0 }
  if (-not $progressData.ContainsKey("sessions")) { $progressData["sessions"] = @() }

  $progressData | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $progressJsonPath -Encoding UTF8

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
