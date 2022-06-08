# PyChess
# Authored by Alex Wolfe on 5/29/2022



import graphics
import copy
import random
import time

# Classes List

class Board():
    def __init__(self):
        self.player1score = 16
        self.player2score = 16
        self.totalalive = self.player1score + self.player2score
        self.drawmoves = True


class Text():
    def __init__(self,windowsize):
        self.block = graphics.Text(graphics.Point(windowsize/2,12*windowsize/13),'')
        self.block2 = graphics.Text(graphics.Point(windowsize/2,windowsize/15),'')

    # Define different text events that display on the screen throughout the game
    def Player1turn(self,win):
        self.block.undraw()
        self.block.setText('Player 1 Turn')
        self.block.setTextColor('black')
        self.block.setSize(15)
        self.block.draw(win)

    def Player2turn(self,win):
        self.block.undraw()
        self.block.setText('Player 2 Turn')
        self.block.setTextColor('black')
        self.block.setSize(15)
        self.block.draw(win)

    def Player1win(self,win,color):
        self.block.undraw()
        self.block.setText('Player 1 Wins!')
        self.block.setTextColor(color)
        self.block.setSize(20)
        self.block.draw(win)

    def Player2win(self,win,color):
        self.block.undraw()
        self.block.setText('Player 2 Wins!')
        self.block.setTextColor(color)
        self.block.setSize(20)
        self.block.draw(win)

    def Check(self,win):
        self.block2.undraw()
        self.block2.setText('Check')
        self.block2.setTextColor('black')
        self.block2.setSize(22)
        self.block2.draw(win)
    
    def Checkmate(self,win,winnercolor):
        self.block2.undraw()
        self.block2.setText('Checkmate!')
        self.block2.setTextColor(winnercolor)
        self.block2.setSize(22)
        self.block2.draw(win)

    def Promotion(self,win):
        self.block2.undraw()
        self.block2.setText('Choose a Piece')
        self.block2.setTextColor('black')
        self.block2.setSize(20)
        self.block2.draw(win)


class Square():
    def __init__(self):
        self.occupied = False
        self.team = 'none'
        self.piece = 'none'
        self.pos = [0,0]

    def Draw(self,win,p1,p2,outline):
        self.p1 = p1
        self.p2 = p2
        square = graphics.Rectangle(p1,p2)
        square.setFill(self.color)
        square.setOutline(outline)
        square.draw(win)
        self.center = graphics.Point((p1.x+p2.x)/2,(p1.y+p2.y)/2)

    def SetColor(self,color):
        self.color = color

    # Places a selected piece on a selected square
    def SetPiece(self,win,piece):
        self.occupied = True
        self.piece = piece
        self.piecetype = piece.type
        self.team = piece.team
        match self.piecetype:
            case 'pawn':
                if self.team == 'player1':
                    image = graphics.Image(self.center,'pawn_white.png')
                    graphics.Image.draw(image,win)
                elif self.team == 'player2':
                    image = graphics.Image(self.center,'pawn_black.png')
                    graphics.Image.draw(image,win)
            case 'king':
                if self.team == 'player1':
                    image = graphics.Image(self.center,'king_white.png')
                    graphics.Image.draw(image,win)
                elif self.team == 'player2':
                    image = graphics.Image(self.center,'king_black.png')
                    graphics.Image.draw(image,win)
            case 'queen':
                if self.team == 'player1':
                    image = graphics.Image(self.center,'queen_white.png')
                    graphics.Image.draw(image,win)
                elif self.team == 'player2':
                    image = graphics.Image(self.center,'queen_black.png')
                    graphics.Image.draw(image,win)
            case 'knight':
                if self.team == 'player1':
                    image = graphics.Image(self.center,'knight_white.png')
                    graphics.Image.draw(image,win)
                elif self.team == 'player2':
                    image = graphics.Image(self.center,'knight_black.png')
                    graphics.Image.draw(image,win)
            case 'rook':
                if self.team == 'player1':
                    image = graphics.Image(self.center,'rook_white.png')
                    graphics.Image.draw(image,win)
                elif self.team == 'player2':
                    image = graphics.Image(self.center,'rook_black.png')
                    graphics.Image.draw(image,win)
            case 'bishop':
                if self.team == 'player1':
                    image = graphics.Image(self.center,'bishop_white.png')
                    graphics.Image.draw(image,win)
                elif self.team == 'player2':
                    image = graphics.Image(self.center,'bishop_black.png')
                    graphics.Image.draw(image,win)

    # Same as SetPiece, but without updating the piece images
    def SimSetPiece(self,piece):
        self.occupied = True
        self.piece = piece
        self.piecetype = piece.type
        self.team = piece.team
    
    def ClearSquare(self):
        self.occupied = False
        self.team = 'none'
        self.piece = 'none'
        match self.color:
            case 'royalblue':
                image = graphics.Image(self.center,'royalblue.png')
                graphics.Image.draw(image,win)
            case 'seashell':
                image = graphics.Image(self.center,'seashell.png')
                graphics.Image.draw(image,win)

    def SimClearSquare(self):
        self.occupied = False
        self.team = 'none'
        self.piece = 'none'
        

