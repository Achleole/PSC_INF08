from replay import *


replay.univers=


famille_cpus=dict()
arbres=dict()
for k in liste_cpus:
  arbres[k.id]=dict()
  loc_cpus[k.id]=[k.id,1]
  arbres[k.id][1]=[k.univers.memoire[k.ptr]]
  
  
for j<n:
  replay.transform
  for k,ind in enumerate(liste_cpus,1):
    branche=arbres[loc_cpus[k.id][0]][loc_cpus[k.id][1]]
    if branche[-1]="NEW":
      loc_cpus[k.id][1]=2*loc_cpus[k.id][1]
      loc_cpus[liste_cpus[ind].id]=[loc_cpus[k.id][0],2*loc_cpus[k.id][1]+1]
      arbres[loc_cpus[k.id][0]][loc_cpus[k.id][1]]=[k.univers.memoire[k.ptr]
      arbres[loc_cpus[liste_cpus[ind].id][0]][loc_cpus[liste_cpus[ind].id][1]]=[]
    else:
      branche.add([k.univers.memoire[k.ptr]])
      
      
      
      
