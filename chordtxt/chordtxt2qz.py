from music21 import *
import os
import codecs
import sys

"""
---------------------------------------
Lutz Menzel
Berlin, Germany, 2023-09-13
Version 00.01
MIT Licence
---------------------------------------
PROJECT: Generate chord progressions in MIDI and MusicXML file from a given chord progression in TXT format and provide transposing batch.
---------------------------------------
My personal goal is to improve my skills in practical piano playing. For this, daily practice is important and to train a wide repertoire of established 
chord progressions that are helpful for songwriting. I believe that with the muscle memory in the fingers, the feeling of playing live is made possible 
and thus a creative environment is created to create new songs. I personally like to practice piano on my Midi-Keyboard using the App ST. For that purpose 
i've started collecting and creating Midi files to open them in ST. But the adaptation of templates from books and various video tutorials and the preparation in MIDI editors 
is very time-consuming and i became unmotivated. First, I needed the simplest editor in which I could quickly capture the templates in a machine-readable format and decided on Notepad 
in TXT format. In addition, I want to be flexible for modulation and train all transcribed examples in all keys in the circle of fifths upwards, downwards 
and chromatically upwards and downwards. For transposing to other keys, a batch job is suitable, which I present in this Python script for parsing and analyzing 
chord progressions in songs. The code provides several data structures for musical notes and chords, and includes functions for parsing a song file and analyzing 
the chords within it. The parse_file function reads a song file and extracts metadata (like the author, title, key, etc.) as well as the sequence of chords in the song.
The get_note_number and get_note_name functions convert between note names (like 'C', 'D#', etc.) and their corresponding numerical values.
The get_pitches function calculates the pitches of a chord based on its root note, chord type, and inversion. The parse_chord_string function takes a string 
representing a chord and returns a dictionary with detailed information about the chord, including its root note, type, inversion, bass note, and the pitches it consists of.
---------------------------------------
Next steps:
* simplify enharmonic
* chordnames
* midi labels
1) IN PROGRESS -- Add Error Handling: try / except
2) IN PROGRESS -- Add docstrings to the functions to explain what they do, what parameters they take, and what they return.
3) Variable Names: Some of the variable names (like actline and tmpactline) could be more descriptive. Clear variable names make your code easier to read and understand.
4) DONE -- The chord types are defined in two places: once in the chords dictionary and once in the separate_chordroot_chordtype function. This redundancy could lead to errors or inconsistencies if you update the chord types in one place but forget to update them in the other. One way to eliminate this redundancy is to define your chord types in a single place and then reference that definition wherever you need it.
5) DONE -- Midi-Range-Config (min/max notes): a) for bass; b ) for chords
6) IN PROGRESS -- Midi-Notes-Octaves calculation: needs to be in the defined range (see point no. 5)
7) Legato-mode: tie common notes
8) DONE -- Meta-Informations: a) add tempo in BPM; b) add meter (e.g. 4/4, 3/4, 6/4)
9) Save into: a) MusicXML; b) MIDI
10) feature integration: Transpose into all Keys: a) QZ (up/down); b) chromatically (up/down)
11) DONE -- Song-Pos in chord-list
12) feature integration: SB import / export files
---------------------------------------
"""
### INITIAL VARIABLES SECTION ###

# Define the notes (7 Stammtöne)
notes_basic = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

# Define the 12 notes enharmonic EQUAL (in sharp notation)
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# List of the enharmonic EQUAL note names (in sharp notation) and mapped to each note number:
note_names = {1:"C", 2:"C#", 3:"D", 4:"D#", 5:"E", 6:"F", 7:"F#", 8:"G", 9:"G#", 10:"A", 11:"A#", 12:"B"}

# Define the enharmonic CORRECT accidentals and map it to enharmonic EQUAL note numbers.
note_values = {
    '###': [4, 6, 8, 9, 11, 1, 3],
    '##': [3, 5, 7, 8, 10, 12, 2],
    '#': [2, 4, 6, 7, 9, 11, 1],
    'neutral': [1, 3, 5, 6, 8, 10, 12],
    'b': [12, 2, 4, 5, 7, 9, 11],
    'bb': [11, 1, 3, 4, 6, 8, 10],
    'bbb': [10, 12, 2, 3, 5, 7, 9]
}

