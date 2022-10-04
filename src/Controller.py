import json
import pygame
import random
import sys
from operator import itemgetter
from src import Enemy
from src import HostileProjectile
from src import Player
from src import Projectile

class Controller:
  def __init__(self, width=640, height=480):
    """
    sets up the necessary instance variables for the controller
    args: obj(self): controller object, int(width): width of screen, int(height): height of screen 
    return: N/A
    """
    pygame.init()
    self.state = "STARTSCREEN"

  ##### setting up screen #####
    self.width = width
    self.height = height
    self.clock = pygame.time.Clock()
    self.screen = pygame.display.set_mode((self.width, self.height))

  ##### setting up background #####
    self.background = pygame.Surface(self.screen.get_size()).convert()
    self.background.fill((250, 250, 250))
    
  ##### setting up score value #####
    self.scoreValue = 0
    self.level = 1
    self.move_counter = 0
    self.make_move = False
    self.input_active = True
    self.text = ""
    self.movevar = 4
    self.movetime = 100
    self.enemy_move = pygame.USEREVENT

  ##### others #####
    pygame.font.init()
    pygame.key.set_repeat(20, 30)

##### main loop #####

  def mainLoop(self):
    """
    defines the game states
    args: object(self): controller object
    return: N/A
    """
    while True:
        
      if(self.state == "STARTSCREEN"):
        self.gameStart()

      elif(self.state == "GAME"):
        self.gameLoop()

      elif(self.state == "GAMEOVER"):
        self.gameOver()

##### levels #####

  def showLevel(self,x,y,level):
    """
    displays the level of the game
    args: object(self): controller object, int(x): x-coordinate of the level, int(y): y-coordinate of the level, int(level): integer level number
    return: N/A
    """
    levelFont = pygame.font.SysFont(None,30)
    level1 = levelFont.render("Level: " + str(level), True, (255, 255, 255))
    self.screen.blit(level1,(x,y))

