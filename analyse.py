from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np

def euclidiandistance(a=0,b=0):
    return abs(a-b)

#distance de substitution utilise pour les chaines de caracteres
def levensteindistance(ch1,ch2):
    m,n= len(ch1),len(ch2)
    import numpy as np
    d= np.zeros((m,n))
    for i in range(m):
        d[i,0]=i
    for j in range(n):
        d[0,j]=j

    for j in range(1,n):
        for i in range(1,m):
            if ch1[i]== ch2[j]:
                substitutioncost=0
            else:
                substitutioncost=1
            d[i,j]=min(d[i-1,j]+1, d[i,j-1]+1, d[i-1,j-1]+ substitutioncost)
    return (d[m-1,n-1])


#etant donne une liste d'elements evaluables par la distance donnee, calculer la partie inferieure de la matrice de distance rangee dans un vecteur
def distancematrix(list,distance=levensteindistance):
    n = len(list)
    ll = np.zeros(((n*n-n)//2))
    for i in range(1,n):
        for j in range(i,n):
            ll[(2*n-i-1)*i//2+j]=distance(list[i],list[j])
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

#tracer un dendrogramme
def tracerdendrogram(list,dist=levensteindistance):
    X = distancematrix(list,dist)
    Z = linkage(X,'ward',optimal_ordering=True)
    fig = plt.figure(figsize=(25,10))
    dn = dendrogram(Z)
    plt.show()


def main():
    mots= ["absent","absente","absents","indenpendants","indenpendant","endependant","independante"]
    print(pleindistancematrix(mots,levensteindistance))
    print(distancematrix(mots,levensteindistance))
    X = distancematrix(mots)
    Z = linkage(X,'average')
    print(Z)
    fig = plt.figure(figsize=(25, 10))
    dn = dendrogram(Z)
    plt.show()

main()
