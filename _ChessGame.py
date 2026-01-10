import _Pieces as p
import _Chessboard as c
import copy
from datetime import datetime
import pickle

#asks for user input of a position using try-except
#custom messages are created with the TypeError constructor
#checks if a piece actually exists at the inputted position
def getPositionOfPiece(board, color):
  while True:
    try:
      letter = input("Enter the letter: ")
      if not letter.lower() in ["a", "b", "c", "d", "e", "f", "g", "h"] :
        raise TypeError("Please enter a valid letter(A-H)")
      number = int(input("Enter the number: "))
      if number < 1 or number > 8:
        raise TypeError("Please enter a valid number(1-8)")
      if not board.checkForPieceInPositon(p.Position(number, letter.upper()), color):
        raise TypeError("You don't have a piece at this position")
    except ValueError:
      print("Please enter an integer")
    except TypeError as e:
      print(e)
    else:
      return p.Position(number, letter.upper())

#same functionality as the getPositionOfPiece method,
#except it doesn't check whether the end position has a piece alread thre
def getTargetPiece(board, color):
  while True:
    try:
      letter = input("Enter the letter: ")
      if not letter.lower() in ["a", "b", "c", "d", "e", "f", "g", "h"] :
        raise TypeError("Please enter a valid letter(A-H)")
      number = int(input("Enter the number: "))
      if number < 1 or number > 8:
        raise TypeError("Please enter a valid number(1-8)")
    except ValueError:
      print("Please enter an integer")
    except TypeError as e:
      print(e)
    else:
      return p.Position(number, letter.upper())

board = c.Chessboard()
now = datetime.now()
fileName = input("Write the file path you would like to load\n(or press Enter to create a new file):")
#user can input previous files storing the Chessboard object of a game in progress
if len(fileName) > 0:
  with open(fileName, "rb") as file:
    board = pickle.load(file)  #converts from binary into the Chessboard object
else:
  #create a brand new file using the internal clock of the user's device
  fileName = now.strftime("%d-%m-%Y_%H%M%S") + ".chessboard" #overwrites the fileName variable
  with open(fileName, "wb") as file:
    file.write(pickle.dumps(copy.deepcopy(board)))

