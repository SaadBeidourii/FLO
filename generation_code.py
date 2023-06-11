import sys
from analyse_lexicale import FloLexer
from analyse_syntaxique import FloParser
import arbre_abstrait

num_etiquette_courante = -1  # Permet de donner des noms différents à toutes les étiquettes (en les appelant e0, e1,e2,...)

afficher_table = False
afficher_nasm = False
"""
Un print qui ne fonctionne que si la variable afficher_table vaut Vrai.
(permet de choisir si on affiche le code assembleur ou la table des symboles)
"""


def printifm(*args, **kwargs):
    if afficher_nasm:
        print(*args, **kwargs)


"""
Un print qui ne fonctionne que si la variable afficher_table vaut Vrai.
(permet de choisir si on affiche le code assembleur ou la table des symboles)
"""


def printift(*args, **kwargs):
    if afficher_table:
        print(*args, **kwargs)


"""
Fonction locale, permet d'afficher un commentaire dans le code nasm.
"""


def nasm_comment(comment):
    if comment != "":
        printifm(
            "\t\t ; " + comment)  # le point virgule indique le début d'un commentaire en nasm. Les tabulations sont là pour faire jolie.
    else:
        printifm("")


"""
Affiche une instruction nasm sur une ligne
Par convention, les derniers opérandes sont nuls si l'opération a moins de 3 arguments.
"""


def nasm_instruction(opcode, op1="", op2="", op3="", comment=""):
    if op2 == "":
        printifm("\t" + opcode + "\t" + op1 + "\t\t", end="")
    elif op3 == "":
        printifm("\t" + opcode + "\t" + op1 + ",\t" + op2 + "\t", end="")
    else:
        printifm("\t" + opcode + "\t" + op1 + ",\t" + op2 + ",\t" + op3, end="")
    nasm_comment(comment)


"""
Retourne le nom d'une nouvelle étiquette
"""


def nasm_nouvelle_etiquette():
    num_etiquette_courante += 1
    return "e" + str(num_etiquette_courante)


"""
Affiche le code nasm correspondant à tout un programme
"""


def gen_programme(programme):
    printifm('%include\t"io.asm"')
    printifm('section\t.bss')
    printifm('sinput:	resb	255	;reserve a 255 byte space in memory for the users input string')
    printifm('v$a:	resd	1')
    printifm('section\t.text')
    printifm('global _start')
    printifm('_start:')
    gen_listeInstructions(programme.listeInstructions)
    nasm_instruction("mov", "eax", "1", "", "1 est le code de SYS_EXIT")
    nasm_instruction("int", "0x80", "", "", "exit")


"""
Affiche le code nasm correspondant à une suite d'instructions
"""


def gen_listeInstructions(listeInstructions):
    for instruction in listeInstructions.instructions:
        gen_instruction(instruction)


"""
Affiche le code nasm correspondant à une instruction
"""


def gen_instruction(instruction):
    if type(instruction) == arbre_abstrait.Ecrire:
        gen_ecrire(instruction)
    elif type(instruction) == arbre_abstrait.InstructionBoucle:
        gen_loop(instruction.condition, instruction.instructions)
    else:
        print("type instruction inconnu", type(instruction))
        exit(0)


"""
Affiche le code nasm correspondant au fait d'envoyer la valeur entière d'une expression sur la sortie standard
"""


def gen_ecrire(ecrire):
    gen_expression(ecrire.exp)  # on calcule et empile la valeur d'expression
    nasm_instruction("pop", "eax", "", "", "")  # on dépile la valeur d'expression sur eax
    nasm_instruction("call", "iprintLF", "", "", "")  # on envoie la valeur d'eax sur la sortie standard


"""
Affiche le code nasm pour calculer et empiler la valeur d'une expression
"""


