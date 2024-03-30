import pygame
import math
import random
import os
import sys

pygame.init()
#вікно гри
screen_width = 800
screen_height =600

#створюэмо вікно гри
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Castle Defend")


clock = pygame.time.Clock()
fps=60

level=1
high_score=0
level_difficulty=0
target_difficulty=1000
DIFFICULTY_MULTIPLIER=1.1
game_over=False
next_level=False
ENEMY_TIMER=1000
last_enemy=pygame.time.get_ticks()
enemies_alive=0
if os.path.exists("score.txt"):
    with open("score.txt","r") as file:
        high_score=int(file.read())




GREY=(100,100,100)

font=pygame.font.SysFont("Future",30)
font_60=pygame.font.SysFont("Future",50)

#встановлюємо картинки
bg=pygame.transform.scale(pygame.image.load("bg.jpg"), (screen_width, screen_height)).convert_alpha()
castle_img=pygame.image.load("castle.png").convert_alpha()
bullet_img=pygame.image.load("bullet.png").convert_alpha()
b_w=bullet_img.get_width()
b_h=bullet_img.get_height()
bullet_img=pygame.transform.scale(bullet_img,(int(b_w*0.04),int(b_h*0.04)))
enemy_animations=[]
enemy_types = ["woman","boy"]
enemy_health = [75,100]



animations_types=['walk','attack','death']
for enemy in enemy_types:
    animation_list=[]
    for animation in animations_types:
        temp_list=[]
        num_of_frames=6
        for i in range(num_of_frames):
            img=pygame.image.load(f'enemyes/{enemy}/{animation}/{i}.png').convert_alpha()
            e_w=img.get_width()
            e_h=img.get_height()
            img=pygame.transform.scale(img,(int(e_w*0.9),int(e_h*0.9)))
            temp_list.append(img)
        animation_list.append(temp_list)
    enemy_animations.append(animation_list)


repair_img=pygame.image.load("repair.png").convert_alpha()
armour_img=pygame.image.load("armour.png").convert_alpha()

