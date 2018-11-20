import pyglet
import random
from math import sin, cos, radians, pi
from pyglet.window.key import DOWN, UP, LEFT, RIGHT

window = pyglet.window.Window(1000, 800)
batch = pyglet.graphics.Batch()   # pro optimalizované vyreslování objektů


class Stone(object):

    def __init__(self,x=None, y=None,direction=None,speed=None, rspeed=None):
        # nečtu obrázek
        num = random.choice(range(0, 20))
        self.image = pyglet.image.load('meteors/{}.png'.format(num))
        
        # střed otáčení dám na střed obrázku
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2
        # z obrázku vytvořím sprite
        self.sprite = pyglet.sprite.Sprite(self.image, batch=batch)

        # pokud není atribut zadán vytvořím ho náhodně
        self.x = x if x is not None else random.randint(0, window.width)
        self.y = y if y is not None else random.randint(0, window.height)
        # musím správně nastavit polohu sprite
        self.sprite.x = self.x
        self.sprite.y = self.y

        self.direction = direction if direction is not None else random.randint(0, 359)
        # rychlost pohybu
        self.speed = speed if speed is not None else random.randint(30, 180)
        # rychlost otáčení
        self.rspeed = rspeed if rspeed is not None else random.randint(-2, 5)

    def tick(self, dt):
        self.bounce()

        # do promenne dt se uloží doba od posledního tiknutí
        self.x += dt * self.speed * cos(pi / 2 - radians(self.direction))
        self.sprite.x = self.x
        self.y += dt * self.speed * sin(pi / 2 - radians(self.direction))
        self.sprite.y = self.y
        self.sprite.rotation +=self.rspeed

    def bounce(self):

        # vzdálenost okraje a středu
        rozmer = min(self.image.width, self.image.height)/2

        if self.x + rozmer >= window.width:
            self.direction = random.randint(190, 350)
            return
        if self.x - rozmer <= 0:
            self.direction = random.randint(10, 170)
            return
        if self.y + rozmer >= window.height:
            self.direction = random.randint(100, 260)
            return
        if self.y - rozmer <= 0:
            self.direction = random.randint(-80, 80)
            return



class Lodka(object):
    
    def __init__(self):
        #vybereme obrázku lodě
        self.obrazek = pyglet.image.load("playerShip1_green.png")
        
        #střed otáčení toho obrázku umístíme do prostřed
        self.obrazek.anchor_x = self.obrazek.width // 2
        self.obrazek.anchor_y = self.obrazek.height // 2
        
        #z obrázku uděláme sprite
        self.sprite =pyglet.sprite.Sprite(self.obrazek, batch=batch)
        
        self.sprite.rotation=60
        self.speed= 200
        self.x=500
        self.y=400
        self.sprite.x = self.x
        self.sprite.y = self.y
    def tiktak(self,t):
        global klavesy
        self.okraj()
        #ovládání lodičky
        for data in klavesy:
            if data == LEFT:
                self.sprite.rotation -= 5
            if data == RIGHT:
                self.sprite.rotation += 5
            if data == UP:
                self.x = self.sprite.x + self.speed*t*sin(pi*self.sprite.rotation/180)
                self.sprite.x=self.x
                self.y = self.sprite.y + self.speed*t*cos(pi*self.sprite.rotation/180)
                self.sprite.y=self.y
            if data == DOWN:
                self.x = self.sprite.x + self.speed*t*-sin(pi*self.sprite.rotation/180)
                self.sprite.x = self.x
                self.y = self.sprite.y + self.speed*t*-cos(pi*self.sprite.rotation/180)
                self.sprite.y = self.y
    
    def okraj(self):
        # vzdálenost okraje a středu
        rozmer = min(self.obrazek.width, self.obrazek.height)/2
        if self.x + rozmer >= window.width:
            self.speed=0
        if self.x - rozmer <= 0:
            self.speed=0
        if self.y + rozmer >= window.height:
            self.speed=0
        if self.y - rozmer <= 0:
            self.speed=0

            
                                                                 
     
        
        

klavesy=set()        
for o in range(1):
    lod=Lodka()
    pyglet.clock.schedule_interval(lod.tiktak, 1/ 30 )

stones = []
for i in range(5):
    stone = Stone()
    pyglet.clock.schedule_interval(stone.tick, 1 / 30)
    stones.append(stone)

#po zmáčknutí klávesy se zapíše do dat
@window.event
def on_key_press(data, mod):
    global klavesy
    klavesy.add(data)
    
#po spuštění klávesy se data vymažou
@window.event
def on_key_release(data, mod):
    global klavesy
    klavesy.remove(data)


@window.event
def on_draw():
    window.clear()
    batch.draw()


pyglet.app.run()