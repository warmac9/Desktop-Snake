import os
import threading
import time
import random

#control playable area
icon_heigth = 8
icon_width = 6
#speed of the game
tick_time = 3
#controls
keyBind = ["w", "d", "s", "a"]

#position of tiles of the snake
pos = [0]
#direction of the tiles
direc = [0]
#current direction
a_direc = 0
score = 0
grow = 1
#controls the score needed to grow the snake
growInterval = 2

#setting for iMac
if(os.uname().sysname == "Darwin"):
    keyBind = ["w", "a", "s", "d"]
    tick_time = 1

#position of tiles of borders of playable area in order to wrap the snake around the map
t_bor = []
b_bor = []
l_bor = []
r_bor = []

#remove playable area
def clean():
    i = 0
    go = 1
    while(go):
        #no ending - clear tile,  .png - tile of the snake, ".mp4" - food
        path = ["", ".png", ".mp4"]
        rem = 0
        for o in path:
            if(os.path.isfile('joj'+str(i)+o)):
                os.remove("joj"+str(i)+o)
                rem = 1
        if(rem == 0):
            go = 0
        i += 1

#initialize playable area
def init():
    global icon_height, icon_width
    for i in range(icon_heigth * icon_width):
        if(i in pos):
            jaj = open("joj" + str(i)+".png", "w")
        else:
            jaj = open("joj"+str(i), "w")
        jaj.write("jaj")
        jaj.close()
    for i in range(icon_width):
        t_bor.append(i*icon_heigth)
        b_bor.append((i+1)*icon_heigth-1)
    for i in range(icon_heigth):
        l_bor.append(i)
        r_bor.append(i+(icon_width-1)*icon_heigth)


stopInterval = []

def set_interval(arg, name):
    global stopInterval
    if name in stopInterval:
        stopInterval.remove(name)
    else:
        arg[1]()
        t = threading.Timer(arg[0], set_interval, [arg, name])
        t.start()

def stop_interval(name):
    global stopInterval
    stopInterval.append(name)

#check if the head of the snake overlaps border in order to wrap him around the map
def check_border(pos, direct):
    if(direct == 0):
        if(pos in t_bor):
            return b_bor[t_bor.index(pos)]
    elif(direct == 1):
        if(pos in r_bor):
            return l_bor[r_bor.index(pos)]
    elif(direct == 2):
        if(pos in b_bor):
            return t_bor[b_bor.index(pos)]
    elif(direct == 3):
        if(pos in l_bor):
            return r_bor[l_bor.index(pos)]

#change position of the tile of the snake based on direction and position
def change_pos(pos, direct):
    if(direct == 0):
        flip=check_border(pos, direct)
        if(flip == None):
            pos -= 1
        else:
            pos = flip
    elif(direct == 1):
        flip=check_border(pos, direct)
        if(flip == None):
            pos += icon_heigth
        else:
            pos = flip
    elif(direct == 2):
        flip=check_border(pos, direct)
        if(flip == None):
            pos += 1
        else:
            pos = flip
    elif(direct == 3):
        flip=check_border(pos, direct)
        if(flip == None):
            pos -= icon_heigth
        else:
            pos = flip
    return pos

#generate food
def food():
    global icon_heigth, icon_width
    satisfied = False
    while not satisfied:
        r = random.randint(0, icon_heigth*icon_width)
        if(os.path.isfile('joj'+str(r))):
            os.rename("joj"+str(r), "joj"+str(r)+".mp4")
            satisfied = True

#check if food is on the position the snake is about to collide with
def check_food(newPos):
    global score, grow
    if(os.path.isfile("joj"+str(newPos)+".mp4")):
        os.rename("joj"+str(newPos)+".mp4", "joj"+str(newPos))
        score += 1
        if(score%growInterval == 0):
            grow = 1
        food()

def tick():
    global pos, direc, a_direc, grow
    #get first position and direction of the tile of the snake, which is used to generate new head position
    p, d = pos[0], direc[0]
    #snake grow by not deleting his tail
    if(grow != 2):
        #pop the tail
        dp, dd = pos.pop(), direc.pop()
    #new head position
    newPos = change_pos(p, d)
    check_food(newPos)
    #grow: 2 prevent deleting(renaming) the tail and setting grow to zero to stop the growth durick the upcoming tick
    if(grow == 2):
        grow = 0
    else:
        #set grow to one, what means the growth will be executed during the upcoming dick
        if(grow  == 1):
            grow = 2
        #delete the tail
        os.rename("joj"+str(dp)+".png", "joj"+str(dp))
    #check if the snake collided with itself
    if(not os.path.isfile("joj"+str(newPos))):
        stop_interval("tick")
        clean()
        print("bum bac")
        print("score:"+str(score))
    #move the head by renaming the file
    os.rename("joj"+str(newPos), "joj"+str(newPos)+".png")
    #insert postion and direction of the head
    direc.insert(0, a_direc)
    pos.insert(0, newPos)

clean()
init()
set_interval([tick_time, tick], "tick")
food()

while True:
    #control the snake through console
    inp = input()
    if(inp in keyBind):
        #check the key to prevent snake going into itself
        if((keyBind.index(inp)%2 + a_direc%2) == 1):
            #match the key with number, which represents direction
            a_direc = keyBind.index(inp)
