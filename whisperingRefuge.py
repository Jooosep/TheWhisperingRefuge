import mysql.connector
import datetime
import random
from random import randrange
import time
import sys


db = mysql.connector.connect(host="localhost",
                             user="dbuser04",
                             passwd="dbpass",
                             db="TheWhisperingRefuge",
                             buffered=True)

cur=db.cursor()

#Area 1 on tiedemieskyla
#Area 2 on kannibaalikyla
#Area 3 on pikkusaari
#Area 4 on kirkon alue

#erityisestot on merkitaan numerolla terrain_square.restriction kolumnissa
#esto 1 on porttikoodi
#esto 2 on avainlukitus1
#esto 3 on avainlukitus2
#esto 4 on ikkuna
#esto 5 on rikkinainen riippusilta
#esto 6 on tiirikoitava ovi

NewAreaDescription = [0,"You have arrived at some sort of village, there are multiple small buildings, but no-ones around", " "," ","You see a small church building nearby, it is in very poor condition."]
KnownAreaDescription = [0,"You arrive at some kind of small village, you have been here before ","area description", " ", "You have returned to a familiar area, there is a small church building nearby"]
visitCounter = [0,0,0,0,0,0]


dt=datetime.datetime(1974,6,6,9,0)
square_side=50 #m
movement_multiplier=50
infection_time = dt
infected = True
infection_message=0
missingPlanks=7
gameOver=0
itemDropChange=0.5
enemySpawnRate=10 #%
spawnReduction=0
despawnCount=2
despawnCountX=0
objects =["FREEZER","CHEST","BRIEFCASE","DRAWER","SACK","CLOSET","BOAT"]
storables =["FREEZER","CHEST","BRIEFCASE","DRAWER","SACK","CLOSET"]
locked=["BRIEFCASE","DRAWER"]
buildings=[6,7,8,9,10,11]
boatMissing=["engine","fixhole","air"]
timer=dt
gateCode1=random.randrange(10,99)
gateCode2=random.randrange(100,999)
stringcode1= str(gateCode1)
stringcode2= str(gateCode2)
stringcode=stringcode2+stringcode1
gateCode=int(stringcode)
sql=("update item_type set description='Paper with writing on it but first part of the paper is torn: %s. Keep in mind that these codes are personal, and misuse is a crime.' where id=16")%(stringcode1)
cur.execute(sql)
sql=("update item_type set description='Paper with writing on it, the text says: This is your new security code for the Northwest gate: %s. Code remains incomplete as rest of the paper is torn.' where id=15")%(stringcode2)
cur.execute(sql)
#player max stats
player_carry_capasity=150
player_max_healt=100
player_max_fatique=100
player_max_speed=15
player_max_attack=100

player_position_x=None
player_position_y=None
def help():
    print('''    
HELP                                    -Displays all available commands
N, NORTH                                -Player moves north
S, SOUTH                                -Player moves south
E, EAST                                 -Player moves east
W, WEST                                 -player moves west
LOOK, L, WATCH, SEE                     -Tells player's current location
LOOK <compass point>                    -Tells player about the area of compass point 
I, INVENTORY, BAG, ITEMS                -Prints a list of items player is currently carrying
DROP <ITEM>                             -Drops the selected item
COMBINE <ITEM> <ITEM>                   -Combines two items to create a new one
COMBINE MENU                            -Displays all combine recipes
TIME                                    -Tells time to player
EQUIP <ITEM>                            -Player equips selected item for example equip shirt    
UNEQUIP <ITEM>                          -Player unequips selected item for example unequip shirt
EXAMINE, INSPECT, STUDY, ANALYZE        -Tells player info about the enemies
EXAMINE <AREA>/<ITEM>/<ENEMY>           -Tells player about the current area they are in
STATS, PLAYER, CHARACTER, CHAR          -Prints current stats of the player
EAT <ITEM>                              -Player eats selected item for example eat apple
SLEEP <how long> default=6h             -Player sleeps for selected time
TAKE, PICK, PICKUP, GRAB <ITEM>         -Player picks up the item and it is placed in inventory
KILL, ATTACK, ENGAGE, FIGHT, BATTLE     -These commands are used in combat to fight enemies
READ <ITEM>                             -Prints the discription of the item    
    ''')
def infect():
    global infected
    global infection_time
    sql="UPDATE player SET infection = 1"
    cur.execute(sql)
    infection_time = dt
    infected=True
    
def player_position():
    sql="SELECT player.x,player.y FROM player"
    cur.execute(sql)
    result=cur.fetchall()
    return result
    
