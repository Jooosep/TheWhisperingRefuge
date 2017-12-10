import mysql.connector
from mysql.connector.errors import IntegrityError
import datetime
import random
db = mysql.connector.connect(host="localhost",
                             user="dbuser",
                             passwd="dbpass",
                             db="whispertest",
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
#jne.

NewAreaDescription = [0,"You have arrived at some sort of village, there are multiple small buildings, but no-ones around", "area description","area description","You see a small church building nearby, it is in very poor condition."]
KnownAreaDescription = [0,"You arrive at some kind of small village, you have been here before ","area description", "area description", "You have returned to a familiar area, there is a small church building nearby"]
visitCounter = [0,0,0,0,0,0]


dt=datetime.datetime(1974,6,6,9,0)
square_side=50 #m
movement_multiplier=50
infection_time = dt
infected = True
infection_message=0

objects =["FREEZER","CHEST","BRIEFCASE","DRAWER"]
storables =["FREEZER","CHEST","BRIEFCASE","DRAWER"]
locked=["BRIEFCASE","DRAWER"]

#player max stats
player_carry_capasity=150
player_max_healt=100
player_max_fatique=100
player_max_speed=15
player_max_attack=100
def help():
    print('''    
HELP									                 -Displays all available commands
N, NORTH								               -Player moves North
S, SOUTH 								               -Player moves South
E, EAST									               -Player moves East
W, WEST									               -player moves West
LOOK, L, WATCH, SEE 					         -Tells player's current location
LOOK <compass point>					         -Tells player about the area of compass point 
I, INVENTORY, BAG, ITEMS				       -Prints a list of items player is currently carrying
DROP <ITEM> 							             -Drops the selected item
COMBINE <ITEM> <ITEM>					         -Combines two items to create a new one
TIME 									                 -Tells time to player
EQUIP <ITEM>							             -Player equips selected item for example equip shirt    
UNEQUIP <ITEM>							           -Player unequips selected item for example unequip shirt
EXAMINE, INSPECT, STUDY, ANALYZE 		   -Tells player info about the enemies
EXAMINE AREA							             -Tells player about the current area they are in
STATS, PLAYER, CHARACTER, CHAR			   -Prints current stats of the player
EAT <ITEM> 								             -Player eats selected item for example eat apple
SLEEP <how long>						           -Player sleeps for selected time
TAKE, PICK, PICKUP, GRAB <ITEM>			   -Player picks up the item and it is placed in inventory
KILL, ATTACK, ENGAGE, FIGHT, BATTLE		 -These commands are used in combat to fight enemies
READ <ITEM>   							           -Prints the discription of the item    
    ''')
def infect():
    global infected
    global infection_time
    sql="UPDATE player SET infection = 1"
    cur.execute(sql)
    infection_time = dt
    infected=True
    
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
    potency = random.randrange(0, 15)
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
    res=cur.fetchall
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
    #print(x)
    time=int((distance/(x/(movement_multiplier*movement_dificulty))))
    tdelta=datetime.timedelta(seconds=time)
    global dt
    dt=(dt+tdelta)
    
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
        print("You lost the game!")
    else:
        sql=(("UPDATE player SET player.hp=%d WHERE player.ID=1") % player_max_healt)
        cur.execute(sql)
def update_player_fatique(totalFatique):
    if totalFatique<=player_max_fatique:
        sql=(("UPDATE player SET player.fatique=%d WHERE player.ID=1") % totalFatique)   
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
            
            print("You dropped", result[i][0])
            break
    
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
                print("You cant get more weight to your poor back!")
            break

def player_position():
    sql="SELECT player.x,player.y FROM player"
    cur.execute(sql)
    result=cur.fetchall()
    return result
    
def split_line(text):
    words = text.split()
    return words

def look():
    global x,y
    print("x: %d, y= %d",x,y)
    sql = "Select terrain_type.description FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
    cur.execute(sql)
    res = cur.fetchall()
    print("Your current location is "+ res[0][0])
    sql ="Select terrain_type.name FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y+1"
    cur.execute(sql)
    res=cur.fetchall()
    if len(res)>0:
        print("To the North there is a " + res[0][0])
    sql ="Select terrain_type.name FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y-1"
    cur.execute(sql)
    res=cur.fetchall()
    if len(res)>0:
        print("To the South there is a " + res[0][0])
    sql ="Select terrain_type.name FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x+1"
    cur.execute(sql)
    res=cur.fetchall()
    if len(res)>0:
        print("To the East there is a " + res[0][0])
    sql ="Select terrain_type.name FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x-1"
    cur.execute(sql)
    res=cur.fetchall()
    if len(res)>0:
        print("To the West there is a " + res[0][0])
 
def retrieve(useable,item):
    sql=(("SELECT item_type.name, item.id FROM item,item_type,player,object WHERE item.type_id=item_type.id and player.x=object.x and player.y=object.y and item.object_ID=object.id and object.name='%s'")%(useable))
    cur.execute(sql)
    result=cur.fetchall()
    if object_is_here(useable)==False:
        print(("There's no %s here!")%(useable.lower()))
    elif object_is_open(useable)==False:
        print(("The %s is closed!")%(useable.lower()))
    elif check_object(item,useable):
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
                
                    sql=("UPDATE item SET item.objectid=NULL, item.player_ID=1 WHERE item.id=%i" % item_id)
                    cur.execute(sql)
                    print("You took", result[i][0])
                else:
                    print("You can't get more weight to your poor back!")
                break
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
        sql=(("SELECT item_type.name,item.id,object.id FROM object,item,item_type WHERE item.type_id=item_type.id and item.player_ID>0 and object.name=%s")%(useable.lower()))
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
        
def object_is_open(useable):
    sql=(("select object.open from object where object.name='%s'")%(useable.lower()))
    cur.execute(sql)
    res = cur.fetchall()
    if len(res)>0:
        return True
    else:
        return False
    
def object_is_here(useable):
    sql=(("select object.name from object,player where object.name=%s and (player.ID=object.player_id or (object.x=player.x and object.y=player.y))" )%(useable.lower()))
    cur.execute(sql)
    res = cur.fetchall()
    if len(res)>0:
        return True
    else:
        return False
    
def mangleWithObjects(command,useable):
    global locked
    print(command)
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
                    sql="Update object set open=1 where id=1"
                    cur.execute(sql)
                    print("You opened the %s."%useable)
                    check_object("chest")
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
                break
                
                
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
                print(locked)
                sql="Update object set open=1 where id=4"
                cur.execute(sql)
                check_object("briefcase")
            else:
                print("Your asking for too much here!")
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
                        print("You manage to cut a sizeable hole into the window and proceed to slip in.")
                        if compasspoint=="N":
                            filtered=''.join([c for c in res[0][1] if c not in compasspoint and"4"])
                            sql="Update terrain_square set restriction='%s' where terrain_square.x=player.x and terrain_square.y=player.y+1"%filtered
                            cur.execute(sql)
                            add_time(square_side, res[0][0])
                            sql= "UPDATE player SET player.y = player.y+1"
                            cur.execute(sql)
                            
                        elif compasspoint=="S":
                            filtered=''.join([c for c in res[0][1] if c not in compasspoint and"4"])
                            sql="Update terrain_square set restriction='%s' where terrain_square.x=player.x and terrain_square.y=player.y-1"%filtered
                            cur.execute(sql)
                            add_time(square_side, res[0][0])
                            sql= "UPDATE player SET player.y = player.y-1"
                            cur.execute(sql)
                            
                        elif compasspoint=="W":  
                            filtered=''.join([c for c in res[0][1] if c not in compasspoint and"4"])
                            sql="Update terrain_square set restriction='%s' where terrain_square.x=player.x-1 and terrain_square.y=player.y"%filtered
                            cur.execute(sql)
                            add_time(square_side, res[0][0])
                            sql= "UPDATE player SET player.x = player.x-1"
                            cur.execute(sql)
                        
                        elif compasspoint=="E":  
                            filtered=''.join([c for c in res[0][1] if c not in compasspoint and"4"])
                            sql="Update terrain_square set restriction='%s' where terrain_square.x=player.x+1 and terrain_square.y=player.y"%filtered
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
                        if res[0][1]!= None:
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
                            sql="Update terrain_square set restriction='NE' where terrain_square.x=-12 and terrain_square.y=7"
                            cur.execute(sql)
                            return
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
                            print("This lock is surprisingly tough to pick, you can't manage!")
                        else:
                            print("You don't have any lockpicks!")                                        
                    elif quickParse(answer2)[1]=="OLD" and quickParse(answer2)[2]=="KEY":
                        if specific_item_check("old key"):
                            print("That was the right key, you proceed to open the door!")
                            sql="Update terrain_square set restriction='NES' where terrain_square.x=-9 and terrain_square.y=4"
                            cur.execute(sql)
                            sql="Update terrain_square set restriction='SW' where terrain_square.x=-10 and terrain_square.y=4"
                            cur.execute(sql)
                            return
                        else:
                            print("you don't have such a key!")
                    elif quickParse(answer2)[1]=="TITANIUM" and quickParse(answer2)[2]=="KEY":
                        if specific_item_check("titanium key"):
                            print("That key didn't fit in the padlock!")
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
                            
def move_north():
    global visitCounter
    sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
    cur.execute(sql)
    res=cur.fetchall()
    oldAreaCode=res[0][2]
    if "S" in res[0][1]:
        print("You can't go through a wall, dummy")
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
                else:
                    print("You can't go through a wall, dummy")
            else:
                add_time(square_side, res[0][0])
                sql= "UPDATE player SET player.y = player.y +1"
                cur.execute(sql)
                sql="select terrain_type.name,terrain_square.description,terrain_square.visitcounter,terrain_square.1stvisit,terrain_square.x,terrain_square.y from terrain_type, terrain_square, player where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
                cur.execute(sql)
                res=cur.fetchall()
                currentSquare = res[0][0]
                print("You entered a " + currentSquare)
                if newAreaCode != None and oldAreaCode != newAreaCode:
                    if visitCounter[newAreaCode]<1:
                        print(NewAreaDescription[newAreaCode])
                        visitCounter[newAreaCode]=1
                    else:
                        print(KnownAreaDescription[newAreaCode])
                if res[0][2]==0:
                    sql=(("UPDATE terrain_square set visitcounter=visitcounter+1 where x=%i and y=%i")%(res[0][4],res[0][5]))
                    cur.execute(sql)
                    print(res[0][3])
                if res[0][1]!= None:
                    print(res[0][1])
                if infected:
                    update_infection()
        else:
            print("The ocean is that way,it would be suicide!")
            
def move_south():
    global visitCounter
    sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
    cur.execute(sql)
    res=cur.fetchall()
    oldAreaCode = res[0][2]
    if "N" in res[0][1]:
        print("You can't go through a wall, dummy")
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
                    elif "2" in res[0][1]:
                        open_door1()
                    elif "3" in res[0][1]:
                        open_door2()
                    elif "S4" in res[0][1]:
                        window_enter(res,"S")
                else:
                    print("You can't go through a wall, dummy")
            else:
                add_time(square_side, res[0][0])
                sql= "UPDATE player SET player.y = player.y -1"
                cur.execute(sql)
                sql="select terrain_type.name,terrain_square.description,terrain_square.visitcounter,terrain_square.1stvisit,terrain_square.x,terrain_square.y from terrain_type, terrain_square, player where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
                cur.execute(sql)
                res=cur.fetchall()
                currentSquare = res[0][0]
                print("You entered a " + currentSquare)
                if newAreaCode != None and oldAreaCode != newAreaCode:
                    if visitCounter[newAreaCode]<1:
                        print(NewAreaDescription[newAreaCode])
                        visitCounter[newAreaCode]=1
                    else:
                        print(KnownAreaDescription[newAreaCode])
                if res[0][2]==0:
                    sql=(("UPDATE terrain_square set visitcounter=visitcounter+1 where x=%i and y=%i")%(res[0][4],res[0][5]))
                    cur.execute(sql)
                    print(res[0][3])
                if res[0][1]!= None:        
                    print(res[0][1])
                if infected:
                    update_infection()
        else:
            print("The ocean is that way,it would be suicide!")
            
def move_east():
    global visitCounter
    sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
    cur.execute(sql)
    res=cur.fetchall()
    oldAreaCode=res[0][2]
    if "W" in res[0][1]:
        print("You can't go through a wall, dummy")
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
                    elif "2" in res[0][1]:
                        open_door1()
                    elif "3" in res[0][1]:
                        open_door2()
                    elif "E4" in res[0][1]:
                        window_enter(res,"E")
                else:
                    print("You can't go through a wall, dummy")
            else:
                add_time(square_side, res[0][0])
                sql= "UPDATE player SET player.x = player.x +1"
                cur.execute(sql)
                sql="select terrain_type.name,terrain_square.description,terrain_square.visitcounter,terrain_square.1stvisit,terrain_square.x,terrain_square.y from terrain_type, terrain_square, player where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
                cur.execute(sql)
                res=cur.fetchall()
                currentSquare = res[0][0]
                print("You entered a " + currentSquare)
                if newAreaCode != None and oldAreaCode != newAreaCode:
                    if visitCounter[newAreaCode]<1:
                        print(NewAreaDescription[newAreaCode])
                        visitCounter[newAreaCode]=1
                    else:
                        print(KnownAreaDescription[newAreaCode])
                if res[0][2]==0:
                    sql=(("UPDATE terrain_square set visitcounter=visitcounter+1 where x=%i and y=%i")%(res[0][4],res[0][5]))
                    cur.execute(sql)
                    print(res[0][3])
                if res[0][1]!= None:
                    print(res[0][1])
                if infected:
                    update_infection()
        else:
            print("The ocean is that way,it would be suicide!")
            
def move_west():
    global visitCounter
    sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
    cur.execute(sql)
    res=cur.fetchall()
    oldAreaCode=res[0][2]
    if "E" in res[0][1]:
        print("You can't go through a wall, dummy")
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
                        print("here we have the gate code function")
                    elif "2" in res[0][1]:
                        open_door1()
                    elif "3" in res[0][1]:
                        open_door2()
                    elif "W4" in res[0][1]:
                        window_enter(res,"W")
                else:
                    print("You can't go through a wall, dummy")
            else:
                add_time(square_side, res[0][0])
                sql= "UPDATE player SET player.x = player.x -1"
                cur.execute(sql)
                sql="select terrain_type.name,terrain_square.description,terrain_square.visitcounter,terrain_square.1stvisit,terrain_square.x,terrain_square.y from terrain_type, terrain_square, player where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
                cur.execute(sql)
                res=cur.fetchall()
                currentSquare = res[0][0]
                print("You entered a " + currentSquare)
                if newAreaCode != None and oldAreaCode != newAreaCode:
                    if visitCounter[newAreaCode]<1:
                        print(NewAreaDescription[newAreaCode])
                        visitCounter[newAreaCode]=1
                    else:
                        print(KnownAreaDescription[newAreaCode])
                if res[0][2]==0:
                    sql=(("UPDATE terrain_square set visitcounter=visitcounter+1 where x=%i and y=%i")%(res[0][4],res[0][5]))
                    cur.execute(sql)
                    print(res[0][3])
                if res[0][1]!= None:
                    print(res[0][1])
                if infected:
                    update_infection()  
        else:
            print("The ocean is that way,it would be suicide!")
            
def specific_item_check(name):
    sql="SELECT item_type.name FROM item,item_type,player WHERE item_type.id=item.type_id and item.player_id=player.id and item_type.name='%s'"%name
    cur.execute(sql)
    res=cur.fetchall()
    if len(res)>0:
        return True
    else:
        return False
    
def check_object(useable,item="default"):
    if item=="default":
        sql=(("SELECT item_type.name, item_type.description, object.open FROM object,item,item_type,player,terrain_square WHERE item.type_id=item_type.id and player.x=object.x and item.objectID=object.ID and object.name='%s'")%(useable.lower()))
        cur.execute(sql)
        result=cur.fetchall()
        if result[0][2]==1:
            if len(result)>1:
                print("You found the following items in the '%s'"% useable)
                for i in range(len(result)):
                    print(result[i][0]+" (" + result[i][0] + ")")
            else:        
                print("Its empty!")
        else:
            print("The %s is closed"%useable)
    else:
        sql=(("SELECT item_type.name FROM item,item_type,player,terrain_square WHERE item.type_id=item_type.id and player.x=object.x and player.y=object.y and item.x=object.x and item.y=object.y and object.name=%s and item_type.name = %s")%(useable,item))
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
        
def extended_look_desription(terrainTypeId,distance,frontTerraintypeId):
    x=random.randint(1,2)
    place=((distance*square_side)-(square_side/2))
    if terrainTypeId==0:
        if frontTerraintypeId==3:
            print("There is fall about %im away" % place)
        else:
            print("There is water about %im away" % (place))
    elif terrainTypeId==1:
        if x==1:
            print("ja noin %im paassa nakyy pienta avartunutta valoa" % (place))
        elif x==2:
            print("ja valo pilkistaa noin %im paasta" % (place))
    elif terrainTypeId==2:
        print("Forest starts about %im away" % (place))
    elif terrainTypeId==3:
        print("There is mountains about %im away" % place)
    elif terrainTypeId==4:
        if frontTerraintypeId==1:
            print("There starts beach about %im away" % place)
        else:
            print("There is something yellow on background about %im away" % (place))
    elif terrainTypeId==5:
        if frontTerraintypeId==2:
            print("Forest go thicker %im away" % place)
        else:
            print("There is starts thick Spruce Forest %im away" % place)
    elif terrainTypeId==10 or terrainTypeId==6 or terrainTypeId==7 or terrainTypeId==8 or terrainTypeId==9:
        print("There is some kind of large object blocking the view %im away" % place)
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
                print("There is %s blocking your vission" % result[0][0])
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
                print("There is %s blocking your vission" % result[0][0])
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
                print("There is %s blocking your vission" % result[0][0])
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
                print("Front of you there is",lastResult[0][0])
                sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x+%i" % distance)
                cur.execute(sql)
                result=cur.fetchall()
                if len(result)>0:
                    extended_look_desription(result[0][0],distance,lastResult[0][0])
                else:
                    extended_look_desription(0, distance,lastResult[0][0])
            else:
                print("There is %s blocking your vission" % result[0][0])    
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
        random=random.randrange(0,100)
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
            
            if result[0][5]==2:
                if random<25:
                    if infected:
                        update_infection()
                    else:
                        infect()
            elif result[0][5]==1:
                if random<20:
                    if infected:
                        update_infection()
                    else:
                        infect()
            elif result[0][5]==3:
                if random<50:
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
    #combineItems=[58,10,37,38,57,31,50,6]
    searchProduct={(37,38):39,(57,58):36,(9,58):80,(38,80):81,(31,58):76,(38,50):82,(19,38):83,(20,38):84,(22,38):85,(6,10):86}
    
    try:
        productId=searchProduct[itemids[0],itemids[1]]
        return productId
    except:
        return False
        
    return False
def combine(twoItems):
    print(twoItems)
    itemnames=[]
    for i in range(len(twoItems)):
        itemnames.append(twoItems[i].lower())
    print(itemnames)
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
                sql=(("INSERT INTO item VALUES (%i,%i,0,0,1)") % (newItemsID,productId))
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
                print(totalWeight)
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
def parse(playerInput):
    playerCaps = playerInput.upper()
    filter = [".", ",",":","AN","A","MOVE", "GO", "OUT", "THE", "AND", "TO","SOME","FOR","ON"]
    splitText = split_line(playerCaps)
    playerText = [c for c in splitText if c not in filter]
    print(playerText)
    
    if len(playerText)<1:
        print("Are you an empty vessel?")
        
    elif playerText[len(playerText)-2] != "FROM" and playerText[len(playerText)-2] != "IN" and playerText[len(playerText)-1] in objects:
        print("we found an object")
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
    elif (playerText[0])=="I":
        inventory()
    elif (playerText[0])=="DROP":
        item=""
        for i in range(len(playerText)):
            if i>=1:
                if i<(len(playerText)-1):
                    item+=(playerText[i]+" ")
                else:
                    item+=(playerText[i])
        drop_item(item)
        
    elif (playerText[0])=="COMBINE":
        if len(playerText)>1:
            item=""
            for i in range(len(playerText)):
                if i>=1:
                    if i<(len(playerText)-1):
                        item+=(playerText[i]+" ")
                    else:
                        item+=(playerText[i])
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
            print("You meant? combine item+item")
            
    elif (playerText[0])=="TIME":
        show_time()
    elif (playerText[0])=="EQUIP":
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
    elif (playerText[0])=="UNEQUIP":
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
    elif (playerText[0])== "EXAMINE":
        if len(playerText)>1:
            if(playerText[1])== "AREA":
                    examine_area()
    elif (playerText[0])=="STATS":
        player_stats()
    elif (playerText[0])=="HELP":
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
            print("You ment? eat 'name of item'")
    elif (playerText[0])=="SLEEP":
        if len(playerText)>1:
            
            sleep(int(playerText[1]))
        else:
            sleep(6)
    elif playerText[0] == "TAKE" or playerText[0] =="PICK" or playerText[0] =="PICKUP" or playerText[0] =="GRAB":
        item=""
        if playerText[len(playerText)-1] in objects and playerText[len(playerText)-2]== "FROM":
            if playerText[1] == "UP":
                for i in range(len(playerText)):
                    if i>=2:
                        if i<(len(playerText)-3):
                            item+=(playerText[i]+" ")
                item+=(playerText[len(playerText)-3])
            
                if check_item_type(item)==True:
                    retrieve(playerText[len(playerText)-1],item)
                else:
                    print("There isn't such an item")
            
            else:
                for i in range(len(playerText)):
                    if i>=1:
                        if i<(len(playerText)-3):
                            item+=(playerText[i]+" ")
                item+=(playerText[len(playerText)-3])
        
                if check_item_type(item)==True:
                    retrieve(playerText[len(playerText)-1],item)
                else:                   
                    print("There isn't such an item")
                
        elif playerText[1] == "UP":
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
                    store(playerText[len(playerText)-1],item)
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
        print(item)
        if check_item_type(item)==True:
            read(item)
            
    else:
        print("Not understood")
        
def main():
    while True:
        #out_of_breath()
        #print(player_carry())
        playerInput = input()
        parse(playerInput)
    
main()
