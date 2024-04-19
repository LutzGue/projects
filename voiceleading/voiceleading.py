import os
import json
from music21 import *
import yaml
#import itertools
from itertools import product,chain
from collections import Counter

class Config:
    """
    Get config data from (config.json) file.
    """
    def __init__(self):
        pass

    def load(self, get_file_name = ''):
        """
        Read data from config file.
        """
        try:
            print(f'get_file_name: ({get_file_name}).')

            # Check if valid (not empty) filename is provided.
            if get_file_name == '':
                raise ValueError("No filename provided. Please provide a filename.")

            # Check if file exists.
            if not os.path.exists(get_file_name):
                raise ValueError("Provided filename (" + get_file_name + ") does not exist. Please provide existing filename.")

            # Loading rows from (existing) config.json file.
            with open(config_file_name, 'r') as file:
                json_data = json.load(file)

            if json_data == '':
                raise ValueError('Config data in the provided file (' + get_file_name + ') is empty. Please provide config informations in the config file.')

            config_data = json_data['data']

            if config_data == '':
                raise ValueError('Config data in the provided file (' + get_file_name + ') in the section (data) is empty. Please provide config informations in the section (data) of the config file.')

            return True, config_data

        except ValueError as ve:
            print(ve)  # Ausgabe der Fehlermeldung
            return False, ve

class Rule:
    """
    Get rule data from (rule.yaml) file.
    """
    def __init__(self):
        pass

    def load(self, get_file_name = ''):
        """
        Read data from config file.
        """
        try:
            print(f'get_file_name: ({get_file_name}).')

            # Check if valid (not empty) filename is provided.
            if get_file_name == '':
                raise ValueError("No filename provided. Please provide a filename.")

            # Check if file exists.
            if not os.path.exists(get_file_name):
                raise ValueError("Provided filename (" + get_file_name + ") does not exist. Please provide existing filename.")

            # Loading rows from (existing) rule.yaml file.
            with open(get_file_name, 'r') as datei:
                json_data = yaml.load(datei, Loader=yaml.FullLoader)

            if json_data == '':
                raise ValueError('Config data in the provided file (' + get_file_name + ') is empty. Please provide config informations in the config file.')

            return True, json_data

        except ValueError as ve:
            print(ve)  # Ausgabe der Fehlermeldung
            return False, ve

