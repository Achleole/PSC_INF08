class Experiment:
    
    def __init__(self):
        univsList = []
        this.speciesList = []
    
    def simulate(self, ancestor, t) :
        """ Crée un nouvel univers et y fait tourner une nouvelle simulation pour un temps t (en nb de tours de slicer) après avoir placé un ancêtre ancestor """
        univ = Univ()
        univsList.append(univ)
        univ.addIndividual(0, ancestor)
        for i in range(t) :
            univ.roundSlicer()
    
    