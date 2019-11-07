import pygame
import speech_recognition as sr

class Pawn:
    def __init__(self, c):
        self.color = c
        self.firstMove = True
    def checkIfValid(self, startx, starty, endx, endy, Board):
        if self.firstMove:
            if(startx == endx):
                if(Board[endx][endy] != "" or abs(startx-endx)>2) return False
                return True
            self.firstMove = False
            return("first")
                        
        else:
            if(startx == endx):
                if(Board[endx][endy] != "" or abs(startx-endx)>1) return False
                return True
            return("second")
    def __str__(self):
        return "Pawn"

class Rook:
    hasMoved = False
    color = ""
    def __init__(self, c):
        self.color = c
    def checkIfValid(self, startx ,starty, endx, endy, Board):
        if(startx == endx or starty == endy):
            return True
        else:
            return False
    def castle(self, Board):
        return ""
    def __str__(self):
        return "Rook"

class Bishop:
    color = ""
    def __init__(self, c):
        self.color = c
    def checkIfValid(self, startx, starty, endx, endy, Board):
        return ""
    def __str__(self):
        return "Bishop"

class Knight:
    color = ""
    def __init__(self, c):
        self.color = c
    def checkIfValid(self, startx, starty, endx, endy, Board):
        return ""
    def __str__(self):
        return "Knight"

class Queen:
    color = ""
    def __init__(self, c):
        self.color = c
    def checkIfValid(self, startx, starty, endx, endy, Board):
        return ""
    def __str__(self):
        return "Queen"

class King:
    color = ""
    hasMoved = False
    def __init__(self, c):
        self.color = c
    def checkIfValid(self, startx, starty, endx, endy, Board):
        return ""
    def castle(self, Board):
        return ""
    def __str__(self):
        return "King"



pygame.init()

def getCoords(let):
    toCheck = let[0]
    return{
    "A":0,
    "B":1,
    "C":2,
    "D":3,
    "E":4,
    "F":5,
    "G":6,
    "H":7
    }.get(toCheck,"NA")

def drawBoard():
    white = (255,255,255)
    black = (0,0,0)
    brown = (255,226,129)
    boxColThing = True
    gameDisplay.fill(white)
    pygame.draw.rect(gameDisplay, black, [off-15, 0, dimY+15, dimY])
    for y in range(0, 8):
        for x in range(0, 8):
            if(boxColThing):
                pygame.draw.rect(gameDisplay, white, [x * sqrLen + off, y * sqrLen + 5, sqrLen-2, sqrLen-2])
                boxColThing = not boxColThing
            else:
                pygame.draw.rect(gameDisplay, brown, [x * sqrLen + off, y * sqrLen + 5, sqrLen-2, sqrLen-2])
                boxColThing = not boxColThing
            if(x == 7):
                boxColThing = not boxColThing

def speak():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        return(r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        speak()
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def parseData(data, turnColor):
    tokens = data.split()
    piece = []
    moves = ""
    for token in tokens:
        token.lower()
        if ["pawn", "rook", "bishop", "queen", "king", "knight"].find(token) > -1:
            piece = token
        elif getCoords(token) != "NA" and len(token)==2:
            moves = getCoords(token) + token[1]
        else : return False
    return(movePiece(piece, turnColor, moves[0], moves[1]))

def BoardReSet():
    Board[0] = [Rook("black"), Knight("black"), Bishop("black"), Queen("black"), King("black"), Bishop("black"), Knight("black"), Rook("black")]
    Board[1] = [Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black")]
    for x in range(2, 6):
        for y in range(8):
            Board[x][y] = ""
    Board[6] = [Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white")]
    Board[7] = [Rook("white"), Knight("white"), Bishop("white"), Queen("white"), King("white"), Bishop("white"), Knight("white"), Rook("white")]

def fillBoard():
    countX = 0
    countY = 0
    for arr in Board:
        countY %= 8
        countY+=1
        for thing in arr:
            countX %= 8
            countX+=1
            if thing != "":
                type = str(thing)
                color = thing.color
                piece = pygame.image.load('recources/{}/{}.png'.format(color, color[0] + type.lower()))
                piece = pygame.transform.scale(piece, (sqrLen, sqrLen))
                gameDisplay.blit(piece, ((countX-1)*sqrLen + off , (countY-1)*sqrLen))

def movePiece(pieceName, color, endX, endY):
    for r in len(Board):
        for c in len(Board):
            piece = Board[r][c]
            if str(piece) == pieceName and piece.color == color:
                if piece.checkIfValid(r,c,endX,endY):
                    Board[endX][endY] = piece
                    Board[r][c] = 0
                    return True
    return False

def game_loop():
    turnColor = "white"
    while True:
        drawBoard()
        fillBoard()
        #command = speak()
        #while(not parseData(command, turnColor)):
            #command = speak()
        turnColor = "white" if turnColor == "black" else "black"
        pygame.display.update()

Board = [[0 for x in range(8)] for y in range(8)]
BoardReSet()
dimX = int(raw_input("Set the x dimension: "))
dimY = int(raw_input("Set the y dimension: "))
sqrLen = dimY/8
off = (dimX-dimY)/2
gameDisplay = pygame.display.set_mode((dimX, dimY))
pygame.display.set_caption("Speech Chess")

game_loop()
pygame.quit()
quit()