class Parser:
    """
    Opens a file and parses elements (meta: key / chords / roman numerals).
    """
    def __init__(self):
        pass

    def load(self, get_file_name = ''):
        """
        Read data from file.
        """
        try:
            print(f'get_file_name: ({get_file_name}).')

            # Check if valid (not empty) filename is provided.
            if get_file_name == '':
                raise ValueError("No filename provided. Please provide a filename.")

            # Check if the provided filename is a full file path
            if not os.path.isfile(get_file_name):
                raise FileNotFoundError("Provided filename (" + get_file_name + ") does not exist. Please provide existing filename.")

            # Loading rows from (existing) file.
            data = self.parse(get_file_name)

            if data == '':
                raise ValueError("ERR: Parsed file to JSON format contains no data.")

            return True, data

        except (ValueError, FileNotFoundError) as e:
            print(e)  # Ausgabe der Fehlermeldung
            return False, e

    def validate(self):
        # 
        pass

    def parse(self, get_file_name):
        """
        Convert text content into JSON format.
        """
        try:
            # init json variable
            data = {
                "meta": {}, 
                "position": []
                }
            
            header = []
            
            # Open file and read text content.
            with open(get_file_name, 'r') as file:
                lines = file.readlines()
                
                # Parsing meta information.
                data["meta"]["title"] = lines[0].strip()
                data["meta"]["author"] = lines[1].strip()
                data["meta"]["created_date"] = lines[2].strip()
                data["meta"]["version_updated"] = lines[3].strip()
                data["meta"]["key"] = lines[4].strip()
                data["meta"]["bpm"] = lines[5].strip()
                data["meta"]["meter"] = lines[6].strip()
                
                # Parsing song data each position.
                for line in lines[7:]:
                    line = line.strip()
                    if line.startswith('#'):
                        description = line[1:].strip()  # Entfernt das #-Zeichen am Anfang und alle folgenden Leerzeichen
                        header.append({"description": description, "level":len(header)+1})
                    else:
                        parts = line.split(':')
                        key = parts[0]
                        roman = parts[1].split(',')[0]
                        label = parts[1].split(',')[1] if len(parts) > 1 and len(parts[1].split(',')) > 1 else ''
                        modulation = parts[1].split('|')[1] if len(parts) > 1 and '|' in parts[1] else ''

                        position = {
                            "header":header,
                            "key":key,
                            "roman":roman,
                            "label":label,
                            "modulation":modulation
                            }

                        data["position"].append(position)

                        # re init header each position.
                        header = []
            return data
        
        except (ValueError, FileNotFoundError) as e:
            print(e)  # Ausgabe der Fehlermeldung
            return False, e
    
    def convert(self, get_parsed_song):
        """
        Convert roman numeral into notes (chords).
        """
        main_key_str = get_parsed_song['meta']['key']
        # XXX:
        main_key_str = 'C'
        main_key = key.Key(main_key_str)

        print(f'--main key: ({main_key}).')

        for position in get_parsed_song['position']:
            print(position['key'], position['roman'], position['label'], position['modulation'])

            roman_numeral = roman.RomanNumeral(position['roman'], main_key)
            chord = roman_numeral.pitches
            main_scale = main_key.getScale()
            scale_degrees = [main_scale.getScaleDegreeFromPitch(p) for p in chord]
            tonic_pitch = main_scale.getTonic().pitchClass
            #chord_degrees = [(degree - main_scale.getScaleDegreeFromPitch(chord[0]) + 1) % 7 for degree in scale_degrees]
            inversion_num = roman_numeral.inversion()

            print([str(p) for p in chord])
            print(inversion_num)
            print(scale_degrees)

            found_chord_notes = []

            # bass
            actBass = ''
            if roman_numeral.bass() is not None:
                actBass = roman_numeral.bass().name
                actBassScale = -1   # placeholder value; TODO: calculate scale degree for bassnote (in case of inversion)
                found_chord_notes.append(actBass)

            # root
            actRoot = ''
            if roman_numeral.root() is not None:
                actRoot = roman_numeral.root().name
                found_chord_notes.append(actRoot)

            # 3rd.
            actThird = ''
            if roman_numeral.third is not None:
                actThird = roman_numeral.third.name
                found_chord_notes.append(actThird)

            # 5th.
            actFifth = ''
            if roman_numeral.fifth is not None:
                actFifth = roman_numeral.fifth.name
                found_chord_notes.append(actFifth)

            # 7th.
            actSeventh = ''
            if roman_numeral.seventh is not None:
                actSeventh = roman_numeral.seventh.name
                found_chord_notes.append(actSeventh)

            # sus2-chord / add2 = T9
            actSecond = ''
            if roman_numeral.getChordStep(2) is not None:
                actSecond = roman_numeral.getChordStep(2).name
                found_chord_notes.append(actSecond)

            # sus4-chord / add4 = T11
            actFourth = ''
            if roman_numeral.getChordStep(4) is not None:
                actFourth = roman_numeral.getChordStep(4).name
                found_chord_notes.append(actFourth)

            # 6-chord / add6 = T13
            actSixth = ''
            if roman_numeral.getChordStep(6) is not None:
                actSixth = roman_numeral.getChordStep(6).name
                found_chord_notes.append(actSixth)

            # GENERATE TENSION LIST (get list of remaining (not mapped) chord-tones)
            # e.g.: "B7add#15" --> T#15:"B#"
            print(found_chord_notes)
            print(roman_numeral)
            
            tension_notes = []
            tension_notes = [note for note in roman_numeral if note not in found_chord_notes]
            
            # check, if all notes are mapped to the scale
            if len(tension_notes) != 0:
                print('!INFO: There are notes that are NOT mapped and added to remaining tension list:', tension_notes)



        return True, 'dummy'

