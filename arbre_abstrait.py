"""
Affiche une chaine de caractère avec une certaine identation
"""


def afficher(s, indent=0):
    print(" " * indent + s)


class Programme:
    def __init__(self, listeInstructions):
        self.listeInstructions = listeInstructions

    def afficher(self, indent=0):
        afficher("<programme>", indent)
        self.listeInstructions.afficher(indent + 1)
        afficher("</programme>", indent)

class Operation:
    def __init__(self, operateur, exp1, exp2):
        self.operateur = operateur
        self.exp1 = exp1
        self.exp2 = exp2

    def afficher(self, indent=0):
        afficher("<operation>", indent)
        afficher(self.operateur, indent + 1)
        self.exp1.afficher(indent + 1)
        self.exp2.afficher(indent + 1)
        afficher("</operation>", indent)


class ListeInstructions:
    def __init__(self):
        self.instructions = []

    def afficher(self, indent=0):
        afficher("<listeInstructions>", indent)
        for instruction in self.instructions:
            instruction.afficher(indent + 1)
        afficher("</listeInstructions>", indent)


class Ecrire:
    def __init__(self, exp):
        self.exp = exp

    def afficher(self, indent=0):
        afficher("<ecrire>", indent)
        self.exp.afficher(indent + 1)
        afficher("</ecrire>", indent)




class Entier:
    def __init__(self, valeur):
        self.valeur = valeur

    def afficher(self, indent=0):
        afficher("[Entier:" + str(self.valeur) + "]", indent)


class Variable:
    def __init__(self, nomVariable):
        self.nomVariable = nomVariable

    def afficher(self, indent=0):
        afficher("[Variable:" + self.nomVariable + "]", indent)


class Lire:
    def afficher(self, indent=0):
        afficher("<lire>", indent)
        afficher("</lire>", indent)


class AppelFonction:
    def __init__(self, nomFonction, arguments):
        self.nomFonction = nomFonction
        self.arguments = arguments

    def afficher(self, indent=0):
        afficher("<appelFonction>", indent)
        afficher(self.nomFonction, indent + 1)
        for argument in self.arguments:
            argument.afficher(indent + 1)
        afficher("</appelFonction>", indent)


class ExprList:
    def __init__(self, expr, exprList=None):
        self.expressions = []
        self.ajouter_expression(expr)
        if exprList:
            self.expressions.extend(exprList.expressions)

    def ajouter_expression(self, expr):
        self.expressions.append(expr)

    def afficher(self, indent=0):
        afficher("<expressionList>", indent)
        for expr in self.expressions:
            expr.afficher(indent + 1)
        afficher("</expressionList>", indent)

    def __iter__(self):
        return iter(self.expressions)


class Booleen:
    def __init__(self, valeur):
        self.valeur = valeur

    def afficher(self, indent=0):

        print("[Booleen:" + str(self.valeur) + "]" + " " * indent)

    def evaluer(self):
        return self.valeur


class BooleenOperation:
    def __init__(self, operateur, operande_gauche, operande_droit):
        self.operateur = operateur
        self.operande_gauche = operande_gauche
        self.operande_droit = operande_droit

    def afficher(self, indent=0):
        afficher("<booleenOperation>", indent)
        afficher(self.operateur, indent + 1)
        self.operande_gauche.afficher(indent + 1)
        self.operande_droit.afficher(indent + 1)
        afficher("</booleenOperation>", indent)

