import os
import pandas as pd

class Calculator:
    
    __slots__ = ["characters", "characterXP", "encounterXP", "difficulty_level", "adventuring_XP", "monsters"]
    
    DIFFICULTY : dict[str, int] = {
        "easy": 0,
        "medium": 1,
        "hard": 2,
        "deadly": 3
    }
    
    # translating the CR to XP values
    CHALLENGE_RATING_TO_XP : dict[str, int] = {
        "0" : 0,
        "1/8" : 25,
        "1/4" : 50,
        "1/2" : 100,
        "1" : 200,
        "2" : 450,
        "3" : 700,
        "4" : 1100,
        "5" : 1800,
        "6" : 2300,
        "7" : 2900,
        "8" : 3900,
        "9" : 5000, 
        "10" : 5900,
        "11" : 7200,
        "12" : 8400,
        "13" : 10000,
        "14" : 11500,
        "15" : 13000,
        "16" : 15000,
        "17" : 18000,
        "18" : 20000,
        "19" : 22000,
        "20" : 25000,
        "21" : 33000,
        "22" : 41000,
        "23" : 50000,
        "24" : 62000,
        "30" : 155000
    }
    # xp per level and per difficulty
    XP_THRESHHOLD : list[tuple[int, int, int, int]] = [
        (25, 50, 75, 100),
        (50, 100, 150, 200),
        (75, 150, 225, 400),
        (125, 250, 375, 500),
        (250, 500, 750, 1100),
        (300, 600, 900, 1400),
        (350, 750, 1100, 1700),
        (450, 900, 1400, 2100),
        (550, 1100, 1600, 2400),
        (600, 1200, 1900, 2800),
        (800, 1600, 2400, 3600),
        (1000, 2000, 3000, 4500),
        (1100, 2200, 3400, 5100),
        (1250, 2500, 3800, 5700),
        (1400, 2800, 4300, 6400),
        (1600, 3200, 4800, 7200),
        (2000, 3900, 5900, 8800),
        (2100, 4200, 6300, 9500),
        (2400, 4900, 7300, 10900),
        (2800, 5700, 8500, 12700)
    ]
    
    MULTIPLIERS : dict[int, float] = {
        1 : 1.0,
        2 : 1.5,
        3 : 2.0,
        7 : 2.5,
        11 : 3.0,
        15 : 4.0
    }
    
    # how much xp an adventurer should make per level per day
    ADVENTURING_DAY_XP : dict[int, int] = {
        1 : 300,
        2 : 600,
        3 : 1200,
        4 : 1700,
        5 : 3500, 
        6 : 4000,
        7 : 5000,
        8 : 6000,
        9 : 7500,
        10 : 9000,
        11 : 10500,
        12 : 11500,
        13 : 13500,
        14 : 15000,
        15 : 18000,
        16 : 20000,
        17 : 25000,
        18 : 27000,
        19 : 30000,
        20 : 40000
    }
    
    def __init__(self, characters : list[int] | None = None, adventuring_XP : int | None = None) -> None:
        holder = ""
        char_lvl = []
        
        if characters:
            char_lvl = characters
        else:
            while str(holder).lower() != "stop":
                holder = input("Please enter the level of your characters party as a number. When done enter 'stop': ")
                if holder.lower() == 'stop':
                    break
                try:
                    if int(holder) > 20 or int(holder) < 1:
                        print("The levels have to be between 1-20")
                    else:
                        char_lvl.append(int(holder))
                except:
                    print("The char level needs to be a number fomr 1-20")
        
        holder=""
        
        while holder.lower() not in ["easy", "medium", "hard", "deadly"]:
            holder = input("What is the difficulty level of your planned encounter: ")
            
            if holder.lower() not in ["easy", "medium", "hard", "deadly"]:
                print("Must be either 'easy', 'medium', 'hard' or 'deadly'")
                
            
            
        self.difficulty_level : int = self.DIFFICULTY[holder]   
        self.characters : list[int] = char_lvl
        self.characterXP : int = self._calcCharacterXP()
        if adventuring_XP:
            self.adventuring_XP : int = adventuring_XP
        else:
            self.adventuring_XP = self._calcAdventuringXP()
        self.monsters : list[tuple[int, str]] = []
        self.encounterXP : int = 0

    def _calcCharacterXP(self) -> int:
        value = 0
        
        for level in self.characters:
            value += self.XP_THRESHHOLD[level - 1][self.difficulty_level]
            
        return value
    
    def _calcAdventuringXP(self) -> int:
        value = 0
        
        for level in self.characters:
            value += self.ADVENTURING_DAY_XP[level]
        
        return value
    
    def _add_Monster(self, name, xp_value) -> None:
        self.monsters.append((xp_value, name))
        self.encounterXP += xp_value
        
    def _setEncounterXP(self, xp) -> None:
        self.encounterXP = xp
        
    def _getCharacterXP(self) -> int:
        return self.characterXP
    
    def _getEncounterXP(self) -> int:
        return self.encounterXP
    
    def _getMultiplier(self) -> float:
        amount = len(self.monsters)
        print(amount)
        if amount == 0:
            return 1.00
        for i, val in enumerate(list(self.MULTIPLIERS.keys())):
            if amount > val:
                if val == 15:
                    return self.MULTIPLIERS[15] 
                continue
            elif amount == val:
                print(self.MULTIPLIERS[val])
                return self.MULTIPLIERS[val]
            else:
                value = list(self.MULTIPLIERS.keys())
                return_value = value[i-1]
                print(return_value)
                return return_value
        return 0.00
                    
