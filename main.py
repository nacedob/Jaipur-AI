#!/usr/bin/env python3
from src.core.game import Game
from src.gui.terminal import TerminalGUI
import sys


def main():
    players = ['human', 'ai']
    try:
        if len(sys.argv) > 1 and sys.argv[1] == 'pygame':
            game = Game(gui='pygame', player_types=players)
        else:
            game = Game(gui='terminal', player_types=players)
        print("Starting Jaipur Game...")
        game.play()
    except KeyboardInterrupt:
        print("\nGame interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        raise e
        print(f"\nAn error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
