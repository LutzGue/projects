"""
Python code that uses the music21 library to generate chord progressions in MIDI and MusicXML file formats from a given chord progression in TXT format. The user can transfer chord progressions from books or websites in a simple input format into a txt file. Voice leading possibilities are calculated for the transitions of the chords. The generated MIDI file can be practiced on the piano and expands your playing skills on the instrument. This develops new improvisation skills. The helper tool can be used to create new txt files for entering chord progressions and generate any number of input documents.
"""
from music21 import *
import os
import codecs
import sys
from itertools import product
import pprint

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

    def parse_file(self):
        """
        Parses a song file and extracts metadata and chords.
        
        Parameters:
        fname (str): The path to the song file.
        
        Returns:
        dict: A dictionary containing the song metadata and chords.
        """

        print('--- START parse_file ---')

        #dirname = os.path.dirname(__file__)
        #filename = os.path.join(dirname, fname)

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
        #song["pitches"] = []

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

                        #song["pitches"].append(parse_chord_string(actline))
                    
            # Output schema
            # return song
                        
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

        # set title and composer
        self.s.append(metadata.Metadata(title = self.file_title, composer = 'Menzel, Lutz'))

        # Set the time signature (e.g. 4/4, 3/4, ..)
        self.s.append(meter.TimeSignature(gettimesignature))

        # Set key
        self.s.append(key.Key(getkey))

        # Open the txt file and read the chords
        #with open(self.txt_file, 'r') as f:
            #chords = f.read().splitlines()
            #print('chords:',chords)

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
                'octave':{
                    'min': 1,
                    'max': 5
                },
                'bass_midi':{
                    'min': pitch.Pitch('A1').midi,
                    'max': pitch.Pitch('F#3').midi
                },
                'root_midi':{
                    'min': pitch.Pitch('A1').midi,
                    'max': pitch.Pitch('F#3').midi
                },
                'third_midi':{
                    'min': pitch.Pitch('D3').midi,
                    'max': pitch.Pitch('C5').midi
                },
                'seventh_midi':{
                    'min': pitch.Pitch('D3').midi,
                    'max': pitch.Pitch('C5').midi
                },
                'fifth_midi':{
                    'min': 48,
                    'max': 60
                },
                'sixth_midi':{
                    'min': 48,
                    'max': 60
                },
                'fourth_midi':{
                    'min': 48,
                    'max': 60
                },
                'second_midi':{
                    'min': 48,
                    'max': 60
                },
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

                pos += 1

                actBass = ''
                if element.bass() is not None:
                    actBass = element.bass().name

                actRoot = ''
                if element.root() is not None:
                    actRoot = element.root().name

                actThird = ''
                if element.third is not None:
                    actThird = element.third.name

                actFifth = ''
                if element.fifth is not None:
                    actFifth = element.fifth.name

                actSeventh = ''
                if element.seventh is not None:
                    actSeventh = element.seventh.name

                actSecond = ''
                if element.getChordStep(2) is not None:
                    actSecond = element.getChordStep(2).name

                actFourth = ''
                if element.getChordStep(4) is not None:
                    actFourth = element.getChordStep(4).name

                actSixth = ''
                if element.getChordStep(6) is not None:
                    actSixth = element.getChordStep(6).name

                # GENERATE TENSION LIST (get list of remaining chord-tones)
                # TODO
                    
                normalOrder = element.normalOrder
                firstPitch = normalOrder[0]
                no = [(pc - firstPitch) % 12 for pc in normalOrder]
                yy = chord.Chord.formatVectorString(no)

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
                            'note':None,
                            'octaves':[],
                            'midi':[]
                        }]
                    }

                vl['position'].append(item)

                #chord_list.append(element.root().name)    # e.g.: C/G --> C
                #chord_list.append(element.bass().name)    # e.g.: C/G --> G (Inversion)
                #chord_list.append(actThird)
                #chord_list.append(actFifth)
                #chord_list.append(actSeventh)
                                
                #chord_list.append(element.figure)                  # e.g.: C, Gm, A7
                #chord_list.append(element.pitchedCommonName)
                #chord_list.append(element.primeForm)
                #chord_list.append(element.root().nameWithOctave)    # e.g.: C/G --> C
                #chord_list.append(element.bass().nameWithOctave)    # e.g.: C/G --> G (Inversion)

                # calculate Bass and other notes VL variations in a given range.
                for i in range(parameters['range']['octave']['min'], parameters['range']['octave']['max'] + 1):

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

        ### Create combinations on vl ###

        act_chord_pos = -1

        for vl_pos in vl['position']:
            
            act_chord_pos += 1

            # Extract 'bass' and 'third' ... octaves for each chord
            bass_octaves = [x for x in vl_pos['bass']['octaves']]
            third_octaves = [x for x in vl_pos['third']['octaves']]
            seventh_octaves = [x for x in vl_pos['seventh']['octaves']]
            fifth_octaves = [x for x in vl_pos['fifth']['octaves']]
            second_octaves = [x for x in vl_pos['second']['octaves']]
            fourth_octaves = [x for x in vl_pos['fourth']['octaves']]
            sixth_octaves = [x for x in vl_pos['sixth']['octaves']]

            result = ''
            result_scale = ''
            # Calculate cartesian product
            # dur:48B | dur:7B2 | m:7A2
            if (vl_pos['chord_type_id'] == '<037>' and vl_pos['chord_type_descr'] == 'minor triad') or (vl_pos['chord_type_id'] == '<037>' and vl_pos['chord_type_descr'] == 'major triad') or (vl_pos['chord_type_id'] == '<036>' and vl_pos['chord_type_descr'] == 'diminished triad') or (vl_pos['chord_type_id'] == '<048>' and vl_pos['chord_type_descr'] == 'augmented triad'): 
                result = list(product(bass_octaves, third_octaves, fifth_octaves))
                result_scale = list([8,3,5])

            elif (vl_pos['chord_type_id'] == '<0258>' and vl_pos['chord_type_descr'] == 'dominant seventh chord') or (vl_pos['chord_type_id'] == '<0358>' and vl_pos['chord_type_descr'] == 'minor seventh chord') or (vl_pos['chord_type_id'] == '<0158>' and vl_pos['chord_type_descr'] == 'major seventh chord') or (vl_pos['chord_type_id'] == '<0148>' and vl_pos['chord_type_descr'] == 'minor-augmented tetrachord') :
                result = list(product(bass_octaves, third_octaves, seventh_octaves))
                result_scale = list([8,3,7])

            elif (vl_pos['chord_type_id'] == '<0369>' and vl_pos['chord_type_descr'] == 'diminished seventh chord') or (vl_pos['chord_type_id'] == '<0258>' and vl_pos['chord_type_descr'] == 'half-diminished seventh chord') or (vl_pos['chord_type_id'] == '<0248>' and vl_pos['chord_type_descr'] == 'augmented seventh chord') or (vl_pos['chord_type_id'] == '<0148>' and vl_pos['chord_type_descr'] == 'augmented major tetrachord'):
                result = list(product(bass_octaves, third_octaves, seventh_octaves, fifth_octaves))
                result_scale = list([8,3,7,5])

            # sus4
            elif (vl_pos['chord_type_extracted'] == 'sus4'):
                result = list(product(bass_octaves, fifth_octaves, fourth_octaves))
                result_scale = list([8,5,4])

            # sus2
            elif (vl_pos['chord_type_extracted'] == 'sus2'):
                result = list(product(bass_octaves, fifth_octaves, second_octaves))
                result_scale = list([8,5,2])

            # tensions
            elif vl_pos['chord_type_id'] in ['<01358>']:  # m9
                result = list(product(bass_octaves, third_octaves, seventh_octaves, second_octaves))
            elif vl_pos['chord_type_id'] in ['<024579>']:  #m11
                result = list(product(bass_octaves, third_octaves, seventh_octaves, fourth_octaves))
            elif vl_pos['chord_type_id'] in ['<013568A>']:  #13
                result = list(product(bass_octaves, third_octaves, seventh_octaves, sixth_octaves))

            for vl_result in result:

                item_vl = {
                    'assessment': vl_result,
                    'scale': result_scale,
                    'voice':[{
                        'note': None,
                        'scale': None
                    },
                    {
                        'note': None,
                        'scale': None
                    },
                    {
                        'note': None,
                        'scale': None
                    }
                    ]
                }

                vl['position'][act_chord_pos]['vl'].append(item_vl)

        pprint.pprint(vl)

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