def game_complete():
    global gameOver
    print("G",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print("a",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print("m",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print("e",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print(" ",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print("c",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print("o",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print("m",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print("p",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print("l",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print("e",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print("t",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print("e",end = "")
    sys.stdout.flush()
    gameOver=1
    time.sleep(2)
    
def game_over():
    global gameOver
    print("G",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print("A",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print("M",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print("E",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print(" ",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print("O",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print("V",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print("E",end = "")
    sys.stdout.flush()
    time.sleep(0.5)
    print("R",end = "")
    sys.stdout.flush()
    gameOver=1
    time.sleep(2)

    
def timedelay(howMany,delay):
    x="."
    for i in range(1,howMany+1):
        time.sleep(delay)
        print(x*i)    
def update_infection(*x):
    global infection_message
    global infection_time
    sql="select player.infection from player"
    cur.execute(sql)
    res=cur.fetchall()
    status=res[0][0]
    increase = 0
    if len(x)<1:
        if dt-infection_time>=datetime.timedelta(hours=12):
            increase=4
            sql="UPDATE player SET infection = infection+4"
            cur.execute(sql)
            infection_time=dt
        if dt-infection_time>=datetime.timedelta(hours=9):
            increase=3
            sql="UPDATE player SET infection = infection+3"
            cur.execute(sql)
            infection_time=dt
        if dt-infection_time>=datetime.timedelta(hours=6):
            increase=2
            sql="UPDATE player SET infection = infection+2"
            cur.execute(sql)
            infection_time=dt
        if dt-infection_time>=datetime.timedelta(hours=3):
            increase=1
            sql="UPDATE player SET infection = infection+1"
            cur.execute(sql)
            infection_time=dt
    else:
        increase=x[0]
        sql=(("UPDATE player SET infection = infection+%d")%increase)
        cur.execute(sql)
    if 25>status+increase>1 and infection_message==0:
        print("You aren't quite yourself today, perhaps this island is getting to you...")
        infection_message+=1
    elif 50>status+increase>25 and infection_message==1:
        print("You are starting to forget the simplest things, something is definitely wrong with you...")
        infection_message+=1
    elif 75>status+increase>50 and infection_message==2:
        print("Your mind is starting to betray you, it's like someone else is in control...")
        infection_message+=1
    elif 100>status+increase>75 and infection_message==3:
        print("You have forgotten your name and all of your past, all you have is a desire to gnaw on some raw flesh, you are on the verge of losing your humanity...")
        infection_message+=1
    elif status+increase>100:
        print("You have lost your body, mind and soul to this island, someone else has taken the reigns and you have no say what happens next... Game Over")
        
def read(item):
    sql="SELECT item_type.name, item.id,item_type.id FROM item,item_type,player,terrain_square WHERE item.type_id=item_type.id and player.x=terrain_square.x and player.y=terrain_square.y and item.x=terrain_square.x and item.y=terrain_square.y"
    cur.execute(sql)
    result=cur.fetchall()
    for i in range(len(result)):
        if result[i][0].upper() == item:
            item_id=result[i][2]
    sql = "Select item_type.text FROM item_type, item where item_type.ID = item.type_id and item.type_ID='"+ str(item_id) +"'"
    cur.execute(sql)
    res = cur.fetchall()
    print(res[0][0])

def check_item_type(item):
    item=item.upper()
    sql = ("SELECT item_type.name FROM item_type WHERE item_type.name LIKE '"+item.lower()+"%'")
    cur.execute(sql)
    result = cur.fetchall()
    for i in range(len(result)):
        if result[i][0].upper() == item:
            return True
    
    return False      

def player_carry_att_speed_hp_fatique():
    sql=("SELECT player.carry,player.att,player.speed,player.hp,player.fatigue FROM player")
    cur.execute(sql)
    result=cur.fetchall()
    return result
def out_of_breath():
    potency = random.randrange(1, 15)
    multiplier = 0.98 ** potency
    return multiplier

def inventory():
    sql = "SELECT item_type.name, COUNT(*) FROM item,item_type WHERE item.type_id=item_type.id and item.player_ID>0 GROUP BY item_type.name"
    cur.execute(sql)
    result = cur.fetchall()
    sql=(("SELECT item_type.name,item_type.part FROM item,item_type WHERE item.type_id=item_type.id and item.equipped>0 GROUP BY item_type.name"))
    cur.execute(sql)
    result2=cur.fetchall()
    sql="SELECT object.name FROM player,object WHERE object.player_id=player.id"
    cur.execute(sql)
    res=cur.fetchall()
    if len(result)>0 or len(res)>0 or len(result2)>0:
        print("You are carrying")
        if len(result)>0:
            for i in range(len(result)):
                print((result[i][0]+"(%s)")%(result[i][1]))
        if len(res)>0:
            for i in range(len(result)):
                print(result[i][0])
        if len(result2)>0:

            sql=(("SELECT item_type.name FROM item,item_type WHERE item.type_id=item_type.id and item.equipped>0 and item_type.part LIKE 'head%'"))
            cur.execute(sql)
            head=cur.fetchall()
            if len(head)>0:
                head=head[0][0]
            else:
                head=""
            sql=(("SELECT item_type.name FROM item,item_type WHERE item.type_id=item_type.id and item.equipped>0 and item_type.part LIKE 'body%'"))
            cur.execute(sql)
            body=cur.fetchall()
            if len(body)>0:
                body=body[0][0]
            else:
                body=""
            sql=(("SELECT item_type.name FROM item,item_type WHERE item.type_id=item_type.id and item.equipped>0 and item_type.part LIKE 'hand%'"))
            cur.execute(sql)
            hand=cur.fetchall()
            if len(hand)>0:
                hand=hand[0][0]
            else:
                hand=""
            sql=(("SELECT item_type.name FROM item,item_type WHERE item.type_id=item_type.id and item.equipped>0 and item_type.part LIKE 'leg%'"))
            cur.execute(sql)
            leg=cur.fetchall()
            if len(leg)>0:
                leg=leg[0][0]
            else:
                leg=""
            sql=(("SELECT item_type.name FROM item,item_type WHERE item.type_id=item_type.id and item.equipped>0 and item_type.part LIKE 'feet%'"))
            cur.execute(sql)
            feet=cur.fetchall()
            if len(feet)>0:
                feet=feet[0][0]
            else:
                feet=""
            print(''' ====Equipped====
|Head: %s     
|Body: %s   
|Hand: %s   
|Legs: %s
|Feet: %s   
================ 
            ''' % (head,body,hand,leg,feet))
            
    else:
        
        print("You don't carry any items with you")   
    
def refresh_spawnrate(reduce=0):
    global spawnReduction
    global enemySpawnRate
    if reduce == 0:
        if spawnReduction==0:
            return
        else:
            spawnReduction-=1
    else:
        enemySpawnRate = 0
        spawnReduction = reduce
        return
    if spawnReduction==0:
        enemySpawnRate=10
timeNOWhour=0

def change_spawnrate():
    global enemySpawnRate
    if dt.hour>=22 and dt.hour<23 or dt.hour>=0 and dt.hour<=7:
        enemySpawnRate=45
    else:
        enemySpawnRate=enemySpawnRate
        
def change_fatigue():
    global timeNOWhour
    
    if timeNOWhour!=dt.hour:
        totalspeed=(float(player_carry_att_speed_hp_fatique()[0][2])*(0.98**player_carry_att_speed_hp_fatique()[0][4]))
        update_player_speed(totalspeed)
        totalfatigue=player_carry_att_speed_hp_fatique()[0][4]+1
        update_player_fatique(totalfatigue)
    timeNOWhour=dt.hour                               
def add_time(distance,terrain_type_id):
    sql=("SELECT terrain_type.movement_difficulty FROM terrain_type WHERE terrain_type.id=%i" % terrain_type_id)
    cur.execute(sql)
    movement_dificulty=int(cur.fetchall()[0][0])
    
    sql=("SELECT player.speed FROM player")
    cur.execute(sql)
    speed=float(cur.fetchall()[0][0])
    #print(speed)
    multiplier=out_of_breath()
    x=speed*multiplier
    print(x)
    print(movement_multiplier*movement_dificulty)
    if (x/(movement_multiplier*movement_dificulty))<(1/150):
        time=distance/(1/150)
    else:
        time=int((distance/(x/(movement_multiplier*movement_dificulty))))
    tdelta=datetime.timedelta(seconds=time)
    global dt
    dt=(dt+tdelta)
    refresh_spawnrate()
    
def show_time():
    print(dt)
def update_player_weight(totalWeight):
    if totalWeight<=player_carry_capasity:
        sql=(("UPDATE player SET player.carry=%d WHERE player.ID=1") % totalWeight)
        cur.execute(sql)
    if totalWeight<0:
        sql=(("UPDATE player SET player.carry=0 WHERE player.ID=1"))
        cur.execute(sql)
def update_player_healt(totalHealt):
    if totalHealt<=player_max_healt and totalHealt>=0:
        sql=(("UPDATE player SET player.hp=%d WHERE player.ID=1") % totalHealt)
        cur.execute(sql)
    elif totalHealt<0:
        game_over()
    else:
        sql=(("UPDATE player SET player.hp=%d WHERE player.ID=1") % player_max_healt)
        cur.execute(sql)
def update_player_fatique(totalFatique):
    if totalFatique<=player_max_fatique:
        sql=(("UPDATE player SET player.fatigue=%d WHERE player.ID=1") % totalFatique)   
        cur.execute(sql)
    if totalFatique>=10:
        sql=(("UPDATE player SET player.fatigue=10 WHERE player.ID=1") )   
        cur.execute(sql)
def update_player_speed(totalSpeed):
    if totalSpeed<=player_max_speed:
        sql=(("UPDATE player SET player.speed=%d WHERE player.ID=1") % totalSpeed) 
        cur.execute(sql)
def update_player_attack(totalAttack):
    if totalAttack<=player_max_attack:
        sql=(("UPDATE player SET player.att=%d WHERE player.ID=1") % totalAttack)
        cur.execute(sql)
    if totalAttack<0:
        sql=(("UPDATE player SET player.att=0 WHERE player.ID=1"))
        cur.execute(sql)
def drop_item(item):
    sql=("SELECT item_type.name,item.id FROM item,item_type WHERE item.type_id=item_type.id and item.player_ID>0")
    cur.execute(sql)
    result=cur.fetchall()
    for i in range(len(result)):
        if result[i][0].upper()==item:
            
            item_id=result[i][1]
            sql=("SELECT item_type.weight FROM item,item_type WHERE item.type_id=item_type.id and item.id=%i" % item_id)
            cur.execute(sql)
            item_weight=cur.fetchall()[0][0]
            
            totalWeight=((player_carry_att_speed_hp_fatique()[0][0])-item_weight)
            update_player_weight(totalWeight)
            
            pos=player_position()
            sql=("UPDATE item SET item.x=%i, item.y=%i, item.player_ID=NULL WHERE item.id=%i" % (pos[0][0],pos[0][1],item_id))
            cur.execute(sql)
            
            print("You dropped the", result[i][0])
            break
    if result[i][0].upper()!=item:
        print("You don't have that kind of item in your inventory")      
def pick_up(item):
    
    sql="SELECT item_type.name, item.id FROM item,item_type,player,terrain_square WHERE item.type_id=item_type.id and player.x=terrain_square.x and player.y=terrain_square.y and item.x=terrain_square.x and item.y=terrain_square.y"
    cur.execute(sql)
    result=cur.fetchall()
    for i in range(len(result)):
        if result[i][0].upper()==item:
            item_id=result[i][1]
            
            sql=("SELECT item_type.weight FROM item,item_type WHERE item.type_id=item_type.id and item.id=%i" % item_id)
            cur.execute(sql)
            item_weight=cur.fetchall()[0][0]
            
            totalWeight=((player_carry_att_speed_hp_fatique()[0][0])+item_weight)
            if totalWeight<player_carry_capasity:
                sql=("UPDATE player SET player.carry=%d WHERE player.ID=1" % totalWeight)
                cur.execute(sql)
            
                sql=("UPDATE item SET item.x=NULL, item.y=NULL, item.player_ID=1 WHERE item.id=%i" % item_id)
                cur.execute(sql)
                print("You took", result[i][0])
            else:
                print("That would put too much weight on your back!")
            break
    
def split_line(text):
    words = text.split()
    return words

def look():
    sql = "Select terrain_type.description,terrain_type.id,terrain_square.restriction FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
    cur.execute(sql)
    result = cur.fetchall()
    current=result[0][1]
    print("Your current location is "+ result[0][0])
    sql ="Select terrain_type.name,terrain_type.id, terrain_square.restriction FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y+1"
    cur.execute(sql)
    res=cur.fetchall()
    if len(res)>0:
        if current not in buildings:
            if res[0][1] not in buildings:
                print("To the north there is a " + res[0][0])
            else:
                if "N" not in res[0][2] or "N6" in res[0][2]:
                    print("To the north there seems to be an entrance to a %s"%res[0][0])
                elif "N4" in res[0][2]:
                    print("To the north there is a %s, you notice a window on the wall facing you."%res[0][0])
                else:
                    print("To the north there is a %s, you don't see an entrance."%res[0][0])
        else:
            if res[0][1] not in buildings:
                if "S" not in result[0][2] or "S6" in result[0][2]:
                    print("To the north there's a door exiting the building")
                elif "S4" in result[0][2]:
                    print("To the north you see a %s through the window."%res[0][0])
                else:
                    print("To the north there's the inside wall of the building.")
            else:
                if "N" in res[0][2]:
                    print("To the north you see a door, it must lead to another room.")
                else:
                    print("To the north there is another room")
            
    else:
        print("To the north is the Atlantic")
        
    sql ="Select terrain_type.name,terrain_type.id, terrain_square.restriction FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y-1"
    cur.execute(sql)
    res=cur.fetchall()
    if len(res)>0:
        if current not in buildings:
            if res[0][1] not in buildings:
                print("To the south there is a " + res[0][0])
            else:
                if "S" not in res[0][2] or "S6" in res[0][2]:
                    print("To the north there seems to be an entrance to a %s"%res[0][0])
                elif "S4" in res[0][2]:
                    print("To the north there is a %s, you notice a window on the wall facing you."%res[0][0])
                else:
                    print("To the north there is a %s, you don't see an entrance."%res[0][0])
        else:
            if res[0][1] not in buildings:
                if "N" not in result[0][2] or "N6" in result[0][2]:
                    print("To the south there's a door exiting the building")
                elif "N4" in result[0][2]:
                    print("To the south you see a %s through the window."%res[0][0])
                else:
                    print("To the south there's the inside wall of the building.")
            else:
                if "S" in res[0][2]:
                    print("To the south you see a door, it must lead to another room.")
                else:
                    print("To the south there is another room")
            
    else:
        print("To the south is the Atlantic")
        
    sql ="Select terrain_type.name,terrain_type.id, terrain_square.restriction FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x+1"
    cur.execute(sql)
    res=cur.fetchall()
    if len(res)>0:
        if current not in buildings:
            if res[0][1] not in buildings:
                print("To the east there is a " + res[0][0])
            else:
                if "E" not in res[0][2] or "E6" in res[0][2]:
                    print("To the east there seems to be an entrance to a %s"%res[0][0])
                elif "E4" in res[0][2]:
                    print("To the east there is a %s, you notice a window on the wall facing you."%res[0][0])
                else:
                    print("To the east there is a %s, you don't see an entrance."%res[0][0])
        else:
            if res[0][1] not in buildings:
                if "W" not in result[0][2] or "W6" in result[0][2]:
                    print("To the east there's a door exiting the building")
                elif "W4" in result[0][2]:
                    print("To the east you see a %s through the window."%res[0][0])
                else:
                    print("To the east there's the inside wall of the building.")
            else:
                if "W" in res[0][2]:
                    print("To the east you see a door, it must lead to another room.")
                else:
                    print("To the east there is another room")
            
    else:
        print("To the east is the Atlantic")
        
    sql ="Select terrain_type.name,terrain_type.id, terrain_square.restriction FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x-1"
    cur.execute(sql)
    res=cur.fetchall()
    if len(res)>0:
        if current not in buildings:
            if res[0][1] not in buildings:
                print("To the west there is a " + res[0][0])
            else:
                if "W" not in res[0][2] or "W6" in res[0][2]:
                    print("To the west there seems to be an entrance to a %s"%res[0][0])
                elif "W4" in res[0][2]:
                    print("To the west there is a %s, you notice a window on the wall facing you."%res[0][0])
                else:
                    print("To the west there is a %s, you don't see an entrance."%res[0][0])
        else:
            if res[0][1] not in buildings:
                if "E" not in result[0][2] or "E6" in result[0][2]:
                    print("To the west there's a door exiting the building")
                elif "E4" in result[0][2]:
                    print("To the west you see a %s through the window."%res[0][0])
                else:
                    print("To the west there's the inside wall of the building.")
            else:
                if "E" in res[0][2]:
                    print("To the north you see a door, it must lead to another room.")
                else:
                    print("To the north there is another room")
            
    else:
        print("To the north is the Atlantic")
 
def retrieve(useable,item):
    sql=(("SELECT item_type.name, item.id FROM item,item_type,player,object WHERE item.type_id=item_type.id and player.x=object.x and player.y=object.y and item.object_ID=object.id and object.name='%s'")%(useable))
    cur.execute(sql)
    result=cur.fetchall()
    if object_is_here(useable)==False:
        print(("There's no %s here!")%(useable.lower()))
        return
    elif object_is_open(useable)==False:
        print(("The %s is closed!")%(useable.lower()))
        return
    elif check_object(useable,item):
        for i in range(len(result)):
            if result[i][0]==item:
                item_id=result[i][1]
                
                sql=("SELECT item_type.weight FROM item,item_type WHERE item.type_id=item_type.id and item.id=%i" % item_id)
                cur.execute(sql)
                item_weight=cur.fetchall()[0][0]
                
                totalWeight=((player_carry_att_speed_hp_fatique()[0][0])+item_weight)
                if totalWeight<player_carry_capasity:
                    sql=("UPDATE player SET player.carry=%d WHERE player.ID=1" % totalWeight)
                    cur.execute(sql)
                
                    sql=("UPDATE item SET item.object_id=NULL, item.player_ID=1 WHERE item.id=%i" % item_id)
                    cur.execute(sql)
                    print("You took", result[i][0])
                else:
                    print("You can't get more weight to your poor back!")
                    return
    else: 
        print("There's no such item there!")
        
def store(useable,item):
    sql=(("SELECT item_type.name, item.id FROM item,item_type,player,object WHERE item.type_id=item_type.id and player.x=object.x and player.y=object.y and item.object_ID=object.id and object.name='%s'")%(useable))
    cur.execute(sql)
    result=cur.fetchall()
    if object_is_here(useable)==False:
        print(("There's no %s here!")%(useable.lower()))
    elif object_is_open(useable)==False:
        print(("The %s is closed!")%(useable.lower()))
    else:
        sql=(("SELECT item_type.name,item.id,object.id FROM object,item,item_type WHERE item.type_id=item_type.id and item.player_ID>0 and object.name='%s'")%(useable.lower()))
        cur.execute(sql)
        result=cur.fetchall()
        obj_id = result[0][2]
        for i in range(len(result)):
            if result[i][0].upper()==item:
                
                item_id=result[i][1]
                sql=("SELECT item_type.weight FROM item,item_type WHERE item.type_id=item_type.id and item.id=%i" % item_id)
                cur.execute(sql)
                item_weight=cur.fetchall()[0][0]
                
                totalWeight=((player_carry_att_speed_hp_fatique()[0][0])-item_weight)
                update_player_weight(totalWeight)
                
                sql=(("UPDATE item SET item.object_id=%i, item.player_ID=NULL WHERE item.id=%i") %(obj_id,item_id))
                cur.execute(sql)
                
                print(("you stored the %s")%(result[i][0]))
                break
        print("You don't even have that")
        
def npc_check():
    sql="select npc.id from npc, player where npc.x=player.x and npc.y=player.y" 
    cur.execute(sql)
    res=cur.fetchall()
    if len(res)>0:
        return res[0][0]   
    else:
        return 0
       
def talk(ID):
    print("What will you ask?")
    if ID==1:
        while True:
            print("\t1) Who are you?")
            print("\t2) What are you working on here?")
            print("\t3) What the hell are you doing here?")
            print("\t4) Can I help you?")
            print()
            ans=input()
            if ans=="1":
                print("\"Who am I!? I am Robert Zuul, one of the greatest scientists of our time. I work here in secrecy, but the whole world might one day face my creation, MUHAHAHAHAAAAHAHA!\"")
                print()
                return
            elif ans=="2":
                print("\"I am working on some microparasites here my friend, in fact some might be in you right now if you haven't been careful with what you've been eating here, MUHAHAHHAHAHAHAHAA!\"")
                print()
                return
            elif ans=="3":
                print("\"You intrude in my laboratory and disrespect me!? I will murder you!\"")
                print()
                print("Oh oh, the mad scientist is charging at you with some acid!")
                sql="update npc set x=NULL where id=1"
                cur.execute(sql)
                sql="insert into enemy values(10000,12,-10,-6,NULL)"
                cur.execute(sql)
                time.sleep(2)
                attack()
                return
            elif ans=="4":
                print("\"Yes, BY GETTING THE HELL OUT OF MY LABORATORY!\"")
                print()
                return
            else:
                print("You must choose one of the options.")
                
def object_is_open(useable):
    sql=(("select object.open from object where object.name='%s'")%(useable.lower()))
    cur.execute(sql)
    res = cur.fetchall()
    if res[0][0]==1:
        return True
    else:
        return False
    
def object_is_here(useable):
    sql=(("select object.name from object,player where object.name='%s' and (player.ID=object.player_id or (object.x=player.x and object.y=player.y))" )%(useable.lower()))
    cur.execute(sql)
    res = cur.fetchall()
    if len(res)>0:
        return True
    else:
        return False
    
def mangleWithObjects(command,useable):
    global locked
    sql=(("select id, name, x, y,key_item_id,open from object where name='%s'")% useable)
    cur.execute(sql)
    res=cur.fetchall()
    if object_is_here(useable):
        if res[0][0]==1:
            if command[0] == "OPEN":
                if res[0][5]==0:
                    sql="Update object set open=1 where id=1"
                    cur.execute(sql)
                    print("You opened the %s."%useable)
                    check_object("freezer")
                else:
                    print("Looks like its already open!")
            elif command[0] == "CLOSE":
                if res[0][5]==1:
                    sql="Update object set open=0 where id=1"
                    cur.execute(sql)
                    print("You closed the %s."%useable)
                else:
                    print("It seems to be closed already!")
            else:
                print("Your asking for too much here!")
                
        elif res[0][0]==2:
            if command[0] == "OPEN":
                if res[0][5]==0:
                    sql="Update object set open=1 where id=2"
                    cur.execute(sql)
                    print("You opened the %s."%useable)
                    check_object("chest")
                else:
                    print("Looks like its already open!")
            elif command[0] == "CLOSE":
                if res[0][5]==1:
                    sql="Update object set open=0 where id=2"
                    cur.execute(sql)
                    print("You closed the %s."%useable)
                else:
                    print("It seems to be closed already!")
            else:
                print("Your asking for too much here!")
                
        elif res[0][0]==3:
            if command[0] == "OPEN":
                if "BRIEFCASE" in locked:
                    print("It's locked, a lockpick might do it")
                elif res[0][5]==0:
                    sql="Update object set open=1 where id=3"
                    cur.execute(sql)
                    print("You opened the %s."%useable)
                else:
                    print("Looks like its already open!")
            elif command[0] == "CLOSE":
                if res[0][5]==1:
                    sql="Update object set open=0 where id=3"
                    cur.execute(sql)
                    print("You closed the %s."%useable)
                else:
                    print("It seems to be closed already!")
            elif "BRIEFCASE" in locked and command[0] == "USE":
                if command[1]== "LOCKPICK":
                    print("Hey, it took you a while but you managed to open it!")
                    locked.remove("BRIEFCASE")
                    print(locked)
                    sql="Update object set open=1 where id=3"
                    cur.execute(sql)
                    check_object("briefcase")
                    
            elif command[0] == "TAKE":
                totalWeight=((player_carry_att_speed_hp_fatique()[0][0])+20)
                if totalWeight<player_carry_capasity:
                    sql=("UPDATE player SET player.carry=%d WHERE player.ID=1" % totalWeight)
                    cur.execute(sql)
                
                    sql=("UPDATE item SET object.x=NULL, object.y=NULL, object.player_ID=1 WHERE object.id=3")
                    cur.execute(sql)
                    print("You took the briefcase with you!")
                else:
                    print("That's too much weight on your back!!")
                    
            elif command[0] == "DROP":
                totalWeight=((player_carry_att_speed_hp_fatique()[0][0])-20)
                sql=("UPDATE player SET player.carry=%d WHERE player.ID=1" % totalWeight)
                cur.execute(sql)
                
                sql=(("UPDATE item SET object.x=%i, object.y=%i, object.player_ID=NULL WHERE object.id=3")%(player_position[0][0],player_position[0][1]))
                cur.execute(sql)
                print("You left the briefcase.")

            else:
                print("Your asking for too much here!")
                
        elif res[0][0]==4:
            if command[0] == "OPEN":
                if "DRAWER" in locked:
                    print("It's jammed shut, maybe you could open it with some force")
                elif res[0][5]==0:
                    sql="Update object set open=1 where id=4"
                    cur.execute(sql)
                    print("You opened the %s."%useable)
                    check_object("drawer")
                else:
                    print("Looks like its already open!")
            elif command[0] == "CLOSE":
                if res[0][5]==1:
                    sql="Update object set open=0 where id=4"
                    cur.execute(sql)
                    print("You closed the %s."%useable)
                else:
                    print("It seems to be closed already!")
            elif "DRAWER" in locked and (command[0] == "HIT" or command[0]=="KICK" or command[0]=="STRIKE" or command[0]=="PUNCH"):
                print("Hey, that did it!")
                locked.remove("DRAWER")
                sql="Update object set open=1 where id=4"
                cur.execute(sql)
                check_object("drawer")
            else:
                print("Your asking for too much here!")
                
        elif res[0][0]==6:
            if command[0] == "OPEN":
                if res[0][5]==0:
                    sql="Update object set open=1 where id=6"
                    cur.execute(sql)
                    print("You opened the %s."%useable)
                    check_object("closet")
                else:
                    print("Looks like its already open!")
            elif command[0] == "CLOSE":
                if res[0][5]==1:
                    sql="Update object set open=0 where id=1"
                    cur.execute(sql)
                    print("You closed the %s."%useable)
                else:
                    print("It seems to be closed already!")
            else:
                print("Your asking for too much here!")
        elif res[0][0]==8:
            if command[0] == "OPEN":
                if res[0][5]==0:
                    sql="Update object set open=1 where id=8"
                    cur.execute(sql)
                    print("You opened the %s."%useable)
                    check_object("closet")
                else:
                    print("Looks like its already open!")
            elif command[0] == "CLOSE":
                if res[0][5]==1:
                    sql="Update object set open=0 where id=8"
                    cur.execute(sql)
                    print("You closed the %s."%useable)
                else:
                    print("It seems to be closed already!")
            else:
                print("Your asking for too much here!")
        elif res[0][0]==7:
            print(command)
            if command[0] == "JUMP" or command[0] == "GET" or command[0] == "STEP":
                if len(boatMissing)<1:
                    while True:
                        ans=input("Time to get out of this hellhole no?(y/n)")
                        if ans=="n":
                            timedelay(3,0.5)
                            print("You jump out of the boat!")
                            return
                        elif ans!="y":
                            print("Input \"y\" or \"n\"!")
                        else:
                            print("You start the engine and drive into the sunset not looking back.")
                            game_complete()
                            return
                else:
                    print("The boat is not repaired yet!")
            elif command[0]=="FIX"or command[0]=="REPAIR" or command[0]=="ADD":
                fix_boat()
            else:
                print("Can't do that")
    else:
        print("There is no %s here..."%useable.lower())
        
def window_enter(res,compasspoint):
    print("You can't simply break through the window, it seems to be toughened glass.")
    print("You will need to use some type of proper tool.")
    answer1=input("Will you attempt to get in through the window?(y/n)")  
    if answer1 == "y":
        answer2=input("What will you do to get in?")
        while True:
            if quickParse(answer2)[0]=="USE":
                if quickParse(answer2)[1]=="GLASSCUTTER" or (quickParse(answer2)[1]=="GLASS" and quickParse(answer2)[2]=="CUTTER"):
                    if specific_item_check("glass cutter"):
                        timedelay(3, 0.7)
                        
                        print("You manage to cut a sizeable hole into the window and proceed to slip in.")
                        if compasspoint=="N":
                            filtered=''.join([c for c in res[0][1] if c not in compasspoint and"4"])
                            sql=(("Update terrain_square set restriction='%s' where terrain_square.x=%i and terrain_square.y=%i")%(filtered,player_position()[0][0],(player_position()[0][1])+1))
                            cur.execute(sql)
                            add_time(square_side, res[0][0])
                            sql= "UPDATE player SET player.y = player.y+1"
                            cur.execute(sql)
                            
                        elif compasspoint=="S":
                            filtered=''.join([c for c in res[0][1] if c not in compasspoint and"4"])
                            sql=(("Update terrain_square set restriction='%s' where terrain_square.x=%i and terrain_square.y=%i")%(filtered,player_position()[0][0],(player_position()[0][1])-1))
                            cur.execute(sql)
                            add_time(square_side, res[0][0])
                            sql= "UPDATE player SET player.y = player.y-1"
                            cur.execute(sql)
                            
                        elif compasspoint=="W":  
                            filtered=''.join([c for c in res[0][1] if c not in compasspoint and"4"])
                            sql=(("Update terrain_square set restriction='%s' where terrain_square.x=%i and terrain_square.y=%i")%(filtered,(player_position()[0][0]-1),player_position()[0][1]))
                            cur.execute(sql)
                            add_time(square_side, res[0][0])
                            sql= "UPDATE player SET player.x = player.x-1"
                            cur.execute(sql)
                        
                        elif compasspoint=="E":  
                            filtered=''.join([c for c in res[0][1] if c not in compasspoint and"4"])
                            sql=(("Update terrain_square set restriction='%s' where terrain_square.x=%i and terrain_square.y=%i")%(filtered,((player_position()[0][0])+1),player_position()[0][1]))
                            cur.execute(sql)
                            add_time(square_side, res[0][0])
                            sql= "UPDATE player SET player.x = player.x+1"
                            cur.execute(sql)
                              
                        sql="select terrain_type.name,terrain_square.description,terrain_square.visitcounter,terrain_square.1stvisit,terrain_square.x,terrain_square.y from terrain_type, terrain_square, player where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
                        cur.execute(sql)
                        res=cur.fetchall()
                        currentSquare = res[0][0]
                        print("You entered a " + currentSquare)
                        if res[0][2]==0:
                            sql=(("UPDATE terrain_square set visitcounter=visitcounter+1 where x=%i and y=%i")%(res[0][4],res[0][5]))
                            cur.execute(sql)
                            print(res[0][3])
                        elif res[0][1]!= None:
                            print(res[0][1])
                        if infected:
                            update_infection()
                        return
                    else:
                        print("You don't have a glass cutter")                                        
            else:
                print("That didn't work")
            while True:
                answer3 = input("Try something else?(y/n)")
                if answer3=="n":
                    return
                elif answer3!="y":
                    print("Input \"y\" or \"n\"!")
                else:
                    break
    elif answer1=="n":
        return
    else:
        print("Input \"y\" or \"n\"!")
        
def open_lockpickable(res,compasspoint):
    print("The door is locked")
    while True:
        answer1=input("Will you attempt to open it?(y/n)")
        if answer1 == "y":
            while True:
                answer2=input("what do you want to try?")
                if quickParse(answer2)[0]=="USE":
                    if quickParse(answer2)[1]=="LOCKPICK":
                        if specific_item_check("lockpick"):
                            rand=randrange(0,10)
                            if rand>2:
                                timedelay(3, 0.5)
                                print("It took you a while but you picked the lock, the door is now open!")
                                if compasspoint=="N":
                                    filtered=''.join([c for c in res[0][1] if c not in compasspoint and"6"])
                                    sql=(("Update terrain_square set restriction='%s' where terrain_square.x=%i and terrain_square.y=%i")%(filtered,player_position()[0][0],(player_position()[0][1])+1))
                                    cur.execute(sql)
                                    
                                elif compasspoint=="S":
                                    filtered=''.join([c for c in res[0][1] if c not in compasspoint and"6"])
                                    sql=(("Update terrain_square set restriction='%s' where terrain_square.x=%i and terrain_square.y=%i")%(filtered,player_position()[0][0],(player_position()[0][1])-1))
                                    cur.execute(sql)
                                    
                                elif compasspoint=="W":  
                                    filtered=''.join([c for c in res[0][1] if c not in compasspoint and"6"])
                                    sql=(("Update terrain_square set restriction='%s' where terrain_square.x=%i and terrain_square.y=%i")%(filtered,(player_position()[0][0]-1),player_position()[0][1]))
                                    cur.execute(sql)
                                
                                elif compasspoint=="E":  
                                    filtered=''.join([c for c in res[0][1] if c not in compasspoint and"6"])
                                    sql=(("Update terrain_square set restriction='%s' where terrain_square.x=%i and terrain_square.y=%i")%(filtered,((player_position()[0][0])+1),player_position()[0][1]))
                                    cur.execute(sql)
                                return
                            else:
                                print("Oh shoot, you broke the lockpick!")
                                item_delete("lockpick")
                        else:
                            print("You don't have any lockpicks!")                                        
                    elif quickParse(answer2)[1]=="OLD" and quickParse(answer2)[2]=="KEY":
                        if specific_item_check("old key"):
                            print("That's not the right key!")
                        else:
                            print("you don't have such a key!")
                    elif quickParse(answer2)[1]=="TITANIUM" and quickParse(answer2)[2]=="KEY":
                        if specific_item_check("titanium key"):
                            print("That key didn't fit in the keyhole!")
                        else:
                            print("you don't have such a key!")
                    elif quickParse(answer2)[1]=="KEY":
                        print("You have to be more specific.")
                    else:
                        print("That didn't work")
                    while True:
                        answer3 = input("The door remains closed, want to try something else?(y/n)")
                        if answer3=="n":
                            return
                        elif answer3!="y":
                            print("Input \"y\" or \"n\"!")
                        else:
                            break
        elif answer1=="n":
            return
        else:
            print("Input \"y\" or \"n\"!")
def open_gate(res):
    global gateCode
    global timer
    false=0
    if timer>dt:
        print("The codepad is not working")
    else:
        print("The gate is locked, on the pillar there seems to a codepad with numbers, you could try entering a code.")
        while True:
            ans=input("Will you enter something?(y/n)")
            if ans=="y":
                ans2=input("ENTER CODE: ")
                if ans2==str(gateCode):
                    timedelay(4,0.5)
                    print("It was the right code, the gate opens slowly!")
                    filtered=''.join([c for c in res[0][1] if c not in "W" and "1"])
                    sql=(("Update terrain_square set restriction='%s' where terrain_square.x=%i and terrain_square.y=%i")%(filtered,(player_position()[0][0]-1),player_position()[0][1]))
                    cur.execute(sql)
                    return
                else:
                    timedelay(3,0.7)
                    print("The gate didn't open and a red light beeped on the codepad!")
                    false+=1
                if false >2:
                    print("The red light stayed on this time, and the codepad is not responsive!")
                    timer=dt+datetime.timedelta(hours=3)
                    return
            if ans=="n":
                print("You left the gate alone.")
                return
            else:
                print("Input y or n!")
        
def open_door1():
    print("The door is locked")
    while True:
        answer1=input("Will you attempt to open it?(y/n)")
        if answer1 == "y":
            while True:
                answer2=input("what do you want to try?")
                if quickParse(answer2)[0]=="USE":
                    if quickParse(answer2)[1]=="LOCKPICK":
                        if specific_item_check("lockpick"):
                            timedelay(4,0.5)
                            print("This lock is surprisingly tough to pick, you can't manage!")
                        else:
                            print("You don't have any lockpicks!")                                        
                    elif quickParse(answer2)[1]=="OLD" and quickParse(answer2)[2]=="KEY":
                        if specific_item_check("old key"):
                            print("This key is way too big for the keyhole, and old... this is a modern lock!")
                        else:
                            print("you don't have such a key!")
                    elif quickParse(answer2)[1]=="TITANIUM" and quickParse(answer2)[2]=="KEY":
                        if specific_item_check("titanium key"):
                            print("That was the right key, you proceed to open the door!")
                            sql="Update terrain_square set restriction='WES' where terrain_square.x=-12 and terrain_square.y=8"
                            cur.execute(sql)
                            return
                        else:
                            print("you don't have such a key!")
                    elif quickParse(answer2)[1]=="KEY":
                        print("You have to be more specific.")
                    else:
                        timedelay(4,0.5)
                        print("That didn't work")
                    while True:
                        answer3 = input("The door remains closed, want to try something else?(y/n)")
                        if answer3=="n":
                            return
                        elif answer3!="y":
                            print("Input \"y\" or \"n\"!")
                        else:
                            break
        elif answer1=="n":
            return
        else:
            print("Input \"y\" or \"n\"!")
            
#def open_gate():
    
def open_door2():
    print("The door is closed with a big padlock")
    while True:
        answer1=input("Will you attempt to open it?(y/n)")
        if answer1 == "y":
            while True:
                answer2=input("what do you want to try?")
                if quickParse(answer2)[0]=="USE":
                    if quickParse(answer2)[1]=="LOCKPICK":
                        if specific_item_check("lockpick"):
                            timedelay(4,0.5)
                            print("This lock is surprisingly tough to pick, you can't manage!")
                        else:
                            print("You don't have any lockpicks!")                                        
                    elif quickParse(answer2)[1]=="OLD" and quickParse(answer2)[2]=="KEY":
                        if specific_item_check("old key"):
                            timedelay(4,0.5)
                            print("That was the right key, you proceed to open the door!")
                            sql="Update terrain_square set restriction='NWS' where terrain_square.x=-9 and terrain_square.y=4"
                            cur.execute(sql)
                            return
                        else:
                            print("you don't have such a key!")
                    elif quickParse(answer2)[1]=="TITANIUM" and quickParse(answer2)[2]=="KEY":
                        if specific_item_check("titanium key"):
                            timedelay(4,0.5)
                            print("That key didn't fit in the padlock!")
                        else:
                            print("you don't have such a key!")
                    elif quickParse(answer2)[1]=="KEY":
                        print("You have to be more specific.")
                    else:
                        timedelay(4,0.5)
                        print("That didn't work")
                    while True:
                        answer3 = input("The door remains closed, want to try something else?(y/n)")
                        if answer3=="n":
                            return
                        elif answer3!="y":
                            print("Input \"y\" or \"n\"!")
                        else:
                            break
        elif answer1=="n":
            return
        else:
            print("Input \"y\" or \"n\"!")
            
def fix_bridge(amount=4):
    global missingPlanks
    amountToFix=missingPlanks-3
    if amount>=count_item("plank"):
        planks=count_item("plank") 
    else: 
        planks=amount
    if player_position()[0][0]==-6 and player_position()[0][1]==7:
        if missingPlanks==0:
            print("The bridge is already intact.")
        else:
            if not specific_item_check("plank"):
                print("You lack the materials!")
            elif not specific_item_check("hammer"):
                print("You need a hammer to make those planks stick")
            elif not specific_item_check("box of nails"):
                print("You need some nails to hammer the planks in")
            else:
                planksNailed=0
                if amountToFix>0:
                    if amountToFix-planks<0:
                        planksNailed=amountToFix
                    else:
                        planksNailed=planks
                else:
                    if missingPlanks-planks<0:
                        planksNailed=missingPlanks
                    else:
                        planksNailed=planks
                missingPlanks-=planksNailed
                item_delete("plank",planksNailed)
                amountToFix=missingPlanks-3
                timedelay(4,0.5)
                print("You nail in a plank.") if planksNailed==1 else print("You nail in %i planks"%planksNailed)
                if amountToFix==0:
                    sql="Update terrain_square set restriction='U' where x=-7 and y=7"
                    cur.execute(sql)
                    print("The gap is now small enough that you can safely cross the bridge.")   
                elif amountToFix>0:
                    print("But there's still too big of a gap.")
                if missingPlanks==0:
                    print("The bridge is now complete.")
    else:
        print("You can't do that here")
    
def fix_boat():
    global boatMissing
    while True:
        if "fixhole" in boatMissing:
            print("The boat is riddled with some holes, you can't inflate it, before you fix those.")
        if "fixhole" not in boatMissing and "air" in boatMissing:
            print("The boat is void of air, you need to inflate it.")
        if "engine" in boatMissing:
            print("You need to hook an engine on this boat to get anywhere.")
        ans=input("What will you use/fix/add on the boat?")
        if quickParse(ans)[0]=="FIX":
            if quickParse(ans)[1]=="HOLES":
                if specific_item_check("duct tape"):
                    print("You fix the holes with some duct tape")
                    boatMissing.remove("fixhole")
                else:
                    print("You don't have the duct tape needed to do this")
            else:
                print("The only thing to fix are the holes.")
        elif quickParse(ans)[0]=="ADD" or quickParse(ans)[0]=="PUT":
            if quickParse(ans)[1]=="ENGINE":
                if specific_item_check("engine"):
                    if specific_item_check("superglue"):
                        timedelay(3, 0.7)
                        print("You make the engine stick with some superglue, nicely done!")
                        item_delete("engine")
                        boatMissing.remove("engine")
                    else:
                        print("Your boat got badly damaged at sea, you need to use some quality glue to add the engine.")
                else:
                    print("You don't have an engine.")
            else:
                print("You can't do that.")
        elif quickParse(ans)[0]=="PUMP":
            if specific_item_check("small pump") and "fixhole" not in boatMissing:
                timedelay(3, 0.7)
                print("You fill the boat with air, nicely done!")
                boatMissing.remove("air")
            elif "fixhole" in boatMissing:
                print("You can't inflate the boat before fixing the holes.")
            else:
                print("You don't have a pump.")
        elif quickParse(ans)[0]=="USE":
            if quickParse(ans)[1]=="PUMP":
                if specific_item_check("small pump") and "fixhole" not in boatMissing:
                    timedelay(3, 0.7)
                    print("You fill the boat with air, nicely done!")
                    boatMissing.remove("air")
                elif "fixhole" in boatMissing:
                    print("You can't inflate the boat before fixing the holes.")
                else:
                    print("You don't have a pump.")
            else:
                print("You can't do that.")
        else:
            print("You can't do that.")
        if len(boatMissing)>0:
            while True:
                ans2=input("Will you continue repairing the boat?(y/n)")
                if ans2=="n":
                    return
                elif ans2!="y":
                    print("Input \"y\" or \"n\"!")
                else:
                    break
        else:
            print("The boat is now in working condition!")
            return
def group_of_cannibals():
    timedelay(4,0.5)
    print("You approach the group of wild men feasting on the cow, but they take notice of you and attack you, you struggle but they are too many, you're dead!")
    game_over()
    return
    
def pack_of_dogs():
    dogsLeft=5
    timedelay(3,0.7)
    print("You approach the pack of feral dogs and they turn to you growling viciously.")
    time.sleep(1)
    timedelay(3,0.7)
    print("The dog in the forefront is inching closer and closer, if it attacks you, the others will as well.")
    time.sleep(1)
    timedelay(3,0.7)
    while True:
        ans= input("This would be the time to be giving! What will you do?") 
        if quickParse(ans)[0]=="GIVE" or quickParse(ans)[0]=="DROP" or quickParse(ans)[0]=="THROW" or quickParse(ans)[0]=="OFFER":
            if "MEAT" in quickParse(ans):
                if approximate_item_check("meat"):
                    timedelay(3,0.7)
                    print("You throw the dog some of your meat and he leaves to eat it.")
                    time.sleep(1)
                    dogsLeft-=1
                    meat=return_approximate_item("meat")
                    item_delete(meat)
                else:
                    timedelay(3,0.7)
                    print("Sadly you forgot to bring the meat, although the dogs thought you certainly delivered :). You're dead.")
                    game_over()
                    return
            else:
                timedelay(3,0.7)
                print("That didn't satisfy the dog, so it feasted on your meat :)")
                game_over()
                return
        elif quickParse(ans)[0]=="RUN" or quickParse(ans)[0]=="LEAVE":
            timedelay(3,0.7)
            print("One does not simply run away from a pack of hungry dogs. You're dead!")
            game_over()
            return
        else:
            timedelay(3,0.7)
            print("Didn't quite get what you meant, but the dogs sure understood it as \"TIME TO FEED!\":). You're dead")
            game_over()
            return
        if dogsLeft>0:
            print("There are %i hungry dogs left" %dogsLeft) if dogsLeft>1 else print("There's only one dog left, and it is most certainly the cutest.")
            time.sleep(1)
            timedelay(3,0.7)
            print("The next dog steps closer asking for a meal, if it attacks you, the others will as well")if dogsLeft>1 else print("It steps forward humbly as the last one, but nevertheless with great expectations.")
            time.sleep(1)
        else:
            timedelay(3,0.7)
            print("Whew, that was nerve-racking, anyway, the dogs won't bother you for a while.")  
            sql="Update terrain_square set restriction='U' where x=2 and y=-1"
            cur.execute(sql)  
            sql="Update terrain_square set description=NULL where y=-1 and (x=3 or x=1)"
            cur.execute(sql)  
            return
def norlax_has_awakened():
    print("You approach the sleeping giant")
    timedelay(3, 0.6)
    print("He seems to sleep very deeply.")
    while True:
        ans=input("What will you do?")
        if quickParse(ans)[0]=="ATTACK" or quickParse(ans)[0]=="FIGHT" or quickParse(ans)[0]=="HIT":
            timedelay(3,0.6)
            print("The man awakened and sent you flying, but you couldn't fly, so you died.")
            game_over()
            return
        elif quickParse(ans)[0]=="PLAY":
            if quickParse(ans)[1]=="GUITAR":
                timedelay(3,0.6)
                print("You play quite loudly but the big man doesn't wake up")
            elif quickParse(ans)[1]=="FLUTE":
                timedelay(3,0.6)
                print("You play a beautiful tune and the big man wakes up in bliss and greets you")
                sql="update terrain_square set restriction=NW4S where x=11 and y=-2"
                cur.execute(sql)
                sql="update terrain_square set description='The big man is in front of his house enjoying the sun' where x=10 and y=-2"
                cur.execute(sql)
                sql="update npc set x=10,y=-2 where id=2"
                cur.execute(sql)
                return
            else:
                print("That had no effect.")
        elif quickParse(ans)[0]=="TALK" or quickParse(ans)[0]=="YELL" or quickParse(ans)[0]=="SCREAM" or quickParse(ans)[0]=="SHOUT":
            print("He is in deep sleep, hibernating perhaps, and can't hear you.")
        elif quickParse(ans)[0]=="USE":
            print("That had no effect.")
        elif quickParse(ans)[0]=="LEAVE" or quickParse(ans)[0]=="WALK" or quickParse(ans)[0]=="RUN":
            print("You left him alone")
            return
        else:
            print("That didn't seem to work.")
        while True:
            ans2= input("Will you try something else?(y/n)")
            if ans2=="y":
                break
            elif ans2=="n":
                return
            else:
                print("input y or n ")
            
def move_north():
    global visitCounter
    sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
    cur.execute(sql)
    res=cur.fetchall()
    oldAreaCode=res[0][2]
    if "S" in res[0][1]:
        print("You can't go through the wall")
    else:
        sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y+1"
        cur.execute(sql)
        res=cur.fetchall()
        if len(res)>0:
            newAreaCode = res[0][2]
            if res[0][0]==5:
                print("The forest is too thick, you cannot pass!")
            elif "N" in res[0][1]:
                restriction= res[0][1]
                if any(str.isdigit(restriction) for restriction in restriction):
                    if "1" in res[0][1]:
                        print("here we have the gate code function")
                    elif "2" in res[0][1]:
                        open_door1()
                    elif "3" in res[0][1]:
                        open_door2()
                    elif "N4" in res[0][1]:
                        window_enter(res,"N")
                    elif "N6" in res[0][1]:
                        open_lockpickable(res,"N")
                else:
                    print("You can't go through the wall")
            else:
                add_time(square_side, res[0][0])
                sql= "UPDATE player SET player.y = player.y +1"
                cur.execute(sql)
                sql="select terrain_type.name,terrain_square.description,terrain_square.visitcounter,terrain_square.1stvisit,terrain_square.x,terrain_square.y from terrain_type, terrain_square, player where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
                cur.execute(sql)
                res=cur.fetchall()
                currentSquare = res[0][0]
                print("You entered:", currentSquare)
                enemySpawn()
                if newAreaCode != None and oldAreaCode != newAreaCode:
                    if visitCounter[newAreaCode]<1:
                        print(NewAreaDescription[newAreaCode])
                        visitCounter[newAreaCode]=1
                    else:
                        print(KnownAreaDescription[newAreaCode])
                if res[0][2]==0:
                    sql=(("UPDATE terrain_square set visitcounter=visitcounter+1 where x=%i and y=%i")%(res[0][4],res[0][5]))
                    cur.execute(sql)
                    if res[0][3]!=None:
                        print(res[0][3])
                elif res[0][1]!= None:
                    print(res[0][1])
                if infected:
                    update_infection()
                randomItemDrops()
        else:
            print("The ocean is that way,it would be suicide!")
            
def move_south():
    global visitCounter
    sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
    cur.execute(sql)
    res=cur.fetchall()
    oldAreaCode = res[0][2]
    if "N" in res[0][1]:
        if "N7" in res[0][1]:
            group_of_cannibals()
        else:
            print("You can't go through the wall")
    else:
        sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y-1"
        cur.execute(sql)
        res=cur.fetchall()
        if len(res)>0:
            newAreaCode = res[0][2]
            if res[0][0]==5:
                print("The forest is too thick, you cannot pass!")
            elif "S" in res[0][1]:
                restriction= res[0][1]
                if any(str.isdigit(restriction) for restriction in restriction):
                    if "1" in res[0][1]:
                        print("here we have the gate code function")
                    elif "N2" in res[0][1]:
                        open_door1()
                    elif "W3" in res[0][1]:
                        open_door2()
                    elif "S4" in res[0][1]:
                        window_enter(res,"S")
                    elif "S6" in res[0][1]:
                        open_lockpickable(res,"S")
                else:
                    print("You can't go through the wall")
            else:
                add_time(square_side, res[0][0])
                sql= "UPDATE player SET player.y = player.y -1"
                cur.execute(sql)
                sql="select terrain_type.name,terrain_square.description,terrain_square.visitcounter,terrain_square.1stvisit,terrain_square.x,terrain_square.y from terrain_type, terrain_square, player where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
                cur.execute(sql)
                res=cur.fetchall()
                currentSquare = res[0][0]
                print("You entered:", currentSquare)
                enemySpawn()
                if newAreaCode != None and oldAreaCode != newAreaCode:
                    if visitCounter[newAreaCode]<1:
                        print(NewAreaDescription[newAreaCode])
                        visitCounter[newAreaCode]=1
                    else:
                        print(KnownAreaDescription[newAreaCode])
                if res[0][2]==0:
                    sql=(("UPDATE terrain_square set visitcounter=visitcounter+1 where x=%i and y=%i")%(res[0][4],res[0][5]))
                    cur.execute(sql)
                    if res[0][3]!=None:
                        print(res[0][3])
                elif res[0][1]!= None:        
                    print(res[0][1])
                if infected:
                    update_infection()
                randomItemDrops()
        else:
            print("The ocean is that way,it would be suicide!")
            
def move_east():
    global visitCounter
    sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
    cur.execute(sql)
    res=cur.fetchall()
    oldAreaCode=res[0][2]
    if "W" in res[0][1]:
        print("You can't go through the wall")
    else:
        sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x+1"
        cur.execute(sql)
        res=cur.fetchall()
        if len(res)>0:
            newAreaCode = res[0][2]
            if res[0][0]==5:
                print("The forest is too thick, you cannot pass!")
            elif "E" in res[0][1]:
                restriction= res[0][1]
                if any(str.isdigit(restriction) for restriction in restriction):
                    if "1" in res[0][1]:
                        print("here we have the gate code function")
                    elif "N2" in res[0][1]:
                        open_door1()
                    elif "W3" in res[0][1]:
                        open_door2()
                    elif "E4" in res[0][1]:
                        window_enter(res,"E")
                    elif "E6" in res[0][1]:
                        open_lockpickable(res,"E")
                    elif "E8" in res[0][1]:
                        pack_of_dogs()
                else:
                    print("You can't go through the wall")
            else:
                add_time(square_side, res[0][0])
                sql= "UPDATE player SET player.x = player.x +1"
                cur.execute(sql)
                sql="select terrain_type.name,terrain_square.description,terrain_square.visitcounter,terrain_square.1stvisit,terrain_square.x,terrain_square.y from terrain_type, terrain_square, player where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
                cur.execute(sql)
                res=cur.fetchall()
                currentSquare = res[0][0]
                print("You entered:", currentSquare)
                enemySpawn()
                if newAreaCode != None and oldAreaCode != newAreaCode:
                    if visitCounter[newAreaCode]<1:
                        print(NewAreaDescription[newAreaCode])
                        visitCounter[newAreaCode]=1
                    else:
                        print(KnownAreaDescription[newAreaCode])
                if res[0][2]==0:
                    sql=(("UPDATE terrain_square set visitcounter=visitcounter+1 where x=%i and y=%i")%(res[0][4],res[0][5]))
                    cur.execute(sql)
                    if res[0][3]!=None:
                        print(res[0][3])
                elif res[0][1]!= None:
                    print(res[0][1])
                if infected:
                    update_infection()
                randomItemDrops()
        else:
            print("The ocean is that way,it would be suicide!")
            
def move_west():
    global visitCounter
    sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
    cur.execute(sql)
    res=cur.fetchall()
    oldAreaCode=res[0][2]
    if "E" in res[0][1]:
        print("You can't go through the wall")
    else:
        sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x-1"
        cur.execute(sql)
        res=cur.fetchall()
        if len(res)>0:
            newAreaCode = res[0][2]
            if res[0][0]==5:
                print("The forest is too thick, you cannot pass!")
            elif "W" in res[0][1]:
                restriction= res[0][1]
                if any(str.isdigit(restriction) for restriction in restriction):
                    if "1" in res[0][1]:
                        open_gate(res)
                    elif "N2" in res[0][1]:
                        open_door1()
                    elif "W3" in res[0][1]:
                        open_door2()
                    elif "W4" in res[0][1]:
                        window_enter(res,"W")
                    elif "W6" in res[0][1]:
                        open_lockpickable(res,"W")
                    elif "5" in res[0][1]:
                        print("The bridge is missing too many planks, you need to add some planks to cross the bridge!")
                    elif "W8" in res[0][1]:
                        pack_of_dogs()
                else:
                    print("You can't go through the wall")
            else:
                add_time(square_side, res[0][0])
                sql= "UPDATE player SET player.x = player.x -1"
                cur.execute(sql)
                sql="select terrain_type.name,terrain_square.description,terrain_square.visitcounter,terrain_square.1stvisit,terrain_square.x,terrain_square.y from terrain_type, terrain_square, player where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
                cur.execute(sql)
                res=cur.fetchall()
                currentSquare = res[0][0]
                print("You entered:", currentSquare)
                enemySpawn()
                if newAreaCode != None and oldAreaCode != newAreaCode:
                    if visitCounter[newAreaCode]<1:
                        print(NewAreaDescription[newAreaCode])
                        visitCounter[newAreaCode]=1
                    else:
                        print(KnownAreaDescription[newAreaCode])
                if res[0][2]==0:
                    sql=(("UPDATE terrain_square set visitcounter=visitcounter+1 where x=%i and y=%i")%(res[0][4],res[0][5]))
                    cur.execute(sql)
                    if res[0][3]!=None:
                        print(res[0][3])
                elif res[0][1]!= None:
                    print(res[0][1])
                if infected:
                    update_infection()  
                randomItemDrops()
        else:
            print("The ocean is that way,it would be suicide!")
            
def count_item(name):
    sql="select COUNT(*) FROM item,item_type,player WHERE item_type.id=item.type_id and item.player_id=player.id and item_type.name='%s'"%name
    cur.execute(sql)
    res=cur.fetchall()
    return res[0][0]
def item_delete(name,amount=1):
    sql="SELECT item.id FROM item,item_type,player WHERE item_type.id=item.type_id and item.player_id=player.id and item_type.name='branches'"
    cur.execute(sql)
    res=cur.fetchall()
    if amount==1 and len(res)>0:
        sql=("Update item set item.player_id=NULL where item.id=%i"%res[0][0])
        cur.execute(sql)
        sql="SELECT item.id FROM item,item_type,player WHERE item_type.id=item.type_id and item.player_id=player.id and item_type.name='branches'"
        cur.execute(sql)
        res=cur.fetchall()
    elif amount==2 and len(res)>1:
        sql=(("Update item set item.player_id=NULL where item.id=%i or item.id=%i")%(res[0][0],res[1][0]))
        cur.execute(sql)
    elif amount==3 and len(res)>2:
        sql=(("Update item set item.player_id=NULL where item.id=%i or item.id=%i or item.id=%i")%(res[0][0],res[1][0],res[2][0]))
        cur.execute(sql)
    elif amount==4 and len(res)>3:
        sql=(("Update item set item.player_id=NULL where item.id=%i or item.id=%i or item.id=%i and item.id=%i")% (res[0][0],res[1][0],res[2][0],res[3][0]))
        cur.execute(sql)
    elif amount==5 and len(res)>4:
        sql=(("Update item set item.player_id=NULL where item.id=%i or item.id=%i or item.id=%i or item.id=%i or item.id=%i")%(res[0][0],res[1][0],res[2][0],res[3][0],res[4][0]))
        cur.execute(sql)
    elif amount=="all" and len(res)>0:
        sql=(("Update item set item.player_id=NULL where item.id in(select ID from (select item.id as ID from item,item_type where item.type_id=item_type.id and item_type.name='%s')as c)")% (name))
        cur.execute(sql)
        
def specific_item_check(name):
    sql="SELECT item_type.name FROM item,item_type,player WHERE item_type.id=item.type_id and item.player_id=player.id and item_type.name='%s'"%name
    cur.execute(sql)
    res=cur.fetchall()
    if len(res)>0:
        return True
    else:
        return False
def approximate_item_check(name):  
    sql="SELECT item_type.name FROM item,item_type,player WHERE item_type.id=item.type_id and item.player_id=player.id and item_type.name like'%"+name+"%'"
    cur.execute(sql)
    res=cur.fetchall()
    if len(res)>0:
        return True
    else:
        return False 
def return_approximate_item(name):
    sql="SELECT item_type.name FROM item,item_type,player WHERE item_type.id=item.type_id and item.player_id=player.id and item_type.name like'%"+name+"%'"
    cur.execute(sql)
    res=cur.fetchall()
    if len(res)>0:
        return res[0][0]
    else:
        return False 
def check_object(useable,item="default"):
    if item=="default":
        sql=(("SELECT item_type.name, item_type.description, object.open FROM object,item,item_type,player,terrain_square WHERE item.type_id=item_type.id and player.x=object.x and player.y=object.y and item.object_ID=object.ID and object.name='%s' group by item_type.name")%(useable.lower()))
        cur.execute(sql)
        result=cur.fetchall()
        if result[0][2]==1:
            if len(result)>0:
                print("You found the following items in the %s:"% useable)
                for i in range(len(result)):
                    print(result[i][0]+" (" + result[i][1] + ")")
            else:        
                print("Its empty!")
        else:
            print("The %s is closed"%useable)
    else:
        sql=(("SELECT item_type.name, item_type.description, object.open FROM object,item,item_type,player,terrain_square WHERE item.type_id=item_type.id and item_type.name= '%s' and player.x=object.x and player.y=object.y and item.object_ID=object.ID and object.name='%s' group by item_type.name")%(item,useable))
        cur.execute(sql)
        result=cur.fetchall()
        if len(result)>0:
            return True
        else:
            return False
            
def examine_area():
    sql=("SELECT item_type.name FROM item,item_type,player,terrain_square WHERE item.type_id=item_type.id and player.x=terrain_square.x and player.y=terrain_square.y and item.x=terrain_square.x and item.y=terrain_square.y")
    cur.execute(sql)
    result=cur.fetchall()
    if len(result)>0:
        print("You found the following items when searching the area ")
        for i in range(len(result)):
            print(result[i][0])
    else:
        print("You found nothing interesting.")
        
def extended_look_desription(terrainTypeId,distance,frontTerraintypeId):
    x=random.randint(1,2)
    place=((distance*square_side)-(square_side/2))
    if terrainTypeId==0:
        if frontTerraintypeId==3:
            print("There is a fall about %im from here" % place)
        else:
            print("There is water about %im from here" % (place))
    elif terrainTypeId==1:
        if x==1:
            print("and after %im you see a loght" % (place))
        elif x==2:
            print("and a light is flickering %im from here" % (place))
    elif terrainTypeId==2:
        print("The forest starts about %im away" % (place))
    elif terrainTypeId==3:
        print("There is mountainside about %im from here" % place)
    elif terrainTypeId==4:
        if frontTerraintypeId==1:
            print("There is a beach about %im from here" % place)
        else:
            print("There is something yellow in the background about %im from here" % (place))
    elif terrainTypeId==5:
        if frontTerraintypeId==2:
            print("The forest gets thicker %im away" % place)
        else:
            print("A thick Spruce Forest starts in about %im from here" % place)
    elif terrainTypeId==10 or terrainTypeId==6 or terrainTypeId==7 or terrainTypeId==8 or terrainTypeId==9:
        print("There is some kind of a large object blocking the view %im away" % place)
def extended_look(direction):
    getTerraintypeId=0
    distance=0
    if direction.upper()=="NORTH":
        
        sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y+1 and terrain_square.x=player.x")
        cur.execute(sql)
        result2=cur.fetchall()
        if len(result2)>0:
            for i in range(1,100):
                sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y+%i and terrain_square.x=player.x" % i)
                cur.execute(sql)
                result=cur.fetchall()
                if len(result)>0:
                    if i==1:
                        getTerraintypeId=result[0][0]
                    if getTerraintypeId==result[0][0]:
                        distance+=1
                    else:
                        break

            distance+=1       
            sql=("SELECT terrain_type.name FROM terrain_type WHERE terrain_type.id=%i" % getTerraintypeId)
            cur.execute(sql)
            result=cur.fetchall()
            lastResult=result
                
                
            if getTerraintypeId==1 or getTerraintypeId==2 or getTerraintypeId==3 or getTerraintypeId==4:
                print("Front of you there is",lastResult[0][0])
                sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y+%i and terrain_square.x=player.x" % distance)
                cur.execute(sql)
                result=cur.fetchall()
                if len(result)>0:
                    extended_look_desription(result[0][0],distance,lastResult[0][0])
                else:
                    extended_look_desription(0, distance,lastResult[0][0])
            else:
                print("There is a %s blocking your vision" % result[0][0])
    if direction.upper()=="SOUTH":
        
        sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y-1 and terrain_square.x=player.x")
        cur.execute(sql)
        result2=cur.fetchall()
        if len(result2)>0:
            for i in range(1,100):
                sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y-%i and terrain_square.x=player.x" % i)
                cur.execute(sql)
                result=cur.fetchall()
                if len(result)>0:
                    if i==1:
                        getTerraintypeId=result[0][0]
                    if getTerraintypeId==result[0][0]:
                        distance+=1
                    else:
                        break

            distance+=1       
            sql=("SELECT terrain_type.name FROM terrain_type WHERE terrain_type.id=%i" % getTerraintypeId)
            cur.execute(sql)
            result=cur.fetchall()
            lastResult=result
                
                
            if getTerraintypeId==1 or getTerraintypeId==2 or getTerraintypeId==3 or getTerraintypeId==4:
                print("Front of you there is",lastResult[0][0])
                sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y-%i and terrain_square.x=player.x" % distance)
                cur.execute(sql)
                result=cur.fetchall()
                if len(result)>0:
                    extended_look_desription(result[0][0],distance,lastResult[0][0])
                else:
                    extended_look_desription(0, distance,lastResult[0][0])
            else:
                print("There is a %s blocking your vision" % result[0][0])
    if direction.upper()=="WEST":
        
        sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x-1")
        cur.execute(sql)
        result2=cur.fetchall()
        if len(result2)>0:
            for i in range(1,100):
                sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x-%i" % i)
                cur.execute(sql)
                result=cur.fetchall()
                if len(result)>0:
                    if i==1:
                        getTerraintypeId=result[0][0]
                    if getTerraintypeId==result[0][0]:
                        distance+=1
                    else:
                        break

            distance+=1       
            sql=("SELECT terrain_type.name FROM terrain_type WHERE terrain_type.id=%i" % getTerraintypeId)
            cur.execute(sql)
            result=cur.fetchall()
            lastResult=result
                
                
            if getTerraintypeId==1 or getTerraintypeId==2 or getTerraintypeId==3 or getTerraintypeId==4:
                print("Front of you there is",lastResult[0][0])
                sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x-%i" % distance)
                cur.execute(sql)
                result=cur.fetchall()
                if len(result)>0:
                    extended_look_desription(result[0][0],distance,lastResult[0][0])
                else:
                    extended_look_desription(0, distance,lastResult[0][0])
            else:
                print("There is a %s blocking your vision" % result[0][0])
    if direction.upper()=="EAST":
        
        sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x+1")
        cur.execute(sql)
        result2=cur.fetchall()
        if len(result2)>0:
            for i in range(1,100):
                sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x+%i" % i)
                cur.execute(sql)
                result=cur.fetchall()
                if len(result)>0:
                    if i==1:
                        getTerraintypeId=result[0][0]
                    if getTerraintypeId==result[0][0]:
                        distance+=1
                    else:
                        break

            distance+=1       
            sql=("SELECT terrain_type.name FROM terrain_type WHERE terrain_type.id=%i" % getTerraintypeId)
            cur.execute(sql)
            result=cur.fetchall()
            lastResult=result
                
                
            if getTerraintypeId==1 or getTerraintypeId==2 or getTerraintypeId==3 or getTerraintypeId==4:
                print("In front of you there is",lastResult[0][0])
                sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x+%i" % distance)
                cur.execute(sql)
                result=cur.fetchall()
                if len(result)>0:
                    extended_look_desription(result[0][0],distance,lastResult[0][0])
                else:
                    extended_look_desription(0, distance,lastResult[0][0])
            else:
                print("There is a %s blocking your vision" % result[0][0])    
def player_stats():
    sql=("SELECT player.carry, player.att,player.speed,player.hp,player.fatigue FROM player")
    cur.execute(sql)
    result=cur.fetchall()
    print(('''
==============
|Healt    %s     
|Carrying %s   
|Attack   %s   
|Fatiogue %s
|Speed    %s   
==============   
    ''') % (result[0][3],result[0][0],result[0][1],result[0][4],result[0][2]))
def eat(foodName):
    sql=(("SELECT item_type.name,item.id,item_type.healing,item_type.weight, COUNT(*),item_type.id FROM item,item_type WHERE item.type_id=item_type.id and item.player_ID>0 and item_type.name LIKE '"+foodName.lower()+"%' GROUP BY item_type.name"))
    cur.execute(sql)
    result=cur.fetchall()
    if len(result)>0:
        rand=random.randint(1,100)
        if result[0][2]!=0:
            itemID=result[0][1]
            
            itemHealing=result[0][2]
            totalHealt=((player_carry_att_speed_hp_fatique()[0][3])+itemHealing)
            update_player_healt(totalHealt)
            
            item_weight=result[0][3]
            totalWeight=((player_carry_att_speed_hp_fatique()[0][0])-item_weight)
            update_player_weight(totalWeight)
            
            sql=(("DELETE FROM item WHERE item.id=%i") % itemID)
            cur.execute(sql)
            print("You ate a ",result[0][0])
            if result[0][5]==2:
                if rand<25:
                    if infected:
                        update_infection()
                    else:
                        infect()
            elif result[0][5]==1:
                if rand<20:
                    if infected:
                        update_infection()
                    else:
                        infect()
            elif result[0][5]==3:
                if rand<50:
                    if infected:
                        update_infection(3)
                    else:
                        infect()
            elif result[0][5]==4:
                    if infected:
                        update_infection(10)
                    else:
                        infect()
        else:
            print("You can't eat %s or do you have metal teeth or something?" % result[0][0])
    else:
        print(("You don't have item called %s in your inventory") % (foodName.lower()))
def sleep(hours):
    global dt
    if hours>12:
        hours=12
    if hours<0:
        hours=0
    itemIshere=0
    sql=(("SELECT item_type.id,item_type.name  FROM item,item_type,player,terrain_square WHERE item.type_id=item_type.id and player.x=terrain_square.x and player.y=terrain_square.y and item.x=terrain_square.x and item.y=terrain_square.y"))
    cur.execute(sql)
    itemsIdsINarea=cur.fetchall()
    checkItemsId=[41,42]
    sql=(("Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"))
    cur.execute(sql)
    terrainTypeId=cur.fetchall()
    
    if (terrainTypeId[0][0])==10 or (terrainTypeId[0][0])==6 or (terrainTypeId[0][0])==7 or (terrainTypeId[0][0])==8 or (terrainTypeId[0][0])==9:
        for i in range(len(itemsIdsINarea)):
            for x in range(len(checkItemsId)):
                if (itemsIdsINarea[i][0])==checkItemsId[x]:
                    itemIshere=1
                    if dt.hour>=22 and dt.hour<=23 or dt.hour>=0 and dt.hour<=8:
                        
                        time=(60*60*hours)
                        tdelta=datetime.timedelta(seconds=time)
                    
                        dt=(dt+tdelta)
                        if infected:
                            update_infection()
                        print("You slept %ih and time is now %s" % (hours,dt))
                        update_player_fatique(0)
                        break
                    else:
                        print("You can't sleep now there is still light")
                        break
        if itemIshere==0:
            print("There is nothing where you can lay on")
    else:
        print("Here is not safe to sleep")
def combineITEMS(itemId1,itemId2):
    itemids=[itemId1,itemId2]
    itemids.sort()
    #item1=0
    #item2=0
    #combineItems=[58,10,37,38,57]
    searchProduct={(37,38):39,(57,58):36,(9,58):80,(38,80):81,(31,58):76,(38,50):82,(19,38):83,(20,38):84,(22,38):85,(6,10):86,(10,58):87,(13,93):94,(13,95):96}
    #39 poison arrow
    #36 bow
    #80 spear
    #81 toxic spear
    #76 slingshot
    #82 toxic axe
    #83 poisoned blade
    #84 poisoned shovel
    #85 poisoned rake
    #86 paperweight
    
    #85 stone spear
    #94 spiked baton
    #96 spiked baseball bat
    
    try:
        productId=searchProduct[itemids[0],itemids[1]]
        return productId
    except:
        return False
        
    return False
def combine(twoItems):
    #print(twoItems)
    itemnames=[]
    for i in range(len(twoItems)):
        itemnames.append(twoItems[i].lower())
    #print(itemnames)
    if (check_item_type(itemnames[0]))==True and (check_item_type(itemnames[1]))==True:
        
        sql=(("SELECT item_type.name,item_type.id FROM item_type,item WHERE item.type_id=item_type.id and item.player_ID>0 and item_type.name like '"+itemnames[0]+"%'"))
        cur.execute(sql)
        item1=cur.fetchall()
        sql=(("SELECT item_type.name,item_type.id FROM item_type,item WHERE item.type_id=item_type.id and item.player_ID>0 and item_type.name like '"+itemnames[1]+"%'"))
        cur.execute(sql)
        item2=cur.fetchall()
        #print(item1[0][1])
        totalLen=(len(item1)+len(item2))
        if totalLen>1:
            try:
                productId=combineITEMS(item1[0][1], item2[0][1])
            except:
                print("You need to have both items in your inventory to able to craft")
                productId=0
            if productId>0:
                sql=("SELECT MAX(item.id) FROM item")
                cur.execute(sql)
                maxId=cur.fetchall()[0][0]
                newItemsID=(maxId+1)
                sql=(("SELECT item_type.name,item_type.weight FROM item_type WHERE item_type.id=%i") % productId)
                cur.execute(sql)
                result=cur.fetchall()
                newItemsName=result[0][0]
                #new Item made for player inv(below)
                sql=(("INSERT INTO item VALUES (%i,%i,0,0,1,NULL,NULL)") % (newItemsID,productId))
                cur.execute(sql)
                
                sql=(("SELECT item.id,item_type.name,item_type.weight FROM item,item_type WHERE item.type_id=item_type.id and item_type.name like '"+itemnames[0]+"%' and item.player_ID>0"))
                cur.execute(sql)
                fItemID=cur.fetchall()
                sql=(("SELECT item.id,item_type.name,item_type.weight FROM item,item_type WHERE item.type_id=item_type.id and item_type.name like '"+itemnames[1]+"%' and item.player_ID>0"))
                cur.execute(sql)
                sItemID=cur.fetchall()
                
                sql=(("DELETE FROM item WHERE item.id=%i")% (fItemID[0][0]))
                cur.execute(sql)
                sql=(("DELETE FROM item WHERE item.id=%i")% (sItemID[0][0]))
                cur.execute(sql)
                
                totalWeight=(((player_carry_att_speed_hp_fatique()[0][0])-(fItemID[0][2]+sItemID[0][2]))+result[0][1])
                #print(totalWeight)
                update_player_weight(totalWeight)
                
                print("You crafted",newItemsName)
        else:
            print("You need to have both items in your inventory to able to craft")
    else:
        print("There isn's such a item(s)")
def equip(item):
    item=item.lower()
    sql=(("SELECT item.id,item_type.name,item_type.att,item_type.defense,item.type_id,item_type.part FROM item, item_type WHERE item.type_id=item_type.id and item.player_ID>0 and item_type.name LIKE '"+item+"%'"))
    #print(sql)
    cur.execute(sql)
    itemINFO=cur.fetchall()
    
    if len(itemINFO)>0:
        itemTypeID=itemINFO[0][4]
        itemID=itemINFO[0][0]
        itemName=itemINFO[0][1]
        itemAtt=itemINFO[0][2]
        itemDEFF=itemINFO[0][3]
        itemPart=itemINFO[0][5]
        
        if itemPart=="feet" or itemPart=="leg" or itemPart=="body" or itemPart=="head" or itemPart=="hand" or itemAtt>0 or itemDEFF>0:
            sql=(("SELECT item_type.name FROM item, item_type WHERE item.type_id=item_type.id and item.equipped=1 and item_type.part like '"+itemPart+"%'"))
            #print(sql)
            cur.execute(sql)
            eqPart=cur.fetchall()
            if len(eqPart)<1:
                sql=(("UPDATE item SET item.player_ID=NULL, item.equipped=1 WHERE item.id=%i") % itemID)
                cur.execute(sql)
                
                totalHP=(player_carry_att_speed_hp_fatique()[0][3]+itemDEFF)
                global player_max_healt
                player_max_healt+=itemDEFF
                update_player_healt(totalHP)
                
                totalAtt=(player_carry_att_speed_hp_fatique()[0][1]+itemAtt)
                update_player_attack(totalAtt)
                print("You have just equipped",itemName)
                
            else:
                print("You have equipment in that slot already")
        else:
            print("You can't equip that")
    else:
        print("You don't have item in your inventory") 
def unEquip(item):
    item=item.lower()
    sql=(("SELECT item.id,item_type.name,item_type.att,item_type.defense,item.type_id,item_type.part FROM item, item_type WHERE item.type_id=item_type.id and item.equipped=1 and item_type.name like '"+item+"%'"))
    cur.execute(sql)
    itemINFO=cur.fetchall()
    
    if len(itemINFO)>0:
        itemTypeID=itemINFO[0][4]
        itemID=itemINFO[0][0]
        itemName=itemINFO[0][1]
        itemAtt=itemINFO[0][2]
        itemDEFF=itemINFO[0][3]
        itemPart=itemINFO[0][5]
        
        sql=(("UPDATE item SET item.player_ID=1, item.equipped=NULL WHERE item.id=%i") % itemID)
        cur.execute(sql)
        
        totalHP=(player_carry_att_speed_hp_fatique()[0][3]-itemDEFF)
        global player_max_healt
        
        if totalHP<1:
            update_player_healt(1)
        else:
            update_player_healt(totalHP)
        player_max_healt-=itemDEFF
        totalAtt=(player_carry_att_speed_hp_fatique()[0][1]-itemAtt)
        update_player_attack(totalAtt)
        print("You have just unequipped",itemName)
        
    else:
        print("You don't have that item equipped")
        
def quickParse(input):
    playerCaps = input.upper()
    filter = [".", ",",":","AN","A","MOVE", "GO", "OUT", "THE", "AND", "TO","SOME","FOR","ON"]
    splitText = split_line(playerCaps)
    playerText = [c for c in splitText if c not in filter]
    return playerText
def removeEnemy(id):
    sql=("DELETE FROM enemy WHERE id=%i" % id)
    cur.execute(sql)
def attack():
    sql="select enemy_type.name from enemy_type,enemy, player where enemy.type_id=enemy_type.id and enemy.x=player.x and enemy.y=player.y"
    cur.execute(sql)
    res=cur.fetchall()
    if len(res)>0:
        combat(res[0][0])
    else:
        print("Theres no-one to attack.")
def combat(enemyName):
    enemyName=enemyName.lower()
    sql=(("SELECT enemy.id,enemy_type.id, enemy_type.name,enemy_type.hp,enemy_type.att,enemy_type.speed,enemy_type.description, enemy_type.description2,enemy_type.seen FROM enemy,enemy_type,player,terrain_square WHERE enemy.type_id=enemy_type.id and player.x=terrain_square.x and player.y=terrain_square.y and enemy.x=terrain_square.x and enemy.y=terrain_square.y and enemy_type.name='%s'")% (enemyName))    
    cur.execute(sql)
    enemyINFO=cur.fetchall()
    
    sql=("SELECT item.type_id FROM item WHERE item.equipped>0")
    if len(enemyINFO)>0:
        print("Attack is starting...")
        hpBuff=((random.randint(1,50))/100+1)
        attBuff=((random.randint(1,30))/100+1)
        speedBuff=((random.randint(1,20))/100+1)
        enemyTypeID=enemyINFO[0][1]
        enemyID=enemyINFO[0][0]
        enemyName=enemyINFO[0][2]
        enemyHP=(float((enemyINFO[0][3]))*hpBuff)
        enemyAtt=(float((enemyINFO[0][4]))*attBuff)
        enemySpeed=(float((enemyINFO[0][5]))*speedBuff)
        
        playerHP=player_carry_att_speed_hp_fatique()[0][3]
        playerAtt=player_carry_att_speed_hp_fatique()[0][1]
        playerSpeed=player_carry_att_speed_hp_fatique()[0][2]
        
        sql=("SELECT item_type.name, item_type.id, item_type.att FROM item,item_type WHERE item.type_id=item_type.id and item.equipped>0 and item_type.part='hand'")
        cur.execute(sql)
        inHand=cur.fetchall()
        ammoName="noammo"
        ammoAtt=0
        if len(inHand)>0:
            if inHand[0][0]=="bow" or inHand[0][0]=="slingshot":
                if inHand[0][0]=="slingshot":
                    ammonation="sammo"
                else:
                    ammonation="arrow"
                
                sql=("SELECT item_type.att ,item_type.name, item.id,item.type_id  FROM item,item_type WHERE item.type_id=item_type.id and item.player_ID>0 and item_type.part='"+ammonation+"'  GROUP BY item_type.att DESC")
                cur.execute(sql)
                ammo=cur.fetchall()
                if len(ammo)>0:
                    ammoID=ammo[0][2]
                    ammoName=ammo[0][1]
                    ammoAtt=ammo[0][0]
                    
                else:
                    ammoName="noammo"
                    ammoAtt=0
        x="."
        timedelay(3, 0.6)
        print("You are in combat with",enemyName)
        if playerSpeed>enemySpeed:
            print("and you were faster than opponent, you hit",enemyName)
            enemyHP-=(playerAtt+ammoAtt)
        else:
            print("and got hit by it")
            playerHP-=enemyAtt
        time.sleep(1.5)
        for i in range(1,4):
            time.sleep(1)
            print(x*i)
        human='''             x====x
             |head|            
        x====x====x====x
        |hand|body|hand|            
        x====x====x====x     
             |legs|       
             x====x
             |feet|
             x====x    '''
        handlesshuman='''             x====x
             |head|            
             x====x
             |body|            
             x====x     
             |legs|       
             x====x
             |feet|
             x====x    '''
        leglesshuman='''             x====x
             |head|            
        x====x====x====x
        |hand|body|hand|            
        x====x====x====x     
             ||||||    '''
        fourlegs='''       xx====x====x====x====x
      x |====|body|====|head|
     x  x====x====x====x====x
        |legs||   |legs||
        x====xx   x====xx
        '''
        bird='''             x====x
             |head|            
             x====x
            x|body|x            
           x x====x x    
             |legs|       
             x====x
                    '''
        
        xx=0
        if enemyHP<0:
            
            if inHand[0][0]=="bow" or inHand[0][0]=="slingshot":
                if ammoAtt>0:
                    print("You killed "+enemyName+" with single shot and got your ammunation back")
                else:
                    print("You hit with your poor range weapon to "+enemyName+" and killed it")
            else:
                print("You killed "+enemyName+" with single blow")
            enemyDrops(enemyTypeID)
            removeEnemy(enemyID)
            update_player_healt(playerHP)
            
        else:
            xxx=0
            if ammoName!="noammo":
                itemdrop=random.randint(1,2)
                
                if itemdrop==1:
                    sql=("DELETE FROM item WHERE item.id=%i" % ammoID)
                    cur.execute(sql)
                else:
                    sql=("UPDATE item SET item.type_id=%i,item.x=%i, item.y=%i, item.player_ID=NULL, item.equipped=NULL WHERE item.id=%i" % (ammo[0][3],player_position()[0][0],player_position()[0][1],ammoID))
                    cur.execute(sql)
            while playerHP>0 or enemyHP>0:
                #sql=("SELECT item_type.name, item_type.id, item_type.att FROM item,item_type WHERE item.type_id=item_type.id and item.equipped>0 and item_type.part='hand'")
                #cur.execute(sql)
                #inHand=cur.fetchall()
                
                if len(inHand)>0:
                    if inHand[0][0]=="bow" or inHand[0][0]=="slingshot":
                        if inHand[0][0]=="slingshot":
                            ammonation="sammo"
                        else:
                            ammonation="arrow"
                        
                        sql=("SELECT item_type.att ,item_type.name, item.id,item.type_id  FROM item,item_type WHERE item.type_id=item_type.id and item.player_ID>0 and item_type.part='"+ammonation+"'  GROUP BY item_type.att DESC")
                        #print(sql)
                        cur.execute(sql)
                        ammo=cur.fetchall()
                        if len(ammo)>0:
                            ammoID=ammo[0][2]
                            ammoName=ammo[0][1]
                            ammoAtt=ammo[0][0]
                            
                        else:
                            ammoName="noammo"
                            ammoAtt=0
                        
               
                
                playerAtt+=ammoAtt
                enemyHitchange=random.randint(1,100)
                playerHitchange=random.randint(1,100)
                playerHitchangeTarget=(1.01**float(playerSpeed))
                enemyCritChange=10 #%
                enemyCritChangeValue=random.randint(1,100)
                playerCritChange=18 #%
                playerCritChangeValue=random.randint(1,100)
                critMultiplier=1.5 
                if xx==0:
                    print("\n"*100)
                    xx=1
                else:
                    x="."
                    timedelay(3, 0.5)
                    print("\n"*100)
                print("You are in combat with the",enemyName)
                print()
                print("\t    Health:%i"%enemyHP)
                pheadHit=80*playerHitchangeTarget
                phandHit=70*playerHitchangeTarget
                pbodyHit=95*playerHitchangeTarget
                plegsHit=70*playerHitchangeTarget
                pfeetHit=20*playerHitchangeTarget
                if enemyTypeID in [1,2,11,12]:
                    print(human)
                    hitlist=["head","hand","body","legs","feet","hands","leg"]
                    damageMultiplier=1
                    if enemySpeed<3:
                        damageMultiplier=1.9
                    elif enemySpeed>15:
                        damageMultiplier=1.5
                    headHit=80*playerHitchangeTarget
                    handHit=70*playerHitchangeTarget
                    bodyHit=95*playerHitchangeTarget
                    legsHit=70*playerHitchangeTarget
                    feetHit=20*playerHitchangeTarget
                elif enemyTypeID==4:
                    print(handlesshuman)
                    hitlist=["head","body","legs","feet","leg"]
                    damageMultiplier=0.9
                    headHit=86*playerHitchangeTarget
                    bodyHit=96*playerHitchangeTarget
                    legsHit=90*playerHitchangeTarget
                    feetHit=70*playerHitchangeTarget
                elif enemyTypeID==3:
                    print(leglesshuman)
                    hitlist=["head","hand","body","hands"]
                    damageMultiplier=2
                    headHit=90*playerHitchangeTarget
                    handHit=80*playerHitchangeTarget
                    bodyHit=100*playerHitchangeTarget
                    
                elif enemyTypeID in [5,6,7,8,9]:
                    print(fourlegs)
                    hitlist=["head","body","legs","feet","leg"]
                    damageMultiplier=1
                    headHit=85*playerHitchangeTarget
                    bodyHit=95*playerHitchangeTarget
                    legsHit=70*playerHitchangeTarget
                    feetHit=40*playerHitchangeTarget
                elif enemyTypeID==10:
                    print(bird)
                    hitlist=["head","body","legs","leg"]
                    damageMultiplier=2
                    headHit=50*playerHitchangeTarget
                    bodyHit=70*playerHitchangeTarget
                    legsHit=5*playerHitchangeTarget
                
                if ammoName!="noammo":
                    playerCritChange+=25   
                print()
                enemyAtt=enemyAtt*damageMultiplier
                if len(inHand)>0:
                    if inHand[0][0]=="slingshot" or inHand[0][0]=="bow" and ammoName=="noammo" :
                        
                        if xxx==0:
                            playerAtt-=(playerAtt*0.70)
                            xxx+=1
                            
                        print("You dont have any ammunition for your",inHand[0][0])
                    
                print("Your attack:",int(playerAtt))
                print("Your crit chance:",playerCritChange)
                print("Your Health:",int(playerHP))
                
                
                playerINPUT=input("Choose where to aim the next attack or run : ")
                
                playerINPUT.lower()
                
               
                if playerINPUT in hitlist or playerINPUT=="run":
                    if playerINPUT=="run":
                        print("You start running..")
                    else:
                        print("hitting...")
                    if playerINPUT=="head" and playerINPUT in hitlist:
                        damageValue=((100-headHit)/100+1)
                        if playerCritChange<=playerCritChangeValue:
                            damage=playerAtt*critMultiplier*damageValue
                        else:
                            damage=playerAtt*damageValue
                        if playerHitchange<=headHit:
                            enemyHP-=damage
                            if ammoName!="noammo":
                                
                                itemdrop=random.randint(1,2)
                                
                                if itemdrop==1:
                                    sql=("DELETE FROM item WHERE item.id=%i" % ammoID)
                                    cur.execute(sql)
                                else:
                                    sql=("UPDATE item SET item.type_id=%i,item.x=%i, item.y=%i, item.player_ID=NULL, item.equipped=NULL WHERE item.id=%i" % (ammo[0][3],player_position()[0][0],player_position()[0][1],ammoID))
                                    cur.execute(sql)
                                
                            print("you hit the enemies head for %i damage" % (int(damage)))
                        else:
                            print("You missed")
                    elif playerINPUT=="feet" and playerINPUT in hitlist:
                        damageValue=((100-feetHit)/100+1)
                        if playerCritChange<=playerCritChangeValue:
                            damage=playerAtt*critMultiplier*damageValue
                        else:
                            damage=playerAtt*damageValue
                        if playerHitchange<=feetHit:
                            enemyHP-=damage
                            if ammoName!="noammo":
                                
                                itemdrop=random.randint(1,2)
                                
                                if itemdrop==1:
                                    sql=("DELETE FROM item WHERE item.id=%i" % ammoID)
                                    cur.execute(sql)
                                else:
                                    sql=("UPDATE item SET item.type_id=%i,item.x=%i, item.y=%i, item.player_ID=NULL, item.equipped=NULL WHERE item.id=%i" % (ammo[0][3],player_position()[0][0],player_position()[0][1],ammoID))
                                    cur.execute(sql)
                            print("you hit the enemies feet for %i" % (int(damage)))
                        else:
                            print("You missed")
                        
                    elif playerINPUT=="legs" and playerINPUT in hitlist:
                        damageValue=((100-legsHit)/100+1)
                        if playerCritChange<=playerCritChangeValue:
                            damage=playerAtt*critMultiplier*damageValue
                        else:
                            damage=playerAtt*damageValue
                        if playerHitchange<=legsHit:
                            enemyHP-=damage
                            if ammoName!="noammo":
                                
                                itemdrop=random.randint(1,2)
                                
                                if itemdrop==1:
                                    sql=("DELETE FROM item WHERE item.id=%i" % ammoID)
                                    cur.execute(sql)
                                else:
                                    sql=("UPDATE item SET item.type_id=%i,item.x=%i, item.y=%i, item.player_ID=NULL, item.equipped=NULL WHERE item.id=%i" % (ammo[0][3],player_position()[0][0],player_position()[0][1],ammoID))
                                    cur.execute(sql)
                            print("you hit the enemies legs",(int(damage)))
                        else:
                            print("You missed")
                        
                    elif playerINPUT=="body" and playerINPUT in hitlist:
                        damageValue=((100-bodyHit)/100+1)
                        if playerCritChange<=playerCritChangeValue:
                            damage=playerAtt*critMultiplier*damageValue
                        else:
                            damage=playerAtt*damageValue
                        if playerHitchange<=bodyHit:
                            enemyHP-=damage
                            if ammoName!="noammo":
                                
                                itemdrop=random.randint(1,2)
                                
                                if itemdrop==1:
                                    sql=("DELETE FROM item WHERE item.id=%i" % ammoID)
                                    cur.execute(sql)
                                else:
                                    sql=("UPDATE item SET item.type_id=%i,item.x=%i, item.y=%i, item.player_ID=NULL, item.equipped=NULL WHERE item.id=%i" % (ammo[0][3],player_position()[0][0],player_position()[0][1],ammoID))
                                    cur.execute(sql)
                            print("you hit the enemies body for %i damage" % (int(damage)))
                        else:
                            print("You missed")
                    elif playerINPUT=="run":
                        if enemyHitchange>=30:
                            playerHP-=(playerHP*0.1+enemyAtt)
                            timedelay(3, 0.5)
                            print("You escaped from %s but you got hit by %i" % (enemyName,(playerHP*0.1+enemyAtt)))
                        else:
                            timedelay(3, 0.5)
                            print("You escaped from the ",enemyName)
                        if enemyTypeID==11:
                            sql=(("UPDATE player SET player.x=4, player.y=7 WHERE player.ID=1"))
                            cur.execute(sql)
                            print('''But..
You wake up on the beach, hear the Ocean waves crashing in the shore.
                            
                            ''')
                        else:
                            removeEnemy(enemyID)
                        update_player_healt(playerHP)
                        break
                    timedelay(3, 0.5)
                    if enemyHP>0:
                        print("Opponent's turn")
                        timedelay(3, 0.5)
                        
                        enemyHit=random.choice(["head","hands","hands","body","body","body","legs","legs","feet","miss"])
                        if enemyHit=="head":
                            damageValue=((100-pheadHit)/100+1)
                            if enemyCritChange<=enemyCritChangeValue:
                                damage=enemyAtt*critMultiplier*damageValue
                            else:
                                damage=enemyAtt*damageValue
                            if enemyCritChange<=pheadHit:
                                playerHP-=damage
                                print("The enemy struck your head")
                            else:
                                print("The enemy missed his attack")
                                
                        elif enemyHit=="hands":
                            damageValue=((100-phandHit)/100+1)
                            if enemyCritChange<=enemyCritChangeValue:
                                damage=enemyAtt*critMultiplier*damageValue
                            else:
                                damage=enemyAtt*damageValue
                            if enemyCritChange<=phandHit:
                                playerHP-=damage
                                print("The enemy hit your hand")
                            else:
                                print("The enemy missed his attack")
                        elif enemyHit=="body":
                            damageValue=((100-pbodyHit)/100+1)
                            if enemyCritChange<=enemyCritChangeValue:
                                damage=enemyAtt*critMultiplier*damageValue
                            else:
                                damage=enemyAtt*damageValue
                            if enemyCritChange<=pbodyHit:
                                playerHP-=damage
                                print("The enemy delivered a blow to your body")
                            else:
                                print("Enemy missed his attack")
                        elif enemyHit=="legs":
                            damageValue=((100-plegsHit)/100+1)
                            if enemyCritChange<=enemyCritChangeValue:
                                damage=enemyAtt*critMultiplier*damageValue
                            else:
                                damage=enemyAtt*damageValue
                            if enemyCritChange<=plegsHit:
                                playerHP-=damage
                                print("The enemy targeted your legs")
                            else:
                                print("The enemy missed his attack")
                        elif enemyHit=="feet":
                            damageValue=((100-pfeetHit)/100+1)
                            if enemyCritChange<=enemyCritChangeValue:
                                damage=enemyAtt*critMultiplier*damageValue
                            else:
                                damage=enemyAtt*damageValue
                            if enemyCritChange<=pfeetHit:
                                playerHP-=damage
                                print("The enemy attacked your feet")
                            else:
                                print("The enemy missed his attack")
                        elif enemyHit=="miss":
                            print("You managed to dodge the opponents attack")
                        
                        timedelay(3, 0.5)
                        print("Your turn is coming...")
                    
                    if playerHP<=0 or enemyHP<=0:
                        if playerHP>0:
                            print("You killed the ",enemyName)
                            enemyDrops(enemyTypeID)
                        else:
                            print("You died")
                        removeEnemy(enemyID)
                        update_player_healt(playerHP)
                        break
                else:
                    print("You didn't hit the enemy")
            
        
    else:   
        print("There isn't that kind of character in area")
        
def itemDrop(type_id,x,y):
    
    xx=random.randint(1000,9999)
    sql=("SELECT MAX(item.id) FROM item")
    cur.execute(sql)
    maxId=cur.fetchall()
    if len(maxId)>0:
        newId=(int((maxId[0][0]))+xx)
    else:
        newId=100
    
    sql=("INSERT INTO item VALUES (%i,%i,%i,%i,NULL,NULL,NULL)" % (newId,type_id,x,y))
    cur.execute(sql)
def itemName(type_id):
    sql=("SELECT item_type.name FROM item_type WHERE item_type.id=%i" % type_id)
    cur.execute(sql)
    result=cur.fetchall()
    return result[0][0]
def enemyDrops(enemy_type_id):
    x=player_position()[0][0]
    y=player_position()[0][1]
    rand=random.choice([1,2,3,4,5,6,7,8,9,10])
    itemDropList=[]
    if enemy_type_id==1: #cannibal
        itemDrop(5,x,y)
        itemDropList.append(itemName(5))
        if rand==1:
            itemDrop(9,x,y)
            itemDropList.append(itemName(9))
        elif rand==2:
            itemDrop(106,x,y)
            itemDropList.append(itemName(106))
        elif rand==3:
            itemDrop(114,x,y)
            itemDropList.append(itemName(114))
        elif rand==4:
            itemDrop(115,x,y)
            itemDropList.append(itemName(115))
        elif rand==5:
            itemDrop(113,x,y)
            itemDropList.append(itemName(113))
    elif enemy_type_id==2: #bulky cannibal
        itemDrop(5,x,y)
        itemDropList.append(itemName(5))
        if rand==1:
            itemDrop(34,x,y)
            itemDropList.append(itemName(34))
        elif rand==2:
            itemDrop(103,x,y)
            itemDropList.append(itemName(103))
        elif rand==3:
            itemDrop(115,x,y)
            itemDropList.append(itemName(115))
        elif rand==4:
            itemDrop(106,x,y)
            itemDropList.append(itemName(106))
        elif rand==5:
            itemDrop(44,x,y)
            itemDropList.append(itemName(44))
        elif rand==6:
            itemDrop(89,x,y)
            itemDropList.append(itemName(89))
    elif enemy_type_id==3: #leggless cannibal
        itemDrop(5,x,y)
        itemDropList.append(itemName(5))
        if rand==1:
            itemDrop(9,x,y)
            itemDropList.append(itemName(9))
        elif rand==2:
            itemDrop(88,x,y)
            itemDropList.append(itemName(88))
        elif rand==3:
            itemDrop(114,x,y)
            itemDropList.append(itemName(114))
        elif rand==4:
            itemDrop(13,x,y)
            itemDropList.append(itemName(13))
        elif rand==5:
            itemDrop(113,x,y)
            itemDropList.append(itemName(113))
    elif enemy_type_id==4: #handdles cannibal
        itemDrop(5,x,y)
        itemDropList.append(itemName(5))
        if rand==1:
            itemDrop(9,x,y)
            itemDropList.append(itemName(9))
        elif rand==2:
            itemDrop(106,x,y)
            itemDropList.append(itemName(106))
        elif rand==3:
            itemDrop(107,x,y)
            itemDropList.append(itemName(107))
        elif rand==4:
            itemDrop(109,x,y)
            itemDropList.append(itemName(109))
        elif rand==5:
            itemDrop(112,x,y)
            itemDropList.append(itemName(112))
    elif enemy_type_id==5: #wild hog meat
        itemDrop(113,x,y)
        itemDropList.append(itemName(113))
        itemDrop(2,x,y)
        itemDropList.append(itemName(2))
    elif enemy_type_id==6: #dog
        itemDrop(125,x,y)
        itemDropList.append(itemName(125))
        if rand==1 or rand==2 or rand==3:
            itemDrop(113,x,y)
            itemDropList.append(itemName(113))
    elif enemy_type_id==7: #cannibal dog
        itemDrop(125,x,y)
        itemDropList.append(itemName(125))
        if rand==1 or rand==2 or rand==3:
                itemDrop(113,x,y)
                itemDropList.append(itemName(113))
    elif enemy_type_id==8: #squirrel
        itemDrop(3,x,y)
        itemDropList.append(itemName(3))
        if rand==1 or rand==2 or rand==3:
            itemDrop(113,x,y)
            itemDropList.append(itemName(113))
    elif enemy_type_id==9: #rat
        itemDrop(4,x,y)
        itemDropList.append(itemName(4))
    elif enemy_type_id==10: #owl
        itemDrop(112,x,y)
        itemDropList.append(itemName(112))
        if rand==1 or rand==3:
            itemDrop(57,x,y)
            itemDropList.append(itemName(57))
        elif rand==2:
            itemDrop(7,x,y)
            itemDropList.append(itemName(7))
    elif enemy_type_id==11:
        itemDrop(60,x,y)
        itemDropList.append(itemName(60))
        itemDrop(103,x,y)
        itemDropList.append(itemName(103))
        itemDrop(5,x,y)
        itemDropList.append(itemName(5))
        itemDrop(52,x,y)
        itemDropList.append(itemName(52))
    if len(itemDropList)>0:
        print("It dropped the following items: ")
        for i in range(len(itemDropList)):
            print(itemDropList[i])
                        
def enemySpawn():
    global despawnCountX
    
    if despawnCountX>=despawnCount:
        sql="DELETE FROM enemy WHERE enemy.spawned>0"
        cur.execute(sql)
    
    neutralEnemiesIds=[5,8,10]
    sql=(("SELECT enemy.id,enemy_type.id, enemy_type.name,enemy_type.hp,enemy_type.att,enemy_type.speed, terrain_square.type_id, enemy_type.description, enemy_type.description2,enemy_type.seen FROM enemy,enemy_type,player,terrain_square WHERE enemy.type_id=enemy_type.id and player.x=terrain_square.x and player.y=terrain_square.y and enemy.x=terrain_square.x and enemy.y=terrain_square.y"))    
    cur.execute(sql)
    enemies=cur.fetchall()
    if len(enemies)>0:
        if enemies[0][1]==11:
            sql=("SELECT MAX(item_type.att) FROM item_type")
            cur.execute(sql)
            maxDamage=cur.fetchall()
            if len(maxDamage)>0:
                maxDamage=(maxDamage[0][0]-10)
            else:
                maxDamage=50
                
            if player_carry_att_speed_hp_fatique()[0][1]>=maxDamage:
                #print(maxDamage)
                print('''
You face the cannibal king, good Luck!                
                ''')
                attack()
            else:
                #print(maxDamage)
                sql=(("UPDATE player SET player.x=-1, player.y=-2 WHERE player.ID=1"))
                cur.execute(sql)
                print('''
Cannibal King: \"You no worthy challenger!\"
The Cannibal King strikes you down before you have time to blink.
                ''')
                time.sleep(2)
                timedelay(3, 1)
                print(''' 
You wake up in the church with a headache, turns out the Cannibal King is a good christian not a murderous beast.                
                ''')
                return
    sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x")
    cur.execute(sql)
    result=cur.fetchall()
    
    if len(enemies)>1: #delete all other enemies expect one
        for i in range(len(enemies)-1):
            id=enemies[(i+1)][0]
            sql=("DELETE FROM enemy WHERE id=%i" % id)
            cur.execute(sql)
    
    elif len(enemies)<1 and (result[0][0]) in [1,2,3,4]:
        sql=("SELECT MAX(enemy.id) FROM enemy")
        cur.execute(sql)
        res=cur.fetchall()
        if len(res)>0:
            #print(res)
            try:
                newId=((res[0][0])+(random.randint(100,9999)))
            except:
                newId=1000
        else:
            newId=1
        spawn=random.randint(1,100)
        enemyTypeId=random.randint(1,10)
        
        if spawn<=enemySpawnRate:
            playerPOS=player_position()
            sql=("INSERT INTO enemy VALUES (%i,%i,%i,%i,1)" % (newId,enemyTypeId,playerPOS[0][0],playerPOS[0][1]) )
            cur.execute(sql)
            despawnCountX+=1
    distanceBetweenYou=random.randint(7,square_side+7)
    sql=(("SELECT enemy.id,enemy_type.id, enemy_type.name,enemy_type.hp,enemy_type.att,enemy_type.speed, terrain_square.type_id, enemy_type.description, enemy_type.description2,enemy_type.seen FROM enemy,enemy_type,player,terrain_square WHERE enemy.type_id=enemy_type.id and player.x=terrain_square.x and player.y=terrain_square.y and enemy.x=terrain_square.x and enemy.y=terrain_square.y"))    
    cur.execute(sql)
    enemies=cur.fetchall()
   
    
    if len(enemies)>0:
        seen=enemies[0][9]
        sql=("UPDATE enemy_type SET seen=1 WHERE id=%i" % enemies[0][1])
        cur.execute(sql)
        #print(enemies)     
        
        timeToReachPlayer=distanceBetweenYou/(enemies[0][5]) #seconds
        
        if (enemies[0][1]) in neutralEnemiesIds:
            action=random.randint(1,10)
            rand=random.choice([1,2,3,4])
            if action==1:
                print("There is a "+enemies[0][2]+" passing you")
            elif action==2:
                if (enemies[0][1])!=10:
                    print("a "+enemies[0][2]+" is running away from you")
                else:
                    print("a "+enemies[0][2]+" is flying past you")
            elif action!=1 or action!=2 or action!=3 or action!=4:
                if enemies[0][1]==8: # squirrle
                    if rand==1:
                        print("a "+enemies[0][2]+" walks past you")
                    elif rand==2:
                        print("a "+enemies[0][2]+" is looking at you")
                    else:
                        print("a "+enemies[0][2]+" is climbing on a tree")
                
                elif enemies[0][1]==10: #owl
                    if rand==1:
                        print("a "+enemies[0][2]+" flew fast past you")
                    elif rand==2:
                        print("a "+enemies[0][2]+" is looking at you weird sitting on the branch ")
                    else:
                        print("a "+enemies[0][2]+" is looking at you like it would like to eat you")
                  
            else:
                print("a "+enemies[0][2]+" is standing still and looking at you")
            
        else:
            #print(str(timeToReachPlayer)+"s")
            #print(str(distanceBetweenYou)+"m")
            
            if distanceBetweenYou<=15:
                if seen>0:
                    print("the "+enemies[0][2]+" sees you")
                else:
                    print(str(enemies[0][7])+" sees you")
                if timeToReachPlayer<=10:
                    if (enemies[0][1])!=3:
                        xxx=1
                        print("it is running towards you aggressively, you don't have time to react")
                    else:
                        xxx=random.randint(1,2)
                        print("it is crawling towards you aggressively, you don't have time to react")
                    if enemies[0][1]==3 and xxx==2:
                        
                        timedelay(3, 0.5)
                        print("but thank god this creature fell in to a hole next to it")
                    else:   
                        combat(enemies[0][2])
                else:
                    #print("but it is moving slowly towards you, and you estimate its gonna reach you in about %is" % (int(timeToReachPlayer)+3))
                    print("but it is moving too slow")
                          
            else:
                if seen>0:
                    rand=random.choice([1,2,3,4])
                    if enemies[0][1]==1: #cannibal
                        if rand==1:  
                            print("a "+enemies[0][2]+" is hitting themeself")
                        else:
                            print("a "+enemies[0][2]+" is eating meat")
                    elif enemies[0][1]==2: #bulky cannibal
                        if rand==1:
                            print("a "+enemies[0][2]+" is flexing")
                        elif rand==2:
                            print("a "+enemies[0][2]+" is doing pushups nearby")
                        elif rand==3:
                            print("a "+enemies[0][2]+" rolled away from you")
                        else:
                            print("a "+enemies[0][2]+" eating meat")
                    elif enemies[0][1]==3: #legless cannibal
                        if rand==1:
                            print("a "+enemies[0][2]+" is hitting themself")
                        elif rand==2:
                            print("a "+enemies[0][2]+" is hitting their head")
                        elif rand==3:
                            print("a "+enemies[0][2]+" is stuck in a pit")
                        else:
                            print("a "+enemies[0][2]+" is eating meat")
                    elif enemies[0][1]==4: #handdles cannibal
                        if rand==1:
                            print("a "+enemies[0][2]+" fell over")
                        elif rand==2:
                            print("a "+enemies[0][2]+" is jumping in circles")
                        elif rand==3 and result[0][0]==2:
                            print("a "+enemies[0][2]+" hitting their head on a tree")
                        else:
                            print("a "+enemies[0][2]+" is eating meat")
                    elif enemies[0][1]==5: # wild hog
                        if rand==1:
                            print("a "+enemies[0][2]+" made sound \"oink oink\" nearby")
                        elif rand==2:
                            print("a "+enemies[0][2]+" squaled nearby")
                        else:
                            print("a "+enemies[0][2]+" noticed you and ran away")
                    elif enemies[0][1]==6 or enemies[0][1]==7: # dog            
                        if rand==1:
                            print("there is a "+enemies[0][2]+" looking at you nearby")
                        elif rand==2:
                            print("you can hear a "+enemies[0][2]+" panting")
                        elif rand==3:
                            print("you hear a woof nearby!")
                        elif rand==4:
                            print("you hear \"Hau hau!\"")
                        else:
                            print("a "+enemies[0][2]+" is eating meat")
                    elif enemies[0][1]==9:
                        if rand==1:
                            print("a "+enemies[0][2]+" eating a squirrel nearby")
                        elif rand==2:
                            print("a "+enemies[0][2]+" is jumping on its hindlegs nearby")   
                        else:
                            print("a "+enemies[0][2]+" walked past you")
                    else:
                        print(enemies[0][2]+" is too far away from you to see properly")
                        
                else:
                    print(str(enemies[0][7])+" is too far away from you to see properly")
    #else:
        #print("No enemy")
                    
def itemString(playerText):
    item=""
    for i in range(len(playerText)):
        if i>=1:
            if i<(len(playerText)-1):
                item+=(playerText[i]+" ")
            else:
                item+=(playerText[i])
    return item

def examine_item(item):
    sql=(("SELECT item_type.description FROM item,item_type WHERE item.type_id=item_type.id and item.player_ID>0 and item_type.name LIKE '"+item+"%' GROUP BY item_type.name"))
    cur.execute(sql)
    result=cur.fetchall()
    if len(result)>0:
        
        print(result[0][0])
    else:
        print("You don't have that kind of item in your inventory")
def examine_enemy(enemy_type):
    sql=(("SELECT enemy_type.description FROM enemy_type WHERE enemy_type.name LIKE '"+enemy_type+"%'"))
    #print(sql)
    cur.execute(sql)
    result=cur.fetchall()
    
    if len(result)>0:
        print(result[0][0])
    else:
        print("There isn't that kind of enemy around.")
def check_enemy_type(enemy_type):
    enemy_type=enemy_type.upper()
    sql = ("SELECT enemy_type.name FROM enemy_type WHERE enemy_type.name LIKE '"+enemy_type+"%'")
    cur.execute(sql)
    result = cur.fetchall()
    for i in range(len(result)):
        if result[i][0].upper() == enemy_type:
            return True
    
    return False

def combineRp():
    print('''
      arrow  + plant        = poison arrow
      string + branches     = bow
      knife  + branches     = spear
      plant  + spear        = toxic spear
       plant + axe          = toxic axe
       sword + plant        = poisoned blade
      shovel + plant        = poisoned shovel
        rake + plant        = poisoned rake
   duct tape + sharp rock   = paperweight
  sharp rock + branches     = stone spear
  rubber band + branches    = slingshot
box of nails + baton        = spiked baton
box of nails + baseball bat = spiked baseball bat
''')

def randomItemDrops():
    x=player_position()[0][0]
    y=player_position()[0][1]
    rand=random.randint(1,100)
    howMany=random.randint(1,3)
    rand2=random.randint(1,10)
    if rand2==1 or rand2 ==2 or rand2==3:
        for i in range(howMany):
            if rand<=50:
                trashItemIds=[58,86,38,17,13,11,10,4,3,2,1,89]
                itemID=random.choice(trashItemIds)
            elif rand<=65:
                commonItemIds=[8,67,12,57,48,35,31,88,91,72,69,34,98,99,106,107,109,110,111]
                itemID=random.choice(commonItemIds)
            elif rand<=70:
                rareItemIds=[6,9,71,47,44,37,76,22,20,50,5,92,93,95,103,105,108]
                itemID=random.choice(rareItemIds)
            elif rand==99:
                legendaryItemIds=[25,19,9,90,49,42,97,100,101,102,104]
                itemID=random.choice(legendaryItemIds)
            else:
                return 
            itemDrop(itemID, x, y)
        if howMany==3:
            print("There's plenty of items here.")
    else:
        return   
def parse(playerInput):
    playerCaps = playerInput.upper()
    filter = [".", ",",":","AN","A","MOVE", "GO", "OUT", "THE", "AND", "TO","SOME","FOR","ON"]
    splitText = split_line(playerCaps)
    playerText = [c for c in splitText if c not in filter]
    
    if len(playerText)<1:
        print("Are you an empty vessel?")
    elif playerText[0]== "K":
        item_delete("branches")
    elif "FIX" not in playerText and "REPAIR" not in playerText and "ADD" not in playerText and playerText[len(playerText)-1] == "BOAT" and len(playerText)>1:
        mangleWithObjects(playerText[:(len(playerText)-1)],playerText[len(playerText)-1].lower())
    elif playerText[len(playerText)-2] != "FROM" and playerText[len(playerText)-2] != "IN" and playerText[len(playerText)-1] in objects and len(playerText)>1:
        mangleWithObjects(playerText[:(len(playerText)-1)],playerText[len(playerText)-1].lower())
        
    elif playerText[0]== "N" or playerText[0]=="NORTH":
        move_north()
    elif (playerText[0])== "S" or playerText[0]=="SOUTH":
        move_south()
    elif (playerText[0])== "W" or playerText[0]=="WEST":
        move_west()
    elif (playerText[0])== "E" or playerText[0]=="EAST":
        move_east()
    elif (playerText[0])== "LOOK" or playerText[0]=="L" or playerText[0]=="WATCH" or playerText[0]=="SEE":
        if len(playerText)>1:
            if (playerText[0])=="LOOK" and (playerText[1])=="NORTH" or (playerText[1])=="SOUTH" or (playerText[1])=="WEST" or (playerText[1])=="EAST":
                extended_look(playerText[1])
        else:
            look()
    elif playerText[0]=="TALK":
        if npc_check()==0:
            print("There's no-one to talk to.")
        else:
            talk(npc_check())
    elif playerText[0]=="RING"and playerText[1]=="BELL":
        if player_position()[0][0]== -1 and player_position()[0][1]==-2:
            print("You ring the bell and it produces a deafening sound that must've been heard in a miles radius.")
            sql="Update terrain_square set restriction='U',description=NULL,1stvisit=NULL where x=-5 and y=-4"
            cur.execute(sql)
            refresh_spawnrate(6)
                   
    elif playerText[0]=="USE":
        if playerText[1]=="PLANK":
            fix_bridge(1)
        elif playerText[1]=="PLANKS":
            fix_bridge()
     #   elif playerText[1]=="":
            
        else:
            print("Can't use that!")
    elif playerText[0]=="ADD":
        if playerText[1]=="PLANK":
            fix_bridge(1)
        elif playerText[1]=="PLANKS":
            fix_bridge()
        else:
            print("Can't add that to anything right now!")
    elif playerText[0]=="FIX":
        if playerText[1]=="BRIDGE":
            fix_bridge()
        else:
            print("Can't fix that!")
    elif (playerText[0])=="I":
        inventory()
    elif (playerText[0])=="DROP" or playerText[0]=="D":
        item=""
        if len(playerText)>1:
            print(playerText)
            item=itemString(playerText)
            print(item)
            drop_item(item)
        else:
            print("You meant drop <item>")
    elif (playerText[0])=="KILL"or playerText[0]=="ATTACK" or playerText[0] =="FIGHT":
        attack()  
    elif (playerText[0])=="COMBINE":
        if len(playerText)>1:
            if playerText[1]=="RECIPES" or playerText[1]=="MENU":
                combineRp()
            else:
                item=itemString(playerText)
                    
                pos=item.find("+")
                if item[(pos-1)]==" " and item[(pos+1)]==" ":
                    newitem=item[:(pos-1)]+item[pos:]
                    print("newitem",newitem)
                    newitem2=newitem[:(pos)]+newitem[(pos+1):]
                
                elif item[(pos-1)]==" " and item[(pos+1)]!=" ":
                    newitem=item[:(pos-1)]+item[pos:]
                    print("newitem",newitem)
                    newitem2=newitem[:(pos)]+newitem[(pos):]
                
                elif item[(pos-1)]!=" " and item[(pos+1)]==" ":
                    newitem=item[:(pos)]+item[pos:]
                    print("newitem",newitem)
                    newitem2=newitem[:(pos+1)]+newitem[(pos+2):]
                else:
                    newitem2=item
                
                pos2=newitem2.find("+")    
                item1=newitem2[0:pos2]
                item2=newitem2[(pos2+1):len(newitem2)]
                
                list=[item1,item2]
                combine(list)
        else:
            print("You meant? combine <item>+<item>")
            
    elif (playerText[0])=="TIME":
        show_time()
    elif (playerText[0])=="EQUIP"or playerText[0]=="EQ":
        item=""
        if len(playerText)>1:
            for i in range(len(playerText)):
                if i>=1:
                    if i<(len(playerText)-1):
                        item+=(playerText[i]+" ")
                    else:
                        item+=(playerText[i])
            equip(item)
        else:
            print("You meant equip item?")
    elif (playerText[0])=="UNEQUIP"or playerText[0]=="UNEQ":
        item=""
        if len(playerText)>1:
            for i in range(len(playerText)):
                if i>=1:
                    if i<(len(playerText)-1):
                        item+=(playerText[i]+" ")
                    else:
                        item+=(playerText[i])
            unEquip(item)
        else:
            print("You meant unequip item?")
    elif (playerText[0])== "EXAMINE"or playerText[0]=="ANALYZE" or playerText[0]=="STUDY":
        if len(playerText)>1:
            if(playerText[1])== "AREA":
                examine_area()
            else:
                item=itemString(playerText)
                if check_item_type(item)==True:
                    examine_item(item)
                elif check_enemy_type(item)==True:
                    examine_enemy(item)
                else:
                    print("You meant examine <area>/<item>/<enemy>")
        else:
            print("You meant examine <area>/<item>/<enemy>")
    elif (playerText[0])=="STATS"or playerText[0]=="PLAYER":
        player_stats()
    elif (playerText[0])=="HELP" or playerText[0]=="INFO":
        help()
    elif (playerText[0])=="EAT":
        item=""
        if len(playerText)>1:
            for i in range(len(playerText)):
                if i>=1:
                    if i<(len(playerText)-1):
                        item+=(playerText[i]+" ")
                    else:
                        item+=(playerText[i])
            eat(item)
        else:
            print("You meant? eat 'name of item'")
    elif (playerText[0])=="SLEEP":
        if len(playerText)>1:
            
            sleep(int(playerText[1]))
        else:
            sleep(6)
    elif playerText[0] == "TAKE" or playerText[0] =="PICK" or playerText[0] =="PICKUP" or playerText[0] =="GRAB" or playerText[0]=="T":
        item=""
        if playerText[len(playerText)-1] in objects and playerText[len(playerText)-2]== "FROM":
            if playerText[1] == "UP":
                for i in range(len(playerText)):
                    if i>=2:
                        if i<(len(playerText)-3):
                            item+=(playerText[i]+" ")
                item+=(playerText[len(playerText)-3])
                print(item)
                if check_item_type(item)==True:
                    retrieve(playerText[len(playerText)-1].lower(),item.lower())
                else:
                    print("There isn't such an item")
            
            else:
                for i in range(len(playerText)):
                    if i>=1:
                        if i<(len(playerText)-3):
                            item+=(playerText[i]+" ")
                item+=(playerText[len(playerText)-3])
                print(item)
                if check_item_type(item)==True:
                    retrieve(playerText[len(playerText)-1].lower(),item.lower())
                else:                   
                    print("There isn't such an item")
                
        elif len(playerText)>1 and playerText[1] == "UP":
            for i in range(len(playerText)):
                if i>=2:
                    if i<(len(playerText)-1):
                        item+=(playerText[i]+" ")
                    else:
                        item+=(playerText[i])
            
            if check_item_type(item)==True:
                pick_up(item)
            
        else:
            for i in range(len(playerText)):
                if i>=1:
                    if i<(len(playerText)-1):
                        item+=(playerText[i]+" ")
                    else:
                        item+=(playerText[i])
            
            if check_item_type(item)==True:
                pick_up(item)
            else:
                print("There isn's such a item")
    elif playerText[0]=="STORE"or playerText[0]=="PUT"or playerText[0]=="PLACE":
        item=""
        if playerText[len(playerText)-1]in objects and playerText[len(playerText)-2]=="IN":
            for i in range(len(playerText)):
                if i>=1:
                    if i<(len(playerText)-3):
                        item+=(playerText[i]+" ")
            item+=(playerText[len(playerText)-3])
        
            if check_item_type(item)==True:
                if playerText[len(playerText)-1] in storables:
                    store(playerText[len(playerText)-1].lower(),item.lower())
                else:
                    print("You can't store anything in there!")
            else:                   
                print("There isn't such an item")
                if "MEAT" in playerText:
                    print("Be more specific about the meat")
        else:
            print("What do you want me to store it in?")    
    elif (playerText[0])== "READ":
        item=""
        for i in range(1,len(playerText)):
            if i<(len(playerText)-1):
                item+=(playerText[i]+" ")
            else:
                item+=(playerText[i])
        if check_item_type(item)==True:
            read(item)
            
    else:
        print("Not understood")
print('''

██╗    ██╗██╗  ██╗██╗███████╗██████╗ ███████╗██████╗ ██╗███╗   ██╗ ██████╗     ██████╗ ███████╗███████╗██╗   ██╗ ██████╗ ███████╗
██║    ██║██║  ██║██║██╔════╝██╔══██╗██╔════╝██╔══██╗██║████╗  ██║██╔════╝     ██╔══██╗██╔════╝██╔════╝██║   ██║██╔════╝ ██╔════╝
██║ █╗ ██║███████║██║███████╗██████╔╝█████╗  ██████╔╝██║██╔██╗ ██║██║  ███╗    ██████╔╝█████╗  █████╗  ██║   ██║██║  ███╗█████╗  
██║███╗██║██╔══██║██║╚════██║██╔═══╝ ██╔══╝  ██╔══██╗██║██║╚██╗██║██║   ██║    ██╔══██╗██╔══╝  ██╔══╝  ██║   ██║██║   ██║██╔══╝  
╚███╔███╔╝██║  ██║██║███████║██║     ███████╗██║  ██║██║██║ ╚████║╚██████╔╝    ██║  ██║███████╗██║     ╚██████╔╝╚██████╔╝███████╗
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚═╝  ╚═╝╚══════╝╚═╝      ╚═════╝  ╚═════╝ ╚══════╝
                                                                                                                                 
Your ship sank in the Atlantic, but you managed to escape with an inflatable boat. You were washed into the shore of a mysterious island,
and your inflatable boat was damaged heavily, so you must survive here for a while at least...
    ''')
def main():
 
    while True:
        if gameOver==0:
            #out_of_breath()
            #print(player_carry())
            playerInput = input()
            parse(playerInput)
            change_spawnrate()
            change_fatigue()
            main()
        else:
            return  
main()