class Voiceleading:
    def __init__(self, config, rule):
        """
        """
        # import Config and Rule informations.
        self.config     = config
        self.rule       = rule

        # sub-classes of VL: Vertical, Horizontal.
        self.vertical   = self.Vertical(self.config, self.rule)
        self.horizontal = self.Horizontal(self.config, self.rule)

    class Vertical:
        def __init__(self, config, rule):
            """
            """
            # import Config and Rule informations from parent Voiceleading class.
            self.config = config
            self.rule = rule

        def generate_building_blocks(self, chord_type_degrees):
            """
            Generate "building blocks" for voice leading vertical based on defined rules.
            """

            chord_type_building_block   = []
            res = []

            for chord_type_degree in chord_type_degrees:
                track_building_block = []
                del track_building_block[:]

                print(f'--chord type: {chord_type_degree}')

                # read track informations and rules.
                act_track_id = 0
                for t in self.rule['track']:
                    act_track_id += 1
                    act_number_of_notes_to_generate = t['data']['anzahl noten']
                    act_track_description = t['data']['beschreibung']['lang']
                    print(f'--Track: ({act_track_id}): {act_track_description} [{act_number_of_notes_to_generate}x]')

                    # Generiere karthesisches produkt der noten-scaledegree Kombinationen (Root, 3rd, 5th, usw.).
                    combinations = product(chord_type_degree, repeat=act_number_of_notes_to_generate)

                    # filtere kombinationen entsprechend ihrer Regeln heraus.
                    filtered_combinations = []
                    act_rule_1 = t['data']['muss bassnote als tiefsten ton enthalten']

                    for combination in combinations:
                        # Voicing-Bauplan enthält Bass note (Root) als tiefsten Ton
                        if not act_rule_1 or (act_rule_1 and combination[0] == 1):
                            filtered_combinations.append(combination)

                    track_building_block.append(filtered_combinations)

                # erstelle jeweils kombinationen aus den drei tracks.
                res = []
                del res[:]
                for combi in product(*track_building_block):
                    res.append(list(combi))

                chord_type_building_block.append(res)

                # prüfe auf vollständigkeit.
                act_rule_2 = self.rule['muss komplett sein']['choice']
                act_rule_2_tracks = self.rule['muss komplett sein']['track']
                complete = [1,3,5,7]
                x = self.check_block_is_complete(res, act_rule_2_tracks, complete)
                print("RESULT:", json.dumps(x, indent=4))

            return True, chord_type_building_block
        
        def check_block_is_complete(self, res, act_rule_2_tracks, complete):
            """
            """
            result = []

            print(res)
            for i in res:
                pair = []
                del pair [:]
                for j in act_rule_2_tracks:
                    pair.append(i[j-1])
                print(pair)
                
                # Kombiniere die Tupel in einer einzigen Liste
                combined_list = list(chain.from_iterable(pair))

                # Verwende set, um die eindeutigen Werte zu erhalten
                distinct_list = list(set(combined_list))

                # Bestimme die Häufigkeit jedes Elements in der kombinierten Liste
                element_counts = Counter(combined_list)

                complete.sort()
                distinct_list.sort()

                # Bestimme die Anzahl der fehlenden Elemente
                missing_elements = len(set(complete) - set(distinct_list))

                # Bestimme das fehlende Element
                missing_elements_list = list(set(complete) - set(distinct_list))

                # Überprüfe, ob die beiden Listen gleich sind
                if complete == distinct_list:
                    compared = True
                else:
                    compared = False

                result.append(
                    {
                        "is_complete": compared, 
                        'missing_count': missing_elements, 
                        'missing_list': missing_elements_list,
                        'element_counts': element_counts
                    }
                )
                    
            return True, result
        
        def synthetic_rollout_notes(self):
            # TODO
            return True, 'dummy'

        def generate_combinations (self):
            # Hier könnte Code zur Analyse der horizontalen Bewegung zwischen zwei Melodien stehen
            pass

    class Horizontal:
        def __init__(self, config, rule):
            self.config = config
            self.rule = rule

        def generate_combinations(self):
            # Hier könnte Code zur Analyse der horizontalen Bewegung zwischen zwei Melodien stehen
            pass

