import string

# automata(name, alpha, states, program, inicialState, finalStates)
# Um elemento pertencente a classe automata é uma
#	name : é uma string que informa o nome dado ao autômato.
#	alpha : é uma lista de strings, em que cada elemento da lista é um componente do alfabeto.
#	states : é uma lista de números variando de 0 a n em que n é número de estados do autômato decrementado de uma unidade.
#	program : é, ou
#		- uma lista vazia, ou
# 		- uma lista de 3-uplas em que cada elemento será, respectivamente:
#			state1 = estado atual do autômato.
#			letter = letra que é necessária para aplicação da função programa naquele estado.
#			state2 = próximo estado de acordo com a letra indicada.
#	inicialState : é um número que indica o estado inicial do autômato, dentre aqueles pertencentes a states.
#	finalStates : é uma lista de estados que está contido ou é igual a states e possui os estados finais do autômato.
# Além disso, dado um elemento X dessa classe, X possui as seguintes funções:
#	X.clear(): limpa todos os dados da classe.
#	X.setName(name): define o nome do autômato.
#	X.setAlpha(alpha): define o alfabeto do autômato.
#	X.setStates(states): define o conjunto de estados do autômato.
#	X.setProgram(program): define o conjunto de funções programa do autômato.
#	X.setInicialState(inicialState): define o estado inicial do autômato.
#	X.setFinalStates(finalStates): define o conjunto de estados finais do autômato.
class automata:
	def __init__(self):
		self.name = None
		self.alpha = []
		self.states = []
		self.program = []
		self.inicialState = None
		self.finalStates = []

	def clear(self):
		self = automata()

	def setName(self, name):
		self.name = name

	def setAlpha(self, alpha):
		self.alpha = alpha

	def setStates(self, states):
		self.states = states

	def setProgram(self, program):
		self.program = program

	def setInicialState(self, inicialState):
		self.inicialState = inicialState

	def setFinalStates(self, finalStates):
		self.finalStates = finalStates

	def insertProgram(self, state1, letter, state2):
		self.program.append((state1, letter, state2))

# getSubset: string char -> list(string)
# Objetivo: dada uma string e um caractere referente ao separador dos subconjuntos presentes na string, a função retorna
#	uma lista com os subconjuntos dados na string. Os possíveis separadores são:
#		- '}' ou ']'.
# Observação: os elementos dos subconjuntos devem estar separados por vírgula e não devem possuir o caractere separador.
# Exemplos: getSubset("", '') -> []
#			getSubset("a,b,c", '}') -> []
#			getSubset("}a,b,c{", '}') -> []
#			getSubset("{a,b,c}", '}') -> [['a','b','c']]
#			getSubset("[1,2,3],[a,b,c]", ']') -> [['1','2','3'],['a','b','c']]
def getSubset(string, separator):
	if string == "":
		return []
	else:
		begin = string.find(chr(ord(separator) - 2))
		if begin == -1:
			return []
		else:
			end = string.find(separator)
			if end == -1 or begin >= end:
				return []
			else:
				auxiliarString = string[begin+1:end]
				auxiliar = auxiliarString.split(',')
				if end + 2 >= len(string):
					return [auxiliar]
				else:
					auxiliar = [auxiliar] + getSubset(string[end + 2:], separator)
					return auxiliar

# isSubset(list, list) -> boolean
# Objetivo: dadas duas listas, verifica se a segunda lista é sublista da primeira, retornando True, nesse caso.
#	Senão, retorna False.
# Observação: listas permutadas são a mesma lista nessa função.
# Exemplo:  isSubset([],[]) -> True
#			isSubset([1,2,3], []) -> True
#			isSubset([], [1,2,3]) -> False
#			isSubset([1,2,3], [2,3]) -> True
def isSubset(original, subset):
	count = 0
	if subset == []:
		return True
	elif original == []:
		return False
	else:
		for x in subset:
			if x in original:
				count += 1
		if count == len(subset):
			return True
		else:
			return False

# delDuplicates(list) -> list
# Objetivo: dada uma lista, retorna essa lista retirando os elementos duplicados.
# Exemplos: delDuplicates([]) -> []
#			delDuplicates([1]) -> [1]
#			delDuplicates([1,1]) -> [1]
def delDuplicates(lst):
  return list(dict.fromkeys(lst))

## DAQUI PARA BAIXO SÓ TEM TRISTEZA

# automato = automata()
# auxiliarString = input()
# auxiliar = auxiliarString.split('=')
#
# automato.setName(auxiliar.pop(0))
#
# if auxiliar == []:
# 	print("Erro na inserção dos dados.")
# else:
# 	auxiliarString = auxiliar.pop(0)
#
# 	auxiliarString = auxiliarString.replace(' ', '')
# 	auxiliarString = auxiliarString.replace('(', '')
# 	auxiliarString = auxiliarString.replace(')', '')
#
# 	# print(auxiliarString)
# 	auxiliar = getSubset(auxiliarString, '}')
# 	# print(auxiliar)
#
# 	if len(auxiliar) != 3 or (not isSubset(auxiliar[0], auxiliar[2])) or auxiliar[0] != delDuplicates(auxiliar[0]) or auxiliar[1] != delDuplicates(auxiliar[1]) or auxiliar[2] != delDuplicates(auxiliar[2]):
# 		print("Erro na inserção dos dados.")
# 	else:
# 		automato.setStates(auxiliar[0])
# 		automato.setAlpha(auxiliar[1])
# 		automato.setFinalStates(auxiliar[2])
#
# 		auxiliar = auxiliarString.split('}')
# 		if len(auxiliar) < 2:
# 			print("Erro na inserção dos dados.")
# 		else:
# 			auxiliar = auxiliar[-2].split('{')
# 			auxiliar = auxiliar[-2].replace(',', '')
#
# 			if not auxiliar in automato.states:
# 				print("Erro na inserção dos dados.")
# 			else:
# 				automato.setInicialState(auxiliar)
#
# 				if input() != "Prog":
# 					print("Erro na inserção dos dados.")
# 				else:
# 					for i in range(len(automato.states)):
# 						for j in range(len(automato.alpha)):
# 							auxiliarString = input()
# 							auxiliar = auxiliarString.split('=')
# 							if len(auxiliar) != 2:
# 								print("Erro na inserção dos dados.8")
# 							else:
# 								auxiliar[0] = auxiliar[0].replace('(', '')
# 								auxiliar[0] = auxiliar[0].replace(')', '')
# 								auxiliar[0] = auxiliar[0].split(',')
# 								if len(auxiliar[0]) != 2 or not auxiliar[0][0] in automato.states or not auxiliar[0][1] in automato.alpha or not auxiliar[1] in automato.states:
# 									print("Erro na inserção dos dados.9")
# 								else:
# 									automato.insertProgram(auxiliar[0][0], auxiliar[0][1], auxiliar[1])
