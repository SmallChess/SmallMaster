import chess
import chess.pgn

names = []
with open("players.tsv") as r:
    for line in r:
        toks = line.strip().split("\t")
        assert(len(toks) == 2)
        name = toks[1].replace('"', "")
        names.append(name)

def fixName(x):
    x = x.replace(" (Computer)", "")
    x = x.replace("Robert James Fischer", "Bobby Fischer")
    x = x.replace("Yifan Hou", "Hou Yifan")
    x = x.replace("Hao Wang", "Wang Hao")
    x = x.replace("Tigran Vartanovich Petrosian", "Tigran Petrosian")
    x = x.replace("Vachier-Lagrave, Maxime", "Maxime Vachier-Lagrave")
    return x

with open("/tmp/A.pgn") as r:
    games = []
    while True:
        game = chess.pgn.read_game(r)
        if game is None:
            break
        w = fixName(game.headers["White"])
        b = fixName(game.headers["Black"])
        if "?" in w or "?" in b:
            continue
        foundW = w in names
        foundB = b in names
        if not foundW and not foundB:
            print("-----------------")
            print(w)
            print(b)
        if foundW and foundB:
            games.append(str(game))

with open("MasterDatabase.pgn", "w") as w:
    for game in games:
        w.write(game + "\n\n")
