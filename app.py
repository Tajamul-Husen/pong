"""
Pygame a library that helps to make games on python easy-peasy.
"""
import pygame
import constants as c


class DottedLine():
    """
    Middle dotted line object.
    """

    def __init__(self, xpos, width, height):
        self.xpos = xpos
        self.width = width
        self.height = height

    def draw(self, win, rnge, ypos):
        """
        Draw dotted line to screen.
        """
        for _ in range(rnge):
            pygame.draw.rect(win, (255, 255, 255),
                             (self.xpos, ypos, self.width, self.height))
            ypos += (self.height + 5)


class ScoreText():
    """
    Player score text object.
    """

    def __init__(self, text='freesansbold.ttf', size=75):
        self.text = text
        self.size = size

    def draw(self, width, height, score):
        """
        Draw score to screen.
        """
        f_text = pygame.font.Font(self.text, self.size)
        text = f_text.render(str(score), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (width, height)
        return (text, text_rect)


class Ball():
    """
    Pong ball object.
    """

    def __init__(self, xpos, ypos, rad, dx, dy):
        self.ball_x = xpos
        self.ball_y = ypos
        self.ball_dx = dx
        self.ball_dy = dy
        self.ball_r = rad
        self.flip_x = False
        self.flip_y = False

    def draw(self, win):
        """
        Draw ball tn screen.
        """
        pygame.draw.circle(win, (255, 255, 255),
                           (self.ball_x, self.ball_y), self.ball_r)

    def move_x(self):
        """
        Set ball x-axis to forward or reverse.
        """
        if not self.flip_x:
            self.ball_x += self.ball_dx
        else:
            self.ball_x -= self.ball_dx

    def move_y(self):
        """
        Set ball y-axis to forward or reverse.
        """
        if not self.flip_y:
            self.ball_y += self.ball_dy
        else:
            self.ball_y -= self.ball_dy

    def reset(self, width, height):
        """
        Reset ball x, y positon.
        """
        self.ball_x = width
        self.ball_y = height


class Paddle():
    """
    Pong paddle object.
    """

    def __init__(self, xpos, ypos, width, height, dy):
        self.paddle_width = width
        self.paddle_height = height
        self.paddle_dy = dy
        self.paddle_x = xpos - (self.paddle_width // 2)
        self.paddle_y = ypos - (self.paddle_height // 2)
        self.score = 0

    def draw(self, win):
        """
        Draw the paddle to screen.
        """
        pygame.draw.rect(win, (255, 255, 255),
                         (self.paddle_x,
                          self.paddle_y, self.paddle_width, self.paddle_height))

    def move_up(self):
        """
        Move paddle up on event.
        """

        if self.paddle_y <= 0:
            self.paddle_y = 0
        else:
            self.paddle_y -= self.paddle_dy

    def move_down(self, height):
        """
        Move paddle down on event.
        """

        if self.paddle_y >= (height - self.paddle_height):
            self.paddle_y = (height - self.paddle_height)
        else:
            self.paddle_y += self.paddle_dy

    def score_update(self, ball, bl_dx, bl_dy, p_dy):
        """
        Update paddle score on score props.
        """
        ball.ball_dx = bl_dx
        ball.ball_dy = bl_dy
        self.paddle_dy = p_dy


def game_loop(width, height, speed):
    """
    Gameloop base setting and defined objects
    """
    run = True
    start = False
    clock = pygame.time.Clock()
    paddle_count = 0

    screen_width = width
    screen_height = height
    game_speed = speed

    text_left = ScoreText('freesansbold.ttf', 75)
    text_right = ScoreText('freesansbold.ttf', 75)
    dot_line = DottedLine(screen_width // 2 - 2, 4, 4)
    ball = Ball(screen_width // 2, screen_height // 2, 6, 1, 1)
    paddle_left = Paddle(10, screen_height // 2, 10, 70, 1)
    paddle_right = Paddle(screen_width - 10, screen_height // 2, 10, 70, 1)
    window = pygame.display.set_mode((screen_width, screen_height))
    bounce = pygame.mixer.Sound("./assets/bounce.wav")

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_UP]:
            paddle_right.move_up()
        if pressed_keys[pygame.K_DOWN]:
            paddle_right.move_down(screen_height)
        if pressed_keys[pygame.K_w]:
            paddle_left.move_up()
        if pressed_keys[pygame.K_s]:
            paddle_left.move_down(screen_height)

        window.fill((0, 0, 0))

        t_left = text_left.draw(
            screen_width // 2 - 100, 50, paddle_left.score)
        t_right = text_right.draw(
            screen_width // 2 + 100, 50, paddle_right.score)

        window.blit(t_left[0], t_left[1])
        window.blit(t_right[0], t_right[1])

        dot_line.draw(window, 70, 0)

        ball.draw(window)
        paddle_left.draw(window)
        paddle_right.draw(window)

        if ball.ball_y >= paddle_right.paddle_y and \
                ball.ball_y <= (paddle_right.paddle_y + paddle_right.paddle_height):
            if ball.ball_x >= (paddle_right.paddle_x - ball.ball_r):
                ball.flip_x = True
                bounce.play()
                paddle_count += 1

        if ball.ball_y >= paddle_left.paddle_y and \
                ball.ball_y <= (paddle_left.paddle_y + paddle_left.paddle_height):
            if ball.ball_x <= (paddle_left.paddle_x + paddle_left.paddle_width + ball.ball_r):
                ball.flip_x = False
                bounce.play()
                paddle_count += 1

        if ball.ball_x >= screen_width - ball.ball_r:
            paddle_left.score += 1
            ball.reset(screen_width // 2, screen_height // 2)

        if ball.ball_y >= screen_height - ball.ball_r:
            ball.flip_y = True

        if ball.ball_x <= ball.ball_r:
            paddle_right.score += 1
            ball.reset(screen_width // 2, screen_height // 2)

        if ball.ball_y <= ball.ball_r:
            ball.flip_y = False

        ball.move_x()
        ball.move_y()

        if paddle_left.score >= 5 or paddle_right.score >= 5:
            paddle_left.score_update(ball, 2, 2, 2)
            paddle_right.score_update(ball, 2, 2, 2)

        if paddle_left.score >= 10 or paddle_right.score >= 10:
            paddle_left.score_update(ball, 3, 3, 3)
            paddle_right.score_update(ball, 3, 3, 3)

        if paddle_left.score >= 15 or paddle_right.score >= 15:
            paddle_left.score_update(ball, 4, 4, 4)
            paddle_right.score_update(ball, 4, 4, 4)

        if paddle_left.score >= 30 or paddle_right.score >= 30:
            paddle_left.score_update(ball, 5, 5, 5)
            paddle_right.score_update(ball, 5, 5, 5)

        if paddle_count == 10:
            paddle_left.score_update(ball, 2, 2, 2)
            paddle_right.score_update(ball, 2, 2, 2)

        pygame.display.update()

        if not start:
            pygame.time.wait(2000)
            start = True

        clock.tick(game_speed)

    pygame.quit()


def game_engine(caps, i, width, height, game_speed):
    """
    The game base configuration.
    """

    pygame.init()
    pygame.display.set_caption(caps.upper())
    icon = pygame.image.load(i)
    pygame.display.set_icon(icon)
    game_loop(width, height, game_speed)


if __name__ == '__main__':
    game_engine(c.CAPTIONS, c.ICON, c.WIDTH, c.HEIGHT, c.GAME_SPEED)



