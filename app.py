import pygame
import numpy as np

class Doc_Game():
    def __init__(self, tam):
        pygame.init()
        self.tam = tam
        self.windows_size = 500
        self.dist =  self.windows_size // (self.tam + 1)
        self.matrix()

        self.win = pygame.display.set_mode((self.windows_size,self.windows_size))
        pygame.display.set_caption("Doc Box Game")
        self.run = True
        self.position_points = []
        self.load_box = True

        self.player1 = False
        self.player2 = False

        self.points_player1 = 0
        self.points_player2 = 0


        self.lines = []

        self.toggle_player(True)
#============================================================
    def play(self):
        while self.run:
            pygame.time.delay(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    self.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    #draw the line
                    self.draw_line(pygame.mouse.get_pos())
                    
                    #sum points
                    self.sum_points()
                    
                    #Toggle user
                    self.change_player()

                    #show matrix
                    self.show_matrix()
                    
                    

                    

                # print(event)

            #Show the board to play
            if self.load_box:
                self.draw_points()
                self.load_box = False
            
#============================================================
    def draw_line(self, position):
        x_click, y_click = position
        run_line = True
        
        for i, row_value in enumerate(self.position_points):
            for j, col_value in enumerate(row_value):
                # print(col_value, end=',')
                x, y = col_value
                rango = 15
                try:
                    next_x = self.position_points[i][j+1][0]
                    next_y = self.position_points[i][j+1][1]
                
                    #=====================HORIZONTAl=====================
                    if (y_click >= y -rango) and (y_click <= y+rango): 
                        if (x_click >= x) and (x_click <= next_x):
                            if self.evaluate_lines(x, y,next_x, y):    
                                self.lines.append( (x, y,next_x, y ))
                                pygame.draw.line(self.win, self.color, [x, y], [next_x, y], 2)
                                self.top_botton[i,j] = 1
                                pygame.display.update()
                                return
                    next_y = self.position_points[i+1][j][1]    


                    #=====================VERTICAL=====================
                    if (x_click >= x - rango) and (x_click <= x+rango): 
                        # print("Vertical\n(Points= x:{}, y:{}), NEXT = (x+1:{}, y+1:{}), USER =( x:{}, user y:{})".format(x, y, next_x, next_y, x_click, y_click))
                        if (y_click >= y) and (y_click <= next_y):
                            if self.evaluate_lines(x, y, x, next_y):
                                self.lines.append( (x, y, x, next_y ))
                                pygame.draw.line(self.win, self.color, [x, y], [x,next_y], 2)
                                self.left_right[i,j] = 1
                                pygame.display.update()
                                return
                    #=====================VERTICAL ERROR =====================                    
                except:
                    final_point_x = self.position_points[i][-1][0]
                    final_point_y = self.position_points[i][-1][1]
                    try:
                        next_y = self.position_points[i+1][-1][1]
                    except:
                        # print('error')
                        run_line = False
                    if run_line: 
                        if (x_click >= final_point_x - rango):
                            if (y_click >= y) and (y_click <= next_y):
                                # print("Points ({}, {}), Click ({}, {}), Next ({}, {})".format(x, y, x_click, y_click,final_point_x, next_y))# final_point_x, x_click, y_click))
                                if self.evaluate_lines(final_point_x, y, final_point_x, next_y):
                                    self.lines.append( (final_point_x, y, final_point_x, next_y ))
                                    pygame.draw.line(self.win, self.color, [final_point_x, y], [final_point_x,next_y], 2)
                                    self.left_right[i,j] = 1
                                    
                                    pygame.display.update()
#============================================================
    def draw_points(self, radius = 5):
        arr_points = []
        for row in range(1, self.tam +1 ):
            for col in range(1,self.tam +1) :
                self.draw_circle(self.dist *col, self.dist*row, radius)
                arr_points.append( (self.dist *col, self.dist*row) )
            self.position_points.append(arr_points)
            arr_points = []
#===========================================================
    def draw_circle(self, x, y, r):
        pygame.draw.circle(self.win, (255,255,255), (x,y) ,r)
        pygame.display.update()
#===========================================================
    def toggle_player(self, gamer=False):
        if gamer:
            # print("Player 1")
            self.color = (255,0,0)
            self.c1 = 'Red'
            self.player1 = True
            self.player2 = False
        else:
            # print("Player 2"

            self.color = (0,255,0)
            self.c2 = 'Green'
            self.player2 = True
            self.player1 = False
#===========================================================
    def evaluate_lines(self, x1, y1, x2, y2):
        points = tuple([x1, y1, x2, y2])
        for line in self.lines:
            if points == line:
                # print(points, line)
                self.change_player()
                return False
        #since if reach here, change the user
        #Toggle user
        return True
#===========================================================
    def matrix(self):
        self.left_right = np.zeros( (self.tam -1, self.tam) )
        self.top_botton = np.zeros( (self.tam, self.tam -1) ) 
#===========================================================
    def rotate_matrix(self):
        print("============================")
        print("LEFTRIGHT\n",self.left_right)
        print("TRANSPOSE\n", np.transpose(self.top_botton))
        print("============================")

#===========================================================
    def show_matrix(self):
        print(self.left_right)
        print(self.top_botton)
#===========================================================
    def sum_points(self):
        for i, horizontal_line in enumerate(self.left_right):
            for j in range(1, len(horizontal_line)):
                if horizontal_line[j-1] == 1 and horizontal_line[j] == 1:
                    if self.top_botton[i][j-1] == 1 and self.top_botton[i+1][j-1]:
                        if self.player1:
                            self.points_player1 += 1
                        else:
                            self.points_player2 += 1
                        
                        self.left_right[i][j-1] = -1
                        #show points
                        print("Points: {}, Player {}".format(self.points_player1, self.c1))
                        print("Points: {}, Player {}".format(self.points_player2, self.c2))
#===========================================================
    def change_player(self):
        if self.player1:
            self.toggle_player()
        else:
            self.toggle_player(True)

    def exit(self):
        pygame.quit()
#===========================================================

game = Doc_Game(4)
game.play()