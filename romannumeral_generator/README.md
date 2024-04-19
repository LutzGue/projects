**Vorbemerkung**
- Dieser Code generiert eine Serie von Zeichenketten basierend auf den vorgegebenen Parametern. Es verwendet eine rekursive Lösung, um alle möglichen Kombinationen zu erzeugen, die den gegebenen Einschränkungen entsprechen.
- Verwendung eine rekursive Lösung wegen nested Klammern und auffüllen der "Lücken" mit Klammern.
- Es werden zunächst alle Kombinationsmöglichkeiten erstellt unbeachtet der Regeln.
- Am Ende werden die Regeln angewendet und aus dem Datensatz herausgefiltert.

**Projektbeschreibung: Harmonisierung von Notenreihen mit römischen Zahlen und variabler Klammer-Hierarchie**

**Hintergrund:**
In diesem Projekt geht es darum, eine Methode zur Harmonisierung von Notenreihen zu entwickeln. Die Noten sind durch römische Zahlen repräsentiert, und wir möchten verschiedene Kombinationen erstellen, die bestimmte Regeln für die Verwendung von Klammern berücksichtigen.

**Projektziele:**
1. Erstellung von n Kombinationen aus römischen Zahlen (x).
2. Berücksichtigung der maximalen Anzahl der Elemente innerhalb einer Klammer (e_limit),  Klammer-Hierarchie (h) für "nested" Klammern, und des maximalen Hierarchie-Limits für ("nested") Klammern (h_limit).
3. Kombination der erstellten Listen zu einem Gesamtergebnis.

**Vorgehensweise:**

1. **Erstellung der Kombinationen (h = 0):**
   - Wir generieren n Kombinationen von x, ohne Klammern zu verwenden.
   - In den folgenden Beispielen sei x = {"T","S","D"} und n = 4.
   - Beispiel: x1 = {1:(T;T;T;T); 2:(T;T;T;S); ...; x:(D;D;D;D)}

2. **Einfache Klammern (h = 1):**
   - Wir verwenden einfache Klammern, um die Kombinationen zu strukturieren.
   - Beispiel für x1-Element 1:(T;T;T;T):
     - Die Bildung der Klammern erfolgt nach dem Prinzip, dass in einer Schleife, ausgehend vom vorletzte Element bis zum ersten Element, die einzelnen Elemente in eine Klammer geschrieben werden. Wichtig ist hierbei, dass das letzte Element nicht in einer Klammer geschrieben wird.
     - x2 = {1:"TT(T)T"; 2:"T(T)TT"; 3:"(T)TTT"}
	 - Anschließend wird versucht 2 Elemente in einer Klammer nach der oben beschriebenen Logik einzufügen. Auch hierbei bleibt das letzte Element unverändert ohne Klammern:
	   - x2 = {4:"T(TT)T"; 5:"(TT)TT"}
	 - Dieses wird so lange wiederholt, bis alle Möglichkeiten für die Klammerbildung ausgeschöpft sind. In unserem Beispiel können 3 Elemente in einer Klammer zusammengefasst werden (Begrenzung vorgegeben durch e_limit).
	   - x2 = {6:"(TTT)T"}
	- Diese Vorgänge werden für alle x1 in einer Schleife durchgeführt.
	- Anschließend werden in den generierten x2 Listen nach Möglichkeiten gesucht, um weitere Klammern hinzuzufügen. Für x2 ergibt sich hierbei für 1:"TT(T)T" folgende Möglichkeit:
	   - x2 = {7:"(T)T(T)T"}
	 
3. **Kombination der Listen:**
   - Wir kombinieren die Listen x1 und x2 zu einem Gesamtergebnis.

