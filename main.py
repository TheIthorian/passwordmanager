from gui import *
from database import init


def main():
    init()
    gui = Gui()
    gui.run_main_loop()


if __name__ == "__main__":
    main()