def gen_expression(expression):
    if type(expression) == arbre_abstrait.Operation:
        gen_operation(expression)  # on calcule et empile la valeur de l'opération
    elif type(expression) == arbre_abstrait.BooleanOperation:
        gen_operation_boolean(expression)  # on calcule et empile la valeur de l'opération
    elif type(expression) == arbre_abstrait.Entier:
        nasm_instruction("push", str(expression.valeur), "", "", "");  # on met sur la pile la valeur entière
        return "entier"
    elif type(expression) == arbre_abstrait.lire:
        nasm_instruction("mov", "eax", "sinput", "", "Place l'adresse de sinput dans eax")
        nasm_instruction("call", "readline", "", "",
                         "Lit une chaîne de caractères depuis l'entrée standard et place la valeur lue dans ebx")
        nasm_instruction("call", "atoi", "", "",
                         "Convertit la chaîne de caractères en entier et place le résultat dans eax")
        nasm_instruction("push", "eax", "", "", "Empile la valeur lue")
        return "entier"
    elif type(expression) == arbre_abstrait.Boolean:
        if expression.valeur == 'Vrai':  # True
            nasm_instruction("push", "1", "", "", "Empile la valeur booléenne True (1)")
        else:  # False
            nasm_instruction("push", "0", "", "", "Empile la valeur booléenne False (0)")
        return "boolean"
    elif type(expression) == arbre_abstrait.ComparisonOperation:
        gen_comparison(expression)

    else:
        print("type d'expression inconnu", type(expression))
        exit(0)


"""
Affiche le code nasm pour calculer l'opération de comparaison et la mettre en haut de la pile
"""
num_etiquette_courante = -1


def nom_nouvelle_etiquette():
    global num_etiquette_courante
    num_etiquette_courante += 1
    return "e" + str(num_etiquette_courante)


def gen_comparison(operation):
    gen_expression(operation.exp1)  # Génère le code pour l'expression de gauche
    gen_expression(operation.exp2)  # Génère le code pour l'expression de droite

    nasm_instruction("pop", "ebx", "", "", "Dépiler la deuxième opérande dans ebx")
    nasm_instruction("pop", "eax", "", "", "Dépiler la première opérande dans eax")

    cmp_instruction = {"==": "jne", "!=": "jne", "<": "jg", ">": "jl", "<=": "jge", ">=": "jle"}

    # Génère l'instruction de comparaison et saute vers l'étiquette appropriée
    label_false = nom_nouvelle_etiquette()
    label_end = nom_nouvelle_etiquette()
    nasm_instruction("cmp", "eax", "ebx", "", "Comparer eax et ebx")
    nasm_instruction(cmp_instruction[operation.op], label_false, "", "",
                     "Sauter à label_false si la comparaison est fausse")
    nasm_instruction("mov", "eax", "1", "", "Définir eax à 1 (vrai)")
    nasm_instruction("jmp", label_end, "", "", "Sauter à label_end")
    nasm_instruction(label_false + ":", "", "", "", "Label_false : définir eax à 0 (faux)")
    nasm_instruction("mov", "eax", "0", "", "")
    nasm_instruction(label_end + ":", "", "", "", "Label_end")

    nasm_instruction("push", "eax", "", "", "Empiler le résultat sur la pile")
    return "boolean"


"""
générer le code nasl pour les instructions de type boucle
"""


def gen_loop(condition, instructions):
    loop_start = nom_nouvelle_etiquette()
    loop_end = nom_nouvelle_etiquette()

    # Évaluer la condition
    gen_expression(condition)

    nasm_instruction("pop", "eax", "", "", "Placer la valeur de la condition dans eax")

    # Sauter à loop_end si la condition est fausse
    nasm_instruction("cmp", "eax", "0", "", "Comparer eax à 0")
    nasm_instruction("je", loop_end, "", "", "Sauter à loop_end si la condition est fausse")

    # Instructions de la boucle
    nasm_instruction(loop_start + ":", "", "", "", "Début de la boucle")
    gen_listeInstructions(instructions)

    # Évaluer à nouveau la condition
    gen_expression(condition)

    nasm_instruction("pop", "eax", "", "", "Placer la valeur de la condition dans eax")

    # Sauter à loop_start si la condition est vraie
    nasm_instruction("cmp", "eax", "0", "", "Comparer eax à 0")
    nasm_instruction("jne", loop_start, "", "", "Sauter à loop_start si la condition est vraie")

    nasm_instruction(loop_end + ":", "", "", "", "Fin de la boucle")


