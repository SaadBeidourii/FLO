import sys
from sly import Parser

import analyse_lexicale
from analyse_lexicale import FloLexer
import arbre_abstrait


class FloParser(Parser):
    # On récupère la liste des lexèmes de l'analyse lexicale
    tokens = FloLexer.tokens
    debugfile = 'parser.out'

    # Règles gramaticales et actions associées

    @_('listeInstructions')
    def prog(self, p):
        return arbre_abstrait.Programme(p[0])

    @_('instruction')
    def listeInstructions(self, p):
        l = arbre_abstrait.ListeInstructions()
        l.instructions.append(p[0])
        return l

    @_('instruction listeInstructions')
    def listeInstructions(self, p):
        p[1].instructions.append(p[0])
        return p[1]

    @_('ecrire')
    def instruction(self, p):
        return p[0]

    @_('ECRIRE "(" expr ")" ";"')
    def ecrire(self, p):
        return arbre_abstrait.Ecrire(p.expr)  # p.expr = p[2]

    ################################
    @_('"(" expr ")"')
    def facteur(self, p):
        return p.expr  # ou p[1]

    @_('ENTIER')
    def facteur(self, p):
        return arbre_abstrait.Entier(p.ENTIER)

    @_('facteur')
    def produit(self, p):
        return p[0]

    @_('produit "*" facteur')
    def produit(self, p):
        return arbre_abstrait.Operation('*', p[0], p[2])

    @_('produit "/" facteur')
    def produit(self, p):
        return arbre_abstrait.Operation('/', p[0], p[2])

    @_('produit "%" facteur')
    def produit(self, p):
        return arbre_abstrait.Operation('%', p[0], p[2])

    @_('produit')
    def expr(self, p):
        return p[0]

    @_('expr "+" produit')
    def expr(self, p):
        return arbre_abstrait.Operation('+', p[0], p[2])

    @_('expr "-" produit')
    def expr(self, p):
        return arbre_abstrait.Operation('-', p[0], p[2])

    @_(' "-" facteur')
    def expr(self, p):
        return arbre_abstrait.Operation("*", arbre_abstrait.Entier(-1), p[1])

    @_('IDENTIFIANT')
    def facteur(self, p):
        return arbre_abstrait.Variable(p.IDENTIFIANT)

    @_('LIRE "(" ")"')
    def facteur(self):
        return arbre_abstrait.Lire()

    @_('IDENTIFIANT "(" ")"')
    def facteur(self, p):
        return arbre_abstrait.AppelFonction(p.IDENTIFIANT, [])

    @_('IDENTIFIANT "(" exprList ")"')
    def facteur(self, p):
        return arbre_abstrait.AppelFonction(p.IDENTIFIANT, p.exprList)

    @_('expr')
    def exprList(self, p):
        return arbre_abstrait.ExprList(p.expr)

    @_('expr "," exprList')
    def exprList(self, p):
        return arbre_abstrait.ExprList(p.expr, p.exprList)

    @_('booleen')
    def expr(self, p):
        return p[0]

    @_('BOOLEEN')
    def booleen(self, p):
        return arbre_abstrait.Booleen(p.BOOLEEN)

    @_('NON booleen')
    def booleen(self, p):
        return arbre_abstrait.Operation('NON', p.booleen)

    @_('booleen ET booleen')
    def booleen(self, p):
        return arbre_abstrait.Operation('ET', p[0], p[2])

    @_('booleen OU booleen')
    def booleen(self, p):
        return arbre_abstrait.Operation('OU', p[0], p[2])

    # En supposant que vous avez également des opérations de comparaison
    @_('facteur EGAL facteur')
    def booleen(self, p):
        return arbre_abstrait.BooleenOperation('EGAL', p[0], p[2])

    @_('facteur NON_EGAL facteur')
    def booleen(self, p):
        return arbre_abstrait.BooleenOperation('NON_EGAL', p[0], p[2])

    @_('facteur INFERIEUR_OU_EGAL facteur')
    def booleen(self, p):
        return arbre_abstrait.BooleenOperation('INFERIEUR_OU_EGAL', p[0], p[2])

    @_('facteur SUPERIEUR_OU_EGAL facteur')
    def booleen(self, p):
        return arbre_abstrait.BooleenOperation('SUPERIEUR_OU_EGAL', p[0], p[2])
    @_('facteur INFERIEUR facteur')
    def booleen(self, p):
        return arbre_abstrait.BooleenOperation('INFERIEUR', p[0], p[2])
    @_('facteur SUPERIEUR facteur')
    def booleen(self, p):
        return arbre_abstrait.BooleenOperation('SUPERIEUR', p[0], p[2])

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