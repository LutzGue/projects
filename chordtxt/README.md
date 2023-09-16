# Project
## Chord Progression Parser and Converter
### Description
Generate chord progressions in MIDI and MusicXML file from a given chord progression in TXT format and provide transposing batch.
### Goal
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
### Next Steps:
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
### *Project names:
- ChordCaster: Progression Converter
- ChordConvert: MIDI & MusicXML Transformer
- ProgressionPivot: Chord Converter
- ChordCraft