### CALL FUNCTIONS SECTION ###

"""
s = stream.Score()
p1 = stream.Part()
p1.id = 'part1'
p1.append(clef.TrebleClef())
p1.insert(4, note.Note('C#4'))
p1.insert(5.3, note.Rest())
p2 = stream.Part()
p2.id = 'part2'
p2.append(clef.BassClef())
p2.insert(2.12, note.Note('D-4', type='half'))
p2.insert(5.5, note.Rest())
s.insert(0, p1)
s.insert(0, p2)
if not s.isWellFormedNotation():
    print("Die Partitur ist nicht wohlgeformt. Überprüfe die Elemente, Notenwerte und Reihenfolge.")
    print(s.write('musicxml'))
s.show('text', addEndTimes=True)
s.write('musicxml', fp = 'test.mxl')
s.write('midi', fp = 'test.midi')

x = 1

# Füge Metadaten hinzu
#score.metadata = metadata.Metadata()
#score.metadata.title = "Grand Staff Sheet"
#score.metadata.composer = "Lutz"

# Erstelle zwei Systeme (eines für den Violinschlüssel, eines für den Bassschlüssel)
treble_staff = stream.Part()
bass_staff = stream.Part()

# Füge Violinschlüssel- und Bassschlüssel-Stimmen hinzu
treble_clef = clef.TrebleClef()
treble_staff.append(treble_clef)

bass_clef = clef.BassClef()
bass_staff.append(bass_clef)

# Setze Taktart und Tonart
treble_staff.append(meter.TimeSignature('4/4'))
bass_staff.append(meter.TimeSignature('4/4'))
treble_staff.append(key.KeySignature(0))
bass_staff.append(key.KeySignature(0))

# Füge ein paar Noten hinzu (Beispielnoten)
treble_notes = ['C5', 'E5', 'G5', 'B5']
bass_notes = ['C3', 'E3', 'G3', 'B3']

for treble_note, bass_note in zip(treble_notes, bass_notes):
    treble_staff.append(note.Note(treble_note, quarterLength=1))
    bass_staff.append(note.Note(bass_note, quarterLength=1))

# Füge die Stimmen zu den Systemen hinzu
staff_group = layout.StaffGroup([treble_staff, bass_staff])

# Füge die StaffGroup zur Partitur hinzu
score.insert(0, staff_group)

# Überprüfe, ob die Partitur wohlgeformt ist
if not score.isWellFormedNotation():
    print("Die Partitur ist nicht wohlgeformt. Überprüfe die Elemente, Notenwerte und Reihenfolge.")
    print(score.write('musicxml'))

# Konfiguriere das music21-Environment und zeige die Partitur an
#configure.run()
score.show()

# Test call --------------------------------
#cp = ChordProgression('D:\\git-repo\\projects\\chordtxt\\chords.txt')
#cp.generate_chord_progression('output.mid', 'output.xml')
#-------------------------------------------

"""

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

    #generate = cp.generate_chord_progression(song)

    #chord_list = calculate_octaves(song)
    #print('chord_list:',chord_list)

    #print(save_into_file(file_path, file_title, chord_list, song['meter']))
