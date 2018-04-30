import Univers
import NextSite
import SimpleNextSite
import Enregistrement
import Instructions
import CPU
import matplotlib.pyplot as plt
import numpy as np
#from pygraphviz import *'





def creer_arbre(n):
    nextSite = NextSite.NextSite(memLen=5000)
    univ = Univers.Univers(nextSite, TAILLE_MEMOIRE=5000, mutation=0)
    univ.LARGEUR_CALCUL_DENSITE = 23
    univ.insDict.initialize(Instructions.instructions) 
    eve = Enregistrement.charger_genome('eve') #charge le genome eve
    ancestor = univ.insDict.toInts(eve) #et convertit en instructions
    univ.addIndividual(0, ancestor) #on ajoute le genome au debut de la memoire
    c = CPU.CPU(0, univ)  #on ajoute un CPU pour lire le genome
    c.generation = 1
    univ.inserer_cpu(c)
    nb=[]
    loc_cpus = dict()
    arbre=dict()
    univ.liste_cpus[0].id="0/1"
    loc_cpus[univ.liste_cpus[0].id.split("/")[1]] = 1
    arbre[1] = 0

    for j in range(n):
        univ.cycle()
        nb+=[len(univ.liste_cpus)]
        k=0
        for k in univ.liste_cpus:
            if  k.id.split("/")[1] in loc_cpus:
                arbre[loc_cpus[k.id.split("/")[1]]]+=1
            else:
                a=loc_cpus[k.id.split("/")[0]]
                loc_cpus[k.id.split("/")[1]]=2*a+1
                loc_cpus[k.id.split("/")[0]]=2*a
                arbre[2*a]=0
                arbre[2*a+1]=0
               
    return(arbre,nb)
 



def exp_arbre(n,m):
    t=[]
    for i in range(m):
        arbre,nb=creer_arbre(n)
        t+=[[arbre,nb]]
        dessiner(arbre,nb)
    return(t)
 

   
def dessiner(arbre,nb):
 
  
    l=list(arbre.keys())
    k=1
    m=dict()
    m[1]=[0,0,arbre[1]]
    fig, axes = plt.subplots()
    axes.set_frame_on(False)
    maxi=0
    while True:
     
        if 2*k in l:
            m[2*k]=[m[k][0],m[k][2],m[k][2]+arbre[2*k]]
            k=2*k
        else:
            while k%2==1:
                k=k//2
            if k==0:
                break
            else:
                k=k+1
                m[k]=[0,m[k//2][2],m[k//2][2]+arbre[k]]
                maxi+=max(1/nb[m[k][1]],(1.5)**(10-m[k][1]/500))
                m[k][0]=maxi

                 
    for j in m:
        plt.plot([m[j][0],m[j][0]],[m[j][1]/500,m[j][2]/500])
        if j!=1:
            plt.plot([m[j//2][0],m[j][0]],[m[j][1]/500,m[j][1]/500])
    plt.show()     

