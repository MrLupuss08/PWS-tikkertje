import pygame
import numpy as np
import sys
import math

pygame.init() #pygame opstarten
res=30
bord=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
      0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,
      0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,
      0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,
      0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,
      0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,
      0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,
      0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,
      0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,
      0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,
      0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,
      0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
pygame.display.set_caption("Tikkertje") #naam van systeem
Scherm_breedte=math.sqrt(len(bord))*res     #buiten class
Scherm_lengte=math.sqrt(len(bord))*res+30
scherm = pygame.display.set_mode((Scherm_breedte, Scherm_lengte))
lettertype1=pygame.font.SysFont("arial",36)
lettertype2=pygame.font.SysFont("arial",20)
#Kleuren bepaald met rbg (rood, groen, blauw) met schaal van 0-255
ZWART=(0,0,0)
GROEN=(0, 255, 0)
ROOD=(255,0,0)
BLAUW=(0, 0, 255)
WIT=(255,255,255)
ACHTERGROND_KLEUR=(50, 150, 255)

grid = np.zeros((15*res,15*res))
grid[6*res:8*res+1,6*res:8*res+1] = 1
muren=[]

class Tikkertje:
    def __init__(self):

        self.muur=pygame.Rect(0,0,res,res)
        for i in range(len(bord)):
            if bord[i]==1:
                self.x=i%math.sqrt(len(bord))
                self.y=i//math.sqrt(len(bord))
                muren.append((self.x,self.y))

        self.klok = pygame.time.Clock() #snelheid van spel (fps)

        self.renner=pygame.Rect(20,20,30,30)
        self.jager=pygame.Rect(Scherm_breedte-30,Scherm_lengte-60,30,30)
        self.score=0
        self.snelheid=1
        self.richting_r=["Noord",0,"X"]
        self.richting_j=["Noord",0,"X"]

    def Beeld(self, scherm):
        scherm.fill(ACHTERGROND_KLEUR)
        for i in range(len(muren)):
            self.x,self.y=muren[i]
            pygame.draw.rect(scherm,BLAUW,(self.x*res,self.y*res,res,res))
        pygame.draw.rect(scherm, ZWART, (0,Scherm_lengte-30,Scherm_breedte,30))
        pygame.draw.rect(scherm, GROEN, self.renner)
        pygame.draw.rect(scherm, ROOD, self.jager)
        scherm.blit(lettertype2.render(str(round(self.score,2)),True,WIT),(10,Scherm_lengte-30))
        pygame.display.flip() #Laat scherm nieuwst aanpassingen zien

    def engine_cumulatief(self, coordinaten,richting):    #coordinaten = renner of jager (zie keys_movement2, daarna running loop)
        self.snelheid=0.15
        self.x_oud = coordinaten.x
        self.y_oud = coordinaten.y
        if richting[0]==richting[2] and richting[1]!=25 and coordinaten==self.jager:
            richting[1]+=1
        if richting[0]==richting[2] and richting[1]!=20 and coordinaten==self.renner:
            richting[1]+=1
        elif richting[0]!=richting[2]:
            richting[1]=1

        if richting[0]=="West" and coordinaten.x!=0:
            coordinaten.x-=richting[1]*self.snelheid
        if richting[0]=="Oost" and coordinaten.x!=Scherm_breedte-30:
            coordinaten.x+=richting[1]*self.snelheid
        if richting[0]=="Noord" and coordinaten.y!=0:
            coordinaten.y-=richting[1]*self.snelheid
        if richting[0]=="Zuid" and coordinaten.y!=Scherm_lengte-60:
            coordinaten.y+=richting[1]*self.snelheid

        if coordinaten.x<0:
            coordinaten.x=0
        if coordinaten.x>Scherm_breedte-30:
            coordinaten.x=Scherm_breedte-30
        if coordinaten.y<0:
            coordinaten.y=0
        if coordinaten.y>Scherm_lengte-60:
            coordinaten.y=Scherm_lengte-60
        for i in range(len(muren)):
            self.muur.x,self.muur.y=muren[i]
            self.muur.x=self.muur.x*res
            self.muur.y=self.muur.y*res
            if coordinaten.colliderect(self.muur):
                coordinaten.x,coordinaten.y=self.x_oud,self.y_oud

    def keys_movement(self, coordinaten,richting): #self.keys is hier een output van een speler
        self.keys=pygame.key.get_pressed()
        richting[2]=richting[0]
        if self.keys[pygame.K_LEFT] and coordinaten.x!=0:
            richting[0]="West"
        elif self.keys[pygame.K_RIGHT] and coordinaten.x!=Scherm_breedte-20:
            richting[0]="Oost"
        elif self.keys[pygame.K_UP] and coordinaten.y!=0:
            richting[0]="Noord"
        elif self.keys[pygame.K_DOWN] and coordinaten.y!=Scherm_lengte-50:
            richting[0]="Zuid"
        else:
            richting[0]="X"
        self.engine_cumulatief(coordinaten,richting)

    def algoritme_1(self, pos_self,richting_self,pos_target,richting_target):
        richting_self[2]=richting_self[0]
        a=pos_target.x-pos_self.x
        if a==0: a=0.0001
        b=pos_target.y-pos_self.y
        if b==0: b=0.0001
        c=abs(a/b)
        if c>1 and a>0:
            richting_self[0]="Oost"
        elif c>1 and a<0:
            richting_self[0]="West"
        elif c<1 and b>0:
            richting_self[0]="Zuid"
        elif c<1 and b<0:
            richting_self[0]="Noord"
        elif c==1 and b<0:
            richting_self[0]="Noord"
        elif c==1 and b>0:
            richting_self[0]="Zuid"
        self.engine_cumulatief(pos_self,richting_self)

    def algoritme_2(self,pos_self,richting_self,pos_target,richting_target):
        richting_self[2]=richting_self[0]
        route=[]
        target=pos_target.copy()
        s=richting_target.copy()
        self.engine_cumulatief(target,s)

        if pos_self.x==pos_target.x or pos_self.y==pos_target.y:
            route.append((target.x,target.y))
        else:
            breedte=(pos_self.x,pos_target.y)
            hoogte=(pos_target.x,pos_self.y)
            if pos_target.x-pos_self.x>pos_target.y-pos_self.y:
                route.append(hoogte)
            else: route.append(breedte)

        rx,ry=route[0]
        if rx>pos_self.x and ry==pos_self.y: richting_self[0]="Oost"
        elif rx<pos_self.x and ry==pos_self.y: richting_self[0]="West"
        elif rx==pos_self.x and ry>pos_self.y: richting_self[0]="Zuid"
        elif rx==pos_self.x and ry<pos_self.y: richting_self[0]="Noord"
        else: richting_self[0]="X"
        self.engine_cumulatief(pos_self,richting_self)

    def agent_movement(self, action, coordinaten, richting):    #hier moet de output dus van de agent zijn
        richting[2]=richting[0]
        if np.array_equal(action, [0, 0, 0, 1, 0]) and coordinaten.x!=0:    #[“Noord”, “Zuid”, “Oost”, “West”, “X”]
            richting[0]="West"
        elif np.array_equal(action, [0, 0, 1, 0, 0]) and coordinaten.x!=Scherm_breedte-20:
            richting[0]="Oost"
        elif np.array_equal(action, [1, 0, 0, 0, 0]) and coordinaten.y!=0:
            richting[0]="Noord"
        elif np.array_equal(action, [0, 1, 0, 0, 0]) and coordinaten.y!=Scherm_lengte-50:
            richting[0]="Zuid"
        else:
            richting[0]="X"
        self.engine_cumulatief(coordinaten,richting)

if __name__ == '__main__':
    tikkertje = Tikkertje()

    running=True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Als je op het kruisje klikt
                running=False

        tikkertje.keys_movement(tikkertje.renner,tikkertje.richting_r)   #
        #self.algoritme2(self.renner,self.richting_j,self.jager)

        tikkertje.algoritme_2(tikkertje.jager,tikkertje.richting_j,tikkertje.renner,tikkertje.richting_r)
        
        tikkertje.score+=1/60
        tikkertje.Beeld(scherm)
        if tikkertje.jager.colliderect(tikkertje.renner):
            scherm.fill(ACHTERGROND_KLEUR)
            scherm.blit(lettertype1.render("Jager wint",True,ZWART),(130,100))
            scherm.blit(lettertype1.render(str(round(tikkertje.score,2)),True,ZWART),(130,200))
            pygame.display.flip()
            tikkertje.klok.tick(2)
            running=False
        
        tikkertje.klok.tick(60) #spel draait op 60 fps

    pygame.quit()
    sys.exit()
