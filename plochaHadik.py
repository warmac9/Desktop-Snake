import os
import threading
import time
import random

icon_heigth = 8
icon_width = 6
tick_time = 3
keyBind = ["w", "d", "s", "a"]

pos = [0]
direc = [0]
a_direc = 0
score = 0
grow = 1
growInterval = 2

if(os.uname().sysname == "Darwin"):
    keyBind = ["w", "a", "s", "d"]
    tick_time = 1

t_bor = []
b_bor = []
l_bor = []
r_bor = []

def clean():
    i = 0
    go = 1
    while(go):
        path = ["", ".png", ".mp4"]
        rem = 0
        for o in path:
            if(os.path.isfile('joj'+str(i)+o)):
                os.remove("joj"+str(i)+o)
                rem = 1
        if(rem == 0):
            go = 0
        i += 1

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

def food():
    global icon_heigth, icon_width
    satisfied = False
    while not satisfied:
        r = random.randint(0, icon_heigth*icon_width)
        if(os.path.isfile('joj'+str(r))):
            os.rename("joj"+str(r), "joj"+str(r)+".mp4")
            satisfied = True

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
    p, d = pos[0], direc[0]
    if(grow != 2):
        dp, dd = pos.pop(), direc.pop()
    newPos = change_pos(p, d)
    check_food(newPos)
    if(grow == 2):
        grow = 0
    else:
        if(grow  == 1):
            grow = 2
        os.rename("joj"+str(dp)+".png", "joj"+str(dp))
    if(not os.path.isfile("joj"+str(newPos))):
        stop_interval("tick")
        clean()
        print("bum bac")
        print("score:"+str(score))
    os.rename("joj"+str(newPos), "joj"+str(newPos)+".png")
    direc.insert(0, a_direc)
    pos.insert(0, newPos)

clean()
init()
set_interval([tick_time, tick], "tick")
food()

while True:
    inp = input()
    if(inp in keyBind):
        if((keyBind.index(inp)%2 + a_direc%2) == 1):
            a_direc = keyBind.index(inp)
