import pygame, sys
from constant import SQUARE_SIZE, WIDTH,HEIGHT,RED, BLUE, WHITE, YELLOW,P_GREEN,GREY
from board import Board
from game import Game
from minimax import minimax
from alphabeta import alphabeta_pruning
from genetic_algo import genetic_algorithm
from button import Button
FPS = 60
pygame.init()


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sholo Ghuti Game')
WIN.fill(YELLOW)
image = pygame.image.load('data\\splash.jpg')
image_rect = image.get_rect(center=(200, 360))
WIN.blit(image, image_rect)
pygame.display.update()
pygame.time.delay(2000)


def get_row_col_from_mouse(pos):
    x , y = pos
    row = y//SQUARE_SIZE
    col = x//SQUARE_SIZE
    return row,col 


def main():

    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    def get_font(): 
        return pygame.font.SysFont('Verdana',35)

    def play(difficulty):
        while True:
            PLAY_MOUSE_POS = pygame.mouse.get_pos()
            if game.turn == BLUE:
                if(difficulty==0):
                    value, new_board = genetic_algorithm(game.get_board(), 10, game)
                    pygame.time.delay(500)
                elif(difficulty==1):
                    value, new_board = alphabeta_pruning(game.get_board(), 4,True, game, float('-inf'), float('inf'))
                elif(difficulty==-1):
                    value, new_board = minimax(game.get_board(),3,True, game)
                game.ai_move(new_board)

            if game.winner()== RED or game.winner()==BLUE:
                while True:
                    val = game.get_standard_of_wining() # receving the fuzzy COG Value into val
                    #print(val)
                    #print(game.winner())
                    Back_MOUSE_POS = pygame.mouse.get_pos()
                    WIN.fill(YELLOW)
                    if(val<=10):
                        if(game.winner()== RED):
                            winnertext = get_font().render("You have beaten AI", True, "black")
                            standardtext = get_font().render("by a narrow margin", True, "black")
                        else:
                            winnertext = get_font().render("AI has beaten you", True, "black")
                            standardtext = get_font().render("by a narrow margin", True, "black")

                    elif(val<=20):
                        if(game.winner()== RED):
                            winnertext = get_font().render("You have beaten AI", True, "black")
                            standardtext = get_font().render("by a moderate margin", True, "black")
                        else:
                            winnertext = get_font().render("AI has beaten you", True, "black")
                            standardtext = get_font().render("by a moderate margin", True, "black")

                    elif(val<=30):
                        if(game.winner()== RED):
                            winnertext = get_font().render("You have beaten AI", True, "black")
                            standardtext = get_font().render("by a huge margin", True, "black")
                        else:
                            winnertext = get_font().render("AI has beaten you", True, "black")
                            standardtext = get_font().render("by a huge margin", True, "black")

                    winnerrect = winnertext.get_rect(center=(200, 200))
                    standardrect = standardtext.get_rect(center=(200, 250))
                    WIN.blit(winnertext, winnerrect)
                    WIN.blit(standardtext, standardrect)

                    run = False
                    backbutton = Button(pos=(200, 450), 
                                text_input="BACK", font=get_font(), base_color="black", hovering_color="red")

                    backbutton.changeColor(Back_MOUSE_POS)
                    backbutton.update(WIN)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if backbutton.checkForInput(Back_MOUSE_POS):
                                main()

                    pygame.display.update()
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    
                    if row < 0 or row >= 9 or col < 0 or col >= 5 :
                        pass
                    else:
                        game.select(row,col)
                game.update()

            PLAY_BACK = Button( pos=(200, 740), text_input="BACK", font=pygame.font.SysFont('Consolas',20), base_color="black", hovering_color="red")
            PLAY_BACK.changeColor(PLAY_MOUSE_POS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        main()
               
            PLAY_BACK.update(WIN)
            pygame.display.update()


    def select_dificulty():
        running = True
        while running:
            WIN.fill(YELLOW)
            fonttext = get_font().render("Dificulty Level", True, "Black")
            fontrect = fonttext.get_rect(center=(200, 50))
            WIN.blit(fonttext,fontrect)
            hard = Button(pos=(200, 350), text_input="Hard (Pruning)", font=pygame.font.SysFont('Verdana', 27), base_color=(22,17, 16), hovering_color=(217, 21, 0))
            medium = Button(pos=(200, 410), text_input="Medium (Minimax)", font=pygame.font.SysFont('Verdana', 27), base_color=(22, 17, 16), hovering_color=(191, 86, 0))
            easy = Button(pos=(200,470), text_input="Easy (Genetic Algo)", font=pygame.font.SysFont('Verdana', 27), base_color=(22, 17, 16), hovering_color=(60, 229, 13))
            back = Button(pos=(200, 650), text_input="Back", font=pygame.font.SysFont('Verdana', 22), base_color=(22,17,16), hovering_color=(164, 2, 34))

            image1 = pygame.image.load('data\\play5.png')
            image_rect = image1.get_rect(center=(200, 170))
            WIN.blit(image1, image_rect)
            
            PLAY_MOUSE_POS = pygame.mouse.get_pos()
            for button in [hard, easy, medium, back]:
                button.changeColor(PLAY_MOUSE_POS)
                button.update(WIN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if hard.checkForInput(PLAY_MOUSE_POS):
                        play(1)
                    elif medium.checkForInput(PLAY_MOUSE_POS):
                        play(-1)
                    elif easy.checkForInput(PLAY_MOUSE_POS):
                        play(0)
                    elif back.checkForInput(PLAY_MOUSE_POS):
                        main_menu()

            pygame.display.update()




    def main_menu():
        while True:
            
            WIN.fill(YELLOW)
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            MENU_TEXT = pygame.font.SysFont('Consolas',50).render("16 Guti", True, "#0d15ff")
            MENU_RECT = MENU_TEXT.get_rect(center=(200, 100))
            image = pygame.image.load('data\\play.png')
            image_rect = image.get_rect(center=(200, 240))
            WIN.blit(image, image_rect)
            PLAY_BUTTON = Button(pos=(200, 450), text_input="PLAY", font=get_font(), base_color="#0d0003", hovering_color="green")
            QUIT_BUTTON = Button(pos=(200, 530), text_input="QUIT", font=get_font(), base_color="#0d0003", hovering_color="red")
            WIN.blit(MENU_TEXT, MENU_RECT)
            
            Dev_text = pygame.font.SysFont('Consolas',15).render("Developed by-", True, "#0d15ff")
            Dev_rect = Dev_text.get_rect(center=(200, 700))
            WIN.blit(Dev_text, Dev_rect)
            
            Dev_text1 = pygame.font.SysFont('Consolas',15).render("Turjo (1907003) & Hasib (1907006)", True, "#00000d")
            Dev_rect1 = Dev_text.get_rect(center=(120,720))
            WIN.blit(Dev_text1, Dev_rect1)
            
            for button in [PLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(WIN)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        select_dificulty()
                    elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()

    main_menu()

main()