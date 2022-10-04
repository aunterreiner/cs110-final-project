import pygame
#model
class Player(pygame.sprite.Sprite):
    def __init__(self, name, x, y, img_file):
        """
        initializes the player
        args: object(self): player object, str(name): name of player, int(x): width of player, int(y): height of player, str(img_file) string path of image file
        return: N/A
        """
        #initialize all the Sprite functionality
        pygame.sprite.Sprite.__init__(self)

        #The following two attributes must be called image and rect
        #pygame assumes you have intitialized these values
        #and uses them to update the screen

        #create surface object image
        self.image = pygame.image.load(img_file).convert_alpha()
        #get the rectangle for positioning
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #set other attributes
        self.name = name
        self.speed = 10
        self.health = 3


    def set_pos(self,x_pos, y_pos):
        """
        sets the player's position
        args: object(self): player object, int(x_pos): x-coordinate of player starting position, int(y_pos): y-coordinate of player starting position
        return: N/A
        """
        self.rect.x = x_pos
        self.rect.y = y_pos

    #methods to make moving our hero easier
    def move_left(self):
        """
        moves the player left
        args: object(self) player object
        return: N/A
        """
        self.rect.x -= self.speed
    def move_right(self):
        """
        moves the player right
        args: object(self) player object
        return: N/A
        """
        self.rect.x += self.speed
