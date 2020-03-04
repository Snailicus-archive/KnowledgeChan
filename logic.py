import csv
from dataclasses import dataclass, field
'''
TODO:
    print essences and combinations prettily - make it good
    search functionality for essences and confluences
'''

RARITIES = ['Unknown', 'Common', 'Uncommon', 'Rare', 'Epic', 'Legendary']
ESSENCES_FILE = 'essences.csv'
COMBINATIONS_FILE = 'combinations.csv'


@dataclass(order=True)
class Essence:
    sort_index: int = field(init=False, repr=False)
    name: str
    rarity: str = 'Unknown'
    description: str = 'No info available(yet)'

    def __hash__(self):
        return
    def __post_init__(self):
        self.sort_index = RARITIES.index(self.rarity)

    def __str__(self):
        return f'{self.name} [{self.rarity}]'

@dataclass
class Confluence:
    name: str
    combinations: list
    description: str = 'No info available(quite yet)'

    def __str__(self):
        return '\n'.join(f'{show_combination(comb)} -> {self.name}' for comb in  self.combinations)

essences = {} # essence.name -> essence
confluences = {} # confluence.name -> confluence
combinations = {} # combination -> confluence

def form(x):
    return x.lower().capitalize().strip()

def show_combination(combination):
    combination = list(combination)
    return ' + '.join(combination)

def commit_essences():
    with open(ESSENCES_FILE, 'w', newline='') as essence_file:
        writer = csv.writer(essence_file)
        for name, rarity in essences.items():
            writer.writerow([name, rarity])

def commit_combinations():
    with open(COMBINATIONS_FILE, 'w', newline='') as combinations_file:
        writer = csv.writer(combinations_file)
        for essences, confluence in combinations.items():
            writer.writerow(list(essences) + [confluence])

def pull_essences():
    with open(ESSENCES_FILE, 'r', newline='') as essence_file:
        reader = csv.reader(essence_file)
        for line in reader:
            essence = Essence(line[0], line[1])
            essences[essence.name] = essence

def pull_combinations():
    with open(COMBINATIONS_FILE, 'r', newline='') as combinations_file:
        reader = csv.reader(combinations_file)
        for line in reader:
            name = line[3]
            combination = frozenset(line[0:3])
            confluence = confluences.get(name)
            if not confluence:
                confluence = Confluence(name, [combination])
                confluences[name] = confluence
            else:
                confluence.combinations.append(combination)
            combinations[combination] = confluence

def create_combination(lst):
    lst = list(map(form, lst))
    for essence in lst:
        if essence not in essences.keys():
            raise NameError(essence)

    comb = frozenset(lst)
    if len(comb) != 3:
        raise IndexError
    return comb

def find_confluence(a, b, c):
    comb = create_combination([a, b, c])
    return combinations[comb], comb

def get_confluence(name):
    return confluences.get(form(name))

def add_essence(name, rarity='Unknown'):
    name, rarity = map(form, [name, rarity])
    essence = Essence(name, rarity)

    if name in essences.keys():
        raise KeyError(name)

    essences[name] = essence

    with open(ESSENCES_FILE, 'a', newline='') as essences_file:
        writer = csv.writer(essences_file)
        writer.writerow([name, rarity])

def add_combination(a, b, c, confluence):
    name = form(confluence)
    combination = create_combination([a, b, c])

    # error if combination already assigned
    if combination in combinations:
        raise KeyError('combination exists')

    # make new confluence if doesnt exist
    conf = confluences.get(name)
    if not conf:
        conf = Confluence(name, [])
        confluences[name] = conf

    combinations[combination] = conf
    conf.combinations.append(combination)

    with open(COMBINATIONS_FILE, 'a', newline='') as comb_file:
        writer = csv.writer(comb_file)
        writer.writerow([a, b, c, name])

if __name__ == '__main__':
    pull_essences()
    pull_combinations()
