import pygame
import sys
import copy
from pyswip import Prolog

pygame.init()

# =========================
# ====== Definations ======
# =========================

# ====== DIFFICULTY ======
class AI_Difficulty:
    Easy = 1
    Medium = 2
    Hard = 3

# ====== STATES ======
class Window:
    MENU = 0
    SETTINGS = 1
    GAME = 2

# ====== Pieces ======
class PieceType:
    EMPTY = 0
    ATTACKER = 1
    DEFENDER = 2
    KING = 3

class PlayerType:
    Human = 0
    AI = 1

class TurnState:
    ATTACKER = 0
    DEFENDER = 1
    WIN_ATTACKER = 2
    WIN_DEFENDER = 3

    @staticmethod
    def switch_turn(turn):
        if turn == TurnState.ATTACKER:
            return TurnState.DEFENDER
        elif turn == TurnState.DEFENDER:
            return TurnState.ATTACKER
        else:
            return turn

# ====== Colors ======
class Colors:
    WHITE = (240,240,240)
    GRAY = (150,150,150)
    BLACK = (20,20,20)
    RED = (200,60,60)
    BLUE = (60,100,200)
    GOLD = (220,180,40)
    YELLOW = (255,255,0)
    DARK_BLUE = (18, 32, 64)

# ====== Settings ======
X = 400
BOARD_SIZE = 11
AttackerPlayer = PlayerType.Human
DefenderPlayer = PlayerType.AI
Difficulty = AI_Difficulty.Easy
isICON = False

