import sys
from ply import lex, yacc

# Definição dos tokens
tokens = (
    'var', 'numero', 'PONTO', 'FACA', 'SER', 'MOSTRE', 'SOME', 'COM',
    'MULTIPLIQUE', 'REPITA', 'VEZES', 'FIM', 'SE', 'SENAO', 'ENTAO'
)

# Definição das expressões regulares para os tokens
t_FACA = r'FACA'
t_SER = r'SER'
t_MOSTRE = r'MOSTRE'
t_SOME = r'SOME'
t_COM = r'COM'
t_MULTIPLIQUE = r'MULTIPLIQUE'
t_REPITA = r'REPITA'
t_VEZES = r'VEZES'
t_FIM = r'FIM'
t_ENTAO = r'ENTAO'
t_SENAO = r'SENAO'
t_SE = r'SE'
t_PONTO = r'\.'

def t_var(t):
    r'[a-zA-Z_][a-zA-Z_]*'

    if t.value in tokens:
        t.type = t.value

    return t

def t_numero(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Erro léxico: Caracter inválido '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()


# Definições da gramática

def p_programa(p):
    '''programa : cmds'''
    p[0] = '#include <stdio.h>\n\n' + 'int main(void){\n'
    p[0] += p[1] + '\n}'

def p_cmds(p):
    '''cmds : cmds cmd
            | cmd'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + '\n' + p[2]

def p_cmd(p):
    '''cmd : atribuicao
           | impressao
           | operacao
           | repeticao
           | condicional'''
    p[0] = p[1]

def p_atribuicao(p):
    '''atribuicao : FACA var SER numero PONTO'''
    p[0] = f'int {p[2]} = {p[4]};'

def p_impressao(p):
    '''impressao : MOSTRE var PONTO
                 | MOSTRE operacao PONTO
                 | MOSTRE numero PONTO'''
    if isinstance(p[2], str):
        p[0] = f'printf("%d\\n", {p[2]});'
    else:
        p[0] = f'printf("%d\\n", {p[2]});'

def p_operacao(p):
    '''operacao : SOME var COM var PONTO
                | SOME var COM numero PONTO
                | SOME numero COM var PONTO
                | SOME numero COM numero PONTO
                | MULTIPLIQUE var COM var PONTO
                | MULTIPLIQUE var COM numero PONTO
                | MULTIPLIQUE numero COM var PONTO
                | MULTIPLIQUE numero COM numero PONTO'''
    if p[1] == 'SOME':
        op = '+'
    elif p[1] == 'MULTIPLIQUE':
        op = '*'
    p[0] = f'({p[2]} {op} {p[4]})'

def p_repeticao(p):
    '''repeticao : REPITA numero VEZES cmds FIM'''
    loop = f'for(int i = 0; i < {p[2]}; i++)' + '{\n'
    loop += p[4] + '\n}\n'
    p[0] = loop

def p_error(p):
    print(f"Erro de sintaxe: {p}")

def p_condicional(p):
  '''condicional : SE var ENTAO cmds FIM
                 | SE var ENTAO cmds SENAO cmds FIM'''
  cond = f'if({p[2]})' + '{\n'
  cond += p[4] + '\n\t}'
  if len(p) == 7:
    cond += '\n\telse' + '{\n'
    cond += p[6] + '\n\t}'
  
  p[0] = cond

# Construir o parser
parser = yacc.yacc()


def get_file_paths(args):
    argc = len(args)
    if argc > 1:
        input_path = args[1]
        if argc == 3:
            output_path = args[2]
            if not output_path.endswith('.c'):
                output_path += '.c'
        else:
            output_path = "exemplo.c"
    else:
        input_path = "exemplo.mag"
        output_path = "exemplo.c"
    return input_path, output_path

def main():
    args = sys.argv
    input_path, output_path = get_file_paths(args)

    lexer = lex.lex()
    parser = yacc.yacc()

    try:
        with open(input_path, "r") as f_in:
            mag_code = f_in.read()
        result = parser.parse(mag_code)
        if result is not None:
            with open(output_path, "w") as f_out:
                f_out.write(result)
        else:
            print("Erro: Nenhuma saída gerada.")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
