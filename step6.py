import chess
import chess.pgn

def fixName(x):
    x = x.replace(" (Computer)", "")
    x = x.replace("Robert James Fischer", "Bobby Fischer")
    x = x.replace("Yifan Hou", "Hou Yifan")
    x = x.replace("Hao Wang", "Wang Hao")
    x = x.replace("Tigran Vartanovich Petrosian", "Tigran Petrosian")
    x = x.replace("Vachier-Lagrave, Maxime", "Maxime Vachier-Lagrave")
    return x

with open("MasterDatabase.pgn") as r:
    names = []
    dates = []
    events = []
    while True:
        game = chess.pgn.read_game(r)
        if game is None:
            break

        w = fixName(game.headers["White"])
        b = fixName(game.headers["Black"])

        if w not in names:
            names.append(w)
        if b not in names:
            names.append(b)

        date = game.headers["Date"].split(".")[0]
        if date not in dates:
            dates.append(int(date))

        event = game.headers["Event"]
        if event not in events:
            events.append(event)

with open("MasterDatabase.events.index", "w") as w:
    for i in events:
        w.write(i + "\n")

with open("MasterDatabase.players.index", "w") as w:
    for i in names:
        w.write(i + "\n")

with open("MasterDatabase.dates.index", "w") as w:
    w.write(str(min(dates)) + "\n")
    w.write(str(max(dates)) + "\n")
