#c.key = key.Key('C')
#c.romanNumeral

#[str(p) for p in c.pitches]

#c.annotateIntervals(inPlace=True, stripSpecifiers=False)
#[ly.text for ly in c.lyrics]

# Get the pitches of the chord and add them to the stream
#for p in c.pitches:
#    n = note.Note(p)
#    n.duration = c.duration
#    self.s.append(n)

##############

#tnc = tinyNotation.Converter()
#tnc.modifierUnderscore = HarmonyModifier
#tnc.load("4/4 d2_m7 g4_7 c_maj7")

#s = tnc.parse().stream
#s.show("text")
#s.transpose(interval.GenericInterval(2), inPlace=True)
#s.show("text")

#############