while not board.checkForCheckmate("white") and not board.checkForCheckmate("black"):
  if "white" in board.checkForCheck():
    print("White is in check!")
  if "black" in board.checkForCheck():
    print("Black is in check!")
  board.displayBoard()
  if board.turnCount % 2 == 0:
    while True:
      print("Player 1's turn (White)")
      print("Enter the position of the piece you would like to move: ")
      startPosition = getPositionOfPiece(board, "white")
      startRowIndex, startColumnIndex = startPosition.convertToIndex()
      piece = board.chessboard[startRowIndex][startColumnIndex] #accesses the piece at the starting position
      print(f"{piece}: ", end="")
      for i, move in enumerate(piece.findAllPossibleMoves(board.chessboard)): #testing purposes
        if i == len(piece.findAllPossibleMoves(board.chessboard)) - 1:
          print(move, end="")
        else:
          print(move, end=", ")
      print()
      print("Enter the position you would to move the piece to: ")
      endPosition = getTargetPiece(board, "white")
      endRowIndex, endColumnIndex = endPosition.convertToIndex()
      moveIsValid = False

      for move in piece.findAllPossibleMoves(board.chessboard): #checks if the inputted position is in the piece's possible moves list
        if move.row == endPosition.row and move.column == endPosition.column:
          moveIsValid = True
          break
      if not moveIsValid:
        print("Cannot make that move, please try again")
      else:
        hypotheticalBoard = copy.deepcopy(board) #uses deepcopy to copy the entire Chessboard object by value, not reference, and create a brand new object
        hypothicalPiece = hypotheticalBoard.chessboard[startRowIndex][startColumnIndex]
        hypothicalEndPiece = hypotheticalBoard.chessboard[endRowIndex][endColumnIndex]
        if hypothicalEndPiece in hypotheticalBoard.currentWhitePieces:
          hypotheticalBoard.currentBlackPieces.remove(hypothicalEndPiece) #removes hypothetical current black piece from the list
        hypothicalPiece.position = endPosition
        hypotheticalBoard.chessboard[endRowIndex][endColumnIndex] = hypotheticalBoard.chessboard[startRowIndex][startColumnIndex]  #makes the switch in the 2D array
        hypotheticalBoard.chessboard[startRowIndex][startColumnIndex] = "__"
        hypotheticalBoard.displayBoard()
        result = hypotheticalBoard.checkForHypotheticalCheck(hypotheticalBoard.chessboard)
        if "white" in result:
          print("You can't make this move, or else you'll be in check")
        else:
          capturedPiece = board.chessboard[endRowIndex][endColumnIndex] #remembers the captured Piece
          print(f"Captured piece: {capturedPiece}")
          piece.position = endPosition
          board.chessboard[endRowIndex][endColumnIndex] = board.chessboard[startRowIndex][startColumnIndex]
          board.chessboard[startRowIndex][startColumnIndex] = "__" #makes the switch on the actual 2D chessboard
          if isinstance(capturedPiece, p.ChessPiece) and capturedPiece.color == "black": #checks if the captured piece is not "__"
            board.eliminatedBlackPieces.append(capturedPiece)
            board.currentBlackPieces.remove(capturedPiece)
            #board.currentBlackPieces = [item for item in board.currentBlackPieces if item != capturedPiece]

          if isinstance(piece, p.Pawn) and piece.isInStartingPosition:
            piece.isInStartingPosition = False #updates the pawn attribute if we move the pawn

          board.checkForPawnPromotion() #checks for pawn promotion every time

          break
  else:
    while True:
      print("Player 2's turn (Black)")
      print("Enter the position of the piece you would like to move: ")
      startPosition = getPositionOfPiece(board, "black")
      startRowIndex, startColumnIndex = startPosition.convertToIndex()
      piece = board.chessboard[startRowIndex][startColumnIndex] #accesses the piece at the starting position
      print(f"{piece}: ", end="")
      for i, move in enumerate(piece.findAllPossibleMoves(board.chessboard)): #testing purposes
        if i == len(piece.findAllPossibleMoves(board.chessboard)) - 1:
          print(move, end="")
        else:
          print(move, end=", ")
      print()
      print("Enter the position you would to move the piece to: ")
      endPosition = getTargetPiece(board, "black")
      endRowIndex, endColumnIndex = endPosition.convertToIndex()
      moveIsValid = False
      for move in piece.findAllPossibleMoves(board.chessboard): #checks if the inputted position is in the piece's possible moves list
        if move.row == endPosition.row and move.column == endPosition.column:
          moveIsValid = True
          break
      if not moveIsValid:
        print("Cannot make that move, please try again")
      else:
        hypotheticalBoard = copy.deepcopy(board) #uses deepcopy to copy the entire Chessboard object by value, not reference, and create a brand new object
        hypothicalPiece = hypotheticalBoard.chessboard[startRowIndex][startColumnIndex]
        hypothicalEndPiece = hypotheticalBoard.chessboard[endRowIndex][endColumnIndex]
        if hypothicalEndPiece in hypotheticalBoard.currentWhitePieces:
          hypotheticalBoard.currentWhitePieces.remove(hypothicalEndPiece) #removes hypothetical current black piece from the list

        hypothicalPiece.position = endPosition
        hypotheticalBoard.chessboard[endRowIndex][endColumnIndex] = hypotheticalBoard.chessboard[startRowIndex][startColumnIndex] #makes the switch in the 2D array
        hypotheticalBoard.chessboard[startRowIndex][startColumnIndex] = "__"
        hypotheticalBoard.displayBoard()
        result = hypotheticalBoard.checkForHypotheticalCheck(hypotheticalBoard.chessboard)
        if "black" in result:
          print("You can't make this move, or else you'll be in check")
        else:
          capturedPiece = board.chessboard[endRowIndex][endColumnIndex] #remembers the captured Piece
          print(f"Captured piece: {capturedPiece}")
          piece.position = endPosition
          board.chessboard[endRowIndex][endColumnIndex] = board.chessboard[startRowIndex][startColumnIndex]
          board.chessboard[startRowIndex][startColumnIndex] = "__" #makes the switch on the actual 2D chessboard
          if isinstance(capturedPiece, p.ChessPiece) and capturedPiece.color == "white": #checks if the captured piece is not "__"
            board.eliminatedWhitePieces.append(capturedPiece)
            board.currentWhitePieces.remove(capturedPiece)
            #board.currentWhitePieces = [item for item in board.currentWhitePieces if item != capturedPiece]

          if isinstance(piece, p.Pawn) and piece.isInStartingPosition: #updates the pawn attribute if we move the pawn
            piece.isInStartingPosition = False

          board.checkForPawnPromotion() #checks for pawn promotion every time
          break
  #updates the internal count of the game
  board.turnCount += 1
  #once the move becomes valid, the board object is overwrite into the same file and converted into binary
  with open(fileName, "wb") as file:
    file.write(pickle.dumps(copy.deepcopy(board)))

#we get here if there's a checkmate on either color
print("Checkmate!")
if board.checkForCheckmate("white"):
  print("Black wins!")
else:
  print("White wins!")
