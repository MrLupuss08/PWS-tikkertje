import pygame
import numpy as np
import sys
import math
import heapq
from random import randint
from typing import List, Tuple, Dict, Set

pygame.init() #pygame opstarten
res=30
bord=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
      0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,
      0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,
      0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
      0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,
      0,0,0,1,1,1,0,0,0,1,1,1,5,0,0,
      0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,
      0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,
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
muren=[]

class Tikkertje:
    def __init__(self):

        self.muur=pygame.Rect(0,0,res,res)
        """
        u=-1
        for i in range(2):
            for j in range(15):
                muren.append((j,u))
                muren.append((u,j))
            u=15
        """

        for i in range(len(bord)):
            if bord[i]==1:
                self.x=i%math.sqrt(len(bord))
                self.y=i//math.sqrt(len(bord))
                muren.append((self.x,self.y))

        for i in range(len(muren)):
            self.x,self.y=muren[i]
            grid[int(self.x*res):int((self.x+1)*res+1),int(self.y*res):int((self.y+1)*res+1)] = 1 #dit komt alleen overeen als de map gespiegeld is over de y-as in het midden, nu is dat zo dus geen zorgen

        self.klok = pygame.time.Clock() #snelheid van spel (fps)

        goedkeuren=True
        while goedkeuren:
            waarde=randint(0,224)
            if bord[waarde]!=1: goedkeuren=False
        self.renner=pygame.Rect(waarde%15*30,waarde//15*30,30,30)
        goedkeuren=True
        while goedkeuren:
            waarde=randint(0,224)
            if bord[waarde]!=1: goedkeuren=False
        self.jager=pygame.Rect(waarde%15*30,waarde//15*30,30,30)
        self.score=0
        self.snelheid=1
        self.richting_r=["Noord",0,"X"]
        self.richting_j=["Noord",0,"X"]
        self.naast_muur=False
        self.voorkeur = "X"
        self.slapen = 0

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
        elif richting[0]==richting[2] and richting[1]!=20 and coordinaten==self.renner:
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

        for i in range(len(muren)):
            self.muur.x,self.muur.y=muren[i]
            self.muur.x=self.muur.x*res
            self.muur.y=self.muur.y*res
            if coordinaten.colliderect(self.muur):
                coordinaten.x,coordinaten.y=self.x_oud,self.y_oud

    def keys_movement(self, pos_self,richting): #self.keys is hier een output van een speler
        self.keys=pygame.key.get_pressed()
        richting[2]=richting[0]
        if self.keys[pygame.K_LEFT] and pos_self.x!=0:
            richting[0]="West"
        elif self.keys[pygame.K_RIGHT] and pos_self.x!=Scherm_breedte-20:
            richting[0]="Oost"
        elif self.keys[pygame.K_UP] and pos_self.y!=0:
            richting[0]="Noord"
        elif self.keys[pygame.K_DOWN] and pos_self.y!=Scherm_lengte-50:
            richting[0]="Zuid"
        else:
            richting[0]="X"
        #self.engine_cumulatief(pos_self,richting)

    def calc_time(self,punt1,punt2,snelheid,player):
        #tussen twee punten berekenen. dus de x'en zijn aan elkaar gelijk of de y'en zijn aan elkaar gelijk
        punt1_x,punt1_y=punt1
        punt2_x,punt2_y=punt2
        time=0
        distance_t=abs(punt1_x+punt1_y-punt2_x-punt2_y)
        distance=0
        if punt1_x>punt2_x and snelheid[1]=="West": speed=snelheid[0].copy()
        elif punt1_x<punt2_x and snelheid[1]=="Oost": speed=snelheid[0].copy()
        elif punt1_y>punt2_y and snelheid[1]=="Noord": speed=snelheid[0].copy()
        elif punt1_y<punt2_y and snelheid[1]=="Zuid": speed=snelheid[0].copy()
        else: speed=1
        while distance<distance_t:
            time+=1
            distance+=speed
            if speed!=25 and player=="jager": speed+=1
            elif speed!=20 and player=="renner": speed+=1
        return time

    def tijd_berekenen(self,punt1,punt2,snelheid,player):
        punt1_x,punt1_y=punt1
        punt2_x,punt2_y=punt2
        time=0
        if punt1_x==punt2_x or punt1_y==punt2_y:
            time=self.calc_time(punt1,punt2,snelheid,player)
        else:
            tussenpunt=((punt1_x,punt2_y))
            time=self.calc_time(punt1,tussenpunt,snelheid,player)+self.calc_time(tussenpunt,punt2,snelheid,player)
        return time



    def muurchecken(self,punt1,punt2):
        punt1_x,punt1_y=punt1
        punt2_x,punt2_y=punt2
        punt1_x=int(punt1_x/res)
        punt1_y=int(punt1_y/res)
        punt2_x=int(punt2_x/res)
        punt2_y=int(punt2_y/res)
        if punt1_x==punt2_x and punt1[0]/res==int(punt1[0]/res):
            vakjes=1
        elif punt1_y==punt2_y and punt1[1]/res==int(punt1[1]/res):
            vakjes=1
        else: vakjes=2
        wissel=False
        for i in range(abs(punt1_x+punt1_y-punt2_x-punt2_y)):
            for j in range(vakjes):
                if punt1_x==punt2_x and punt1_y>punt2_y:
                    if muren.count((punt1_x+j,punt1_y-i))==1:
                        wissel=True

                elif punt1_x==punt2_x and punt1_y<punt2_y:
                    if muren.count((punt1_x+j,punt1_y+i))==1:
                        wissel=True


                elif punt1_x>punt2_x and punt1_y==punt2_y:
                    if muren.count((punt1_x-i,punt1_y+j))==1:
                        wissel=True

                elif punt1_x<punt2_x and punt1_y==punt2_y:
                    if muren.count((punt1_x+i,punt1_y+j))==1:
                        wissel=True
        if wissel==True: return "nee"
        else: return "ja"







    def algoritme_j(self,pos_self,richting_self,pos_target,richting_target):
        richting_self[2]=richting_self[0]
        #voorspelling maken waar de ander zal zijn
        target=pos_target.copy()
        s=richting_target.copy()
        self.engine_cumulatief(target,s)

        pogingen=0
        tellertje=1
        tellertje2=1
        punten=[]
        breedte=(pos_self.x,target.y)
        hoogte=(target.x,pos_self.y)
        goedkeuren=True
        binnendoor=False
        route=[]
        closed=[]
        while goedkeuren==True:
            
            breedte=(pos_self.x,target.y)
            hoogte=(target.x,pos_self.y)
            if pogingen==0:
                if pos_self.x==target.x or pos_self.y==target.y:
                    route.append((target.x,target.y))
                pogingen=1

            if pogingen==1:
                if richting_self[0]=="Noord" or richting_self[0]=="Zuid" or richting_self[0]=="X":
                    route.append(breedte)
                elif richting_self[0]=="Oost" or richting_self[0]=="West":
                    route.append(hoogte)
                route.append((target.x,target.y))
                pogingen=2

            elif pogingen==2:    
                if closed[0]==breedte:
                    route.append(hoogte)
                if closed[0]==hoogte:
                    route.append(breedte)
                route.append((target.x,target.y))
                pogingen=3
            
            elif pogingen==3:
                print("3")
                hbhr=[]
                bhbr=[]
                for i in range(15):
                    hbhr.append((pos_self.x,(pos_self.y-tellertje*res)%450))
                    hbhr.append((target.x,(pos_self.y+tellertje*res)%450))
                    hbhr.append((target.x,target.y))
                    muren=False
                    for i in range(len(hbhr)):
                        if i==0:
                            if self.muurchecken((pos_self.x,pos_self.y),hbhr[i])=="nee": muren=True
                        else:
                            if self.muurchecken(hbhr[i-1],hbhr[i])=="nee": muren=True
                    if muren==False: 
                        punten.append(hbhr[0])
                    hbhr=[]

                    bhbr.append(((pos_self.x-tellertje*res)%450,pos_self.y))
                    bhbr.append(((pos_self.x-tellertje*res)%450,target.y))
                    bhbr.append((target.x,target.y))
                    muren=False
                    for i in range(len(bhbr)):
                        if i==0:
                            if self.muurchecken((pos_self.x,pos_self.y),bhbr[i])=="nee": muren=True
                        else:
                            if self.muurchecken(bhbr[i-1],bhbr[i])=="nee": muren=True
                    if muren==False: 
                        punten.append(bhbr[0])
                    bhbr=[]
                    tellertje+=1
                    tellertje2+=1
                tijd=[]
                for i in range(len(punten)):
                    tijd.append(self.tijd_berekenen((pos_self.x,pos_self.y),punten[i],richting_self,"jager"))
                route.append(punten[tijd.index(min(tijd))])
                pogingen=4
                tellertje=1

            if pogingen>3: break
               
            teller=1
            for i in range(len(route)):
                if i==0:
                    if self.muurchecken((pos_self.x,pos_self.y),route[i])=="nee": teller=0
                else:
                    if self.muurchecken(route[i-1],route[i])=="nee": teller=0
            if teller==1 and len(route)>0: 
                goedkeuren=False
            elif teller==0 and len(route)>0:
                closed.append(route[0])
                route=[]
                print("NEEEEE!")

        rx,ry=route[0]
        if rx>pos_self.x and ry==pos_self.y: richting_self[0]="Oost"
        elif rx<pos_self.x and ry==pos_self.y: richting_self[0]="West"
        elif rx==pos_self.x and ry>pos_self.y: richting_self[0]="Zuid"
        elif rx==pos_self.x and ry<pos_self.y: richting_self[0]="Noord"
        else: richting_self[0]="X"
        
        
        print("Richting jager:", richting_self[0])
        print("----------------")










    def algoritme_r(self,pos_self,richting_self,pos_target,richting_target,voorkeur,naast_muur,slapen):
        richting_self[2]=richting_self[0]
        self_x,self_y=pos_self.x,pos_self.y
        self_x=int((self_x)/res)
        self_y=int((self_y)/res)
        richtingen=["Noord","Oost","Zuid","West"]        
        aanliggenden=[(int((pos_self.x+40)/30),self_y),(self_x-1,self_y),(self_x,int((pos_self.y+40)/30)),(self_x,self_y-1)]
        if self.slapen == 0:
            if self.naast_muur==False:
                for i in range(4):
                    if aanliggenden[i] in muren:
                        self.naast_muur=True
                if self.naast_muur==True:
                    ri=richtingen.index(richting_self[2])
                    if aanliggenden[0] in muren and richting_self[0]=="Oost": richting_self[0]=richtingen[(ri+1)%4]; self.slapen=30
                    elif aanliggenden[0] in muren and richting_self[0]=="West": richting_self[0]=richtingen[(ri+1)%4]; self.slapen=30
                    elif aanliggenden[1] in muren and richting_self[0]=="Oost": richting_self[0]=richtingen[(ri+1)%4]; self.slapen=30
                    elif aanliggenden[1] in muren and richting_self[0]=="West": richting_self[0]=richtingen[(ri+1)%4]; self.slapen=30
                    elif aanliggenden[2] in muren and richting_self[0]=="Noord": richting_self[0]=richtingen[(ri+1)%4]; self.slapen=30
                    elif aanliggenden[2] in muren and richting_self[0]=="Zuid": richting_self[0]=richtingen[(ri+1)%4]; self.slapen=30
                    elif aanliggenden[3] in muren and richting_self[0]=="Noord": richting_self[0]=richtingen[(ri+1)%4]; self.slapen=30
                    elif aanliggenden[3] in muren and richting_self[0]=="Zuid": richting_self[0]=richtingen[(ri+1)%4]; self.slapen=30
                    print(richting_self[0])
                
            if self.naast_muur==True and self.voorkeur=="X":
                if richting_self[0] == "Oost" and muren.count((self_x,int((pos_self.y+40)/30))): self.voorkeur="rechts"
                elif richting_self[0]=="Oost" and muren.count((self_x,self_y-1)): self.voorkeur="links"
                elif richting_self[0]=="West" and muren.count((self_x,int((pos_self.y+40)/30))): self.voorkeur="links"
                elif richting_self[0]=="West" and muren.count((self_x,self_y-1)): self.voorkeur="rechts"
                elif richting_self[0]=="Noord" and muren.count((int((pos_self.x+40)/30),self_y)): self.voorkeur="rechts"
                elif richting_self[0]=="Noord" and muren.count((self_x-1,self_y)): self.voorkeur="links"
                elif richting_self[0]=="Zuid" and muren.count((int((pos_self.x+40)/30),self_y)): self.voorkeur="links"
                elif richting_self[0]=="Zuid" and muren.count((self_x-1,self_y)): self.voorkeur="rechts"
                
            elif self.naast_muur==True:
                ri=richtingen.index(richting_self[0])
                if self.voorkeur=="rechts":
                    if richting_self[0]=="Noord" and muren.count((self_x+2,self_y+1))==0:
                        richting_self[0]=richtingen[(ri+1)%4]
                        self.slapen=30
                    elif richting_self[0]=="Oost" and muren.count((self_x,self_y+2))==0:
                        richting_self[0]=richtingen[(ri+1)%4]
                        self.slapen=30
                    elif richting_self[0]=="Zuid" and muren.count((self_x-2,self_y))==0:
                        richting_self[0]=richtingen[(ri+1)%4]
                        self.slapen=30
                    elif richting_self[0]=="West" and muren.count((self_x+1,self_y-2))==0:
                        richting_self[0]=richtingen[(ri+1)%4]
                        self.slapen=30
                elif self.voorkeur=="links":
                    if richting_self[0]=="Noord" and muren.count((self_x-2,self_y+1))==0:
                        richting_self[0]=richtingen[(ri-1)%4]
                        self.slapen=30
                    elif richting_self[0]=="Oost" and muren.count((self_x,self_y-2))==0:
                        richting_self[0]=richtingen[(ri-1)%4]
                        self.slapen=30
                    elif richting_self[0]=="Zuid" and muren.count((self_x+2,self_y))==0:
                        richting_self[0]=richtingen[(ri-1)%4]
                        self.slapen=30
                    elif richting_self[0]=="West" and muren.count((self_x+1,self_y+2))==0:
                        richting_self[0]=richtingen[(ri-1)%4]
                        self.slapen=30
                
            if self.naast_muur==False:
                self.voorkeur="X"
                tijd=[]
                for i in range(len(muren)):
                    mx,my=muren[i]
                    tijd.append(self.tijd_berekenen((pos_self.x,pos_self.y),(mx*30+15,my*30+15),richting_self,"renner"))
                target=muren[tijd.index(min(tijd))]
                target=(target[0]*30+15,target[1]*30+15)
                if target[0]!=pos_self.x and target[1]!=pos_self.y:
                    target=(pos_self.x,target[1])
                tx,ty=target
                if tx>pos_self.x and ty==pos_self.y: richting_self[0]="Oost"
                elif tx<pos_self.x and ty==pos_self.y: richting_self[0]="West"
                elif tx==pos_self.x and ty>pos_self.y: richting_self[0]="Zuid"
                elif tx==pos_self.x and ty<pos_self.y: richting_self[0]="Noord"
        else: self.slapen-=1











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

        #tikkertje.keys_movement(tikkertje.renner,tikkertje.richting_r)
        tikkertje.algoritme_r(tikkertje.renner,tikkertje.richting_r,tikkertje.jager,tikkertje.richting_j,tikkertje.voorkeur,tikkertje.naast_muur,tikkertje.slapen)

        #tikkertje.keys_movement(tikkertje.jager,tikkertje.richting_j) 
        tikkertje.algoritme_j(tikkertje.jager,tikkertje.richting_j,tikkertje.renner,tikkertje.richting_r)

        tikkertje.engine_cumulatief(tikkertje.renner,tikkertje.richting_r)
        tikkertje.engine_cumulatief(tikkertje.jager,tikkertje.richting_j)

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
