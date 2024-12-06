"""
Arquivo auxiliar com dados utilizados
"""

# tokens da linguagem 
tokens = (
  'CMDS',
  'CMD',
  'FACA',
  'SER',
  'SOME',
  'MOSTRE',
  'FIM',
  'REPITA',
  'VEZES',
  'MULTIPLIQUE',
  'SE',
  'ENTAO',
  'SENAO',
  'var',
  'numero'
)

class Variaveis():
  vars: set

  def __init__(self):
    self.vars = set()
  
  def update_variaveis(self, conjunto):
    """
    Método para incluir no conjunto as variáveis encontradas
    """
    self.vars = self.vars.union(set(conjunto))

  def get_variaveis(self):
    return self.vars