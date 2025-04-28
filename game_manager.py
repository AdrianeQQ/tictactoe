import pygame
from tic_tac_toe import TicTacToe
from player import Player
from ai_player import AIPlayer

BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
WIN_COLOR = (255, 0, 0)
MODES = {
  "3x3": 3,
  "5x5": 5,
  "6x6": 5,
  "7x7": 5,
  "8x8": 5,
  "9x9": 5,
  "10x10": 5
}
AI_DEPTH = {
  "3x3": 8,
  "5x5": 5,
  "6x6": 5,
  "7x7": 4,
  "8x8": 4,
  "9x9": 3,
  "10x10": 3
}

class GameManager:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption("Tic Tac Toe")
    self.game = None
    self.players = []
    self.current_player_index = 0
    self.back_button = pygame.Rect(10, 10, 300, 100)

  def draw_board(self):
    self.screen.fill(BG_COLOR)
    for i in range(self.game.dimensions - 1):
      pygame.draw.line(self.screen, LINE_COLOR, (50, 250 + i * 200), (50 + self.game.dimensions * 200, 250 + i * 200), 10)
      pygame.draw.line(self.screen, LINE_COLOR, (250 + i * 200, 50), (250 + i * 200, 50 + self.game.dimensions * 200), 10)
    pygame.display.update()

  def draw_menu(self):
    self.screen = pygame.display.set_mode((700, 700))
    self.screen.fill(BG_COLOR)
    font = pygame.font.SysFont("times new roman", 50)
    title_text = font.render("Wybierz tryb gry:", True, LINE_COLOR)
    self.screen.blit(title_text, (160, 20))

    font = pygame.font.SysFont("times new roman", 40)
    pvp_button = pygame.Rect(20, 100, 300, 100)
    pygame.draw.rect(self.screen, LINE_COLOR, pvp_button, 5)
    pvp_text = font.render("Gracz vs Gracz", True, LINE_COLOR)
    self.screen.blit(pvp_text, (43, 125))

    pva_button = pygame.Rect(380, 100, 300, 100)
    pygame.draw.rect(self.screen, LINE_COLOR, pva_button, 5)
    pva_text = font.render("Gracz vs AI", True, LINE_COLOR)
    self.screen.blit(pva_text, (433, 125))

    button_3x3 = pygame.Rect(20, 250, 300, 100)
    button_5x5 = pygame.Rect(380, 250, 300, 100)
    button_6x6 = pygame.Rect(20, 360, 300, 100)
    button_7x7 = pygame.Rect(380, 360, 300, 100)
    button_8x8 = pygame.Rect(20, 470, 300, 100)
    button_9x9 = pygame.Rect(380, 470, 300, 100)
    button_10x10 = pygame.Rect(200, 580, 300, 100)

    button_map = {
      "3x3": button_3x3,
      "5x5": button_5x5,
      "6x6": button_6x6,
      "7x7": button_7x7,
      "8x8": button_8x8,
      "9x9": button_9x9,
      "10x10": button_10x10
    }
    text_positions = {
        "3x3": (140, 275),
        "5x5": (500, 275),
        "6x6": (140, 385),
        "7x7": (500, 385),
        "8x8": (140, 495),
        "9x9": (500, 495),
        "10x10": (300, 605)
    }
    selected_mode = "3x3"

    for mode, button in button_map.items():
      color = WIN_COLOR if mode == selected_mode else LINE_COLOR
      pygame.draw.rect(self.screen, color, button, 5)
      mode_text = font.render(mode, True, LINE_COLOR)
      self.screen.blit(mode_text, text_positions[mode])
    pygame.display.update()

    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
          if pvp_button.collidepoint(event.pos):
            return ["pvp", selected_mode]
          if pva_button.collidepoint(event.pos):
            return ["pva", selected_mode]
          for mode, button in button_map.items():
            if button.collidepoint(event.pos):
              pygame.draw.rect(self.screen, LINE_COLOR, button_map[selected_mode], 5)
              pygame.draw.rect(self.screen, WIN_COLOR, button, 5)
              selected_mode = mode
              pygame.display.update()
              break

  def draw_move(self, row, col, symbol):
    if symbol == "X":
      pygame.draw.line(self.screen, LINE_COLOR, (col * 200 + 75, row * 200 + 75), (col * 200 + 225, row * 200 + 225), 10)
      pygame.draw.line(self.screen, LINE_COLOR, (col * 200 + 225, row * 200 + 75), (col * 200 + 75, row * 200 + 225), 10)
    else:
      pygame.draw.circle(self.screen, LINE_COLOR, (col * 200 + 150, row * 200 + 150), 75, 8)
    pygame.display.update()

  def draw_back_button(self):
    font = pygame.font.SysFont("times new roman", 40)
    pygame.draw.rect(self.screen, BG_COLOR, self.back_button)
    pygame.draw.rect(self.screen, LINE_COLOR, self.back_button, 5)
    pvp_text = font.render("Menu", True, LINE_COLOR)
    self.screen.blit(pvp_text, (110, 35))
    pygame.display.update()

  def setup_game(self):
    game_type, mode = self.draw_menu()
    dimensions = int(mode.split("x")[0])
    req_wins = MODES[mode]
    self.screen = pygame.display.set_mode((dimensions * 200 + 100, dimensions * 200 + 100))
    self.game = TicTacToe(dimensions, req_wins)

    if game_type == "pvp":
      self.players = [Player("X"), Player("O")]
    else:
      self.players = [Player("X"), AIPlayer("O", AI_DEPTH[mode])]
      #self.players = [AIPlayer("X", AI_DEPTH[mode]), Player("O")]

    self.current_player_index = 0
    self.draw_board()

  def run_game(self):
    self.setup_game()
    running = True
    show_back = False
    while running:
        current_player = self.players[self.current_player_index]
        if self.game.winner is None and isinstance(current_player, AIPlayer):
            move = current_player.get_move(self.game)
            if move is not None:
                r, c = move
                current_player.make_move(self.game)
                self.draw_move(r, c, current_player.symbol)
                self.game.winner = self.game.check_winner(self.screen)
                self.current_player_index = (self.current_player_index + 1) % 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game.winner and self.back_button.collidepoint(event.pos):
                    self.setup_game()
                    show_back = False
                    continue
                if self.game.winner is None:
                    col = (event.pos[0] - 50) // 200
                    row = (event.pos[1] - 50) // 200
                    current_player = self.players[self.current_player_index]
                    if current_player.make_move(self.game, row, col):
                        self.draw_move(row, col, current_player.symbol)
                        self.game.winner = self.game.check_winner(self.screen)
                        self.current_player_index = (self.current_player_index + 1) % 2
        if self.game.winner and not show_back:      
            self.draw_back_button()
            show_back = True
        pygame.display.update()
    pygame.quit()
    exit()