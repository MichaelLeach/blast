import tingbot
from tingbot import *
from random import randint

# 320x240

class Game:
    def __init__(self):
        self.player_pos = (160, 200)
        self.left_touch_area = (0, 150, 90, 90)
        self.right_touch_area = (230, 150, 90, 90)
        self.bullets = [(160, 25), (160, 50), (160, 75), (160, 100), (160, 125), (160, 150), (160, 175)]
        self.globe = { 'size' : 1, 'pos' : (100, 100), 'color' : 'blue' }
        self.moving_left = False
        self.moving_right = False
        self.score = 0
        if 'high_score' in tingbot.app.settings:
            self.high_score = tingbot.app.settings['high_score']
        else:
            self.high_score = 0
        
game = Game()

def contains_pos(rect, pos):
    return pos[0] > rect[0] and pos[0] < rect[0] + rect[2] and pos[1] > rect[1] and pos[1] < rect[1] + rect[3]

def colides(rect_1, rect_2):
    return True


@every(seconds=1.0/30)
def loop():
    screen.fill(color='black')
    
    # grow globe
    game.globe['size'] = game.globe['size'] + 2
    if game.globe['size'] <= 50:
        game.globe['color'] = 'blue'
    else:
        game.globe['color'] = 'red'
    
    # move player
    if game.moving_left:
        game.player_pos = (game.player_pos[0] - 10, game.player_pos[1])

    if game.moving_right:
        game.player_pos = (game.player_pos[0] + 10, game.player_pos[1])
    
    # move bullets
    for i in range(0, len(game.bullets)):
        bullet = game.bullets[i]
        y = bullet[1] - 10
        x = bullet[0]
        if y <= 0:
            y += 175
            x = game.player_pos[0]
            
        game.bullets[i] = (x, y)
        
    
    # bullet collision
    for bullet in game.bullets:
        if contains_pos((game.globe['pos'][0] - game.globe['size'] * 0.5,
                         game.globe['pos'][1] - game.globe['size'] * 0.5, 
                         game.globe['size'], 
                         game.globe['size']), bullet):
            game.score += 52 - game.globe['size']
            if game.score < 0: game.score = 0
            if game.score > game.high_score:
                game.high_score = game.score
                tingbot.app.settings['high_score'] = game.high_score

            game.globe['size'] = 1
            game.globe['pos'] = (randint(40,280), randint(40, 140))
        
    #draw globe
    screen.rectangle(xy=game.globe['pos'], size=(game.globe['size'], game.globe['size']), color=game.globe['color'])

    # draw bulltes
    for bullet in game.bullets:
        screen.rectangle(xy=bullet, size=(5,5), color='yellow')

    # draw player
    screen.rectangle(xy=game.player_pos, size=(30,30), color=(100,250,150))
    
    # draw hud
    screen.text('Score {0}'.format(game.score), color='white', xy=(5,5), align='topleft', font_size=15)
    screen.text('High Score {0}'.format(game.high_score), color='white', xy=(315,5), align='topright', font_size=15)

@touch()
def on_touch(xy, action):
            
    if action == 'up':
        game.moving_right = False
        game.moving_left = False
        
    if action == 'down':
        if contains_pos(game.right_touch_area, xy):
            game.moving_right = True
        if contains_pos(game.left_touch_area, xy):
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
