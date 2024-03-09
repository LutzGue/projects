"""
chord melody woiceleading
v0.0.1
2024-03-03
Lutz Menzel
MIT 2

# TODO # BUG # NOTE # FIXME # HACK # XXX

# NOTE: MuseScore4 > Datei > Export > Hauptpartitur [x] | Piano [_] > MusicXML | Komprimiert (.mxl) | Gesamtes Layout | 
"""

from music21 import *
import os
import pprint

from config import config

class ChordProgression:
    """
    """
    def __init__(self, config):
        """
        """
        # imported parameters from config JSON file
        self.config = config

        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.file_title = '0003b.mxl'
        self.file_name = os.path.join(self.script_path, self.file_title)
        self.file_exists = os.path.exists(self.file_name)

    def start(self):
        """
        """
        res = ''
        res = self.open()
        print(res)

    def open(self):

        # Überprüfen Sie das aktuelle Arbeitsverzeichnis
        if not self.file_exists:
            return "ERR: file does not exists."

        sp = converter.parse(self.file_name)
        
        noten_und_akkorde = []
        for element in sp.recurse():
            if isinstance(element, stream.PartStaff):
                pprint.pprint(f'*** part: {element.id}')
            if isinstance(element, layout.StaffLayout):
                pprint.pprint(f'*** staff_nr:: {element.staffNumber}')
            if isinstance(element, clef.TrebleClef):
                pprint.pprint(f'*** clef: {element.name}')
            if isinstance(element, clef.BassClef):
                pprint.pprint(f'*** clef: {element.name}')
            if isinstance(element, stream.Voice):
                pprint.pprint(f'*** voice_id: {element.id}')
            if isinstance(element, stream.Measure):
                #if not element.clef is None:
                #    clef_type = element.clef.name
                #else:
                #    clef_type = 'bass'
                pprint.pprint(f'--- measure: {element.measureNumber} ---')
            if isinstance(element, tempo.MetronomeMark):
                pprint.pprint(f'bpm: {element.number}')
            if isinstance(element, meter.TimeSignature):
                pprint.pprint(f'timesign: {element.numerator} / {element.denominator}')
            if isinstance(element, key.KeySignature):
                pprint.pprint(f'keysign: {element.sharps}')
            if isinstance(element, note.Rest):
                pprint.pprint(f'*** {element.beat} rest: {element.duration.quarterLength}')
            if isinstance(element, note.Note):
                if len(element.lyrics) > 0:
                    pprint.pprint(f'key: {element.lyrics[0].rawText}')
                pprint.pprint(f'*** {element.beat} voice: {element.activeSite.id} note: {element.nameWithOctave} {element.duration.quarterLength}')
                pprint.pprint(element.activeSite)
                pprint.pprint(element.activeSite.voices)
                if len(element.beams) > 0:
                    pprint.pprint(element.beams)

            if isinstance(element, chord.Chord):
                if hasattr(element, 'figure'):
                    pprint.pprint(element.figure)
                    if len(element.notes) > 0:
                        pprint.pprint(element.notes)
                if hasattr(element, 'romanNumeral'):
                    pprint.pprint(element.romanNumeral.figure)
                    actRoman = roman.RomanNumeral(element.romanNumeral.figure, 'g')
                    pprint.pprint(actRoman.figureAndKey)
                    pprint.pprint(actRoman.notes)
            #else:
            #    pprint.pprint(element)

        # return sp.elements, 
        return None
 
# create class
cp = ChordProgression(config)

# NOTE: process start
res = ''
res = cp.start()
print(res)