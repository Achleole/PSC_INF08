from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import numpy as np
from replay import *
from pygraphviz import *


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
      




def euclidiandistance(a=0,b=0):
    return abs(a-b)

def levensteindistance(ch1,ch2):
    "distance de substitution utilise pour les chaines de caracteres et pour les listes"
    m,n= len(ch1),len(ch2)
    d= np.zeros((m,n),dtype=np.int8)
    cost = 1
    if ch1[0]==ch2[0]:
        cost =0
    for i in range(m):
        d[i,0]=i+cost
    for j in range(n):
        d[0,j]=j+cost

    for j in range(1,n):
        for i in range(1,m):
            if ch1[i]== ch2[j]:
                substitutioncost=0
            else:
                substitutioncost=1
            d[i,j]=min(d[i-1,j]+1, d[i,j-1]+1, d[i-1,j-1]+ substitutioncost)
    return (d[m-1,n-1]/max(m,n))


def levensteindistancecouple(a,b):
    "Prendre la partie chaine(liste) de la structure de donnee sous forme (chaine,_,_) et calculer la distance de substitution"
    (ch,i,j)=a
    (chh,ii,jj)=b
    return levensteindistance(ch,chh)



def distancematrix(list,distance=levensteindistance):
    "etant donne une liste d'elements evaluables par la distance donnee, calculer la partie inferieure de la matrice de distance rangee dans un vecteur"
    n = len(list)
    ll = np.zeros(((n*n-n)//2))
    s=0
    for i in range(0,n):
        for j in range(0,n):
            if i<j:
                ll[s]=distance(list[i],list[j])
                s+=1
    return ll


#n'est pas utilise dans le programme
#etant donnee une liste d'elements evaluables par la distance donnee, calculer la matrice
# dont la position i,j represente la distance entre le i et j-iemes elements de la liste
def pleindistancematrix(list,distance=levensteindistance):
    n = len(list)
    ll = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            ll[i,j] = distance(list[i],list[j])
    return ll

def clusteringCluster(list,distance=levensteindistancecouple,epsilon=0.01):
    X = distancematrix(list,distance)
    Z = linkage(X, 'average')
    clus = fcluster(Z,epsilon)
    l=[]
    maxclus = max(clus)
    for i in range(1,maxclus+1):
        listaajouter = [j for j in range(len(clus)) if clus[j]==i]
        l.append(listaajouter)
    #print(l)
    return l



def main():
    mots= ["absent","absente","absents","indenpendants","indenpendant","endependant","independante"]
    clusteringCluster(mots,0.01)
    #print(pleindistancematrix(mots,levensteindistance))
    #print(distancematrix(mots,levensteindistance))
    X = distancematrix(mots)
    Z = linkage(X,'average')
    resultat = fcluster(Z,0.01)
    print(resultat)
    #print(Z)
    fig = plt.figure(figsize=(25, 10))
    dn = dendrogram(Z)
    #plt.show()

#main()



def dictOfDictToList(dictofdict):
    l=[]
    for cpuid in dictofdict:
        for instructionid in dictofdict[cpuid]:
            l.append((dictofdict[cpuid][instructionid],cpuid,instructionid))
    return l


def constructTree(univ,fichier,epsilon=0.1):
    dictofdict=creer_arbres(univ,fichier)
    treeConstructed = dict()
    for cpuid in dictofdict:
        treeConstructed[cpuid] = dict()
        for instructionid in dictofdict[cpuid]:
            treeConstructed[cpuid][instructionid]=0
    ACluster = dictOfDictToList(dictofdict)
    X = distancematrix(ACluster,levensteindistancecouple)
    Z = linkage(X, 'average')
    clus = fcluster(Z, epsilon)
    print("clus est ",clus)
    print("Acluster est ",ACluster)
    for i in range(len(ACluster)):
        (instruction,ccpuid,iinstructionid)=ACluster[i]
        treeConstructed[ccpuid][iinstructionid]=clus[i]
    return (Acluster,treeConstructed,max(clus))

def test():
    tree1 = {123: "abcabcabc", 234: "abcabcabcd", 345: "abcabcacb"}
    tree2 = {1223: "defdefdef", 2434: "abcabcaad", 3545: "defdefdefd"}
    treeoftree = {1: tree1, 2: tree2}
    l = (dictOfDictToList(treeoftree))
    # print(l)
    d = distancematrix(l, levensteindistancecouple)
    Z = linkage(d, 'average')
    clus = fcluster(Z, 0.1)
    print(clus)
    print(constructTree(treeoftree, 0.1))



def interaction(treeConstructed,maxclus):
    "(i,j) represente le nombre de fois où un membre de cluster i est suivi d'un membre de cluster j "
    stat = np.ones((maxclus,maxclus),dtype=int16)
    for cpuid in treeConstructed:
        for instructionid in treeConstructed[cpuid]:
            if treeConstructed[cpuid].has_key(instructionid//2):
                stat[treeConstructed[cpuid][instructionid//2]-1,treeConstructed[cpuid][instructionid]-1]+=1
    G=AGraph()
    for i in range(maxclus):
        G.add_node('i')
    n=np.max(stat)
    for i in range(maxclus):
        for j in range(maxclus): 
            G.add_edge('i','j',arrowsize=3*stat[i][j]/n)  
    print(G)
    return(G)
                                             
