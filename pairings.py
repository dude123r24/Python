import random

def read_players(file_name):
    with open(file_name, 'r') as f:
        return [name.strip() for name in f.readlines()]

def save_pairings(pairings, file_name):
    with open(file_name, 'w') as f:
        for pairing in pairings:
            f.write(','.join(pairing) + '\n')

def get_pairings(players, file_name):
    try:
        with open(file_name, 'r') as f:
            print ("File {} found".format(file_name))
            pairings = [line.strip().split(',') for line in f.readlines()]
            print ("get_pairings: pairings = {}".format(pairings))
            return [pairing for pairing in pairings if all(name in players for name in pairing)]
    except FileNotFoundError:
        print ("File {} not found".format(file_name))
        return []

def get_all_pairings(players):
    players = players[0].split(",")
    n = len(players)
    print ("get_all_pairings: players = {}".format(players))
    pairings = [(players[i], players[j]) for i in range(n) for j in range(i+1, n)]
    print ("get_all_pairings: pairings = {}".format(pairings))
    print ("Game : {}".format(random.sample(pairings,2)) ) 
    return pairings


def main():
    players = read_players("players.txt")
    n = len(players)
    print ("n={}".format(n))
    print ("players = {}".format(players))

    get_all_pairings(players)


    pairings_file = "pairings.txt"
    pairings = get_pairings(players, pairings_file)
    print ("pairings = {}".format(pairings))

    players = [player for player in players if not any(player in pairing for pairing in pairings)]
    while len(players) >= 2:
        pairing = random.sample(players, 2)
        print ("pairing = {}".format(pairing))

        pairings.append(pairing)
        print ("pairings = {}".format(pairings))

        players = [player for player in players if player not in pairing]
        print ("players = {}".format(players))

    save_pairings(pairings, pairings_file)

    for i, pairing in enumerate(pairings):
        print(f"Pairing {i + 1}: {pairing[0]} and {pairing[1]}")

if __name__ == "__main__":
    main()
