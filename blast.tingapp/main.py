import tingbot
from tingbot import *
from random import randint

# 320x240

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Entity:
    def __init__(self, pos, size, color):
        self.pos = pos
        self.size = size
        self.color = color
    
    def  draw(self):
        screen.rectangle(xy=(self.pos.x, self.pos.y), size=(self.size.width, self.size.height), color=self.color)

    def contains_pos(self, other_pos):
        half_width = self.size.width * 0.5
        half_height = self.size.height * 0.5
        return other_pos.x > self.pos.x  - half_width and \
                other_pos.x < self.pos.x + half_width and \
                other_pos.y > self.pos.y - half_height and \
                other_pos.y < self.pos.y + half_height

class Game:
    def __init__(self):
        self.left_touch_area = Entity(Pos(45, 195), Size(90, 90), 'none')
        self.right_touch_area = Entity(Pos(274, 195), Size(90, 90), 'none')
        
        self.player = Entity(Pos(160, 200), Size(30,30), (100,250,150))
        
        self.bullets = []
        for i in range(1, 6):
            bullet = Entity(Pos(160, i * 25), Size(5, 5), 'yellow')
            self.bullets.append(bullet)
        
        self.globe = Entity(Pos(100, 100), Size(1,1), 'blue')
        
        self.moving_left = False
        self.moving_right = False
        
        self.score = 0
        
        if 'high_score' in tingbot.app.settings:
            self.high_score = tingbot.app.settings['high_score']
        else:
            self.high_score = 0
        
game = Game()

@every(seconds=1.0/30)
def loop():
    screen.fill(color='black')
    
    # grow globe
    new_size = game.globe.size.width + 2
    game.globe.size.width =  new_size
    game.globe.size.height = new_size
    if new_size <= 50:
        game.globe.color = 'blue'
    else:
        game.globe.color = 'red'
    
    # move player
    if game.moving_left:
        game.player.pos.x = game.player.pos.x - 10

    if game.moving_right:
        game.player.pos.x = game.player.pos.x + 10
    
    # move bullets
    for bullet in game.bullets:
        bullet.pos.y = bullet.pos.y - 10
        if bullet.pos.y <= 0:
            bullet.pos.y += 175
            bullet.pos.x = game.player.pos.x
    
    # bullet collision
    for bullet in game.bullets:
        if game.globe.contains_pos(bullet.pos):
            game.score += 52 - game.globe.size.width
            if game.score < 0: game.score = 0
            if game.score > game.high_score:
                game.high_score = game.score
                tingbot.app.settings['high_score'] = game.high_score

            game.globe.size = Size(1, 1)
            game.globe.pos = Pos(randint(40,280), randint(40, 140))
        
    #draw globe
    game.globe.draw()
    
    # draw bulltes
    for bullet in game.bullets:
        bullet.draw()

    # draw player
    game.player.draw()
    
    # draw hud
    screen.text('Score {0}'.format(game.score), color='white', xy=(5,5), align='topleft', font_size=15)
    screen.text('High Score {0}'.format(game.high_score), color='white', xy=(315,5), align='topright', font_size=15)

@touch()
def on_touch(xy, action):
    if action == 'up':
        game.moving_right = False
        game.moving_left = False
        
    touch_pos = Pos(xy[0], xy[1])
    if action == 'down':
        if game.right_touch_area.contains_pos(touch_pos):
            game.moving_right = True
        if game.left_touch_area.contains_pos(touch_pos):
            game.moving_left = True

@right_button.down
def right_down():
    game.moving_right = True

@right_button.up
def right_up():
    game.moving_right = False
    
@left_button.down
def left_down():
    game.moving_left = True

@left_button.up
def left_up():
    game.moving_left = False
    
tingbot.run()
