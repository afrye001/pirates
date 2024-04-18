
from game import location
import game.config as config
from game.display import announce
from game.events import *
from game.items import Item
import random
import numpy
from game import event
from game.combat import Monster
import game.combat as combat
from game.display import menu

class VolcanoIsland(location.Location): 
    def __init__(self, x, y, w):
        super().__init__(x, y, w)  

        self.name = "volcano island" 
        self.symbol = 'T'
        self.visitable = True
        self.starting_location = BeachWithShip(self)
        self.locations = {}

        self.locations["northBeach"] = NorthBeach(self)
        self.locations["southBeach"] = self.starting_location
        self.locations["eastBeach"] = EastBeach(self)
        self.locations["westBeach"] = WestBeach(self)

        self.locations['ash-forest'] = AshForest(self)
        self.locations['hideout'] = Hideout(self)

        self.locations['great-volcano'] = GreatVolcano(self)


    def enter(self, ship): 
        print("You arrive at a treacherous island with a volcano at it's center. It's sure to have treasure.")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)

        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self


        self.event_chance = 0
        self.events.append(seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())

class EastBeach(location.SubLocation): 
    def __init__(self, m):
        super().__init__(m)
        self.name = "eastBeach" 
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['west'] = self

        self.event_chance = 0
        self.events.append(seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates()) 

    def enter(self): 
        description = "You venture toward the island's east beach, the sand feels hot."
        announce(description) 

    def process_verb(self, verb, cmd_list, nouns): 
        if (verb == "west"): 
            config.the_player.next_loc = self.main_location.locations["ash-forest"]
        if (verb == "south"): 
            config.the_player.next_loc = self.main_location.locations["southBeach"]
        if (verb == "north"): 
            config.the_player.next_loc = self.main_location.locations["northBeach"]

class WestBeach(location.locations): 
    def __init__ (self, m): 
        super().__init__(m)
        self.name = "westBeach"
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['north'] = self

    def enter(self): 
        description = "You venture toward the island's west beach, there seems to be burnt palm trees."
        announce(description) 

    def process_verb(self, verb, cmd_list, nouns): 
        if (verb == "east"): 
            config.the_player.next_loc = self.main_location.locations["ash-forest"]
        if (verb == "south"): 
            config.the_player.next_loc = self.main_location.locations["southBeach"]
        if (verb == "north"): 
            config.the_player.next_loc = self.main_location.locations["northBeach"]

class NorthBeach(location.locations): 
    def __init__(self, m): 
        super().__init__(m)

        self.name = "North Beach"
        self.verbs['west'] = self
        self.verbs['east'] = self
        self.verbs['south'] = self

    def enter(self): 
        description = "You venture toward the island's north beach, the air is dense with smoke from the Volcano."
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["ash-forest"]
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["eastBeach"]
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["westBeach"]

# ash forest 

class AshForest(location.locations): 
    def __init__(self, m): 
        super().__init__(m) 

        self.name = "Ash Forest" 
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

    def enter(self): 
        description = "You venture toward the Ash Forest. \nIt is covered in a thick layer of foggy smoke and its trees are long dead.\nThe Great Volcano lies to the North.\nYou notice a delapidated hideout nearby."
        announce(description) 

    def process_verb(self, verb, cmd_list, nouns): 
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["great-volcano"]
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["eastBeach"]
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["westBeach"]
        if (verb == "enter"):
            config.the_player.go = True
            config.the_player.next_loc = self.main_location.locations["hideout"]

class Hideout(location.locations): 
    def __init__(self, m): 
        super().__init__(m)
        self.name = "hideout"
        self.verbs['exit'] = self
        self.verbs['leave'] = self
        self.verbs['go back'] = self

        self.event_chance = 100
        ## EVENTS GO HERE ## 

class OldWiseManEvent(event.Event):
    def __init__(self):
        super().__init__(m)
        raise NotImplementedError("This planned event 'oldWiseMan' has not been implemented yet.") 
