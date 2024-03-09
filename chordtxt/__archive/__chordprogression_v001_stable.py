"""
generation of chordprogressions, provided in txt files, transposed in keys.
# TODO # BUG # NOTE # FIXME # HACK # XXX
"""
from music21 import *
import os
import codecs
from itertools import product, combinations, groupby
import pprint
import json
import datetime

class ChordProgression:
    """
    """
    def __init__(self, config):
        """
        """
        # imported parameters from config JSON file
        self.config = config

        # Define the path to the chordtxt import-file to parse
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.files = []

        # note sheet
        self.s = stream.Stream()
        self.sheet = stream.Score()

    def start(self):
        """
        """
        # create input-/output filenames
        self.files = ''
        self.files = self.set_files()
        #pprint.pprint(self.files)

        # NOTE: start framework
        res = self.framework()

        pass

    def template(self):
        """
        template generator for blank txt files in user defined project folders.
        """
        template_dateipfad = os.path.join(self.script_path, self.config['template']['filename'])
        zielordner = os.path.join(self.script_path, self.config['template']['target_folder'])
        anzahl_kopien = self.config['template']['copies']

        # Check if input (.txt)-file exists in the specific folder
        if os.path.exists(template_dateipfad):

            with open(template_dateipfad, 'r') as template_datei:
                template_inhalt = template_datei.read()

            for nummer in range(1, anzahl_kopien + 1):
                nummer_formatiert = str(nummer).zfill(4)  # Fügt führende Nullen hinzu, um die Nummer zu formatieren
                zieldatei_pfad = f"{zielordner}\\{self.config['file']['prefix']['txt']}{nummer_formatiert}{self.config['file']['suffix']['txt']}{self.config['file']['extension']['txt']}"

                with open(zieldatei_pfad, 'w') as zieldatei:
                    zieldatei.write(template_inhalt)
        else:
            print(f"!!!Template file {template_dateipfad} not found.")
        pass

    def framework(self):
        """
        iterates through all defined files, transposing chord progressions in user defined keys.
        """
        iteration = 0

        # stage 1: iterate all filenames
        files = ''
        files = self.files
        for file in files:

            txt_filename = file[0]['txt_name']
            txt_title = file[0]['title']
            txt_path = file[0]['path']

            print('')
            print('---', 'title:', txt_title)
            print('---', 'path:', txt_path)
            print('')

            # NOTE: read meta and chordprogressions from current input file (.txt)
            song = ''
            song = self.parse_file(txt_filename)

            ####pprint.pprint(song)

            # stage 2: iterate all transpose keys

            # get transposed keys
            origin_key = song['key']
            keys = self.get_keys(origin_key)
            target_key = keys['qz']

            for act_key in target_key:

                # calculate interval for transposing chords
                act_origin_key = key.Key(origin_key)
                act_target_key = key.Key(act_key['qz_name'])
                act_interval = interval.Interval(act_origin_key.tonic, act_target_key.tonic)

                print('')
                print(origin_key, act_key['qz_name'], act_interval.directedName)
                print('')

                # stage 3: iterate all chords
                chord_id = 0
                chords = ''
                chords = song['chords']
                chord_type = song['chord_type']
                vlv_list = {'position':[]}
                for chord in chords:

                    chord_id += 1

                    # current combination
                    iteration += 1

                    print('')
                    print('---', 'id:', iteration, '| title:', txt_title, '| transpo-key:', act_target_key, '| chord:', chord)
                    print('---', 'path:', txt_path)
                    print('')

                    # transpose current base chord into current qz
                    act_base_chord = harmony.ChordSymbol(chord.strip())
                    act_transposed_chord = act_base_chord.transpose(act_interval)

                    print(act_base_chord.root().name, act_transposed_chord.root().name)
                    print(act_base_chord.figure, act_transposed_chord.figure)

                    #c.writeAsChord = True
                    #z = self.extract_chordtype(chord)

                    act_chord_type = song['chord_type'][chord_id - 1]

                    # NOTE: voice leading vertical
                    vlv = self.voice_leading_vertical(act_transposed_chord, act_chord_type)
                    vlv_list['position'].append(vlv)

                    ### FINAL LIST of vlv ###
                    ###pprint.pprint(vlv)



                # voice leading horizontal
                # vlh = self.voice_leading_horizontal('x','y')

                #NOTE: generate all voice leading VERTICAL and analyze interval matrix and write grand sheet into mxl and mid file.
                self.grand_staff_sheet_vlv(vlv_list, act_key['qz_name'])

                #NOTE: generate all voice leading HORIZONTAL and analyze interval matrix and write grand sheet into mxl and mid files.
                ### self.grand_staff_sheet_vlh(vlv_list, act_key['qz_name'])

        self.writefile()

        pass

    def set_files(self):
        """
        """
        file_path = os.path.join(self.script_path, self.config['file']['source_folder'])
        txt_files = self.config['file']['source_files']

        # init result list for files
        file_list = []

        # check if specific path was provided by user
        if file_path != '':

            # in case no file manually was provided by user, get a list of all files in the specific folder
            if(len(txt_files)==0):
                ### BATCH JOB: Hole Liste aller .txt-Dateien im angegebenen Ordner für den batch job
                txt_files = [f for f in os.listdir(file_path) if f.endswith(self.config['file']['extension']['txt'])]

            # Iterieren Sie über jede Datei und verarbeiten Sie sie
            for file in txt_files:
                
                file_title = file[:-4]
                
                # input file name (.txt)
                file_name_txt = os.path.join(file_path, file)
                
                # output file names
                file_name_mid = os.path.join(file_path, self.config['file']['prefix']['midi'] 
                                             + file_title 
                                             + self.config['file']['suffix']['midi'] 
                                             + self.config['file']['extension']['midi'])
                file_name_mxl = os.path.join(file_path, self.config['file']['prefix']['musicxml'] 
                                             + file_title 
                                             + self.config['file']['suffix']['musicxml'] 
                                             + self.config['file']['extension']['musicxml'])
                file_name_rom = os.path.join(file_path, self.config['file']['prefix']['roman'] 
                                             + file_title 
                                             + self.config['file']['suffix']['roman'] 
                                             + self.config['file']['extension']['roman'])

                # Check if input (.txt)-file exists in the specific folder
                if os.path.exists(file_name_txt):

                    item = [{
                        'path':file_path,
                        'title':file_title,
                        'txt_name':file_name_txt,
                        'mid_name':file_name_mid,
                        'mxl_name':file_name_mxl,
                        'rom_name':file_name_rom    # roman numeral file-type
                        },     
                    ]

                    file_list.append(item)

                    file_name_without_extension = os.path.join(file_path, file_title)
                else:
                    print(f"!!!File {file_name_txt} not found.")
        else:
            print(f"!!!No Folder specified.")
        
        return file_list

    def voice_leading_vertical(self, act_chord, chord_type):
        print('vlv:', act_chord, chord_type)

        # NOTE: define the range of generated octaves and midi note ids for each voice note.
        parameters = {
            'range':{
                # global range for vl-vertical generation (min:1;max:5)
                'octave':{
                    'min': 1,
                    'max': 5
                },
                # TODO: LIMIT the interval range of each chord vlv. This reduces computation time IN ADVANCE ("pre") of vlh combinations (NOTE: bad defined range can cause empty vlv for chords!)
                'interval_pre_limiter':{
                    'max': 30,
                    'min': 0
                },
                # interval range of each chord vlv. This interval is used for calculation KPI in vlh ("post") (NOTE: bad defined range can cause empty vlv for chords!)
                'interval':{
                    'max': 20,
                    'min': 0
                },
                # TODO: smooth Soprano line
                'soprano':{
                    'max':'5',
                    'min':'0',
                    'force': False
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
                    'min': pitch.Pitch('D3').midi,
                    'max': pitch.Pitch('C5').midi
                },
                # add 6 = T13 (e.g. "Cm13")
                'sixth_midi':{
                    'min': pitch.Pitch('D3').midi,
                    'max': pitch.Pitch('C5').midi
                },
                # 6-chord (instead of 5) (e.g.: "C6")
                'sixth_chord_midi':{
                    'min': pitch.Pitch('D3').midi,
                    'max': pitch.Pitch('C5').midi
                },
                # add 4 = T11 (e.g. "Cm11")
                'fourth_midi':{
                    'min': pitch.Pitch('D3').midi,
                    'max': pitch.Pitch('C5').midi
                },
                # sus4 (instead of third) (e.g. "Csus4")
                'sus4_chord_midi':{
                    'min': pitch.Pitch('D3').midi,
                    'max': pitch.Pitch('C5').midi
                },
                # add 2 = T9 (e.g.: "C9", "C/D")
                'second_midi':{
                    'min': pitch.Pitch('D3').midi,
                    'max': pitch.Pitch('C5').midi
                },
                # sus2 (instead of third) (e.g. "Csus2")
                'sus2_chord_midi':{
                    'min': pitch.Pitch('D3').midi,
                    'max': pitch.Pitch('C5').midi
                },
                # OTHERS (Tensions) (e.g.: TBD.)
                'tension_midi':{
                    'min': pitch.Pitch('D3').midi,
                    'max': pitch.Pitch('C5').midi
                }
            }
        }

        ### initial output dictionary for calculated voiceleading options. ###

        #---------------------------
        """
        # create dictionary framework for transposing (iterations in intervals using start key)
        vl0 = self.transpose_qz('C', 'p5', 8)
        
        for act_qz in vl0['qz']:
            
            # calculate all possible voice leadings options for the chords in the current transposed key
            tmp = self.create_position(act_qz['qz_name'])

            # add positions into main dictionary framework for all transposed keys and loop again
            vl0['qz'][act_qz['qz_id']]['position'].append(tmp)

        # output final dictionary containing all transposed chords in all voice leadings
        pprint.pprint(vl0)
        """
        #---------------------------

        #vl = {'position':[]}

        chord_notes = act_chord.pitchNames
        found_chord_notes = []

        # bass
        actBass = ''
        if act_chord.bass() is not None:
            actBass = act_chord.bass().name
            actBassScale = -1   # placeholder value; TODO: calculate scale degree for bassnote (in case of inversion)
            found_chord_notes.append(actBass)

        # root
        actRoot = ''
        if act_chord.root() is not None:
            actRoot = act_chord.root().name
            found_chord_notes.append(actRoot)

        # 3rd.
        actThird = ''
        if act_chord.third is not None:
            actThird = act_chord.third.name
            found_chord_notes.append(actThird)

        # 5th.
        actFifth = ''
        if act_chord.fifth is not None:
            actFifth = act_chord.fifth.name
            found_chord_notes.append(actFifth)

        # 7th.
        actSeventh = ''
        if act_chord.seventh is not None:
            actSeventh = act_chord.seventh.name
            found_chord_notes.append(actSeventh)

        # sus2-chord / add2 = T9
        actSecond = ''
        if act_chord.getChordStep(2) is not None:
            actSecond = act_chord.getChordStep(2).name
            found_chord_notes.append(actSecond)

        # sus4-chord / add4 = T11
        actFourth = ''
        if act_chord.getChordStep(4) is not None:
            actFourth = act_chord.getChordStep(4).name
            found_chord_notes.append(actFourth)

        # 6-chord / add6 = T13
        actSixth = ''
        if act_chord.getChordStep(6) is not None:
            actSixth = act_chord.getChordStep(6).name
            found_chord_notes.append(actSixth)

        # GENERATE TENSION LIST (get list of remaining (not mapped) chord-tones)
        # e.g.: "B7add#15" --> T#15:"B#"
        print(found_chord_notes)
        print(chord_notes)
        
        tension_notes = []
        tension_notes = [note for note in chord_notes if note not in found_chord_notes]
        
        # check, if all notes are mapped to the scale
        if len(tension_notes) != 0:
            print('!INFO: There are notes that are NOT mapped and added to remaining tension list:', tension_notes)

        # ------------------
            
        normalOrder = act_chord.normalOrder
        firstPitch = normalOrder[0]
        no = [(pc - firstPitch) % 12 for pc in normalOrder]

        vl = {
                'chord_type_extracted': chord_type,
                'chord_name': act_chord.figure,
                'inversion_nr': act_chord.inversion(),
                'chord_type_descr': act_chord.commonName,
                'chord_quality': act_chord.quality,
                'chord_type_id': act_chord.primeFormString,
                'normal_order': act_chord.normalOrderString, ###
                'normal_order_0': no, ###
                'forte_class': act_chord.forteClass, ###
                'interval_vector': act_chord.intervalVectorString,
                'geometric': act_chord.geometricNormalForm(),
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

        #vl['position'].append(item)

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
                        vl['bass']['octaves'].append(bass_note)
                        vl['bass']['midi'].append(bass_midi)

            if actRoot != '':
                root_note = actRoot + str(i)
                if pitch.Pitch(root_note).midi is not None:
                    root_midi = pitch.Pitch(root_note).midi
                    if root_midi >= parameters['range']['root_midi']['min'] and root_midi <= parameters['range']['root_midi']['max']:
                        vl['root']['octaves'].append(root_note)
                        vl['root']['midi'].append(root_midi)

            if actThird != '':
                third_note = actThird + str(i)
                if pitch.Pitch(third_note).midi is not None:
                    third_midi = pitch.Pitch(third_note).midi
                    if third_midi >= parameters['range']['third_midi']['min'] and third_midi <= parameters['range']['third_midi']['max']:
                        vl['third']['octaves'].append(third_note)
                        vl['third']['midi'].append(third_midi)

            if actSeventh != '':
                seventh_note = actSeventh + str(i)
                if pitch.Pitch(seventh_note).midi is not None:
                    seventh_midi = pitch.Pitch(seventh_note).midi
                    if seventh_midi >= parameters['range']['seventh_midi']['min'] and seventh_midi <= parameters['range']['seventh_midi']['max']:
                        vl['seventh']['octaves'].append(seventh_note)
                        vl['seventh']['midi'].append(seventh_midi)

            if actFifth != '':
                fifth_note = actFifth + str(i)
                if pitch.Pitch(fifth_note).midi is not None:
                    fifth_midi = pitch.Pitch(fifth_note).midi
                    if fifth_midi >= parameters['range']['fifth_midi']['min'] and fifth_midi <= parameters['range']['fifth_midi']['max']:
                        vl['fifth']['octaves'].append(fifth_note)
                        vl['fifth']['midi'].append(fifth_midi)

            if actSecond != '':
                second_note = actSecond + str(i)
                if pitch.Pitch(second_note).midi is not None:
                    second_midi = pitch.Pitch(second_note).midi
                    if second_midi >= parameters['range']['second_midi']['min'] and second_midi <= parameters['range']['second_midi']['max']:
                        vl['second']['octaves'].append(second_note)
                        vl['second']['midi'].append(second_midi)

            if actFourth != '':
                fourth_note = actFourth + str(i)
                if pitch.Pitch(fourth_note).midi is not None:
                    fourth_midi = pitch.Pitch(fourth_note).midi
                    if fourth_midi >= parameters['range']['fourth_midi']['min'] and fourth_midi <= parameters['range']['fourth_midi']['max']:
                        vl['fourth']['octaves'].append(fourth_note)
                        vl['fourth']['midi'].append(fourth_midi)

            if actSixth != '':
                sixth_note = actSixth + str(i)
                if pitch.Pitch(sixth_note).midi is not None:
                    sixth_midi = pitch.Pitch(sixth_note).midi
                    if sixth_midi >= parameters['range']['sixth_midi']['min'] and sixth_midi <= parameters['range']['sixth_midi']['max']:
                        vl['sixth']['octaves'].append(sixth_note)
                        vl['sixth']['midi'].append(sixth_midi)
            
            # TODO: actTensions = ()...)

        ### Create combinations on vl ###

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
        bass_octaves = [x for x in vl['bass']['octaves']]

        if not isInRootPosition:
            root_octaves = [x for x in vl['root']['octaves']]
        
        if not isThirdDoubled:
            third_octaves = [x for x in vl['third']['octaves']]

        if not isSeventhDoubled:
            seventh_octaves = [x for x in vl['seventh']['octaves']]

        if not isFifthDoubled:
            fifth_octaves = [x for x in vl['fifth']['octaves']]

        if not isSecondDoubled:
            second_octaves = [x for x in vl['second']['octaves']]

        if not isFourthDoubled:
            fourth_octaves = [x for x in vl['fourth']['octaves']]

        if not isSixthDoubled:
            sixth_octaves = [x for x in vl['sixth']['octaves']]

        # TODO: tensions_octaves = [...]

        result = ''
        result_scale = ''
        # Calculate cartesian product
        # dur:48B | dur:7B2 | m:7A2
        if (vl['chord_type_id'] == '<037>' and vl['chord_type_descr'] == 'minor triad') or (vl['chord_type_id'] == '<037>' and vl['chord_type_descr'] == 'major triad') or (vl['chord_type_id'] == '<036>' and vl['chord_type_descr'] == 'diminished triad') or (vl['chord_type_id'] == '<048>' and vl['chord_type_descr'] == 'augmented triad'): 
            
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

        elif (vl['chord_type_id'] == '<0258>' and vl['chord_type_descr'] == 'dominant seventh chord') or (vl['chord_type_id'] == '<0358>' and vl['chord_type_descr'] == 'minor seventh chord') or (vl['chord_type_id'] == '<0158>' and vl['chord_type_descr'] == 'major seventh chord') or (vl['chord_type_id'] == '<0148>' and vl['chord_type_descr'] == 'minor-augmented tetrachord') :

            if isInRootPosition:
                result = list(product(bass_octaves, third_octaves, seventh_octaves))
                result_scale = list([8,3,7])
            else:
                result = list(product(bass_octaves, root_octaves, third_octaves, seventh_octaves))
                result_scale = list([actBassScale,8,3,7])

        elif (vl['chord_type_id'] == '<0369>' and vl['chord_type_descr'] == 'diminished seventh chord') or (vl['chord_type_id'] == '<0258>' and vl['chord_type_descr'] == 'half-diminished seventh chord') or (vl['chord_type_id'] == '<0248>' and vl['chord_type_descr'] == 'augmented seventh chord') or (vl['chord_type_id'] == '<0148>' and vl['chord_type_descr'] == 'augmented major tetrachord'):

            if isInRootPosition:
                result = list(product(bass_octaves, third_octaves, seventh_octaves, fifth_octaves))
                result_scale = list([8,3,7,5])
            else:
                result = list(product(bass_octaves, root_octaves, third_octaves, seventh_octaves, fifth_octaves))
                result_scale = list([actBassScale,8,3,7,5])

        # sus4
        elif (vl['chord_type_extracted'] == 'sus4'):

            if isInRootPosition:
                result = list(product(bass_octaves, fifth_octaves, fourth_octaves))
                result_scale = list([8,5,4])
            else:
                result = list(product(bass_octaves, root_octaves, fifth_octaves, fourth_octaves))
                result_scale = list([actBassScale,8,5,4])

        # sus2
        elif (vl['chord_type_extracted'] == 'sus2'):
            
            if isInRootPosition:
                result = list(product(bass_octaves, fifth_octaves, second_octaves))
                result_scale = list([8,5,2])
            else:
                result = list(product(bass_octaves, root_octaves, fifth_octaves, second_octaves))
                result_scale = list([actBassScale,8,5,2])
        # tensions
        elif vl['chord_type_id'] in ['<01358>']:  # m9

            if isInRootPosition:
                result = list(product(bass_octaves, third_octaves, seventh_octaves, second_octaves))
                result_scale = list([8,3,7,9])
            else:
                result = list(product(bass_octaves, root_octaves, third_octaves, seventh_octaves, second_octaves))
                result_scale = list([actBassScale,8,3,7,9])

        elif vl['chord_type_id'] in ['<024579>']:  #m11

            if isInRootPosition:
                result = list(product(bass_octaves, third_octaves, seventh_octaves, fourth_octaves))
                result_scale = list([8,3,7,11])
            else:
                result = list(product(bass_octaves, root_octaves, third_octaves, seventh_octaves, fourth_octaves))
                result_scale = list([actBassScale,8,3,7,11])

        elif vl['chord_type_id'] in ['<013568A>']:  #13

            if isInRootPosition:
                result = list(product(bass_octaves, third_octaves, seventh_octaves, sixth_octaves))
                result_scale = list([8,3,7,13])
            else:
                result = list(product(bass_octaves, root_octaves, third_octaves, seventh_octaves, sixth_octaves))
                result_scale = list([actBassScale,8,3,7,13])
        else:
            print("!!! Unknown chord type:", vl['chord_type_extracted'], "No combinations processed.")

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

            #self.ss.append(ch)

            #print(ch)

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
                    'basic_chord_sound': True,
                    'extended_chord_sound': False,
                    'assessment': '',
                    'max_semitones': '',
                    'min_semitones': '',
                    'is_in_max_range': None,
                    'is_in_min_range': None,
                    'chord_list': ch
                }

                # get interval matrix
                act_assessment_item = self.analyze_chord_intervals(item_vl)
                
                if act_assessment_item['status'] == True:
                    item_vl['assessment'] = act_assessment_item['analyze']

                    # get max interval
                    max_semitone = max(
                        act_assessment_item['analyze'], 
                        key=lambda x: x['interval_semitones']
                    )
                    item_vl['max_semitones'] = max_semitone
                    item_vl['is_in_max_range'] = (max_semitone['interval_semitones'] <= parameters['range']['interval']['max'])

                    # get min interval
                    min_semitone = min(
                        act_assessment_item['analyze'], 
                        key=lambda x: x['interval_semitones']
                    )
                    item_vl['min_semitones'] = min_semitone
                    item_vl['is_in_min_range'] = (min_semitone['interval_semitones'] >= parameters['range']['interval']['min'])

                    # add new item into the dictionary
                    vl['vl'].append(item_vl)
                else:
                    print('!!!', 'analyze_chord_intervals not processed all data.')

        # OUTPUT RESULT dictionary
        #pprint.pprint(vl['position'][0])
        #pprint.pprint(vl)

        #self.ss.write('musicxml', fp = 'test_0001.mxl')

        return vl
    
    def voice_leading_horizontal(self, vl_from, vl_to):
        print('vlh:')
        pass

    def get_keys(self, qz_start_txt):
        """ 
        """
        iteration_count = self.config['transpose']['iterations']
        transpose_interval = self.config['transpose']['interval']

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

            return vl0
        
        except Exception as e:
            print("!!! ERROR:", e)
            return None

    def write_file(self):
        pass

    def analyze_chord_intervals(self, vlv):
        """
        Analyzing vertical voiceleading interval structure of the chord.
        """
        result = {
            'analyze':[],
            'status':False
        }

        # Extrahiere die Notennamen aus der Liste
        note_names = [note[0] for note in vlv['note_scale']]

        # Erzeuge alle möglichen Paare von Noten
        note_pairs = list(combinations(note_names, 2))

        # Drucke die Paare
        for pair in note_pairs:

            act_interval = interval.Interval(pitch.Pitch(pair[0]), pitch.Pitch(pair[1]))

            #print(f'{pair[0]},{pair[1]},{act_interval}')

            item = {
                'txt': '(' + pair[0] + ' ' + pair[1] + '):' + act_interval.name + '/' + act_interval.semiSimpleName,
                'from': pair[0],
                'to': pair[1],
                'interval1': act_interval.name,
                'interval2':  act_interval.semiSimpleName,
                'interval_semitones': act_interval.semitones
            }

            result['analyze'].append(item)

        result['status'] = True

        #pprint.pprint(result)

        return result

    def parse_file(self, filename):

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
        song["chord_type"] = []
        song["roman"] = []
        song["roman_base"] = []

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

                        # parse chord-type
                        act_chord_type = self.extract_chordtype(actline)
                        song["chord_type"].append(act_chord_type)

                        # map roman numerals
                        act_roman = roman.romanNumeralFromChord(harmony.ChordSymbol(actline), key.Key(song['key']), preferSecondaryDominants=True)
                        song["roman"].append(act_roman.figure)
                        song["roman_base"].append(act_roman.romanNumeralAlone)
            
            # The parsed output song needs to contain 11 lines to be well-processed.
            check_song = len(song)
            check_song_pos = len(song["pos"])
            check_song_chords = len(song["chords"])

            if check_song > 10 and check_song_pos > 0 and check_song_chords > 0:
                #print('STATUS: parse_file was SUCCESSFULL. Song contains', check_song, 'lines /', check_song_pos, check_song_chords, 'chords.')
                return song

            else:
                print('STATUS: parse_file with ERROR. Song contains', check_song, 'lines /', check_song_pos, check_song_chords, 'chords.')
                return None
        
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return None
        
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            return None
        
    def extract_chordtype(self, getfullchordname):
        """
        Der Grundton wird identifiziert und entfernt. Dann werden '#' und '-' Zeichen vom verbleibenden Teil des Akkords entfernt. Schließlich wird alles nach dem Schrägstrich-Zeichen für den Akkordtyp entfernt.
        """
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

            return akkordtyp
        
        except Exception as e:
            print("!!! ERROR:", e)
            return None
        
    def grand_staff_sheet_vlv(self, vlv_list, get_key = 'C', force_interval_range = True):
        """
        Dieser Code erstellt ein Notenblatt mit einem Bass- und einem Violinschlüssel, die für die linke und rechte Hand des Klaviers verwendet werden. Die Noten A1 und A2 werden in der Basslinie für die linke Hand dargestellt, während die Noten A3, C4 und E4 als Akkord in der Violinlinie für die rechte Hand dargestellt werden. Die beiden Notenlinien sind durch eine Akkoladenklammer verbunden.
        """
        p1 = stream.Part()
        p2 = stream.Part()

        p1.append(tempo.MetronomeMark(number=60))

        p1.clef = clef.TrebleClef()
        p2.clef = clef.BassClef()
        
        p1.keySignature = key.Key(get_key)
        p2.keySignature = key.Key(get_key)

        p1.timeSignature = meter.TimeSignature('4/4')
        p2.timeSignature = meter.TimeSignature('4/4')

        for act_vlv_pos in vlv_list['position']:

            for act_vlv in act_vlv_pos['vl']:

                if not force_interval_range or (force_interval_range and act_vlv['is_in_max_range'] and act_vlv['is_in_min_range']):

                    msg_interval_check_max = ''
                    msg_interval_check_min = ''
                    if not act_vlv['is_in_max_range']:
                        msg_interval_check_max = '\ntoo high'          
                    if not act_vlv['is_in_min_range']:
                        msg_interval_check_min = '\ntoo low'   

                    act_vlh_chord = act_vlv['chord_list']
                    c = chord.Chord(act_vlh_chord)

                    act_msg = ''
                    for j in act_vlv['assessment']:
                        act_msg = act_msg + '\n' + j['txt']

                    c.lyric = act_vlv_pos['chord_name'].replace('-','b')  + '\n' + roman.romanNumeralFromChord(harmony.ChordSymbol(act_vlv_pos['chord_name']), key.Key(get_key), preferSecondaryDominants=True).figure + act_msg  + msg_interval_check_max  + msg_interval_check_min

                    ####print(act_vlh_chord)
                    
                    p2.append(c)
            
        
        
        sp = stream.Score()
        sp.insert(0, p1)
        sp.insert(0, p2)

        #sp.insert(3.0, layout.SystemLayout())

        #sp.insert(0, p3)
        staffGroup1 = layout.StaffGroup([p1, p2],
            name='Piano', abbreviation='Pno.', symbol='brace')
        staffGroup1.barTogether = 'Mensurstrich'
        sp.insert(0, staffGroup1)

        tmsp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        act_store_filename = 'generated_sheet_vlv_' + tmsp

        # Write the stream to a MIDI file
        sp.write('midi', fp = act_store_filename + '.mid')

        # Write the stream to a MusicXML file
        sp.write('musicxml', fp = act_store_filename + '_' + get_key +'_' + '.mxl')

        # pianoroll
        #sp.plot('pianoroll')

    def grand_staff_sheet_vlh(self, vlv_list, get_key = 'C', limit_result = 100000, force_interval_range = True, force_common_notes = False, use_second_best_common_notes = False):
        """
        Dieser Code erstellt ein Notenblatt mit einem Bass- und einem Violinschlüssel, die für die linke und rechte Hand des Klaviers verwendet werden. Die Noten A1 und A2 werden in der Basslinie für die linke Hand dargestellt, während die Noten A3, C4 und E4 als Akkord in der Violinlinie für die rechte Hand dargestellt werden. Die beiden Notenlinien sind durch eine Akkoladenklammer verbunden.
        """
        p1 = stream.Part()
        p2 = stream.Part()

        p1.append(tempo.MetronomeMark(number=60))

        p1.clef = clef.TrebleClef()
        p2.clef = clef.BassClef()
        
        p1.keySignature = key.Key(get_key)
        p2.keySignature = key.Key(get_key)

        p1.timeSignature = meter.TimeSignature('4/4')
        p2.timeSignature = meter.TimeSignature('4/4')

        #print(len(vlv_list['position']))
              
        result = []
        act_pos_id = 0
        for act_pos in vlv_list['position']:
            act_pos_id += 1

            act_vlv_id = 0
            for act_vlv in act_pos['vl']:

                if not force_interval_range or (force_interval_range and act_vlv['is_in_max_range'] and act_vlv['is_in_min_range']):

                    msg_interval_check_max = ''
                    msg_interval_check_min = ''
                    if not act_vlv['is_in_max_range']:
                        msg_interval_check_max = '\ntoo high'          
                    if not act_vlv['is_in_min_range']:
                        msg_interval_check_min = '\ntoo low'   

                    act_vlv_id += 1
                    result.append((act_pos_id, act_vlv_id, act_vlv['chord_list']))

        # Gruppieren Sie die Elemente in 'txt' nach ihrer Position (erste Spalte)
        grouped_txt = [list(g) for k, g in groupby(result, lambda x: x[0])]

        # Erzeugen Sie alle Kombinationen
        combinations = list(product(*grouped_txt))

        ###############################################################
        ### ITERATE ALL COMBINATIONS (n-LIMITED results for safety) ###
        ###############################################################

        vlh_list = {'header':None, 'position':[]}
        act_vlh_id = 0

        min_common_notes = 99999    # statistics for total min
        max_common_notes = 0        # statistics for total max
        
        for combo in combinations[:limit_result]:
            act_vlh_id += 1

            # add separator between each vlh blocks
            #if act_vlh_id > 1:
            #    rest = note.Rest(quarterLength=1)
            #    p2.append(rest)

            # vlh block
            #print(combo)      

            # ANALYZING vlh
            #print(f'\n### ANALYZING vlh ###')
            combo_from = ''
            combo_to = ''
            common_notes_count = 0
            common_notes_count_total = 0
            if force_common_notes:
                for y in range(0, len(combo) - 1):
                    combo_from = chord.Chord(combo[y][2]).pitches
                    combo_to = chord.Chord(combo[y + 1][2]).pitches
                    #print(f'from: {combo_from}\nto: {combo_to}')

                    ### Analyzing COMMON NOTES ###
                    """
                    Gemeinsamen Elemente aus zwei Listen identifizieren und in eine neue Liste schreiben.
                    """
                    # Identifizieren gemeinsame Elemente
                    result_common_notes = tuple(set(combo_from) & set(combo_to))
                    common_notes_count = len(result_common_notes)
                    common_notes_count_total += common_notes_count

                    item1 = {'common_notes_item':{
                            'notes': result_common_notes,
                            'count': common_notes_count
                        }
                    }
                    #print(f'item1: {item1}')
                    
                    # TODO: Analyzing horizontl INTERVAL vector

                    # TODO: avoid large steps in soprano S

                    # TODO: in case 0 common vlh --> contrary motion S--B


                item2 = {'count': common_notes_count_total,
                    'vlh':combo
                }
                #print(f'item2: {item2}')
                vlh_list['position'].append(item2)

                # calculate statistics for min max
                if min_common_notes > common_notes_count_total:
                    min_common_notes = common_notes_count_total
                if max_common_notes < common_notes_count_total:
                    max_common_notes = common_notes_count_total


            #for x in combo:
                #print('xxx',chord.Chord(x[2]))

                #vlh_chord_list.append(item)
                ####p2.append(chord.Chord(x[2]))
                
                #c.lyric = act_vlh_id

        item3 = {
            'generated':act_vlh_id,     # amount of possible voice leading horizontal variations.
            'min':min_common_notes,     # minimum common notes for sorting descending ranking.
            'max':max_common_notes,     # maximum common notes for sorting descending ranking.
            'key':get_key
        }
        #print(f'item3: {item3}\n')
        vlh_list['header'] = item3
        
        #print(f'-- Generated {act_vlh_id} HORIZONTAL voice leadings in the Key of {get_key}, limit: {limit_result}), min: {min_common_notes}, max:{max_common_notes}.')

        ########################
        ### GENERATING SHEET ###
        ########################

        pprint.pprint(vlh_list['header'])

        counter = 0
        get_max = vlh_list['header']['max']

        # 2nd best common note for strict all common notes
        range_common_notes = 0
        if force_common_notes:
            if use_second_best_common_notes and (get_max > 1):
                range_common_notes = (get_max - 1)
            else:
                range_common_notes = get_max

        print(f"--force_common_notes: {force_common_notes}, 2nd_best: {use_second_best_common_notes}, range_common_notes: {range_common_notes}, get_max: {get_max}, ")
        
        # generate
        for x in vlh_list['position']:

            if x['count'] >= range_common_notes:

                counter += 1

                # add chord progression into lead sheet
                for z in x['vlh']:
                    p2.append(chord.Chord(z[2]))
                    #c.lyric = act_vlh_id
                
                # insert a separator after each block
                rest = note.Rest(quarterLength=1)
                p2.append(rest)

        print(f'--sheet vlh count: {counter}')

        sp = stream.Score()
        sp.insert(0, p1)
        sp.insert(0, p2)
        #sp.insert(0, p3)
        staffGroup1 = layout.StaffGroup([p1, p2],
            name='Piano', abbreviation='Pno.', symbol='brace')
        staffGroup1.barTogether = 'Mensurstrich'
        sp.insert(0, staffGroup1)

        tmsp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        act_store_filename = 'generated_sheet_vlh_' + get_key + '_' + str(counter) + '_' + tmsp

        # Write the stream to a MIDI file
        sp.write('midi', fp = act_store_filename + '.mid')

        # Write the stream to a MusicXML file
        sp.write('musicxml', fp = act_store_filename + '.mxl')

        # pianoroll
        #sp.plot('pianoroll')

    def writefile(self):        
        pass

### CALL FUNCTIONS ###
    
# import config JSON
with open('D:\git-repo\projects\chordtxt\config.json', 'r') as file:
    data = json.load(file)

config = data['data']
#pprint.pprint(config)

# create class
cp = ChordProgression(config)

# create templates
#cp.template()

# process start
cp.start()