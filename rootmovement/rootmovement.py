"""
This code first converts the Roman numerals to chords in the given key. Then it analyzes the chord progression to determine the intervals between the root notes of the chords. Finally, it assigns the root movement types based on the calculated intervals. Please note that this code assumes that the music21 library is installed and that the Roman numerals are provided in uppercase for major chords and lowercase for minor chords. The key is assumed to be provided as the first element of the chord progression list. The remaining elements are the Roman numerals representing the chords. The root movement types are defined in the root_movement_types dictionary and can be adjusted as needed. The code then prints the chord progression, the calculated intervals, and the assigned root movement types. Please ensure to install the music21 library by running pip install music21 in your Python environment before running this code.
"""

from music21 import *
from collections import Counter

# Definieren Sie die Zuordnung von Intervallen zu Wurzelbewegungstypen
"""
The following combinations given cover all possible intervals (and the corresponding complementary intervals) in Western music theory, for both authentic and plagal fundamental progressions. Each interval is associated with a corresponding step (main step, third step, second step) and a category (Authentic or Plagal). The direction "down" was indicated by the minus (-) sign. There is no additional sign for the move "up".
"""
root_movement_types = {
    # Authentischen Grundtonfortschreitungen (A)
        # Hauptschritt (H) -- AH down
        "P-5": "AH",    "P4": "AH",
        "d-5": "A#/bH", "A4": "A#/bH",

        # Terzschritt (T/t) -- AT down
        "m-3": "At",    "M6": "At",
        "M-3": "AT",    "m6": "AT",
        "d-3": "A#/bt", "A6": "A#/bt",

        # Sekundschritt (S/s) -- AS up
        "M2": "AS",     "m-7": "AS",
        "m2": "As",     "M-7": "As",
        "d2": "A#/bs",  "A-7": "A#/bs",

    # Plagale Grundtonfortschreitungen (P)
        # Hauptschritt (H) -- PH up
        "P5": "PH",     "P-4": "PH",
        "A5": "P#/bH",  "d-4": "P#/bH",
        
        # Terzschritt (T) -- PT up
        "M3": "PT",     "m-6": "PT",
        "m3": "Pt",     "M-6": "Pt",
        "d3": "P#/bt",  "A-6": "P#/bt",

        # Sekundschritt (S) -- PS down
        "M-2": "PS",    "m7": "PS",
        "m-2": "Ps",    "M7": "Ps",
        "A-2": "P#/bs", "d7": "P#/bs",

    # "kein-schritt" (None)
    "P1": None
}

def roman_to_chord(chord_tuple):
    key, roman_numeral = chord_tuple
    rn = roman.RomanNumeral(roman_numeral, key)
    pitches = rn.pitches
    chord_notes = ' '.join(str(pitch) for pitch in pitches)
    chord_name = chord.Chord(chord_notes).pitchedCommonName
    chord_bass_note = rn.bass().name
    root = rn.root().name
    print(f'roman2chord: {key}:{roman_numeral} --> {chord_name}/{chord_bass_note}, R: {root}')
    return root

def analyze_chord_progression(chord_progression):
    chords = [roman_to_chord(chord_tuple) for chord_tuple in chord_progression]
    intervals = []
    for i in range(len(chords) - 1):
        chord_interval = interval.Interval(noteStart=note.Note(chords[i]), noteEnd=note.Note(chords[i+1]))
        interval_direction = chord_interval.direction
        intervals.append(f"{chord_interval.directedName}")
    return intervals

def assign_root_movement_type(intervals):
    return [root_movement_types.get(interval, "Unbekannt") for interval in intervals]

