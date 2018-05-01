from Instructions_Tierra import *

TAILLE_STACK = 10


class CPU:
    TAILLE_STACK = 10

    # ptr stocke l'adresse actuellement pointee par le CPU
    def __init__(self, ptr, univers, ax=0, bx=0, cx=0, dx=0, stack=None, stack_ptr=0, father=None, id = None):
        """Doit contenir la meme valeur que ptr dans bx (pour eve)"""
        if id ==None:
            self.id = univers.nextId(father)
        else:
            self.id = id
        self.ax = ax
        self.bx = bx
        self.cx = cx
        self.dx = dx
        self.univers = univers
        self.ptr = ptr
        if stack is None :
            self.stack = [0]*TAILLE_STACK
        else :
            self.stack = stack
        self.stack_ptr = stack_ptr

    def execute(self):
        """execute l'instruction actuellement pointee par le CPU puis passe a la suivante\
        Met a jour la localisation du CPU\
        Attention, les instructions sont stockees dans le dictionnaire de l'univers sous forme de chaine de caractere\
        correspondant EXACTEMENT au nom des fonctions"""
        if self.ptr >= self.univers.TAILLE_MEMOIRE or self.ptr < 0:
            self.ptr=self.univers.ind(self.ptr)
        ins = self.univers.insDict.toString(self.univers.memoire[self.ptr])
        if ins == "HCF":
            HCF(self)
        else:
            self.univers.supprimer_cpu_localisation(self)
            try:
                f = eval(ins)
                f(self)
            except Exception as e:
                print("Instruction ayant echoue : ", ins)
                print(e)
            finally:
                self.incrementer_ptr()
                self.univers.ajouter_cpu_localisation(self)

    def incrementer_ptr(self):
        if self.ptr == self.univers.TAILLE_MEMOIRE-1:
            self.ptr=0
        else:
            self.ptr +=1

    def incrementer_stack_ptr(self):
        self.stack_ptr = (self.stack_ptr + 1) % (TAILLE_STACK)

    def decrementer_stack_ptr(self):
        self.stack_ptr = (self.stack_ptr - 1) % (TAILLE_STACK)

    def pop_stack(self):
        "Retourne la valeur du stack qui est au dessus i.e en stack_ptr - 1 SANS DECREMENTER\
        le stack pointeur"
        return self.stack[(self.stack_ptr - 1) % TAILLE_STACK]

    def push_stack(self, x):
        "Met la valeur de l'argument dans la stack SANS INCREMENTER le stack\
        pointeur"
        self.stack[self.stack_ptr] = x

    def die(self):
        # self.enlever_localisation()
        self.univers.tuer_cpu(self)

    # FONCTIONS D'AFFICHAGE
    def afficher_etat(self):
        print("valeurs de ax, bx, cx et dx : ")
        print(self.ax, self.bx, self.cx, self.dx)
        print("Etat du pointeur d'instructions")
        self.ptr = self.univers.ind(self.ptr)
        print(self.ptr, " sur ", self.univers.memoire[self.ptr])
        print('valeur de la stack : ', self.stack)
        print('pointeur de la stack : ', self.stack_ptr)
    def copy(self,nUnivers):
        return CPU(self.ptr, nUnivers, self.ax, self.bx, self.cx, self.dx, self.stack[:], self.stack_ptr, None, self.id)
    def __ne__(self,other):
        return not self.__eq__(other)
    def __eq__(self,other):
        if other is None:
            return self is None
        else:
            bool = self.ptr == other.ptr
            bool *= self.ax == other.ax
            bool *= self.bx == other.bx
            bool *= self.cx == other.cx
            bool *= self.dx == other.dx
            bool *= self.stack == other.stack
            bool *= self.stack_ptr == other.stack_ptr
            bool *= self.id == other.id
            return bool
