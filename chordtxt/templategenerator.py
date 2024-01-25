"""
Projektbeschreibung: Automatisierte Vervielfältigung von Templates

**Projektziel:**
Das Ziel dieses Projekts ist es, ein Python-Skript zu entwickeln, das ein gegebenes Template aus einer Datei (`template.txt`) liest und automatisch eine vordefinierte Anzahl von Kopien erstellt. Jede Kopie wird dabei im Zielpfad abgelegt und fortlaufend nummeriert.

**Funktionalitäten:**
1. **Template-Lesevorgang:**
   - Das Skript öffnet die angegebene Template-Datei (`template.txt`) und liest deren Inhalt.

2. **Vervielfältigung und Nummerierung:**
   - Für jede gewünschte Kopie wird eine neue Datei im Zielpfad erstellt.
   - Die Dateien werden mit fortlaufenden Nummern (beginnend bei 0001) benannt und mit dem Inhalt des Templates gefüllt.

3. **Formatierung der Nummern:**
   - Die Nummern der erstellten Dateien werden so formatiert, dass sie stets eine feste Anzahl von Stellen aufweisen. In diesem Fall werden führende Nullen hinzugefügt, um eine vierstellige Nummer zu gewährleisten.

**Verwendung:**
1. Der Benutzer legt das zu verwendende Template (`template.txt`) im gleichen Verzeichnis wie das Python-Skript ab.
2. Der Benutzer gibt den Pfad des Zielpfads an, in dem die Kopien erstellt werden sollen.
3. Der Benutzer legt fest, wie viele Kopien des Templates erstellt werden sollen.

**Beispiel:**
Angenommen, der Benutzer möchte 5 Kopien des Templates erstellen. Das Skript erstellt dann die Dateien `0001.txt`, `0002.txt`, ..., `0005.txt` im angegebenen Zielpfad.

**Vorteile:**
- Automatisierung von wiederholten Aufgaben bei der Erstellung von Kopien aus einem Template.
- Fortlaufende Nummerierung erleichtert die Identifizierung und Organisation der erstellten Dateien.

**Anpassbarkeit:**
Das Skript ist anpassbar und ermöglicht es dem Benutzer, verschiedene Templates zu verwenden und die Anzahl der zu erstellenden Kopien zu variieren.

**Zukünftige Erweiterungen:**
- Hinzufügen von Optionen für benutzerdefinierte Dateinamen oder Erweiterungen.
- Implementierung einer grafischen Benutzeroberfläche (GUI) für eine benutzerfreundlichere Interaktion.

**Fazit:**
Dieses Projekt bietet eine effiziente Lösung für die automatisierte Vervielfältigung von Templates, was besonders nützlich ist, wenn wiederholte Aufgaben in der Dateierstellung erforderlich sind.
"""

#import shutil
import os

def kopiere_template(template_dateipfad, zielordner, anzahl_kopien):
    with open(template_dateipfad, 'r') as template_datei:
        template_inhalt = template_datei.read()

    for nummer in range(1, anzahl_kopien + 1):
        nummer_formatiert = str(nummer).zfill(4)  # Fügt führende Nullen hinzu, um die Nummer zu formatieren
        zieldatei_pfad = f"{zielordner}/{nummer_formatiert}.txt"

        with open(zieldatei_pfad, 'w') as zieldatei:
            zieldatei.write(template_inhalt)

if __name__ == "__main__":

    template_name = "template.txt"

    script_verzeichnis = os.path.dirname(os.path.realpath(__file__))
    template_pfad = os.path.join(script_verzeichnis, "txt", template_name)
    print("template:",template_pfad)

    script_verzeichnis = os.path.dirname(os.path.realpath(__file__))
    
    #ziel_ordner = os.path.join(script_verzeichnis, "txt", "02_chord_progressions_for_songwriters","01_ascending_basslines")
    ziel_ordner = os.path.join(script_verzeichnis, "txt", "03_reharmonization_techniques","10_basic_piano_voicing_techniques")
    
    print("target:",ziel_ordner)

    anzahl_kopien = 21  # Anzahl der gewünschten Kopien
    print("copies:",anzahl_kopien)

    kopiere_template(template_pfad, ziel_ordner, anzahl_kopien)