"""def gen_if(condition, if_instructions, else_instructions=None):
    else_label = nom_nouvelle_etiquette()
    end_label = nom_nouvelle_etiquette()

    # Évaluer la condition
    gen_expression(condition)

    nasm_instruction("pop", "eax", "", "", "Placer la valeur de la condition dans eax")

    # Sauter à else_label si la condition est fausse
    nasm_instruction("cmp", "eax", "0", "", "Comparer eax à 0")
    nasm_instruction("je", else_label, "", "", "Sauter à else_label si la condition est fausse")

    # Instructions du "si"
    gen_instructions(if_instructions)

    # Sauter à end_label après l'exécution des instructions du "si"
    nasm_instruction("jmp", end_label, "", "", "Sauter à end_label")

    nasm_instruction(else_label + ":", "", "", "", "Étiquette du 'sinon'")

    if else_instructions:
        # Instructions du "sinon"
        gen_instructions(else_instructions)

    nasm_instruction(end_label + ":", "", "", "", "Étiquette de fin")"""

"""
Affiche le code nasm pour calculer l'opération boolean et la mettre en haut de la pile
"""


def gen_operation_boolean(operation):
    op = operation.op

    type_exp1 = gen_expression(operation.exp1)
    type_exp2 = gen_expression(operation.exp2)

    if type_exp1 != "boolean" or type_exp2 != "boolean":
        print("Erreur de type : Les opérateurs logiques doivent être appliqués à des booléens.")
        exit(0)

    if op == "ou":
        nasm_instruction("pop", "ebx", "", "", "Dépile la seconde opérande dans ebx")
        nasm_instruction("pop", "eax", "", "", "Dépile la première opérande dans eax")
        nasm_instruction("or", "eax", "ebx", "", "Opération logique OR (bitwise) entre eax et ebx")
    elif op == "et":
        nasm_instruction("pop", "ebx", "", "", "Dépile la seconde opérande dans ebx")
        nasm_instruction("pop", "eax", "", "", "Dépile la première opérande dans eax")
        nasm_instruction("and", "eax", "ebx", "", "Opération logique AND (bitwise) entre eax et ebx")
    elif op == "non":
        nasm_instruction("pop", "eax", "", "", "Dépile l'opérande dans eax")
        nasm_instruction("xor", "eax", "1", "", "Opération logique XOR (bitwise) avec 1 pour la négation")
    nasm_instruction("push", "eax", "", "", "Empile le résultat")

    return "boolean"


"""
Affiche le code nasm pour calculer l'opération et la mettre en haut de la pile
"""


def gen_operation(operation):
    op = operation.op

    gen_expression(operation.exp1)  # on calcule et empile la valeur de exp1
    gen_expression(operation.exp2)  # on calcule et empile la valeur de exp2

    nasm_instruction("pop", "ebx", "", "", "dépile la seconde operande dans ebx")
    nasm_instruction("pop", "eax", "", "", "dépile la permière operande dans eax")

    code = {"+": "add", "*": "imul", "-": "sub",
            "/": "idiv"}  # Un dictionnaire qui associe à chaque opérateur sa fonction nasm
    # Voir: https://www.bencode.net/blob/nasmcheatsheet.pdf
    if op in ['+', '-']:
        nasm_instruction(code[op], "eax", "ebx", "",
                         "effectue l'opération eax" + op + "ebx et met le résultat dans eax")
    if op == '*':
        nasm_instruction(code[op], "ebx", "", "", "effectue l'opération eax" + op + "ebx et met le résultat dans eax")

    elif op == '/':
        nasm_instruction("xor", "edx", "edx", "", "initialise edx à 0")
        nasm_instruction("idiv", "ebx", "", "", "effectue la division edx:eax / ebx")
    nasm_instruction("push", "eax", "", "", "empile le résultat");


if __name__ == "__main__":
    afficher_nasm = True
    lexer = FloLexer()
    parser = FloParser()
    if len(sys.argv) < 3 or sys.argv[1] not in ["-nasm", "-table"]:
        print("usage: python3 generation_code.py -nasm|-table NOM_FICHIER_SOURCE.flo")
        exit(0)
    if sys.argv[1] == "-nasm":
        afficher_nasm = True
    else:
        afficher_tableSymboles = True
    with open(sys.argv[2], "r") as f:
        data = f.read()
        try:
            arbre = parser.parse(lexer.tokenize(data))
            gen_programme(arbre)
        except EOFError:
            exit()