#!/usr/bin/python3
#                               MIND MAZE
#Roguelike project, by Nino Mulac, Ilane Pelletier, Arwen Duee-Moreau, Hugo Durand, Vaiki Martelli, and Kylian Girard
from time import sleep,time
import random
from typing import *
from tkinter import *
from pynput.mouse import Controller
import copy
import math
def nonefunc(x=0,y=0,z=0):
    "test"
    return

def sign(x : float) -> Literal[-1,1]:
    "Returns the sign of a float"
    if x > 0:
        return 1
    return -1

def heal(creature) -> True:
    """Heals a creature \n
    Deprecated, we will prefer using the Status class"""
    creature.hp+=3
    return True

def teleport(creature, unique : bool) -> bool:
    "Teleports a creature from a place to another in the game's floor"
    f=theGame().floor
    l=len(f)
    c=Coord(random.randint(0,l),random.randint(0,l))
    while f[c]!=Map.empty:
        c=f[Coord(random.randint(0,l),random.randint(0,l))]
    f.move(creature,c-f.pos(creature))
    return unique

def getch():
    """Single char input, only works only on mac/linux/windows OS terminals"""
    try:
        import termios
        # POSIX system. Create and return a getch that manipulates the tty.
        import sys, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch().decode('utf-8')

def tir(unique):
    devant= theGame().floor._elem[theGame().floor.hero]
    i=5
    while(((devant+theGame().floor.hero.facing) in theGame().floor) and theGame().floor.get(devant+theGame().floor.hero.facing) in theGame().floor.listground and i!=0):
        devant+=theGame().floor.hero.facing
        i-=1
    if ((devant+theGame().floor.hero.facing) in theGame().floor) and isinstance(theGame().floor.get(devant+theGame().floor.hero.facing),Hero):
        #theGame().floor.get(Devant+theGame().floor.hero.facing).meet(hero)
        if theGame().floor.get(devant+theGame().floor.hero.facing).meet(theGame().floor.hero) == True:
            theGame().floor.rm(devant+theGame().floor.hero.facing)

def jet(unique):
    "Throw the item"
    Devant= theGame().floor._elem[theGame().floor.hero]+theGame().floor.hero.facing
    i=5
    while((Devant+theGame().floor.hero.facing in theGame().floor) and theGame().floor.get(Devant+theGame().floor.hero.facing)in theGame().floor.listground and i!=0):
        Devant+=theGame().floor.hero.facing
        i-=1
    if ((Devant+theGame().floor.hero.facing) in theGame().floor) and isinstance(theGame().floor.get(Devant+theGame().floor.hero.facing),Creature):
        theGame().floor.get(Devant+theGame().floor.hero.facing).action+=8
    elif ((Devant+theGame().floor.hero.facing) in theGame().floor) and theGame().floor.get(Devant+theGame().floor.hero.facing)in theGame().floor.listground:
        theGame().floor.put(Devant+theGame().floor.hero.facing, Used("used chewing-gum","u"))
    elif ((Devant+theGame().floor.hero.facing) in theGame().floor) and isinstance(theGame().floor.get(Devant+theGame().floor.hero.facing), Equipment) or (Devant+theGame().floor.hero.facing) in theGame().floor and theGame().floor.get(Devant+theGame().floor.hero.facing)== theGame().floor.empty:
       
        theGame().floor.put(Devant,Used("used chewing-gum","u"))
    else:
        theGame().floor.put(Devant, Used("used chewing-gum","u"))
    return unique

class Coord(object):
    "Vec2D object, created by rectangular or polar coordinates(with int coords in normal condition, but if broken, can have floats.(used for the moving anims)"
    def __init__(self,x : int ,y : int ,angle=False,broken=False):
        if not(angle):
            self.x=x
            self.y=y
        else:
            self.x=x*math.cos(y)
            self.y=x*math.sin(y)
        if not(broken):
            self.x=int(self.x)
            self.y=int(self.y)

    def __repr__(self) -> str:
        return "<"+str(self.x)+","+str(self.y)+">"

    def __eq__(self,other) -> bool:
        return self.x==other.x and self.y==other.y

    def __ne__(self,other) -> bool:
        return not(self==other)

    def __add__(self,other):
        if type(other) is Coord:
            return Coord(self.x+other.x,self.y+other.y)
        if (type(other) is int) or (type(other) is float):
            return Coord(self.x+other,self.y+other)

    def __neg__(self):
        return Coord(-self.x,-self.y)

    def  __mul__(self,other):
        if type(other) is Coord:
            return Coord(self.x*other.x,self.y*other.y)
        if (type(other) is int) or (type(other) is float):
            return Coord(self.x*other,self.y*other)

    def __sub__(self,other):
        if type(other) is Coord:
            return Coord(self.x-other.x,self.y-other.y)
        if (type(other) is int) or (type(other) is float):
            return Coord(self.x-other,self.y-other)

    def __abs__(self):
        return Coord(abs(self.x),abs(self.y))

    def __floordiv__(self,other):
        if type(other) is Coord:
            return Coord(self.x/other.x,self.y/other.y)
        if (type(other) is int) or (type(other) is float):
            return Coord(self.x/other,self.y/other)

    def __truediv__(self,other):
        if type(other) is Coord:
            return Coord(self.x/other.x,self.y/other.y)
        if (type(other) is int) or (type(other) is float):
            return Coord(self.x/other,self.y/other)

    def __len__(self) -> float:
        return math.sqrt(self.x**2+self.y**2)

    def __lt__(self,other) -> bool:
        if type(other) is Coord:
            return len(self)<len(other)
        if (type(other) is int) or (type(other) is float):
            return len(self)<other

    def __gt__(self,other) -> bool:
        if type(other) is Coord:
            return len(self)>len(other)
        if (type(other) is int) or (type(other) is float):
            return len(self)>other

    def __le__(self,other) -> bool:
        if type(other) is Coord:
            return len(self)<=len(other)
        if (type(other) is int) or (type(other) is float):
            return len(self)<=other

    def __ge__(self,other) -> bool:
        if type(other) is Coord:
            return len(self)>=len(other)
        if (type(other) is int) or (type(other) is float):
            return len(self)>=other

    def __index__(self) -> tuple:
        return (self.x,self.y)

    def distance(self,other) -> float:
        "Diagonal distance between two points"
        return (self-other).__len__()

    def dirtrig(self):
        "Direction from the center to a point"
        if self==Coord(0,0):
            return Coord(0,0)
        cos=self.x/self.__len__()
        if cos>1/math.sqrt(2)-0.1:
            return Coord(-1,0)
        if cos<-1/math.sqrt(2)+0.1:
            return Coord(1,0)
        if self.y>0:
            return Coord(0,-1)
        return Coord(0,1)

    def direction(self,other):
        "Direction from a point to another"
        return (self-other).dirtrig()

    def inverse(self):
        "Inverse of a Coord(swapping x and y)"
        return Coord(self.y,self.x)

    def coin1(self,other):
        "First combinaison of two Coords"
        return Coord(self.x,other.y)

    def coin2(self,other):
        "Second combinaison of two Coords"
        return Coord(other.x,self.y)

    def middle(self,other):
        "Middle of two Coords"
        return (self+other)//2

    def facing(self):
        "Function to choose the correct direction of an image"
        #cp=Coord(self.x,self.y/2)
        cp=self.dirtrig()
        if cp==Coord(0,0):
            return 0
        if cp==Coord(0,-1):
            return 0
        if cp==Coord(0,1):
            return 1
        if cp==Coord(1,0):
            return 2
        if cp==Coord(-1,0):
            return 3

