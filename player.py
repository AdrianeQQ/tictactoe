class Player:
  def __init__(self, symbol):
    self.symbol = symbol

  def make_move(self, game, row, col):
    if game.make_move(row, col, self.symbol):
      return True
    return False