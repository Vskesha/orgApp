from tkinter import *
from time import sleep


class HanoiTower(Canvas):

    def __init__(self):
        super().__init__(bg='grey40')
        self.n_game = None
        self.text_info = None
        self.previous_column = 0
        self._from = None
        self._to = None
        self.end_position = None
        self.end_position_rect = None
        self.choose_button = None
        self.choose_text = None
        self.selected = False
        self.master.title('Hanoi Tower')
        self.pack(fill=BOTH, expand=TRUE)
        self.update()
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.bagels = [[], [], []]
        self.min_bagel = 10
        self.draw_towers()
        self.choosing_start_position()
        self.colors = ('grey20', 'grey30', 'grey40', 'purple', 'blue', 'cyan', 'green', 'yellow', 'orange', 'red')

    def draw_towers(self):
        radius = (self.width / 60)
        height = (self.height * 0.7)
        base_radius = (self.width / 7)
        base_height = (self.height / 30)
        for i in range(3):
            down_point = (self.width * (i / 3 + 1 / 6), self.height * 0.85)
            self.create_rectangle(down_point[0] - radius,
                                  down_point[1] - height,
                                  down_point[0] + radius,
                                  down_point[1],
                                  fill='white', outline='black')
            self.create_rectangle(down_point[0] - base_radius,
                                  down_point[1],
                                  down_point[0] + base_radius,
                                  down_point[1] + base_height,
                                  fill='white', outline='black')
        self.text_info = self.create_text(self.width / 2, self.height / 2, anchor=CENTER,
                                          font=f'Arial {self.height//8} bold')
        self.update()

    def choosing_start_position(self):
        # print('Choosing start position')
        self.choose_text = self.create_text(self.width / 2, self.height / 20,
                                            font=f'Arial {self.height // 40} bold',
                                            anchor=CENTER,
                                            text='Choose start position and press "OK"')
        self.choose_button = Button(self, anchor=CENTER, background='cyan',
                                    font=f'Arial {self.height // 40} bold',
                                    text='OK', padx=70)
        self.choose_button.place(x=self.width / 2, y=self.height * 19 / 20, anchor=CENTER)
        self.bind('<Button-1>', self.add_bagel)
        self.n_game = Button(self, anchor=CENTER, background='cyan',
                             font=f'Arial {self.height // 40} bold',
                             text='New game', command=self.new_game,
                             padx=40)
        self.n_game.place(x=self.width * 5 // 6, y=self.height * 19 / 20, anchor=CENTER)

    def new_game(self):
        self.destroy()
        HanoiTower()

    def add_bagel(self, event):
        self.choose_button.configure(command=self.choosing_end_position)
        if self.min_bagel < 1:
            return
        i = event.x // (self.width // 3)
        bagel = self.draw_bagel(bagel_column=i, column_amount=len(self.bagels[i]), bagel_size=self.min_bagel)
        self.bagels[i].append([self.min_bagel, bagel, i])
        self.previous_column = i
        self.min_bagel -= 1

    def choosing_end_position(self):
        # print('Start position selected. Choosing end position')
        # print(self.bagels)
        self.itemconfigure(self.choose_text, text='Choose end position and press "OK"')
        self.update()
        self.unbind('<Button-1>')
        self.bind('<Button-1>', self.draw_end_position)

    def automatically(self):
        # print('automatically')
        self.delete(self.choose_text)
        self.choose_button.destroy()
        self.unbind('<Button-1>')
        for n in range(1, 11-self.min_bagel):
            maximum = self.min_bagel + n
            max_column = 0
            for i, column in enumerate(self.bagels):
                for bagel in column:
                    if bagel[0] == maximum:
                        max_column = i
            if max_column == self.previous_column:
                continue
            temp_column = 3 - max_column - self.previous_column
            if ((self.bagels[temp_column] and self.bagels[temp_column][-1][0] - self.bagels[max_column][-1][0] == 1)
                    or (n == 10 and not self.bagels[temp_column]) and temp_column == self.end_position):
                self._from = max_column
                self._to = temp_column
                # print('Moving without recursion')
                self.move_bagel()
                sleep(0.05)
                max_column = temp_column
            self.auto_moving(fr=self.previous_column, to=max_column, n=n - 1)
            self.previous_column = max_column
        if self.previous_column != self.end_position:
            self.auto_moving(fr=self.previous_column, to=self.end_position, n=10 - self.min_bagel)

    def auto_moving(self, fr, to, n):
        temp = 3 - fr - to
        if n <= 1:
            self._from = fr
            self._to = to
            self.move_bagel()
            return
        self.auto_moving(fr=fr, to=temp, n=n - 1)
        sleep(0.05)
        self._from = fr
        self._to = to
        self.move_bagel()
        sleep(0.05)
        self.auto_moving(fr=temp, to=to, n=n - 1)
        sleep(0.05)

    def gaming(self):
        # print(f"End position - {self.end_position}. It is gaming")
        self.itemconfigure(self.choose_text, text='Move rings from one tower to another. Try to solve this')
        self.unbind('<Button-1>')
        self.bind('<Button-1>', self.get_from_to)
        self.choose_button.configure(command=self.automatically, text='Auto')

    def get_from_to(self, event):
        i = event.x // (self.width // 3)
        if self._from is None:
            if self.bagels[i]:
                self._from = i
                self.itemconfigure(self.bagels[i][-1][1], width=5)
        else:
            self._to = i
            self.move_bagel()

    def move_bagel(self):
        # print(f'Try to move from {self._from} to {self._to}.  ', end='')
        ba = self.bagels
        to = self._to
        fr = self._from
        if fr == to:
            self.itemconfigure(ba[fr][-1][1], width=1)
        elif ba[fr]:
            if not ba[to] or ba[fr][-1][0] < ba[to][-1][0]:
                # moving bagel to respective position
                # print('-->  Ok')
                self.itemconfigure(ba[fr][-1][1], width=1)
                self.coords(ba[fr][-1][1], *self.bagel_coords(to, len(ba[to]), ba[fr][-1][0]))
                self.update()
                ab = ba[fr].pop()
                ab[2] = to
                ba[to].append(ab)
            else:
                # print('-->  Bagel is bigger')
                self.itemconfigure(ba[fr][-1][1], width=1)
                self.itemconfigure(self.text_info, text='Bagel is bigger', fill='red')
                self.update()
                sleep(1)
                self.itemconfigure(self.text_info, text='')
                self.update()
        else:
            # print('-->  There is no bagels')
            self.itemconfigure(self.text_info, text='There is no bagels', fill='red')
            self.update()
            sleep(1)
            self.itemconfigure(self.text_info, text='')
            self.update()
        self.winner()
        self._from = self._to = None

    def winner(self):
        bagels = self.bagels
        i = self.end_position
        if bagels[i] and not bagels[(i + 1) % 3] and not bagels[(i + 2) % 3]:
            # print('You win!!!')
            self.itemconfigure(self.text_info, text='YOU WIN!!!', fill='green')
            self.update()

    def draw_end_position(self, event):
        self.choose_button.configure(command=self.gaming)
        self.end_position = event.x // (self.width // 3)
        # print(self.end_position)
        xc = self.width * (1 / 6 + self.end_position / 3)
        yc = self.height / 2
        w = self.width / 6.1
        h = self.height * 0.4
        if self.end_position_rect is None:
            self.end_position_rect = self.create_rectangle(xc-w, yc-h, xc+w, yc+h, outline='green', width=3)
        else:
            self.coords(self.end_position_rect, xc-w, yc-h, xc+w, yc+h)
        self.update()

    def draw_bagel(self, bagel_column, column_amount, bagel_size):
        coords = self.bagel_coords(bagel_column, column_amount, bagel_size)
        return self.create_rectangle(*coords,
                                     fill=self.colors[bagel_size - 1],
                                     outline='black')

    def bagel_coords(self, bagel_column, column_amount, bagel_size):
        bagel_height = self.height * 0.7 / 10
        bagel_radius = self.width / 30 + bagel_size * self.width / 80
        down_position = self.height * 0.85 - column_amount * bagel_height
        bagel_x_position = self.width * (bagel_column / 3 + 1 / 6)
        return (bagel_x_position - bagel_radius,
                down_position - bagel_height,
                bagel_x_position + bagel_radius,
                down_position)


def main():
    win = Tk()
    win.update()
    width = win.winfo_screenwidth() // 10
    height = win.winfo_screenheight() // 10
    win.geometry(f'{width * 8}x{height * 8}+{width}+{height}')
    HanoiTower()
    win.mainloop()


if __name__ == '__main__':
    main()
