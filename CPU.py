from Instructions_Tierra import *

TAILLE_STACK = 10


class CPU:
    TAILLE_STACK = 10

    # ptr stocke l'adresse actuellement pointee par le CPU
    def __init__(self, ptr, univers, ax=0, bx=0, cx=0, dx=0, stack_ptr=0):
        self.ax = ax
        self.bx = bx
        self.cx = cx
        self.dx = dx
        self.univers = univers
        self.ptr = ptr
        self.stack = [0]*TAILLE_STACK #ce changement pas POUR le debogage, a conserver (mais pourquoi necessaire ???)
        self.stack_ptr = stack_ptr
        self.nvx = [] #debogage ?
        self.nbInsExec = 0 #pour le debogage

    def execute(self):
        "execute l'instruction actuellement pointee par le CPU puis passe a la suivante\
        Attention, les instructions sont stockees dans le dictionnaire de l'univers sous forme de chaine de caractere\
        correspondant EXACTEMENT au nom des fonctions"
        self.ptr = self.univers.ind(self.ptr)
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
        self.nbInsExec += 1
        0

    def incrementer_ptr(self):
        self.ptr = self.univers.ind((self.ptr + 1))

    def incrementer_stack_ptr(self):
        self.stack_ptr = (self.stack_ptr + 1) % (TAILLE_STACK)
        0

    def decrementer_stack_ptr(self):
        self.stack_ptr = (self.stack_ptr - 1) % (TAILLE_STACK)
        0

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
