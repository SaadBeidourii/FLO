import sys
from sly import Parser

import analyse_lexicale
from analyse_lexicale import FloLexer
import arbre_abstrait


class FloParser(Parser):
    # Get the list of tokens from the lexical analysis
    tokens = FloLexer.tokens
    debugfile = 'parser.out'

    # Grammar rules and associated actions

    @_('prog')
    def start(self, p):
        return p.prog

    @_('fonction listeInstructions')
    def prog(self, p):
        return arbre_abstrait.Programme(p.fonction, p.listeInstructions)

    @_('')
    def fonction(self, p):
        return None

    @_('declaration fonction')
    def fonction(self, p):
        return arbre_abstrait.Fonction(p.declaration, p.fonction)

    @_('DECLARATION TYPE IDENTIFIANT ";"')
    def declaration(self, p):
        return arbre_abstrait.Declaration(p.TYPE, p.IDENTIFIANT)

    @_('AFFECTATION IDENTIFIANT "=" expression ";"')
    def declaration(self, p):
        return arbre_abstrait.Affectation(p.IDENTIFIANT, p.expression)

    @_('DECLARATION TYPE IDENTIFIANT "=" expression ";"')
    def declaration(self, p):
        return arbre_abstrait.DeclarationAffectation(p.TYPE, p.IDENTIFIANT, p.expression)

    @_('instruction')
    def listeInstructions(self, p):
        l = arbre_abstrait.ListeInstructions()
        l.ajouter_instruction(p.instruction)
        return l

    @_('instruction listeInstructions')
    def listeInstructions(self, p):
        p.listeInstructions.ajouter_instruction(p.instruction)
        return p.listeInstructions

    @_('ecrire')
    def instruction(self, p):
        return p.ecrire

    @_('ECRIRE "(" expression ")" ";"')
    def ecrire(self, p):
        return arbre_abstrait.Ecrire(p.expression)

    @_('SI "(" expression ")" "{" listeInstructions "}"')
    def instruction(self, p):
        return arbre_abstrait.InstructionConditionnelle(p.expression, p.listeInstructions)

    @_('SI "(" expression ")" "{" listeInstructions "}" SINON SI "(" expression ")" "{" listeInstructions "}"')
    def instruction(self, p):
        return arbre_abstrait.InstructionConditionnelle(p.expression, p.listeInstructions, [(p.expression2, p.listeInstructions2)])

    @_('SI "(" expression ")" "{" listeInstructions "}" SINON "{" listeInstructions "}"')
    def instruction(self, p):
        return arbre_abstrait.InstructionConditionnelle(p.expression, p.listeInstructions, p.listeInstructions2)

    @_('TANT_QUE "(" expression ")" "{" listeInstructions "}"')
    def instruction(self, p):
        return arbre_abstrait.InstructionBoucleTantQue(p.expression, p.listeInstructions)


if __name__ == '__main__':
    lexer = FloLexer()
    parser = FloParser()
    if len(sys.argv) < 2:
        print("usage: python3 analyse_syntaxique.py NOM_FICHIER_SOURCE.flo")
    else:
        with open(sys.argv[1], "r") as f:
            data = f.read()
            try:
                arbre = parser.parse(lexer.tokenize(data))
                arbre.afficher()
            except EOFError:
                exit()
