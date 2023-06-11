import sys
from copy import deepcopy

from cffi.ffiplatform import flatten

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


def is_nested(variable_defs):
    pass


def gen_programme1(programme):
    global is_in_function
    printifm('%include\t"io.asm"')
    printifm('section\t.bss')
    printifm('sinput:	resb	255	;reserve a 255 byte space in memory for the users input string')
    printifm('v$a:	resd	1')
    printifm('section\t.text')
    printifm('global _start')
    nasm_comment("===== Generating function declarations =====")
    programme_copy = deepcopy(programme)
    for instruction in programme_copy.liste_instructions.instructions:
        if type(instruction) == arbre_abstrait.FunctionDeclaration:
            gen_def_fonction(instruction)
    nasm_comment("===== End of function declarations =====")

    nasm_comment("===== Generating main function =====")
    printifm('main:')

    nasm_instruction("push", "ebp", "", "", "")
    nasm_instruction("mov", "ebp", "esp", "", "")
    # allocating space for local variables
    variable_defs = programme_copy.liste_instructions.get_variable_definitions()
    # flatten the list of lists of variable definitions
    while is_nested(variable_defs):
        variable_defs = flatten(variable_defs)

    space_for_local_variables = len(variable_defs) * 4
    nasm_instruction("sub", "esp", str(space_for_local_variables), "", "")
    for i in range(len(variable_defs)):
        variable_defs[i].offset = f"-{(i + 1) * 4}"

    global is_in_function
    gen_listeInstructions1(programme_copy.liste_instructions)
    nasm_instruction("leave", "", "", "", "")
    nasm_instruction("ret", "", "", "", "")
    nasm_comment("===== End of main function =====")
    printifm("_start:")
    nasm_instruction("call", "main", "", "", "")
    nasm_instruction("mov", "eax", "1", "", "1 est le code de SYS_EXIT")
    nasm_instruction("mov", "ebx", "0", comment="0 est le code de retour correct ici")
    nasm_instruction("int", "0x80", "", "", "exit")


"""

Affiche le code nasm correspondant à une suite d'instructions

"""


def gen_listeInstructions1(listeInstructions):
    for instruction in reversed(listeInstructions.instructions):
        gen_listeInstructions1(instruction)


"""

Affiche le code nasm correspondant à une instruction

"""


def gen_instructio1(instruction):
    if type(instruction) == arbre_abstrait.Ecrire:

        gen_ecrire1(instruction)

    else:

        print("type instruction inconnu", type(instruction))

        exit(0)


"""

Affiche le code nasm correspondant au fait d'envoyer la valeur entière d'une expression sur la sortie standard

"""


def gen_ecrire1(ecrire):
    gen_expression1(ecrire.exp)  # on calcule et empile la valeur d'expression

    nasm_instruction("pop", "eax", "", "", "")  # on dépile la valeur d'expression sur eax

    nasm_instruction("call", "iprintLF", "", "", "")  # on envoie la valeur d'eax sur la sortie standard


"""

Affiche le code nasm pour calculer et empiler la valeur d'une expression

"""


def gen_expression1(expression):
    if type(expression) == arbre_abstrait.Operation:

        gen_operation(expression)  # on calcule et empile la valeur de l'opération

    elif type(expression) == arbre_abstrait.BooleenOperation:

        gen_operation_booleen1(expression)

    elif type(expression) == arbre_abstrait.Entier:

        nasm_instruction("push", str(expression.valeur), "", "", "");  # on met sur la pile la valeur entière

    elif type(expression) == arbre_abstrait.Lire:

        nasm_instruction("mov", "eax", "sinput", "", "Place l'adresse de sinput dans eax")

        nasm_instruction("call", "readline", "", "",
                         "Lit une chaîne de caractères depuis l'entrée standard et place la valeur lue dans ebx")

        nasm_instruction("call", "atoi", "", "",
                         "Convertit la chaîne de caractères en entier et place le résultat dans eax")

        nasm_instruction("push", "eax", "", "", "Empile la valeur lue")

        return "entier"

    elif type(expression) == arbre_abstrait.Booleen:

        if expression.valeur == "Vrai":

            nasm_instruction("push", "1", "", "", "Empile la valeur booléenne True 1")

        else:

            nasm_instruction("push", "0", "", "", "Empile la valeur booléenne False 0")

        return "booleen"
    elif type(expression) == arbre_abstrait.Sinon:
        gen_condition(expression)
    elif type(expression) == arbre_abstrait.InstructionConditionnelle:
        gen_condition(expression)
    elif type(expression) == arbre_abstrait.SiNonSi:
        gen_condition(expression)
    elif type(expression) == arbre_abstrait.TantQue:
        gen_while(expression)
    elif type(expression) == arbre_abstrait.InstructionRetourner:
        gen_return_statement(expression)

    else:

        print("type d'expression inconnu", type(expression))

        exit(0)


