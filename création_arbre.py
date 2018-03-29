from replay import *


def creer_arbres(univ,fichier):
  replay=Replay()  
  replay.univers=univ
  replay.openLoad(fichier)
  

  famille_cpus=dict()
  arbres=dict()
  for k in replay.univers.liste_cpus:
    arbres[k.id]=dict()
    loc_cpus[k.id]=[k.id,1]
    arbres[k.id][1]=[k.univers.memoire[k.ptr]]
  
  for j<n:
    replay.tourSlicer()
    for k,ind in enumerate(k.univers.liste_cpus,1):
      branche=arbres[loc_cpus[k.id][0]][loc_cpus[k.id][1]]
      if branche[-1]="NEW":
        loc_cpus[k.id][1]=2*loc_cpus[k.id][1]
        loc_cpus[k.univers.liste_cpus[ind].id]=[loc_cpus[k.id][0],2*loc_cpus[k.id][1]+1]
        arbres[loc_cpus[k.id][0]][loc_cpus[k.id][1]]=[k.univers.memoire[k.ptr]
        arbres[loc_cpus[k.univers.liste_cpus[ind].id][0]][loc_cpus[k.univers.liste_cpus[ind].id][1]]=[]
      else:
        branche.add([k.univers.memoire[k.ptr]])
      
      
      
      
