class Experiment:
    
    def __init__(self):
        univsList = []
        this.speciesList = []
    
    def simulate(self, ancestor, t) :
        """ Cree un nouvel univers et y fait tourner une nouvelle simulation pour un temps t (en nb de tours de slicer) après avoir placé un ancêtre ancestor """
        univ = Univers()
        univsList.append(univ)
        univ.addIndividual(0, ancestor)
        for i in range(t) :
            univ.executer_cpus()
    
    