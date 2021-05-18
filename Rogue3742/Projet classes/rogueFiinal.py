import random
import copy 
import math 

def heal(creature):
    creature.hp += 3
    return True
    
def teleport(creature, unique):
    orig = theGame().floor.pos(creature)
    dest = None 
    while not isinstance(dest,Coord) and dest == None:
        tempdest= Coord(random.randint(0,theGame().floor.size),random.randint(0,theGame().floor.size))
        if theGame().floor.get(tempdest) == theGame().floor.ground :
            dest = tempdest
            theGame().floor._mat[orig.y][orig.x] = theGame().floor.ground
            theGame().floor._mat[dest.y][dest.x] = creature
            theGame().floor._elem[creature] = dest
        
                
    return unique
    
    
class Element():
    
    def __init__(self,name,abbrv=None,usage=None):
        self.name=name
        if abbrv==None:
            self.abbrv= name[0]
        else:
            self.abbrv= abbrv
        self.usage = usage 
    
    def __repr__(self):
        return self.abbrv
        
    def description(self):
        return "<"+self.name+">"
    
    def meet(self,hero):
        raise NotImplementedError()
    
        
class Creature(Element):
    
    def __init__(self,name,hp,abbrv=None,strength=1):
        Element.__init__(self,name,abbrv)
        self.hp=hp
        self.strength =strength
    
    def description(self):
        return Element.description(self)+"("+str(self.hp)+")"
        
    def meet(self,hero):
        self.hp-=hero.strength
        theGame().addMessage("The " +hero.name+" hits the "+self.description())
        if self.hp<=0:
            return True 
            if not isinstance(self,Hero):
                hero.xp += self.hp + self.strength
                if hero.xp >= 15 + 5 * hero.level :
                    hero.xp= 0
                    hero.levelup()
                    
                    
                    
        return False


class Hero(Creature):
    
    def __init__(self,name="Hero",hp=10,abbrv="@",strength=2):
        Creature.__init__(self,name,hp,abbrv,strength)
        self.xp=0
        self.level=1
        self._inventory=[]
        self.hpmax= hp 
    
    def levelup(self):
        self.hpmax += 2
        self.level+=1
        self.streght+=1
        self.hp = self.hpmax
        
    
    def description(self):
        return Creature.description(self) + str(self._inventory)
    
    def take(self,elem):
        if not isinstance(elem,Equipment):
            raise TypeError("Not a Equipement")
        self._inventory.append(elem)
        
    def fullDescription(self) :
        result=""
        for i in self.__dict__:
            if i != "_inventory":
                result+="> "+i+" : "+str(self.__dict__[i])+"\n"
        result+= "> INVENTORY : "+ str([x.name for x in self._inventory]) 
        return result
        
    def use(self,item):
        if not isinstance(item,Equipment):
            raise TypeError()
        if item not in self._inventory:
            raise ValueError()
        if item.use(self)==True:
            self._inventory.remove(item)

class Equipment(Element):
    
    def meet(self,hero):
        hero.take(self)
        theGame().addMessage("You pick up a "+self.name)
        return True
        
    def use(self,creature):
        if self.usage != None:
            theGame().addMessage("The "+creature.name+" uses the "+self.name)
            return self.usage(creature)
        else: 
            theGame().addMessage("The "+self.name+" is not usable")
            return False
            


class Coord(object):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        
    
    def __eq__(self,other):
        if self.x == other.x and self.y == other.y:
            return True 
        return False 
            
    def __repr__(self):
        return "<"+str(self.x)+","+str(self.y)+">"
        
    def __add__(self,other):
        return Coord(self.x+other.x,self.y+other.y)
        
    def __sub__(self,other):
        return Coord(self.x-other.x,self.y-other.y)
    
    def distance(self,other):
        return math.sqrt((self.x-other.x)**2+(self.y-other.y)**2)
        
    def direction(self,other):
        cos= ((self-other).x)/self.distance(other)
        if cos > 1/math.sqrt(2):
            return Coord(-1,0)
        elif cos < -1/math.sqrt(2):
            return Coord(1,0)
        elif (self-other).y > 0 :
            return Coord(0,-1)
        else :
            return Coord(0,1)
        
        
