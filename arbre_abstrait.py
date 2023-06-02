"""
Affiche une chaîne de caractères avec une certaine indentation
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


class ListeInstructions:
    def __init__(self):
        self.instructions = []

    def ajouter_instruction(self, instruction):
        self.instructions.append(instruction)

    def afficher(self, indent=0):
        afficher("<listeInstructions>", indent)
        for instruction in self.instructions:
            instruction.afficher(indent + 1)
        afficher("</listeInstructions>", indent)


class Declaration:
    def __init__(self, type_var, nom_variable):
        self.type_var = type_var
        self.nom_variable = nom_variable

    def afficher(self, indent=0):
        afficher("<declaration>", indent)
        afficher(self.type_var + " " + self.nom_variable, indent + 1)
        afficher("</declaration>", indent)


class Affectation:
    def __init__(self, nom_variable, expression):
        self.nom_variable = nom_variable
        self.expression = expression

    def afficher(self, indent=0):
        afficher("<affectation>", indent)
        afficher(self.nom_variable, indent + 1)
        self.expression.afficher(indent + 1)
        afficher("</affectation>", indent)


class InstructionConditionnelle:
    def __init__(self, conditions, instructions):
        self.conditions = conditions
        self.instructions = instructions

    def afficher(self, indent=0):
        afficher("<instructionConditionnelle>", indent)
        for condition, instruction in zip(self.conditions, self.instructions):
            afficher("<condition>", indent + 1)
            condition.afficher(indent + 2)
            afficher("</condition>", indent + 1)
            instruction.afficher(indent + 1)
        afficher("</instructionConditionnelle>", indent)


class InstructionBoucle:
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions

    def afficher(self, indent=0):
        afficher("<instructionBoucle>", indent)
        afficher("<condition>", indent + 1)
        self.condition.afficher(indent + 2)
        afficher("</condition>", indent + 1)
        self.instructions.afficher(indent + 1)
        afficher("</instructionBoucle>", indent)


class Retourner:
    def __init__(self, expression):
        self.expression = expression

    def afficher(self, indent=0):
        afficher("<retourner>", indent)
        self.expression.afficher(indent + 1)
        afficher("</retourner>", indent)


class Ecrire:
    def __init__(self, expression):
        self.expression = expression

    def afficher(self, indent=0):
        afficher("<ecrire>", indent)
        self.expression.afficher(indent + 1)
        afficher("</ecrire>", indent)


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


class Entier:
    def __init__(self, valeur):
        self.valeur = valeur

    def afficher(self, indent=0):
        afficher("<entier>", indent)
        afficher(str(self.valeur), indent + 1)
        afficher("</entier>", indent)


class Booleen:
    def __init__(self, valeur):
        self.valeur = valeur

    def afficher(self, indent=0):
        afficher("<booleen>", indent)
        afficher(str(self.valeur), indent + 1)
        afficher("</booleen>", indent)


class Variable:
    def __init__(self, nom_variable):
        self.nom_variable = nom_variable

    def afficher(self, indent=0):
        afficher("<variable>", indent)
        afficher(self.nom_variable, indent + 1)
        afficher("</variable>", indent)


class Lire:
    def afficher(self, indent=0):
        afficher("<lire>", indent)
        afficher("</lire>", indent)


class AppelFonction:
    def __init__(self, nom_fonction, arguments):
        self.nom_fonction = nom_fonction
        self.arguments = arguments

    def afficher(self, indent=0):
        afficher("<appelFonction>", indent)
        afficher(self.nom_fonction, indent + 1)
        for argument in self.arguments:
            argument.afficher(indent + 1)
        afficher("</appelFonction>", indent)


class ExprList:
    def __init__(self, expressions=None):
        self.expressions = expressions if expressions is not None else []

    def ajouter_expression(self, expression):
        self.expressions.append(expression)

    def afficher(self, indent=0):
        afficher("<expressionList>", indent)
        for expr in self.expressions:
            expr.afficher(indent + 1)
        afficher("</expressionList>", indent)

    def __iter__(self):
        return iter(self.expressions)
