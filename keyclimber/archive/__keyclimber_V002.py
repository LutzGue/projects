import mido
import os
from music21 import *

"""
-------------------------
Lutz Menzel
Berlin. 2023-09-16
MIT License
-------------------------
The program, "K<yClimber", is designed to import MIDI and MusicXML files, transpose them by 7 semitones, and then save the transposed music back as MIDI and MusicXML files. Here’s a step-by-step description of what the program does:
-------------------------
"""

### FUNCTION SECTION

def import_transpose(import_filename, export_filename, import_codec):
    """
    Import MIDI and MusicXML files, transpose and save new MIDI file.
    -------------------------
    The program starts by importing the MIDI file using the mido library and the MusicXML file using the music21 library.
    Transpose the music: The program then transposes all the notes in the imported MIDI and MusicXML files by 7 semitones. In the case of MIDI files, it directly modifies the note values in the MIDI messages. For MusicXML files, it uses the transpose function provided by music21.
    Save the transposed music: Finally, the program saves the transposed music back as MIDI and MusicXML files.
    """

    try:

        # path to filename
        dirname = os.path.dirname(__file__)

        rel_filename_import = os.path.join(dirname, import_filename)
        rel_filename_export = os.path.join(dirname, export_filename)

        # Check if file exists
        if not os.path.exists(rel_filename_import):
            print(f"File {rel_filename_import} not found.")
            return None

        # cases import_codec
        if(import_codec == 'midi'):
            import_transpose_midi(rel_filename_import, rel_filename_export)
        elif(import_codec == 'musicxml'):
            import_transpose_musicxml(rel_filename_import, rel_filename_export)
        else:
            print(f"unknown import_codec {import_codec}")

        return "SUCCESS"

    except FileNotFoundError:
        print(f"File {rel_filename_import} not found.")
        return None
    
    except Exception as e:
        print(f"Error reading file {rel_filename_import}: {e}")
        return None

def import_transpose_midi(import_filename, export_filename):

    # MIDI-Datei importieren und transponieren
    midi = mido.MidiFile(import_filename)
    for i, track in enumerate(midi.tracks):
        for msg in track:
            if msg.type == 'note_on' or msg.type == 'note_off':
                msg.note = (msg.note + 7) % 128

    # MIDI-Datei speichern
    midi.save(export_filename)

    return "SUCCESS"

def import_transpose_musicxml(import_filename, export_filename):
    orig_piece = converter.parse(import_filename)

    is_well_formed = orig_piece.isWellFormedNotation()
    print('orig_piece: ', is_well_formed)
    orig_key = orig_piece.analyze('key')
    print('orig_key:', orig_key)

    target_key = pitch.Pitch('C')
    if orig_key.type == 'minor':
        target_key = pitch.Pitch('A')

    if target_key.name != orig_key.tonic.name:
        move = interval.Interval(orig_key.tonic, target_key)
        base_piece = orig_piece.transpose(move)

    print('base_piece:', base_piece.isWellFormedNotation())
    base_key = base_piece.analyze('key')
    print('base_key:', base_key)

    move = interval.Interval('-P5')
    final_chords = []

    for _ in range(7):
        transp_piece = base_piece.transpose(move)
        # Recursively search for ChordSymbol elements
        chord_elements = transp_piece.recurse().getElementsByClass('ChordSymbol')
        # Append the transposed chords to the final_chords list
        final_chords.extend([str(chord) for chord in chord_elements])

    print('Final Chords___:', final_chords)

    print('final_chords well formated:', final_chords.isWellFormedNotation())

    # Save the final combined file
    final_chords.write('musicxml', export_filename)

    return "SUCCESS"

### CALL SECTION

### --- MIDI ---
#### import_filename = 'mid\\0001.midi'
#### export_filename = 'mid\\0001_mid_transp.midi'
#### import_codec = 'midi'  ### 'midi / musicxml'

#### --- MUSICXML ---
#import_filename = 'musicxml\\46.musicxml'
#export_filename = 'musicxml\\46_transp.musicxml'
#import_codec = 'musicxml'  ### 'midi / musicxml'

### --- MXL ---
import_filename = 'musicxml\\0003.mxl'
export_filename = 'musicxml\\0003_transp.mxl'
import_codec = 'musicxml'  ### 'midi / musicxml'

print(import_transpose(import_filename, export_filename, import_codec))