def draw_text(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    screen.blit(img,(x,y))

def show_info():
    draw_text("Money: "+str(castle.money),font,GREY,10,10)
    draw_text("Score: " + str(castle.score), font, GREY, 180, 10)
    draw_text("High Score: " + str(high_score), font, GREY, 180, 30)
    draw_text("Level: " + str(level), font, GREY, screen_width//2, 10)
    draw_text("Health: " + str(castle.health)+"/"+str(castle.max_health), font, GREY, screen_width - 230,screen_height-50)
    draw_text("1000 ",font,GREY,screen_width-210,70)
    draw_text("500 ", font, GREY, screen_width -70,70)

#клас замку
class Castle():
    def __init__(self,img100,x,y,scale):
        self.health=1000
        self.max_health=self.health
        self.fired=False
        self.money=0
        self.score=0



        width=img100.get_width()
        height=img100.get_height()

        self.img100=pygame.transform.scale(img100,(int(width*scale),(int(height*scale))))
        self.rect=self.img100.get_rect()
        self.rect.x=x+20
        self.rect.y=y

    def shoot(self):
        pos=pygame.mouse.get_pos()
        x_dist=pos[1]-1000
        y_dist = -(pos[1] - self.rect.midleft[1])
        self.angle=math.degrees(math.atan2(y_dist,x_dist))

        if pygame.mouse.get_pressed()[0] and self.fired==False and pos[1]>70:
            self.fired=True
            bullet=Bullet(bullet_img,630,380,self.angle)
            bullet_group.add(bullet)
        if pygame.mouse.get_pressed()[0]==False:
            self.fired = False


    def draw(self):
        self.image=self.img100

        screen.blit(self.image,self.rect)


    def repair(self):
        if self.money>=1000 and self.health<self.max_health:
            self.health+=500
            self.money-=1000
            if castle.health>castle.max_health:
                castle.health=castle.max_health
    def armour(self):
        if self.money>=500:
            self.max_health+=250
            self.health+=250
            self.money-=500



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

class Enemy(pygame.sprite.Sprite):
    def __init__(self,health,animation_list,x,y,speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive=True
        self.speed=speed
        self.health=health
        self.last_attack=pygame.time.get_ticks()
        self.attack_cooldown=2000
        self.animation_list=animation_list
        self.frame_index=0
        self.action=0
        self.uptade_time=pygame.time.get_ticks()

        self.image=self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, 35, 55)
        self.rect.center=(x,y)


    def update(self,surface,target,bullet_group):
        if self.alive:
            if pygame.sprite.spritecollide(self,bullet_group,True):
                self.health-=25


            if self.rect.right > target.rect.left:
                self.uptade_action(1)

            if self.action==0:
                self.rect.x +=self.speed

            if self.action==1:
                if pygame.time.get_ticks()-self.last_attack>self.attack_cooldown:
                    target.health-=25
                    if target.health<0:
                        target.health=0

                    self.last_attack=pygame.time.get_ticks()


            if self.health<=0:
                target.money+=50
                target.score+=100
                self.action=2
                self.alive=False

        self.update_animation()


        surface.blit(self.image, (self.rect.x - 10, self.rect.y - 15))
    def update_animation(self):
        ANIMATION_COULDOWN=250
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks()-self.uptade_time > ANIMATION_COULDOWN:
            self.uptade_time=pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action==2:
              self.frame_index=len(self.animation_list[self.action])-1
            else:
                self.frame_index=0

    def uptade_action(self,new_action):
        if new_action!= self.action:
            self.action=new_action
            self.frame_index=0
            self.uptade_date=pygame.time.get_ticks()


class Button():
    def __init__(self,x,y,image,scale):
        width=image.get_width()
        height=image.get_height()
        self.image=pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.clicked=False

    def draw(self,surface):
        action=False
        pos=pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                self.clicked=True
                action=True
        if pygame.mouse.get_pressed()[0]==0:
            self.clicked=False

        surface.blit(self.image,(self.rect.x,self.rect.y))

        return action
class Crosshair():
    def __init__(self,scale):
        image=pygame.image.load("crosshair.png").convert_alpha()
        width=image.get_width()
        height=image.get_height()

        self.image=pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.rect=self.image.get_rect()

        pygame.mouse.set_visible(False)
    def draw(self):
        mx,my=pygame.mouse.get_pos()
        self.rect.center=(mx,my)
        screen.blit(self.image,self.rect)

castle=Castle(castle_img,500,180,0.4)

crosshair=Crosshair(0.45)


repair_button=Button(screen_width-220,10,repair_img,0.2)
armour_button=Button(screen_width-75,10,armour_img,0.1)


bullet_group=pygame.sprite.Group()
enemy_group=pygame.sprite.Group()



#цикл
run=True
while run:

    clock.tick(fps)

    if game_over==False:



        screen.blit(bg,(0,0))

        # відмальовуємо замок
        castle.draw()
        castle.shoot()

        crosshair.draw()

        bullet_group.update()
        bullet_group.draw(screen)

        enemy_group.update(screen,castle,bullet_group)

        show_info()




        if repair_button.draw(screen):
            castle.repair()
        if armour_button.draw(screen):
            castle.armour()


        if level_difficulty<target_difficulty:
            if pygame.time.get_ticks()-last_enemy>ENEMY_TIMER:
                e=random.randint(0,len(enemy_types)-1)
                enemy = Enemy(enemy_health[e], enemy_animations[e], -10, screen_height - 120, 1)
                enemy_group.add(enemy)
                last_enemy=pygame.time.get_ticks()
                level_difficulty+=enemy_health[e]


        if level_difficulty>=target_difficulty:
            enemies_alive=0
            for e in enemy_group:
                if e.alive==True:
                    enemies_alive+=1
            if enemies_alive==0 and next_level==False:
                next_level=True
                level_reset_time=pygame.time.get_ticks()

        if next_level==True:
            draw_text("LEVEL COMPLETE!",font_60,(223,99,111),230,100)

            if castle.score > high_score:
                high_score=castle.score
                with open("score.txt","w") as file:
                    file.write(str(high_score))
            if pygame.time.get_ticks()-level_reset_time>1500:
                next_level=False
                level+=1
                last_enemy=pygame.time.get_ticks()
                target_difficulty *= DIFFICULTY_MULTIPLIER
                level_difficulty=0
                enemy_group.empty()
        if castle.health<=0:
            game_over=True
    else:
        draw_text("GAME OVER!",font,(223,99,111),300,300 )
        draw_text('PRESS "A"TO PLAY AGAIN!', font,(223,99,111), 250, 360)
        pygame.mouse.set_visible(True)
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            game_over=False
            level = 1
            target_difficulty=1000
            level_difficulty=0
            last_enemy=pygame.time.get_ticks()
            enemy_group.empty()
            castle.score=0
            castle.health=1000
            castle.max_health=castle.health
            castle.money=0
            pygame.mouse.set_visible(False)


        #вихід з гри
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
            sys.exit()
    pygame.display.update()

pygame.quit()