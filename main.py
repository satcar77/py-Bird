#!/usr/bin/env python
import pygame as pg
import os,sys,random
SCREEN_SIZE = (432, 730)
BACKGROUND_COLOR = (50, 50, 50)
PIPE_GAP=150

class Background(object):
    def __init__(self):
        self.frameindex=[(0,0)]
        self.zoom_index=3
        self.size=(144*self.zoom_index,256*self.zoom_index)
        self.rect=pg.Rect((0,0),self.size)
        self.frame=split(SPRITE_SHEET,(144,256),self.frameindex,self.size)
    def draw(self,surface):
        surface.blit(self.frame[0],self.rect)

class UpObstacle(pg.sprite.Sprite):
    def __init__(self,height,xposition=432):
        pg.sprite.Sprite.__init__(self)
        self.zoom_index=3
        self.size=(26*self.zoom_index,121*self.zoom_index)
        self.vari=self.size[0]
        self.rect=pg.Rect((xposition,height-self.size[1]),self.size)
        self.frameindex=[(303,0)]
        self.framelist=split(SPRITE_SHEET,(26,121),self.frameindex,self.size)
    def draw(self,surface):
        surface.blit(self.framelist[0],self.rect)
    def animate(self):
        self.rect.x-=2
class DObstacle(pg.sprite.Sprite):
    def __init__(self,height,xposition=432):
        pg.sprite.Sprite.__init__(self)
        self.zoom_index=3
        self.size=(26*self.zoom_index,121*self.zoom_index)
        self.vari=self.size[0]
        self.rect=pg.Rect((xposition,height),self.size)
        self.frameindex=[(330,0)]
        self.framelist=split(SPRITE_SHEET,(26,121),self.frameindex,self.size)
    def draw(self,surface):
        surface.blit(self.framelist[0],self.rect)
    def animate(self):
        self.rect.x-=2

class Score_obs(object):
    def __init__(self,height,xposition=432+30):
        self.size=(1,PIPE_GAP)
        self.rect=pg.Rect((xposition,height),self.size)
    def draw(self,surface):
        surface.fill(pg.Color("red"),self.rect)
    def animate(self):
        self.rect.x-=2
class _Physics(object):
    def __init__(self):
        """You can experiment with different gravity here."""
        self.x_vel = self.y_vel = 0
        self.grav = 0.15
        self.fall = True
        self.angle_vel=0
        self.grav_angle=0.09
        self.start=1
    def physics_update(self):
        """update the velocity according to the gravity"""
        if self.start:
            self.y_vel=0
            self.angle_vel=0
        elif self.fall:
            self.y_vel += self.grav
            self.angle_vel-=self.grav_angle
        
        else:
            self.y_vel=0
            
def atOver(surface,score,hi_score):
    zoom=3
    gameover_index=[(145,198)]
    board_index=[(146,58)]
    gameover_size=(95*zoom,21*zoom)
    board_size=(113*zoom,58*zoom)
    start_size=(40*zoom,14*zoom)
    start_index=[(242,213)]
    gameover=split(SPRITE_SHEET,(95,21),gameover_index,gameover_size)[0]
    board=split(SPRITE_SHEET,(113,58),board_index,board_size)[0]
    start=split(SPRITE_SHEET,(40,14),start_index,start_size)[0]          
    surface.blit(gameover,pg.Rect((100-10,100),gameover_size))
    surface.blit(board,pg.Rect((100-50,200),board_size))
    surface.blit(start,pg.Rect((100+50,400),start_size))        
    make_text(surface,(280,250),score)
    make_text(surface,(280,320),hi_score)
class Bird(_Physics,pg.sprite.Sprite):
    def __init__(self):
        _Physics.__init__(self)
        pg.sprite.Sprite.__init__(self)
        self.power=-4.0
        self.zoom_index=3
        self.size=(17*self.zoom_index,12*self.zoom_index)
        self.rect=pg.Rect((150,SCREEN_SIZE[1]/2-100),self.size)
        self.frameindex=[(223,124),(264,90),(264,64)]
        self.frames=split(SPRITE_SHEET,(17,12),self.frameindex,self.size)
        self.image=None
        self.animation_index=0
        self.anim_timer=pg.time.get_ticks()
        self.over=False
        self.angle=0
        self.touchdown=False
        self.score=0
        self.start=1
        self.hi_score=0
    def jump(self):
        if not self.over:
            self.y_vel=self.power
            self.angle_vel=4
        self.start=0

    def atStart(self,surface):
        tap=[(171,122)]
        tap_size=(40,49)
        tap_display_size=(tap_size[0]*3,tap_size[1]*3)
        tap_rect=pg.Rect((0,0),tap_display_size)
        image=split(SPRITE_SHEET,tap_size,tap,tap_display_size)
        tap_rect.centerx=SCREEN_SIZE[0]/2+50
        tap_rect.centery=SCREEN_SIZE[1]/2-70
        surface.blit(image[0],tap_rect)
    def check_collisions(self, index, surface_obs,pipe,score_obs):
        """
        This function checks for the collision with pipe,ground and score rectangle. 
whenever player hits the score rectangle, the score increments by 1
        """
        unaltered = True
        while pg.sprite.collide_rect(self, surface_obs):
            self.rect[index] -= 1
            unaltered = False
            self.over=True
            self.fall=False
            self.touchdown=True
        if pg.sprite.spritecollideany(self, pipe):
            
            unaltered = False
            self.over=True
        if pg.sprite.spritecollideany(self,score_obs):
            score_obs.remove(pg.sprite.spritecollideany(self,score_obs))
            self.score+=1
        return unaltered


    def update(self,obstacles,pipes,surface_obs):
        if not self.touchdown:
            self.animate()
        self.check_collisions(1,obstacles,pipes,surface_obs)
        self.physics_update()
        self.rect.y+=self.y_vel
        self.angle+=self.angle_vel    
    def draw(self,screen):
        screen.blit(self.image,self.rect)
        if self.touchdown:
            atOver(screen,self.score,self.hi_score)
            if self.score>self.hi_score:
                self.hi_score=self.score
        if self.start:
            self.atStart(screen)
    def animate(self):
        now=pg.time.get_ticks()
        self.image=self.frames[self.animation_index]
        if (now-self.anim_timer)>100:
            self.animation_index=self.animation_index+1
            self.anim_timer=now
        if self.animation_index>=len(self.frames):
            self.animation_index=0
        self.image=pg.transform.rotate(self.image,self.angle)
        if self.angle>30:
            self.angle=30
        elif self.angle<-90:
            self.angle=-90
    def score(self):
        return self.score
    def check_over(self):
        return self.over
