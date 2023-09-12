import pygame
import random


class Snake:
    def __init__(self):
        self.dis_width = 600
        self.dis_height = 400
        self.snake_speed = 1
        self.speed_adjust = False
        self.snake_block = 25
        self.snake_border = round(self.snake_block / 20)
        self.size_of_food = 20
        self.border = round(30 / self.snake_block) * self.snake_block

        self.white = (255, 255, 255)
        self.yellow = 'yellow'
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        pygame.init()
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption('Змійка by VsKesha')
        self.clock = pygame.time.Clock()

    def get_food(self, snake):
        x = round(random.randrange(self.border, self.dis_width - self.snake_block - self.border) / self.snake_block) * self.snake_block
        y = round(random.randrange(self.border, self.dis_height - self.snake_block - self.border) / self.snake_block) * self.snake_block
        for x1, y1 in snake:
            if x == x1 and y == y1:
                x, y = self.get_food(snake)
        return [x, y]

    def your_score(self, score=0):
        score_font = pygame.font.SysFont("comicsansms", 35)
        value = score_font.render("Рахунок: " + str(score) + "    P - пауза", True, self.yellow)
        self.dis.blit(value, [0, 0])
        pygame.display.update()

    def your_speed(self, speed=1):
        speed_font = pygame.font.SysFont("comicsansms", 35)
        value = speed_font.render("Швидкість: " + str(speed), True, self.yellow)
        self.dis.blit(value, [self.dis_width - 180, 0])
        pygame.display.update()

    def show_message(self, msg, color, coords=None, font_size=30):
        coords = coords or (self.dis_width / 7, self.dis_height / 3)
        font_style = pygame.font.SysFont("comicsansms", font_size)
        mesg = font_style.render(msg, True, color)  # .set_alpha(100)
        self.dis.blit(mesg, coords)
        pygame.display.update()

    def refresh_screen(self):
        # makes grid on the screen
        self.dis.fill('black')
        for i in range(self.border + self.snake_block, self.dis_width - self.snake_block, self.snake_block):
            pygame.draw.line(self.dis, 'grey10', [i, self.border], [i, self.dis_height - self.border], self.snake_border * 2)
        for i in range(self.border + self.snake_block, self.dis_height - self.snake_block, self.snake_block):
            pygame.draw.line(self.dis, 'grey10', [self.border, i], [self.dis_width - self.border, i], self.snake_border * 2)
        border_points = [
            [self.border, self.border],
            [self.dis_width - self.border - self.snake_border, self.border],
            [self.dis_width - self.border - self.snake_border, self.dis_height - self.border - self.snake_border],
            [self.border, self.dis_height - self.border - self.snake_border]]
        pygame.draw.lines(self.dis, (150, 150, 150), True, border_points, self.snake_border * 2)

    def draw_food(self, foodx, foody):
        pygame.draw.circle(self.dis, 'yellow', [foodx + round(self.snake_block / 2), foody + round(self.snake_block / 2)],
                           self.size_of_food / 2)
        pygame.draw.circle(self.dis, self.blue, [foodx + round(self.snake_block / 2), foody + round(self.snake_block / 2)], self.size_of_food / 3)

    def draw_snake(self, snake, direct):
        # draw tail
        if len(snake) > 1:
            tail = snake[0]
            previos = snake[1]
            t1 = []
            t2 = []
            t3 = []
            if tail[0] > previos[0]:  # tail goes left
                t1 = [tail[0] + 1, tail[1] + 1]
                t2 = [tail[0] + 1, tail[1] + self.snake_block - 1]
                t3 = [tail[0] + self.snake_block, tail[1] + round(self.snake_block / 2)]
            if tail[0] < previos[0]:  # tail goes right
                t1 = [tail[0] + self.snake_block - 1, tail[1] + 1]
                t2 = [tail[0] + self.snake_block - 1, tail[1] + self.snake_block - 1]
                t3 = [tail[0], tail[1] + round(self.snake_block / 2)]
            else:
                if tail[1] > previos[1]:  # tail goes up
                    t1 = [tail[0] + 1, tail[1] + 1]
                    t2 = [tail[0] + self.snake_block - 1, tail[1] + 1]
                    t3 = [tail[0] + round(self.snake_block / 2), tail[1] + self.snake_block]
                elif tail[1] < previos[1]:  # tail goes down
                    t1 = [tail[0] + 1, tail[1] + self.snake_block - 1]
                    t2 = [tail[0] + self.snake_block - 1, tail[1] + self.snake_block - 1]
                    t3 = [tail[0] + round(self.snake_block / 2), tail[1]]
            points = [t1, t2, t3]
            pygame.draw.polygon(self.dis, self.green, points)
            # pygame.draw.polygon

        # draw body of snake
        for x in snake[1:-1]:
            pygame.draw.rect(self.dis, self.green, [x[0] + 1, x[1] + 1, self.snake_block - 2, self.snake_block - 2])

        # draw_head(snake)
        head = snake[-1]
        center = [head[0] + round(self.snake_block / 2), head[1] + round(self.snake_block / 2)]
        head_radius = self.snake_block / 1.4
        pygame.draw.circle(self.dis, self.green, [center[0], center[1]], head_radius)

        # draw_eyes and tongue
        eyes_color = 'white'
        tongue_color = 'red'
        eye_size = head_radius * 0.35
        distance_forward = round(head_radius * 0.4)
        distance_between_eyes = round(head_radius * 0.5)
        tongue_length = round(head_radius * 0.3)
        tongue_thickness = round(head_radius * 0.05)
        eye_coord1 = []
        eye_coord2 = []
        tongue_coord = []
        if not direct:
            direct = 'right'
        if direct == 'up':
            eye_coord1 = [center[0] - distance_between_eyes, center[1] - distance_forward]
            eye_coord2 = [center[0] + distance_between_eyes, center[1] - distance_forward]
            tongue_coord = [center[0] - tongue_thickness, center[1] - head_radius - tongue_length, tongue_thickness * 2,
                            tongue_length]
        elif direct == 'down':
            eye_coord1 = [center[0] - distance_between_eyes, center[1] + distance_forward]
            eye_coord2 = [center[0] + distance_between_eyes, center[1] + distance_forward]
            tongue_coord = [center[0] - tongue_thickness, center[1] + head_radius, tongue_thickness * 2, tongue_length]
        elif direct == 'left':
            eye_coord1 = [center[0] - distance_forward, center[1] + distance_between_eyes]
            eye_coord2 = [center[0] - distance_forward, center[1] - distance_between_eyes]
            tongue_coord = [center[0] - head_radius - tongue_length, center[1] - tongue_thickness, tongue_length,
                            tongue_thickness * 2]
        elif direct == 'right':
            eye_coord1 = [center[0] + distance_forward, center[1] - distance_between_eyes]
            eye_coord2 = [center[0] + distance_forward, center[1] + distance_between_eyes]
            tongue_coord = [center[0] + head_radius, center[1] - tongue_thickness, tongue_length, tongue_thickness * 2]
        pygame.draw.circle(self.dis, eyes_color, eye_coord1, eye_size)
        pygame.draw.circle(self.dis, 'black', eye_coord1, eye_size / 2)
        pygame.draw.circle(self.dis, eyes_color, eye_coord2, eye_size)
        pygame.draw.circle(self.dis, 'black', eye_coord2, eye_size / 2)
        pygame.draw.rect(self.dis, tongue_color, tongue_coord)
        # pygame.draw.ellipse

    def game_menu(self):
        global snake_speed
        global speed_adjust
        self.refresh_screen()
        self.your_score()
        self.your_speed()
        menu_bg = pygame.Surface([self.dis_width, self.dis_height])  # .set_alpha(50)
        pygame.draw.rect(menu_bg, 'grey20', [0, 0, self.dis_width, self.dis_height])
        menu_bg.set_alpha(200)
        self.dis.blit(menu_bg, [0, 0])
        self.show_message("ЗМІЙКА", "grey5", [self.dis_width / 2 - 100, self.border], 80)
        self.show_message("by vskesha", "dark green", [self.dis_width / 2 + 100, self.border + 50], 30)
        x = self.dis_width / 2 - 200
        y = self.dis_height / 2
        self.show_message("Вибери швидкість:", 'black', [x, y], 50)
        self.show_message('"1" - "9" вибрати швидкість', 'black', [x, y + 50], 30)
        self.show_message('"A" - автоматично', 'black', [x, y + 80], 30)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.game_close()
                    elif event.key == pygame.K_a:
                        speed_adjust = True
                        break
                    elif event.key == pygame.K_1:
                        snake_speed = 1
                        break
                    elif event.key == pygame.K_2:
                        snake_speed = 2
                        break
                    elif event.key == pygame.K_3:
                        snake_speed = 3
                        break
                    elif event.key == pygame.K_4:
                        snake_speed = 4
                        break
                    elif event.key == pygame.K_5:
                        snake_speed = 5
                        break
                    elif event.key == pygame.K_6:
                        snake_speed = 6
                        break
                    elif event.key == pygame.K_7:
                        snake_speed = 7
                        break
                    elif event.key == pygame.K_8:
                        snake_speed = 8
                        break
                    elif event.key == pygame.K_9:
                        snake_speed = 9
                        break
            else:
                continue
            break

    def game_pause(self):
        # print("GAME PAUSED")
        paused = True
        x = self.dis_width / 4
        y = self.dis_height / 3
        self.show_message("ПАУЗА!", self.red, [x, y], 50)
        self.show_message("Нажми С для продовження", self.red, [x, y + 65], 35)
        self.show_message("Нажми Q щоб вийти", self.red, [x, y + 100], 35)

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        # print("GAME RESUMED")
                        paused = False
                    if event.key == pygame.K_q:
                        self.game_close()

    def game_close(self):
        pygame.quit()
        quit()

    def game_over(self):
        while True:
            x = self.dis_width / 4
            y = self.dis_height / 3
            self.show_message("ПОРАЗКА!", self.red, [x, y], 50)
            self.show_message("Нажми С - нова гра", self.red, [x, y + 65], 35)
            self.show_message("Нажми Q - вийти", self.red, [x, y + 100], 35)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.game_close()
                    if event.key == pygame.K_c:
                        self.gameloop()

    def gameloop(self):
        # getting start position of the snake
        x1 = round(self.dis_width / 2 / self.snake_block) * self.snake_block
        y1 = round(self.dis_height / 2 / self.snake_block) * self.snake_block
        direction = 'right'
        snake_List = []
        Length_of_snake = 3
        Score = 0
        foodx, foody = self.get_food(snake_List)
        global snake_speed
        global speed_adjust
        self.game_menu()

        while True:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    self.game_close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.game_pause()
                    elif event.key == pygame.K_q:
                        self.game_close()
                    elif event.key == pygame.K_LEFT and direction != 'right':
                        direction = 'left'
                    elif event.key == pygame.K_RIGHT and direction != 'left':
                        direction = 'right'
                    elif event.key == pygame.K_UP and direction != 'down':
                        direction = 'up'
                    elif event.key == pygame.K_DOWN and direction != 'up':
                        direction = 'down'

            if direction == 'left':
                x1 -= self.snake_block
            elif direction == 'right':
                x1 += self.snake_block
            elif direction == 'up':
                y1 -= self.snake_block
            elif direction == 'down':
                y1 += self.snake_block

            if x1 >= self.dis_width - self.border or x1 < self.border or y1 >= self.dis_height - self.border or y1 < self.border:
                self.game_over()

            snake_head = [x1, y1]
            snake_List.append(snake_head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_head:
                    self.game_over()

            self.refresh_screen()
            self.draw_food(foodx, foody)
            self.draw_snake(snake_List, direction)
            self.your_score(Score)
            self.your_speed(snake_speed)

            if x1 == foodx and y1 == foody:
                self.show_message("Нямм", 'yellow', [foodx + self.snake_block, foody + self.snake_block])
                foodx, foody = self.get_food(snake_List)
                Length_of_snake += 1
                Score += snake_speed
            if self.speed_adjust:
                snake_speed = 1 + (Length_of_snake - 3) // 10
            self.clock.tick(snake_speed)


def main():
    snake = Snake()
    snake.gameloop()


if __name__ == '__main__':
    main()
