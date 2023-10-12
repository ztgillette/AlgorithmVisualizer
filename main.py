import pygame
import sys
from Colors import *
from Board import *
from Button import *
from Algorithms import *

def main():

    # Initialize Pygame
    pygame.init()

    # Constants
    WIDTH, HEIGHT = 1000, 800
    FPS = 60

    # Create the game window
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Algorithm Visualizer")

    # Load game assets (if any)
    board = Board(win, 800, 800, 20, 20, GRAY)

    # buttons
    resetButton = Button(win, board.resetCells, 825, 50, 150, 50, "Reset")
    randomBoardButton = Button(win, board.fillRandom, 825, 125, 150, 50, "Randomize")
    startButton = Button(win, board.resume, 825, 200, 150, 50, "Start")
    pauseButton = Button(win, board.pause, 825, 275, 150, 50, "Pause")

    # algorithm
    algo = Algorithms()

    # Main game loop
    run = True
    clock = pygame.time.Clock()

    while run:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mosx, mosy = event.pos
                board.detectMouseClick(mosx,mosy)
                resetButton.detectMouseClick(mosx, mosy)
                randomBoardButton.detectMouseClick(mosx, mosy)
                startButton.detectMouseClick(mosx, mosy)
                pauseButton.detectMouseClick(mosx, mosy)
            elif event.type == pygame.MOUSEBUTTONUP:
                board.detectMouseUnclick()
                
            # Additional event handling here
            # ...
        
        # Update game state
        # ...
        board.detectMouseHover()
        
        # Draw to the screen
        
        # Draw game objects here
        # ...
        board = algo.BFS(board)
        board.draw()

        #draw buttons
        resetButton.draw()
        randomBoardButton.draw()
        startButton.draw()
        pauseButton.draw()

        # Update the display
        pygame.display.update()
        
        # Cap the frame rate
        clock.tick(FPS)

    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()