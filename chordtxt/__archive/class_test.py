class BeispielKlasse:
    def __init__(self, var_a):
        self.var_a = var_a
        self.var_b = 'x'

    def funkt_a(self):
        print("Funkt_a wurde aufgerufen.")
        self.var_b = 'value b'
        self.funkt_b()

    def funkt_b(self):
        print("Funkt_b wurde aufgerufen.")
        print('|',self.var_a, '|',self.var_b,'|')

# Instanz der Klasse erstellen
beispiel_instanz = BeispielKlasse('value_a')

# Funktion funkt_a aufrufen, die dann funkt_b aufruft
beispiel_instanz.funkt_a()