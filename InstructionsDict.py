import random

class InstructionsDict :
    """ est un dictionnaire a double sens contenant les instructions et les entiers associes """
    def __init__(self):
        """Cree un dictionnaire d'instructions vide"""
        self.intToStr = {}
        self.strToInt = {}
    
    def initialize(self, list):
        for pair in list :
            self.addInstr(pair[1], pair[0])
    
    def addInstr(self, instr, nb):
        """Ajoute une correspondance instruction <-> entier"""
        self.intToStr[nb] = instr
        self.strToInt[instr] = nb
        
    def delInstr(self, ins):
        """Supprime une correspondance instruction <-> entier"""
        if type(ins)==int :
            st = self.intToStr[ins]
            del self.intToStr[ins]
            del self.strToInt[st]
        else :
            nb = self.strToInt[ins]
            del self.strToInt[ins]
            del self.intToStr[nb]
    
    def toInts(self, stList):
        """Renvoie une liste d'entiers traduction de la liste d'instructions sous forme de Strings stList"""
        intList = []
        for ins in stList :
            intList.append(self.strToInt[ins])
        return intList
    
    def toInt(self, st):
        """Renvoie l'entier traduction de l'instruction sous forme de String st"""
        return self.strToInt[st]
    
    def toStrings(self, intList):
        """Renvoie une liste d'instructions sous forme de Strings traduction de la liste d'entiers intList"""
        stList = []
        for nb in intList :
            stList.append(self.intToStr[nb])
        return stList
    
    def toString(self, nb):
        """Renvoie la String traduction de l'entier nb"""
        if nb not in self.intToStr :
            nb = random.randint(0,self.nbInstructions()-1)
        return self.intToStr[nb]

    def nbInstructions(self):
        return len(self.intToStr)
