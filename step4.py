import os
import glob
import chess.pgn
from dateutil import parser

for file in glob.glob("*.pgn"):
    games = []
    with open(file) as r:
        print(file)
        while True:
            game = chess.pgn.read_game(r)
            if game is None:
                break
            date = game.headers["Date"].replace("1867.??6.01", "1867.06.01")
            date = date.replace(".??", "")
            date = date.replace(".?", ".01")
            date = parser.parse(date)
            games.append( { "pgn":str(game), "time":date.timestamp() })
    assert(len(games))
    games.sort(key=lambda x: x["time"], reverse=True)
    with open(os.path.basename(file), "w") as w:
        for game in games:
            w.write(game["pgn"] + "\n\n")
    print("Sorted: " + os.path.basename(file))
