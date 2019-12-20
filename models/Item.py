import re

class Item:
    OPTION_NAME_MASTER_LIST = [
        "ATK",
        "ATK Spd",
        "Crit",
        "Crit DMG",
        "Penetration",
        "Lifesteal",
        "Dodge",
        "P.Dodge",
        "M.Dodge",
        "Block",
        "P.Block",
        "M.Block",
        "DEF",
        "P.DEF",
        "M.DEF",
        "Max HP",
        "ACC",
        "Debuff ACC",
        "CC Resist",
        "Crit Resistance",
        "P.Crit Resistance",
        "M.Crit Resistance",
        "MP Recovery/Sec",
        "MP Recovery/Attack",
        "ERROR"
    ]
    Error_Counter = 0


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.stats_img = None
        self.stats_text_arr = []
        self.option_dictionary = dict()
        for key in Item.OPTION_NAME_MASTER_LIST:
            self.option_dictionary[key] = 0


    def GenerateStatsDictionary(self):
        simplified_arr = [""] * len(self.stats_text_arr)
        for i in range(0, len(self.stats_text_arr)):
            simplified_arr[i] = re.sub("^Option: ","", self.stats_text_arr[i])
            simplified_arr[i] = re.sub(" \+*\d+[\.,]*\d*%*$", "", simplified_arr[i])

            if(simplified_arr[i] in Item.OPTION_NAME_MASTER_LIST):
                self.option_dictionary[simplified_arr[i]] = self.option_dictionary[simplified_arr[i]] + 1
            else:
                print("=============== E R R O R ===================")
                print("Could not find the option name: {}".format(simplified_arr[i]))
                print("=============================================")
                self.option_dictionary["ERROR"] = self.option_dictionary["ERROR"] + 1

        return self.option_dictionary

    def GetStats(self):
        result = ""
        for key in self.option_dictionary.keys():
            if(self.option_dictionary[key] > 0):
                result = result + key + ", "
        return result

    def IsError(self):
        dic = self.GenerateStatsDictionary()
        self.GetStats()
        print("------------------------------------")
        print("[IsItemUseful] Checking : {}".format(self.GetStats()))
        if (self.option_dictionary["ERROR"] > 0):
            Item.Error_Counter = Item.Error_Counter + 1
            print("[IsItemUseful] Found an error.... {} ".format(Item.Error_Counter))
            return True
        return False

    def IsUseful(self):
        dic = self.GenerateStatsDictionary()
        self.GetStats()
        print("------------------------------------")
        print("[IsItemUseful] Checking : {}".format(self.GetStats()))
        if(self.option_dictionary["ERROR"] > 0):
            Item.Error_Counter = Item.Error_Counter + 1
            print("[IsItemUseful] Found an error.... {} ".format(Item.Error_Counter))
            return True

        if(dic['ATK'] + dic['Crit DMG'] >= 2):
            if (dic['ATK'] + dic['Crit DMG'] >= 3): #God Tier
                return True
            if (dic['Crit'] >= 1):
                return True
            if (dic['Penetration'] >= 1):
                return True
            if (dic['ATK Spd'] >= 1):
                return True
            if (dic['MP Recovery/Attack'] >= 1):
                return True
            if (dic['Lifesteal'] >= 1): ## Probably don't need this....
                return True

        if(dic['MP Recovery/Attack'] + dic['ATK Spd'] >= 3): #Niche?
            return True

        if(dic['P.Block'] + dic['P.DEF'] >= 3): #God Tier
            return True
        if(dic['M.Block'] + dic['M.DEF'] >= 3): #God Tier
            return True
        if (dic['M.Block'] + dic['M.DEF'] + dic['P.Block'] + dic['P.DEF'] +
                dic['Block'] + dic['DEF'] + dic['Max HP'] >= 3):  # Tanky
            return True

        if(dic['Crit Resistance'] + dic['M.Crit Resistance'] + dic['P.Crit Resistance'] >= 4): #Niche?
            return True
        if(dic['CC Resist'] >= 3): #Niche?
            return True
        if(dic['Dodge'] + dic['M.Dodge'] >= 3): #Niche?
            return True
        if(dic['Dodge'] + dic['P.Dodge'] >= 3): #Niche?
            return True

        print("[IsItemUseful] Not useful")
        return False
