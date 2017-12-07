# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.

instructions tierra
"""
"l=longueur de la mémoire circulaire"
"d=distance de recherche maximale des templates"
"t=longueur maximale des templates"

import random as rd ; #il faut le placer ailleurs ?

def ifz(c):
    "execute la prochaine istruction si c.cx=0, la passe sinon"
    if c.cx!=0:
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
    "place l'adresse au sommet de la pile et saute au template le plus proche en avant:"
    c.stack.push(c.index)
    jmpb(c)

def ret(c):
    "enlève l'adresse du haut de la pile et va s'y placer"
    c.index=c.stack.pop()
    
def adrf():
    "cherche un template en avant et place son adresse dans c.ax"
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
				c.ax=(adr+1)%l
                return()
    
	c.ax=(c.index+1)%l

def adrb(c):
    "cherche un template en arrière et place son adresse dans c.ax"
    # ne devrait-on pas aussi mettre la longueur du template dans cx, comme dans Tierra ?
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
    adr=(c.index-n)%l
    for k in range(d):
        for i in range(n):
            if template[i]==c.universe.memory[adr]:
                adr=(adr+1)%l
            else:
                adr=(adr-i-1)%l
                break
            if i==n-1:
				c.ax=(adr+1)%l
                return()
	c.ax=(c.index+1)%l
    
def new(c):
    "crée un nouveau cpu"
	create(c)

def read(c):
	"lit l'instruction correspondant à l'adresse présente dans c.ax et la place dans la pile"
	c.stack.push(c.universe.memory[c.ax])

def write(c):
	"place l'instruction au sommet de la pile à l'adresse contenue dans c.ax"
	C.universe.memory[c.ax]=c.stack.pop()

def nop0(c):
    "I don't know what does it do"
    return None
    
def nop1(c):
    "I don't know what does it do"
    return None

def pushA(c):
    c.stack.append(c.ax)    
    "push A in the c.stack"
def pushB(c): 
    "push B in the c.stack"
    c.stack.append(c.bx) 
def pushC(c): 
    "push C in the c.stack"
    c.stack.append(c.cx)    
def pushD(c): 
    "push D in the c.stack"
    c.stack.append(c.dx)

def popA(c): 
    c.ax=c.stack.pop()
def popB(c):
    c.bx=c.stack.pop()
def popC(c):
    c.cx=c.stack.pop()
def popD(c):
    c.dx=c.stack.pop()

def movCD(c):
    "C takes the value of D"
    c.cx=c.dx
def movAB(c):
    "B takes the value of  A"
    c.bx=c.cx
def movii(c):
    "unknown function"

def subCAB(c):
    c.cx=c.ax-c.bx
def subAAC(c):
    c.ax=c.ax-c.cx
def incA(c):
    c.ax+=1
def incB(c):
    c.bx+=1
def incC(c):
    c.cx+=1
def incD(c):
    c.dx+=1
def decC(c):
    c.cx-=1
def zero(c):
    c.cx=0
def not0(c):  #c'est vraiment ça qu'il faut faire ??
    "inverse the unity number"
    if c.cx%2==0:
        c.cx+=1
    else:
        c.cx-=1
def shl(c):
    "double the value of C"
    c.cx*=2

def rand(c) :
    c.cx = int(l*rd.random())
    c.index = c.index=(c.index+1)%l #cette étape semble oubliée dans d'autres instructions
