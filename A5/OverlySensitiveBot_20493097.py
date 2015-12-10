from pdbot import PDBot
import random

class OverlySensitiveBot(PDBot):
    def __init__(self):
        # initialize self
        self.init()    

    def init(self):
        # hardcode give and take chance
        self.give_chance = 0.35

        # trust point system, exponent of trusting_factor
        self.trust_point = 0
        # trusting factor, how much the bot
        # trusts more for every give of the other player
        self.trusting_factor = 1.1

        # hurt factor, how much trust is lost everytime
        # the other player takes
        self.hurt_factor = 2

    def get_play(self):
        if random.uniform(0,1) <= self.give_chance:
            # give for self.give_chance percent of the time
            return "give 2"
        else:
            # take for (1- self.take_chance) percent of the time
            return "take 1"

    def make_play(self, other_play):
        if other_play == "give 2":
            self.trust_point+= 1
            take_chance = 1 - self.give_chance
            self.give_chance*= self.trusting_factor ** self.trust_point
            self.give_chance = (self.give_chance) / (self.give_chance + take_chance)
        else:
            # 
            self.trust_point/= self.hurt_factor
            # actual calculation is take_chance = (1 - self.give_chance) + self.give_chance
            take_chance = 1
            # "reset" the chances the bot give and takes
            # causes the bot to be more inclined to take
            self.give_chance = (self.give_chance) / (self.give_chance + take_chance)

        print self.give_chance, (1-self.give_chance)
