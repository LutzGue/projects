from music21 import *
"""
Central place to define parameters for generation vlv and vlh.
Define the range of generated octaves and midi note ids for each voice note.
NOTE: If the ranges are too strictly limited, it can lead to the fact that no VLV or VLH can be generated.
"""
parameters = {
    'range':{

        # --- PRE-FILTER (VERTICAL) ---

        # NOTE: PRE-FILTER (VERTICAL): global range for vl-vertical generation. Synthetically generated set of notes in the defined range.
        # NOTE: (1) min:1 --> generates (C1, C#1, D1, ..., B1, ...)
        # NOTE: (2) max:5 --> generates (..., C5, C#5, D5, ..., B5)
        # NOTE: EXAMPLE 1:
        #    'min': 1,
        #    'max': 5
        'octave':{
            'min': 1,
            'max': 5
        },

        # NOTE: PRE-FILTER (VERTICAL): LIMIT the interval range of each chord vlv. This reduces computation time IN ADVANCE ("pre") of vlh combinations. HINT: Bad defined range can cause empty vlv for chords!). 
        # NOTE: (1) max_ambitus:m14 --> (C0, E0, G1, C1):P8 < m14 --> keep vlv-candidate (not filtered out)
        # NOTE: (2) min_ambitus:m9 --> (C0, E0, G1, C1):P8 > m9 --> skip vlv-candidate (filtered out)
        # NOTE: EXAMPLE 1 -- jazz 3-note voicing:
        #    'max_ambitus': interval.Interval('m14').semitones,
        #    'min_ambitus': interval.Interval('m10').semitones
        # NOTE: EXAMPLE 2 -- jazz 3-note voicing:
        #    'max_ambitus': interval.Interval('m17').semitones,
        #    'min_ambitus': interval.Interval('m9').semitones
        # NOTE: EXAMPLE 3 -- jazz 3-note voicing ("Levine: II V I"):
        #    'max_ambitus': interval.Interval('M17').semitones,
        #    'min_ambitus': interval.Interval('m10').semitones
        'interval_pre_limiter':{
            'max_ambitus': interval.Interval('P11').semitones,
            'min_ambitus': interval.Interval('M9').semitones
        },

        # -- POST-FILTER (HORIZONTAL) ---

        # NOTE: POST-FILTER (HORIZONTAL and VERTICAL-ambitus): Interval range of each chord vl-horizontal. This interval is used for calculation KPI in vlh ("post"). HINT: Bad defined range can cause empty vlh for chords!
        # NOTE: (1) max_ambitus: m17 --> (C0, E0, G1, C1):P8 < m17 --> keep vlv candidate
        # NOTE: (2) min_ambitus: m9 --> (C0, E0, G1, C1):P8 < m9 --> skip vlv candidate
        # NOTE: (3) min_interval: m3 --> minimum space between the inner-intervals of vlv-candidate
        # NOTE: EXAMPLE 1 -- jazz 3-note voicing:
        #    'max_ambitus': interval.Interval('m14').semitones,
        #    'min_ambitus': interval.Interval('m10').semitones,
        #    'min_interval': interval.Interval('P1').semitones
        # NOTE: EXAMPLE 2 -- jazz 3-note voicing:
        #    'max_ambitus': interval.Interval('m17').semitones,
        #    'min_ambitus': interval.Interval('m9').semitones,
        #    'min_interval': interval.Interval('P1').semitones
        # NOTE: EXAMPLE 3 -- jazz 3-note voicing ("Levine: II V I"):
        #    'max_ambitus': interval.Interval('M17').semitones,
        #    'min_ambitus': interval.Interval('m10').semitones,
        #    'min_interval': interval.Interval('P4').semitones
        'interval':{
            'max_ambitus': interval.Interval('P11').semitones,
            'min_ambitus': interval.Interval('M9').semitones,
            'min_interval': interval.Interval('P1').semitones
        },
        
        # NOTE: smooth Soprano line. Define the leaps and steps.
        # NOTE: EXAMPLE 1 -- jazz 3-note voicing
        #    'max':interval.Interval('M3').semitones,
        #    'min':interval.Interval('P1').semitones
        'soprano':{
            'max':interval.Interval('P8').semitones,
            'min':interval.Interval('P1').semitones
        },

        # bass note is the lowest note (A1;F#3)
        'bass_midi':{
            'min': pitch.Pitch('A1').midi,
            'max': pitch.Pitch('F#3').midi
        },
        # doubling the root above the bass note (in case of bass note is different to root)
        'root_midi':{
            'min': pitch.Pitch('A1').midi,
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
            'min': pitch.Pitch('D-3').midi,
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