# ⏳ Lernreich – Schütze deine Lernzeit, sieh deinen Fortschritt

**Lernreich** ist ein minimalistischer, werbefreier und 100% privater Fokus-Timer für Windows. Die App hilft dir, deine Lernzeit zu schützen, gesunde Lerngewohnheiten aufzubauen und deinen Lernfortschritt spielerisch zu verfolgen.

---

## ⚡ Schnellinstallation über PowerShell

Du kannst die Windows-Installationsdatei direkt über deine PowerShell herunterladen und ausführen. Kopiere einfach den folgenden Befehl, füge ihn in deine PowerShell ein und drücke **Enter**:

```powershell
Invoke-WebRequest -Uri "https://lernreich.pro/downloads/Lernreich-Setup.exe" -OutFile "$env:TEMP\Lernreich-Setup.exe"; Start-Process "$env:TEMP\Lernreich-Setup.exe"
```

*Dieser Befehl lädt die Installationsdatei sicher in dein temporäres Verzeichnis herunter und startet sofort den Windows-Installationsassistenten.*

---

## ✨ Die wichtigsten Funktionen im Überblick

Lernreich bietet dir alles, was du für konzentriertes Arbeiten brauchst, ohne dich durch unnötigen Schnickschnack abzulenken:

*   **⏳ Fokus-Sanduhr**
    Stelle eine Fokus-Sanduhr auf bis zu 2,5 Stunden ein. Eine interaktive Checkliste vor dem Start hilft dir, dich optimal vorzubereiten (z.B. Smartphone wegzulegen) und Ablenkungen zu eliminieren.
*   **🎮 XP & Level-System**
    Sammle XP für deine konzentrierte Lernzeit (1 Stunde Lernen = 100 XP). Steige im Level auf und mache deinen Fleiß visuell spürbar.
*   **🔥 Streak-System**
    Konzentriere dich täglich für mindestens 10 Minuten, um deine Serie (Streak) aufrechtzuerhalten, und sichere dir zusätzliche Streak-Bonus-XP.
*   **📅 Aktivitäts-Heatmap**
    Deine Lerntage werden in einer wunderschönen Aktivitäts-Heatmap im cleanen GitHub-Stil visualisiert. So erkennst du deine Lernmuster auf einen Blick.
*   **📊 Statistiken & Wochenberichte**
    Behalte deine Gesamtstunden, deine absolvierten Fokus-Sessions und deine Streaks im Auge. Ein kompakter Wochenbericht zeigt dir zudem dein am häufigsten gelerntes Fach.
*   **📝 Lernjournal & Notizen**
    Halte fest, was du in einer Session gelernt hast. Notizen werden lokal als saubere Markdown-Dateien auf deiner Festplatte gespeichert.
*   **🔄 Spaced Repetition (Wiederholungen)**
    Vergiss das Gelernte nicht: Plane strukturierte Wiederholungen für morgen, in 3 oder in 7 Tagen direkt in der App.
*   **🛡️ 100% Offline & Datenschutzfreundlich**
    Kein Cloud-Zwang, keine Registrierung und keine Werbung. Alle deine Daten verbleiben ausschließlich lokal auf deinem eigenen PC.

---

## 💻 Systemvoraussetzungen

*   **Betriebssystem:** Windows 10 oder Windows 11 (64-Bit)
*   **Speicherplatz:** ca. 50 MB freier Speicherplatz

---

## 🛠️ Entwicklung & Build des Installers

Falls du den Installer selbst lokal kompilieren und erstellen möchtest, kannst du das im Repository enthaltene PowerShell-Skript nutzen:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\installer\build-installer.ps1
```

*Hinweis: Der signierte Setup-Assistent wird im Ordner `downloads/Lernreich-Setup.exe` ausgegeben.*

---

*Entwickelt von [Bytewerk Studio](https://github.com/bytewerkstudio).*