class Pawn():
    def __init__(self,team,pos):
        self.team = team
        self.type = 'pawn'
        self.pos = pos
        self.col = pos[0]
        self.row = pos[1]
        self.numberofmoves = 0

    def GetContestingMoves(self,squares,player):
        available = []
        self.col = self.pos[0]
        self.row = self.pos[1]
        if player == 'player1':
            if self.row > 0 and self.col > 0:
                if squares[self.col-1][self.row-1].team != player and squares[self.col-1][self.row-1].team != 'none':
                    available.append([self.col-1, self.row-1])
            if self.row > 0 and self.col < 7:
                if squares[self.col+1][self.row-1].team != player and squares[self.col+1][self.row-1].team != 'none':
                    available.append([self.col+1, self.row-1])
        else:
            if self.row < 7 and self.col < 7:
                if squares[self.col+1][self.row+1].team != player and squares[self.col+1][self.row+1].team != 'none':
                    available.append([self.col+1, self.row+1])
            if self.row < 7 and self.col > 0:
                if squares[self.col-1][self.row+1].team != player and squares[self.col-1][self.row+1].team != 'none':
                    available.append([self.col-1, self.row+1])
        return available

    # Gets all available moves that a piece can make. Not counting check limitations
    def GetMoves(self,squares,player):
        available = []
        self.col = self.pos[0]
        self.row = self.pos[1]
        if player == 'player1':
            if self.numberofmoves == 0:
                if self.row > 1:
                    if squares[self.col][self.row-1].occupied is False and squares[self.col][self.row-2].occupied is False:
                        available.append([self.col, self.row-2])
            if self.row > 0:
                if squares[self.col][self.row-1].occupied is False:
                    available.append([self.col, self.row-1])
            if self.row > 0 and self.col > 0:
                if squares[self.col-1][self.row-1].team != player and squares[self.col-1][self.row-1].team != 'none':
                    available.append([self.col-1, self.row-1])
            if self.row > 0 and self.col < 7:
                if squares[self.col+1][self.row-1].team != player and squares[self.col+1][self.row-1].team != 'none':
                    available.append([self.col+1, self.row-1])
            if self.col < 7 and self.row == 3:
                if squares[self.col+1][self.row].occupied and squares[self.col+1][self.row].team != player:
                    if squares[self.col+1][self.row].piece.numberofmoves == 1:
                        available.append([self.col+1,self.row-1])
            if self.col > 0 and self.row == 3:
                if squares[self.col-1][self.row].occupied and squares[self.col-1][self.row].team != player:
                    if squares[self.col-1][self.row].piece.numberofmoves == 1:
                        available.append([self.col-1,self.row-1])
        else:
            if self.numberofmoves == 0:
                if self.row < 6:
                    if squares[self.col][self.row+1].occupied is False and squares[self.col][self.row+2].occupied is False:
                        available.append([self.col, self.row+2])
            if self.row < 7:
                if squares[self.col][self.row+1].occupied is False:
                    available.append([self.col, self.row+1])
            if self.row < 7 and self.col < 7:
                if squares[self.col+1][self.row+1].team != player and squares[self.col+1][self.row+1].team != 'none':
                    available.append([self.col+1, self.row+1])
            if self.row < 7 and self.col > 0:
                if squares[self.col-1][self.row+1].team != player and squares[self.col-1][self.row+1].team != 'none':
                    available.append([self.col-1, self.row+1])
            if self.col < 7 and self.row == 4:
                if self.row == 4 and squares[self.col+1][self.row].occupied and squares[self.col+1][self.row].team != player:
                    if squares[self.col+1][self.row].piece.numberofmoves == 1:
                        available.append([self.col+1,self.row+1])
            if self.col > 0 and self.row == 4:
                if squares[self.col-1][self.row].occupied and squares[self.col-1][self.row].team != player:
                    if squares[self.col-1][self.row].piece.numberofmoves == 1:
                        available.append([self.col-1,self.row+1])
        return available


class King():
    def __init__(self,team,pos):
        self.team = team
        self.type = 'king'
        self.pos = pos
        self.col = pos[0]
        self.row = pos[1]
        self.numberofmoves = 0

    def GetMoves(self,squares,player):
        available = []
        self.col = self.pos[0]
        self.row = self.pos[1]
        if self.row > 0:
            if squares[self.col][self.row-1].team != player:
                available.append([self.col, self.row-1])
        if self.row < 7:
            if squares[self.col][self.row+1].team != player:
                available.append([self.col, self.row+1])
        if self.col > 0:
            if squares[self.col-1][self.row].team != player:
                available.append([self.col-1, self.row])
        if self.col < 7:
            if squares[self.col+1][self.row].team != player:
                available.append([self.col+1, self.row])
        if self.row > 0 and self.col > 0:
            if squares[self.col-1][self.row-1].team != player:
                available.append([self.col-1, self.row-1])
        if self.row > 0 and self.col < 7:
            if squares[self.col+1][self.row-1].team != player:
                available.append([self.col+1, self.row-1])
        if self.row < 7 and self.col > 0:
            if squares[self.col-1][self.row+1].team != player:
                available.append([self.col-1, self.row+1])
        if self.row < 7 and self.col < 7:
            if squares[self.col+1][self.row+1].team != player:
                available.append([self.col+1, self.row+1])
        return available

    # Bool function used to determine if king is in check
    def InCheck(self,squares):
        contested = []
        for k in range(0,8):
            for j in range(0,8):
                if squares[k][j].occupied is True and squares[k][j].team != self.team:
                    results = squares[k][j].piece.GetMoves(squares,squares[k][j].team)
                    for i in range(len(results)):
                        contested.append(results[i])
        if self.pos in contested:
            return True
        else:
            return False


class Queen():
    def __init__(self,team,pos):
        self.team = team
        self.type = 'queen'
        self.pos = pos
        self.col = pos[0]
        self.row = pos[1]
        self.numberofmoves = 0

    def GetMoves(self,squares,player):
        available = []
        self.col = self.pos[0]
        self.row = self.pos[1]
        for k in range(1,8):
            if self.col+k <= 7 and self.row-k >= 0:
                if squares[self.col+k][self.row-k].occupied is False:
                    available.append([self.col+k, self.row-k])
                elif squares[self.col+k][self.row-k].team != player:
                    available.append([self.col+k, self.row-k])
                    break
                else:
                    break
            else:
                break
        for k in range(1,8):
            if self.col-k >= 0 and self.row-k >= 0:
                if squares[self.col-k][self.row-k].occupied is False:
                    available.append([self.col-k, self.row-k])
                elif squares[self.col-k][self.row-k].team != player:
                    available.append([self.col-k, self.row-k])
                    break
                else:
                    break
            else:
                break           
        for k in range(1,8):
            if self.col-k >= 0 and self.row+k <= 7:
                if squares[self.col-k][self.row+k].occupied is False:
                    available.append([self.col-k, self.row+k])
                elif squares[self.col-k][self.row+k].team != player:
                    available.append([self.col-k, self.row+k])
                    break
                else:
                    break
            else:
                break
        for k in range(1,8):
            if self.col+k <= 7 and self.row+k <= 7:
                if squares[self.col+k][self.row+k].occupied is False:
                    available.append([self.col+k, self.row+k])
                elif squares[self.col+k][self.row+k].team != player:
                    available.append([self.col+k, self.row+k])
                    break
                else:
                    break
            else:
                break
        for k in range(self.row+1,8):
            if squares[self.col][k].occupied is False:
                available.append([self.col,k])
            elif squares[self.col][k].team != player:
                available.append([self.col,k])
                break
            else:
                break
        for k in range(self.row-1,-1,-1):
            if squares[self.col][k].occupied is False:
                available.append([self.col,k])
            elif squares[self.col][k].team != player:
                available.append([self.col,k])
                break
            else:
                break
        for k in range(self.col+1,8):
            if squares[k][self.row].occupied is False:
                available.append([k,self.row])
            elif squares[k][self.row].team != player:
                available.append([k,self.row])
                break
            else:
                break
        for k in range(self.col-1,-1,-1):
            if squares[k][self.row].occupied is False:
                available.append([k,self.row])
            elif squares[k][self.row].team != player:
                available.append([k,self.row])
                break
            else:
                break
        return available


