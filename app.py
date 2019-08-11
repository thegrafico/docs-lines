"""
Author: Raul Pichardo Avalo
Date: August 2019

Dots and Box Game
Take more boxes than your opponent. You move by connecting two dots with a line. 
When you place the last ‘wall’ of a single square (box), the box is yours. The players 
move in turn, but whenever a player takes a box (s)he must move again. The board game 
ends when all 25 boxes have been taken. The player with the most boxes wins.

When all four of the lines around a single box are in place, the player who 
made the last move owns the box. The box is marked in that player’s color and 
(s)he must move again.
"""

import pygame
import numpy as np

class Dots_Game():
    def __init__(self, tam):
        pygame.init()
        """
        Setup of the gamme
        """
        #How many docs will be in the board
        self.tam = tam

        #size of the windows to play the game
        self.windows_size = 500

        #choose the distance between the points 
        self.dist =  self.windows_size // (self.tam + 1)
        
        #create matrix to store user line position
        self.matrix()

        #screem to play
        self.win = pygame.display.set_mode((self.windows_size,self.windows_size))
        
        #Title of the game
        pygame.display.set_caption("Docs Box Game")

        #Variables of the game
        self.run = True
        self.position_points = []
        self.load_box = True
        
        #Players
        self.player1 = False
        self.player2 = False
        
        self.points_player1 = 0
        self.points_player2 = 0
        
        #Colors
        self.black = (0,0,0)
        self.white = (255,255,255)

        #text show player points
        self.font = pygame.font.SysFont("arial", 15)
        self.text1 = self.font.render("  RED: ", True, self.white)
        self.win.blit(self.text1, (0,0))

        self.text2 = self.font.render("GREEN: ", True, self.white)
        self.win.blit(self.text2, (self.windows_size - (self.text2.get_width() *2), 0))

        #Show points of the player
        self.show_points(0, (0,0), self.text1.get_width() )
        self.show_points(0, (self.windows_size - (self.text2.get_width() * 2),0), self.text2.get_width() )
        
        #store the position of the lines
        self.lines = []

        #Change the user player
        self.toggle_player(True)