# Define the chords unsing interval structure
# IMPORTANT: 1) Keep order range lenghts of Chord-type-descriptions DESCENDING in the list below! 
#            2) Don't remove default label "M" for major Chords.
chords = {
    'Sus4': ['R', 'P4', 'P5'],
    'Sus2': ['R', 'M2', 'P5'],
    'Maj7': ['R', 'M3', 'P5', 'M7'],
    'maj7': ['R', 'M3', 'P5', 'M7'],
    'Maj9': ['R', 'M3', 'P5', 'M7','M9'],
    'maj9': ['R', 'M3', 'P5', 'M7','M9'],
    'o7': ['R', 'm3', 'b5', 'b7'],
    'o': ['R', 'm3', 'b5'],
    'm7add11': ['R', 'm3', 'P5', 'm7', 'P11'],
    'm7': ['R', 'm3', 'P5', 'm7'],
    'm': ['R', 'm3', 'P5'],
    '+': ['R', 'M3', '#5'],
    '6': ['R', 'M3', 'P5', 'M6'],
    '7': ['R', 'M3', 'P5', 'm7'],
    'M': ['R', 'M3', 'P5'],
    '11': ['R', 'M3', 'P5', 'm7', 'M9', 'P11'],
    '13': ['R', 'M3', 'P5', 'm7', 'M9', 'P11', 'M13'],
    'add9': ['R', 'M3', 'P5', 'M9'],
    '7#9': ['R', 'M3', 'P5', 'm7','#9'],
}

# Midi-Range-Config (min/max notes): a) for bass; b ) for chords
# Midi-Notes-Octaves calculation: needs to be in the defined range
midi_range_bass = {'min': 'C0', 'max': 'E1'}
midi_range_chords = {'min': 'E1', 'max': 'E3'}

"""
# Beispiel für den Bereich der möglichen Noten auf dem Klavier (von C0 bis B7)
range_of_notes = [note + str(octave) for note in ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'] for octave in range(8)]

print('range:',range_of_notes)
"""

### FUNCTION SECTION ###