class GameElements:
    def __init__(self):
        self.board = [[PieceType.EMPTY]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.turn = TurnState.ATTACKER
        self.dead_attackers = 0
        self.dead_defenders = 0
        self.selectedCell = None
        self.history = []   

    def reset(self):
        self.board = [[PieceType.EMPTY]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.turn = TurnState.ATTACKER
        self.dead_attackers = 0
        self.dead_defenders = 0
        self.selectedCell = None
        self.history = []   
        mid = BOARD_SIZE // 2

        for i in range(mid - 1, mid + 2):
            for j in range(mid - 1, mid + 2):
                self.board[i][j] = PieceType.DEFENDER

        self.board[mid - 2][mid] = PieceType.DEFENDER
        self.board[mid + 2][mid] = PieceType.DEFENDER
        self.board[mid][mid - 2] = PieceType.DEFENDER
        self.board[mid][mid + 2] = PieceType.DEFENDER
        self.board[mid][mid] = PieceType.KING

        for i in range(mid - 2, mid + 3):
            self.board[0][i] = PieceType.ATTACKER
            self.board[BOARD_SIZE - 1][i] = PieceType.ATTACKER
            self.board[i][0] = PieceType.ATTACKER
            self.board[i][BOARD_SIZE - 1] = PieceType.ATTACKER

        self.board[1][mid] = PieceType.ATTACKER
        self.board[BOARD_SIZE - 2][mid] = PieceType.ATTACKER
        self.board[mid][BOARD_SIZE - 2] = PieceType.ATTACKER
        self.board[mid][1] = PieceType.ATTACKER

gameElements = GameElements()
appWindow = Window.MENU

WIDTH = 3 * X
HEIGHT = 2 * X

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tafl UI")

CELL = (2 * X) / BOARD_SIZE
ATTACKER_ICON_FILE = "attacker.png"
DEFENDER_ICON_FILE = "defender.png"
KING_ICON_FILE = "king.png"

CELL_RADIUS = CELL//2 - 4

ATTACKER_ICON = pygame.transform.scale(pygame.image.load(ATTACKER_ICON_FILE).convert_alpha(), (CELL_RADIUS*2, CELL_RADIUS*2)) 
DEFENDER_ICON = pygame.transform.scale(pygame.image.load(DEFENDER_ICON_FILE).convert_alpha(), (CELL_RADIUS*2, CELL_RADIUS*2)) 
KING_ICON = pygame.transform.scale(pygame.image.load(KING_ICON_FILE).convert_alpha(), (CELL_RADIUS*2, CELL_RADIUS*2)) 

font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

# ====== BUTTONS ======
start_btn = pygame.Rect(WIDTH//2 - 60, 180, 120, 40)
settings_btn = pygame.Rect(WIDTH//2 - 60, 240, 120, 40) 
back_btn = pygame.Rect(2*X + 20, 220, 100, 40)
undo_btn = pygame.Rect(2*X + 20, 280, 100, 40)   

difficulty_btn = pygame.Rect(WIDTH//2 - 110, 170, 220, 40) 
p1_btn = pygame.Rect(WIDTH//2 - 110, 230, 220, 40)    
p2_btn = pygame.Rect(WIDTH//2 - 110, 290, 220, 40)  
icon_btn = pygame.Rect(WIDTH//2 - 110, 350, 220, 40)  
board_size_btn = pygame.Rect(WIDTH//2 - 110, 410, 220, 40)  
settings_back_btn = pygame.Rect(WIDTH//2 - 60, 470, 120, 40) 

class Drawer:
    @staticmethod
    def draw_board():
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x = c * CELL
                y = r * CELL

                color = Colors.WHITE if (r+c)%2==0 else Colors.GRAY
                pygame.draw.rect(screen, color, (x, y, CELL, CELL))

                if gameElements.selectedCell == (r,c):
                    pygame.draw.rect(screen, Colors.YELLOW, (x,y,CELL,CELL), 3)

                piece = gameElements.board[r][c]
                if piece != PieceType.EMPTY:
                    center = (x + CELL//2, y + CELL//2)
                    
                    
                    color = Colors.WHITE
                    name = "none"
                    icon = ATTACKER_ICON
                    if piece == PieceType.ATTACKER:
                        icon = ATTACKER_ICON
                        name = "ATK"
                        color = Colors.RED
                    elif piece == PieceType.DEFENDER:
                        icon = DEFENDER_ICON
                        color = Colors.BLUE
                        name = "DEF"
                    elif piece == PieceType.KING:
                        icon = KING_ICON
                        color = Colors.GOLD
                        name = "King"

                    if isICON:
                        screen.blit(icon, (center[0] - CELL_RADIUS, center[1] - CELL_RADIUS))
                    else:
                        text = font.render(name, True, (0, 0, 0))
                        text_rect = text.get_rect(center=center)
                        pygame.draw.circle(screen, color, center, CELL_RADIUS)
                        screen.blit(text, text_rect)

    @staticmethod
    def draw_panel():
        panel_x = 2 * X
        pygame.draw.rect(screen, Colors.BLACK, (panel_x, 0, X, 2*X))

        t = "None .."
        color = Colors.WHITE
        if gameElements.turn == TurnState.ATTACKER:
            t = "Attackers"
        elif gameElements.turn == TurnState.DEFENDER:
            t = "Defenders"
        elif gameElements.turn == TurnState.WIN_ATTACKER:
            t = "Attackers Won!"
            color = Colors.GOLD
        elif gameElements.turn == TurnState.WIN_DEFENDER:
            t = "Defenders Won!"
            color = Colors.GOLD

        screen.blit(big_font.render("Turn:", True, Colors.WHITE), (panel_x+10, 20))
        screen.blit(font.render(t, True, color), (panel_x+10, 50))

        dead_attackers = 24 - prologInterface.numberOfAttackers(gameElements.board)
        dead_defenders = 13 - prologInterface.numberOfDefenders(gameElements.board)

        screen.blit(font.render(f"Attackers dead: {dead_attackers}", True, Colors.WHITE), (panel_x+10, 120))
        screen.blit(font.render(f"Defenders dead: {dead_defenders}", True, Colors.WHITE), (panel_x+10, 160))

        pygame.draw.rect(screen, Colors.GRAY, back_btn)
        screen.blit(font.render("Back", True, Colors.BLACK), (back_btn.x+20, back_btn.y+10))

        pygame.draw.rect(screen, Colors.GRAY, undo_btn) 
        screen.blit(font.render("Undo", True, Colors.BLACK), (undo_btn.x+20, undo_btn.y+10)) 



    @staticmethod
    def draw_menu():
        screen.fill(Colors.DARK_BLUE)
        screen.blit(big_font.render("The Viking Chess (TAFL) GAME", True, Colors.WHITE), (WIDTH//2 - 170, 100))

        pygame.draw.rect(screen, Colors.GRAY, start_btn)
        screen.blit(font.render("Start", True, Colors.BLACK), (start_btn.x+30, start_btn.y+10))

        pygame.draw.rect(screen, Colors.GRAY, settings_btn)   
        screen.blit(font.render("Settings", True, Colors.BLACK), (settings_btn.x+18, settings_btn.y+10))  

        screen.blit(font.render("Mohamed Khaled 20230595", True, Colors.WHITE), (WIDTH//2 - 120, HEIGHT - 90))
        screen.blit(font.render("Mahmoud Abd elaziz 20230603", True, Colors.WHITE), (WIDTH//2 - 120, HEIGHT - 60))
        screen.blit(font.render("Marwan Hussein 20230381", True, Colors.WHITE), (WIDTH//2 - 120, HEIGHT - 30))


    @staticmethod
    def draw_settings():  
        screen.fill(Colors.DARK_BLUE)
        screen.blit(big_font.render("SETTINGS", True, Colors.WHITE), (WIDTH//2 - 70, 90))

        diff_text = "Easy" if Difficulty == AI_Difficulty.Easy else "Medium" if Difficulty == AI_Difficulty.Medium else "Hard"
        p1_text = "Human" if AttackerPlayer == PlayerType.Human else "AI"
        p2_text = "Human" if DefenderPlayer == PlayerType.Human else "AI"

        pygame.draw.rect(screen, Colors.GRAY, difficulty_btn)
        screen.blit(font.render(f"Difficulty: {diff_text}", True, Colors.BLACK),
                    (difficulty_btn.x+15, difficulty_btn.y+10))

        pygame.draw.rect(screen, Colors.GRAY, p1_btn)
        screen.blit(font.render(f"Player 1 (Attacker): {p1_text}", True, Colors.BLACK),
                    (p1_btn.x+10, p1_btn.y+10))

        pygame.draw.rect(screen, Colors.GRAY, p2_btn)
        screen.blit(font.render(f"Player 2 (Defender): {p2_text}", True, Colors.BLACK),
                    (p2_btn.x+10, p2_btn.y+10))

        pygame.draw.rect(screen, Colors.GRAY, settings_back_btn)
        screen.blit(font.render("Back", True, Colors.BLACK),
                    (settings_back_btn.x+35, settings_back_btn.y+10))
        
        pygame.draw.rect(screen, Colors.GRAY, icon_btn)
        if isICON:
            screen.blit(font.render("Fancy icons", True, Colors.BLACK),
                        (icon_btn.x+35, icon_btn.y+10))
        else:
            screen.blit(font.render("Simple icons", True, Colors.BLACK),
                        (icon_btn.x+35, icon_btn.y+10))
        
        pygame.draw.rect(screen, Colors.GRAY, board_size_btn)
        if BOARD_SIZE == 11:
            screen.blit(font.render("Board size 11", True, Colors.BLACK),
                        (board_size_btn.x+35, board_size_btn.y+10))
        else:
            screen.blit(font.render("Board size 9", True, Colors.BLACK),
                        (board_size_btn.x+35, board_size_btn.y+10))

        screen.blit(font.render("Mohamed Khaled 20230595", True, Colors.WHITE), (WIDTH//2 - 120, HEIGHT - 90))
        screen.blit(font.render("Mahmoud Abd elaziz 20230603", True, Colors.WHITE), (WIDTH//2 - 120, HEIGHT - 60))
        screen.blit(font.render("Marwan Hussein 20230381", True, Colors.WHITE), (WIDTH//2 - 120, HEIGHT - 30))

class PrologInterface:
    def __init__(self):
        self.prolog = Prolog()
        self.prolog.consult("ai.pl")
        q = "set_prolog_flag(stack_limit, 32_000_000_000)"
        res = self._query(q)
        print(res)

    def _board_term(self, board):
        return str(board)

    def _query(self, query_text):
        try:
            return next(self.prolog.query(query_text), None)
        except Exception as e:
            print("Prolog error:", e)
            return None

    def numberOfAttackers(self, board):
        q = f"number_of_pieces({self._board_term(board)}, attacker, Count)"
        result = self._query(q)
        if result is None:
            return 0
        return int(result["Count"])
    
    def numberOfDefenders(self, board):
        q = f"number_of_pieces({self._board_term(board)}, defender, Count)"
        result = self._query(q)
        if result is None:
            return 0
        return int(result["Count"])

    def terminalState(self, board):
        q = f"terminal_state({self._board_term(board)}, Val)"
        result = self._query(q)
        return result is not None

    def validMove(self, board, sr, sc, er, ec):
        q = f"valid_move({self._board_term(board)}, {sr}, {sc}, {er}, {ec})"
        result = self._query(q)
        return result is not None

    def makeMove(self, board, sr, sc, er, ec):
        q = f"make_move({self._board_term(board)}, {sr}, {sc}, {er}, {ec}, NewBoard)"
        result = self._query(q)
        if result is None:
            return board
        return result["NewBoard"]

    def getAttackerMove(self, board, depth):
        q = f"best_attacker_move({self._board_term(board)}, {depth}, SR, SC, ER, EC)"
        result = self._query(q)
        if result is None:
            return (0, 0, 0, 0)
        return (
            int(result["SR"]),
            int(result["SC"]),
            int(result["ER"]),
            int(result["EC"])
        )

    def getDefenderMove(self, board, depth):
        q = f"best_defender_move({self._board_term(board)}, {depth}, SR, SC, ER, EC)"
        result = self._query(q)
        if result is None:
            return (0, 0, 0, 0)
        return (
            int(result["SR"]),
            int(result["SC"]),
            int(result["ER"]),
            int(result["EC"])
        )

prologInterface = PrologInterface()

def validMove(sr, sc, er, ec):
    return prologInterface.validMove(gameElements.board, sr, sc, er, ec)

def save_history(mover):  
    game = gameElements
    game.history.append({
        "board": copy.deepcopy(game.board),
        "turn": game.turn,
        "dead_attackers": game.dead_attackers,
        "dead_defenders": game.dead_defenders,
        "selectedCell": game.selectedCell,
        "mover": mover
    })

def undo_last_human_turn():  
    game = gameElements
    while game.history:
        last = game.history.pop()
        game.board = copy.deepcopy(last["board"])
        game.turn = last["turn"]
        game.dead_attackers = last["dead_attackers"]
        game.dead_defenders = last["dead_defenders"]
        game.selectedCell = last["selectedCell"]
        if last["mover"] == PlayerType.Human:
            break

def makeMove(sr, sc, er, ec):
    if not validMove(sr, sc, er, ec):
        return False
    board = prologInterface.makeMove(gameElements.board, sr, sc, er, ec)
    gameElements.board = board
    return True

def AI_attackerMove():
    save_history(PlayerType.AI)   
    move = prologInterface.getAttackerMove(gameElements.board, Difficulty)
    sr, sc, er, ec = move
    ok = makeMove(sr, sc, er, ec)
    if not ok:
        gameElements.history.pop()  
    return ok

def AI_defenderMove():
    save_history(PlayerType.AI) 
    move = prologInterface.getDefenderMove(gameElements.board, Difficulty)
    sr, sc, er, ec = move
    ok = makeMove(sr, sc, er, ec)
    if not ok:
        gameElements.history.pop() 
    return ok

# ====== HELPERS ======
def get_cell(pos):
    x,y = pos
    if x >= 2*X or y >= 2*X:
        return None
    return y//CELL, x//CELL

def cycle_difficulty(): 
    global Difficulty
    if Difficulty == AI_Difficulty.Easy:
        Difficulty = AI_Difficulty.Medium
    elif Difficulty == AI_Difficulty.Medium:
        Difficulty = AI_Difficulty.Hard
    else:
        Difficulty = AI_Difficulty.Easy

def toggle_player1(): 
    global AttackerPlayer
    AttackerPlayer = PlayerType.AI if AttackerPlayer == PlayerType.Human else PlayerType.Human

def toggle_player2(): 
    global DefenderPlayer
    DefenderPlayer = PlayerType.AI if DefenderPlayer == PlayerType.Human else PlayerType.Human

def toggle_icon(): 
    global isICON
    isICON = not isICON

def toggle_board_size(): 
    global BOARD_SIZE, CELL, ATTACKER_ICON, DEFENDER_ICON, KING_ICON, CELL_RADIUS
    BOARD_SIZE = 9 + 11 - BOARD_SIZE
    CELL = (2 * X) / BOARD_SIZE
    CELL_RADIUS = CELL//2 - 4
    ATTACKER_ICON = pygame.transform.scale(pygame.image.load(ATTACKER_ICON_FILE).convert_alpha(), (CELL_RADIUS*2, CELL_RADIUS*2)) 
    DEFENDER_ICON = pygame.transform.scale(pygame.image.load(DEFENDER_ICON_FILE).convert_alpha(), (CELL_RADIUS*2, CELL_RADIUS*2)) 
    KING_ICON = pygame.transform.scale(pygame.image.load(KING_ICON_FILE).convert_alpha(), (CELL_RADIUS*2, CELL_RADIUS*2)) 

def getNumberOfAttackers(board):
    count = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == PieceType.ATTACKER:
                count += 1
    return count

def getNumberOfDefenders(board):
    count = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == PieceType.DEFENDER or board[r][c] == PieceType.KING:
                count += 1
    return count

# ====== MAIN LOOP ======
running = True
gameElements.reset()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if appWindow ==Window.MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    gameElements.reset()
                    appWindow =Window.GAME
                elif settings_btn.collidepoint(event.pos):
                    appWindow =Window.SETTINGS 
            continue

        if appWindow == Window.SETTINGS:    
            if event.type == pygame.MOUSEBUTTONDOWN:         
                if difficulty_btn.collidepoint(event.pos):   
                    cycle_difficulty()                     
                elif p1_btn.collidepoint(event.pos):       
                    toggle_player1()                       
                elif p2_btn.collidepoint(event.pos):      
                    toggle_player2()      
                elif icon_btn.collidepoint(event.pos):      
                    toggle_icon()   
                elif board_size_btn.collidepoint(event.pos):      
                    toggle_board_size()   
                elif settings_back_btn.collidepoint(event.pos): 
                    appWindow = Window.MENU       
            continue

        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_btn.collidepoint(event.pos):
                appWindow = Window.MENU
                continue

            if undo_btn.collidepoint(event.pos): 
                undo_last_human_turn()         
                continue

        if gameElements.turn == TurnState.WIN_ATTACKER:
            continue
        
        if gameElements.turn == TurnState.WIN_DEFENDER:
            continue

        if prologInterface.terminalState(gameElements.board):
            if gameElements.turn == TurnState.ATTACKER:
                gameElements.turn = TurnState.WIN_DEFENDER
            else:
                gameElements.turn = TurnState.WIN_ATTACKER
            continue

        if gameElements.turn == TurnState.ATTACKER and getNumberOfAttackers(gameElements.board) == 0:
            gameElements.turn = TurnState.switch_turn(gameElements.turn)
            continue

        if gameElements.turn == TurnState.ATTACKER and AttackerPlayer == PlayerType.AI:
            AI_attackerMove()
            gameElements.turn = TurnState.switch_turn(gameElements.turn)
            continue

        if gameElements.turn == TurnState.DEFENDER and DefenderPlayer == PlayerType.AI:
            AI_defenderMove()
            gameElements.turn = TurnState.switch_turn(gameElements.turn)
            continue

        if event.type == pygame.MOUSEBUTTONDOWN:
            cell = get_cell(event.pos)
            if cell is None:
                continue

            r,c = cell
            r = int(r)
            c = int(c)
            if gameElements.selectedCell is None:
                if gameElements.board[r][c] == PieceType.ATTACKER and gameElements.turn == TurnState.ATTACKER:
                    gameElements.selectedCell = (r,c)
                elif gameElements.board[r][c] == PieceType.DEFENDER and gameElements.turn == TurnState.DEFENDER:
                    gameElements.selectedCell = (r,c)
                elif gameElements.board[r][c] == PieceType.KING and gameElements.turn == TurnState.DEFENDER:
                    gameElements.selectedCell = (r,c)
            else:
                sr,sc = gameElements.selectedCell
                if (r,c) == gameElements.selectedCell:
                    gameElements.selectedCell = None
                elif gameElements.board[r][c] == PieceType.EMPTY:
                    save_history(PlayerType.Human) 
                    if makeMove(sr, sc, r, c):
                        gameElements.selectedCell = None
                        gameElements.turn = TurnState.switch_turn(gameElements.turn)
                    else:
                        gameElements.history.pop()    
                else:
                    if gameElements.board[r][c] == PieceType.ATTACKER and gameElements.turn == TurnState.ATTACKER:
                        gameElements.selectedCell = (r,c)
                    elif gameElements.board[r][c] == PieceType.DEFENDER and gameElements.turn == TurnState.DEFENDER:
                        gameElements.selectedCell = (r,c)
                    elif gameElements.board[r][c] == PieceType.KING and gameElements.turn == TurnState.DEFENDER:
                        gameElements.selectedCell = (r,c)

    screen.fill(Colors.DARK_BLUE)

    if appWindow ==Window.MENU:
        Drawer.draw_menu()
    elif appWindow ==Window.SETTINGS:
        Drawer.draw_settings()   
    elif appWindow ==Window.GAME:
        Drawer.draw_board()
        Drawer.draw_panel()

    pygame.display.flip()

pygame.quit()
sys.exit()