##### show score #####

  def showScore(self,x,y, gameScore):
    """
    displays the score of the game
    args: object(self): controller object, int(x): x-coordinate of the score, int(y): y-coordinate of the score, int(gameScore): integer value of the score
    return: N/A
    """
    scoreFont = pygame.font.SysFont(None,30)
    score = scoreFont.render("Score: " + str(gameScore), True, (255, 255, 255))
    self.screen.blit(score,(x,y))

  def increaseLevel(self):
    """
    increases the level of the game and increases difficulty
    args: object(self): controller object
    return: N/A
    """
    self.level += 1
    if self.movevar:
      self.movevar -= 1
    if self.movetime > 10:
      self.movetime -= 10
    self.showLevel(10,10, self.level)
    for enemy in self.enemies:
      enemy.shot_freq //= 2
    self.set_enemy_timer()

  def initalizeEnemies(self):
    """
    creates the group of enemies
    args: object(self): controller object
    return: N/A
    """
    self.enemies = pygame.sprite.Group()
    self.enemies.update()
    margin = 20
    width = 60
    for x in range(margin, self.width - margin, width):
      for y in range(margin, int(self.height/4), width):
        self.enemies.add(Enemy.Enemy(x, y))
    return self.enemies

  def set_enemy_timer(self):
    """
    sets the move timer of the enemies
    args: object(self): controller object
    return: N/A
    """
    pygame.time.set_timer(self.enemy_move, 0)
    pygame.time.set_timer(self.enemy_move, self.movetime)

  def user_type(self, bg):
    """
    allows the user to type their highscore name on screen
    args: str(self): name of controller object, object(bg): background for the text
    return: N/A
    """
    font = pygame.font.SysFont(None,30)
    message = font.render('Please enter your name: ', False, (255,255,255))
    while True:
      for event in pygame.event.get():
        if(event.type == pygame.KEYUP):
            if event.key == pygame.K_RETURN:
              return
            elif event.key == pygame.K_BACKSPACE:
              if self.text:
                self.text = self.text[:-1]
            else:
              self.text += chr(event.key)

      text = font.render(self.text, False, (255,255,255))
      self.screen.blit(bg, (0,0))
      self.screen.blit(message,(200,100))
      self.screen.blit(text, (200,200))
      pygame.display.flip()


 ##### game loop #####

  def gameLoop(self):
    """
    defines what happens in the game state
    args: object(self): controller object
    return: N/A
    """
    self.custom_background2 = pygame.image.load("assets/gameScreen/space.jpeg").convert()
    self.custom_background2 = pygame.transform.smoothscale(self.custom_background2, self.screen.get_size())

    self.enemies = self.initalizeEnemies()
    self.enemies_remaining = 20
    ##### create sprite groups ##### 

    self.player = Player.Player("Conan", 50, 80, "assets/gameScreen/player.png")
    self.projectiles = pygame.sprite.Group()
    self.enemybullets = pygame.sprite.Group()
    self.all_sprites = pygame.sprite.Group((self.player,) + tuple(self.enemies))
    self.player.set_pos(250, 400)

    self.set_enemy_timer()
    while self.state == "GAME":

      ##### levels #####
      if (self.enemies_remaining == 0):
        self.enemies = self.initalizeEnemies()
        self.enemies.update()
        self.increaseLevel()
        self.enemies_remaining = 20
        self.all_sprites = pygame.sprite.Group((self.player,) + tuple(self.enemies))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

      ##### events #####

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()
        if event.type == self.enemy_move:
          for i in self.enemies:
            i.move(1)
        if event.type == pygame.KEYDOWN:
          if(event.key == pygame.K_LEFT):
            if self.player.rect.x == 0:
              self.player.rect.x == 0
            else:
              self.player.move_left()
          elif(event.key == pygame.K_RIGHT):
            if self.player.rect.x == 550:
              self.player.rect.x == 550
            else:
              self.player.move_right()
          elif(event.key == pygame.K_SPACE):
            ##### projectiles #####
            if len(self.projectiles.sprites()) <= 1000:
              p = Projectile.Projectile(640,self.player.rect.x, self.player.rect.y)
              pos = self.player.rect.midtop
              p.rect.x=pos[0]
              p.rect.y = pos[1]
              self.projectiles.add(p)
            else:
              print("can't shoot")
              
          
        ##### destroying enemies #####
        
      fight = pygame.sprite.groupcollide(self.enemies, self.projectiles, False, True)
      if fight:
        for enemy in fight:
          enemy.kill()
          self.scoreValue += 1
          self.enemies_remaining -= 1

      ##### redraw the entire screen #####
      self.enemies.update()
      self.projectiles.update()
      self.enemybullets.update()
      self.screen.blit(self.custom_background2, (0,0))

      ##### enemies shooting #####
      for enemy in self.enemies:
        if random.randrange(enemy.shot_freq) == 1:
          enemy_bullet = HostileProjectile.hostileProjectile(0,enemy.rect.x, enemy.rect.y)
          enemy_pos = enemy.rect.midtop
          enemy_bullet.rect.x= enemy_pos[0]
          enemy_bullet.rect.y = enemy_pos[1]
          self.enemybullets.add(enemy_bullet)

      ##### gameover conditions #####
            
      for enemy in self.enemies:
        if enemy.rect.y == 400:
          self.state = "GAMEOVER"
          self.user_type(self.custom_background2)
          print("Enemy Breach")
          break

      collision_fight = pygame.sprite.spritecollide(self.player, self.enemies, True)
      if collision_fight:
        self.state = "GAMEOVER"
        self.user_type(self.custom_background2)
        print("Enemy Collision")

      player_shot = pygame.sprite.spritecollide(self.player, self.enemybullets, True)
      if player_shot:
        self.state = "GAMEOVER"
        self.user_type(self.custom_background2)
        print("Player Shot")