def parse_file(fname):
    """
    Parses a song file and extracts metadata and chords.
    
    Parameters:
    fname (str): The path to the song file.
    
    Returns:
    dict: A dictionary containing the song metadata and chords.
    """

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, fname)

    # Check if file exists
    if not os.path.exists(filename):
        print(f"File {filename} not found.")
        return None

    # Define the meta information of the song in the dictionary and initialize values
    # You can maintain this list based on the schema in the chordtxt file
    meta = [
        "author", 
        "title", 
        "key", 
        "bassnote", 
        "convertto", 
        "type", 
        "marker", 
        "tempo", 
        "meter"
    ]

    # Define song information based on previous meta fields and initialize values
    song = {metaitem: "" for metaitem in meta}

    # Add array for chords / pitches into the song schema and initialize values
    song["pos"] = []
    song["chords"] = []
    song["pitches"] = []

    try:

        # Open the file and parse it
        with codecs.open(filename, 'r', 'utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                # Parse meta information and write into song schema
                if i < len(meta):
                    song[meta[i]] = line.strip()
                else:
                    # Parse and Write chords into array
                    actline = line.strip()

                    # blank section or dot (.) character in chord progression means copy chord from previous
                    if(actline == '' or actline == '.'): 
                        actline = tmpactline
                    else: 
                        tmpactline = actline

                    song["pos"].append(i - len(meta))
                    song["chords"].append(actline)
                    song["pitches"].append(parse_chord_string(actline))
                
        # Output schema
        return song
    
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None
    
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return None

def get_note_number(note_name):

    # Split the note name into the note and the modifier
    if len(note_name) > 1:
        note = note_name[0]
        modifier = note_name[1:]
    else:
        note = note_name
        modifier = 'neutral'
    
    # Get the index of the note in the notes list
    index = notes_basic.index(note)
    
    # Return the corresponding note value
    return note_values[modifier][index]

def get_note_name(note_number):
    # Return the corresponding note name
    return note_names[note_number]

def get_pitches(root_note_enharm_correct, chord_name, inversion):

    # Get the intervals of the chord
    intervals = chords[chord_name]

    root_note_enharm_equal = get_note_name(get_note_number(root_note_enharm_correct))
    
    # Convert the root note to an index
    root_index = notes.index(root_note_enharm_equal)
    
    # Convert the intervals to pitches
    pitches = [notes[(root_index + {'R' : 0,  # c
                                    'm2': 1,  # c#/db
                                    'm9': 1,  # c#/db
                                    'M2': 2,  # d
                                    'M9': 2,  # d
                                    'm3': 3,  # d#/eb
                                    '#9': 3,  # d#/eb
                                    'M3': 4,  # e
                                    'P4': 5,  # f
                                    'P11': 5, # f
                                    '#4': 6,  # f#/gb
                                    'b5': 6,  # f#/gb
                                    'P5': 7,  # g
                                    '#5': 8,  # g#/ab
                                    'm6': 8,  # g#/ab
                                    'M6': 9,  # a
                                    'M13': 9, # a
                                    'b7': 9,  # a
                                    'm7': 10, # a#/bb
                                    'M7': 11, # b
                                    '#7': 0   # c
                                    }[interval]) % len(notes)] for interval in intervals]
    
    # Apply the inversion
    for i in range(inversion):
        pitches = pitches[1:] + [pitches[0]]
    
    return pitches

def parse_chord_string(input_string):
    """
    Parses a chord string and returns detailed information about the chord.
    
    Parameters:
    input_string (str): The chord string.
    
    Returns:
    dict: A dictionary containing detailed information about the chord.

    examples:
       "G"       -- (G G G)
       "G/f"     -- (G F G)
       "G/C"     -- (G G C)
       "G/f/C"   -- (G F C)
    """
    try:

        chord_informations = {'root': None}

        split_strings = input_string.split('/')

        # split chordroot and chordtype
        root, chord_type = separate_chordroot_chordtype(split_strings[0])

        # print(get_pitches(root, chord_type, 0))
        
        # store chordroot note
        chord_informations['root'] = root
        chord_informations['type'] = chord_type
        
        if len(split_strings) > 1:
            for string in split_strings[1:]:
                if string[0].isupper():
                    chord_informations['bass'] = string
                else:
                    chord_informations['inversion'] = string[0].upper() + string[1:]

        # fill in empty values for inversion and/or bass note with root note
        chord_informations['inversion'] = chord_informations.get('inversion', chord_informations['root'])
        chord_informations['bass'] = chord_informations.get('bass', chord_informations['root'])

        # make all notes to enharmonic EQUAL
        chord_informations['root'] = get_note_name(get_note_number(chord_informations['root']))
        chord_informations['inversion'] = get_note_name(get_note_number(chord_informations['inversion']))
        chord_informations['bass'] = get_note_name(get_note_number(chord_informations['bass']))

        # calculate inversion number
        calc_inversion = get_pitches(root, chord_type, 0).index(chord_informations['inversion'])
        chord_informations['inversion_id'] = calc_inversion

        chord_informations['pitches'] = get_pitches(root, chord_type, calc_inversion)

        return chord_informations
    
    except Exception as e:
        print(f"!!! Error parsing chord string {input_string}: {e}")
        sys.exit()
        return None

def separate_chordroot_chordtype(chord):
    """
    Separates the root note and chord type from a chord string.
    
    Parameters:
    chord (str): The chord string.
    
    Returns:
    tuple: A tuple containing the root note and chord type.
    """
    # Iterate over chord types
    for chord_type in chords.keys():
        if chord.endswith(chord_type):
            return chord[:-len(chord_type)], chord_type

    # If no match found, return the whole chord as root and 'M' (for Major Triad) as default type
    return chord, 'M'

def save_into_file(export_file_path, export_filename, chords, gettimesignature):
    """
    Stores the new chordprogression into musicxml / MXL / MIDI file.
    """

    print('timesignature:',gettimesignature)

    if(len(chords)>0):

        store_file = os.path.join(export_file_path, export_filename)
        print("store_file:",store_file)

        # Define the chords
        # chords = ['C2 E3 G3 C4', 'G3 B3 D4', 'C4 E4 G4']

        # Create a stream
        s = stream.Stream()

        s.append(metadata.Metadata(composer = "LUM"))
        s.append(metadata.Metadata(title = "PROGRESSION"))

        # Set the time signature to 3/4
        s.metadata = metadata.Metadata()
        s.metadata.timeSignature = meter.TimeSignature(gettimesignature)

        # Set the time signature again to ensure it's included in the MusicXML output
        s.append(meter.TimeSignature(gettimesignature))

        count = 1
        # Add the chords to the stream with the calculated duration
        for c in chords:

            # ----------------------
            #c.simplifyEnharmonics(inPlace=True, keyContext=key.Key('A-'))
            #ch.pitchedCommonName
            # ----------------------

            es = analysis.enharmonics.EnharmonicSimplifier(c.split())
            es.bestPitches()

            # get chord block
            ch = chord.Chord(es)

            # Römisches Numeral als Label hinzufügen
            roman_numeral = roman.romanNumeralFromChord(ch, 'C', preferSecondaryDominants=True)
            ch.addLyric(str(roman_numeral.figure))

           

            # label chord id
            #ch.addLyric(str(count))
            #ch.addLyric(sf)

            # add data
            s.append(ch)

            count += 1

        # Write to a MusicXML file
        s.write('musicxml', fp=store_file + '.mxl')

        # Write to a MIDI file
        s.write('midi', fp=store_file + '.midi')

        # --- OPEN IN MUSE4 ---
        #### s.show("text")
        #### s.show()
    else:
        print("!!! empty chords in txt content --> skipped creating output file.")

    return "SUCCESS"

def calculate_octaves(song):

    """
    Jede bass-note und jede note im akkord wird für die möglichen 88 töne auf dem klavier mit den oktaven versehen.
    Hier werden die Oktaven für die Noten im Akkord und die Bassnote mit den entsprechenden Oktavbrüchen versieht.
    """

    chord_list = []

    # mapping notennamen zu ids
    note_names = {1: "C", 2: "C#", 3: "D", 4: "D#", 5: "E", 6: "F", 7: "F#", 8: "G", 9: "G#", 10: "A", 11: "A#", 12: "B"}

    # iterate chords
    for i in song['pitches']:

        print('----')

        # init previous note id zur identifikation des oktav-bruches
        prev_note_id = 0
        note_octave = 4
        txt = ''

        # Get Bassnote
        bass_octave = 3
        bass = i['bass']

        txt = txt + bass + str(bass_octave)
        print(bass, bass_octave)

        # Iterate Notes in Chords
        for note in i['pitches']:
            # Get the ID of the note name using the get method
            note_id = next((id for id, name in note_names.items() if name == note), None)

            # Assign the ID to the note name in the mapping dictionary
            if note_id is not None:

                # identifikation des oktav-bruches
                if note_id > prev_note_id:
                    prev_note_id = note_id
                else:
                    prev_note_id = note_id
                    note_octave += 1

                txt = txt + ' ' + note + str(note_octave)
                print(note, note_octave)
  
        chord_list.append(txt)
        print('txt:',txt)

    return chord_list

### CALL FUNCTIONS SECTION ###

# Define the path to the chordtxt import-file to parse
# You can edit this variable

script_verzeichnis = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_verzeichnis, "txt", "02_chord_progressions_for_songwriters","01_ascending_basslines")
print("file_path:",file_path)