class Knight():
    def __init__(self,team,pos):
        self.team = team
        self.type = 'knight'
        self.pos = pos
        self.col = pos[0]
        self.row = pos[1]
        self.numberofmoves = 0

    def GetMoves(self,squares,player):
        available = []
        self.col = self.pos[0]
        self.row = self.pos[1]
        if self.row > 0 and self.col > 1:
            if squares[self.col-2][self.row-1].team != player:
                available.append([self.col-2,self.row-1])
        if self.row > 1 and self.col > 0:
            if squares[self.col-1][self.row-2].team != player:
                available.append([self.col-1, self.row-2])
        if self.row > 0 and self.col < 6:
            if squares[self.col+2][self.row-1].team != player:
                available.append([self.col+2,self.row-1])
        if self.row > 1 and self.col < 7:
            if squares[self.col+1][self.row-2].team != player:
                available.append([self.col+1, self.row-2])      
        if self.row < 7 and self.col > 1:
            if squares[self.col-2][self.row+1].team != player:
                available.append([self.col-2,self.row+1])
        if self.row < 6 and self.col > 0:
            if squares[self.col-1][self.row+2].team != player:
                available.append([self.col-1, self.row+2])
        if self.row < 7 and self.col < 6:
            if squares[self.col+2][self.row+1].team != player:
                available.append([self.col+2,self.row+1])
        if self.row < 6 and self.col < 7:
            if squares[self.col+1][self.row+2].team != player:
                available.append([self.col+1, self.row+2]) 
        return available


class Bishop():
    def __init__(self,team,pos):
        self.team = team
        self.type = 'bishop'
        self.pos = pos
        self.col = pos[0]
        self.row = pos[1]
        self.numberofmoves = 0

    def GetMoves(self,squares,player):
        available = []
        self.col = self.pos[0]
        self.row = self.pos[1]
        for k in range(1,8):
            if self.col+k <= 7 and self.row-k >= 0:
                if squares[self.col+k][self.row-k].occupied is False:
                    available.append([self.col+k, self.row-k])
                elif squares[self.col+k][self.row-k].team != player:
                    available.append([self.col+k, self.row-k])
                    break
                else:
                    break
            else:
                break
        for k in range(1,8):
            if self.col-k >= 0 and self.row-k >= 0:
                if squares[self.col-k][self.row-k].occupied is False:
                    available.append([self.col-k, self.row-k])
                elif squares[self.col-k][self.row-k].team != player:
                    available.append([self.col-k, self.row-k])
                    break
                else:
                    break
            else:
                break           
        for k in range(1,8):
            if self.col-k >= 0 and self.row+k <= 7:
                if squares[self.col-k][self.row+k].occupied is False:
                    available.append([self.col-k, self.row+k])
                elif squares[self.col-k][self.row+k].team != player:
                    available.append([self.col-k, self.row+k])
                    break
                else:
                    break
            else:
                break
        for k in range(1,8):
            if self.col+k <= 7 and self.row+k <= 7:
                if squares[self.col+k][self.row+k].occupied is False:
                    available.append([self.col+k, self.row+k])
                elif squares[self.col+k][self.row+k].team != player:
                    available.append([self.col+k, self.row+k])
                    break
                else:
                    break
            else:
                break
        return available


class Rook():
    def __init__(self,team,pos):
        self.team = team
        self.type = 'rook'
        self.pos = pos
        self.col = pos[0]
        self.row = pos[1]
        self.numberofmoves = 0

    def GetMoves(self,squares,player):
        available = []
        self.col = self.pos[0]
        self.row = self.pos[1]
        for k in range(self.row+1,8):
            if squares[self.col][k].occupied is False:
                available.append([self.col,k])
            elif squares[self.col][k].team != player:
                available.append([self.col,k])
                break
            else:
                break
        for k in range(self.row-1,-1,-1):
            if squares[self.col][k].occupied is False:
                available.append([self.col,k])
            elif squares[self.col][k].team != player:
                available.append([self.col,k])
                break
            else:
                break
        for k in range(self.col+1,8):
            if squares[k][self.row].occupied is False:
                available.append([k,self.row])
            elif squares[k][self.row].team != player:
                available.append([k,self.row])
                break
            else:
                break
        for k in range(self.col-1,-1,-1):
            if squares[k][self.row].occupied is False:
                available.append([k,self.row])
            elif squares[k][self.row].team != player:
                available.append([k,self.row])
                break
            else:
                break
        return available


# Functions List

def initializeGame(win,board,squaresize,team1color,team2color):
    board.player1score = 16
    board.player2score = 16
    drawPromoters(win,squaresize)
    # Create Array of Squares that make up game board
    squares = [[Square() for i in range(9)] for i in range(9)]
    for k in range(0,8):
        for j in range(0,8):
            squares[k][j].pos = [k,j]
            if (k+j) % 2:
                squares[k][j].SetColor(team2color)
            else:
                squares[k][j].SetColor(team1color)
            p1 = graphics.Point(k*squaresize+squaresize,j*squaresize+squaresize)
            p2 = graphics.Point(p1.x+squaresize,p1.y+squaresize)
            squares[k][j].Draw(win,p1,p2,'black')
    # Assign Pieces to squares in starting configuration
    for k in range(0,8):
        squares[k][6].SetPiece(win,Pawn('player1',[k,6]))
        squares[k][1].SetPiece(win,Pawn('player2',[k,1]))  
    squares[0][7].SetPiece(win,Rook('player1',[0,7]))
    squares[7][7].SetPiece(win,Rook('player1',[7,7]))
    squares[0][0].SetPiece(win,Rook('player2',[0,0]))
    squares[7][0].SetPiece(win,Rook('player2',[7,0]))
    squares[1][7].SetPiece(win,Knight('player1',[1,7]))
    squares[6][7].SetPiece(win,Knight('player1',[6,7]))
    squares[1][0].SetPiece(win,Knight('player2',[1,0]))
    squares[6][0].SetPiece(win,Knight('player2',[6,0]))
    squares[2][7].SetPiece(win,Bishop('player1',[2,7]))
    squares[5][7].SetPiece(win,Bishop('player1',[5,7]))
    squares[2][0].SetPiece(win,Bishop('player2',[2,0]))
    squares[5][0].SetPiece(win,Bishop('player2',[5,0]))
    squares[3][7].SetPiece(win,Queen('player1',[3,7]))
    squares[3][0].SetPiece(win,Queen('player2',[3,0]))
    kp1 = King('player1',[4,7])
    kp2 = King('player2',[4,0])
    squares[4][7].SetPiece(win,kp1)
    squares[4][0].SetPiece(win,kp2)
    drawMoveButton(win)
    drawexitButton(win)
    return [squares,kp1,kp2]

# Draws clickable piece images for promotion of pawns
def drawPromoters(win,squaresize):
    promoters = ['knight_black.png','bishop_black.png','rook_black.png','queen_black.png','knight_white.png','bishop_white.png','rook_white.png','queen_white.png']
    for i in range(4):
        p1 = graphics.Point(0,i*squaresize+3*squaresize)
        p2 = graphics.Point(p1.x+squaresize,p1.y+squaresize)
        center = graphics.Point((p1.x+p2.x)/2,(p1.y+p2.y)/2)
        image = graphics.Image(center,promoters[i])
        graphics.Image.draw(image,win)
    for k in range(4,8):
        p1 = graphics.Point(9*squaresize,(k-4)*squaresize+3*squaresize)
        p2 = graphics.Point(p1.x+squaresize,p1.y+squaresize)
        center = graphics.Point((p1.x+p2.x)/2,(p1.y+p2.y)/2)
        image = graphics.Image(center,promoters[k])
        graphics.Image.draw(image,win)

