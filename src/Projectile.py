import pygame

class Projectile(pygame.sprite.Sprite):
  def __init__(self,limit,x,y):
    """ 
    initializes the Projectile
    args: object(self): Projectile object, int(limit): the Porjectile's y_coordinate limit, int(x): width of Projectile, int(y): height of Projectile
    return: N/A
    """
    super().__init__()
    self.image = pygame.image.load('assets/gameScreen/bullet.png').convert_alpha()
    self.rect = self.image.get_rect()
    self.limit = limit
    self.speed = 10

  def update(self):
    """
    updates the Projectile's postion
    args: object(self): Projectile object
    return: N/A
    """
    self.rect.y -= self.speed

