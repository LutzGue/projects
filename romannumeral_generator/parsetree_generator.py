import random

def rand_element():

    # Liste der Werte
    r = ['I', 'ii', 'iii','IV','V','vi','vii°','vii°7','#IV°7','V7','II7']
    v = ['', '<e>']
    h = ['', '<e>']

    # String, in dem der Ersatz vorgenommen wird
    extend = '["<r>"<v>"?"]<h>'

    # Zufällige Auswahl aus der Liste
    random.seed()
    random_choice_r = random.choice(r)

    random.seed()
    random_choice_v = random.choice(v)

    random.seed()
    random_choice_h = random.choice(h)

    # Ersetzen des Suchbegriffs '<r>' durch die zufällige Auswahl
    result = extend.replace('<r>', random_choice_r)
    result = result.replace('<v>', random_choice_v)
    result = result.replace('<h>', random_choice_h)

    return result

def generate_parsetree():
    n = 4
    elements = rand_element()
    for _ in range(n):
        count = elements.count('<e>')
        for i in range(count):
            elements = elements.replace('<e>', rand_element(), (i+1))
            act_count_items = elements.count('"?"')
            if act_count_items > 8:
                return None

    tonic_start = [
        '["I""?"]',
        '["V""?"]'
        ''
        ]

    connection = [
        '["ii7""?"]',
        '["IV""?"]',
        ''
        ]

    cadence = [
        '["V""?"]["I""?"]',
        '["V7""?"]["I""?"]',
        '["V""?"]["iv""?"]',
        ]

    random.seed()
    random_choice_tonic_start = random.choice(tonic_start)

    random.seed()
    random_choice_connection = random.choice(connection)

    random.seed()
    random_choice_cadence = random.choice(cadence)

    start = '["C"' + random_choice_tonic_start + elements + random_choice_connection + random_choice_cadence + ']'
    start = start.replace('<e>', '')

    parse_tree_visual = start

    count_items = start.count('"?"')

    start = start.replace('"["', '", ["')
    start = start.replace('""?"', '", "?"')
    start = start.replace(']"?"', '], "?"')
    start = start.replace('"]["', '"], ["')

    parse_tree_list = start

    data = {
        "count": count_items,
        "visual": parse_tree_visual,
        "list": parse_tree_list
    }

    return data

# Testaufruf
for _ in range(10):
    result = generate_parsetree()
    print(result)