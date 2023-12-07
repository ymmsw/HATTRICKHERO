# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 11:00:02 2023

@author: Ymmsw
"""

import pygame
import simpleGE

class Goalpost(simpleGE.SuperSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("GPP.png")
        self.setSize(100, 50)
        self.y = 450
        self.x = 320
        self.setBoundAction(self.BOUNCE)
        self.reset()
        
    def reset(self):
        self.setDX(30)
        
class Striker(simpleGE.SuperSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("jude.png")
        self.setSize(100, 100)
        self.y = 120
        self.x = 380
        
class Ball(simpleGE.SuperSprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("kiss.png")
        self.setSize(20, 20)
        self.y = 160
        self.x = 320
        self.setDY(0)
        self.ballBitch = simpleGE.Sound("selina.wav")
        self.ballSound = simpleGE.Sound("catwoman2.wav")
        self.score = 0
        self.misses = 0
        self.timerStarted = False
        
    def checkEvents(self):
        if self.scene.isKeyPressed(pygame.K_SPACE):
            self.setDY(21)
            self.timerStarted = True
        if self.collidesWith(self.scene.goalpost):
            self.scene.points.goalpoint()
            self.ballBitch.play()
            self.reset()    
        self.checkbounds()
            
    def checkbounds(self):
        if self.rect.bottom > self.screen.get_height():
            self.scene.points.misspoint()
            self.ballSound.play()
            self.reset() 
            
            
    def reset(self):
        self.y = 160
        self.x = 320
        self.setDY(0)    


        



        
        
class Instructions(simpleGE.MultiLabel):
    def __init__(self):
        super().__init__()
        self.textLines = ["CLICK TO START"
                          , "Score a HATTRICK to win the game! "]
        self.center = ((340, 240))
        self.size = ((590, 100))
        self.font = pygame.font.Font("consequences.ttf",  25)
        self.fgColor = (0x00, 0X00, 0X00)
        self.bgColor = (0x00, 0XF0, 0X00)
        self.hide()


class Points(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.goals = 0
        self.misses = 0
        self.text = f"Goals: {self.goals} | Misses: {self.misses}"
        self.center = (200, 30)
        self.size = (370, 40)
        self.font = pygame.font.Font("consequences.ttf", 25)
        self.fgColor = (0x00, 0x00, 0x00)
        self.bgColor = (0x00, 0xFF, 0x00)
        self.gameOver = False
        self.update_text()

    def goalpoint(self):
        self.goals += 1
        self.update_text()
            
    def misspoint(self):
        self.misses += 1
        self.update_text()
        
    def checkEvents(self):
        if self.misses == 3:
            self.gameOver = True
        if self.goals == 3:
            self.gameOver = True
            
    def reset(self):
        self.gameOver = False
        


        

    def update_text(self):
        self.text = f"Goals: {self.goals} | Misses: {self.misses}"


class LblTimer(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.timer = simpleGE.Timer()
        self.timeOver = False
        self.center = (85, 60)
        self.size = (140, 25)
        self.font = pygame.font.Font("consequences.ttf", 20)
        self.fgColor = (0x00, 0x00, 0x00)
        self.bgColor = (0x00, 0xFF, 0x00)
        



    def checkEvents(self):
        timeLeft = max(0, 8 - self.timer.getElapsedTime())
        self.text = f"{timeLeft: 2f}"
            
        if timeLeft == 0 :
           self.timeOver = True
            
    def reset(self):
        self.timeQuit = False
        self.timer.start()
        
class BtnQuit(simpleGE.Button):
    def __init__(self):
        super().__init__()
        self.text = "Quit"
        self.center = (415, 380)
        self.size = (170, 45)
        self.font = pygame.font.Font("consequences.ttf", 40)
        self.fgColor = (0x00, 0x00, 0x00)
        self.bgColor = (0x00, 0xFF, 0x00) 
        self.hide()
      
        
class BtnReset(simpleGE.Button):
    def __init__(self):
        super().__init__()
        self.text = "Reset"
        self.center = (215, 380)
        self.size = (170, 45)
        self.font = pygame.font.Font("consequences.ttf", 40)
        self.fgColor = (0x00, 0x00, 0x00)
        self.bgColor = (0x00, 0xFF, 0x00) 
        self.hide()
 
        
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("FP.jpg")
        self.background = pygame.transform.scale(self.background, (640, 480))
        self.setCaption("Score a Hattrick")
        self.goalpost = Goalpost(self)
        self.ball = Ball(self)
        self.striker = Striker(self)
        self.instructions = Instructions()
        self.points = Points()
        self.lblTimer = LblTimer()
        self.score = 0
        self.misses = 0
        self.btnQuit = BtnQuit()
        self.btnReset = BtnReset()
        self.font = pygame.font.Font("consequences.ttf", 36)
   
        self.sprites = [self.goalpost, self.ball, self.striker, self.instructions, self.points, self.lblTimer, self.btnReset, self.btnQuit]
 
        

    def pauseGame(self):
        self.lblTimer.hide()
        self.points.hide()
        self.btnQuit.show((220, 240))
        self.btnReset.show((420, 240))


    def resetGame(self):
        self.instructions.hide()
        self.btnQuit.hide()
        self.btnReset.hide()
        self.lblTimer.show((320, 240))
        self.lblTimer.reset()
        

        

        
        
    def update(self):
        if self.instructions.clicked:
            self.resetGame()    
            
        if self.lblTimer.timeOver:
            self.pauseGame()
            
        if self.points.gameOver:
            self.pauseGame()
            
        if self.btnQuit.clicked:
            self.stop()
            
        if self.btnReset.clicked:
            self.resetGame()
            

        
def main():
    game = Game()
    game.start()
    

    
 


if __name__ == "__main__":
    main()