import pygame
import speech_recognition as sr
import _thread

class Pawn:
    def __init__(self, c):
        self.color = c
        self.firstMove = True
    def checkIfValid(self, startx, starty, endx, endy, Board):
        if self.firstMove:
            if(startx == endx):
                if(Board[endy][endx] != "" or abs(starty-endy)>2):return False
            elif(abs(startx-endx) == 1):
                if(Board[endy][endx] == "" or abs(starty-endy)>1):return False
            else: return False
            self.firstMove = False
            return True
                        
        else:
            if(startx == endx):
                if(Board[endy][endx] != "" or abs(startx-endx)>1):return False
            elif(startx+1 == endx or startx-1 == endx):
                if(Board[endy][endx] == "" or abs(starty-endy)>1):return False
            else: return False
            return True
    def __str__(self):
        return "pawn"

class Rook:
    hasMoved = False
    color = ""
    def __init__(self, c):
        self.color = c
    def checkIfValid(self, startx ,starty, endx, endy, Board):
        if(startx == endx):
            for y in range(starty+1, endy):
                if(Board[y][startx] != ""): return False
            if(Board[endy][endx] != ''):
                if(Board[endy][endx].color == self.color):return False
            return True
        elif(starty == endy):
            for x in range(startx+1, endx):
                if(Board[starty][x] != ""): return False
            return True
        else:
            return False
    def castle(self, Board):
        return ""
    def __str__(self):
        return "rook"

class Bishop:
    color = ""
    def __init__(self, c):
        self.color = c
    def checkIfValid(self, startx, starty, endx, endy, Board):
        if(abs(startx-endx)==abs(starty-endy)):
            xsign = int((endx-startx)/abs(startx-endx))
            ysign = int((endy-starty)/abs(starty-endy))
            for i in range(1, abs(startx-endx)):
                if(Board[starty + i*ysign][startx + i*xsign] != ""):return False
            return True
        return False
    def __str__(self):
        return "bishop"

class Knight:
    color = ""
    def __init__(self, c):
        self.color = c
    def checkIfValid(self, startx, starty, endx, endy, Board):
        if(abs(startx-endx)==2 and abs(starty-endy)==1): return True
        if(abs(startx-endx)==1 and abs(starty-endy)==2): return True
        return False
    def __str__(self):
        return "knight"

class Queen:
    color = ""
    def __init__(self, c):
        self.color = c
    def checkIfValid(self, startx, starty, endx, endy, Board):
        r = Rook(self.color)
        b = Bishop(self.color)
        return r.checkIfValid(startx, starty, endx, endy, Board) or b.checkIfValid(startx, starty, endx, endy, Board)
    def __str__(self):
        return "queen"

class King:
    color = ""
    hasMoved = False
    def __init__(self, c):
        self.color = c
    def checkIfValid(self, startx, starty, endx, endy, Board):
        return (abs(startx-endx)<=1 and abs(starty-endy)<=1)
    def castle(self, Board):
        return ""
    def __str__(self):
        return "king"



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
    boxColThing = False
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
    piece = ""
    moves = []
    for token in tokens:
        p = token.lower()
        if p in ["pawn", "rook", "bishop", "queen", "king", "knight"]:
            piece = token.lower()
        elif getCoords(token) != "NA" and len(token)==2:
            moves = [getCoords(token), token[1]]
        else : return False
    return(movePiece(piece, turnColor, int(moves[0]), int(moves[1])-1))

def BoardReSet():
    Board[0] = [Rook("white"), Knight("white"), Bishop("white"), Queen("white"), King("white"), Bishop("white"), Knight("white"), Rook("white")]
    Board[1] = [Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white")]
    for x in range(2, 6):
        for y in range(8):
            Board[x][y] = ""
    Board[6] = [Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black")]
    Board[7] = [Rook("black"), Knight("black"), Bishop("black"), Queen("black"), King("black"), Bishop("black"), Knight("black"), Rook("black")]

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
    print("Here!")
    for r in range(len(Board)):
        for c in range(len(Board)):
            piece = Board[r][c]
            if str(piece) == pieceName and piece.color == color:
                print("Possiblility ({0}, {1}), ({2}, {3})".format(c,r,endX,endY))
                if piece.checkIfValid(c,r,endX,endY,Board):
                    if(Board[endY][endX] != ''):
                        if(Board[endY][endX].color == piece.color):return False
                    Board[endY][endX] = piece
                    Board[r][c] = ""
                    return True
    return False

def getInput(turnColor, garb1, garb2):
    command = input("Enter the piece and space: ")
    while(not parseData(command, turnColor)):
        print("Not valid")
        command = input("Enter the piece and space: ")
    validIn[0] = True

def game_loop():
    turnColor = "white"
    _thread.start_new_thread(getInput, ( turnColor, '', ''))
    while True:
        drawBoard()
        fillBoard()
        pygame.display.update()
        if(validIn[0]): 
            turnColor = "white" if turnColor == "black" else "black"
            validIn[0] = False
            _thread.start_new_thread(getInput, ( turnColor, '', ''))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

Board = [[0 for x in range(8)] for y in range(8)]
validIn = [False]
BoardReSet()
dimX = int(input("Set the x dimension: "))
dimY = int(input("Set the y dimension: "))
sqrLen = int(dimY/8)
off = (dimX-dimY)/2
gameDisplay = pygame.display.set_mode((dimX, dimY))
pygame.display.set_caption("Speech Chess")

game_loop()
