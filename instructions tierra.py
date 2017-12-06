# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.

instructions tierra
"""
"l=longuer de la mémoire circulaire"
"d=distance de recherche maximale des templates"
"t=longueur maximale des templates"

def ifz(c):
    "execute la prochaine istruction si Cx=0, la passe sinon"
    if Cx!=0:
        c.index=(c.index+1)%l

def jmp(c):
    "saute au template le plus proche en avant"
    adr=(c.index+1)%l
	template=[]
	for k in range(t):
		if c.universe.memory[adr]==nop0
			template+=[nop1]
		elif c.universe.memory[adr]==nop1
			template+=[nop0]
		else:
			adr=(adr+1)%l
			break
		adr=(adr+1)%l
	n=len(template)
    for k in range(d):
        for i in range(n):
            if template[i]==c.universe.memory[adr]:
                adr=(adr+1)%l
            else:
                adr=(adr-i+1)%l
                break
            if i==n-1:
				c.index=adr
                return()
    
def jmpb(c):
    "saute au template le plus proche en arrière"
	adr=(c.index+1)%l
	template=[]
	for k in range(t):
		if c.universe.memory[adr]==nop0
			template+=[nop1]
		elif c.universe.memory[adr]==nop1
			emplate+=[nop0]
		else:
			adr=(adr+1)%l
			break
		adr=(adr+1)%l
	n=len(template)
    adr=(c.index-n)%l
    for k in range(d):
        for i in range(n):
            if template[i]==c.universe.memory[adr]:
                adr=(adr+1)%l
            else:
                adr=(adr-i-1)%l
                break
            if i==n-1:
				c.index=adr
                return()
    
def call(c):
    "place l'adresse au sommet de la pile et saute au template le plus proche en avant:
    stack.push(c.index)
    jmpb()

def ret(c):
    "enlève l'adresse du haut de la pile et va s'y placer"
    c.index=stack.pop()
    return()
    
def adrf():
    "cherche un template en avant et place son adresse dans Ax"
    adr=(c.index+1)%l
	template=[]
	for k in range(t):
		if c.universe.memory[adr]==nop0
			template+=[nop1]
		elif c.universe.memory[adr]==nop1
			emplate+=[nop0]
		else:
			adr=(adr+1)%l
			break
		adr=(adr+1)%l
	n=len(template)
    for k in range(d):
        for i in range(n):
            if template[i]==c.universe.memory[adr]:
                adr=(adr+1)%l
            else:
                adr=(adr-i+1)%l
                break
            if i==n-1:
				AX=(adr+1)%l
                return()
    
	Ax=(c.index+1)%l

def adrb(c):
    "cherche un template en arrière et place son adresse dans Ax"
	adr=(c.index+1)%l
	template=[]
	for k in range(t):
		if c.universe.memory[adr]==nop0
			template+=[nop1]
		elif c.universe.memory[adr]==nop1
			emplate+=[nop0]
		else:
			adr=(adr+1)%l
			break
		adr=(adr+1)%l
	n=len(template)
    adr=(c.index-n)%l
    for k in range(d):
        for i in range(n):
            if template[i]==c.universe.memory[adr]:
                adr=(adr+1)%l
            else:
                adr=(adr-i-1)%l
                break
            if i==n-1:
				Ax=(adr+1)%l
                return()
	Ax=(c.index+1)%l
    
def new(c):
    "crée un nouveau cpu"
	create(c)

def read(c):
	"lit l'instruction correspondant à l'adresse présente dans Ax et la place dans la pile"
	c.stack.push(c.universe.memory[Ax])

def write(c):
	"place l'instruction au sommet de la pile à l'adresse contenue dans Ax"
	C.universe.memory[Ax]=c.stack.pop()
