import sys
from ply import lex, yacc

# Definição dos tokens
tokens = (
    'FACA', 'SER', 'MOSTRE', 'SOME', 'COM', 'MULTIPLIQUE', 'REPITA', 'VEZES', 'FIM',
    'var', 'numero'
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

def t_var(t):
    r'[a-zA-Z_]*'
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
    print("Erro de token: ", t.value)
    t.lexer.skip(1)

# Passo 2: Análise sintática

def p_programa(p):
    '''programa : cmds'''
    p[0] = p[1]

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
           | repeticao'''
    p[0] = '\t' + p[1]

def p_atribuicao(p):
    '''atribuicao : FACA var SER numero'''
    p[0] = f'int {p[2]} = {p[4]};'

def p_impressao(p):
    '''impressao : MOSTRE var
                 | MOSTRE operacao'''
    p[0] = f'printf("{p[2]} = %d\\n", {p[2]});'

def p_operacao(p):
    '''operacao : SOME var COM var
                | SOME var COM numero
                | SOME numero COM var
                | SOME numero COM numero
                | MULTIPLIQUE var COM var
                | MULTIPLIQUE var COM numero
                | MULTIPLIQUE numero COM var
                | MULTIPLIQUE numero COM numero'''
    p[0] = f'{p[2]} {p[1]} {p[4]}'

def p_repeticao(p):
    '''repeticao : REPITA numero VEZES cmds FIM'''
    loop = f'\tfor(int i = 0; i < {p[2]}; i++)' + '{\n'
    loop += '\t' + p[4] + '\n}\n'
    p[0] = loop

def p_error(p):
    print("Erro de sintaxe: ", p)

# Passo 3: Chamando a função e gerando o arquivo de saída

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

args = sys.argv
input_path, output_path = get_file_paths(args)

lexer = lex.lex()
yaccer = yacc.yacc()

try:
    with open(input_path, "r") as f_in:
        mag_code = f_in.read()
    result = yaccer.parse(mag_code)
    with open(output_path, "w") as f_out:
        f_out.write(result)
except Exception as e:
    print(e)
