from ast import Index
import _Pieces as p
import copy

class Chessboard:
  def __init__(self):
    #need to initialize each chess piece object beforehand to make sure
    #the same object is added to the 2D array and the corresponding current pieces list
    br1 = p.Rook("black", p.Position(8, "A"), True)
    bn1 = p.Knight("black", p.Position(8, "B"))
    bb1 = p.Bishop("black", p.Position(8, "C"))
    bq1 = p.Queen("black", p.Position(8, "D"))
    bk1 = p.King("black", p.Position(8, "E"), True)
    bb2 = p.Bishop("black", p.Position(8, "F"))
    bn2 = p.Knight("black", p.Position(8, "G"))
    br2 = p.Rook("black", p.Position(8, "H"), True)

    wr1 = p.Rook("white", p.Position(1, "A"), True)
    wn1 = p.Knight("white", p.Position(1, "B"))
    wb1 = p.Bishop("white", p.Position(1, "C"))
    wq1 = p.Queen("white", p.Position(1, "D"))
    wk1 = p.King("white", p.Position(1, "E"), True)
    wb2 = p.Bishop("white", p.Position(1, "F"))
    wn2 = p.Knight("white", p.Position(1, "G"))
    wr2 = p.Rook("white", p.Position(1, "H"), True)

    self.chessboard = [[br1, bn1, bb1, bq1, bk1, bb2, bn2, br2],
                       ["__", "__", "__", "__", "__", "__", "__", "__"],
                       ["__", "__", "__", "__", "__", "__", "__", "__"],
                       ["__", "__", "__", "__", "__", "__", "__", "__"],
                       ["__", "__", "__", "__", "__", "__", "__", "__"],
                       ["__", "__", "__", "__", "__", "__", "__", "__"],
                       ["__", "__", "__", "__", "__", "__", "__", "__"],
                       [wr1, wn1, wb1, wq1, wk1, wb2, wn2, wr2]]
    self.currentWhitePieces = [wr1, wn1, wb1, wq1, wk1, wb2, wn2, wr2]
    self.currentBlackPieces = [br1, bn1, bb1, bq1, bk1, bb2, bn2, br2]
    chessboardLetters = ["A", "B", "C", "D", "E", "F", "G", "H"]
    for i in range(8):
      #need to make an object that is added to both the chessboard and current pieces
      wp1 = p.Pawn("white", p.Position(2, chessboardLetters[i]), True)
      bp1 = p.Pawn("black", p.Position(7, chessboardLetters[i]),True)
      self.chessboard[1][i] = bp1
      self.currentBlackPieces.append(bp1)
      self.chessboard[6][i] = wp1
      self.currentWhitePieces.append(wp1)
    self.eliminatedWhitePieces = []
    self.eliminatedBlackPieces = []
    self.turnCount = 0 # need to save internally so it can be loaded into binary and accessed at a later time through files
    # remembers the next turn of a game instead of defaulting to white

  #used for displaying the letters above and below the board
  def displayLetterMarkers(self):
    topBottomEnd = [" ", "A ", "B ", "C ", "D ", "E ", "F ", "G ", "H ", "  "]
    for character in topBottomEnd:
      print(character, end="  ")
    print()

  #displays board with letters and numbers display on the border
  def displayBoard(self):
    print("Current White Pieces: ") #debug purposes
    for piece in self.currentWhitePieces:
      print(piece, end=" ")
    print()
    print("Current Black Pieces: ") #debug purposes
    for piece in self.currentBlackPieces:
      print(piece, end=" ")
    print()
    print("Eliminated White Pieces: ") #debug purposes
    for piece in self.eliminatedWhitePieces:
      print(piece, end=" ")
    print()
    print("Eliminated Black Pieces: ") #debug purposes
    for piece in self.eliminatedBlackPieces:
      print(piece, end=" ")
    print()
    self.displayLetterMarkers()
    for i in range(8):
      print(f"{8 - i}", end= "  ")
      for location in self.chessboard[i]:
        print(location, end="  ")
      print(f"{8 - i}")
    self.displayLetterMarkers()

  #returns the positions of both kings in a Position object
  @staticmethod
  def locateKings(chessboard):
    whiteKingPosition = None
    blackKingPosition = None
    for row in chessboard:
      for location in row:
        if isinstance(location, p.King) and location.color == "white":
          whiteKingPosition = location.position
        elif isinstance(location, p.King) and location.color == "black":
          blackKingPosition = location.position
        if whiteKingPosition != None and blackKingPosition != None:
          break
    return whiteKingPosition, blackKingPosition

  #checks all of the opposing color's pieces and all of their possible moves
  #if one possible move points to the king's position, then it is in check
  #returns a string of the colors in check (shouldn't be possible to have both, but we're checking for edge case)
  def checkForCheck(self):
    whiteKingPosition, blackKingPosition = Chessboard.locateKings(self.chessboard)
    result = ""
    for whitePiece in self.currentWhitePieces:
      for possibleMove in whitePiece.findAllPossibleMoves(self.chessboard):
        if possibleMove == blackKingPosition:
          result += "black"
    for blackPiece in self.currentBlackPieces:
      for possibleMove in blackPiece.findAllPossibleMoves(self.chessboard):
        if possibleMove == whiteKingPosition:
          result += "white"
    return result

  #similar logic to checkForCheck function, except it's using a modified 2D array chessboard
  def checkForHypotheticalCheck(self, chessboard):
    whiteKingPosition, blackKingPosition = Chessboard.locateKings(chessboard)
    result = ""
    for whitePiece in self.currentWhitePieces:
      for possibleMove in whitePiece.findAllPossibleMoves(chessboard):
        if possibleMove == blackKingPosition:
          result += "black"
    for blackPiece in self.currentBlackPieces:
      for possibleMove in blackPiece.findAllPossibleMoves(chessboard):
        if possibleMove == whiteKingPosition:
          result += "white"
    return result

  #checks all of the pieces with the same color as the king in check and loads each of their possible moves on a hypothetical board
  #if one possible move remove the check, then the function returns false
  def checkForCheckmate(self, color):
        checkResult = self.checkForCheck()
        if color == "white" and "white" not in checkResult: # checks if the king is specified king is actually in check
          return False
        elif color == "black" and "black" not in checkResult:
          return False

        whiteKingPosition, blackKingPosition = self.locateKings(self.chessboard)
        if color == "white":
          for whitePiece in self.currentWhitePieces:
            currentRowIndex, currentColumnIndex = whitePiece.position.convertToIndex()
            for possibleMove in whitePiece.findAllPossibleMoves(self.chessboard):
              if possibleMove:
                potentialChessBoard = copy.deepcopy(self.chessboard)
                newRowIndex, newColumnIndex = possibleMove.convertToIndex()
                potentialChessBoard[newRowIndex][newColumnIndex] = whitePiece
                potentialChessBoard[currentRowIndex][currentColumnIndex] = "__"
                if "white" not in self.checkForHypotheticalCheck(potentialChessBoard):
                  return False
        else:
          for blackPiece in self.currentBlackPieces:
            currentRowIndex, currentColumnIndex = blackPiece.position.convertToIndex()
            for possibleMove in blackPiece.findAllPossibleMoves(self.chessboard):
              if possibleMove:
                potentialChessBoard = copy.deepcopy(self.chessboard)
                newRowIndex, newColumnIndex = possibleMove.convertToIndex()
                potentialChessBoard[newRowIndex][newColumnIndex] = blackPiece
                potentialChessBoard[currentRowIndex][currentColumnIndex] = "__"
                if "black" not in self.checkForHypotheticalCheck(potentialChessBoard):
                  return False
        return True
  #checks the top and bottom rows of the 2D array for pawns with their corresponding colors on the chessboard
  #edge case: it should be impossible for a white pawn to end up on the bottom row and vice versa
  def checkForPawnPromotion(self):
    for i in range(len(self.chessboard[0])):
      topRow = self.chessboard[0][i]
      if isinstance(topRow, p.Pawn) and topRow.color == "white":
        self.pawnPromotion(topRow.position.convertToIndex()[0], topRow.position.convertToIndex()[1], "white")
    for i in range(len(self.chessboard[7])):
      bottomRow = self.chessboard[7][i]
      if isinstance(bottomRow, p.Pawn) and bottomRow.color == "black":
        self.pawnPromotion(bottomRow.position.convertToIndex()[0], bottomRow.position.convertToIndex()[1], "black")
  #asks the user for a number input representing the type of piece they would like to replace
  #removes the pawn from current pieces and adds the new piece to the current piece for the respected color
  #updates the chess piece at the location of the pawn on the chessboard
  def pawnPromotion(self, rowIndex, columnIndex, color):
    print("You can promote your pawn!")
    print(f"Row Index: {rowIndex}, Column Index: {columnIndex}, Color: {color}") # debug purposes
    while True:
      try:
        promotionNum = int(input("1. Queen\n2. Rook\n3. Knight\n4. Bishop\n5. Keep as Pawn\n Enter the number for the piece you would like to promote to: "))
        if promotionNum < 1 or promotionNum > 5:
          raise IndexError("Please enter a number within the range(1-5)")
      except ValueError:
        print("Please enter a valid number")
      except IndexError as e:
        print(e)
      else:
        if promotionNum != 5:
          result = f"The pawn at {p.Position.convertToPosition(rowIndex, columnIndex)} has been converted into a "
          if color == "white":
            self.currentWhitePieces.remove(self.chessboard[rowIndex][columnIndex])
          else:
            self.currentBlackPieces.remove(self.chessboard[rowIndex][columnIndex])
          match promotionNum:
            case 1: #queen
              queen = p.Queen(color, p.Position.convertToPosition(rowIndex, columnIndex))
              self.chessboard[rowIndex][columnIndex] = queen
              if color == "white":
                self.currentWhitePieces.append(queen)
              else:
                self.currentBlackPieces.append(queen)
              print(result + "queen!")
              break
            case 2: #rook
              rook = p.Rook(color, p.Position.convertToPosition(rowIndex, columnIndex))
              self.chessboard[rowIndex][columnIndex] = rook
              if color == "white":
                self.currentWhitePieces.append(rook)
              else:
                self.currentBlackPieces.append(rook)
              print(result + "rook!")
              break
            case 3: #knight
              knight = p.Knight(color, p.Position.convertToPosition(rowIndex, columnIndex))
              self.chessboard[rowIndex][columnIndex] = knight
              if color == "white":
                self.currentWhitePieces.append(knight)
              else:
                self.currentBlackPieces.append(knight)
              print(result + "knight!")
              break
            case 4: #bishop
              bishop = p.Bishop(color, p.Position.convertToPosition(rowIndex, columnIndex))
              self.chessboard[rowIndex][columnIndex] = bishop
              if color == "white":
                self.currentWhitePieces.append(bishop)
              else:
                self.currentBlackPieces.append(bishop)
              print(result + "bishop!")
              break
          self.displayBoard()

  #helper function to check if a piece exists at a specific position
  def checkForPieceInPositon(self, position, color):
    rowIndex, columnIndex = position.convertToIndex()
    if isinstance(self.chessboard[rowIndex][columnIndex], p.ChessPiece) and self.chessboard[rowIndex][columnIndex].color == color:
      return True
    return False



#for testing purpose
chessboard = Chessboard()
chessboard.displayBoard()