# Creates main game window
def CreateWindow(size,color):
    win = graphics.GraphWin('PyChess',size,size)
    win.setBackground(color) 
    return win  

# Handles start menu and choosing of game mode
def StartMenu(win,windowsize):
    background = graphics.Rectangle(graphics.Point(0,0),graphics.Point(windowsize,windowsize))
    background.setOutline(team1color)
    background.setFill(team1color)
    header = graphics.Text(graphics.Point(windowsize/2,windowsize/4),'PyChess')
    header.setSize(30)
    header.setTextColor(team2color)
    name = graphics.Text(graphics.Point(windowsize/2,9*windowsize/11),'by Alex Wolfe')
    name.setSize(15)
    name.setTextColor('black')
    kw = graphics.Image(graphics.Point(windowsize/5,windowsize/2),'king_white.png')
    kb = graphics.Image(graphics.Point(4*windowsize/5,windowsize/2),'king_black.png')
    rect1 = graphics.Rectangle(graphics.Point(windowsize/2-100,windowsize/2-50),graphics.Point(windowsize/2+100,windowsize/2+50))
    text1 = graphics.Text(graphics.Point(windowsize/2,windowsize/2),'2 Player Game')
    rect2 = graphics.Rectangle(graphics.Point(windowsize/2-100,windowsize/2+150-50),graphics.Point(windowsize/2+100,windowsize/2+150+50))
    text2 = graphics.Text(graphics.Point(windowsize/2,windowsize/2+150),'VS Computer')
    rect3 = graphics.Rectangle(graphics.Point(windowsize/2-50,12*windowsize/13-25),graphics.Point(windowsize/2+50,12*windowsize/13+25))
    text3 = graphics.Text(graphics.Point(windowsize/2,12*windowsize/13),'Quit')
    background.draw(win)
    header.draw(win)
    name.draw(win)
    kw.draw(win)
    kb.draw(win)
    rect1.draw(win)
    rect2.draw(win)
    rect3.draw(win)
    text1.draw(win)
    text2.draw(win)
    text3.draw(win)
    while True:
        click = win.getMouse()
        xcoord = int(click.x)
        ycoord = int(click.y)
        if xcoord > int(windowsize/2-100) and xcoord < int(windowsize/2+100) and ycoord > int(windowsize/2-50) and ycoord < int(windowsize/2+50):
            background.undraw()
            header.undraw()
            kw.undraw()
            kb.undraw()
            rect1.undraw()
            rect2.undraw()
            rect3.undraw()
            text1.undraw()
            text2.undraw()
            text3.undraw()
            return '2player'
        elif xcoord > int(windowsize/2-100) and xcoord < int(windowsize/2+100) and ycoord > int(windowsize/2+150-50) and ycoord < int(windowsize/2+150+50):
            header.undraw()
            background.undraw()
            kw.undraw()
            kb.undraw()
            rect1.undraw()
            rect2.undraw()
            rect3.undraw()
            text1.undraw()
            text2.undraw()
            text3.undraw()
            return 'cpu'
        elif xcoord > int(windowsize/2-50) and xcoord < int(windowsize/2+50) and ycoord > int(12*windowsize/13-25) and ycoord < int(12*windowsize/13+25):
            header.undraw()
            background.undraw()
            kw.undraw()
            kb.undraw()
            rect1.undraw()
            rect2.undraw()
            rect3.undraw()
            text1.undraw()
            text2.undraw()
            text3.undraw()
            return 'quit'

# Draws button that controls whether or not available moves are drawn
def drawMoveButton(win):
    box = graphics.Rectangle(graphics.Point(windowsize/2-60,720+10),graphics.Point(windowsize/2+60,720-10))
    q = graphics.Text(graphics.Point((box.p1.x+box.p2.x)/2,(box.p1.y+box.p2.y)/2),'Toggle Draw Moves')
    q.setSize(10)
    box.draw(win)
    q.draw(win)

# Takes in click coords, and checks whether or not draw move toggle button was clicked
def drawMoveToggle(board,x,y):
    if x > windowsize/2-60 and x < windowsize/2+60 and y > 720-10 and y < 720+10:
        if board.drawmoves:
            board.drawmoves = False
        else:
            board.drawmoves = True

# Draws quit to start menu button
def drawexitButton(win):
    box = graphics.Rectangle(graphics.Point(30,720+10),graphics.Point(130,720-10))
    q = graphics.Text(graphics.Point((box.p1.x+box.p2.x)/2,(box.p1.y+box.p2.y)/2),'Quit to Start')
    q.setSize(10)
    box.draw(win)
    q.draw(win)

# Take in click coords, and checks whether or not quit to start was clicked
def exitButton(x,y):
    if x > 30 and x < 130 and y > 720-10 and y < 720+10:
        return True
    return False
        
# Takes in available moves for a piece, and displays them on the board
def DrawAvailableMoves(available,squares,squaresize,win,board,selected):
    moveshapes = []
    if board.drawmoves:
        for k in range(len(available)):
            if squares[available[k][0]][available[k][1]].occupied and squares[available[k][0]][available[k][1]].team != selected.team:
                moveshapes.append(graphics.Rectangle(squares[available[k][0]][available[k][1]].p1,squares[available[k][0]][available[k][1]].p2))
                moveshapes[k].setOutline('red')
                moveshapes[k].setWidth(3)
                moveshapes[k].draw(win)
            elif squares[available[k][0]][available[k][1]].occupied:
                moveshapes.append(graphics.Circle(squares[available[k][0]][available[k][1]].center,squaresize/7))
                moveshapes[k].setFill('green')
                moveshapes[k].setWidth(3)
                moveshapes[k].draw(win)
            elif selected.piecetype == 'pawn' and available[k][0] != selected.pos[0]:
                moveshapes.append(graphics.Rectangle(squares[available[k][0]][available[k][1]].p1,squares[available[k][0]][available[k][1]].p2))
                moveshapes[k].setOutline('red')
                moveshapes[k].setWidth(3)
                moveshapes[k].draw(win)
            else:
                moveshapes.append(graphics.Circle(squares[available[k][0]][available[k][1]].center,squaresize/7))
                moveshapes[k].setFill('whitesmoke')
                moveshapes[k].draw(win)
    else:
        for k in range(len(available)):
            moveshapes.append(graphics.Rectangle(selected.p1,selected.p2))
            moveshapes[k].setOutline('darkorange')
            moveshapes[k].setWidth(4)
            moveshapes[k].draw(win)
    return moveshapes

