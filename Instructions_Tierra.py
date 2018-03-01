from Utilitaire import *

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
    c.cx = c.ax - c.bx

def subAAC(c):
    c.ax = c.ax - c.cx

def incA(c):
    c.ax += 1

def incB(c):
    c.bx += 1

def incC(c):
    c.cx += 1

def incD(c):
    c.dx += 1

def decA(c):
    c.ax -= 1

def decB(c):
    c.bx -= 1

def decC(c):
    c.cx -= 1

def decD(c):
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
    c.ax = c.pop_stack()
    c.decrementer_stack_ptr()

def popB(c):
    c.bx = c.pop_stack()
    c.decrementer_stack_ptr()

def popC(c):
    c.cx = c.pop_stack()
    c.decrementer_stack_ptr()

def popD(c):
    c.dx = c.pop_stack()
    c.decrementer_stack_ptr()

def jmp(c):
    try:
        l_pattern, indice, i = trouver_template_complementaire(c, LIMITE_RECHERCHE)
    except PatternNotFoundException as e:
        c.ptr += e.l_pattern
        print("pattern non trouve")
    except NoPatternException:
        print("pas de pattern apres l'instruction jmp")
        return
    else:
        c.ptr = indice + l_pattern- 1 #on soustrait 1 car le ptr va ensuite etre incremente


def jmpb(c):
    try:
        l_pattern, indice, i = trouver_template_complementaire_arriere(c, LIMITE_RECHERCHE)
    except PatternNotFoundException as e:
        c.ptr += e.l_pattern
    except NoPatternException:
        return
    else:
        c.ptr = indice + l_pattern - 1  # on soustrait 1 car le ptr va ensuite etre incremente
        #print('truc')

def call(c):
    try:
        l_pattern, indice, i = trouver_template_complementaire(c, LIMITE_RECHERCHE)
    except NoPatternException:
        c.push_stack(c.ptr+1)
        c.incrementer_stack_ptr()#cf doc tierra sur le comportement de la fonction (j'ai un doute)
    except PatternNotFoundException as e:
        c.ptr += e.l_pattern
    else:
        c.push_stack(c.ptr + l_pattern + 1)
        #c.incrementer_stack_ptr() #on stocke l'ANCIENNE adresse + l_pattern
        c.ptr = indice + l_pattern - 1 #car on va a l'adresse apres le pattern


def ret(c):
    x = c.pop_stack()
    #c.decrementer_stack_ptr()
    c.ptr = x - 1 #car on va incrementer ensuite c.ptr

def movDC(c):
    c.dx = c.cx

def movBA(c):
    c.bx = c.ax

def movii(c):
    #sert a copier le contenu d'une case dans une autree
    u = c.univers
    c.bx = u.ind(c.bx)
    c.ax = u.ind(c.ax)
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
    c.univers.inserer_cpu(CPU.CPU(c.ax,c.univers, bx=c.ax, father=c))

def rand(c):
    c.ax  = c.univers.nextSite.getNext()
    "Place dans c.ax une valeur aleatoire"

def read(c):
    "Lit l'instruction correspondant a l'adresse presente dans c.bx et la place dans la stack"
    c.bx = c.univers.ind(c.bx)
    c.push_stack(c.univers.memoire[c.bx])
    c.incrementer_stack_ptr()

def write(c):
    "Ecrit l'instruction au sommet de la pile dans l'adresse contenue dans c.ax"
    c.ax = c.univers.ind(c.ax)
    a = random.random()
    if a>c.univers.mutation:
        c.univers.memoire[c.ax] = c.pop_stack()
    else:
        c.univers.memoire[c.ax] = random.randint(0,37)
    c.decrementer_stack_ptr()

def HCF(c):
    "Tue le cpu qui la lit"
    c.die()
