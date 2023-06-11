import sys
from sly import Lexer


class FloLexer(Lexer):
    # Noms des lexèmes (sauf les litéraux). En majuscule. Ordre non important
    tokens = {IDENTIFIANT, TYPE, ENTIER, ECRIRE, INFERIEUR_OU_EGAL, LIRE, SI, SINON, SINON_SI, TANT_QUE,
              RETOURNER, EGAL, SUPERIEUR_OU_EGAL, BOOLEEN, NON_EGAL, ET, OU, NON, FAUX, VRAI, RETOURNER, INFERIEUR,
              SUPERIEUR}

    # Les caractères litéraux sont des caractères uniques qui sont retournés tel quel quand rencontré par l'analyse lexicale.
    # Les litéraux sont vérifiés en dernier, après toutes les autres règles définies par des expressions régulières.
    # Donc, si une règle commence par un de ces littérals (comme INFERIEUR_OU_EGAL), cette règle aura la priorité.
    literals = {'+', '*', '(', ')', ";", "-", "/", "%", ",", "{", "}", "="}

    # chaines contenant les caractère à ignorer. Ici espace et tabulation
    ignore = ' \t'

    @_(r'0|[1-9][0-9]*')
    def ENTIER(self, t):
        t.value = int(t.value)
        return t

    # cas général
    IDENTIFIANT = r'[a-zA-Z][a-zA-Z0-9_]*'  # en général, variable ou nom de fonction
    IDENTIFIANT['si'] = SI
    IDENTIFIANT['sinon'] = SINON
    IDENTIFIANT[r'sinon_si'] = SINON_SI
    IDENTIFIANT['tantque'] = TANT_QUE
    IDENTIFIANT['retourner'] = RETOURNER
    IDENTIFIANT['Vrai'] = BOOLEEN
    IDENTIFIANT['Faux'] = BOOLEEN
    IDENTIFIANT['et'] = ET
    IDENTIFIANT['ou'] = OU

    NON = r'!'
    EGAL = r'=='
    INFERIEUR_OU_EGAL = r'<='
    SUPERIEUR_OU_EGAL = r'>='
    INFERIEUR = r'<'
    SUPERIEUR = r'>'

    # cas spéciaux:
    IDENTIFIANT['ecrire'] = ECRIRE
    IDENTIFIANT['booleen'] = TYPE
    IDENTIFIANT['entier'] = TYPE

    # Syntaxe des commentaires à ignorer
    ignore_comment = r'\#.*'

    # Permet de conserver les numéros de ligne. Utile pour les messages d'erreurs

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # En cas d'erreur, indique où elle se trouve
    def error(self, t):
        print(f'Ligne{self.lineno}: caractère inattendu "{t.value[0]}"')
        self.index += 1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: python3 analyse_lexicale.py NOM_FICHIER_SOURCE.flo")
    else:
        with open(sys.argv[1], "r") as f:
            data = f.read()
            lexer = FloLexer()
            for tok in lexer.tokenize(data):
                print(tok)