# Erases display of available moves
def EraseMoveshapes(moveshapes):
    for k in range(len(moveshapes)):
        moveshapes[k].undraw()

# Takes in click x and y pos, and outputs col and row that was clicked on
def GetClickCoords(click):
    normx = click.x/squaresize
    normy = click.y/squaresize
    col = int((normx-1) // 1)
    row = int((normy-1) // 1)
    return [col,row]

# Castles the king and selected rook
def Castle(squares,selected,selected2):
    if selected2.pos[0] > selected.pos[0]:
        Move(squares,selected,squares[selected.pos[0]+2][selected.pos[1]],board)
        Move(squares,selected2,squares[selected.pos[0]+1][selected.pos[1]],board)
    else:
        Move(squares,selected,squares[selected.pos[0]-2][selected.pos[1]],board)
        Move(squares,selected2,squares[selected.pos[0]-1][selected.pos[1]],board)

# Moves a piece to an empty square, and checks for promotion of pawn and checks for en passant
def Move(squares,selected,selected2,board):
    team = selected.team
    selected.piece.pos = selected2.pos
    selected.piece.numberofmoves+=1
    if (selected.piecetype == 'pawn' and (selected.piece.pos[1] == 7 or selected.piece.pos[1] == 0)):
        text.Promotion(win)
        while True:
            click = win.getMouse()
            [x,y] = GetClickCoords(click)
            if team == 'player1':
                match [x,y]:
                    case [8,2]:
                        selected2.SetPiece(win,Knight('player1',selected.piece.pos))
                        selected2.piece.numberofmoves = selected.piece.numberofmoves
                        selected.ClearSquare()
                        break
                    case [8,3]:
                        selected2.SetPiece(win,Bishop('player1',selected.piece.pos))
                        selected2.piece.numberofmoves = selected.piece.numberofmoves
                        selected.ClearSquare()
                        break
                    case [8,4]:
                        selected2.SetPiece(win,Rook('player1',selected.piece.pos))
                        selected2.piece.numberofmoves = selected.piece.numberofmoves
                        selected.ClearSquare()
                        break
                    case [8,5]:
                        selected2.SetPiece(win,Queen('player1',selected.piece.pos))
                        selected2.piece.numberofmoves = selected.piece.numberofmoves
                        selected.ClearSquare()
                        break
            else:
                match [x,y]:
                    case [-1,2]:
                        selected2.SetPiece(win,Knight('player2',selected.piece.pos))
                        selected2.piece.numberofmoves = selected.piece.numberofmoves
                        selected.ClearSquare()
                        break
                    case [-1,3]:
                        selected2.SetPiece(win,Bishop('player2',selected.piece.pos))
                        selected2.piece.numberofmoves = selected.piece.numberofmoves
                        selected.ClearSquare()
                        break
                    case [-1,4]:
                        selected2.SetPiece(win,Rook('player2',selected.piece.pos))
                        selected2.piece.numberofmoves = selected.piece.numberofmoves
                        selected.ClearSquare()
                        break
                    case [-1,5]:
                        selected2.SetPiece(win,Queen('player2',selected.piece.pos))
                        selected2.piece.numberofmoves = selected.piece.numberofmoves
                        selected.ClearSquare()
                        break
    elif selected.piecetype == 'pawn' and selected2.pos[0] != selected.pos[0]:
        selected2.SetPiece(win,selected.piece)
        selected.ClearSquare()
        if team == 'player1':
            board.player2score-=1
            squares[selected2.pos[0]][selected2.pos[1]+1].ClearSquare()
        else:
            board.player1score-=1
            squares[selected2.pos[0]][selected2.pos[1]-1].ClearSquare()
    else:
        selected2.SetPiece(win,selected.piece)
        selected.ClearSquare()

# Simplified move function used in SimulateforCheck function
def SimMove(selected,selected2):
    selected.piece.pos = selected2.pos
    selected2.SimSetPiece(selected.piece)
    selected.SimClearSquare()

# Used by cpu to move a piece. CPU can only promote pawns to queens
def cpuMove(selected,selected2):
    team = selected.team
    selected.piece.pos = selected2.pos
    selected.piece.numberofmoves+=1
    if (selected.piecetype == 'pawn' and (selected.piece.pos[1] == 7 or selected.piece.pos[1] == 0)):
        if team == 'player1':
            selected2.ClearSquare()
            selected2.SetPiece(win,Queen('player1',selected2.pos))
            selected2.piece.numberofmoves = selected.piece.numberofmoves
            selected.ClearSquare()
        else:
            selected2.ClearSquare()
            selected2.SetPiece(win,Queen('player2',selected2.pos))
            selected2.piece.numberofmoves = selected.piece.numberofmoves
            selected.ClearSquare()
    else:
        selected2.SetPiece(win,selected.piece)
        selected.ClearSquare()

# Moves a piece to a occupied square, capturing the enemy piece. Checks for promotion of pawn
def Overtake(selected,selected2,board,team):
    if team == 'player1':
        board.player1score-=1
    else:
        board.player2score-=1
    selected.piece.numberofmoves+=1
    selected.piece.pos = selected2.piece.pos
    if (selected.piecetype == 'pawn' and (selected2.piece.row == 7 or selected2.piece.row == 0)):
        text.Promotion(win)
        while True:
            click = win.getMouse()
            [x,y] = GetClickCoords(click)
            if team == 'player1':
                match [x,y]:
                    case [-1,3]:
                        selected2.ClearSquare()
                        selected2.SetPiece(win,Knight('player1',selected2.piece.pos))
                        selected2.piece.numberofmoves = selected.piece.numberofmoves
                        selected.ClearSquare()
                        break
                    case [-1,4]:
                        selected2.ClearSquare()
                        selected2.SetPiece(win,Bishop('player1',selected2.piece.pos))
                        selected2.piece.numberofmoves = selected.piece.numberofmoves
                        selected.ClearSquare()
                        break
                    case [-1,5]:
                        selected2.ClearSquare()
                        selected2.SetPiece(win,Rook('player1',selected2.piece.pos))
                        selected2.piece.numberofmoves = selected.piece.numberofmoves
                        selected.ClearSquare()
                        break
                    case [-1,6]:
                        selected2.ClearSquare()
                        selected2.SetPiece(win,Queen('player1',selected2.piece.pos))
                        selected2.piece.numberofmoves = selected.piece.numberofmoves
                        selected.ClearSquare()
                        break
            else:
                match [x,y]:
                    case [8,3]:
                        selected2.ClearSquare()
                        selected2.SetPiece(win,Knight('player2',selected2.piece.pos))
                        selected2.piece.numberofmoves = selected.piece.numberofmoves
                        selected.ClearSquare()
                        break
                    case [8,4]:
                        selected2.ClearSquare()
                        selected2.SetPiece(win,Bishop('player2',selected2.piece.pos))
                        selected2.piece.numberofmoves = selected.piece.numberofmoves
                        selected.ClearSquare()
                        break
                    case [8,5]:
                        selected2.ClearSquare()
                        selected2.SetPiece(win,Rook('player2',selected2.piece.pos))
                        selected2.piece.numberofmoves = selected.piece.numberofmoves
                        selected.ClearSquare()
                        break
                    case [8,6]:
                        selected2.ClearSquare()
                        selected2.SetPiece(win,Queen('player2',selected2.piece.pos))
                        selected2.piece.numberofmoves = selected.piece.numberofmoves
                        selected.ClearSquare()
                        break
    else:
        selected2.piece.pos = [-1,-1]
        selected2.ClearSquare()
        selected2.SetPiece(win,selected.piece)
        selected.ClearSquare()

# Simplified overtake function used in SimulateforCheck function
def SimOvertake(selected,selected2):
    selected.piece.pos = selected2.piece.pos
    selected2.piece.pos = [-1,-1]
    selected2.SimClearSquare()
    selected2.SimSetPiece(selected.piece)
    selected.SimClearSquare()

# Used by cpu to overtake enemy piece
def cpuOvertake(selected,selected2,board,team):
    if team == 'player1':
        board.player1score-=1
    else:
        board.player2score-=1
    selected.piece.numberofmoves+=1
    selected.piece.pos = selected2.piece.pos
    if (selected.piecetype == 'pawn' and (selected2.piece.row == 7 or selected2.piece.row == 0)):
        if team == 'player1':
            selected2.ClearSquare()
            selected2.SetPiece(win,Queen('player1',selected2.piece.pos))
            selected2.piece.numberofmoves = selected.piece.numberofmoves
            selected.ClearSquare()
        else:
            selected2.ClearSquare()
            selected2.SetPiece(win,Queen('player2',selected2.piece.pos))
            selected2.piece.numberofmoves = selected.piece.numberofmoves
            selected.ClearSquare()
    else:
        selected2.piece.pos = [-1,-1]
        selected2.ClearSquare()
        selected2.SetPiece(win,selected.piece)
        selected.ClearSquare()

# Updates player piece score in top right and left of screen
def UpdateScore(board,p1scorenumber,p2scorenumber):
    p1score = board.player1score
    p1scorenumber.setText(str(p1score))
    p2score = board.player2score
    p2scorenumber.setText(str(p2score))

# Filters a set of available moves for a selected piece, removing moves 
#   that would cause the player to put themself in check
# Can be toggled between filtering for moves that do not put the player in check, and
#   filtering for moves that do put the enemy in check
# Done by simulating the move on a copied (dummy) board, and running the inCheck function
def SimulateforCheck(squares,availableprecheck,player,pos,type):
    passed = []
    checkmates = []
    col = pos[0]
    row = pos[1]
    if type == 'd':
        for l in range(len(availableprecheck)):
            dummysquares = copy.deepcopy(squares)
            dummyselected = dummysquares[col][row]
            dummyselected2 = dummysquares[availableprecheck[l][0]][availableprecheck[l][1]]
            if dummyselected2.occupied and dummyselected2.team != player:
                SimOvertake(dummyselected,dummyselected2)
            else:
                SimMove(dummyselected,dummyselected2)
            if player == 'player1':
                if dummyselected.piecetype == 'king':
                    if dummyselected2.piece.InCheck(dummysquares) is False:
                        passed.append(availableprecheck[l])
                else:
                    if kp1.InCheck(dummysquares) is False:
                        passed.append(availableprecheck[l])
            else:
                if dummyselected.piecetype == 'king':
                    if dummyselected2.piece.InCheck(dummysquares) is False:
                        passed.append(availableprecheck[l])
                else:
                    if kp2.InCheck(dummysquares) is False:
                        passed.append(availableprecheck[l])
        return passed
    elif type == 'a':
        for l in range(len(availableprecheck)):
            dummysquares = copy.deepcopy(squares)
            dummyselected = dummysquares[col][row]
            dummyselected2 = dummysquares[availableprecheck[l][0]][availableprecheck[l][1]]
            if dummyselected2.occupied and dummyselected2.team != player:
                SimOvertake(dummyselected,dummyselected2)
            else:
                SimMove(dummyselected,dummyselected2)
            if player == 'player1':
                    if kp2.InCheck(dummysquares):
                        passed.append(availableprecheck[l])
                    if CheckforMate(dummysquares,'player2'):
                        checkmates.append(availableprecheck[l])
            else:
                    if kp1.InCheck(dummysquares):
                        passed.append(availableprecheck[l])
                    if CheckforMate(dummysquares,'player1'):
                        checkmates.append(availableprecheck[l])
        return (passed,checkmates)   

# Adds move at rook if castling is a legal move
def checkCastling(squares,moves,team,pos):
    finalmoves = moves
    if squares[pos[0]+1][pos[1]].occupied is False and squares[pos[0]+3][pos[1]].occupied and squares[pos[0]+2][pos[1]].occupied is False and\
    squares[pos[0]+3][pos[1]].piece.numberofmoves == 0 and isContested(squares,[pos[0]+1,pos[1]],team) is False and\
    isContested(squares,[pos[0]+2,pos[1]],team) is False:
        finalmoves.append([pos[0]+3,pos[1]])
    if squares[pos[0]-1][pos[1]].occupied is False and squares[pos[0]-4][pos[1]].occupied and squares[pos[0]-2][pos[1]].occupied is False and\
    squares[pos[0]-3][pos[1]].occupied is False and squares[pos[0]-4][pos[1]].piece.numberofmoves == 0 and\
    isContested(squares,[pos[0]-1,pos[1]],team) is False and isContested(squares,[pos[0]-2,pos[1]],team) is False and\
    isContested(squares,[pos[0]-3,pos[1]],team) is False:
        finalmoves.append([pos[0]-4,pos[1]])
    return finalmoves

# Bool function that checks if a square is contested by enemy  
def isContested(squares,pos,team):
    contested = []
    if squares[pos[0]][pos[1]].team != team and squares[pos[0]][pos[1]].occupied is True:
        enemyteam = squares[pos[0]][pos[1]].team
        piecetype = squares[pos[0]][pos[1]].piecetype
        piecedict = {'king':King(enemyteam,pos),'queen':Queen(enemyteam,pos),'rook':Rook(enemyteam,pos),'bishop':Bishop(enemyteam,pos),'knight':Knight(enemyteam,pos),'pawn':Pawn(enemyteam,pos)}
        squares[pos[0]][pos[1]].SimClearSquare()
        for k in range(0,8):
            for j in range(0,8):
                if squares[k][j].occupied is True and squares[k][j].team != team:
                    if squares[k][j].piecetype == 'pawn':
                        results = squares[k][j].piece.GetContestingMoves(squares,squares[k][j].team)
                    else:
                        results = squares[k][j].piece.GetMoves(squares,squares[k][j].team)
                    for i in range(len(results)):
                        contested.append(results[i])
        squares[pos[0]][pos[1]].SimSetPiece(piecedict[piecetype])
        if pos in contested:
            return True
        else:
            return False
    else:
        for k in range(0,8):
            for j in range(0,8):
                if squares[k][j].occupied is True and squares[k][j].team != team:
                    results = squares[k][j].piece.GetMoves(squares,squares[k][j].team)
                    for i in range(len(results)):
                        contested.append(results[i])
        if pos in contested:
            return True
        else:
            return False
# Bool function that checks if player is in checkmate or stalemate
def CheckforMate(squares,player):
    for n in range(0,8):
        for m in range(0,8):
            if squares[n][m].team == player:
                moves = squares[n][m].piece.GetMoves(squares,player)
                remaining = SimulateforCheck(squares,moves,player,squares[n][m].piece.pos,'d')
                if len(remaining)>0:
                    return False
    return True

# Handles game end, and prompts player to start new game or quit
def gameOver(win,windowsize,color):
    resetbox = graphics.Rectangle(graphics.Point(windowsize/2-100,windowsize/3-50),graphics.Point(windowsize/2+100,windowsize/3+50))
    resettext = graphics.Text(graphics.Point((resetbox.p1.x+resetbox.p2.x)/2,(resetbox.p1.y+resetbox.p2.y)/2),'Rematch')
    endbox = graphics.Rectangle(graphics.Point(windowsize/2-100,2*windowsize/3-50),graphics.Point(windowsize/2+100,2*windowsize/3+50))
    endtext = graphics.Text(graphics.Point((endbox.p1.x+endbox.p2.x)/2,(endbox.p1.y+endbox.p2.y)/2),'Quit')
    resetbox.setFill(color)
    resetbox.setOutline('black')
    resetbox.setWidth(6)
    endbox.setFill(color)
    endbox.setOutline('black')
    endbox.setWidth(6)
    resettext.setSize(20)
    endtext.setSize(20)
    resetbox.draw(win)
    resettext.draw(win)
    endbox.draw(win)
    endtext.draw(win)
    while True:
        click = win.getMouse()
        xcoord = int(click.x)
        ycoord = int(click.y)
        if xcoord > resetbox.p1.x and xcoord < resetbox.p2.x and ycoord > resetbox.p1.y and ycoord < resetbox.p2.y:
            resetbox.undraw()
            resettext.undraw()
            endbox.undraw()
            endtext.undraw()
            return 'newgame'
        if xcoord > endbox.p1.x and xcoord < endbox.p2.x and ycoord > endbox.p1.y and ycoord < endbox.p2.y:
            resetbox.undraw()
            resettext.undraw()
            endbox.undraw()
            endtext.undraw()
            return 'gameover'

# Algorithm for choosing best move for cpu to make
def GetCPUMove(squares):
    # Get all available moves for the cpu
    bestovertake = []
    available = []
    highestvalue = 0
    rank = {'queen':5,'rook':4,'bishop':3,'knight':2,'pawn':1}
    for k in range(8):
        for j in range(8):
            selected = squares[k][j]
            if selected.occupied is False:
                continue
            elif selected.piece.team != 'player2':
                continue
            availableprecheck = selected.piece.GetMoves(squares,selected.team)
            available = SimulateforCheck(squares,availableprecheck,selected.team,selected.piece.pos,'d')
            # Prioritize putting enemy in check but not while sacrificing a piece without a trade
            (bestmoves,checkmates) = SimulateforCheck(squares,available,selected.team,selected.piece.pos,'a')
            if len(checkmates) > 0:
                return (selected,squares[checkmates[0][0]][checkmates[0][1]])
            if len(bestmoves) > 0:
                for n in range(len(bestmoves)):
                    if isContested(squares,bestmoves[n],'player2') is True:
                        piecetype = selected.piecetype
                        pos = selected.piece.pos
                        piecedict = {'king':King('player2',pos),'queen':Queen('player2',pos),'rook':Rook('player2',pos),'bishop':Bishop('player2',pos),'knight':Knight('player2',pos),'pawn':Pawn('player2',pos)}
                        selected.SimClearSquare()
                        if isContested(squares,bestmoves[n],'player1') is True or rank[squares[bestmoves[n][0]][bestmoves[n][1]].piecetype] > rank[selected.piecetype]:
                            selected.SimSetPiece(piecedict[piecetype])
                            return (selected,squares[bestmoves[n][0]][bestmoves[n][1]])
                        else:
                            selected.SimSetPiece(piecedict[piecetype])
                    else:
                        return (selected,squares[bestmoves[n][0]][bestmoves[n][1]])
            # Next prioritize taking enemy piece in order of piece value
            for i in range(len(available)):
                option = squares[available[i][0]][available[i][1]]
                if option.occupied:
                    if isContested(squares,[available[i][0],available[i][1]],'player2') is False:
                        if rank[option.piecetype] > highestvalue:
                            bestovertake = [available[i][0],available[i][1]]
                            bestfrom = selected
                            highestvalue = rank[option.piecetype]
                    else:
                        if rank[option.piecetype] > highestvalue and rank[option.piecetype] > rank[selected.piecetype]:
                            bestovertake = [available[i][0],available[i][1]]
                            bestfrom = selected
                            highestvalue = rank[option.piecetype]
    if len(bestovertake) > 0 and highestvalue > 1:
        return (bestfrom, squares[bestovertake[0]][bestovertake[1]])
    # Next prioritize castling
    if kp2.numberofmoves == 0:
        castles = checkCastling(squares,[],'player2',kp2.pos)
        if len(castles) > 0:
            return (squares[kp2.pos[0]][kp2.pos[1]],squares[castles[0][0]][castles[0][1]])
    # Else, make random move
    while True:
        k = random.randint(0,8)
        j = random.randint(0,8)
        selected = squares[k][j]
        if selected.occupied is False:
            continue
        elif selected.piece.team != 'player2':
            continue
        availableprecheck = selected.piece.GetMoves(squares,selected.team)
        available = SimulateforCheck(squares,availableprecheck,selected.team,selected.piece.pos,'d')
        if len(available) == 0:
            continue
        elif len(available) == 1:
            return (selected,squares[available[0][0]][available[0][1]])
        else:
            n = random.randint(0,len(available)-1)
            return (selected,squares[available[n][0]][available[n][1]])



# Begin Game Setup
boardsize = 750
windowsize = boardsize
squaresize = boardsize/10
team1color = 'seashell'
team2color = 'royalblue'
board = Board()
win = CreateWindow(windowsize,team1color)
text = Text(windowsize)
mode = StartMenu(win,windowsize)
p1scoreboard = graphics.Text(graphics.Point(130,60),'Player 1 Pieces')
p1scoreboard.draw(win)
p2scoreboard = graphics.Text(graphics.Point(600,60),'Player 2 Pieces')
p2scoreboard.draw(win)
p1score = board.player1score
p1scorenumber = graphics.Text(graphics.Point(198,60),str(p1score))
p1scorenumber.draw(win)
p2score = board.player2score
p2scorenumber = graphics.Text(graphics.Point(668,60),str(p2score))
p2scorenumber.draw(win)
p1gamescore = 0
p2gamescore = 0
gamescore = graphics.Text(graphics.Point(660, 20),(str(p1gamescore),'-',str(p2gamescore)))
gamescore.draw(win)
[squares,kp1,kp2] = initializeGame(win,board,squaresize,team1color,team2color)



# Begin Game Loop
turn = 'player1'
text.Player1turn(win)
if mode == 'quit':
    turn = 'gameover'
while True:
    moveshapes = []
    available = []
    while turn == 'player1':
        UpdateScore(board,p1scorenumber,p2scorenumber)
        if CheckforMate(squares,turn):
            text.Stalemate(win,team1color)
            win.setBackground(team2color)
            turn = gameOver(win,windowsize,'orange')
            break
        click = win.getMouse()
        drawMoveToggle(board,click.x,click.y)
        if (exitButton(click.x,click.y)):
            turn = 'player1'
            text.Player1turn(win)
            mode = StartMenu(win,windowsize)
            gamescore.setText('0-0')
            [squares,kp1,kp2] = initializeGame(win,board,squaresize,team1color,team2color)
            win.setBackground(team1color)
            text.block2.undraw()
            if mode == 'quit':
                turn = 'gameover'
            break
        [col,row] = GetClickCoords(click)
        EraseMoveshapes(moveshapes)
        if [col,row] in available:
            EraseMoveshapes(moveshapes)
            moveshapes = []
            available = []
            selected2 = squares[col][row]
            if selected2.team == 'player2':
                Overtake(selected,selected2,board,selected2.team)
            elif selected2.occupied is False:
                Move(squares,selected,selected2,board)
            else:
                Castle(squares,selected,selected2)
            turn = 'player2'
            if kp1.InCheck(squares) is False:
                text.block2.undraw()
            if kp2.InCheck(squares) is False:
                text.Player2turn(win)
                break  
            if CheckforMate(squares,turn):
                text.Checkmate(win,team1color)
                text.Player1win(win,team1color)
                win.setBackground(team2color)
                p1gamescore+=1
                gamescore.setText((str(p1gamescore),'-',str(p2gamescore)))
                turn = gameOver(win,windowsize,'orange')
                break
            text.Check(win)
        elif squares[col][row].team == turn:
            selected = squares[col][row]
            EraseMoveshapes(moveshapes)
            availableprecheck = selected.piece.GetMoves(squares,selected.team)
            if selected.piecetype == 'king' and selected.piece.numberofmoves == 0:
                availableprecheck = checkCastling(squares,availableprecheck,selected.team,selected.pos)
            available = SimulateforCheck(squares,availableprecheck,selected.team,selected.piece.pos,'d')
            moveshapes = DrawAvailableMoves(available,squares,squaresize,win,board,selected)
        else:
            available = []
            moveshapes = []

    while turn == 'player2' and mode == '2player':
        UpdateScore(board,p1scorenumber,p2scorenumber)
        if CheckforMate(squares,turn):
            text.Stalemate(win,team1color)
            win.setBackground(team2color)
            turn = gameOver(win,windowsize,'orange')
            break
        click = win.getMouse()
        drawMoveToggle(board,click.x,click.y)
        if (exitButton(click.x,click.y)):
            turn = 'player1'
            text.Player1turn(win)
            mode = StartMenu(win,windowsize)
            gamescore.setText('0-0')
            [squares,kp1,kp2] = initializeGame(win,board,squaresize,team1color,team2color)
            win.setBackground(team1color)
            text.block2.undraw()
            if mode == 'quit':
                turn = 'gameover'
            break
        [col,row] = GetClickCoords(click)
        EraseMoveshapes(moveshapes)
        if [col,row] in available:
            EraseMoveshapes(moveshapes)
            moveshapes = []
            available = []
            selected2 = squares[col][row]
            if selected2.team == 'player1':
                Overtake(selected,selected2,board,selected2.team)
            elif selected2.occupied is False:
                Move(squares,selected,selected2,board)
            else:
                Castle(squares,selected,selected2)
            turn = 'player1'
            if kp2.InCheck(squares) is False:
                text.block2.undraw()
            if kp1.InCheck(squares) is False:
                text.Player1turn(win)
                break
            if CheckforMate(squares,turn):
                text.Checkmate(win,team1color)
                text.Player2win(win,team1color)
                win.setBackground(team2color)
                p2gamescore+=1
                gamescore.setText((str(p1gamescore),'-',str(p2gamescore)))
                turn = gameOver(win,windowsize,'orange')
                break
            text.Check(win)
        elif squares[col][row].team == turn:
            selected = squares[col][row]
            EraseMoveshapes(moveshapes)
            availableprecheck = selected.piece.GetMoves(squares,selected.team)
            if selected.piecetype == 'king' and selected.piece.numberofmoves == 0:
                availableprecheck = checkCastling(squares,availableprecheck,selected.team,selected.pos)
            available = SimulateforCheck(squares,availableprecheck,selected.team,selected.piece.pos,'d')
            moveshapes = DrawAvailableMoves(available,squares,squaresize,win,board,selected)
        else:
            available = []
            moveshapes = []

    while turn == 'player2' and mode == 'cpu':
        UpdateScore(board,p1scorenumber,p2scorenumber)
        time.sleep(1)
        if CheckforMate(squares,turn):
            text.Stalemate(win,team1color)
            win.setBackground(team2color)
            turn = gameOver(win,windowsize,'orange')
            break
        bestmoves = []
        bettermoves = []
        available = []
        (movefrom, moveto) = GetCPUMove(squares)
        selected = movefrom
        selected2 = moveto
        if selected2.team == 'player1':
            cpuOvertake(selected,selected2,board,selected2.team)
        elif selected2.occupied is False:
            cpuMove(selected,selected2)
        turn = 'player1'
        if kp2.InCheck(squares) is False:
            text.block2.undraw()
        if kp1.InCheck(squares) is False:
            text.Player1turn(win)
            break
        if CheckforMate(squares,turn):
            text.Checkmate(win,team1color)
            text.Player2win(win,team1color)
            win.setBackground(team2color)
            p2gamescore+=1
            gamescore.setText((str(p1gamescore),'-',str(p2gamescore)))
            turn = gameOver(win,windowsize,'orange')
            break
        text.Check(win)
    if turn == 'gameover':
        win.close()
        break
    if turn == 'newgame':
            [squares,kp1,kp2] = initializeGame(win,board,squaresize,team1color,team2color)
            win.setBackground(team1color)
            text.block2.undraw()
            turn = 'player1'
            text.Player1turn(win)