#============================================================
    def play(self):
        """
        Start the game
        """
        while self.run:
            pygame.time.delay(100)

            #Look for event every 100 miliseconds 
            for event in pygame.event.get():

                #Exit from the game
                if event.type == pygame.QUIT:
                    self.run = False        
                    pygame.display.update()
                    self.exit()

                #if the user click in the windows
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    #draw the line in the position the user click
                    self.draw_line(pygame.mouse.get_pos())
                    
                    #sum points
                    self.sum_points()

                    self.show_color_rect_player([self.windows_size // 2, 0])
            
            #Show the board to play only one time
            if self.load_box:
                self.draw_points()
                self.load_box = False
            
            try:
                #update the screen game
                pygame.display.update()
            except:
                pass
#============================================================
    def draw_line(self, position):
        """
        Draw the line taking the position of the user click
        Position: (x,y) tuple, with the position user click
        """
        #position when user click
        x_click, y_click = position

        #Evaluate last condition
        run_line = True

        #Iterating trough the board        
        for i, row_value in enumerate(self.position_points):
            for j, col_value in enumerate(row_value):
                
                #Position of the points in the board below the user click
                x, y = col_value

                #range to take in consideration the user click
                rango = 15
                try:
                    #Getting the position of the point ahead of the user click
                    next_x = self.position_points[i][j+1][0]
                    next_y = self.position_points[i][j+1][1]
                
                    #=====================HORIZONTAl=====================
                    #if the user click between two points horizontal in the board,
                    # then draw a line between those points
                    if (y_click >= y - rango) and (y_click <= y+rango): 
                        if (x_click >= x + 5) and (x_click <= next_x -5):
                            
                            #Verify is the user is clicking a line that is already draw
                            if self.evaluate_lines(x, y,next_x, y):    
                                
                                #store the position where line going to be draw
                                self.lines.append( (x, y,next_x, y ))
                                
                                #Change the player
                                self.change_player()

                                #draw the line between points user click
                                pygame.draw.line(self.win, self.color, [x, y], [next_x, y], 2)
                                
                                #fill up the matrix
                                self.top_botton[i,j] = 1  
                                
                                #finish this function over here
                                return
                    #=====================VERTICAL=====================

                    #Getting the position of the point in the y-axis below the user click
                    next_y = self.position_points[i+1][j][1]   

                    #if the user click in the range when 2 points are alingned verticaly
                    if (x_click >= x - rango) and (x_click <= x+rango): 
                        if (y_click >= y + 10) and (y_click <= next_y - 10):
                            
                            #Verify if there is not line between 2 points user is clicking
                            if self.evaluate_lines(x, y, x, next_y):

                                #store the line position
                                self.lines.append( (x, y, x, next_y ))

                                #Toggle user
                                self.change_player()

                                #Draw the line
                                pygame.draw.line(self.win, self.color, [x, y], [x,next_y], 2)
                                
                                #Store the value in the matrix
                                self.left_right[i,j] = 1

                                #Finish function over here
                                return
                    #=====================VERTICAL ERROR =====================
                    # Index out of range error. this is because we are evaluating the last points
                    # with the next point, but there is not next points                    
                except:
                    #Getting the position x,y of the last points horizontaly in the board
                    final_point_x = self.position_points[i][-1][0]
                    final_point_y = self.position_points[i][-1][1]
                    try:
                        #Getting the last point in the board verticaly
                        next_y = self.position_points[i+1][-1][1]
                    except:
                        #if the code get here thats mean the last point in the board is reached
                        run_line = False
                    
                    #is the last point of the board is not reached
                    if run_line: 

                        #Verify where the user click and get those points
                        if (x_click >= final_point_x - rango):
                            if (y_click >= y) and (y_click <= next_y):
                                
                                #verify is the line is empty
                                if self.evaluate_lines(final_point_x, y, final_point_x, next_y):

                                    #Save the line position
                                    self.lines.append( (final_point_x, y, final_point_x, next_y ))
                                    
                                    #change user
                                    self.change_player()
                                    
                                    #Draw line
                                    pygame.draw.line(self.win, self.color, [final_point_x, y], [final_point_x,next_y], 2)
                                    
                                    #fill the matrix
                                    self.left_right[i,j] = 1
#============================================================
    def draw_points(self, radius = 5):
        """
        Draw all docs in the board
        radius: radius of the doc
        """
        arr_points = []
        #Iterate trought the windows and draw all pints
        for row in range(1, self.tam +1 ):
            for col in range(1,self.tam +1) :
                
                
                #call the function to draw the circle
                self.draw_circle(self.dist *col, self.dist*row, radius)
                
                #add the position of the point to a list
                arr_points.append( (self.dist *col, self.dist*row) )

            #store the arr_poiints to a new array and clean it
            self.position_points.append(arr_points)
            arr_points = []
#===========================================================
    def draw_circle(self, x, y, r):
        """
        Draw the circle in the board
        x: Position in x
        y: position in y
        r: radius
        """
        pygame.draw.circle(self.win, (255,255,255), (x,y) ,r)
#===========================================================
    def toggle_player(self, gamer=False):
        """
        Toggle the player
        """
        if gamer:
            # print("Player 1")
            self.color = (255,0,0)
            self.color_next_player = (0,255,0)
            self.c1 = 'Red'
            self.player1 = True
            self.player2 = False
        else:
            # print("Player 2"
            self.color = (0,255,0)
            self.color_next_player = (255,0,0)
            self.c2 = 'Green'
            self.player2 = True
            self.player1 = False
#===========================================================
    def evaluate_lines(self, x1, y1, x2, y2):
        """
        Verify is the line with the position x1,y1,x2,y2 is empty
        """
        points = tuple([x1, y1, x2, y2])
        
        #Iterate all over the lines in the list with have the lines draw
        for line in self.lines:

            #if the line have a color
            if points == line:
                # print("User is clicking line with color")
                return False
        #if the line is empty
        return True
#===========================================================
    def matrix(self):
        """
        Create the matrix of the game depending the size of the board.
        """
        self.left_right = np.zeros( (self.tam -1, self.tam) )
        self.top_botton = np.zeros( (self.tam, self.tam -1) )
#===========================================================
    def show_matrix(self):
        """
        Display the matrix in the console
        """
        print(self.left_right)
        print(self.top_botton)
#===========================================================
    def sum_points(self):
        """
        Sum points to the user who end fill a box
        """
        change = False
        #Iterate trought the matrix that have all the position of the lines verticaly
        for i, vertical_line in enumerate(self.left_right):
            for j in range(1, len(vertical_line)):

                #Verify the value in the matrix to sum a point
                if vertical_line[j-1] == 1 and (vertical_line[j] == 1 or vertical_line[j] == -1):
                    if self.top_botton[i][j-1] == 1 and self.top_botton[i+1][j-1]:
                        
                        #Verify the player
                        if self.player1:

                            #Clean the points for player 1
                            for x in range(5):
                                self.remove_text(self.points_player1, (self.text1.get_width(),0))
                                pygame.display.update()
                            
                            #Sum a point
                            self.points_player1 += 1

                            #show the point in the the screen 
                            self.show_points(self.points_player1, (0,0), self.text1.get_width())
                        else:
                            
                            #Clean the points for player 2
                            for x in range(10):
                                self.remove_text(self.points_player2, (self.windows_size - (self.text2.get_width() * 2) + self.text2.get_width() , 0))

                            #Sum point
                            self.points_player2 += 1                            
                            
                            #show points of player 2
                            self.show_points(self.points_player2, (self.windows_size - (self.text2.get_width() * 2), 0), self.text2.get_width() )
                                
                        #if the user get the box fill up, draw a box with the color of the user
                        self.fill_square( (i, j-1))
                        
                        self.left_right[i][j-1] = -1
                        
                        change = True
                        #Toggle user
                        # self.toggle_player()
        if change:
            # Toggle user
            self.change_player()
            

#===========================================================
    def fill_square(self, p1):
        """
        Create a inner box with the color of the user that complete a square. 
        p1: point with the firts x, and the firts y. with these 2 values we can draw the square
        in the position that we want. 
        """

        #Calculate point
        point1 = (self.windows_size / (len(self.position_points[0]) + 1 ))
        
        #Calculate point position
        fp1 = point1 + p1[0] * (point1)
        fp2 = point1 + p1[1] * (point1)

        #Draw the square using the the calculation    
        pygame.draw.rect(self.win, self.color, [fp2 + point1//4 , fp1 + point1//4, point1//2, point1//2])

#===========================================================
    def remove_text(self, point, text_position):
        """
        Clean the screen
        """
        text = self.font.render("{}".format(point), True, self.black)
        self.win.blit(text, (text_position[0], text_position[1]))
        
    def show_points(self, points, text_position, text_width):
        """
        Update the screen with the points of the player
        """
        #draw the text with the points
        text = self.font.render("{}".format(points), True, self.white)
        
        #show in the screen 
        self.win.blit(text, (text_position[0] + text_width, text_position[1]) )
        pygame.display.update()
#===========================================================
    def change_player(self):
        """
        change the player
        """
        if self.player1:
            self.toggle_player()
        else:
            self.toggle_player(True)
#===========================================================
    def show_color_rect_player(self, pos):
        """
        Draw a rect in the middle of the screen with the color of the player who play. 
        """
        pygame.draw.rect(self.win, self.color_next_player, [pos[0] - self.dist//2, pos[1], self.dist + self.dist//2,self.dist//2])
#===========================================================
    def exit(self):
        """
        Finish the game
        """
        pygame.quit()
#===========================================================

#Start playing
#the board is 10x10
game = Dots_Game(10)
game.play()