"""

Affiche le code nasm pour calculer l'opération et la mettre en haut de la pile

"""


def gen_operation_booleen1(operation):
    op = operation.op

    type_exp1 = gen_expression1(operation.operande_gauche)

    type_exp2 = gen_expression1(operation.operande_droit)

    if type_exp1 != "booleen" or type_exp2 != "booleen":
        print("Erreur de type : Les opérateurs logiques doivent être appliqués à des booléens.")

        exit(0)

    if op == arbre_abstrait.OperationEnum.OR:

        nasm_instruction("pop", "ebx", "", "", "Dépile la seconde opérande dans ebx")

        nasm_instruction("pop", "eax", "", "", "Dépile la première opérande dans eax")

        nasm_instruction("or", "eax", "ebx", "", "Opération logique OR (bitwise) entre eax et ebx")

    elif op == arbre_abstrait.OperationEnum.AND:

        nasm_instruction("pop", "ebx", "", "", "Dépile la seconde opérande dans ebx")

        nasm_instruction("pop", "eax", "", "", "Dépile la première opérande dans eax")

        nasm_instruction("and", "eax", "ebx", "", "Opération logique AND (bitwise) entre eax et ebx")

    elif op == arbre_abstrait.OperationEnum.NOT:

        nasm_instruction("pop", "eax", "", "", "Dépile l'opérande dans eax")

        nasm_instruction("xor", "eax", "1", "", "Opération logique XOR (bitwise) avec 1 pour la négation")

    nasm_instruction("push", "eax", "", "", "Empile le résultat")

    return "booleen"


def gen_comparison1(operation):
    gen_expression1(operation.exp1)

    gen_expression1(operation.exp2)

    nasm_instruction("pop", "ebx", "", "", "Dépiler la deuxième opérande dans ebx")

    nasm_instruction("pop", "eax", "", "", "Dépiler la première opérande dans eax")

    cmp_instruction = {"==": "jne", "!=": "jne", "<": "jg", ">": "jl", "<=": "jge", ">=": "jle"}

    # Génère l'instruction de comparaison et saute vers l'étiquette appropriée

    label_false = nom_nouvelle_etiquette()

    label_end = nom_nouvelle_etiquette()

    nasm_instruction("cmp", "eax", "ebx", "", "Comparer eax et ebx")

    nasm_instruction(cmp_instruction[operation.operateur], label_false, "", "",
                     "Sauter à label_false si la comparaison est fausse")

    nasm_instruction("mov", "eax", "1", "", "Définir eax à 1 (vrai)")

    nasm_instruction("jmp", label_end, "", "", "Sauter à label_end")

    nasm_instruction(label_false + ":", "", "", "", "Label_false : définir eax à 0 (faux)")

    nasm_instruction("mov", "eax", "0", "", "")

    nasm_instruction(label_end + ":", "", "", "", "Label_end")

    nasm_instruction("push", "eax", "", "", "Empiler le résultat sur la pile")

    return "booleen"


def gen_operation(operation):
    op = operation.op

    gen_expression1(operation.exp1)

    gen_expression1(operation.exp2)

    nasm_instruction("pop", "ebx", "", "", "dépile la seconde operande dans ebx")

    nasm_instruction("pop", "eax", "", "", "dépile la permière operande dans eax")

    code = {"+": "add", "*": "imul", "-": "sub", "/": "idiv"}

    if op in ['+', '-']:
        nasm_instruction(code[op], "eax", "ebx", "",
                         "effectue l'opération eax" + op + "ebx et met le résultat dans eax")

    if op == '*':
        nasm_instruction(code[op], "ebx", "", "", "effectue l'opération eax" + op + "ebx et met le résultat dans eax")

    if op == '/':
        nasm_instruction("xor", "edx", "edx", "", "initialise edx à 0")

        nasm_instruction("idiv", "ebx", "", "", "effectue la division edx:eax / ebx")

    nasm_instruction("push", "eax", "", "", "empile le résultat")


