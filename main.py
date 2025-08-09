#!/usr/bin/env python3
from src.game import Game
from src.gui.terminal import TerminalGUI
import sys


def main():
    try:
        if len(sys.argv) > 1 and sys.argv[1] == 'pygame':
            game = Game('pygame')
        else:
            game = Game('terminal')
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