class Game(object):
    equipments = { 0: [ Equipment("potion","!",usage = heal), Equipment("gold","o") ], 1: [ Equipment("sword"), Equipment("bow"),Equipment("potion","!", usage = lambda creature: teleport(creature,unique=True)) ], 2: [ Equipment("chainmail") ] , 3 : [ Equipment("portoloin","w",usage=lambda creature: teleport(creature,unique=False)),]}
    monsters = { 0: [ Creature("Goblin",4), Creature("Bat",2,"W") ], 1: [ Creature("Ork",6,strength=2), Creature("Blob",10) ], 5: [ Creature("Dragon",20,strength=3) ] }
    _actions= { "z" : lambda hero: theGame().floor.move(hero,Coord(0, -1)), "q" : lambda hero: theGame().floor.move(hero,Coord(-1, 0)),"s" : lambda hero: theGame().floor.move(hero,Coord(0, 1)),"d" : lambda hero: theGame().floor.move(hero,Coord(1, 0)), "i" : lambda hero: theGame().addMessage(hero.fullDescription()), "k" : lambda hero:hero.__setattr__('hp',0)," " : lambda hero:None, "u": lambda hero:hero.use(theGame().select(hero._inventory))} 
    def __init__(self,hero=None,level=1,floor=None):
        if hero == None:
            self.hero=Hero("Hero",10,"@",2)
        else:
            self.hero = hero
        self.level = level 
        self.floor = floor
        self._message = []
        
    
    def buildFloor(self):
        self.floor= Map(hero=self.hero)
    
    def addMessage(self,msg):
        self._message.append(msg)
        
    def readMessages(self):
        chaine = ""
        if len(self._message )!= 0:
            for i in self._message :
                chaine += i+". "
        self._message = []
        return chaine    
        
    def randElement(self,collection):
        X = random.expovariate(1/self.level)
        cles=[]
        for i in collection :
            if i < X :
                cles.append(i)
        liste = collection[max(cles)]
        return copy.copy(random.choice(liste))
                
    def randEquipment(self):
        return self.randElement(self.equipments)
    def randMonster(self):
        return self.randElement(self.monsters)
        
    def select(self,l):
        print("Choose item> "+str([str(l.index(i))+": "+i.name for i in l]))
        x = getch()
        if x.isdigit() and x in [str(l.index(i)) for i in l]:
            return l[int(x)]
        else: 
            return None
        
    def play(self):
        """Main game loop"""
        self.buildFloor()
        print("--- Welcome Hero! ---")
        while self.hero.hp > 0:
            print()
            print(self.floor)
            print(self.hero.description())
            print(self.readMessages())
            c = getch()
            if c in Game._actions:
                theGame()._actions[c](self.hero)
            self.floor.moveAllMonsters()
        print("--- Game Over ---")
       
