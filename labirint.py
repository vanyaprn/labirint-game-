from pygame import*

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed 
   
    def update(self):
        if pacman.rect.x <= win_w - 80 and pacman.x_speed > 0 or pacman.rect.x >= 0 and pacman.x_speed < 0:
            self.rect.x +=  self.x_speed
        platforms = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: 
            for p in platforms:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms:
                self.rect.left = max(self.rect.left, p.rect.right)
        
        if pacman.rect.y <= win_h - 80 and pacman.y_speed > 0 or pacman.rect.y >= 0 and pacman.y_speed <0:        
            self.rect.y += self.y_speed
        platforms = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms:
                self.rect.top = max(self.rect.top, p.rect.bottom)        

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    side = 'left'
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        if self.rect.x >= win_w - 85:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        self.rect.x += self.speed 
        if self.rect.x > win_w + 10:
            self.kill()

win_w = 700
win_h = 700
window = display.set_mode((win_h, win_w))
display.set_caption('Лабиринт')
back  = (119, 210, 223)

black = (0, 0, 0)

barriers = sprite.Group()

bullets = sprite.Group()

monsters = sprite.Group()

w1 = GameSprite('wall.png', win_w/2 - win_w/3, win_h/2, 300, 50)
w2 = GameSprite('wall.png', 370, 100, 50, 400)
barriers.add(w1)
barriers.add(w2)

pacman = Player('pacman.png', 5, win_h - 80, 80, 80, 0, 0)
award = GameSprite('award.png', win_w - 85, win_h - 100, 80, 80)

monster_1 = GameSprite('enemy.png', win_w - 80, 150, 80, 80)
monster_2 = GameSprite('monster.png', win_w - 80, 230, 80, 80)
monsters.add(monster_1)
monsters.add(monster_2)



finish = False

run = True
while run:
    time.delay(50)
    for even in event.get():
        if even.type == QUIT:
            run = False
        elif even.type == KEYDOWN:
            if even.key == K_LEFT:
                pacman.x_speed = -5
            elif even.key == K_RIGHT:
                pacman.x_speed = 5
            elif even.key == K_UP:
                pacman.y_speed = -5
            elif even.key == K_DOWN:
                pacman.y_speed = 5
            elif even.key == K_SPACE:
                pacman.fire()
        
        elif even.type == KEYUP:
            if even.key == K_LEFT:
                pacman.x_speed = 0
            elif even.key == K_RIGHT:
                pacman.x_speed = 0
            elif even.key == K_UP:
                pacman.y_speed = 0
            elif even.key == K_DOWN:
                pacman.y_speed = 0
    if not finish:
        
        window.fill(back)
        pacman.update()
        bullets.update()
        barriers.draw(window)
        bullets.draw(window)
        
        award.reset()
        pacman.reset()
        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)
        
        if sprite.spritecollide(pacman, monsters, False):
            finish = True
            img = image.load('lose.jpg')
            dis = img.get_width() // img.get_height()
            window.fill(black)
            window.blit(transform.scale(img, (win_h * dis, win_h)), (0, 0)) 
        if sprite.collide_rect(pacman, award):
            finish = True
            img = image.load('win.jpg')
            window.fill(black)
            window.blit(transform.scale(img, (win_w, win_h)), (0, 0))
    
    display.update()
