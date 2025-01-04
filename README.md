## Summary

Create famous chess players’ games in PGN format on Chessgames.com.

## Usage

    # Remove old cache if needed
    rm -rf step1/*

    python3 step1.py
    python3 step2.py
    chmod a+x step2.sh
    ./step2.sh

    mv 1* step2/ # Could failed if no games...
    mv 2* step2/ # Could failed if no games...
    mv 3* step2/ # Could failed if no games...

    python3 step3.py
    python3 step4.py

    scp *.pgn smallchess@smallchess.com:smallchess.com/Games/

    cat *.pgn > /tmp/A.pgn
    python3 step5.py

    grep -v "EventDate" MasterDatabase.pgn | grep -v "PlyCount" | grep -v "ECO" | grep -v "Round" | grep -v "Elo" | grep -v Site > /tmp/A.pgn
    pgn-extract -s -d/tmp/dupes.pgn -o/tmp/unique.pgn /tmp/A.pgn
    cat prefix.pgn_ /tmp/unique.pgn > /tmp/B.pgn
    mv /tmp/B.pgn MasterDatabase.pgn
    ls -lah MasterDatabase.pgn

    python3 step6.py