txt_files = []

#### MANUAL INPUT: only selected file processing (instead of batch job)
#### txt_files.append("0001.txt")
#### txt_files.append("0003.txt")

if(len(txt_files)==0):
    ### BATCH JOB: Hole Liste aller .txt-Dateien im angegebenen Ordner für den batch job
    txt_files = [f for f in os.listdir(file_path) if f.endswith('.txt')]

# Iterieren Sie über jede Datei und verarbeiten Sie sie
for file_name in txt_files:
    print("Processing file:", file_name)

    file_title = file_name[:-4]
    file_extension = '.txt'

    file_name = os.path.join(file_path,file_title + file_extension)
    print("source_file:",file_name)

    ### CALL FUNCTIONS ###

    song = parse_file(file_name)
    print('--song:',song)

    chord_list = calculate_octaves(song)
    print('chord_list:',chord_list)

    print(save_into_file(file_path, file_title, chord_list, song['meter']))

### Test the functions ###

#print(get_note_name(get_note_number('Dbbb')))
#print(get_pitches('C', 'Maj7', 0))

#example_string = "D#/bb/G"
#print(parse_chord_string(example_string))

#root, chord_type = separate_chordroot_chordtype('CbbSus2')
#print('Root:', root)
#print('Chord Type:', chord_type)