class Status(object):
    "Status affecting a creature each turn, making her losing points from a stat"
    def __init__(self,name,effect,cible="hp",prb=1):
        self.name=name
        self.cible=cible
        self.effect=effect
        self.prb=prb

class Element(object):
    "Basic Element of the roguelike"
    def __init__(self,name,abbrv=None,transparent=False,f=False):
        self.name=name
        self.transparent=transparent
        if abbrv==None:
            self.abbrv=name[0]
        else:
            self.abbrv=abbrv
        self.f=f

    def __repr__(self) -> str:
        return self.abbrv

    def description(self) -> str:
        "Description of the Element"
        return "<{}>".format(self.name)

    def meet(self,hero):
        "Warning! Not defined for Elements yet!"
        raise NotImplementedError("Not implemented yet")

    def accord(self):
        return f"e {self.name}" if self.f else f" {self.name}"

class Decoration(Element):
    def __init__(self,name,abbrv=None,transparent=False):
        Element.__init__(self,name,abbrv,transparent)

    def meet(self,other):
        return False

    #def __eq__(self,other):
    #    return self.name==other.name

class Creature(Element):
    "Element with hps and strength, movable in a Map"
    def __init__(self,name,hp,abbrv=None,strength=1,defense=0,inventory=[],equips=[None,None,None,None],bourse=0,vitesse=1,level=1,action=0,power=None):
        Element.__init__(self,name,abbrv,transparent=True)
        self.hp=int(hp*(1.5**level))
        self.hpmax=self.hp
        self.level=level
        self.strength=int(strength*(1.5**level))
        self.defense=int(defense*(1.5**level))
        self.xp=(self.hp+3*self.strength)*level
        self.bourse=bourse
        self._inventory=inventory
        self.equips=equips
        self.listeffects=[]
        self.dpl=[]
        self.vitesse=vitesse
        self.facing=Coord(0,0)
        self.action=action
        self.power=power

    def description(self) -> str:
        "Description of the Creature"
        return Element.description(self)+f"({self.hp})*{self.level}*"

    def meet(self,other) -> bool:
        "Encounter between two creatures: the first(self) is attacked by the second(other)"
        self.hp-=(other.strength-random.randint(0,self.defense))
        if other.power!=None:
            self.listeffects.append(other.power)
        theGame().addMessage(f"Le {other.name} hits le {self.description()}")
        if self.hp<=0:
            return other.gainxp(self)
        return False

    def statuslose(self,status : Status):
        "Make the Creature be affected by its statuses"
        if status.cible in self.__dict__:
            if random.random<status.prb:
                self.__setitem__(status.cible,self.__getitem__(status.cible)+status.effect)

    def creaturn(self):
        "Move a creature where it has to go, and affect it with its statuses"
        #if len(self.dpl)==0:
            #recalculer l'itinéraire
            #print("jesépakoifer")
        #theGame().floor.move(self,self.dpl[0])
        #self.dpl.pop(0)
        self.action-=1
        for status in self.listeffects:
            if not(status.permanent):
                self.statuslose(status)

    def take(self,equip)-> True:
        "Taking an Equipment: we add it to the Creature's inventory"
        if isinstance(equip,Equipment):
            if  len(self._inventory)<=9:
                self._inventory.append(equip)
                return True
            return False
        raise TypeError

    def gainxp(self,creature):
        "Killing a Creature makes you gain xp."
        self.xp+= creature.xp
        if self.xp>=5+5*self.level:
            self.xp=0
            self.levelup()
        return True

    def levelup(self):
        "Level up : stats are increased"
        self.hpmax+=2
        self.level+=1
        self.strength+=1
        self.hp=self.hpmax
        theGame().addMessage(f"Le {self.description} a gagné un niveau!(niveau {self.level})")

    def throw(self,equip):
        "Throw the item"
        devant= theGame().floor._elem[self]+self.facing
        i=5
        while((devant+self.facing in theGame().floor) and theGame().floor.get(devant+self.facing)in Map.listground and i!=0):
            devant+=self.facing
            i-=1
        if ((devant+self.facing) in theGame().floor) and isinstance(theGame().floor.get(devant+self.facing),Creature):
            theGame().floor.get(devant+self.facing).action+=8
        elif ((devant+self.facing) in theGame().floor) and theGame().floor.get(devant+self.facing)in Map.listground:
            theGame().floor.put(devant+theGame().floor.hero.facing, equip if equip.used=="idem" else equip.used)
        elif ((devant+self.facing) in theGame().floor) and (isinstance(theGame().floor.get(devant+self.facing), Equipment) or theGame().floor.get(devant+self.facing)==Map.empty):
            theGame().floor.put(devant,equip if equip.used=="idem" else equip.used)
        else:
            theGame().floor.put(devant,equip if equip.used=="idem" else equip.used)
        self._inventory.remove(equip)

class Pills(Element):
    "Pills are the game's money: we find them randomly in the game, they have a value according to their gold value."
    def __init__(self,name,abbvr=None,usage=None,transparent=True, valeur_pillule=0):
        Equipment.__init__(self,name,abbvr,usage,transparent)
        self.valeur_pillule=valeur_pillule

    def meet(self, creature : Creature):
        "Meet a pill: we add her value to our bourse."
        theGame().addMessage(f"Tu as ramassé des médicaments (tu les mets dans tes poches)")
        creature.bourse+=self.valeur_pillule
        return True

class Equipment(Element):
    "Pickable and usable Element"
    def __init__(self,name,abbvr=None,usage=None,transparent=True,enchant=[],f=False,used=None):
        Element.__init__(self,name,abbvr,transparent,f)
        self.usage=usage
        self.enchant=enchant
        self.used=used

    def meet(self,creature : Creature) -> True:
        "Meet a equipment: add him to the creature's equipment"
        a=creature.take(self)
        if a:
            theGame().addMessage(f"Tu as ramassé un{self.accord()}")
        else:
            theGame().addMessage(f"Mince, tu n'as plus de place!")
        return a

    def use(self,creature) -> bool:
        "Use an equipment on a creature"
        if self.usage!=None:
            theGame().addMessage(f"The {creature.name} uses the {self.name}")
            return self.usage(creature)
        theGame().addMessage(f"The {self.name} is not usable")
        return False