class Sheet:
    def __init__(self):
        pass

    def generate(self):
        # Hier könnte Code zur Analyse der horizontalen Bewegung zwischen zwei Melodien stehen
        pass

# CALL section:
if __name__ == "__main__":
    try:
        # Initialization variables.
        act_file_count = 0
        act_transpo_iteration = 0

        # Get actual project folder.
        script_path = os.path.dirname(os.path.realpath(__file__))
        print(f'script_path: ({script_path}).')

        # Load configuration informations from config.json file.
        c = Config()
        config_file_name = os.path.join(script_path, 'json', 'config.json')
        result = c.load(config_file_name)
        if result[0]:
            config_data = result[1]
        else:
            print(f"ERR: ({result[1]}).")
            raise ValueError('!!!Config data issue. ENDING SCRIPT FORCED!')
        
        # Load rules from rule.yaml file.
        r = Rule()
        rule_file_name = os.path.join(script_path, 'yaml', 'rule.yaml')
        result = r.load(rule_file_name)
        if result[0]:
            rule_data = result[1]
        else:
            print(f"ERR: ({result[1]}).")
            raise ValueError('!!!Rule data issue. ENDING SCRIPT FORCED!')

        # Load informations from chordprogression file.
        act_song_file_path = os.path.join(script_path, config_data['file']['source_folder'])
        act_file_title_arr = config_data['file']['source_files']
        
        # in case no file manually was provided by user, get a list of all files in the specific folder.
        if(len(act_file_title_arr) == 0):
            # BATCH JOB: Hole Liste aller .rom-Dateien im angegebenen Ordner für den batch job
            act_file_title_arr = [f for f in os.listdir(act_song_file_path) if f.endswith(config_data['file']['extension']['roman'])]

        # in case of there are no files to process.
        if(len(act_file_title_arr) == 0):
            print(f"ERR: No files to process. Please check config.json or files in the specific song folder to read.")
            raise ValueError('!!!No files to process. ENDING SCRIPT!')
        
        total_amount_of_batch_files = len(act_file_title_arr)
        print(f"-- files to process: ({total_amount_of_batch_files}).")

        ### Framework ###
        # iterates through all defined files, transposing chord progressions in user defined keys.
        
        p = Parser()
        vl = Voiceleading(config_data, rule_data)
        vlv = vl.vertical

        # generiere "building blocks" für VL-Vertical Lombinationen.
        chord_type_degrees = [(1,3,5),(1,3,5,7),(1,4,5),(1,2,5)]
        result = vlv.generate_building_blocks(chord_type_degrees)
        if not result[0]:
            print(f"ERR: ({result[1]}).")
            print(f"!VL-Vertical generate building blocks issue!")

        #print("RESULT:", json.dumps(result, indent=4))
        print("RESULT:", result)

        vlh = vl.horizontal

        # stage 1: iterate all filenames
        for act_file_title in act_file_title_arr:
            act_file_count += 1
            print(f'-- song: ({act_file_count} / {total_amount_of_batch_files}), ({act_file_title})')

            act_song_file_name = os.path.join(script_path, config_data['file']['source_folder'], act_file_title)
            
            result = p.load(act_song_file_name)
            if not result[0]:
                print(f"ERR: ({result[1]}).")
                print(f"!SKIPPING processing of the specific (not valid) file ({act_song_file_name})!")
                continue    # Skip processing of specific not valid file.

            print('...PROCESSING...')

            parsed_song = result[1]

            result = p.convert(parsed_song)
            if not result[0]:
                print(f"ERR: ({result[1]}).")
                print(f"!SKIPPING processing of the specific parsed song!")
                continue    # Skip processing of specific not valid file.

            # genereriere noten
            result = vlv.synthetic_rollout_notes()
            if not result[0]:
                print(f"ERR: ({result[1]}).")
                print(f"!VL-Vertical generate notes issue!")

            #print("RESULT:", json.dumps(result, indent=4))

    except ValueError as ve:
        print(ve)  # Ausgabe der Fehlermeldung