def make_text(screen,where,score=0):
    numbers_index=[(369,0),(0,0),(41,0),(82,0),(123,0),(164,0),(205,0),(246,0),(287,0),(328,0)]
    num_size=(41,62)
    num_size_displayed=(num_size[0]/2,num_size[1]/2)
    numbers=split(NUM_SHEET,num_size,numbers_index,num_size_displayed)
    place =2
    temp=score
    surface=pg.Surface((num_size_displayed[0]*3,num_size_displayed[1]),pg.SRCALPHA, 32)
    if temp==0:
        surface.blit(numbers[0],pg.Rect((num_size_displayed[0]*2,0),num_size_displayed))
    while temp!=0:
        digit=temp%10
        surface.blit(numbers[digit],pg.Rect((num_size_displayed[0]*place,0),num_size_displayed))
        place=place-1
        temp/=10
    screen.blit(surface,pg.Rect(where,num_size_displayed))

class Control(object):
    """event loop and game states."""
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.clock = pg.time.Clock()
        self.fps = 70.0
        self.keys = pg.key.get_pressed()
        self.done = False
        self.player = Bird()
        self.surface=Surface()
        self.background=Background()
        self.obstacles=[]
        self.tick=pg.time.get_ticks()
        self.score=0
        self.scoreobs=[]
        self.restart_rect=pg.Rect((100+50,400),(40*3,14*3))
    def random_obs(self):
        yposition=random.randint(90,350)
        obs=UpObstacle(yposition)
        obs1=DObstacle(PIPE_GAP+yposition)
        self.scoreobs.append(Score_obs(yposition))
        return obs,obs1
    def restart(self):
        hi_score=self.player.hi_score
        self.__init__()
        self.player.hi_score=hi_score

    def auto_spawn(self):
        now=pg.time.get_ticks()
        if (now-self.tick)/1000>1:
            for i in self.random_obs():
                self.obstacles.append(i)

            self.tick=now
    def event_loop(self):
        
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                pg.quit()
                sys.exit()
            elif pg.mouse.get_pressed()[0]:
               
                self.player.jump()

            if self.done:
                pos = pg.mouse.get_pos()
                if pg.mouse.get_pressed()[0] and self.restart_rect.collidepoint(pos):
                    self.restart()
    def check_done(self):
        self.done=self.player.check_over()
    def draw(self):
        self.background.draw(self.screen)
        
        for obs in self.obstacles:
            obs.draw(self.screen)
       
        self.surface.draw(self.screen)
        
        self.player.draw(self.screen)
        make_text(self.screen,(SCREEN_SIZE[0]/2-40,50),self.score)

    def main_loop(self):
        """As simple as that"""
        while 1:
            self.player.update(self.surface,self.obstacles,self.scoreobs)
            if not self.player.start:
                self.auto_spawn()
            self.draw()
            if not self.done:
                for obs in self.obstacles:
                    obs.animate()
                self.surface.animate()
                for obs in self.scoreobs:
                    obs.animate()
            self.event_loop()
            self.check_done()
            self.score=self.player.score
            pg.display.update()
            self.clock.tick(self.fps)
            
class Surface(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.zoom_index=3
        self.size=(154*self.zoom_index,45*self.zoom_index)
        self.vari=self.size[0]
        self.rect=pg.Rect((0,SCREEN_SIZE[1]-self.size[1]),self.size)
        self.rect1=pg.Rect((0,SCREEN_SIZE[1]-self.size[1]),self.size)
        self.rect2=pg.Rect((0,SCREEN_SIZE[1]-self.size[1]),self.size)
        self.frameindex=[(146,0)]
        self.frame=split(SPRITE_SHEET,(154,56),self.frameindex,self.size)
    def draw(self,surface):
        
        self.rect1.x=self.vari
        self.rect2.x=self.vari-self.size[0]
        surface.blit(self.frame[0],self.rect1)
        surface.blit(self.frame[0],self.rect2)
        
    def animate(self):
        self.vari-=2
        if self.vari<=0:
            self.vari=self.size[0]

def split(sheet, size, frames,en_size):

    subsurfaces = []
    for fr in frames:
        rect = pg.Rect((fr[0],fr[1]), size)
        subsurfaces.append(pg.transform.scale(sheet.subsurface(rect),en_size))
    return subsurfaces

if __name__ == "__main__":
    global SPRITE_SHEET,NUM_SHEET
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption("PY BIRD")
    pg.display.set_mode(SCREEN_SIZE)
    SPRITE_SHEET=pg.image.load("sprite.png").convert_alpha()
    NUM_SHEET=pg.image.load("numbers.png").convert_alpha()
    run_it = Control()
    run_it.main_loop()
    pg.quit()
    sys.exit() 
            
    
