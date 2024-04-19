**Project Description**
**Project Name**
Chord Progression Analysis and Root Movement Type Assignment

**Objective**
The objective of this project is to develop a program that analyzes a given chord progression in Roman Numerals in the possible keys of "Major" and "Minor", and determines the intervals of the root between the respective chords. Subsequently, these intervals are assigned to certain root movement types "Authentic" and "Plagal". By using this root motion classification, it is possible to quickly find out personal composing style and determine styles for own harmonizations. The code is written in Python and use the "music21" library.

**Requirements**
*(1) Romann Numeral Conversion:* The user inputs a chord progression with Roman Numerals in a specific key. The chord progression contains a list of tuples, where each tuple contains the key and the Roman Numeral. For example, input in the key of C Major: [("C", "I"),("C", "V"), ("C","IV"), ("C","vi"), ("C","I")]. The converted result is: {C,G,F,Am,C}. Keys in "Major" are in uppercase and keys in "Minor" are in lowercase.

*(2) Chord Progression Interval Analysis:* This program should be able to analyze a given chord progression. For example, if the chord progression {C,G,F,Am,C} is given, the program should be able to to determine the intervals of the root notes between the respective chords. The expectedexpected result would be {C-G: P5 up; G-F: M2 down; F-A: M3 up; A-C: m3 up}. It is important to note, that the root note is NOT to be confused with the bass note!

*(3) Root Movement Typ Assignment:* After analyzing the chord progression, the program should be able to assign the specific intervals in combination with the addition of "up" and "down" to the corresponding root movement type. For example, if the intervals are {P5 up; M2 down; M3 up; m3 up}, the program should be able to assign these intervals to the root movement types {"PH"; "As"; "PT"; "Pt"}. The different use of upper and lower case letters is intentional.