from random import *
from time import *
import pygame

pygame.init()
W = 500
H = 500
win = pygame.display.set_mode((W,H))
S = (176, 199, 247)
WHITE = (255, 255, 255)
LIGB = (123, 200, 246)
BLACK = (0, 0, 0)
YEL = (255, 255, 0)
RED = (255, 0, 0)
BG = (222, 122, 52)
BLUE = (0, 0, 255)
vremya = pygame.time.Clock()

class Game():
    finish = False
    run = True
    current_level = 0
    win = False
    events = list()
    keys_pressed = {}
    enemy_spisok = []
    start_x = 10
    start_y = 10

    def create_monsters(self, cislo_ryadov = 3, cislo_monstrov = 9):
        self.enemy_spisok.clear()
        for i in range(cislo_ryadov):
            for z in range(cislo_monstrov):
                enemy = Picture('monstr2.png', x = self.start_x + 55*z+25*i, y = self.start_y + 55*i)
                self.enemy_spisok.append(enemy)
            cislo_monstrov -= 1
        
    def update(self):
        self.events = pygame.event.get()
        self.keys_pressed = pygame.key.get_pressed()

    def viplunul(self):
        pass 
        #TODO: сделать монстра который выплевывает мячик

    def otcet(self):
        cifri = Label('3', 0, 0, 500, 500, 250, 250, None, RED, 1, 50)
        for i in range(3, 0, -1):
            win.blit(bg_image, (0, 0))
            cifri.set_text(str(i))
            cifri.draw()
            pygame.display.update()
            sleep(0.9)
            

class Area():
    def __init__(self,x = 0,y = 0,w = 20,h = 10,cvet_bg = BG):
        self.rect = pygame.Rect(x,y,w,h)
        self.cvet_bg = cvet_bg
    def collidepoint(self,x, y):
        return self.rect.collidepoint(x,y)
    def colliderect(self, rect):
        return self.rect.colliderect(rect)


class Label(Area):
    def __init__(self, text = '', x = 0, y = 0, w = 20, h = 10, sh_x = 2, sh_y = 5, cvet_bg = None, cvet_text = BLACK, bordur = 0, fsize = 20):
        super().__init__(x=x, y=y,w=w,h=h, cvet_bg = cvet_bg)
        self.text = text
        self.sh_x = sh_x
        self.sh_y = sh_y
        self.bordur = bordur
        self.fsize = fsize
        self.cvet_text = cvet_text
        self.set_text(text, cvet_text = cvet_text)
    def set_text(self, text, fsize = None, cvet_text = None):
        if cvet_text is None:
            cvet_text = self.cvet_text
        if fsize is None:
            fsize = self.fsize
        self.image = pygame.font.Font(None, fsize).render(text, True, cvet_text)
    def draw(self, sh_x = None, sh_y = None):
        if sh_x is None:
            sh_x = self.sh_x
        if sh_y is None:
            sh_y = self.sh_y
        if not self.cvet_bg is None:
            pygame.draw.rect(win,self.cvet_bg, self.rect)
        win.blit(self.image,(self.rect.x + sh_x, self.rect.y + sh_y))
        if self.bordur >= 0:
            self.draw_bordur(WHITE)
    def draw_bordur(self, color):
        pygame.draw.rect(win, color, self.rect, self.bordur)

class Baton(Label):
    func = None

    def update(self):
        for event in game.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if self.rect.collidepoint(*pos):
                    if not self.func is None:
                        self.func()

    def onclick(self, func):
        self.func = func
class Picture(Area):
    def __init__(self, file_name, x, y, w = 60, h = 50):
        super().__init__(x=x, y=y,w=w,h=h)
        self.image = pygame.image.load(file_name)
    def draw(self):
        win.blit(self.image,(self.rect.x, self.rect.y))


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, speed, w_s, h_s):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(filename), (w_s, h_s))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w_s = w_s
        self.h_s = h_s
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Brevno(GameSprite):
    def update(self):
        keys_pressed = game.keys_pressed
        if keys_pressed[pygame.K_RIGHT] and self.rect.x < W - self.rect.width:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
            
game = Game()

def poshalka():
    print('poshalochka')

def finish_False():
    game.finish = False
    game.create_monsters()
    ball.draw()
    brevno.update()
    brevno.reset()
    game.otcet()


knopka = Baton('lalalalal', x = 160, y = 350, w = 150, h = 50, sh_x = 17, sh_y = 10, cvet_bg = None, cvet_text = WHITE, bordur = 3, fsize = 40)
knopka.onclick(poshalka)

knopka_restart = Baton('СНАЧАЛА', 160, 425, 150, 50, 10, 10, None, WHITE, 3, 40)
knopka_restart.onclick(finish_False)

pobeda = GameSprite('victory.png', 50, 50, 0, 400, 200)
qaz = Picture('game_over.jpg', 0, 50)

game.create_monsters()

bg_image = pygame.image.load('volshebnyj_les.jpg')
ball = Picture('myach2.png', 200, 300)        
ball.draw()
brevno = Brevno('brevno.png', 200, 450, 5, 111, 25)        
brevno.reset()
speed = 5
dx = 1
dy = 1
total = 0
move_right = False
move_left = False

FPS = 60 

game.otcet()
    
while game.run == True:

    game.update()

    for event in game.events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
    if ball.colliderect(brevno.rect):
        dy *= -1
    for m in game.enemy_spisok:
        if m.colliderect(ball.rect):
            dy *= -1
            game.enemy_spisok.remove(m)
            break
    win.blit(bg_image, (0, 0))

    if not game.finish:
        ball.rect.x += speed * dx
        if ball.rect.x >= 450 or ball.rect.x <= 0:
            dx *= -1
        ball.rect.y += speed * dy
        if ball.rect.y >= 500 or ball.rect.y <= 0:
            dy *= -1
        ball.draw()

        brevno.update()
        brevno.reset()
        for m in game.enemy_spisok:
            m.draw()
        
        if ball.rect.y >= 500:
            pygame.display.update()
            game.finish = True

        elif len(game.enemy_spisok) <= 0:
            game.win = True
            pygame.display.update()
            game.finish = True
    else:
        if game.win:
            pobeda.reset()
        else:
            win.fill((0, 0, 0))
            qaz.draw()

            knopka.update()
            knopka.draw()

            knopka_restart.update()
            knopka_restart.draw()

    pygame.display.update()
    vremya.tick(FPS)
#сделать кнопки