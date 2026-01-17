import abc

class Position:
  #each letter corresponds with a column index in the 2D array
  letterToIndexDict = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}


  def __init__(self, row, column):
    self.row = row
    self.column = column

  #converts from number, letter convention to rowIndex, columnIndex
  def convertToIndex(self):
    rowIndex = 8 - self.row
    columnIndex = self.letterToIndexDict[self.column]
    return [rowIndex, columnIndex]

  #overwrites the == to make comparing positions easier
  def __eq__(self, other):
    if isinstance(other, Position):
        return self.row == other.row and self.column == other.column
    return False

  #converts from rowIndex, columnIndex convention to number, letter
  @classmethod
  def convertToPosition(cls, rowIndex, columnIndex):
    if rowIndex < 0 or rowIndex > 7:
      print("Row Index is out of range")
      return False
    elif not columnIndex in cls.letterToIndexDict.values():
      print("Column Index is out of range")
      return False
    row = 8 - rowIndex
    for key in cls.letterToIndexDict.keys():
      if cls.letterToIndexDict[key] == columnIndex:
        column = key
        return Position(row, column)

  #checks the validity of a rowIndex, columnIndex position (useful for generating possible moves)
  @staticmethod
  def checkIfIndexIsInBounds(rowIndex, columnIndex):
    if rowIndex < 0 or rowIndex > 7:
      return False
    elif columnIndex < 0 or columnIndex > 7:
      return False
    return True


  def __str__(self):
    return f"{self.column} {self.row}"

class ChessPiece(abc.ABC):
  def __init__(self, color, position):
    self.color = color
    self.position = position

  #overwrites the == to make comparisions between chess pieces much more efficient
  def __eq__(self, other):
    if isinstance(other, ChessPiece):
        return self.color == other.color and self.position == other.position
    return False

  #method returns a list of possible objects of position
  @abc.abstractclassmethod
  def findAllPossibleMoves(self, chessboard):
    pass

  def __str__(self):
    if self.color == "white":
      return "W"
    return "B"

class Pawn(ChessPiece):
  def __init__(self, color, position, isInStartingPosition):
    super().__init__(color, position)
    self.isInStartingPosition = isInStartingPosition

  #checks if the pawn can move forward
  #if it can move forward and is in starting position, then check if it can move forward two spaces
  #checks if there's an opposing piece in the diagonal to capture
  #white and black pawns move in opposite directions
  def findAllPossibleMoves(self, chessboard):
    result = []
    rowIndex, columnIndex = self.position.convertToIndex()
    if self.color == "white":
      if Position.checkIfIndexIsInBounds(rowIndex - 1, columnIndex) and chessboard[rowIndex - 1][columnIndex] == "__":
        result.append(Position.convertToPosition(rowIndex - 1, columnIndex))
        if self.isInStartingPosition and Position.checkIfIndexIsInBounds(rowIndex - 2, columnIndex) and chessboard[rowIndex - 2][columnIndex] == "__":
          result.append(Position.convertToPosition(rowIndex - 2, columnIndex))
      if Position.checkIfIndexIsInBounds(rowIndex - 1, columnIndex - 1) and chessboard[rowIndex - 1][columnIndex - 1] != "__" and chessboard[rowIndex - 1][columnIndex - 1].color == "black":
        result.append(Position.convertToPosition(rowIndex - 1, columnIndex - 1))
      if Position.checkIfIndexIsInBounds(rowIndex - 1, columnIndex + 1) and chessboard[rowIndex - 1][columnIndex + 1] != "__" and chessboard[rowIndex - 1][columnIndex + 1].color == "black":
        result.append(Position.convertToPosition(rowIndex - 1, columnIndex + 1))
    else:
      if Position.checkIfIndexIsInBounds(rowIndex + 1, columnIndex) and chessboard[rowIndex + 1][columnIndex] == "__":
          result.append(Position.convertToPosition(rowIndex + 1, columnIndex))
          if self.isInStartingPosition and Position.checkIfIndexIsInBounds(rowIndex + 2, columnIndex) and chessboard[rowIndex + 2][columnIndex] == "__":
            result.append(Position.convertToPosition(rowIndex + 2, columnIndex))
      if Position.checkIfIndexIsInBounds(rowIndex + 1, columnIndex - 1) and chessboard[rowIndex + 1][columnIndex - 1] != "__" and chessboard[rowIndex + 1][columnIndex - 1].color == "white":
        result.append(Position.convertToPosition(rowIndex + 1, columnIndex - 1))
      if Position.checkIfIndexIsInBounds(rowIndex + 1, columnIndex + 1) and chessboard[rowIndex + 1][columnIndex + 1] != "__" and chessboard[rowIndex + 1][columnIndex + 1].color == "white":
        result.append(Position.convertToPosition(rowIndex + 1, columnIndex + 1))
    return result

  def __str__(self):
    return super().__str__() + "p"

