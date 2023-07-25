import utime
import urandom
from machine import Pin, I2C, ADC
import ssd1306
class PingPong:
    
    def __init__(self):
        #setup display

        i2c = I2C(sda=Pin(4), scl=Pin(5))
        self.display = ssd1306.SSD1306_I2C(64, 48, i2c)
        
        self.game_work = 1
        #ball (square)
        self.posx = 1
        self.posy = 4
        self.rect1x = 3
        self.rect1y = 3
        self.y1 = 0
        self.x1 = 0
        self.work = 1
        
        #rocket
        self.rocketx = 32
        self.rockety = 35
        self.rect2x = 20
        self.rect2y =2

        #life
        self.lifex = 4
        self.lifey = 3
        self.liferectx = 2
        self.liferecty = 2
        self.lifes = 2
        
        #check log need if catch new bags
        self.log = 1
        #score
        self.exit = 0
        self.score = 0

    def start_game(self):

        while self.game_work:
            
            self.display.fill(0)
            self._draw_borders()
            self._check_pot()
            self._check_rect_rocket()
            self._check_pos_ball()
            self._check_direction_ball()
            self._draw_ball()
            self._draw_rocket()
            self._draw_lifes()
            self._draw_score()
            
            self.display.show()
            
            if self.log:
                self._log_system(0,0,1)
                
        self.display.fill(0)
        self.display.text("Game",0,0,1)
        self.display.text("over",0,10,1)
        self.display.text(":(",0,20,1)
        self.display.text("score:", 0, 30, 1)
        self.display.text(f"{self.score}", 0, 40, 1)
        self.display.show()
                
    def _draw_ball(self):
        self.display.fill_rect(self.posx, self.posy, self.rect1x, self.rect1y, 1)
    def _draw_rocket(self):
        self.display.fill_rect(self.rocketx, self.rockety, self.rect2x, self.rect2y, 1)
    def _draw_score(self):
        self.display.text(f"{self.score}", 46, 2, 1)
    def _check_pos_ball(self):
        if self.posy >= 44:
            self.y1 = 1; self._check_lifes()
        elif self.posy == 0:
            self.y1 = 0
        if self.posx == 60:
            self.x1 = 1
        elif self.posx == 0:
            self.x1 = 0
        
    def _check_direction_ball(self):
        if self.y1:
            self.posy -= 1
        else:
            self.posy += 1
        if self.x1: 
            self.posx -= 1
        else: 
            self.posx += 1
    
    def _check_rect_rocket(self):
        if self.rockety == self.posy + 3 or self.rockety == self.posy + 2:
            for i in range(self.rocketx, self.rocketx + self.rect2x + 1):
                for b in range(self.posx , self.posx + 3):
                    if i == b: self.y1 = 1; self.score +=1; self.exit = 1; break
                if self.exit: self.exit = 0; break
                    
    def _log_system(self, cbal, crocket, score):
        if cbal: 
            print(f"ball posx:{self.posx} ball posy:{self.posy}")
        if crocket: 
            print(f"rocket posx:{self.rocketx} rocket posy:{self.rockety}")
        if score: 
            print(self.score)
            
        
        
        
    def _draw_borders(self):
        self.display.hline(0, 0, 64, 1)
        self.display.vline(0, 0, 48, 1)
        self.display.hline(0, 47, 64, 1)
        self.display.vline(63, 0, 48, 1)
    
    def _draw_lifes(self):

        for i in range(0, self.lifes + 1):
            self.display.fill_rect(self.lifex, self.lifey, self.liferectx, self.liferecty, 1)
            self.lifex += 4
        self.lifex = 4
            
    def _check_lifes(self):
        if self.lifes:
            random = self._randint(0, 64)
            self.lifes -= 1
            utime.sleep(2)
            self.posx = random
            self.posy = 10
        else:
            utime.sleep(2)
            self.game_work = 0

    def _randint(self, min, max):
        span = max - min + 1
        div = 0x3fffffff // span
        offset = urandom.getrandbits(30) // div
        val = min + offset
        return val
    
    def _check_pot(self):
        adc = ADC(0)
        scaled_value = (adc.read() - 0) * (64 - self.rect2x - 0) // (1024 - 0) + 0
        self.rocketx = scaled_value 
        

PingPong().start_game()
