#! /usr/bin/python
'''
tetris.py

starts the game
'''
from traceback import print_exc

if __name__ == "__main__":
    from traceback_plus import print_exc_plus

    try:
        from main import main

        main()
    except Exception as e:
        print_exc(e)