class Used(Equipment):
   def __init__(self,name,abbrv="", usage=None):
      Equipment.__init__(self, name, abbrv, usage=None)

   def meet(self,creature):
      creature.action+=8
      print(creature.action)
      return True

class Enchant(object):
    "Enchant on upgrade to apply on an Equipment"
    def __init__(self,name="+",effect=None,increase=[("force",1)]):
        self.name=name
        self.effect=effect
        self.increase=increase

    def appy(self,equip : Equipment):
        "Enchanting an Equipment: we increase the attributes targeted and add an effect, if necessary"
        equip.name+=" "+self.name
        for i in self.increase:
            equip.__setitem__(i[0],i[1]+equip.__getitem__(i[0]))
            if self.effect!=None:
                equip.enchant.append(self.effect)

class Hero(Creature):
    "The Hero, controled by the player in the game."
    def __init__(self, name="Hero", hp=37, abbrv="@", strength=2,satiete=20):
        Creature.__init__(self,name,hp,abbrv,strength)
        self.joie=50
        self.tristesse=50
        self.colere=50
        self.peur=50
        self.xp=0
        self.satiete=satiete
        self.tour=0
        self.famine=False
        self.satieteInit=satiete

    def description(self) -> str:
        "Short description of the Hero."
        return Creature.description(self)+"{} ${}".format(self._inventory,self.bourse)

    def __repr__(self) -> str:
        return self.abbrv

    def fullDescription(self) -> str:
        "Long description of the hero, including all his attributes"
        a=self.__dict__
        res=""
        for i in a:
            if i[0]!="_":
                res+=f"> {i} : {a[i]}\n"
        res+="> INVENTORY : "+str([x.name for x in self._inventory])
        return res

    def kill(self) -> None:
        "Function to kill the hero"
        self.hp=0

    def use(self,item : Equipment) -> None:
        "Using an item: we use it with Equipment.use() and remove it from the Hero's inventory if necessary"
        if not(isinstance(item,Equipment)):
            raise TypeError("C'est pas un équipement!")
        if not(item in self._inventory):
            raise ValueError("Tu l'as pas, tu peux pas l'utiliser!")
        if item.use(self):
            self._inventory.remove(item)

    def levelup(self) -> None:
        "Level up : stats are increased"
        self.hpmax+=2
        self.level+=1
        self.strength+=1
        self.hp=self.hpmax
        theGame().addMessage(f"Bien joué! Bravo!! Tu es maintenant niveau {self.level}")

    def food(self) -> None:
        """The food level.
        Decreases every 3 turns, from 20 to 0.
        At 0, the hero loses hp each 3 turns."""
        self.tour+=1
        if self.satiete==0:
            self.famine==True
        if self.satiete>=20:
            self.famine==False
            self.satiete=20
        if self.tour %3==0 and self.satiete>0:
            self.satiete-=1
        if self.tour %3==0 and self.famine==True:
            self.hp-=1

    def sleep(self) -> None:
        listdpl=[Coord(0,-1), Coord(-1,-1), Coord(-1,0), Coord(-1,1), Coord(0,1), Coord(1,1), Coord(1,0), Coord(1,-1)]
        pos=theGame().floor.pos(self)
        for i in listdpl:
            if isinstance(theGame().floor.get(pos+i),Element) and theGame().floor.get(pos+i).name=="lit":
                self.hp+=5
                for _ in range(10):
                    theGame().gameturn("<space>")

class Weapon(Equipment):
    "Equipable Equipment, increasing the creature's strength(Weapon: slot 0 in the Creature's equips)"
    def __init__(self, name, force, durabilite, abbrv="", usage=None,f=False):
        Equipment.__init__(self, name, abbrv,f=f,used="idem")
        self.usage = usage
        self.force=force
        self.durabilite=durabilite

    def equiper(self,creature : Creature) -> None:
        "Equipment of a weapon: we unequip the previous weapon,replace it by the new one, and increase the creature's strength."
        if creature.equips[0]!=None:
            creature.equips[0].desequiper(creature)
        creature.strength+=self.force
        creature.equips[0]=self

    def desequiper(self,creature : Creature) -> None:
        "Unequiping a Weapon: we decrease the creature's force and empty the slot"
        creature.equips[0]=None
        creature.strength-=self.force

    def use(self,creature : Creature) -> True:
        "Using a weapon: equip it and return True to remove it from the inventory."
        self.equiper(creature)
        return True

class Armor(Equipment):
    "Equipable Equipment, increasing the creature's defense(Armor: slot 1 in the Creature's equips)"
    def __init__(self, name, defense, durabilite, abbrv="", usage=None):
        Equipment.__init__(self, name, abbrv,used="idem")
        self.usage = usage
        self.defense=defense
        self.durabilite=durabilite

    def equiper(self,creature : Creature) -> None:
        "Equipment of a armor: we unequip the previous armor,replace it by the new one, and increase the creature's defense."
        if creature.equips[0]!=None:
            creature.equips[1].desequiper(creature)
        creature.hp+=self.defense
        creature.equips[1]=self

    def desequiper(self,creature : Creature) -> None:
        "Unequiping an Armor: we decrease the creature's defense and empty the slot"
        creature.hp-=self.defense
        creature.equips[1]=None

    def use(self,creature : Creature) -> True:
        "Using a armor: equip it and return True to remove it from the inventory."
        self.equiper(creature)
        return True

class Amulet(Equipment):
    "Equipable Equipment, increasing the hero's defense, strength, or other things if needed(Amulet: slot 2 in the Hero's equips)"
    def __init__(self,name,defense=0,force=0,courage=0,abbrv="",usage=None):
        Equipment.__init__(self, name, abbrv,used="idem")
        self.usage = usage
        self.defense=defense
        self.force=force
        self.courage=courage

    def equiper (self,creature : Hero) -> None:
        "Equipment of a amulet: we unequip the previous amulet,replace it by the new one, and increase the hero's stats."
        if creature.equips[0]!=None:
            creature.equips[2].desequiper(creature)
        creature.hp+=self.defense
        creature.strength+=self.force
        creature.courage+=self.courage
        creature.equips[2]=self

    def desequiper (self,creature : Hero) -> None:
        "Unequiping a Amulet: we decrease the hero's stats and empty the slot"
        creature.hp-=self.defense
        creature.strength-=self.force
        creature.courage-=self.courage
        creature.equips[2]=None

    def use(self,creature : Hero) -> True:
        "Using a amulet: equip it and return True to remove it from the inventory. Warning: only the Hero can equip an amulet!"
        if isinstance(creature,Hero):
            self.equiper(creature)
            return True
        raise TypeError("Not a Hero!")

class NPC(Creature):
    "NPC creature, can talk when met."
    def __init__(self, name, hp=100, abbrv="", strength=0, defense=0,actif=None):
        Creature.__init__(self, name, hp, abbrv, strength,defense,actif)
        self.actif=actif

    def meet(self, other) -> None:
        "Adds dialogues in the messages."
        if isinstance(other,Hero):
            if self.actif!=None:
                for i in self.actif:
                    theGame().addMessage(self.name+" : "+ i)

