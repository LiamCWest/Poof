#the main file, where everything starts

from logic.game import gameManager # import the game manager

def main(): # main function, where everything starts
    gameManager.init() # initialize the game manager
    gameManager.start() # start the game manager

if __name__ == "__main__": # if this file is being run directly
    main() # run the main function