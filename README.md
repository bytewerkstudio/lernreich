# Lernreich

Lernreich ist ein minimalistischer, werbefreier und privater Fokus-Timer für Windows. Die Anwendung unterstützt Sie dabei, Ihre Lernzeit zu schützen, gesunde Gewohnheiten aufzubauen und Ihren Fortschritt zu verfolgen.

## PowerShell-Installation

Sie können den Windows-Installationsassistenten direkt über die PowerShell herunterladen und ausführen. Kopieren Sie dazu folgenden Befehl und führen Sie ihn aus:

```powershell
Start-BitsTransfer -Source "https://lernreich.pro/downloads/Lernreich-Setup.exe" -Destination "$env:TEMP\Lernreich-Setup.exe"; Start-Process "$env:TEMP\Lernreich-Setup.exe"
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


## Versionshistorie

### v1.4.0 (03.06.2026)
* **Strikter Ablenkungsschutz:** Automatische Minimierung ablenkender Anwendungen und Webseiten (wie Social Media, YouTube, Netflix, Discord, Steam) während aktiver Fokus-Sessions inklusive Benachrichtigungen.

### v1.3.0 (03.06.2026)
* **Benutzername im Setup:** Festlegen des Benutzernamens direkt während des Installationsassistenten.
* **Kreisförmige Checkboxen:** iOS-Schalter in der Fokus-Vorbereitung durch animierte kreisförmige Checkboxen ersetzt.
* **Layout & Encoding-Korrekturen:** Anzeigebehebung der Timer-Sanduhr und Beseitigung von Umlaut-Encodingfehlern im Setup.

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
