import pygame
#model
class Enemy(pygame.sprite.Sprite):
  def __init__(self, x, y):
    """
    initializes the enemy class
    args: object(self): enemy object, int(x): width of enemy, int(y): height of enemy
    return: N/A
    """
    super().__init__()
    self.sprites = []
    self.sprites.append(pygame.image.load('assets/gameScreen/enemy_1.png'))
    self.sprites.append(pygame.image.load('assets/gameScreen/enemy_2.png'))

    self.current_sprite = 0 
    self.image = self.sprites[self.current_sprite]

    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.shot_freq = 3000
  
  def update(self):
    """
    updates the enemy's movement
    args: object(self): enemy object
    return: N/A
    """
    self.current_sprite += 1
    
    if self.current_sprite >= len(self.sprites):
      self.current_sprite = 0
    self.image = self.sprites[self.current_sprite]

  def set_pos(self,x_pos, y_pos):
    """
    sets the enemy's position
    args: object(self): enemy object, int(x_pos): x-coordinate of enemy starting position, int(y_pos): y-coordinate of enemy starting position
    return: N/A
    """
    self.rect.x = x_pos
    self.rect.y = y_pos

  def move(self, vel):
    """
    defines the enemies movement
    args: object(self): enemy object, int(vel) the enemies integer speed
    return: N/A
    """
    self.rect.y += vel