class Seller(NPC):
    "Particular NPC that can sell you Equipments or Actions(<not implemented yet)."
    def __init__(self, name="Infirmière", hp=100, abbrv="M", strength=0,defense=0, actif=["Bonjour, mon loulou. Quel age as tu? Ah oui tu es jeune!","Et qu'as tu dans des poches? Si tu as trouvé des pillules bleus ou jaunes ne les mangent pas!","Vient plutot me les donner, en échange je te donnerai des cookies ou des sucreries.","C'est d'accord?","Alors, as tu trouvé ce type de médicaments?"],dialoguenon=["Ce n'est pas grave loulou, reviens me voir si tu en trouves."],dialogueoui=["Ah oui effectivement, contre quoi veux tu me les échanger?"]):
        NPC.__init__(self, name, hp, abbrv, strength,defense, actif)
        self.dialoguenon=dialoguenon
        self.dialogueoui=dialogueoui
        self.chariot=[]
        for i in range(5):
            self.chariot.append(theGame().randEquipment())

    def meet(self,creature) -> None:
        "Inits the dialogues and waits for the response with bind"
        if isinstance(creature,Hero):
            [theGame().addMessage(self.name+" : "+ i) for i in self.actif]
            theGame().fenetre.bind('b', self.fin_de_discussion())

    def response(self) -> None:
        "shopping not implemented yet"
        [theGame().addMessage(i) for i in self.dialogueoui]

    def fin_de_discussion(self) -> None:
        "Prints dialogs and exits"
        [theGame().addMessage(i) for i in self.dialoguenon]

class Room(object):
    "Room defined by her corner's coord"
    def __init__(self,c1:Coord,c2:Coord):
        self.c1=c1
        self.c2=c2

    def __contains__(self,coord:Coord)->bool:
        "Check if a Coord is in the Room"
        return self.c1.x<=coord.x<=self.c2.x and self.c1.y<=coord.y<=self.c2.y

    def __repr__(self) -> str:
        return f"[<{self.c1.x},{self.c1.y}>, <{self.c2.x},{self.c2.y}>]"

    def center(self) -> Coord:
        "Returns the center of the Room, using the Coord.middle method"
        return self.c1.middle(self.c2)

    def coins(self) -> List[Coord]:
        "Returns a list of all corners from the room"
        return [self.c1,self.c2,self.c1.coin1(self.c2),self.c2.coin1(self.c1)]

    def intersect(self,other) -> bool:
        "Checks if two rooms share Coords"
        for i in self.coins():
            if i in other:
                return True
        for i in other.coins():
            if i in self:
                return True
        return False

    def randCoord(self) -> Coord:
        "Returns a random Coord in the Room."
        return Coord(random.randint(self.c1.x,self.c2.x),random.randint(self.c1.y,self.c2.y))

    def randEmptyCoord(self,map) -> Coord:
        "Returns a coord not assigned to any Element in the Map"
        coord=self.center()
        cc=self.center()
        while coord in map._elem.values() or coord==cc:
            coord=self.randCoord()
        return coord

    def decorate(self,map,seller=True) -> None:
        "Adds random elements in the Room in the Map"
        map.put(self.randEmptyCoord(map),theGame().randEquipment())
        map.put(self.randEmptyCoord(map),theGame().randMonster())
        map.put(self.randEmptyCoord(map),theGame().randDecoration())
        if seller==True:
            map.put(random.choice(map._rooms).randEmptyCoord(map),theGame().randSeller())

class Attack(object):
    "An attack: basically a tile with an animation"
    def __init__(self,name,dmg : int,turns : int,effect : List[Status]) -> None:
        self.dmg=dmg
        self.effect=effect