def calculate_statistics(root_movement_types):
    """
    This code calculates the total number of elements, the total number of non-empty elements, the absolute frequency of authentic and plagal fundamental progressions, and the relative proportions of these two categories.

    Beispiel:
    Wurzelbewegungstypen: ['AS', 'AH', 'Ps', 'As', None, 'AH']

    Ergebnis:
    total_count = 6 # alle Elemente 
    total_count_not_empty = 5 # alle Elemente ohne "None"
    absolut: {("A":4),("P":1),("X":1)}
    quote_a = (4/5)*100 = 80% # relative quote für Authentische elemente ohne None
    quote_p = (1/5)*100 = 20% # relative quote für Plagale elemente ohne None
    Ausgabe: "80% authentische : 20% plagale Grunttonfortschreitungen"
    """
    total_count = len(root_movement_types)
    total_count_not_empty = len([x for x in root_movement_types if x is not None])
    absolut = Counter([x[0] for x in root_movement_types if x is not None])
    quote_a = (absolut.get('A', 0) / total_count_not_empty) * 100
    quote_p = (absolut.get('P', 0) / total_count_not_empty) * 100
    return total_count, total_count_not_empty, absolut, quote_a, quote_p

# Beispielverwendung
#chord_progression = [("C", "I"),("C", "vii°7/vi")]
#chord_progression = [("C", "I"),("C", "IV"),("C", "vii°6"),("C", "I"),("C", "I6"),("C", "V46"),("C", "V7"),("C", "I")]
#chord_progression = [("C", "I6"),("C", "II56"),("C", "V46"),("C", "#iv°56"),("C", "V46"),("C", "V7"),("C", "I")]
#chord_progression = [("C", "I"),("C", "V6"),("C", "#IV°43/vi"),("C", "V6/vi"),("C", "V65/vi"),("C", "vi"),("C","#IV°7"),("C","V4"),("C","V32"),("C","vii°7/IV"),("C","IV"),("C","V7"),("C","I")]
#chord_progression = [("C","vi"),("C","vi/I/iii"),("C","IV/I/iii"),("C","I/I/iii"),("C","I/iii"),("C","iii"),("C","vi"),("C","I")]
#chord_progression = [("C","II7/iii"),("C","iii"),("C","V"),("C","I")]
#chord_progression = [("C","V"),("C","ii/V/ii"),("C","vii°7/V/ii"),("C","V/ii"),("C","ii")]
#chord_progression = [('C', 'I'), ('C', 'V/iii/II7/I'), ('C', 'iii/II7/I'), ('C', 'II7/I'), ('C', 'I'), ('C', 'II7/V/iii'), ('C', 'V/iii'), ('C', 'ii/iii'), ('C', 'iii'), ('C', 'V'), ('C', 'I')]
#chord_progression = [('C', 'I'), ('C', 'iii/I'), ('C', 'iii/ii/I'), ('C', 'V/ii/I'), ('C', 'ii/I'), ('C', 'I'), ('C', 'V/ii'), ('C', 'ii'), ('C', 'V'), ('C', 'I')]
#chord_progression = [('C', 'I'), ('C', 'IV/ii/V'), ('C', 'vii°/ii/ii/V'), ('C', 'ii/ii/V'), ('C', 'ii/V'), ('C', 'V'), ('C', 'ii7'), ('C', 'V'), ('C', 'I')]
chord_progression = [('C', 'I'), ('C', 'I/vii°/#IV°7'), ('C', 'V/iii/vii°/#IV°7'), ('C', 'iii/vii°/#IV°7'), ('C', 'I/vii°/#IV°7'), ('C', 'vii°/#IV°7'), ('C', '#IV°7'), ('C', 'IV'), ('C', 'V'), ('C', 'I')]

intervals = analyze_chord_progression(chord_progression)
root_movement_types = assign_root_movement_type(intervals)

print(f"Akkordprogression: {chord_progression}")
print(f"Intervalle: {intervals}")
print(f"Grundtonfortschreitungen: {root_movement_types}")

total_count, total_count_not_empty, absolut, quote_a, quote_p = calculate_statistics(root_movement_types)

print(f"Absolut: {absolut}")
print(f"Auswertung: {round(quote_a)}% authentische, {round(quote_p)}% plagale Grundtonfortschreitungen.")