#checks all possible positions the knight can go(only checks every type of move once)
#need to always check if the positions is in bounds before proceeding(short-circuit evaluation)
class Knight(ChessPiece):
  def findAllPossibleMoves(self, chessboard):
    result = []
    rowIndex, columnIndex = self.position.convertToIndex()
    possibleIndexChanges = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, 2], [-1, 2], [1, -2], [-1, -2]]
    for rowChange, columnChange in possibleIndexChanges:
      if Position.checkIfIndexIsInBounds(rowIndex + rowChange, columnIndex + columnChange) and (chessboard[rowIndex + rowChange][columnIndex + columnChange] == "__" or chessboard[rowIndex + rowChange][columnIndex + columnChange].color != self.color):
        result.append(Position.convertToPosition(rowIndex + rowChange, columnIndex + columnChange))
    return result

  def __str__(self):
    return super().__str__() + "n"

#checks all possible diagonal moves in each diagonal direction
#if it encounters an out of bounds position, the while loop ends
#if it encounters a piece on its diagonal trajectory, if it is opposite color, add it to the list and end the loop
class Bishop(ChessPiece):
  def findAllPossibleMoves(self, chessboard):
    result = []
    rowIndex, columnIndex = self.position.convertToIndex()
    possibleIndexChanges = [[1, -1], [1, 1], [-1, 1], [-1, -1]]
    for rowChange, columnChange in possibleIndexChanges:
      rowIndex += rowChange
      columnIndex += columnChange
      while Position.checkIfIndexIsInBounds(rowIndex, columnIndex):
        if isinstance(chessboard[rowIndex][columnIndex], ChessPiece):
          if chessboard[rowIndex][columnIndex].color != self.color:
            result.append(Position.convertToPosition(rowIndex, columnIndex))
          break
        else:
          result.append(Position.convertToPosition(rowIndex, columnIndex))
        rowIndex += rowChange
        columnIndex += columnChange
      rowIndex, columnIndex = self.position.convertToIndex()
    return result

  def __str__(self):
    return super().__str__() + "b"

#checks all possible one-directional paths all the way until out of bounds or another piece is encountered
#similar opposite color piece logic once it hits it
class Rook(ChessPiece):
  def __init__(self, color, position, isInStartingPosition):
    super().__init__(color, position)
    self.isInStartingPosition = isInStartingPosition

  def findAllPossibleMoves(self, chessboard):
    result = []
    rowIndex, columnIndex = self.position.convertToIndex()
    possibleIndexChanges = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    for rowChange, columnChange in possibleIndexChanges:
      rowIndex += rowChange
      columnIndex += columnChange
      while Position.checkIfIndexIsInBounds(rowIndex, columnIndex):
        if isinstance(chessboard[rowIndex][columnIndex], ChessPiece):
          if chessboard[rowIndex][columnIndex].color != self.color:
            result.append(Position.convertToPosition(rowIndex, columnIndex))
          break
        else:
          result.append(Position.convertToPosition(rowIndex, columnIndex))
        rowIndex += rowChange
        columnIndex += columnChange
      rowIndex, columnIndex = self.position.convertToIndex()



    return result

  def __str__(self):
    return super().__str__() + "r"

