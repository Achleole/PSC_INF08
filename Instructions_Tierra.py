from Utilitaire import *
import random
import CPU

LIMITE_RECHERCHE = 10

#Definit la limite de recherhe pour le template
longueur_pattern = 0

def nop0(cpu):
    pass

def nop1(cpu):
    pass

def not0(cpu):
    if cpu.cx % 2 == 0:
        cpu.cx += 1
    else:
        cpu.cx -= 1

def shl(c):
    c.cx = (c.cx << 1)

def zero(c):
    c.cx = 0

def ifz(c):
    #Si cx vaut 0, on ne fait rien car le CPU va ensuite de lui
    #meme incrementer son ptr
    if c.cx != 0:
        c.incrementer_ptr()

def subCAB(c):
    diff = c.ax - c.bx
    if diff >= c.univers.TAILLE_MEMOIRE or diff < 0:
        diff = c.univers.ind(diff)
    c.cx = diff

def subAAC(c):
    diff = c.ax - c.cx
    if diff >= c.univers.TAILLE_MEMOIRE or diff < 0:
        diff = c.univers.ind(diff)
    c.ax = diff

def incA(c):
    if c.ax == c.univers.TAILLE_MEMOIRE-1:
        c.ax = 0
    else:
        c.ax += 1

def incB(c):
    if c.bx == c.univers.TAILLE_MEMOIRE-1:
        c.bx = 0
    else:
        c.bx += 1

def incC(c):
    if c.cx == c.univers.TAILLE_MEMOIRE-1:
        c.cx = 0
    else:
        c.cx += 1

def incD(c):
    if c.dx == c.univers.TAILLE_MEMOIRE-1:
        c.dx = 0
    else:
        c.dx += 1

def decA(c):
    if c.ax == 0:
        c.ax = c.univers.TAILLE_MEMOIRE-1
    else:
        c.ax -= 1

def decB(c):
    if c.bx == 0:
        c.bx = c.univers.TAILLE_MEMOIRE-1
    else:
        c.bx -= 1

def decC(c):
    if c.cx == 0:
        c.cx = c.univers.TAILLE_MEMOIRE-1
    else:
        c.cx -= 1

def decD(c):
    if c.dx == 0:
        c.dx = c.univers.TAILLE_MEMOIRE-1
    else:
        c.dx -= 1

def pushA(c):
    c.push_stack(c.ax)
    c.incrementer_stack_ptr()

def pushB(c):
    c.push_stack(c.bx)
    c.incrementer_stack_ptr()

def pushC(c):
    c.push_stack(c.cx)
    c.incrementer_stack_ptr()

def pushD(c):
    c.push_stack(c.dx)
    c.incrementer_stack_ptr()

def popA(c):
    c.ax = max(0, min(c.pop_stack(), len(c.univers.memoire)))
    c.decrementer_stack_ptr()

def popB(c):
    c.bx = max(0, min(c.pop_stack(), len(c.univers.memoire)))
    c.decrementer_stack_ptr()

def popC(c):
    c.cx = max(0, min(c.pop_stack(), len(c.univers.memoire)))
    c.decrementer_stack_ptr()

def popD(c):
    c.dx =  max(0, min(c.pop_stack(), len(c.univers.memoire)))
    c.decrementer_stack_ptr()

def jmp(c):
    try:
        l_pattern, indice, i = trouver_template_complementaire(c, LIMITE_RECHERCHE)
    except PatternNotFoundException as e:
        summ = c.ptr + e.l_pattern
        if summ >= c.univers.TAILLE_MEMOIRE:
            summ = c.univers.ind(summ)
        c.ptr = summ
    except NoPatternException:
        return
    else:
        summ = indice + l_pattern- 1 #on soustrait 1 car le ptr va ensuite etre incremente
        if summ >= c.univers.TAILLE_MEMOIRE:
            summ = c.univers.ind(summ)
        c.ptr = summ

