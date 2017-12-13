class InstructionsDict :
    """ est un dictionnaire à double sens contenant les instructions et les entiers associés """
    def __init__(self):
        """Crée un dictionnaire d'instructions vide"""
        intToStr = {}
        strToInt = {}
    
    def addInstr(self, instr, nb):
        """Ajoute une correspondance instruction <-> entier"""
        intToStr[nb] = instr
        strToInt[instr] = nb
        
    def delInstr(self, ins):
        """Supprime une correspondance instruction <-> entier"""
        if type(ins)==int :
            st = intToStr[ins]
            del intToStr[ins]
            del strToInt[st]
        else :
            nb = strToInt[ins]
            del strToInt[ins]
            del intToStr[nb]
    
    def toInts(self, stList):
        """Renvoie une liste d'entiers traduction de la liste d'instructions sous forme de Strings stList"""
        intList = []
        for ins in stList :
            intList.append(strToInt[ins])
        return intList
    
    def toStrings(self, intList):
        """Renvoie une liste d'instructions sous forme de Strings traduction de la liste d'entiers intList"""
        stList = []
        for nb in intList :
            stList.append(intToStr[nb])
        return stList
