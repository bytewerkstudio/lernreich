# Lernreich

Lernreich ist ein minimalistischer, werbefreier und privater Fokus-Timer für Windows. Die Anwendung unterstützt Sie dabei, Ihre Lernzeit zu schützen, gesunde Gewohnheiten aufzubauen und Ihren Fortschritt zu verfolgen.

## PowerShell-Installation

Sie können den Windows-Installationsassistenten direkt über die PowerShell herunterladen und ausführen. Kopieren Sie dazu folgenden Befehl und führen Sie ihn aus:

```powershell
Invoke-WebRequest -Uri "https://lernreich.pro/downloads/Lernreich-Setup.exe" -OutFile "$env:TEMP\Lernreich-Setup.exe"; Start-Process "$env:TEMP\Lernreich-Setup.exe"
```

## Funktionen

* **Fokus-Sanduhr:** Einstellbare Sessions bis zu 2,5 Stunden inklusive Vorbereitungs-Checkliste.
* **XP- und Level-System:** Visualisierung des Lernfortschritts durch Erfahrungspunkte (1 Stunde = 100 XP).
* **Streak-System:** Motivation durch tägliche Fokus-Serien (ab 10 Minuten Fokuszeit pro Tag).
* **Aktivitäts-Heatmap:** Übersichtliche Darstellung der Lerntage in einer Heatmap im GitHub-Stil.
* **Statistiken:** Auswertung von Gesamtstunden, absolvierten Einheiten und wöchentlichen Berichten.
* **Lernjournal:** Lokales Speichern von Sitzungsnotizen als saubere Markdown-Dateien.
* **Wiederholungen:** Integrierte Planung von Wiederholungen nach dem Prinzip der Spaced Repetition.
* **Datenschutz:** 100% Offline-Betrieb. Keine Registrierung, keine Cloud-Anbindung, alle Daten verbleiben lokal.

## Systemvoraussetzungen

* **Betriebssystem:** Windows 10 / Windows 11 (64-Bit)
* **Speicherplatz:** ca. 50 MB

## Entwicklung und Build

Um den Setup-Installer lokal neu zu erstellen, führen Sie folgendes Skript aus:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\installer\build-installer.ps1
```

---

Entwickelt von [Bytewerk Studio](https://github.com/bytewerkstudio).
