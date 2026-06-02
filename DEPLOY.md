# Lernreich-Website – Veröffentlichen mit Netlify + Strato-Domain

Statische Website (HTML/CSS/JS), kein Build nötig. Ordner: `E:\Projekt\website`

Öffentlicher Anbieter-/Studio-Name: **Bytewerk Studio**. Inhaber: Hijratullah Haqmal.

## Schritt 1 – Vorher ausfüllen
- `impressum.html` → echte Daten eintragen (in DE Pflicht!)
- `datenschutz.html` → Kontaktdaten ergänzen
- `index.html` → Zeile mit `og:url` auf deine echte Domain setzen

## Schritt 2 – Auf Netlify hochladen (einfachste Variante: Drag & Drop)
1. Auf https://app.netlify.com einloggen (kostenloses Konto).
2. Reiter **„Sites"** → unten den Bereich **„Drag and drop your site folder here"**.
3. Den **Inhalt** des Ordners `website` (oder den Ordner selbst) dort hineinziehen.
4. Netlify gibt dir sofort eine Test-URL wie `https://zufallsname.netlify.app`.

> Tipp: Unter **Site configuration → Change site name** kannst du den Subdomain-Namen anpassen.

## Schritt 3 – Deine Strato-Domain verbinden
1. In Netlify: **Domain management → Add a domain** → deine Domain eingeben (z. B. `lernreich.de`).
2. Netlify zeigt dir an, welche DNS-Einträge nötig sind. Standard:
   - **A-Record** für die Haupt-Domain (`@`) → IP **`75.2.60.5`**
   - **CNAME** für `www` → `DEIN-SITENAME.netlify.app`
3. Diese Einträge bei **Strato** setzen:
   - Strato-Login → **Domainverwaltung** → deine Domain → **DNS-Einstellungen / Nameserver-Einstellungen** verwalten.
   - A-Record `@` auf `75.2.60.5` setzen.
   - CNAME `www` auf `DEIN-SITENAME.netlify.app` setzen.
   - Vorhandene widersprüchliche Einträge (alte A-Records) entfernen.
4. Zurück in Netlify auf **Verify / Check DNS** klicken. Die Umstellung kann **bis zu 24–48 h** dauern (meist schneller).
5. **HTTPS:** Netlify stellt automatisch ein kostenloses SSL-Zertifikat (Let's Encrypt) aus, sobald die DNS-Einträge greifen. Danach „Force HTTPS" aktivieren.

> Aktuelle Netlify-IP bitte im Netlify-Dialog gegenprüfen – sie kann sich ändern.

## Alternative – über GitHub (für automatische Updates)
Wenn die Website später in einem GitHub-Repo liegt: in Netlify **„Add new site → Import from Git"**,
Repo auswählen, **Publish directory = `website`** setzen. Jeder Push aktualisiert die Seite automatisch.

## Hinweis zum Download
Der Hauptdownload ist `downloads/Lernreich-Setup.exe` (~20 MB, Version 1.2). Dieser Setup-Assistent
fragt Sprache, Installationsordner, Desktop-Verknüpfung, Startmenü-Verknüpfung und „nach der
Installation starten" ab. Danach kopiert er Lernreich in den gewählten Ordner, registriert die
Deinstallation in Windows. Nach Abschluss wird kein zusätzliches Erfolgsfenster angezeigt.
Bei der Deinstallation werden Programmdateien und Verknüpfungen entfernt; Lernfortschritt und
Statistikdaten in `AppData\Roaming\Lernreich` werden erst nach Rückfrage gelöscht.

Öffentlich im Download-Ordner liegt nur der Setup-Installer. Die private App-Datei für den Build
liegt außerhalb der Website unter `uploads\private-build\Lernreich.exe` und wird beim Erstellen des
Setups in `Lernreich-Setup.exe` eingebettet.

Wenn `uploads\private-build\Lernreich.exe` aktualisiert wurde, den Installer danach neu bauen:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\installer\build-installer.ps1
```

Alternativ kannst du den Setup-Installer später über **GitHub-Releases** anbieten und in
`index.html` den Download-Link (`downloads/Lernreich-Setup.exe`) entsprechend ändern.

## Download-Zähler
Der Download-Button sendet bei jedem Klick einen Eintrag an das Netlify-Formular
`download-stat`. Netlify erkennt das Formular über die technische Seite
`download-stat.html`. Nach dem Deploy findest du die Zählung in Netlify unter:

**Site → Forms → download-stat**

Wenn dort noch nichts erscheint: Die komplette, aktualisierte Website erneut deployen
und danach einmal selbst auf den Download-Button klicken. Erst dann taucht der erste
Eintrag sicher im Formularbereich auf.

Das zählt Download-Klicks auf `Lernreich-Setup.exe`. Abgebrochene Downloads oder Rechtsklicks
werden nicht zuverlässig als abgeschlossene Downloads erkannt.

Zusätzlich werden beim Klick ungefähre IP-Standortdaten über `https://api.ipquery.io/?format=json`
abgefragt und als Formularfelder gespeichert: Land, Ländercode, Region, Stadt und Zeitzone.
Außerdem werden Browser-Sprache und Bildschirmgröße gespeichert. Die Standortdaten sind nicht
GPS-genau und können je nach Internetanbieter abweichen.

> Wichtig: Ein **selbst-signiertes** Zertifikat entfernt die Windows-SmartScreen-Warnung nur auf
> PCs, auf denen das Zertifikat installiert wurde. Für einen warnungsfreien Download durch alle
> Besucher ist ein **gekauftes** Code-Signing-Zertifikat (Sectigo/DigiCert) nötig.
