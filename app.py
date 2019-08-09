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

        self.black = (0,0,0)
        self.white = (255,255,255)

        self.font = pygame.font.SysFont("arial", 15)
        self.text1 = self.font.render("  RED: ", True, self.white)
        self.win.blit(self.text1, (0,0))

        self.text2 = self.font.render("GREEN: ", True, self.white)
        self.win.blit(self.text2, (self.windows_size - (self.text2.get_width() *2), 0))


        self.show_points(0, (0,0), self.text1.get_width() )
        self.show_points(0, (self.windows_size - (self.text2.get_width() * 2),0), self.text2.get_width() )
        
        # self.show_points(0, (self.windows_size - text.get_width()), text2.get_width())

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

                    self.clean_player([self.windows_size // 2, 0])


                    #show matrix
                    # self.show_matrix()
                # print(event)
            
            #Show the board to play
            if self.load_box:
                self.draw_points()
                self.load_box = False
            
            #update game
            pygame.display.update()
            
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
                    if (y_click >= y - rango) and (y_click <= y+rango): 
                        if (x_click >= x + 5) and (x_click <= next_x -5):
                            if self.evaluate_lines(x, y,next_x, y):    
                                
                                #store the position where line going to be draw
                                self.lines.append( (x, y,next_x, y ))
                                
                                self.change_player()

                                #draw the line
                                pygame.draw.line(self.win, self.color, [x, y], [next_x, y], 2)
                                
                                #fill up the matrix
                                self.top_botton[i,j] = 1  
                                
                                return
                    #=====================VERTICAL=====================
                    next_y = self.position_points[i+1][j][1]   

                    if (x_click >= x - rango) and (x_click <= x+rango): 
                        # print("Vertical\n(Points= x:{}, y:{}), NEXT = (x+1:{}, y+1:{}), USER =( x:{}, user y:{})".format(x, y, next_x, next_y, x_click, y_click))
                        if (y_click >= y + 10) and (y_click <= next_y - 10):
                            print("Click: {},{}, Range: {}, {}".format(x_click, y_click, y - rango , y+rango))
                            if self.evaluate_lines(x, y, x, next_y):
                                self.lines.append( (x, y, x, next_y ))

                                #Toggle user
                                self.change_player()

                                #Draw the line
                                pygame.draw.line(self.win, self.color, [x, y], [x,next_y], 2)
                                
                                #Store the value in the matrix
                                self.left_right[i,j] = 1
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
                                    self.change_player()

                                    pygame.draw.line(self.win, self.color, [final_point_x, y], [final_point_x,next_y], 2)
                                    self.left_right[i,j] = 1
                                    
                                    #Toggle user
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
        # pygame.display.update()
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
                print("User is clicking line with color")
                return False
        #since if reach here, change the user
        #Toggle user
        return True
#===========================================================
    def matrix(self):
        self.left_right = np.zeros( (self.tam -1, self.tam) )
        self.top_botton = np.zeros( (self.tam, self.tam -1) )
#===========================================================
    def show_matrix(self):
        print(self.left_right)
        print(self.top_botton)
#===========================================================
    def sum_points(self):
        for i, vertical_line in enumerate(self.left_right):
            for j in range(1, len(vertical_line)):
                if vertical_line[j-1] == 1 and (vertical_line[j] == 1 or vertical_line[j] == -1):
                    if self.top_botton[i][j-1] == 1 and self.top_botton[i+1][j-1]:
                        if self.player1:
                            for x in range(5):
                                self.remove_text(self.points_player1, (self.text1.get_width(),0))
                                pygame.display.update()

                            self.points_player1 += 1

                            self.show_points(self.points_player1, (0,0), self.text1.get_width())
                        else:

                            for x in range(10):
                                self.remove_text(self.points_player2, (self.windows_size - (self.text2.get_width() * 2) + self.text2.get_width() , 0))

                            self.points_player2 += 1                            
                            self.show_points(self.points_player2, (self.windows_size - (self.text2.get_width() * 2), 0), self.text2.get_width() )
                        self.fill_square( (i, j-1), (i,j), (i+1, j-1))
                        
                        self.left_right[i][j-1] = -1
#===========================================================
    def fill_square(self, p1, p2, p3):
        point1 = (self.windows_size / (len(self.position_points[0]) + 1 ))
        
        #first point
        fp1 = point1 + p1[0] * (point1)
        fp2 = point1 + p1[1] * (point1)

        # #Second point
        # sp1 = point1 + p2[0] * (point1)
        # sp2 = point1 + p2[1] * (point1)

        # #Four point
        # fop1 = point1 + p3[0] * (point1)
        # fop2 = point1 + p3[1] * (point1)

        # #3r point
        # tp1 = sp2        
        # tp2 = fop1 

        pygame.draw.rect(self.win, self.color, [fp2 + point1//4 , fp1 + point1//4, point1//2, point1//2])
        # pygame.display.update()
        # print("Point 1", fp1, fp2)
#===========================================================
    def remove_text(self, point, text_position):
        text = self.font.render("{}".format(point), True, self.black)
        self.win.blit(text, (text_position[0], text_position[1]))
        
    def show_points(self, points, text_position, text_width):
        text = self.font.render("{}".format(points), True, self.white)
        self.win.blit(text, (text_position[0] + text_width, text_position[1]) )
        pygame.display.update()
#===========================================================
    def change_player(self):
        if self.player1:
            self.toggle_player()
        else:
            self.toggle_player(True)
#===========================================================
    def clean_player(self, pos):
        pygame.draw.rect(self.win, self.color, [pos[0] - self.dist//2, pos[1], self.dist + self.dist//2,self.dist//2])
#===========================================================
    def exit(self):
        pygame.quit()
#===========================================================

game = Doc_Game(10)
game.play()