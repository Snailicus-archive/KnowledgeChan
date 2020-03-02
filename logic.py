import csv

'''
TODO:
    write the actual bot
    fix error in add combination
    print essences and combinations prettily - make it good
    search functionality for essences and confluences
'''


essences = {}
combinations = {}

def form(x):
    return x.lower().capitalize()

def commit_essences():
    with open('essences.csv', 'w', newline='') as essence_file:
        writer = csv.writer(essence_file)
        for name, rarity in essences.items():
            writer.writerow([name, rarity])

def commit_combinations():
    with open('combinations.csv', 'w', newline='') as combinations_file:
        writer = csv.writer(combinations_file)
        for essences, confluence in combinations.items():
            writer.writerow(list(essences) + [confluence])

def pull_essences():
    with open('essences.csv', 'r', newline='') as essence_file:
        reader = csv.reader(essence_file)
        for line in reader:
            essences[line[0]] = line[1]

def pull_combinations():
    with open('combinations.csv', 'r', newline='') as combinations_file:
        reader = csv.reader(combinations_file)
        for line in reader:
            combinations[frozenset(line[0:3])] = line[3]

def find_confluence(a, b, c):
    a, b, c = map(form, [a, b, c])
    return combinations[frozenset([a, b, c])]

def add_essence(name, rarity):
    essences[form(name)] = form(rarity)

change_essence_rarity = add_essence

def add_combination(a, b, c, confluence):
    a, b, c = map(form, [a, b, c])
    if not all(essence in essences.keys() for essence in [a, b, c]):
        raise Exception("missing essence")
    combinations[frozenset([a, b, c])] = form(confluence)


if __name__ == '__main__':
    pull_essences()
    pull_combinations()
