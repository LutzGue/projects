"""
Python code that uses the music21 library to generate chord progressions in MIDI and MusicXML file formats from a given chord progression in TXT format. The user can transfer chord progressions from books or websites in a simple input format into a txt file. Voice leading possibilities are calculated for the transitions of the chords. The generated MIDI file can be practiced on the piano and expands your playing skills on the instrument. This develops new improvisation skills. The helper tool can be used to create new txt files for entering chord progressions and generate any number of input documents.

TODO:
    0) integrate "position" section inside of "qz-transpose" framework
    1) slash bass notes
        a) lowest note is bass note: skip vertical-vl variations that violates this condition
        b) add root note into vertical-vl (above root note)
    2) create stream in grand staff sheet to visualize all vl-vertical possibilities to chords
    3) roll out vl-vertical options based on starting chord vl-vertical and connected using vl-horizontal rules and ranking
    4) parameters: add min/max parameters for sus4 and sus2 chord types
    5) input TXT can be used to enter roman numerales and keys. It will be automatically converted into chords.
"""
from music21 import *
import os
import codecs
from itertools import product
import pprint
import json

class ChordProgression:
    """
    Klasse für Akkord-Progressionen.
    """
    def __init__(self, file_title, fname_source, fname_midi, fname_musicxml):
        """
        Konstruktor der Klasse. Er nimmt den Pfad zu einer TXT-Datei, die die Akkordfolge enthält, als Argument und initialisiert einen music21 Stream.
        """
        self.file_title = file_title
        self.fname_source = fname_source
        self.fname_midi = fname_midi
        self.fname_musicxml = fname_musicxml

        self.s = stream.Stream()

        # Erstelle ein neues Notenblatt
        self.sheet = stream.Score()

    def parse_file(self):
        """
        Parses a song file and extracts metadata and chords.
        
        Parameters:
        fname (str): The path to the song file.
        
        Returns:
        dict: A dictionary containing the song metadata and chords.
        """

        print('--- START parse_file ---')

        self.grand_staff_sheet()

        filename = self.fname_source

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
                        
            # The parsed output song needs to contain 11 lines to be well-processed.
            check_song = len(song)
            check_song_pos = len(song["pos"])
            check_song_chords = len(song["chords"])

            if check_song > 10 and check_song_pos > 0 and check_song_chords > 0:
                print('STATUS: parse_file was SUCCESSFULL. Song contains', check_song, 'lines /', check_song_pos, check_song_chords, 'chords.')

                # Call function to generate chords into sheet.
                self.generate_chord_progression(song)

            else:
                print('STATUS: parse_file with ERROR. Song contains', check_song, 'lines /', check_song_pos, check_song_chords, 'chords.')

            return 'SUCCESS'
        
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return None
        
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            return None

    def generate_chord_progression(self, song):
        """
        Methode generiert Akkordfolgen in MIDI- und MusicXML-Dateiformaten. Sie liest die Akkorde aus der TXT-Datei, fügt sie dem music21 Stream hinzu und schreibt dann den Stream in die Ausgabedateien.
        Documentation library music21.harmony:
        https://web.mit.edu/music21/doc/moduleReference/moduleHarmony.html#music21.harmony.ChordSymbol.findFigure
        https://web.mit.edu/music21/doc/moduleReference/moduleHarmony.html#music21.harmony.realizeChordSymbolDurations
        Documentation MuseScore4:
        https://musescore.org/en/handbook/3/chord-notation-systems
        """

        print('--- START generate_chord_progression ---')

        gettimesignature = song['meter']  # e.g.: '4/4'
        getkey           = song['key']    # e.g.: "C"

        # ---------------



        # -------------------------

        # Erstelle die beiden Notensysteme
        bass_clef = clef.BassClef()
        treble_clef = clef.TrebleClef()

        # Füge die Notensysteme zum Notenblatt hinzu
        self.sheet.append([bass_clef, treble_clef])

        # Erstelle die beiden Notenlinien
        left_hand = stream.Part()
        right_hand = stream.Part()

        # Füge die Notenlinien zum Notenblatt hinzu
        self.sheet.insert(0, left_hand)
        self.sheet.insert(0, right_hand)

        # Erstelle die Noten
        a1 = note.Note('A1')
        a2 = note.Note('A2')
        a3 = note.Note('A3')
        c4 = note.Note('C4')
        e4 = note.Note('E4')

        # Füge die Noten zur linken Hand hinzu
        left_hand.append([a1, a2])

        # Erstelle den Akkord
        #chord_tmp = chord.Chord([a3, c4, e4])

        # Füge den Akkord zur rechten Hand hinzu
        right_hand.append([a3, c4, e4])

        # Verbinde die beiden Notenlinien mit einer Akkoladenklammer
        # Verbinde die beiden Notenlinien mit einer Akkoladenklammer
        bracket = spanner.Line(left_hand[-1], right_hand[0])
        self.sheet.insert(0, bracket)

        self.sheet.show('text')

        # Write the stream to a MIDI file
        self.sheet.write('midi', fp = 'sheet_0001.mid')

        # Write the stream to a MusicXML file
        self.sheet.write('musicxml', fp = 'sheet_0001.mxl')

        # ---------------

        # Load the .mxl file
        score_template = converter.parse('grand_sheet_piano_0000.xml')

        # Holen Sie sich die Partitur
        partitur = score_template.getElementsByClass('Part')[0]

        # Holen Sie sich den Violinschlüssel
        violinschluessel = None
        bassschluessel = None
        for element in partitur.recurse():
            if isinstance(element, clef.TrebleClef):
                violinschluessel = element
            elif isinstance(element, clef.BassClef):
                bassschluessel = element

        # Erstellen Sie eine neue Note
        neue_note = note.Note('C#4')

        # Fügen Sie die neue Note zum Violinschlüssel hinzu
        violinschluessel.insert(0, neue_note)

        # Save the modified score as a new .mxl file
        score_template.write('musicxml', fp='grand_sheet_piano_0001.xml')
        score_template.write('midi', fp='grand_sheet_piano_0001.mid')

        # Show the modified score
        score_template.show('text')

        # ---------------

        # set title and composer
        self.s.append(metadata.Metadata(title = self.file_title, composer = 'Menzel, Lutz'))

        # Set the time signature (e.g. 4/4, 3/4, ..)
        self.s.append(meter.TimeSignature(gettimesignature))

        # Set key
        self.s.append(key.Key(getkey))

        chords = song['chords']
        print('chords:',chords)

        i = 0
        previous_c = ''

        # Add each chord to the stream
        for chord in chords:
            #print('chord:',chord)
            
            c = harmony.ChordSymbol(chord.strip())
            d = roman.romanNumeralFromChord(c, getkey, preferSecondaryDominants=True)
            c.writeAsChord = True

            r = d.figure
            if (i == 0):
                r = getkey + ':' + r

            c.lyric = chord.strip() + '\n' + r

            #print('s:',c)

            if c != previous_c:
                self.s.append(c)
            else:
                rest = note.Rest(quarterLength=1)
                self.s.append(rest)

            i += 1
            previous_c = c

        # Write the stream to a MIDI file
        self.s.write('midi', fp = self.fname_midi)

        # Write the stream to a MusicXML file
        self.s.write('musicxml', fp = self.fname_musicxml)

        self.s.show('text')
        
        # pianoroll
        #self.s.plot('pianoroll')

        # Krumhansl key estimation graph
        #p = graph.plot.WindowedKey(self.s)
        #p.run()

        self.transpose_chords()
        self.voiceleading(song)

    def extract_chordtype(self, getfullchordname):
        """
        Der Grundton wird identifiziert und entfernt. Dann werden '#' und '-' Zeichen vom verbleibenden Teil des Akkords entfernt. Schließlich wird alles nach dem Schrägstrich-Zeichen für den Akkordtyp entfernt.
        """
        print('---START','extract_chordtype')

        try:

            # Identifiziere Grundton
            grundton = ''
            for char in getfullchordname:
                if char in 'CDEFGAB':
                    grundton += char
                else:
                    break

            # Entferne '#' und '-' Zeichen
            akkordteil = getfullchordname[len(grundton):].lstrip('#').lstrip('-')

            # Entferne alles nach dem Schrägstrich-Zeichen
            akkordtyp_parts = akkordteil.split('/')
            akkordtyp = akkordtyp_parts[0]

            print('---END','extract_chordtype')

            return akkordtyp
        
        except Exception as e:
            print("!!! ERROR:", e)
            return None

    def transpose_chords(self):
        """
        Methode für eine Transponierungsfunktion. Die Akkorde werden im Stream transponieren.
        """
        print('--- START transpose_chords ---')
        # Placeholder for transposing function
        pass

    def voiceleading(self, song):
        """
        Methode zur berechnung der möglichen voiceleading optionen.
        """
        print('--- START voiceleading ---')
        # Placeholder for voiceleading function

        self.vl_get_chord_type(song)

        self.vl_get_bass_note()
        self.vl_get_bass_is_inversion()
        self.vl_roll_out_notes()
        self.vl_get_root_motion()

        pass

    def vl_get_chord_type(self, song):
        """
        Methode um zu den Akkorden den Akkord-Typ zu ermitteln. Hierdurch werden die basic chord tones (z.B. 1, 3, 7) festgelegt und von den nicht benötigten tönen (z.B. 5th) und Tension notes (z.B. T9, T11, T13) unterschieden.
        
        music21 CHORD_TABLE:
            https://github.com/cuthbertLab/music21/blob/f457a2ba52ea3f978d805cd52fa101dfb0dd8577/music21/harmony.py#L60
        """
        print('--- START vl_get_chord_type ---')

        # define the range of generated octaves and midi note ids for each voice note.
        parameters = {
            'range':{
                # global range for vl-vertical generation (min:1;max:5)
                'octave':{
                    'min': 1,
                    'max': 5
                },
                # bass note is the lowest note (A1;F#3)
                'bass_midi':{
                    'min': pitch.Pitch('A1').midi,
                    'max': pitch.Pitch('F#3').midi
                },
                # doubling the root above the bass note (in case of bass note is different to root)
                'root_midi':{
                    'min': pitch.Pitch('D3').midi,
                    'max': pitch.Pitch('C5').midi
                },
                # 3rd. (e.g.: "C";"Cm";"C7";...)
                'third_midi':{
                    'min': pitch.Pitch('D3').midi,
                    'max': pitch.Pitch('C5').midi
                },
                # 7th. (e.g.: "C7";"Cm7";...)
                'seventh_midi':{
                    'min': pitch.Pitch('D3').midi,
                    'max': pitch.Pitch('C5').midi
                },
                # 5th. (e.g.: "C";"Cm";"C7";"Cdim";"Cdim7";"C+";"C+7";"Cm7b5";...)
                'fifth_midi':{
                    'min': 48,
                    'max': 60
                },
                # add 6 = T13 (e.g. "Cm13")
                'sixth_midi':{
                    'min': 48,
                    'max': 60
                },
                # 6-chord (instead of 5) (e.g.: "C6")
                'sixth_chord_midi':{
                    'min': 48,
                    'max': 60
                },
                # add 4 = T11 (e.g. "Cm11")
                'fourth_midi':{
                    'min': 48,
                    'max': 60
                },
                # sus4 (instead of third) (e.g. "Csus4")
                'sus4_chord_midi':{
                    'min': 48,
                    'max': 60
                },
                # add 2 = T9 (e.g.: "C9", "C/D")
                'second_midi':{
                    'min': 48,
                    'max': 60
                },
                # sus2 (instead of third) (e.g. "Csus2")
                'sus2_chord_midi':{
                    'min': 48,
                    'max': 60
                },
                # OTHERS (Tensions) (e.g.: TBD.)
                'tension_midi':{
                    'min': 48,
                    'max': 60
                }
            }
        }

        ### initial output dictionary for calculated voiceleading options. ###

        #---------------------------

        # create dictionary framework for transposing (iterations in intervals using start key)
        vl0 = self.transpose_qz('C', 'p5', 8)
        
        for act_qz in vl0['qz']:
            
            # calculate all possible voice leadings options for the chords in the current transposed key
            tmp = self.create_position(act_qz['qz_name'])

            # add positions into main dictionary framework for all transposed keys and loop again
            vl0['qz'][act_qz['qz_id']]['position'].append(tmp)

        # output final dictionary containing all transposed chords in all voice leadings
        pprint.pprint(vl0)

        #---------------------------

        vl = {'position':[]}

        #chord_list = []
        pos = -1

        for element in self.s.recurse():
            
            if 'ChordSymbol' in element.classes:

                chord_notes = element.pitchNames
                found_chord_notes = []

                pos += 1

                # bass
                actBass = ''
                if element.bass() is not None:
                    actBass = element.bass().name
                    actBassScale = -1   # placeholder value; TODO: calculate scale degree for bassnote (in case of inversion)
                    found_chord_notes.append(actBass)

                # root
                actRoot = ''
                if element.root() is not None:
                    actRoot = element.root().name
                    found_chord_notes.append(actRoot)

                # 3rd.
                actThird = ''
                if element.third is not None:
                    actThird = element.third.name
                    found_chord_notes.append(actThird)

                # 5th.
                actFifth = ''
                if element.fifth is not None:
                    actFifth = element.fifth.name
                    found_chord_notes.append(actFifth)

                # 7th.
                actSeventh = ''
                if element.seventh is not None:
                    actSeventh = element.seventh.name
                    found_chord_notes.append(actSeventh)

                # sus2-chord / add2 = T9
                actSecond = ''
                if element.getChordStep(2) is not None:
                    actSecond = element.getChordStep(2).name
                    found_chord_notes.append(actSecond)

                # sus4-chord / add4 = T11
                actFourth = ''
                if element.getChordStep(4) is not None:
                    actFourth = element.getChordStep(4).name
                    found_chord_notes.append(actFourth)

                # 6-chord / add6 = T13
                actSixth = ''
                if element.getChordStep(6) is not None:
                    actSixth = element.getChordStep(6).name
                    found_chord_notes.append(actSixth)

                # GENERATE TENSION LIST (get list of remaining (not mapped) chord-tones)
                # e.g.: "B7add#15" --> T#15:"B#"
                print(found_chord_notes)
                print(chord_notes)
                
                tension_notes = []
                tension_notes = [note for note in chord_notes if note not in found_chord_notes]
                
                # check, if all notes are mapped to the scale
                if len(tension_notes) == 0:
                    print("SUCCESS: All notes are mapped to the scale.")
                else:
                    print('!INFO: There are notes that are NOT mapped and added to remaining tension list:', tension_notes)

                # ------------------
                    
                normalOrder = element.normalOrder
                firstPitch = normalOrder[0]
                no = [(pc - firstPitch) % 12 for pc in normalOrder]

                item = {
                        'pos': (pos + 1),
                        'chord_orig_name': song['chords'][pos],
                        'chord_type_extracted': self.extract_chordtype(element.figure),
                        'chord_name': element.figure,
                        'inversion_nr': element.inversion(),
                        'chord_type_descr': element.commonName,
                        'chord_quality': element.quality,
                        'chord_type_id': element.primeFormString,
                        'normal_order': element.normalOrderString, ###
                        'normal_order_0': no, ###
                        'forte_class': element.forteClass, ###
                        'interval_vector': element.intervalVectorString,
                        'geometric': element.geometricNormalForm(),
                        'vl':[],
                        'bass':{
                            'note': actBass,
                            # in case of inversions, convert bass into scalenumber
                            'scale': actBassScale,      
                            'octaves': [],
                            'midi': []
                        },
                        'root':{
                            'note': actRoot,
                            'octaves': [],
                            'midi': []
                        },
                        'third':{
                            'note':actThird,
                            'octaves':[],
                            'midi': []
                        },
                        'seventh':{
                            'note':actSeventh,
                            'octaves':[],
                            'midi': []
                        },
                        'fifth':{
                            'note':actFifth,
                            'octaves':[],
                            'midi': []
                        },
                        'second':{
                            'note':actSecond,
                            'octaves':[],
                            'midi': []
                        },
                        'fourth':{
                            'note':actFourth,
                            'octaves':[],
                            'midi': []
                        },
                        'sixth':{
                            'note':actSixth,
                            'octaves':[],
                            'midi': []
                        },
                        'tensions':[{
                            'note':tension_notes,
                            'octaves':[],
                            'midi':[]
                        }]
                    }

                vl['position'].append(item)

                # calculate Bass and other notes VL variations in a given range.
                for i in range(parameters['range']['octave']['min'], parameters['range']['octave']['max'] + 1):

                    # check cases: 1) root note (no inversion) or 2) slash bass (inversion)
                    isInRootPosition = True
                    if actBass != actRoot:
                        isInRootPosition = False
                    
                    # initialize variables
                    isThirdDoubled = False
                    isFifthDoubled = False
                    isSeventhDoubled = False
                    isSecondDoubled = False
                    isFourthDoubled = False
                    isSixthDoubled = False
                    #isTensionsDoubled = False

                    bass_scale = -1

                    # case is inversion: bass note doubles maybe 3rd or 5th, or others
                    if not isInRootPosition:
                        if actBass == actThird:
                            isThirdDoubled = True
                            bass_scale = 3
                        elif actBass == actFifth:
                            isFifthDoubled = True
                            bass_scale = 5
                        elif actBass == actSeventh:
                            isSeventhDoubled = True
                            bass_scale = 7
                        elif actBass == actSecond:
                            isSecondDoubled = True
                            bass_scale = 2
                        elif actBass == actFourth:
                            isFourthDoubled = True
                            bass_scale = 4
                        elif actBass == actSixth:
                            isSixthDoubled = True
                            bass_scale = 6
                        # TODO: elif actBass == tension_notes
                    else:
                        bass_scale = 8

                    # TODO: case sus2 / sus4

                    if actBass != '':
                        bass_note = actBass + str(i)
                        if pitch.Pitch(bass_note).midi is not None:
                            bass_midi = pitch.Pitch(bass_note).midi
                            if bass_midi >= parameters['range']['bass_midi']['min'] and bass_midi <= parameters['range']['bass_midi']['max']:
                                vl['position'][pos]['bass']['octaves'].append(bass_note)
                                vl['position'][pos]['bass']['midi'].append(bass_midi)

                    if actRoot != '':
                        root_note = actRoot + str(i)
                        if pitch.Pitch(root_note).midi is not None:
                            root_midi = pitch.Pitch(root_note).midi
                            if root_midi >= parameters['range']['root_midi']['min'] and root_midi <= parameters['range']['root_midi']['max']:
                                vl['position'][pos]['root']['octaves'].append(root_note)
                                vl['position'][pos]['root']['midi'].append(root_midi)

                    if actThird != '':
                        third_note = actThird + str(i)
                        if pitch.Pitch(third_note).midi is not None:
                            third_midi = pitch.Pitch(third_note).midi
                            if third_midi >= parameters['range']['third_midi']['min'] and third_midi <= parameters['range']['third_midi']['max']:
                                vl['position'][pos]['third']['octaves'].append(third_note)
                                vl['position'][pos]['third']['midi'].append(third_midi)

                    if actSeventh != '':
                        seventh_note = actSeventh + str(i)
                        if pitch.Pitch(seventh_note).midi is not None:
                            seventh_midi = pitch.Pitch(seventh_note).midi
                            if seventh_midi >= parameters['range']['seventh_midi']['min'] and seventh_midi <= parameters['range']['seventh_midi']['max']:
                                vl['position'][pos]['seventh']['octaves'].append(seventh_note)
                                vl['position'][pos]['seventh']['midi'].append(seventh_midi)

                    if actFifth != '':
                        fifth_note = actFifth + str(i)
                        if pitch.Pitch(fifth_note).midi is not None:
                            fifth_midi = pitch.Pitch(fifth_note).midi
                            if fifth_midi >= parameters['range']['fifth_midi']['min'] and fifth_midi <= parameters['range']['fifth_midi']['max']:
                                vl['position'][pos]['fifth']['octaves'].append(fifth_note)
                                vl['position'][pos]['fifth']['midi'].append(fifth_midi)

                    if actSecond != '':
                        second_note = actSecond + str(i)
                        if pitch.Pitch(second_note).midi is not None:
                            second_midi = pitch.Pitch(second_note).midi
                            if second_midi >= parameters['range']['second_midi']['min'] and second_midi <= parameters['range']['second_midi']['max']:
                                vl['position'][pos]['second']['octaves'].append(second_note)
                                vl['position'][pos]['second']['midi'].append(second_midi)

                    if actFourth != '':
                        fourth_note = actFourth + str(i)
                        if pitch.Pitch(fourth_note).midi is not None:
                            fourth_midi = pitch.Pitch(fourth_note).midi
                            if fourth_midi >= parameters['range']['fourth_midi']['min'] and fourth_midi <= parameters['range']['fourth_midi']['max']:
                                vl['position'][pos]['fourth']['octaves'].append(fourth_note)
                                vl['position'][pos]['fourth']['midi'].append(fourth_midi)

                    if actSixth != '':
                        sixth_note = actSixth + str(i)
                        if pitch.Pitch(sixth_note).midi is not None:
                            sixth_midi = pitch.Pitch(sixth_note).midi
                            if sixth_midi >= parameters['range']['sixth_midi']['min'] and sixth_midi <= parameters['range']['sixth_midi']['max']:
                                vl['position'][pos]['sixth']['octaves'].append(sixth_note)
                                vl['position'][pos]['sixth']['midi'].append(sixth_midi)
                    
                    # TODO: actTensions = ()...)

        ### Create combinations on vl ###

        act_chord_pos = -1

        for vl_pos in vl['position']:
            
            act_chord_pos += 1

            # initialize variables
            bass_octaves = ['']
            root_octaves = ['']
            third_octaves = ['']
            seventh_octaves = ['']
            fifth_octaves = ['']
            second_octaves = ['']
            fourth_octaves = ['']
            sixth_octaves = ['']
            #TODO: tensions_octaves = ['']

            # Extract 'bass' and 'third' ... octaves for each chord
            bass_octaves = [x for x in vl_pos['bass']['octaves']]

            if not isInRootPosition:
                root_octaves = [x for x in vl_pos['root']['octaves']]
            
            if not isThirdDoubled:
                third_octaves = [x for x in vl_pos['third']['octaves']]

            if not isSeventhDoubled:
                seventh_octaves = [x for x in vl_pos['seventh']['octaves']]

            if not isFifthDoubled:
                fifth_octaves = [x for x in vl_pos['fifth']['octaves']]

            if not isSecondDoubled:
                second_octaves = [x for x in vl_pos['second']['octaves']]

            if not isFourthDoubled:
                fourth_octaves = [x for x in vl_pos['fourth']['octaves']]

            if not isSixthDoubled:
                sixth_octaves = [x for x in vl_pos['sixth']['octaves']]

            # TODO: tensions_octaves = [...]

            result = ''
            result_scale = ''
            # Calculate cartesian product
            # dur:48B | dur:7B2 | m:7A2
            if (vl_pos['chord_type_id'] == '<037>' and vl_pos['chord_type_descr'] == 'minor triad') or (vl_pos['chord_type_id'] == '<037>' and vl_pos['chord_type_descr'] == 'major triad') or (vl_pos['chord_type_id'] == '<036>' and vl_pos['chord_type_descr'] == 'diminished triad') or (vl_pos['chord_type_id'] == '<048>' and vl_pos['chord_type_descr'] == 'augmented triad'): 
                
                """
                if isInRootPosition:
                    result = list(product(bass_octaves, third_octaves, fifth_octaves))
                    result_scale = list([8,3,5])
                else:
                    result = list(product(bass_octaves, root_octaves, third_octaves, fifth_octaves))
                    result_scale = list([actBassScale,8,3,5])
                """

                result = list(product(bass_octaves, root_octaves, third_octaves, fifth_octaves))
                result_scale = list([bass_scale,8,3,5])

            elif (vl_pos['chord_type_id'] == '<0258>' and vl_pos['chord_type_descr'] == 'dominant seventh chord') or (vl_pos['chord_type_id'] == '<0358>' and vl_pos['chord_type_descr'] == 'minor seventh chord') or (vl_pos['chord_type_id'] == '<0158>' and vl_pos['chord_type_descr'] == 'major seventh chord') or (vl_pos['chord_type_id'] == '<0148>' and vl_pos['chord_type_descr'] == 'minor-augmented tetrachord') :

                if isInRootPosition:
                    result = list(product(bass_octaves, third_octaves, seventh_octaves))
                    result_scale = list([8,3,7])
                else:
                    result = list(product(bass_octaves, root_octaves, third_octaves, seventh_octaves))
                    result_scale = list([actBassScale,8,3,7])

            elif (vl_pos['chord_type_id'] == '<0369>' and vl_pos['chord_type_descr'] == 'diminished seventh chord') or (vl_pos['chord_type_id'] == '<0258>' and vl_pos['chord_type_descr'] == 'half-diminished seventh chord') or (vl_pos['chord_type_id'] == '<0248>' and vl_pos['chord_type_descr'] == 'augmented seventh chord') or (vl_pos['chord_type_id'] == '<0148>' and vl_pos['chord_type_descr'] == 'augmented major tetrachord'):

                if isInRootPosition:
                    result = list(product(bass_octaves, third_octaves, seventh_octaves, fifth_octaves))
                    result_scale = list([8,3,7,5])
                else:
                    result = list(product(bass_octaves, root_octaves, third_octaves, seventh_octaves, fifth_octaves))
                    result_scale = list([actBassScale,8,3,7,5])

            # sus4
            elif (vl_pos['chord_type_extracted'] == 'sus4'):

                if isInRootPosition:
                    result = list(product(bass_octaves, fifth_octaves, fourth_octaves))
                    result_scale = list([8,5,4])
                else:
                    result = list(product(bass_octaves, root_octaves, fifth_octaves, fourth_octaves))
                    result_scale = list([actBassScale,8,5,4])

            # sus2
            elif (vl_pos['chord_type_extracted'] == 'sus2'):
                
                if isInRootPosition:
                    result = list(product(bass_octaves, fifth_octaves, second_octaves))
                    result_scale = list([8,5,2])
                else:
                    result = list(product(bass_octaves, root_octaves, fifth_octaves, second_octaves))
                    result_scale = list([actBassScale,8,5,2])
            # tensions
            elif vl_pos['chord_type_id'] in ['<01358>']:  # m9

                if isInRootPosition:
                    result = list(product(bass_octaves, third_octaves, seventh_octaves, second_octaves))
                    result_scale = list([8,3,7,9])
                else:
                    result = list(product(bass_octaves, root_octaves, third_octaves, seventh_octaves, second_octaves))
                    result_scale = list([actBassScale,8,3,7,9])

            elif vl_pos['chord_type_id'] in ['<024579>']:  #m11

                if isInRootPosition:
                    result = list(product(bass_octaves, third_octaves, seventh_octaves, fourth_octaves))
                    result_scale = list([8,3,7,11])
                else:
                    result = list(product(bass_octaves, root_octaves, third_octaves, seventh_octaves, fourth_octaves))
                    result_scale = list([actBassScale,8,3,7,11])

            elif vl_pos['chord_type_id'] in ['<013568A>']:  #13

                if isInRootPosition:
                    result = list(product(bass_octaves, third_octaves, seventh_octaves, sixth_octaves))
                    result_scale = list([8,3,7,13])
                else:
                    result = list(product(bass_octaves, root_octaves, third_octaves, seventh_octaves, sixth_octaves))
                    result_scale = list([actBassScale,8,3,7,13])

            # TODO: elif vl_pos['chord_type_id'] in ['...']:  #OTHER TENSIONS (remaining notes in chord)

            # iterate all calculated vl-vertical variations
            for vl_result in result:

                result_tuple_midi = []
                for mm in vl_result:
                    if mm != '':
                        result_tuple_midi.append(pitch.Pitch(mm).midi)
                    else:
                        result_tuple_midi.append(-1)

                # create tuples of notes and scale degrees
                result_tuple = tuple(zip(vl_result, result_scale, result_tuple_midi))
                
                # remove empty items containing ''
                result_tuple_clean = tuple(item for item in result_tuple if item[0] != '')

                # Sortiere die Tupel nach den MIDI-Nummern
                result_tuple_ordered = sorted(result_tuple_clean, key=lambda x: x[2])

                # Erstelle eine Liste nur aus den gefilterten und sortierten Notennamen
                note_names = [note[0] for note in result_tuple_ordered]
                s = ' '.join(note_names)
                ch = chord.Chord(s)

                self.ss.append(ch)

                print(ch)

                # check, if bass note is lowest note in the calculated vl-vertical variations. if not, skip this entry.
                bass_check = True
                for nn in vl_result[1:]:
                    if nn != '':
                        if pitch.Pitch(nn).midi < pitch.Pitch(vl_result[0]).midi:
                            bass_check = False
                            print('!INFO:', 'bass check failed (lowest note):', vl_result, 'Skipped that vl-vertical variation for the the list.')
                            break

                # only in case bass note check is OK continue adding entry
                if bass_check:

                    # create new calculated vl-vertical variation item for the dictionary
                    item_vl = {
                        'note_scale': result_tuple_ordered,
                        'assessment': 'e.g.: 10th spacing on top'
                    }

                    # add new item into the dictionary
                    vl['position'][act_chord_pos]['vl'].append(item_vl)

        # OUTPUT RESULT dictionary
        #pprint.pprint(vl['position'][0])
        pprint.pprint(vl['position'])

        self.ss.write('musicxml', fp = 'test_0001.mxl')

        #return pprint.pformat(v1)
        pass

    def transpose_qz(self, qz_start_txt = 'C', transpose_interval = 'p5', iteration_count = 8):
        """ 
        create transpose framework as main dictionary
        input parameter:
        - transpose_interval = 'p5'   # QZ_up::p5 // QZ_down:: -p5
        - iteration_count = 8         # 8::(C--C#) // 8::(C--Cb)
        """
        print('--- START:', 'transpose_qz')

        try:
            qz_start = key.Key(qz_start_txt)
            qz_prev = qz_start

            vl0 = {'qz':[]}

            itm0 = {'qz_id':None, 'qz_name':None, 'position':[]}
            itm0['qz_id'] = 0
            itm0['qz_name'] = qz_start.tonicPitchNameWithCase # .name / qz_start.mode / .tonic / .tonicPitchNameWithCase
            vl0['qz'].append(itm0)
            
            for act_qz_id in range(1, iteration_count):
                itm0 = {'qz_id':None, 'qz_name':None, 'position':[]}
                qz_act = qz_prev.transpose(transpose_interval)
                itm0['qz_id'] = act_qz_id
                itm0['qz_name'] = qz_act.tonicPitchNameWithCase
                vl0['qz'].append(itm0)

                qz_prev = qz_act

            #pprint.pprint(vl0)
                
            print('--- END:', 'transpose_qz')

            return vl0
        
        except Exception as e:
            print("!!! ERROR:", e)
            return None

    def create_position(self, qz_name = 'C'):
        """
        position framework for creating voiceliading options
        """
        print('--- START:', 'create_position')
        try:
            vl = {'placeholder1':qz_name}

            #pprint.pprint(vl)
                
            print('--- END:', 'create_position')

            return vl

        except Exception as e:
            print("!!! ERROR:", e)
            return None

    def vl_get_bass_note(self):
        """
        Methode um die Bassnote (tiefste Note) im Akkord zu identifiziern.
        """
        print('--- START vl_get_bass_note ---')
        # Placeholder for function
        pass

    def vl_get_bass_is_inversion(self):
        """
        Methode um für den spezialfall des voiceleading inversions im Bass zu identifizieren (z.B. C/E --> /3rd.; CMaj7/B --> spezialfall: /7th)
        """
        print('--- START vl_get_bass_is_inversion ---')
        # Placeholder for function
        pass

    def vl_roll_out_notes(self):
        """
        Methode um alle kombinationen der im Akkord enthaltenen noten auszurollenK
        """
        print('--- START vl_roll_out_notes ---')
        # Placeholder for function
        pass

    def vl_get_root_motion(self):
        """
        Methode um die Typen der Bass-Bewegung zwischen zwei Akkorden zu klassifizieren (z.B. QZ/2nd./3rd.).
        """
        print('--- START vl_get_root_motion ---')
        # Placeholder for function
        pass

    def grand_staff_sheet(self):
        """
        Dieser Code erstellt ein Notenblatt mit einem Bass- und einem Violinschlüssel, die für die linke und rechte Hand des Klaviers verwendet werden. Die Noten A1 und A2 werden in der Basslinie für die linke Hand dargestellt, während die Noten A3, C4 und E4 als Akkord in der Violinlinie für die rechte Hand dargestellt werden. Die beiden Notenlinien sind durch eine Akkoladenklammer verbunden.
        """

        p1 = stream.Part()
        p2 = stream.Part()
        p1.clef = clef.TrebleClef()
        p2.clef = clef.BassClef()
        p1.keySignature = key.Key('G')
        p2.keySignature = key.Key('G')
        p1.timeSignature = meter.TimeSignature('3/4')
        p2.timeSignature = meter.TimeSignature('3/4')
        p1.append(note.Note('C5', type='whole'))
        p1.append(note.Note('D5', type='whole'))
        p2.append(note.Note('C3', type='whole'))
        p2.append(chord.Chord('D2 E3 G4'))
        #p3 = stream.Part()
        #p3.append(note.Note('F#4', type='whole'))
        #p3.append(note.Note('G#4', type='whole'))
        #p3.append(chord.Chord('D E G'))
        sp = stream.Score()
        sp.insert(0, p1)
        sp.insert(0, p2)
        #sp.insert(0, p3)
        staffGroup1 = layout.StaffGroup([p1, p2],
            name='Piano', abbreviation='Pno.', symbol='brace')
        staffGroup1.barTogether = 'Mensurstrich'
        sp.insert(0, staffGroup1)
        #staffGroup2 = layout.StaffGroup([p3],
        #    name='Xylophone', abbreviation='Xyl.', symbol='bracket')
        #sp.insert(0, staffGroup2)

        # Write the stream to a MIDI file
        sp.write('midi', fp = 'sheet_0003.mid')

        # Write the stream to a MusicXML file
        sp.write('musicxml', fp = 'sheet_0003.mxl')

