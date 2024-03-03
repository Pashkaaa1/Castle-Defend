import pygame
import math
import random


pygame.init()
#вікно гри
screen_width = 800
screen_height =600

#створюэмо вікно гри
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Castle Defend")


clock = pygame.time.Clock()
fps=60

#встановлюємо картинки
bg=pygame.transform.scale(pygame.image.load("../castle/bg.jpg"), (screen_width, screen_height)).convert_alpha()
castle_img=pygame.image.load("../castle/castle.png").convert_alpha()
bullet_img=pygame.image.load("../castle/bullet.png").convert_alpha()
b_w=bullet_img.get_width()
b_h=bullet_img.get_height()
bullet_img=pygame.transform.scale(bullet_img,(int(b_w*0.04),int(b_h*0.04)))



#клас замку
class Castle():
    def __init__(self,img100,x,y,scale):
        self.health=1000
        self.max_health=self.health
        self.fired=False
        width=img100.get_width()
        height=img100.get_height()

        self.img100=pygame.transform.scale(img100,(int(width*scale),(int(height*scale))))
        self.rect=self.img100.get_rect()
        self.rect.x=x
        self.rect.y=y

    def shoot(self):
        pos=pygame.mouse.get_pos()
        x_dist=pos[0]-self.rect.midleft[0]
        y_dist = -(pos[1] - self.rect.midleft[1])
        self.angle=math.degrees(math.atan2(y_dist,x_dist))

        if pygame.mouse.get_pressed()[0] and self.fired==False:
            self.fired=True
            bullet=Bullet(bullet_img,630,380,self.angle)
            bullet_group.add(bullet)
        if pygame.mouse.get_pressed()[0]==False:
            self.fired = False


    def draw(self):
        self.image=self.img100

        screen.blit(self.image,self.rect)
class Bullet(pygame.sprite.Sprite):
    def __init__(self,image,x,y,angle):
        pygame.sprite.Sprite.__init__(self)
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.angle=math.radians(angle)
        self.speed=10
        self.dx= math.cos(self.angle)*self.speed
        self.dy= -(math.sin(self.angle)*self.speed)

    def update(self):
        if self.rect.right<0 or self.rect.left>screen_width or self.rect.bottom<0 or self.rect.top>screen_height:
            self.kill()
        self.rect.x += self.dx
        self.rect.y +=self.dy

castle=Castle(castle_img,500,180,0.3)

bullet_group=pygame.sprite.Group()
 #цикл
run=True
while run:

    clock.tick(fps)


    screen.blit(bg,(0,0))

    # відмальовуємо замок
    castle.draw()
    castle.shoot()

    bullet_group.update()
    bullet_group.draw(screen)
    #вихід з гри
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

    pygame.display.update()

pygame.quit()