import pygame

WIN_COLOR = (255, 0, 0)

class TicTacToe:
  def __init__(self, dimensions, req_wins):
    self.dimensions = dimensions
    self.req_wins = req_wins
    self.board_state = []
    for i in range(self.dimensions):
      self.board_state.append([None] * self.dimensions)
    self.winner = None
    self.last_move = None

  def is_valid_move(self, row, col):
    if col < 0 or col > self.dimensions - 1 or row < 0 or row > self.dimensions - 1:
      return False
    if self.board_state[row][col] is not None:
      return False
    if self.winner is not None:
      return False
    return True
  
  def make_move(self, row, col, symbol):
    if self.is_valid_move(row, col):
      self.board_state[row][col] = symbol
      self.last_move = (row, col)
      return True
    return False

  def check_winner(self, screen):
    if self.last_move is None:
      return None
    clicked_row, clicked_col = self.last_move
    symbol = self.board_state[clicked_row][clicked_col]
    x_pos = clicked_col * 200 + 150
    y_pos = clicked_row * 200 + 150

    left = 0
    right = 0
    current_col = clicked_col - 1
    while current_col >= 0 and self.board_state[clicked_row][current_col] == symbol:
      left += 1
      current_col -= 1
    current_col = clicked_col + 1
    while current_col <= self.dimensions - 1 and self.board_state[clicked_row][current_col] == symbol:
      right += 1
      current_col += 1
    if left + right >= self.req_wins - 1:
      pygame.draw.line(screen, WIN_COLOR, (x_pos - left * 200 - 100, y_pos), (x_pos + right * 200 + 100, y_pos), 8)
      return symbol
    
    top = 0
    bottom = 0
    current_row = clicked_row - 1
    while current_row >= 0 and self.board_state[current_row][clicked_col] == symbol:
      top += 1
      current_row -= 1
    current_row = clicked_row + 1
    while current_row <= self.dimensions - 1 and self.board_state[current_row][clicked_col] == symbol:
      bottom += 1
      current_row += 1
    if top + bottom >= self.req_wins - 1:
      pygame.draw.line(screen, WIN_COLOR, (x_pos, y_pos - top * 200 - 100), (x_pos, y_pos + bottom * 200 + 100), 8)
      return symbol
    
    left_top = 0
    right_bottom = 0
    current_row = clicked_row - 1
    current_col = clicked_col - 1
    while current_row >= 0 and current_col >= 0 and self.board_state[current_row][current_col] == symbol:
      left_top += 1
      current_row -= 1
      current_col -= 1
    current_row = clicked_row + 1
    current_col = clicked_col + 1
    while current_row <= self.dimensions - 1 and current_col <= self.dimensions - 1 and self.board_state[current_row][current_col] == symbol:
      right_bottom += 1
      current_row += 1
      current_col += 1
    if left_top + right_bottom >= self.req_wins - 1:
      pygame.draw.line(screen, WIN_COLOR, (x_pos - left_top * 200 - 100, y_pos - left_top * 200 - 100), (x_pos + right_bottom * 200 + 100, y_pos + right_bottom * 200 + 100), 8)
      return symbol
    
    right_top = 0
    left_bottom = 0
    current_row = clicked_row - 1
    current_col = clicked_col + 1
    while current_row >= 0 and current_col <= self.dimensions - 1 and self.board_state[current_row][current_col] == symbol:
      right_top += 1
      current_row -= 1
      current_col += 1
    current_row = clicked_row + 1
    current_col = clicked_col - 1
    while current_row <= self.dimensions - 1 and current_col >= 0 and self.board_state[current_row][current_col] == symbol:
      left_bottom += 1
      current_row += 1
      current_col -= 1
    if right_top + left_bottom >= self.req_wins - 1:
      pygame.draw.line(screen, WIN_COLOR, (x_pos + right_top * 200 + 100, y_pos - right_top * 200 - 100), (x_pos - left_bottom * 200 - 100, y_pos + left_bottom * 200 + 100), 8)
      return symbol
    
    for row in self.board_state:
      for cell in row:
        if cell is None:
          return None
    return "draw"