class Map(object):
    ground = "."
    dir = {"z" : Coord(0,-1) , "s" : Coord(0,1) , "d" :Coord(1,0) , "q" : Coord(-1,0) }
    empty = " "
    
    def __init__(self,size=20,pos=False,hero=None,nbrooms=7):
        self.size = size
        if hero == None:
            self.hero=Hero("Hero",10,"@",2)
        else:
            self.hero=hero
        self.hero._inventory=[]
        
        if type(pos) == bool :
            self.pose = Coord(1,1) 
        elif type(pos) == str:
            self.pose = Coord(int(pos[1]),int(pos[3]))
        else:
            self.pose = pos
        
        self._roomsToReach=[]
        self._rooms=[]
        self._mat=[]
        for i in range(self.size):
            ligne=[]
            for j in range(self.size):
                ligne.append(self.empty)
            self._mat.append(ligne[:])
        self.nbrooms=nbrooms
        self._elem={}
        self.generateRooms(self.nbrooms)
        self.reachAllRooms()
        self._elem={ self.hero : self._rooms[0].center()}
        self._mat[self._rooms[0].center().y][self._rooms[0].center().x] = self.hero
        for r in self._rooms:
            r.decorate(self)
            
    def __repr__(self):
        rep = ""
        for i in range(len(self._mat)):
            l= i 
            for j in range(len(self._mat[0])):
                rep += str(self._mat[l][j])
            rep +="\n"
        
        return rep
        
    def __len__(self):
        return self.size
    
    def __contains__(self,item):
        if isinstance(item,Coord):
            return (item.x < self.size and item.y < self.size and item.x >= 0 and item.y >= 0 )
        if isinstance(item,str):
            return item in self.__repr__()
        if isinstance(item,Element):
            return item in self._elem
            

    def get(self,c):
        self.checkCoord(c)
        return self._mat[c.y][c.x]
        
            
    
    def pos(self,e):
        self.checkElement(e)
        return(self._elem[e])
    
    def put (self,c,e):
        self.checkCoord(c)
        self.checkElement(e)
        if self._mat[c.y][c.x] != self.ground :
            raise ValueError('Incorrect cell')
        if e in self:
            raise KeyError('Already placed')
        self._mat[c.y][c.x]=e
        self._elem[e]=c
    
    def rm(self,c):
        del self._elem[self.get(c)]
        self._mat[c.y][c.x]=self.ground

    def move(self, e, way):
        """Moves the element e in the direction way."""
        orig = self.pos(e)
        dest = orig + way
        if dest in self:
            if self.get(dest) == Map.ground:
                self._mat[orig.y][orig.x] = Map.ground
                self._mat[dest.y][dest.x] = e
                self._elem[e] = dest
            elif self.get(dest) != Map.empty and self.get(dest).meet(e) and self.get(dest) != self.hero:
                self.rm(dest)
                
                
    def addRoom(self,room):
        self._roomsToReach.append(room)
        for i in range(room.c1.x,room.c2.x+1):
            for j in range(room.c1.y,room.c2.y+1):
                self._mat[j][i]=self.ground
            
    def findRoom(self,coord):
        for i in self._roomsToReach:
            if coord in i :
                return i
        return False
        
    def intersectNone(self,room):
        state = True
        for i in self._roomsToReach :
            if room.intersect(i):
                state = False 
        return state
            
            
    def dig(self,coord):
        self._mat[coord.y][coord.x]=self.ground
        for i in self._roomsToReach:
            if coord in i :
                self._rooms.append(i)
                self._roomsToReach.remove(i)
                
    def corridor(self,start,end):
        if start.y<=end.y:
            for i in range(start.y,end.y+1):
                self.dig(Coord(start.x,i))
        else:
            for i in range(start.y,end.y-1,-1):
                self.dig(Coord(start.x,i))
        if start.x<=end.x:
            for i in range(start.x,end.x+1):
                self.dig(Coord(i,end.y))
        else:
            for i in range(start.x,end.x-1,-1):
                self.dig(Coord(i,end.y))
            
        
    def reach(self):
        start= random.choice(self._rooms).center()
        end = random.choice(self._roomsToReach).center()
        self.corridor(start,end)
        
    def reachAllRooms(self):
        self._rooms.append(self._roomsToReach.pop(0))
        while len(self._roomsToReach) != 0 :
            self.reach()
            
    def randRoom(self):
        x1=random.randint(0,len(self._mat[0])-3)
        y1=random.randint(0,len(self._mat)-3)
        coin =Coord(x1,y1)
        x2= x1 + random.randint(3,8) 
        if x2 >= len(self):
            x2 = len(self) -1
        y2 =y1 + random.randint(3,8)
        if y2 >= len(self) :
            y2 = len(self)-1
        return Room(coin,Coord(x2,y2))
        
    def generateRooms(self,n):
        for i in range(n) :
            piece = self.randRoom()
            if self.intersectNone(piece):
                self.addRoom(piece)
                
    
    def checkCoord(self,c):
        if not isinstance(c,Coord):
            raise TypeError('Not a Coord')
        if not c in self:
            raise IndexError('Out of map coord')
    
    def checkElement(self,e) :
        if not isinstance(e,Element):
            raise TypeError('Not a Element')
        
    def moveAllMonsters(self):
        for mon in self._elem :
            if isinstance(mon,Creature) and not isinstance(mon,Hero) :
                self.move(mon,self._elem[mon].direction(self._elem[self.hero]))

    def play(self):
        print("--- Welcome Hero! ---")
        while self.hero.hp > 0:
            print()
            print(self)
            print(self.hero.description())
            self.move(self.hero, Map.dir[getch()])
        print("--- Game Over ---")

        


 
 
class Room():
    def __init__(self,c1,c2):
        self.c1= c1
        self.c2=c2
    
    def __repr__(self):
        return "[<"+str(self.c1.x)+","+str(self.c1.y)+">, <"+str(self.c2.x)+","+str(self.c2.y)+">]"
    
    def __contains__(self,other):
        if self.c1.x<=other.x and other.x<=self.c2.x and self.c1.y<=other.y and other.y<=self.c2.y :
            return True
        return False
    
    def center(self):
        return Coord((self.c2.x+self.c1.x)//2,(self.c2.y+self.c1.y)//2)
    
    def intersect(self, other):
        """Test if the room has an intersection with another room"""
        sc3 = Coord(self.c2.x, self.c1.y)
        sc4 = Coord(self.c1.x, self.c2.y)
        return self.c1 in other or self.c2 in other or sc3 in other or sc4 in other or other.c1 in self
    
    def randCoord(self):
        return Coord(random.randint(self.c1.x,self.c2.x),random.randint(self.c1.y,self.c2.y))
        
    def randEmptyCoord(self,map) :
        accomplished = False
        while not accomplished:
            cord = self.randCoord()
            if map.get(cord) == map.ground and cord != self.center():
                accomplished = True
        return cord
    
    def decorate(self,map) :
        map.put(self.randEmptyCoord(map), theGame().randEquipment())
        map.put(self.randEmptyCoord(map), theGame().randMonster())


 
def getch() :
    """Single char input, only works only on mac/linux/windows OS terminals"""
    try :
        import termios
        # POSIX system. Create and return a getch that manipulates the tty.
        import sys,tty
        fd=sys.stdin.fileno()
        old_settings=termios.tcgetattr(fd)
        try :
            tty.setraw(fd)
            ch=sys.stdin.read(1)
        finally :
            termios.tcsetattr(fd,termios.TCSADRAIN,old_settings)
        return ch
    except ImportError :
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch().decode('utf-8')


def theGame(game=Game()) :
    return game

m=theGame()
m.play()