class Map(object):
    "Map of the Game, where Creatures live."
    ground1="."
    ground2=","
    ground3="`"
    ground4="´"
    listground=[ground1,ground2,ground3,ground4]
    empty=" "
    def __init__(self,size=10,hero=None,nbrooms=10):
        self.nbrooms=nbrooms
        self._rooms=[]
        self._roomsToReach=[]
        if hero==None:
            self.hero=theGame().hero
        else:
            self.hero=hero
        self._mat=[[self.empty for i in range(size)] for k in range(size)]
        self._elem={}
        self._attacks={}
        self.generateRooms(self.nbrooms)
        self.reachAllRooms()
        self.blankmap=[[str(self._mat[j][i]) for i in range(len(self))] for j in range(len(self))]
        self.put(self._rooms[0].center(),self.hero)
        for i in self._elem.keys():
            self._mat[self._elem.get(i).y][self._elem.get(i).x]=i.abbrv
        for i in self._rooms:
            i.decorate(self,i==self._rooms[1])
        self.generateEscalier()

    def __repr__(self) -> str:
        return "\n".join(["".join([str(self._mat[n][k]) for k in range(len(self))]) for n in range(len(self))])+"\n"

    def __len__(self) -> int:
        "Returns the len of the tiles matrix, since the Map is a square"
        return len(self._mat)

    def __contains__(self,item) -> bool:
        "Check, for an element, if it is in _elem, or for a coord, if it is in the map"
        if isinstance(item,Coord):
            return 0<=item.x<=len(self)-1 and 0<=item.y<=len(self)-1
        return item in self._elem.keys()

    def __getitem__(self,item) -> Any:
        "Returns, for an Element, its Coord in the map, and for a Coord, its Element"
        if type(item) is Coord:
            return self.get(item)
        else:
            return self.pos(item)

    def __setitem__(self,cle,valeur)->None:
        "Moves or adds elements to the given Coord."
        if type(cle) is Coord:
            self.put(cle,valeur)
        else:
            if not cle in self:
                self.put(valeur,cle)
            else:
                self.tp(cle,valeur)

    def get(self,coord : Coord, testeroupas=True) -> Element:
        "Returns the Element in the Map having this Coord."
        if testeroupas:
            self.checkCoord(coord)
        for i,j in self._elem.items():
            if j==coord:
                return i
        return self._mat[coord.y][coord.x]

    def pos(self,element : Element) -> Coord:
        "Returns the Coords of an Element"
        self.checkElement(element)
        return self._elem.get(element)

    def groundize(self,coord : Coord) -> None:
        "Puts a ground on a cell.(we have 4 different grounds, and they are saved in blankmap)"
        self._mat[coord.y][coord.x]=self.blankmap[coord.y][coord.x]

    def elementize(self,coord : Coord, abbrv : str) -> None:
        "Puts the abbvr of an Element on the Map."
        self._mat[coord.y][coord.x]=abbrv

    def put(self,coord : Coord,element : Element) -> None:
        "Puts an Element at the given Coord."
        if type(coord) is type(None) or type(element) is type(None):
            return 
        self.checkCoord(coord)
        self.checkElement(element)
        if self[coord]==self.empty or (isinstance(self[coord],Element)) or (isinstance(self[coord],Special_ground)):
            raise ValueError('Incorrect cell')
        if element in self:
            raise KeyError('Already placed')
        self._elem[element]=Coord(coord.x,coord.y)
        self.elementize(coord,element.abbrv)

    def rm(self,element : Element) -> None:
        "Removes the Element from the Map(or the element at the given Coord)"
        if type(element) is Coord:
            self.checkCoord(element)
            self._elem = {key:val for key, val in self._elem.items() if not val == element}
            self.groundize(element)
        else:
            self.groundize(self.pos(self._elem.pop(element)))

    def move(self,element : Element,way : Coord) -> None:
        "Moves an element from a Coord to another relatively, meets the destination."
        coordarr=self.pos(element)+way
        if isinstance(element, Creature):
            element.facing=way
        if coordarr in self:
            if not coordarr in self._elem.values() and self._mat[coordarr.y][coordarr.x] in Map.listground:
                self.groundize(self.pos(element))
                self._elem[element]=coordarr
                self.elementize(coordarr,element.abbrv)
            elif self._mat[coordarr.y][coordarr.x]!=Map.empty:
                if self.get(coordarr).meet(element):
                    self.rm(coordarr)

    def tp(self,element : Element,dest : Coord) -> None:
        "Moves absolutely"
        self.move(element,self.pos(element)-dest)

    def fillrectangle(self,c1:Coord,c2:Coord,thing=empty) -> None:
        "Fills a rectangle of Cords with a given object. For a list, the object will be chosen randomly"
        if type(thing) is list:
            for i in range(c1.x,c2.x+1):
                for j in range(c1.y,c2.y+1):
                    self._mat[j][i]=random.choice(thing)
        else:
            for i in range(c1.x,c2.x+1):
                for j in range(c1.y,c2.y+1):
                    self._mat[j][i]=thing

    def addRoom(self,room:Room) -> None:
        "Adds a Room to the list of rooms to reach, and fills the Map with grounds"
        self._roomsToReach.append(room)
        self.fillrectangle(room.c1,room.c2,Map.listground)

    def findRoom(self,coord : Coord) -> Any:
        "Finds the first Room of the map containing the Coord, returns False if none."
        for i in self._roomsToReach:
            if coord in i:
                return i
        return False

    def intersectNone(self,room : Room) -> bool:
        "Check if any Room on the Map intersects the one we're checking"
        for i in self._roomsToReach:
            if room.intersect(i):
                return False
        return True

    def dig(self,coord : Coord) -> None:
        "Groundizes a Coord, and if it is in a room, removes it from roomToReach."
        self._mat[coord.y][coord.x]=random.choice(self.listground)
        a=self.findRoom(coord)
        if a:
            self._rooms.append(a)
            self._roomsToReach.remove(a)

    def corridor(self,c1 : Coord,c2 : Coord) -> None:
        "Digs from a Coord to another"
        self.dig(c1)
        coord=Coord(c1.x,c1.y)
        while not(coord==c2):
            coord+=self.dircorridor(coord,c2)
            self.dig(coord)

    def dircorridor(self,c1 : Coord,c2 : Coord) -> Coord:
        "Returns the direction to dig to."
        if c1.y!=c2.y:
            return Coord(0,1) if c1.y<c2.y else Coord(0,-1)
        if c1.x!=c2.x:
            return Coord(1,0) if c1.x<c2.x else Coord(-1,0)

    def reach(self) -> None:
        "Digs between two random rooms."
        r1=random.choice(self._rooms)
        r2=random.choice(self._roomsToReach)
        self.corridor(r1.center(),r2.center())

    def reachAllRooms(self) -> None:
        "Reachs all rooms of the Map."
        self._rooms.append(self._roomsToReach.pop(0))
        while len(self._roomsToReach)>0:
            self.reach()

    def randRoom(self) -> Room:
        "Creates a random room"
        x1=random.randint(0,len(self)-3)
        y1=random.randint(0,len(self)-3)
        largeur=random.randint(3,8)
        hauteur=random.randint(3,8)
        x2=min(len(self)-1,x1+largeur)
        y2=min(len(self)-1,y1+hauteur)
        return Room(Coord(x1,y1),Coord(x2,y2))

    def generateRooms(self,n) -> None:
        "Creates n Rooms, and if possible, adds them to the Map (-> puts from 0 to n new Rooms)"
        for i in range(n):
            r=self.randRoom()
            if self.intersectNone(r):
                self.addRoom(r)

    def generateEscalier(self):
        if self.get(self._rooms[0].center()+Coord(0,1))!= self.empty:
            self.rm(self._rooms[0].center()+Coord(0,1))
        self.put((self._rooms[0].center()+Coord(0,1)),Stairs("Monter",">",up=True))
        salle_down= random.choice(self._rooms)
        while salle_down == self._rooms[0]:
            salle_down= random.choice(self._rooms)
        if self.get(salle_down.center()+Coord(0,1)) not in self.listground:
            self.rm(salle_down.center()+Coord(0,1))
        self.put(salle_down.center()+Coord(0,1),Stairs("Descendre","<",up=False))

    def checkCoord(self,coord) -> None:
        "Method to check if an object is a Coord in the Map. Raises errors."
        if not(type(coord) is Coord):
            raise TypeError('Not a Coord')
        if not coord in self:
            raise IndexError('Out of map coord')

    def checkElement(self,elem) -> None:
        "Method to check if an object is an Element. Raises errors."
        if not(isinstance(elem,Element)) and not(isinstance(elem,Special_ground)):
            raise TypeError('Not a Element')

    def moveAllMonsters(self) -> None:
        """Moves all creatures from the map, except the Hero."""
        direction = [Coord(0,1),Coord(0,-1),Coord(1,0),Coord(-1,0),Coord(-1,1),Coord(-1,-1),Coord(1,1),Coord(1,-1)]
        for i in self._elem:
            if isinstance(i,Creature) and not (isinstance(i,Hero) or isinstance(i,NPC)):
                i.creaturn()
                if i.action>0:
                    i.action-=1
                    pass
                if self._elem[i].distance(self._elem[self.hero])<=1 :
                    self.hero.meet(i)
                elif self.get(self._elem[i]+self._elem[i].direction(self._elem[self.hero])) in self.listground or isinstance(self.get(self._elem[i]+self._elem[i].direction(self._elem[self.hero])),Used) :
                    if self._elem[i].distance(self._elem[self.hero])<6 :
                        self.move(i,self._elem[i].direction(self._elem[self.hero]))
                    elif random.randint(0,3)==0:
                        deplacement = random.choice(direction)
                        self.move(i,deplacement)

                else:
                    if self._elem[i].distance(self._elem[self.hero])<6 :
                        posmonstre = self.pos(i)
                        poshero = self.pos(self.hero)
                        new = posmonstre - poshero #permet de savoir quelle direction donner si la premiere ne marche pas

                        if (self.pos(i).direction(self.pos(self.hero))).x != 0:
                            self.move(i,Coord(0,sign(new.x)))
                        else:
                            self.move(i,Coord(sign(new.y),0))
                    elif random.randint(0,3)==0:
                        deplacement = random.choice(direction)
                        self.move(i,deplacement)

