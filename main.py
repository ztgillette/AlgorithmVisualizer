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
    FPS = 240

    # Create the game window
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Algorithm Visualizer")

    # Load game assets (if any)
    board = Board(win, 800, 800, 50, 50, GRAY)

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
                for button in board.buttons:
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
        if(board.modeswitch):

            if(isinstance(board, Graph)):
                board = Board(win, 800, 800, 50, 50, GRAY)
            else:
                board = Graph(win, 800, 800, 50, 50, GRAY)

        if(board.clockcounter >= board.clockmax):
            if board.algo == "BFS":
                board = board.algorithm.BFS(board);
            elif board.algo == "DFS":
                board = board.algorithm.DFS(board);
            elif board.algo == "A*":
                board = board.algorithm.ASTAR(board)

            board.clockcounter = 0
        else:
            board.clockcounter += 1



        board.draw()

        #draw buttons
        for button in board.buttons:
            button.draw()
        pygame.draw.rect(win, BLACK, (825, 250, 150, 3)) #dividing line
        pygame.draw.rect(win, BLACK, (825, 425, 150, 3)) #dividing line

        # Update the display
        pygame.display.update()
        
        # Cap the frame rate
        clock.tick(FPS)

    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()