###### display level, score, sprites on screen #####

      self.showLevel(10,10, self.level)
      self.showScore(400,10, self.scoreValue)

      self.all_sprites.draw(self.screen)
      self.projectiles.draw(self.screen)
      self.enemybullets.draw(self.screen)
      # update the screen
      pygame.display.flip()
  
##### START #####
  def gameStart(self): 
    """
    defines what happens in the game start state
    args: object(self): controller object
    return: N/A
    """
    
    self.custom_background = pygame.image.load("assets/startScreen/startscreen.png").convert()
    self.custom_background = pygame.transform.smoothscale(self.custom_background, self.screen.get_size())

    game_title = pygame.image.load('assets/startScreen/game_title.png').convert()
    title_size = game_title.get_size()
    game_title = pygame.transform.smoothscale(game_title,(title_size[0]//5,title_size[1]//5))

    present = pygame.image.load('assets/startScreen/present.png').convert()
    present_size = present.get_size()
    present = pygame.transform.smoothscale(present,(present_size[0]//5,present_size[1]//5))

    start_button = pygame.image.load('assets/startScreen/start_button.png').convert()
    start_size = start_button.get_size()
    start_button = pygame.transform.smoothscale(start_button,(start_size[0]//5,start_size[1]//5))
    rect = start_button.get_rect()
    rect = pygame.draw.rect(self.screen,(0, 0, 255),(400, 200, 100, 100))

    self.screen.blit(self.custom_background,(0,0))
    self.screen.blit(start_button, rect)
    self.screen.blit(game_title, (25,100))
    self.screen.blit(present, (25, 50))

    pygame.display.flip()

    while self.state == "STARTSCREEN":
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
          if rect.collidepoint(event.pos):
            print("game")
            self.state = "GAME"
      

##### GameOver #####

  def gameOver(self):
    """
    defines what happens in the game over state
    args: object(self): controller object
    return: N/A
    """
    
    self.player.kill()

    self.custom_background1 = pygame.image.load("assets/endScreen/bg.png").convert()
    self.custom_background1 = pygame.transform.smoothscale(self.custom_background1, self.screen.get_size())

    self.screen.blit(self.custom_background1,(0,0))

    self.playerName = self.text
    
    def saveScores(highscores):
      """
      saves a list of scores into a JSON file
      args: list(highscores): list of highscores
      return: N/A
      """
      fptr = open("etc/highscore.json", "w")
      json.dump(highscores, fptr)
      fptr.close()

    def loadScores():
      """
      returns the highscores from the JSON file
      args: N/A
      return: list(highscores): list of highscores
      """
      try:
        fptr = open("etc/highscore.json", "r")
        highscores = json.load(fptr)
      except FileNotFoundError:
        highscores = [] 
      fptr.close() 
      return sorted(highscores, key = itemgetter(1) , reverse = True)

    highscores = loadScores() 
    highscores.append([self.playerName, self.scoreValue])
    highscores = sorted(highscores, key = itemgetter(1) , reverse = True)
    saveScores(sorted(highscores, key = itemgetter(1), reverse = True))
    highscoreFont = pygame.font.SysFont(None,30)
    score_iter = 1
    leaderboard = 1
    for name, score in enumerate(highscores, start = 1):
      if leaderboard <= 10:
        score_dis = highscoreFont.render(f'{name} {score}', False, (255, 255, 255))
        self.screen.blit(score_dis, (25, score_iter + 150))
        score_iter += 30
        leaderboard += 1

    leaderboard = pygame.image.load('assets/endScreen/leaderboard.jpg').convert()
    lb_size = leaderboard.get_size()
    leaderboard = pygame.transform.smoothscale(leaderboard,(lb_size[0]//5,lb_size[1]//5))

    restart_button = pygame.image.load('assets/endScreen/restart_button.png').convert()
    rect = restart_button.get_rect()
    rect.center = (500, 135)

    self.screen.blit(restart_button, rect)
    self.screen.blit(leaderboard, (30,120))

    pygame.display.flip()

    while self.state == "GAMEOVER":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
              if rect.collidepoint(event.pos):
                self.__init__()