class Special_ground(object):
    "Special ground affecting the hero"
    def __init__(self,name,abbrv="#",effect=None):
        self.name=name
        self.abbrv=abbrv
        self.effect=effect

    def __repr__(self) -> str:
        return self.abbrv

class Stairs(Special_ground):
    "Stairs allowing the Hero to change the stage he plays in."
    def __init__(self,name,abbrv="#",effect=True,up=False):
        Special_ground.__init__(self,name,abbrv,effect)
        self.up=up

    def meet(self,hero):
        "Changes the stage where the Hero is."
        if isinstance(hero,Hero):
            if self.up==True:
                if theGame().stage==theGame().first_stage:
                    return
                print("MONTE")
                theGame().addMessage(f"{hero.name} prend les escaliers et monte.")
                theGame().stage=theGame().stage+1
                theGame().floor=theGame().etages[theGame().stage]
                theGame().seenmap=[[Map.empty for i in range(theGame().sizemap+2)] for k in range(theGame().sizemap+2)]

            else:
                print("DESCEND")
                theGame().addMessage(f"{hero.name} prend les escaliers et descend.")
                print(theGame().stage)
                theGame().stage=theGame().stage-1
                theGame().floor=theGame().etages[theGame().stage]
                theGame().seenmap=[[Map.empty for i in range(theGame().sizemap+2)] for k in range(theGame().sizemap+2)]
                #self.placescalier()