### CALL FUNCTIONS SECTION ##

# Define the path to the chordtxt import-file to parse
# You can edit this variable
script_verzeichnis = os.path.dirname(os.path.realpath(__file__))

#file_path = os.path.join(script_verzeichnis, "txt", "02_chord_progressions_for_songwriters","01_ascending_basslines")
#file_path = os.path.join(script_verzeichnis, "txt", "03_reharmonization_techniques","10_basic_piano_voicing_techniques")
file_path = os.path.join(script_verzeichnis, "txt", "02_chord_progressions_for_songwriters","11_chords")

print("file_path:",file_path)

txt_files = []

#### MANUAL INPUT: only selected file processing (instead of batch job)
#txt_files.append("0001.txt")
txt_files.append("0002.txt")
#txt_files.append("0003.txt")

if(len(txt_files)==0):
    ### BATCH JOB: Hole Liste aller .txt-Dateien im angegebenen Ordner für den batch job
    txt_files = [f for f in os.listdir(file_path) if f.endswith('.txt')]

# Iterieren Sie über jede Datei und verarbeiten Sie sie
for file_name in txt_files:
    print()
    print("=== Processing file:", file_name, '===')

    file_title = file_name[:-4]

    file_name_without_extension = os.path.join(file_path, file_title)

    ### CALL FUNCTIONS ###

    cp = ChordProgression(file_title, file_name_without_extension + '.txt', file_name_without_extension + '.mid', file_name_without_extension + '.mxl')

    song = cp.parse_file()

    print('--song:',song)