4. **Weitere Klammern (h = 2):**
   - Sofern die Bedingung h_limit erfüllt ist, fügen Wir eine zusätzliche Ebene von Klammern hinzu.
   - Beispiel für x2-Element 6:"(TTT)T":
     - Bei der Bildung der Klammern finden alle in Punkt 2 beschriebenen Regeln Anwendung und werden für alle Elemente durchlaufen:
       - x3 = {1:"(T(T)T)T"; 2:"((TT)T)T"; 3:"((T)TT)T"; ...}

	- Anschließend werden in den generierten Kombinationen, welche bereits Klammern enthalten, nach Möglichkeiten gesucht zusätzliche Klammern hinzuzufügen. Es werden sozusagen "Lücken" gesucht, indenen weitere Klammern hinzugefügt werden können. Dabei dürfen keine Kombinationen generiert werden, die gegen die Regel verstoßen, dass neben der neu erzeugten geschlossenen Klammer immer ein Element ohne Klammer bestehen muss.
    Es ergibt sich hierbei z.B. für "TT(T)T" die Möglichkeit eine weitere Klammer einzubauen:
		 - Korrektes Ergebnis ist: {"(T)T(T)T"}
         - Unerwünschte generierte Kombinationen (aufgrund von Verletzung der o.g. Regel): {"(TT)(T)T"} oder {"(T)T(T)(T)"} oder {"(T)(T)(T)(T)"} oder {"(TTTT)"} oder {"T(TTT)"}
         
5. **Weitere Kombinationen:**
   - Wir kombinieren die Listen x3 und das bisherige Ergebnis.

6. **Fortsetzung (h > 2):**
   - Sofern die Bedingung h_limit erfüllt ist, können wir weitere Hierarchieebenen hinzufügen.
   - Bei der Bildung der Klammern finden alle in Punkt 2 beschriebenen Regeln Anwendung und werden für alle Elemente durchlaufen:
   - Das Ergebnis wird in das Gesamtergebnis kombiniert.

**Ergebnis:**
Das kombinierte Ergebnis enthält alle möglichen Kombinationen von römischen Zahlen mit den entsprechenden Klammern.

**Teil 2:**
Die Konvertierung von Parsing-Bäumen in semikolongetrennte Elemente mit Bezug zum rechten Element neben der runden Klammer unter Verwendung des |-Zeichens.

In jedem Fall wird das Element in der runden Klammer durch das Element rechts von der runden Klammer geteilt und dann durch Semikolons von den anderen Elementen getrennt. 
Zu Beachten ist hierbei, dass der Text innerhalb der eckigen Klammern größer gleich 1 Zeichen lang sein kann. Die eckigen Klammern werden im Ergebnis mit der Semikolung Trennung nicht mehr benötigt und werden entfernt.

Das Programm sollte in der Lage sein, auch komplexere und verschachtelte Eingaben zu verarbeiten, wie im Beispiel gezeigt. 
Es sollte auch in der Lage sein, Elemente zu verarbeiten, die mehr als ein Zeichen enthalten. 

**Anforderung:**
1. Das Programm sollte in der Lage sein, eine Zeichenkette zu verarbeiten, die Parsing-Bäume repräsentiert. Jedes Element im Baum ist durch eckige Klammern `[]` gekennzeichnet und kann ein oder mehrere Zeichen enthalten.
2. Das Programm sollte in der Lage sein, verschachtelte Strukturen zu verarbeiten, die durch runde Klammern `()` dargestellt werden.
3. Für jedes Element in den runden Klammern, das Programm sollte es durch das Element rechts von der runden Klammer teilen, unter Verwendung des `|`-Zeichens.
4. Das Programm sollte in der Lage sein, alle Elemente in semikolongetrennte Elemente zu konvertieren.
5. Die eckigen Klammern werden im Ergebnis nicht mehr benötigt und sollten entfernt werden.