def gen_condition(condition: arbre_abstrait.Sinon or arbre_abstrait.InstructionConditionnelle):
    nasm_comment(f"===== Generating condition =====")
    label_else = nasm_nouvelle_etiquette()
    label_fin = nasm_nouvelle_etiquette()
    gen_expression1(condition.expr)
    nasm_instruction("pop", "eax", "", "", "")
    nasm_instruction("cmp", "eax", "0", "", "")
    nasm_instruction("je", label_else, "", "", "")
    gen_listeInstructions1(condition.scope1)
    nasm_instruction("jmp", label_fin, "", "", "")
    printift(label_else + ":")
    printift(label_fin + ":")
    nasm_instruction("push", "eax", "", "", "")
    nasm_comment(f"===== Finished generating condition =====")


def gen_while(while_statement: arbre_abstrait.TantQue):
    nasm_comment(f"===== Generating while loop =====")
    label_debut = nasm_nouvelle_etiquette()
    label_fin = nasm_nouvelle_etiquette()
    printift(label_debut + ":")
    gen_expression1(while_statement.expr)
    nasm_instruction("pop", "eax", "", "", "")
    nasm_instruction("cmp", "eax", "0", "", "")
    nasm_instruction("je", label_fin, "", "", "")
    gen_listeInstructions1(while_statement.scope)
    nasm_instruction("jmp", label_debut, "", "", "")
    printift(label_fin + ":")
    nasm_instruction("push", "eax", "", "", "")
    nasm_comment(f"===== Finished generating while loop =====")

def gen_return_statement(return_statement: arbre_abstrait.InstructionRetourner):
    nasm_comment(f"===== Generating return statement =====")
    gen_expression1(return_statement.exp)
    nasm_instruction("pop", "eax", "", "", comment="Pop return value from stack")
    nasm_instruction("leave", "", "", "", comment="Clean up stack")
    nasm_instruction("ret", "", "", "", comment="Return to caller")
    nasm_comment(f"===== Finished generating return statement =====")

def gen_def_fonction(function: arbre_abstrait.FunctionDeclaration):
    nasm_comment(f"===== Generating function {function.name} =====")
    printift(f"_{function.name}:")
    nasm_comment(f"===== Initialising function {function.name} =====")
    nasm_instruction("push", "ebp", "", "", "")
    nasm_instruction("mov", "ebp", "esp", "", "")

    nasm_comment(f"===== Storing arguments of function {function.name} =====")
    # storing the arguments in FunctionDeclaration.args
    for i in range(len(function.args)):
        nasm_comment(f"===== Storing argument {function.args[i].name} =====")
        function.args[i].offset = f"+{(len(function.args) - i - 1) * 4 + 8}"
        nasm_comment(f"===== Stored argument {function.args[i].name} at offset {function.args[i].offset} =====")
    nasm_comment(f"===== Allocating local variables of function {function.name} =====")
    # allocating space for local variables
    variable_defs = function.scope.get_variable_definitions()


    nasm_comment(f"===== Found {len(variable_defs)} local variables in function {function.name} =====")

    space_for_local_variables = len(variable_defs) * 4
    nasm_instruction("sub", "esp", str(space_for_local_variables), "",
                     f"Substracting space for local variables from esp ({space_for_local_variables})")
    for i in range(len(variable_defs)):
        nasm_comment(f"===== Storing local variable {variable_defs[i].name} =====")
        variable_defs[i].offset = f"-{(i + 1) * 4}"
        nasm_comment(f"===== Stored local variable {variable_defs[i].name} at offset {variable_defs[i].offset} =====")

    global is_in_function
    is_in_function = True
    nasm_comment(f"===== Generating instructions of function {function.name} =====")
    gen_listeInstructions1(function.scope)
    nasm_comment(f"===== Finished generating instructions of function {function.name} =====")
    nasm_comment(f"===== Cleaning up function {function.name} =====")
    nasm_instruction("leave", "", "", "", comment="Clean up stack")
    nasm_instruction("ret", "", "", "", comment="Return to caller")
    nasm_comment(f"===== Finished cleaning up function {function.name} =====")
    nasm_comment(f"===== Finished generating function {function.name} =====")
    is_in_function = False



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

            gen_programme1(arbre)

        except EOFError:

            exit()
