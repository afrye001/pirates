from game import event
from game.player import Player
from game.context import Context
import game.config as config
import random

# class Kraken(Context, event.Event): 
#     '''Randomly applies a Kraken to attack your ship if in deeper waters; has potentially catastropic effects.'''
#     def __init__(self): 
#         self.name = 'The Kraken has attacked your ship!'

#     def process(self): 
#         raise NotImplemented("Kraken functionality unimplemented")


class Kraken (Context, event.Event):
    '''Event with the kraken that attacks pirates. Uses parsing to deal with it.'''

    def __init__ (self):
        super().__init__()
        self.name = "the kraken approaches!"
        self.kraken = 1
        self.verbs['run'] = self
        self.verbs['attack'] = self
        self.verbs['help'] = self
        self.result = {}
        self.go = False

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "run"):
            self.go = True
            r = random.randint(1,10)
            if (r < 5):
                self.result["message"] = "the kraken returns to the depths."
                if (self.kraken > 1):
                    self.kraken = self.kraken - 1
            else:
                c = random.choice(config.the_player.get_pirates())
                if (c.isLucky() == True):
                    self.result["message"] = "Luckily, the kraken is disinterested."
                else:
                    self.result["message"] = c.get_name() + " is attacked by the kraken."
                    if (c.inflict_damage (self.kraken, "killed by the kraken's tentacles")):
                        self.result["message"] = ".. " + c.get_name() + " is strangled to death by the kraken!"

        elif (verb == "fight"):
            self.kraken = self.kraken
            self.result["newevents"].append (Kraken())
            self.result["message"] = "the kraken is killed."
            self.go = True
        elif (verb == "help"):
            print ("the kraken will continue to harrass your crew until you run or fight.")
            self.go = False
        else:
            print ("the only options are to either run or fight.")
            self.go = False

    def process (self, world):

        self.go = False
        self.result = {}
        self.result["newevents"] = [ self ]
        self.result["message"] = "default message"

        while (self.go == False):
            print (str (self.kraken) + " the kraken has appeared what do you want to do?")
            Player.get_interaction ([self])

        return self.result


