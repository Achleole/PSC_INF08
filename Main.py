import os 
import Univers
import NextSite
from Enregistrement import *
from CPU import *
import Instructions
import CPU
import Statistiques
import NextSite
import Experiment

e = Experiment.Experiment()
e.setFolderName("experiences_16_avril")
TM = [500]
e.experiment1(TM)