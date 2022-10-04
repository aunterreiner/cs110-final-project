import pygame

class hostileProjectile(pygame.sprite.Sprite):
  def __init__(self,limit,x,y):
    """ 
    initializes the hostileProjectile
    args: object(self): hostileProjectile object, int(limit): the hostilePorjectile's y_coordinate limit, int(x): width of hostileProjectile, int(y): height of hostileProjectile
    return: N/A
    """
    super().__init__()
    self.image = pygame.image.load('assets/gameScreen/hostile_projectile.png').convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.limit = limit
    self.speed = 1

  def update(self):
    """
    updates the hostileProjectile's postion
    args: object(self): hostileProjectile object
    return: N/A
    """
    self.rect.y += self.speed