**Beispiele:**
Eingabe: `([Tp])[S][S][D][S]` Ausgabe: `Tp|S;S;D;S`
Eingabe: `([T][S])[T][T][Sp]` Ausgabe: `T|T;S|T;T;T;Sp`
Eingabe: `(([S])[T][S][S])[S]` Ausgabe: `S|T|S;T|S;S|S;S|S;S`
Eingabe: `[T](([T][T])[S])[T]` Ausgabe: `T;T|S|T;T|S|T;S|T;T`
Eingabe: `[T][T][D][D][D]` Ausgabe: `T;T;D;D;D`
Eingabe: `([T]([D])[D7])[S][D]` Ausgabe: `T|S;D|D|S;D7|S;S;D`

**Parsetree syntax:**
Python-Code, der die letzten Elemente (gekennzeichnet mit Fragezeichen Symbol) mit ihren entsprechenden Pfaden aus einem ParseTree auflistet. Der Code geht davon aus, dass der ParseTree als verschachtelte Liste repräsentiert wird.

Dieser Code durchläuft rekursiv den ParseTree und fügt den Pfad jedes Elements, das mit einem Fragezeichen endet, zu den Ergebnissen hinzu. Die Ausgabe ist eine Liste von Pfaden zu den letzten Elementen im ParseTree. 

Python-Code, der die Pfade zu den letzten Elementen (gekennzeichnet mit Fragezeichen Symbol) in umgekehrter Reihenfolge auflistet.

Dieser Code durchläuft rekursiv den ParseTree und fügt den Pfad jedes Elements, das mit einem Fragezeichen endet, zu den Ergebnissen hinzu. Die Ausgabe ist eine Liste von Pfaden zu den letzten Elementen im ParseTree in umgekehrter Reihenfolge.

Eingabe: 
`(D)DT` 
--> `([D])[D][T]` 
Ausgabe:  
`["C"_"major"["D"["D" "?"]"?"]["T" "?"]]` 
--> `["C"_"major"["D"["D" "D"]"G"]["T" "C"]]`
--> `["C"_"major"["V"["V" "D"]"G"]["I" "C"]]`

Eingabe:
["C"_"major"["D"["D"["S"["N" "?"]"?"]"?"]"?"]["T""?"]["Tp"["S"["D""?"]["Tg""?"]"?"]"?"]["T""?"]]

parse_tree = '["C_major", ["D", ["D", ["S", ["N", "?"], "?"], "?"], "?"], ["T", "?"], ["Tp", ["S", ["D", "?"], ["Tg", "?"], "?"], "?"], ["T", "?"]]'

Ausgabe:
1. N|S|D|D|C_major
2. S|D|D|C_major
3. D|D|C_major
4. D|C_major
5. T|C_major
6. D|S|Tp|C_major
7. Tg|S|Tp|C_major
8. S|Tp|C_major
9. Tp|C_major
10. T|C_major

[
    'N|S|D|D|C_major', 
    'S|D|D|C_major', 
    'D|D|C_major', 
    'D|C_major', 
    'T|C_major', 
    'D|S|Tp|C_major', 
    'Tg|S|Tp|C_major', 
    'S|Tp|C_major', 
    'Tp|C_major', 
    'T|C_major'
]
**ParseTree Random Generator**
- die im vorgegebene string `start` enthaltenen werte `<e>` sollen mit mit dem string aus `extend ` ersetzt werden. dieser schritt wird mehrfach wiederholt.
- die anzahl der maximalen durchläufe für das ersetzten ist begrenzt und wird vorgegeben mit n.
- sobald das limit aus `n` erreicht wurde wird der ersetztungsprozess gestoppt und die verbleibendenden werte `<e>` anschließend mit leerem string ersetzt.

Beispiel:
n = 10
start start = '["C"_"major"<e>]'
start = '["C"_"major"<e>]'
extend ='["T"<e>"?"]<e>'

Beispielergebnisse:

horizontale_erweiterung = '["C"_"major"["D""?"]["T""?"]]'
vertikale_erweiterung = '["C"_"major"["D"["T""?"]"?"]]'

Zufalls-Generierte ParseTrees:
["C"_"major"["I"["ii"["V""?"]["ii"["iii""?"]"?"]"?"]"?"]]