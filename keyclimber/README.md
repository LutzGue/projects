# KeyClimber
## Transposing music files
### Description
The program "KeyClimber" is designed to import MIDI and MusicXML files, transpose them in circle of fifths up/down and chromatically, and then save the transposed music back as MIDI and MusicXML files.

1) Import MIDI and MusicXML files: The program starts by importing the MIDI file using the mido library and the MusicXML file using the music21 library.

2) Transpose the music: The program then transposes all the notes in the imported MIDI and MusicXML files by 7 semitones. In the case of MIDI files, it directly modifies the note values in the MIDI messages. For MusicXML files, it uses the transpose function provided by music21.

3) Save the transposed music: Finally, the program saves the transposed music back as MIDI and MusicXML files.

*Other Project names:
- TranspoTune
- KeyClimber
- HarmonyHike