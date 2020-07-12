import pygame
import time
from main import valid, solve
from boards import get_board
from time import sleep

pygame.init()

white = (255, 255, 255)
grey = (230, 230, 230)
black = (0, 0, 0)
blue = (0, 0, 38)
red = (255, 0, 0)

s_width = 550
s_height = 650
play_width = 495
play_height = 495
box_size = 55
top_left_x = 29
top_left_y = 110

BG = pygame.transform.scale(pygame.image.load(
    "images/bg.gif"), (s_width, s_height))

font1 = pygame.font.SysFont("comicsans", 60)
font2 = pygame.font.SysFont("comicsans", 25)
font3 = pygame.font.SysFont("comicsans", 30)
font5 = pygame.font.SysFont("comicsans", 40)

# =================================


class Grid:
    board = get_board()

    def __init__(self, width, height, rows=9, cols=9):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height)
                       for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    # when we delete/backspace
    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    # get position of element in board (row, column)
    def click(self, pos):
        if (pos[0] > 29 and pos[0] < 524) and (pos[1] > 110 and pos[1] < 705):
            x = (pos[0] - 29)//box_size
            y = (pos[1] - 110)//box_size
            return (int(y), int(x))
        else:
            return None

    # assigns selected True for the box selected, False for everything else
    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(
            self.cols)] for i in range(self.rows)]

    # takes user entered value and check if it's the right number
    def place(self, val):
        row, col = self.selected
        # only if it's already empty
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, self.selected) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, black, (int(top_left_x), int((i * box_size) + top_left_y)),
                             (int(play_width + top_left_x), int((i * box_size) + top_left_y)), thick)
            pygame.draw.line(win, black, (int((i * box_size) + top_left_x), int(top_left_y)),
                             (int((i * box_size) + top_left_x), int(play_height + top_left_y)), thick)

        for i in range(9):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

# =================================


class Cube:

    def __init__(self, value, row, col, width, height):
        self.value = value
        # value, values present there when user hits enter
        self.temp = 0
        # temp, value user enters (before hitting enter)
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

    def draw(self, win):
        x = top_left_x + (self.col * box_size)
        y = top_left_y + (self.row * box_size)
        if self.temp != 0 and self.value == 0:
            text = font5.render(str(self.temp), 1,
                                (128, 128, 128), (255, 255, 255))
            win.blit(text, (int(x+5), int(y+5)))
        elif not(self.value == 0):
            text = font5.render(str(self.value), 1, (0, 0, 0), (255, 255, 255))
            win.blit(text, (int(x + (box_size/2 - text.get_width()/2)),
                            int(y + (box_size/2 - text.get_height()/2))))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, box_size, box_size), 3)

# =================================


def main():
    icon = pygame.image.load("images/icon.png")
    pygame.display.set_icon(icon)

    # pygame.mixer.music.load("bg_music.mp3")
    # pygame.mixer.music.play(-1)

    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption("Sudoku")

    label = font1.render("SUDOKU", 1, white)
    warn = font2.render("(15 chances / block)", 1, grey, blue)
    time_show = font2.render(" Press 'M' to mute ", 1, black, white)

    win.blit(BG, (0, 0))
    win.blit(label, (int(top_left_x + play_width/2 - (label.get_width()/2)), 20))
    win.blit(warn, (int(s_width - warn.get_width() - 15), 75))
    win.blit(time_show, (int(s_width - time_show.get_width() - 15), 50))

    win.fill((250, 250, 250), ((top_left_x, top_left_y),
                               (play_width, play_height)))

    pygame.display.update()

    # -----------------------------------------------------------------------------

    key = None
    start = time.time()
    strikes = 0
    board = Grid(play_width, play_height)

    run = True
    while run:
        play_time = round(time.time()-start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    pygame.mixer.music.pause()
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if not board.place(board.cubes[i][j].temp):
                            strikes += 1
                        key = None
                    if board.is_finished():
                        font4 = pygame.font.SysFont("comicsans", 70)
                        text = font4.render("GAME OVER !", 1, grey)
                        win.blit(text, (int(s_width/2 - (text.get_width()/2)),
                                        int(s_height/2 - (text.get_height()/2))))
                        run = False

            # when mouse pressed, Grid selected stores (i,j) Cube selected = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # loc selected, (row,col) sent
                clicked = board.click(pos)
                if clicked:
                    # Grid selected stores (row,col)
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes, s_width, s_height)
        pygame.display.update()

# ============================


def format_time(secs):
    sec = secs % 60
    minute = secs//60
    hour = minute//60

    mat = str(minute) + ":" + str(sec) + "  "
    return mat

# =============================


def redraw_window(win, board, time, strikes, width, height):
    text = font3.render("Time: " + format_time(time),
                        1, white, (0, 0, 38))
    win.blit(text, (int(width - 130), int(height - 30)))

    text = font3.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (30, int(height - 30)))

    board.draw(win)


main()
sleep(1)
pygame.quit()