def jmpb(c):
    try:
        l_pattern, indice, i = trouver_template_complementaire_arriere(c, LIMITE_RECHERCHE)
    except PatternNotFoundException as e:
        summ = c.ptr + e.l_pattern
        if summ >= c.univers.TAILLE_MEMOIRE:
            summ = c.univers.ind(summ)
        c.ptr = summ
    except NoPatternException:
        return
    else:
        summ = indice + l_pattern - 1  # on soustrait 1 car le ptr va ensuite etre incremente
        if summ >= c.univers.TAILLE_MEMOIRE:
            summ = c.univers.ind(summ)
        c.ptr = summ

def call(c):
    try:
        l_pattern, indice, i = trouver_template_complementaire(c, LIMITE_RECHERCHE)
    except NoPatternException:
        c.push_stack(c.ptr+1)
        c.incrementer_stack_ptr()#cf doc tierra sur le comportement de la fonction (j'ai un doute)
    except PatternNotFoundException as e:
        summ = c.ptr + e.l_pattern
        if summ >= c.univers.TAILLE_MEMOIRE:
            summ = c.univers.ind(summ)
        c.ptr = summ
    else:
        c.push_stack(c.ptr + l_pattern + 1)
        #c.incrementer_stack_ptr() #on stocke l'ANCIENNE adresse + l_pattern
        summ = indice + l_pattern - 1  # on soustrait 1 car le ptr va ensuite etre incremente
        if summ >= c.univers.TAILLE_MEMOIRE:
            summ = c.univers.ind(summ)
        c.ptr = summ #car on va a l'adresse apres le pattern


def ret(c):
    x = c.pop_stack()
    #c.decrementer_stack_ptr()
    if x >= c.univers.TAILLE_MEMOIRE+1 or x < 1 :
        c.ptr = c.univers.ind(x-1)
    else:
        c.ptr = x - 1 #car on va incrementer ensuite c.ptr

def movDC(c):
    c.dx = c.cx

def movBA(c):
    c.bx = c.ax

def movii(c):
    #sert a copier le contenu d'une case dans une autree
    u = c.univers
    #c.bx = u.ind(c.bx)
    #c.ax = u.ind(c.ax)
    u.memoire[c.ax] = u.memoire[c.bx]

def adr(c, fonc=trouver_template_complementaire):
    try:
        l_pattern, indice, i = fonc(c, LIMITE_RECHERCHE)
    except NoPatternException:
        pass
    except PatternNotFoundException as e:
        pass
    else:
        c.ax = indice + l_pattern #car on stocke l'adresse suivant le pattern


def adrb(c):
    adr(c, trouver_template_complementaire_arriere)

def adrf(c):
    adr(c, trouver_template_complementaire_avant)

#													NOUVELLES INSTRUCTIONS
def new(c):
    "Creer un nouveau cpu a l'endroit de ax"
    c.univers.inserer_cpu(CPU.CPU(c.ax,c.univers, bx=c.ax, father=c)) #il faut que c.ax, sinon le code va buguer

def rand(c):
    c.ax  = c.univers.nextSite.getNext(c)
    "Place dans c.ax une valeur aleatoire"

def read(c):
    "Lit l'instruction correspondant a l'adresse presente dans c.bx et la place dans la stack"
    c.push_stack(c.univers.memoire[c.bx])
    c.incrementer_stack_ptr()

def write(c):
    "Ecrit l'instruction au sommet de la pile dans l'adresse contenue dans c.ax"
    #c.ax = c.univers.ind(c.ax)
    a = random.random()
    if a > c.univers.mutation: #ecriture normale
        c.univers.memoire[c.ax] = c.pop_stack()
    elif c.univers.mutation >= a > 2.*c.univers.mutation/3: #deletion
        c.pop_stack()
        c.ax -= 1
    elif 2.*c.univers.mutation/3 >= a > c.univers.mutation/3.: #insertion
        c.univers.memoire[c.ax] = random.randint(0,c.univers.insDict.nbInstructions()-1)
        c.ax += 1
        c.univers.memoire[c.ax] = c.pop_stack()
    else: #mutation
        c.univers.memoire[c.ax] = random.randint(0,c.univers.insDict.nbInstructions()-1)
    c.decrementer_stack_ptr()

def HCF(c):
    "Tue le cpu qui la lit"
    c.die()

############### Super instructions
def rw(c):
    read(c)
    write(c)

def shll(c):
    shl(c)
    shl(c)