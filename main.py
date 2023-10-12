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
    buttons = []
    buttons.append(Button(win, board.resetCells, 825, 25, 150, 50, "Reset"))
    buttons.append(Button(win, board.fillRandom, 825, 100, 150, 50, "Randomize"))
    buttons.append(Button(win, board.playpause, 825, 175, 150, 50, "Play / Pause"))
    buttons.append(Button(win, board.setBFS, 825, 275, 150, 50, "BFS", board))
    buttons.append(Button(win, board.setDFS, 825, 350, 150, 50, "DFS", board))

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
                for button in buttons:
                    button.detectMouseClick(mosx, mosy)
                
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
        if board.algo == "BFS":
            board = board.algorithm.BFS(board);
        elif board.algo == "DFS":
            board = board.algorithm.DFS(board);
        board.draw()

        #draw buttons
        for button in buttons:
            button.draw()
        pygame.draw.rect(win, BLACK, (825, 250, 150, 3)) #dividing line

        # Update the display
        pygame.display.update()
        
        # Cap the frame rate
        clock.tick(FPS)

    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()