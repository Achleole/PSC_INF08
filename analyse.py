def levenshteinDistance(ch1,ch2):
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
    print(d)