#checks all possible one-directional paths all the way using the bishop and rook paths combined
#similar opposite color piece logic once it hits it
class Queen(ChessPiece):
  def findAllPossibleMoves(self, chessboard):
    result = []
    rowIndex, columnIndex = self.position.convertToIndex()
    possibleIndexChanges = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    for rowChange, columnChange in possibleIndexChanges:
      rowIndex += rowChange
      columnIndex += columnChange
      while Position.checkIfIndexIsInBounds(rowIndex, columnIndex):
        if isinstance(chessboard[rowIndex][columnIndex], ChessPiece):
          if chessboard[rowIndex][columnIndex].color != self.color:
            result.append(Position.convertToPosition(rowIndex, columnIndex))
          break
        else:
          result.append(Position.convertToPosition(rowIndex, columnIndex))
        rowIndex += rowChange
        columnIndex += columnChange
      rowIndex, columnIndex = self.position.convertToIndex()
    return result

  def __str__(self):
    return super().__str__() + "q"

#king can only move one position on a diagonal or to a postion adjecent to them
class King(ChessPiece):
  def __init__(self, color, position, isInStartingPosition):
    super().__init__(color, position)
    self.isInStartingPosition = isInStartingPosition
    self.isAttemptingToCastle = False

  def findAllPossibleMoves(self, chessboard):
    result = []
    rowIndex, columnIndex = self.position.convertToIndex()
    possibleIndexChanges = [[1, 1], [1, -1], [-1, 1], [-1, -1], [1, 0], [-1, 0], [0, -1], [0, 1]]
    for rowChange, columnChange in possibleIndexChanges:
      if Position.checkIfIndexIsInBounds(rowIndex + rowChange, columnIndex + columnChange) and (chessboard[rowIndex + rowChange][columnIndex + columnChange] == "__" or chessboard[rowIndex + rowChange][columnIndex + columnChange].color != self.color):
        result.append(Position.convertToPosition(rowIndex + rowChange, columnIndex + columnChange))

    if self.isInStartingPosition and self.position.convertToIndex() == [0, 4]:
      if not (isinstance(chessboard[0][1], ChessPiece) or isinstance(chessboard[0][2], ChessPiece) or isinstance(chessboard[0][3], ChessPiece)) and isinstance(chessboard[0][0], Rook):
        result.append(Position.convertToPosition(0, 2))
        self.isAttemptingToCastle = True
    elif self.isInStartingPosition and self.position.convertToIndex() == [0, 4]:
      if not (isinstance(chessboard[0][6], ChessPiece) or isinstance(chessboard[0][5], ChessPiece)) and isinstance(chessboard[0][7], Rook):
        result.append(Position.convertToPosition(0, 6))
        self.isAttemptingToCastle = True
    elif self.isInStartingPosition and self.position.convertToIndex() == [7, 4]:
      if not (isinstance(chessboard[7][1], ChessPiece) or isinstance(chessboard[7][2], ChessPiece) or isinstance(chessboard[7][3], ChessPiece)) and isinstance(chessboard[7][0], Rook):
        result.append(Position.convertToPosition(7, 2))
        self.isAttemptingToCastle = True
    elif self.isInStartingPosition and self.position.convertToIndex() == [7, 4]:
      if not (isinstance(chessboard[7][6], ChessPiece) or isinstance(chessboard[7][5], ChessPiece)) and isinstance(chessboard[7][7], Rook):
        result.append(Position.convertToPosition(7, 6))
        self.isAttemptingToCastle = True
    
    return result

    


  def __str__(self):
    return super().__str__() + "k"





