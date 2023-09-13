import tkinter
import random
import time


class TicTacToe(tkinter.Canvas):
    def __init__(self, window, width=300):
        self.width = width
        super().__init__(window, width=self.width, height=self.width, background='grey70')
        self.state = [None, None, None, None, None, None, None, None, None]
        self.empty_squares = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.win_combinations = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        self.colors = (('brown1', 'brown2', 'coral', 'coral3', 'OliveDrab1', 'orange red'),
                       ('cyan', 'cyan3', 'cornflower blue', 'DarkBlue', 'dark cyan', 'navy'))
        self.get_colors()
        self.bind('<Button-1>', self.click)
        self.game_menu = True
        self.game_running = True
        self.ready = True
        self.game_mode = ''
        self.first_move_x = 1  # 1 - first move x; -1 - first move o
        self.last_win = ''
        self.win_table = {'x_win': 0, 'o_win': 0, 'draw': 0}

    def click(self, event):
        if self.game_menu == True:
            w = self.width / 3
            h = self.width / 10
            n = self.width / 4
            if event.x > 2 * n - w and event.x < 2 * n + w:
                if event.y > n - h and event.y < n + h:
                    self.game_mode = 'comp hard'
                elif event.y > 2 * n - h and event.y < 2 * n + h:
                    self.game_mode = 'comp easy'
                elif event.y > 3 * n - h and event.y < 3 * n + h:
                    self.game_mode = 'person person'
            if self.game_mode:
                self.first_move_x = 1
                self.last_win = ''
                self.win_table = {'x_win': 0, 'o_win': 0, 'draw': 0}
                self.start_new_game()
                self.game_menu = False
        elif self.game_running and self.ready:
            x = self.width / 2
            y = self.width * 30 / 31
            h = self.width / 30
            w = h * 3
            if x - w < event.x < x + w and y - h < event.y < y + h:
                self.game_menu = True
                self.draw_menu()
            else:
                column = event.x // round(self.width / 3)
                row = event.y // round(self.width / 3)
                i = row * 3 + column
                if self.state[i] is None:
                    if self.game_mode == 'person person':
                        if self.first_move_x == 1:
                            if len(self.empty_squares) % 2:
                                self.state[i] = 'x'
                            else:
                                self.state[i] = 'o'
                        if self.first_move_x == -1:
                            if len(self.empty_squares) % 2:
                                self.state[i] = 'o'
                            else:
                                self.state[i] = 'x'
                    else:
                        self.state[i] = 'x'
                    self.empty_squares.remove(i)
                    self.add_figure(column, row)
                    self.get_winner()
                    if not self.last_win and self.game_mode != 'person person':
                        self.bot_move()
        elif self.ready:
            self.start_new_game()

    def bot_move(self):
        if self.empty_squares:
            i = self.best_move()
        else:
            return
        self.state[i] = 'o'
        self.empty_squares.remove(i)
        column = i % 3
        row = i // 3
        self.add_figure(column, row)
        self.get_winner()

    def best_move(self):
        if self.game_mode == 'comp easy' and len(self.empty_squares) > 7:
            return random.choice(self.empty_squares)
        for combination in self.win_combinations:
            i, j, k = combination
            line = [self.state[i], self.state[j], self.state[k]]
            if line.count('o') == 2 and None in line:
                return combination[line.index(None)]
        for combination in self.win_combinations:
            i, j, k = combination
            line = [self.state[i], self.state[j], self.state[k]]
            if line.count('x') == 2 and None in line:
                return combination[line.index(None)]
        free_combination = []
        future_combination = []
        future_xcombination = []
        for combination in self.win_combinations:
            i, j, k = combination
            line = [self.state[i], self.state[j], self.state[k]]
            if line.count('x') == 0:
                for l in range(3):
                    if line[l] != 'o':
                        free_combination.append(combination[l])
                if line.count('o') == 1:
                    for l in range(3):
                        if line[l] != 'o':
                            future_combination.append(combination[l])
            if line.count('o') == 0 and line.count('x') == 1:
                for l in range(3):
                    if line[l] != 'x':
                        future_xcombination.append(combination[l])
        for i in range(9):
            if future_xcombination.count(i) == 2:
                return i
        for i in range(9):
            if future_combination.count(i) == 2:
                return i
        max_count = 0
        max_index = random.choice(self.empty_squares)
        for i in range(9):
            if max_count < free_combination.count(i):
                max_count = free_combination.count(i)
                max_index = i
        return max_index

    def get_colors(self):
        self.x_color = random.choice(self.colors[0])
        self.o_color = random.choice(self.colors[1])

    def draw_menu(self):
        self.delete('all')
        self.draw_button(self.width / 2, self.width / 4, 'КОМП ТЯЖКО')
        self.draw_button(self.width / 2, self.width / 2, 'КОМП ЛЕГКО')
        self.draw_button(self.width / 2, self.width * 3 / 4, 'ДВА ГРАВЦІ')
        self.sign()

    def draw_button(self, x, y, text):
        w = self.width / 3
        h = self.width / 10
        self.create_oval(x - w - h, y - h, x - w + h, y + h, fill='grey15', outline='black')
        self.create_oval(x + w - h, y - h, x + w + h, y + h, fill='grey15', outline='black')
        self.create_rectangle(x - w, y - h, x + w, y + h, fill='grey15', outline='grey15')
        self.create_line(x - w, y - h, x + w, y - h, fill='black')
        self.create_line(x - w, y + h, x + w, y + h, fill='black')
        self.create_text(x, y + h / 5, text=text, font=('Courier', round(h * 0.75), 'bold'), fill='white')

    def add_figure(self, column, row):
        if len(self.empty_squares) % 2:
            self.add_o(column, row)
        else:
            self.add_x(column, row)

    def add_x(self, column, row):
        x = column * round(self.width / 3)
        y = row * round(self.width / 3)
        self.create_line(
            x + round(self.width / 20),
            y + round(self.width / 20),
            x + round(self.width * 85 / 300),
            y + round(self.width * 85 / 300),
            width=round(self.width / 50),
            fill=self.x_color)
        self.create_line(
            x + round(self.width * 85 / 300),
            y + round(self.width / 20),
            x + round(self.width / 20),
            y + round(self.width * 85 / 300),
            width=round(self.width / 50),
            fill=self.x_color)
        self.update()

    def add_o(self, column, row):
        x = column * round(self.width / 3)
        y = row * round(self.width / 3)
        self.create_oval(
            x + round(self.width / 20),
            y + round(self.width / 20),
            x + round(self.width * 85 / 300),
            y + round(self.width * 85 / 300),
            width=round(self.width / 50),
            outline=self.o_color)
        self.update()

    def draw_lines(self):
        self.delete('all')
        x = round(self.width / 3)
        s = self.width
        self.create_line(x, 0, x, s, fill='grey20')
        self.create_line(2 * x, 0, 2 * x, s, fill='grey20')
        self.create_line(0, x, s, x, fill='grey20')
        self.create_line(0, 2 * x, s, 2 * x, fill='grey20')
        self.update()
        self.sign()

    def draw_explanation(self):
        pos_x = self.width / 6
        pos_o = self.width / 2
        width = self.width / 100
        size = self.width / 35
        if self.game_mode == 'person person':
            if self.first_move_x == 1:
                text = ' - Гравець1      - Гравець2 '
            else:
                text = ' - Гравець2      - Гравець1 '
        else:
            if self.first_move_x == 1:
                text = ' - Гравець       - Компʼютер'
            else:
                text = ' - Компʼютер     - Гравець  '
        self.create_line(pos_x, width, pos_x + size, width + size, width=width, fill=self.x_color)
        self.create_line(pos_x + size, width, pos_x, width + size, width=width, fill=self.x_color)
        self.create_oval(pos_o, width, pos_o + size, width + size, width=width, outline=self.o_color)
        self.create_text(pos_o, size, text=text, font=('Courier', round(size), 'bold'), fill='grey15')
        self.update()

    def draw_menu_button(self):
        x = self.width / 2
        y = self.width * 30 / 31
        h = self.width / 30
        w = h * 3
        self.create_rectangle(x - w, y - h, x + w, y + h, outline='black', fill='grey15')
        self.create_text(x, y + h / 3, text='МЕНЮ', font=('Courier', round(h * 1.5), 'bold'), fill='white')
        self.update()

    def draw_winline(self):
        if self.win_line < 3:  # draw horizontal winline
            self.create_line(
                0,
                self.width * (self.win_combinations[self.win_line][0] / 9 + 1 / 6),
                self.width,
                self.width * (self.win_combinations[self.win_line][0] / 9 + 1 / 6),
                width=round(self.width / 50),
                fill=random.choice(random.choice(self.colors)))
        elif self.win_line < 6:  # draw vertical winline
            self.create_line(
                self.width * (self.win_combinations[self.win_line][0] / 3 + 1 / 6),
                0,
                self.width * (self.win_combinations[self.win_line][0] / 3 + 1 / 6),
                self.width,
                width=round(self.width / 50),
                fill=random.choice(random.choice(self.colors)))
        elif self.win_line == 6:  # first diagonal line
            self.create_line(
                0,
                0,
                self.width,
                self.width,
                width=round(self.width / 50),
                fill=random.choice(random.choice(self.colors)))
        elif self.win_line == 7:  # second diagonal line
            self.create_line(
                self.width,
                0,
                0,
                self.width,
                width=round(self.width / 50),
                fill=random.choice(random.choice(self.colors)))
        self.update()

    def draw_wintable(self):
        text = ''
        if self.last_win == 'x_win':
            if self.game_mode == 'person person':
                text = '1-й виграв'
            else:
                text = 'Ви виграли'
        elif self.last_win == 'o_win':
            if self.game_mode == 'person person':
                text = '2-й виграв'
            else:
                text = 'Ви програли'
        else:
            text = 'Нічия'
        self.create_text(self.width / 2, self.width / 2,
                         text=text, font=('Arial', round(self.width / 10), 'bold'), fill='grey15')
        self.update()
        time.sleep(1)
        self.delete('all')
        self.sign()
        if self.game_mode == 'person person':
            text = ['Гравець1', 'Гравець2']
        else:
            text = ['Перемоги', 'Поразки ']
        self.create_text(self.width / 2, self.width / 2.5,
                         text=f'{text[0]} - {self.win_table["x_win"]}\n{text[1]} - {self.win_table["o_win"]}\nНічия    - {self.win_table["draw"]}',
                         font=('Courier', round(self.width / 11), 'bold'), fill='grey15')
        self.update()
        time.sleep(1)
        self.create_text(self.width / 2, self.width * 3 / 4,
                         text='Клацни для продовження',
                         font=('Arial', round(self.width / 25), 'italic'), fill='brown')

    def sign(self):
        self.create_text(self.width * 9 / 10, self.width * 39 / 40,
                         text='by VsKesha', font=('Arial', round(self.width / 40), 'italic'), fill='Blue')
        self.update()

    def start_new_game(self):
        self.state = [None, None, None, None, None, None, None, None, None]
        self.empty_squares = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.get_colors()
        self.delete('all')
        self.draw_lines()
        self.draw_explanation()
        self.draw_menu_button()
        self.game_running = True
        if self.first_move_x == -1 and self.game_mode != 'person person':
            self.bot_move()

    def get_winner(self):
        self.last_win = ''
        if not self.empty_squares:
            self.last_win = 'draw'
            self.win_line = 9
        for n, combination in enumerate(self.win_combinations):
            i, j, k = combination
            if self.state[i] and self.state[i] == self.state[j] and self.state[j] == self.state[k]:
                self.win_line = n
                if self.state[i] == 'x':
                    self.last_win = 'x_win'
                elif self.state[i] == 'o':
                    self.last_win = 'o_win'
        if self.last_win:
            self.game_ending()

    def game_ending(self):
        self.ready = False
        self.game_running = False
        self.win_table[self.last_win] += 1
        if self.win_line < 9:
            for i in range(5):
                self.draw_winline()
                time.sleep(0.3)
        self.draw_wintable()
        if self.last_win == 'x_win':
            self.first_move_x = 1
        elif self.last_win == 'o_win':
            self.first_move_x = -1
        else:
            self.first_move_x *= -1
        self.ready = True


def main():
    window = tkinter.Tk()
    window.title('Хрестики-Нyлики')
    game = TicTacToe(window, 600)
    game.pack()
    game.draw_menu()
    window.mainloop()


if __name__ == '__main__':
    main()