def main():
    #create a calculator instance
    calc = Calculator()
    
    # import all monsters
    mcr = pd.read_csv("Monster_CR.csv")
    
    dungeon_name = input("Please name your dungeon or quest (This will be used as the filename): ")
    with open(f"{dungeon_name}.txt", "w") as dungeon:
        encounter_count = 1
        dungeon.write(f"Dungeonname: {dungeon_name}\n")
        adventurer_XP = calc.__getattribute__("adventuring_XP")
        dungeon.write(f"Adventurer Day XP: {adventurer_XP}\n")
        encounter_ended = False
        start = True
        while not encounter_ended:
            if start:
                dungeon.write(f"Encounter: {encounter_count}\n")
                start = False
                
            monster = ""
            while monster.lower() != 'stop':
                monster = input("Which monster would you like to add to the encounter (type stop to finish): ")
                if monster.lower() == "stop":
                    break
                
                if monster in mcr["Name"].values:
                    check = mcr.loc[mcr["Name"]==monster, "CR"]
                    check = check.values[0]
                    xp_val = calc.CHALLENGE_RATING_TO_XP[check]
                    calc._add_Monster(name=monster, xp_value=xp_val)                    
                    encounter_XP = calc._getEncounterXP()
                    multiplier = calc._getMultiplier()
                    remaining_xp = calc._getCharacterXP() - (encounter_XP * multiplier)
                    if remaining_xp < 0:
                        print("WARNING: Encounter difficulty is now reached.")
                    dungeon.write(f"\tMonster: {monster}, CR: {check}, encounter XP: {encounter_XP * multiplier}, maximum XP: {calc._getCharacterXP()}\n")
                    print(f"\tMonster: {monster}, CR: {check}, encounter XP: {encounter_XP * multiplier}")
                else:
                    print("Unfortunately the monster wasn't found. Did you maybe have a typo?")
            
            more_encounter = input("Do you want to add another encounter? Y/N: ")
            
            while True:
                if more_encounter.lower() == "y":
                    encounter_count += 1
                    start = True
                    chars = calc.characters
                    encounter_XP = calc._getEncounterXP()
                    adventurer_XP = adventurer_XP - encounter_XP
                    dungeon.write(f"\nRemaining adventurer XP: {adventurer_XP}\n\n")
                    print(f"Remaining xp per day: {adventurer_XP}")
                    calc = Calculator(chars)
                    break
                elif more_encounter.lower() == "n":
                    encounter_ended = True
                    break
                else:
                    print("Answer must be either 'y' or 'n'")
                
                                
if __name__ == "__main__":
    main()    