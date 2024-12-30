from pygame import *
from random import randint
win = display.set_mode((700,500))
background = transform.scale(image.load('galaxy.jpg'),(700,500))
mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()
clock = time.Clock()

class Game_sprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y, player_w, player_h):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_w, player_h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(Game_sprite):
    def update(self):
        keys_presed = key.get_pressed()
        if keys_presed[K_RIGHT] and self.rect.x < 500:
            self.rect.x += self.speed
        if keys_presed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bulling('bullet.png', -15, self.rect.centerx, self.rect.top, 15, 20)
        bullets.add(bullet)

lost = 0
class Enemy(Game_sprite):
    direction = 'left'
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(50,650)
            self.rect.y = 0
            lost += 1

class Bulling(Game_sprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
bullets = sprite.Group()

monsters = sprite.Group()

for i in range(5):
    monster = Enemy('ufo.png', 1, randint(50, 650), randint(1,5), 65, 50)
    monsters.add(monster)

raketa = Player('rocket.png', 10, 10, 350, 50, 150)

font.init()
text = font.SysFont('arial', 36)
result = font.SysFont('arial', 100)
score = 0

finish = False

run = True
while run :
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                raketa.fire()
    if not finish:
        win.blit(background,(0,0))
        score_text = text.render(f'счёт: {score}', True, (255,255,255))
        win.blit(score_text, (10,20))
        lost_text = text.render(f"пропущено: {lost}", True, (255,255,255))
        win.blit(lost_text, (10,60))
        raketa.reset()
        raketa.update()
        monsters.update()
        monsters.draw(win)
        bullets.update()
        bullets.draw(win)
        
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for i in collides:
            score+=1
            monster = Enemy('ufo.png', randint(1,3), randint(50, 650), randint(1,5), 65, 50)
            monsters.add(monster)
        if sprite.spritecollide(raketa, monsters, False) or lost >=3:
            finish = True
            lose = result.render('XAXAXAX', True, (255, 0, 0))
            win.blit(lose, (150,150))
        if score >= 5:
            finish = True 
            winner = result.render('gagner', True, (0,255, 0))
            win.blit(winner, (150,150))
        display.update()
        clock.tick(60)