class Game(object):
    """The Game class.
    \nPlease use theGame() to remain in the same game..."""
    _actions={"z" : lambda hero : theGame().floor.move(hero,Coord(0,-1)),
              "a" : lambda hero : theGame().floor.move(hero,Coord(-1,-1)),
              "q" : lambda hero : theGame().floor.move(hero,Coord(-1,0)),
              "w" : lambda hero : theGame().floor.move(hero,Coord(-1,1)),
              "x" : lambda hero : theGame().floor.move(hero,Coord(0,1)),
              "c" : lambda hero : theGame().floor.move(hero,Coord(1,1)),
              "d" : lambda hero : theGame().floor.move(hero,Coord(1,0)),
              "e" : lambda hero : theGame().floor.move(hero,Coord(1,-1)),
              "i" : lambda hero : theGame().addMessage(hero.fullDescription()),
              "r" : lambda hero : theGame().hero.sleep(),
              "k" : lambda hero : hero.kill(),
              "<space>" : lambda hero : theGame().tour(),
              "u" : lambda hero : hero.use(theGame().select(hero._inventory)),
              "j" : lambda hero : hero.throw(theGame().select(hero._inventory))}
    monsters = { 0: [ Creature("Goblin",4), Creature("Bat",2,"W") ],
                 1: [ Creature("Ork",6,strength=2), Creature("Blob",10) ],
                 5: [ Creature("Dragon",20,strength=3) ] }
    equipments = { 0: [ Weapon("épée",3,37,"s",f=True),Equipment("gum","g", usage=lambda creature: jet(True),used=Used("used chewing-gum","u")) ,Equipment("potion","!",usage=lambda creature : heal(creature),f=True),Pills("or1","b",valeur_pillule=1)],
                   1: [ Equipment("lance-pierre","a", usage=lambda creature: tir(False)),Equipment("potion","!",usage= lambda creature : teleport(creature,True),f=True) ,Pills("or2","j",valeur_pillule=2)],
                   2: [ Armor("plaid",5,376506), Pills("or5","p",valeur_pillule=5) ],
                   3: [ Equipment("portoloin","w",usage= lambda creature : teleport(creature,False)), Pills("or10","J", valeur_pillule=10)]}
    marchande = { 0: [ Weapon("épée",3,37,"s",f=True),Equipment("gum","g", usage=lambda creature: jet(True),used=Used("used chewing-gum","u")) ,Equipment("potion","!",usage=lambda creature : heal(creature),f=True)],
                   1: [ Equipment("lance-pierre","a", usage=lambda creature: tir(False)),Equipment("potion","!",usage= lambda creature : teleport(creature,True),f=True)],
                   2: [ Armor("plaid",5,376506)],
                   3: [ Equipment("portoloin","w",usage= lambda creature : teleport(creature,False))]}
    decorations = { 0:[Decoration("lit","Be",False)]}
    def __init__(self,hero=None,sizemap=20,stage=10,fl=None):
        self.hero=Hero()
        if hero!=None:
            self.hero=hero
        self.floor=None
        self._message=[]
        self.seenmap=[[Map.empty for i in range(sizemap+2)] for k in range(sizemap+2)]
        self.sizemap=sizemap
        self.viewablemap=[[Map.empty for i in range(self.sizemap+2)] for k in range(self.sizemap+2)]
        self.stage=stage
        self.first_stage=self.stage
        self.etages=[]
        self.level=self.first_stage-self.stage+1

    def buildFloor(self) -> None:
        "Creates the Game's floor."
        for _ in range(10):
            self.etages.append(Map(self.sizemap,nbrooms=int(self.sizemap/2)))
        self.floor=self.etages[0]

    def addMessage(self,msg) -> None:
        "Adds a message to be printed on the screen."
        self._message.append(msg)

    def readMessages(self) -> str:
        "Returns all messages to be printed on the screen"
        if self._message!=[]:
            a=". ".join(self._message)+". "
            self._message=[]
            return a
        return ""

    def randElement(self,collection : dict) -> Element:
        "Returns a copy from an element of a dictionnary in the form {rarity<int> : List[Element],...}"
        x=random.expovariate(1/self.level)
        n=int(x)
        while not(n in collection):
            n-=1
        return copy.copy(random.choice(collection[n]))

    def randEquipment(self) -> Equipment:
        "Returns a random Equipment using randElement"
        return self.randElement(self.equipments)

    def randMonster(self) -> Creature:
        "Returns a random Creature using randElement"
        return self.randElement(self.monsters)

    def randDecoration(self) -> Decoration:
        "Returns a random Equipment using randElement"
        return self.randElement(self.decorations)

    def randSeller(self):
        return Seller()

    def select(self,l : List[Equipment]) -> Equipment:
        """Prints the inventory and uses getch to choose which Equipment to use.
        Not in the graphical interface yet"""
        print("Choose item>",[f"{i}: {l[i].name}" for i in range(len(l))])
        a=getch()
        if a in [str(i) for i in range(len(l))]:
            return l[int(a)]

    def initgraph(self)-> None:
        "Creates the dictionary of images,and binds actions to the Tk window, then creates the mainloop."
        genPATH=__file__
        imgPATH=genPATH[0:-12]+"images/"
        hero_fi=PhotoImage(file=imgPATH+"hero_face_i.png")
        hero_ri=PhotoImage(file=imgPATH+"hero_right_i.png")
        hero_bi=PhotoImage(file=imgPATH+"hero_back_i.png")
        hero_li=PhotoImage(file=imgPATH+"hero_left_i.png")
        hero_fw1=PhotoImage(file=imgPATH+"hero_face_w1.png")
        hero_rw1=PhotoImage(file=imgPATH+"hero_right_w1.png")
        hero_bw1=PhotoImage(file=imgPATH+"hero_back_w1.png")
        hero_lw1=PhotoImage(file=imgPATH+"hero_left_w1.png")
        hero_fw2=PhotoImage(file=imgPATH+"hero_face_w2.png")
        hero_rw2=PhotoImage(file=imgPATH+"hero_right_w2.png")
        hero_bw2=PhotoImage(file=imgPATH+"hero_back_w2.png")
        hero_lw2=PhotoImage(file=imgPATH+"hero_left_w2.png")
        sol_img1=PhotoImage(file=imgPATH+"sol_1.png")
        sol_img2=PhotoImage(file=imgPATH+"sol_2.png")
        sol_img3=PhotoImage(file=imgPATH+"sol_3.png")
        sol_img4=PhotoImage(file=imgPATH+"sol_4.png")
        pot_img1=PhotoImage(file=imgPATH+"fiole_1.png")
        pot_img3=PhotoImage(file=imgPATH+"fiole_3.png")
        bequille_img=PhotoImage(file=imgPATH+"bequille.png")
        chew_img=PhotoImage(file=imgPATH+"chewing-gum.png")
        gum_img=PhotoImage(file=imgPATH+"gum.png")
        ted_img=PhotoImage(file=imgPATH+"ourson_1.png")
        sad_img=PhotoImage(file=imgPATH+"tristesse_1.png")
        or1_img=PhotoImage(file=imgPATH+"or1.png")
        or2_img=PhotoImage(file=imgPATH+"or2.png")
        or5_img=PhotoImage(file=imgPATH+"or5.png")
        or10_img=PhotoImage(file=imgPATH+"or10.png")
        marchand_f=PhotoImage(file=imgPATH+"marchand_de_face.png")
        marchand_f=PhotoImage(file=imgPATH+"marchand_de_face2.png")
        marchand_d=PhotoImage(file=imgPATH+"marchand_vers_droite.png")
        marchand_g=PhotoImage(file=imgPATH+"marchand_vers_gauche.png")
        marchand_sf=PhotoImage(file=imgPATH+"marchand_sucette_de_face.png")
        img_stonelance=PhotoImage(file=imgPATH+"lancepierre.png")
        esc_up=PhotoImage(file=imgPATH+"escalier_up.png")
        esc_down=PhotoImage(file=imgPATH+"escalier_down.png")
        vide = PhotoImage(file=imgPATH+"empty.png").zoom(2)
        hotbar = PhotoImage(file=imgPATH+"hotbar.png").zoom(2)
        faim100 = PhotoImage(file=imgPATH+"faim100.png").zoom(2)
        faim75 = PhotoImage(file=imgPATH+"faim75.png").zoom(2)
        faim50 = PhotoImage(file=imgPATH+"faim50.png").zoom(2)
        faim25 = PhotoImage(file=imgPATH+"faim25.png").zoom(2)
        faim0 = PhotoImage(file=imgPATH+"faim0.png").zoom(2)
        red=PhotoImage(file=imgPATH+"red.png")
        dred=PhotoImage(file=imgPATH+"darkred.png")
        gre=PhotoImage(file=imgPATH+"green.png")
        dgre=PhotoImage(file=imgPATH+"darkgreen.png")
        blu=PhotoImage(file=imgPATH+"blue.png")
        dblu=PhotoImage(file=imgPATH+"darkblue.png")
        yel=PhotoImage(file=imgPATH+"yellow.png")
        dyel=PhotoImage(file=imgPATH+"darkyellow.png")
        lig=PhotoImage(file=imgPATH+"lightblue.png")
        dlig=PhotoImage(file=imgPATH+"darklightblue.png")
        ora=PhotoImage(file=imgPATH+"orange.png")
        dora=PhotoImage(file=imgPATH+"darkorange.png")
        vie =PhotoImage(file=imgPATH+"health.png")
        herobox = PhotoImage(file=imgPATH+"hero_box.png").zoom(3)
        dialoguebox = PhotoImage(file=imgPATH+"dialogue.png")
        self.dicimages={"." : sol_img1,"," : sol_img2,"`" : sol_img3,"´" : sol_img4,"@" : [hero_fi,hero_bi,hero_li,hero_ri],"!" : pot_img3,"G" : ted_img,"W":ted_img,"O":sad_img,"B":ted_img,"D":ted_img,"s":bequille_img, "a" : img_stonelance,"!":pot_img1,"c":pot_img3,"b":or1_img,"j":or2_img,"p":or5_img,"P":or10_img,"M":marchand_f,'inventory':hotbar, 'faim100' : faim100 , 'faim75' : faim75 , 'faim50' : faim50 , 'faim25' : faim25 , 'faim0': faim0, 'empty' : vide , 'herobox' : herobox , 'health' : vie,'dialogue' : dialoguebox.zoom(5), ">" : esc_up, "<" : esc_down,"u":chew_img,"g":gum_img}
        self.dicanim={"@":[hero_fw1,hero_bw1,hero_lw1,hero_rw1,hero_fw2,hero_bw2,hero_lw2,hero_rw2]}
        #dictionnaire pour avoir les images en zoom dans l'inventaire
        self.dicinventory={"@" : hero_fi.zoom(2),"!" : pot_img3.zoom(2), "a" : img_stonelance.zoom(2),"s":bequille_img.zoom(2),"!":pot_img1.zoom(2),"c":pot_img3.zoom(2),"b":or1_img.zoom(2),"j":or2_img.zoom(2),"p":or5_img.zoom(2),"P":or10_img.zoom(2),"g":gum_img.zoom(2)}
        self.dicseen={"dy":dyel,"do":dora,"dl":dlig,"db":dblu,"dg":dgre,"dr":dred}
        self.dicviewable={"ye":yel,"or":ora,"li":lig,"bl":blu,"gr":gre,"re":red}
        self.canvas.config(width=1000,height=800)
        self.seeMap()
        self.updategraph()
        [self.fenetre.bind(i,self.gameturn) for i in self._actions]
        self.canvas.pack()
        self.fenetre.mainloop()

    def gameturn(self,event) -> None:
        "Makes an action according to the bind result"
        poshero=self.floor.pos(self.hero)
        if isinstance(event,Event) and event.char in self._actions:
            self._actions[event.char](self.floor.hero)
        [self.fenetre.bind(i,nonefunc) for i in self._actions]
        self.hero.food()
        self.floor.moveAllMonsters()
        self.seeMap()
        for i in range(3):
            print("TURN")
            self.updategraph(i,[self.floor.pos(self.hero),poshero])
            print(poshero,self.floor.pos(self.hero))
            sleep(0.1)
        [self.fenetre.bind(i,self.gameturn) for i in self._actions]

    def updategraph(self,n=0,position=None) -> None:
        """Main graphic function.
        Displays the map on the canvas, using the images defined in initgraph.
        Then adds the minimap on the corner of the screen (place not defined yet, currently (600,600)).
        And ends the game if the Hero is dead."""
        y=0
        self.canvas.delete("all")
        print(self.floor,"\n".join(["".join([str(self.viewablemap[n][k]) for k in range(self.sizemap)]) for n in range(self.sizemap)])+"\n") #-> debug
        if position==None:
            poshero=self.floor.pos(self.hero)
        else:
            poshero=position[0]+(position[0]-position[1])/(n+1)
        for i in self.viewablemap:
            x=0
            for k in i:
                if k!=Map.empty:
                    self.canvas.create_image(((Coord(x,y)-poshero)*32+Coord(401,400)).__index__(),image=self.dicimages.get(self.floor.blankmap[int(y)][int(x)]))
                if k in self.dicimages:
                    image=self.dicimages.get(k)
                    if type(image) is list:
                        self.canvas.create_image(((Coord(x,y)-poshero)*32+Coord(401,400)).__index__(),image=image[self.hero.facing.facing()] if n==0 else self.dicanim.get(k)[self.hero.facing.facing()+(4*(n-1))])
                    else:
                        self.canvas.create_image(((Coord(x,y)-poshero)*32+Coord(401,400)).__index__(),image=image)
                else:
                    self.canvas.create_text(((Coord(x,y)-poshero)*32+Coord(401,400)).__index__(),text=str(k),font="Arial 16")
                x+=1
            y+=1
        #truc pour l'interface
        if theGame().floor.hero.hp>=1:
            self.canvas.create_image(50 , 400 , image = self.dicimages['inventory'])
            #affiche  le niveau de satiete grace a un cookie
            satiete = theGame().floor.hero.satiete*5
            if satiete >= 100:
                self.canvas.create_image(750,150,image = self.dicimages['faim100'])
            elif satiete >= 75:
                self.canvas.create_image(750,150,image = self.dicimages['faim75'])
            elif satiete >= 50:
                self.canvas.create_image(750,150,image = self.dicimages['faim50'])
            elif satiete >= 25:
                self.canvas.create_image(750,150,image = self.dicimages['faim25'])
            elif satiete > 0:
                self.canvas.create_image(750,150,image = self.dicimages['faim0'])
                #mettre un message comme quoi le niveau de nourriture est bas
            else:
                self.canvas.create_image(750,150,image = self.dicimages['empty'])
                #mettre un message comme quoi le joueur doit manger
            #petite fenetre qui va contenir le personnage
            self.canvas.create_image(870, 160 , image = self.dicimages['herobox'])
        #affichage du niveau de vie
        for i in range (theGame().floor.hero.hp):
            self.canvas.create_image(130+32*(i-20*(i//20)),50+40*(i//20),image = self.dicimages['health'])
        #affichage des objets dans l'inventaire
        place = 0
        for e in theGame().floor.hero._inventory:
            picture = (self.dicinventory.get(e.abbrv))
            self.canvas.create_image(50,45+78*(place),image = picture)
            place = place+1
        y=650
        
        for i in self.seenmap:
            x=800
            for k in i:
                if k!=Map.empty:
                    self.canvas.create_image(x,y,image=self.dicseen.get("dy"))
                x+=4
            y+=4
        y=650
        for i in self.viewablemap:
            x=800
            for k in i:
                if k!=Map.empty:
                    self.canvas.create_image(x,y,image=self.dicviewable.get("ye"))
                x+=4
            y+=4
        #affichage des dialogue dans la boite de dialogue
        self.canvas.create_image(420,710,image = self.dicimages['dialogue'])

        if position == None or n==2:
            self.canvas.create_text(500,750,text=self.readMessages(),font="Arial 25 italic",fill="white")
        #inventaire ecrit: self.canvas.create_text(500,770,text=self.floor.hero.description(),font="Arial 16 italic",fill="white")
        #fin de la boite de dialogue
        self.canvas.pack()
        if theGame().floor.hero.hp<1:
            self.endgame()

    def begingame(self):
        """Inits the Game, creates the Tk window and the Canvas, launches the mainloop by executing initgraph.
        \n Not perfect yet"""
        self.buildFloor()
        #self.mouse=Controller()
        self.fenetre=Tk()
        self.fenetre.title('DG')
        self.fenetre.attributes("-fullscreen",True)
        self.fenetre.configure(background="pink")
        self.canvas=Canvas(self.fenetre,width=1200,height=800,background="black")
        #time.sleep(5)
        self.canvas.place(x=0,y=0)
        self.canvas.create_text(85,120,text="NEW GAME",font="Arial 16 italic",fill="blue")
        #self.bouton_quitter = Button(self.fenetre, text='Quitter', command=self.fenetre.destroy) #util pour le fullscreen
        #self.bouton_quitter.place(x=1200,y=800)
        self.canvas.delete("all")
        self.canvas.destroy()
        #bouton_jouer = Button(self.fenetre,text='Jouer',command=self.beginplay)
        #bouton_jouer.place(x=1500,y=800)
        self.canvas=Canvas(self.fenetre,width=1200,height=800,background="black")
        self.canvas.place(x=0,y=0)
        #bouton_quitter = Button(self.fenetre, text='Quitter', command=self.fenetre.destroy)
        #bouton_quitter.place(x=1200,y=800)
        self.initgraph()

    def endgame(self) -> None:
        "Ends the game"
        self.canvas.delete("all")
        self.canvas=Canvas(self.fenetre,width=1200,height=800,background="black")
        self.canvas.place(x=0,y=0)
        self.canvas.create_text(85,120,text="GAME OVER",font="Arial 16 italic",fill="blue")

    def seeMap(self):
        "Modifies the value of viewablemap and seenmap to match to the tiles viewable and seen."
        theta=0
        self.viewablemap=[[" " for i in range(self.sizemap+2)] for k in range(self.sizemap+2)]
        ch=self.floor[self.floor.hero]
        while theta<=2*math.pi:
            r=0
            cv=Coord(0,0)
            while r<=6 and (ch+cv in self.floor) and (self.floor[ch+cv] in Map.listground or self.floor[self.floor.hero]==ch+cv or (isinstance(self.floor[ch+cv],Element) and self.floor[ch+cv].transparent==True)):
                self.seenmap[(cv+ch).y][(cv+ch).x]=self.floor[cv+ch]
                self.viewablemap[(cv+ch).y][(cv+ch).x]=str(self.floor[cv+ch])
                r+=0.2
                cv=Coord(r,theta,True)
            cv=Coord(r+0.5,theta,True)
            if r<6 and ch+cv in self.floor:
                self.seenmap[(cv+ch).y][(cv+ch).x]=self.floor[cv+ch]
                self.viewablemap[(cv+ch).y][(cv+ch).x]=str(self.floor[cv+ch])
            theta+=math.pi/32

def theGame(game = Game()) -> Game:
    "Returns the Game singleton."
    return game

theGame().begingame()
