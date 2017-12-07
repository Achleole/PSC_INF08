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
    "place l'adresse au sommet de la pile et saute au template le plus proche en avant:"
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
				ax=(adr+1)%l
                return()
	ax=(c.index+1)%l
    
def new(c):
    "crée un nouveau cpu"
	create(c)

def read(c):
	"lit l'instruction correspondant à l'adresse présente dans Ax et la place dans la pile"
	c.stack.push(c.universe.memory[ax])

def write(c):
	"place l'instruction au sommet de la pile à l'adresse contenue dans Ax"
	C.universe.memory[ax]=c.stack.pop()

def nop1(self):
    "I don't know what does it do"
    return None
def nop2(self):
    "I don't know what does it do"
    return None

def pushA(self):
    stack.append(AX)    
    "push A in the stack"
def pushB(self): 
    "push B in the stack"
    stack.append(BX) 
def pushC(self): 
    "push C in the stack"
    stack.append(CX)    
def pushD(self): 
    "push D in the stack"
    stack.append(DX)

def popA(self): 
    AX=stack.pop()
def popB(self):
    BX=stack.pop()
def popC(self):
    CX=stack.pop()
def popD(self):
    DX=stack.pop()

def movcd(self):
    "C takes the value of D"
    CX=DX
def movab(self):
    "B takes the value of  A"
    BX=CX
def movii(self):
    "unknown function"

def subCAB(self):
    CX=AX-BX
def subAAC(self):
    AX=AX-CX
def incA(self):
    AX+=1
def incB(self):
    BX+=1
def incC(self):
    CX+=1
def incD(self):
    DX+=1
def decC(self):
    CX-=1
def zero(self):
    CX=0
def not0(self):
    "inverse the unity number"
    if CX%2==0:
        CX+=1
    else:
        CX-=1
def shl(self):
    "double the value of C"
    CX*=2
