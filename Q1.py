import string

# automata(name, alpha, states, program, initialState, finalStates)
# Um elemento pertencente a classe automata é uma
#	name : é uma string que informa o nome dado ao autômato.
#	alpha : é uma lista de strings, em que cada elemento da lista é um componente do alfabeto.
#	states : é uma lista de estados do mesmo tipo (ANY) equivalente ao conjunto de estados do autômato, onde:
#	program : é, ou
#		- uma lista vazia, ou
# 		- uma lista de 3-uplas em que cada elemento será, respectivamente:
#			state1 = estado atual do autômato.
#			letter = letra que é necessária para aplicação da função programa naquele estado.
#			state2 = próximo estado de acordo com a letra indicada.
#	initialState : é o estado inicial do autômato.
#	finalStates : é uma lista de estados que está contido ou é igual a states e possui os estados finais do autômato.
# Além disso, dado um elemento X dessa classe, X possui as seguintes funções:
#	X.clear(): limpa todos os dados da classe.
#	X.setName(name): define o nome do autômato.
#	X.setAlpha(alpha): define o alfabeto do autômato.
#	X.setStates(states): define o conjunto de estados do autômato.
#	X.setProgram(program): define o conjunto de funções programa do autômato.
#	X.setInitialState(initialState): define o estado inicial do autômato.
#	X.setFinalStates(finalStates): define o conjunto de estados finais do autômato.
#	X.insertState(state): insere um estado no conjunto de estados do autômato.
#	X.insertFinalState(state): insere um estado no conjunto de estados finais do autômato.
#		Caso o estado não pertença ao conjunto de estados do autômato, retorna False e não insere
#		ele no conjunto de estados finais. Senão, insere ele e retora True.
#	X.insertTransition(state1, letter, state2): insere uma 3-upla no conjunto de funções programa do autômato.
class automata:
	def __init__(self):
		self.name = None
		self.alpha = []
		self.states = []
		self.program = []
		self.initialState = None
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

	def setInitialState(self, initialState):
		self.initialState = initialState

	def setFinalStates(self, finalStates):
		self.finalStates = finalStates

	def insertState(self, state):
		self.states.append(state)

	def insertFinalState(self, state):
		if state in self.states:
			self.finalStates.append(state)
			return True
		else:
			return False

	def insertTransition(self, state1, letter, state2):
		self.program.append((state1, letter, state2))

	# getTransitions(state, char) -> list
	# Objetivo: dado um estado e uma letra, a função devolve uma lista de transições que partem do estado em questão e utilizam a letra para fazer a transição.
	def getTransitions(self, state, letter):
		list = []
		for transition in self.program:
			if state == transition[0] and letter == transition[1]:
				list.append(transition)
		return list

	# checkWord(string) -> boolean
	# Objetivo: dada uma palavra, a função verifica se a palavra pertence a linguagem dada pelo autômato em questão. Caso pertença, devolve True. Senão, devolve False.
	def checkWord(self, string):
		def checkWordRecursive(automata, currentState, string):
			boolFlag = False
			if string == "":
				if currentState in automata.finalStates:
					return True
				else:
					return False
			else:
				for i in range(1,len(string)+1):
					transitions = automata.getTransitions(currentState, string[0:i])
					for transition in transitions:
						boolFlag = boolFlag or checkWordRecursive(automata, transition[2], string[i:])
						break
				return boolFlag
		return checkWordRecursive(self, self.initialState, string)

	# convertToDFA(automata) -> automata
	# Objetivo: dado um automato não-determinístico, essa função devolve um autômato determinístico equivalente.
	def convertToDFA(self):
		# isFinalState(automata, DFAstate) -> boolean
		# Objetivo: dado um autômato não-determinístico e um estado da conversão desse autômato para um determinístico, retorna True caso esse estado seja final e False, caso contrário.
		#	DFAstate: é um estado dado por uma lista de estados referentes aos estados do autômato que será transformado.
		def isFinalState(automata, DFAstate):
			for state in automata.finalStates:
				if state in DFAstate:
					return True
			return False

		DFAversion = automata()
		DFAversion.name = self.name
		DFAversion.alpha = self.alpha
		DFAversion.insertState([self.initialState])
		DFAversion.initialState = [self.initialState]

		if self.initialState in self.finalStates:
			DFAversion.insertFinalState([self.initialState])

		for DFAstate in DFAversion.states:
			for letter in DFAversion.alpha:
				auxiliarDFAstate = []

				# Verificando as transições para cada "subestado", visto que a transição do estado <qaqbqc...qx> com 'a' letra a se dá pela união das transições de cada "subestado" 'qi' com a mesma letra 'a'.
				for state in DFAstate:
					auxiliarList = []
					auxTransitions = self.getTransitions(state, letter)
					for transition in auxTransitions:
						auxiliarList.append(transition)
						auxiliarDFAstate.append(transition[2])

				if auxiliarDFAstate:
					# Normalizando o estado
					auxiliarDFAstate = delDuplicates(auxiliarDFAstate)
					auxiliarDFAstate.sort()

					# Inserindo a transição ou/e o estado no conjunto de estados ou/e no conjunto de estados finais.
					DFAversion.insertTransition(DFAstate, letter, auxiliarDFAstate)
					if auxiliarDFAstate not in DFAversion.states:
						DFAversion.insertState(auxiliarDFAstate)
						if isFinalState(self, auxiliarDFAstate):
							DFAversion.insertFinalState(auxiliarDFAstate)
		return DFAversion

# --------------------------------------- Funções auxiliares ---------------------------------------

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


# getInitialState(string) -> string
# Objetivo: dada uma string no seguinte formato:
#		<M>=({<q0>,...,<qn>},{<s1>,...,<sn>},<ini>,{ <f0>,...,<fn>}), onde
#		< M >: nome dado ao autômato;
# 		< qi >: para 0 ≤ i ≤ n, com n ∈ N e n ≥ 0, representa um estado do autômato;
# 		< si >: para 1 ≤ i ≤ n, com n ∈ N e n ≥ 1, representa um símbolo do alfabeto da
# 			linguagem reconhecida pelo autômato;
# 		< ini >: indica o estado inicial do autômato, sendo que ini é um estado do autômato;
# 		< fi >: para 0 ≤ i ≤ n, com n ∈ N e n ≥ 0, representa um estado final do autômato,
# 			sendo que fi é um estado do autômato;
#	A função retorna o estado final do autômato.
def getInitialState(string):
	count = 0
	index = 0
	beginInitialState = -1
	endInitialState = -1
	for char in string:
		index += 1
		if char == '}' or char == '{':
			count += 1
			if count == 4:
				beginInitialState = index + 2
			elif count == 5:
				endInitialState = index - 2
	return string[beginInitialState-1:endInitialState]


# readFromFile(automata, string) -> int
# Objetivo: dado um elemento da classe automata e o nome de um arquivo no seguinte formato:
# 		<M>=({<q0>,...,<qn>},{<s1>,...,<sn>},<ini>,{ <f0>,...,<fn>})
# 		Prog
# 		(<q0>,<s1>)=<q1>
# 		...
# 		(<qn>,<sn>)=<q0>
#
# 		onde:
# 		<M>: nome dado ao autômato;
# 		<qi>: para 0 ≤ i ≤ n, com n ∈ N e n ≥ 0, representa um estado do autômato;
# 		<si>: para 1 ≤ i ≤ n, com n ∈ N e n ≥ 1, representa um símbolo do alfabeto da
# 			linguagem reconhecida pelo autômato;
# 		<ini>: indica o estado inicial do autômato, sendo que ini é um estado do autômato;
# 		<fi>: para 0 ≤ i ≤ n, com n ∈ N e n ≥ 0, representa um estado final do autômato,
# 			sendo que fi é um estado do autômato;
# 		(<qi>, <si>)=<qj>: descreve a função programa aplicada a um estado qi e um
# 			símbolo de entrada si que leva a computação a um estado qj.
#	A função lê esse arquivo e armazena os dados na classe automata.
#	A função pode retornar números de -9 a 0, com os seguintes significados:
#		 0: tudo ocorreu como o esperado e o automato foi preenchido com sucesso.
#		-1: problema na leitura da primeira linha do arquivo sem a leitura do nome efetuada
#		-2: problema na leitura da primeira linha do arquivo com a leitura do nome efetuada
#		-3: automato inválido pois o conjunto dos estados finais não é subconjunto do conjunto dos estados do autômato.
#		-4: autômato inválido pois o estado inicial não pertence ao conjunto dos estados.
#		-5: linha escrito "Prog" não identificada.
#		-6: identificação do '=' na leitura das funções programa indefinida.
#		-7: leitura das tupla de entrada da função programa indefinida.
#		-8: função programa com estados de entrada ou saída não pertencentes ao conjunto de estados.
#		-9: função programa com letra de entrada não pertencente ao conjunto de símbolos do alfabeto.
def readFromFile(automata, filename):
	file = open(filename, "r")

	line = file.readline()
	line = line.replace('\n', "")
	line = line.replace(' ', "")
	line = line.split('=')

	if len(line) != 2:
		return -1

	auxiliar = getSubset(line[1], '}')
	initialState = getInitialState(line[1])

	if len(auxiliar) != 3:
		return -2
	elif not isSubset(auxiliar[0], auxiliar[2]):
		return -3
	elif initialState not in auxiliar[0]:
		return -4

	automata.setName(line[0])
	automata.setStates(auxiliar[0])
	automata.setAlpha(auxiliar[1])
	automata.setFinalStates(auxiliar[2])
	automata.setInitialState(initialState)

	line = file.readline()
	line = line.replace('\n', "")

	if line != "Prog":
		return -5

	for line in file:
		line = line.replace('\n', "")
		line = line.replace(' ', "")
		line = line.split('=')

		if len(line) != 2:
			return -6

		line[0] = line[0].replace('(', "")
		line[0] = line[0].replace(')', "")
		auxiliar = line[0].split(',')

		if len(auxiliar) != 2:
			return -7
		elif auxiliar[0] not in automata.states or line[1] not in automata.states:
			return -8
		elif auxiliar[1] not in automata.alpha:
			return -9

		automata.insertTransition(auxiliar[0],auxiliar[1],line[1])

	file.close()
	return 0


# writeInFile(DFA, string) -> void
# Objetivo: dado um autômato finito determinístico que foi feito apartir de uma conversão de um AFN para um AFD e um nome de um arquivo,
#  a função cria um arquivo de texto (.txt) com o nome dado e escreve as informações desse autômato no seguinte formato:
# 		<M>=({<q0>,...,<qn>},{<s1>,...,<sn>},<ini>,{ <f0>,...,<fn>})
# 		Prog
# 		(<q0>,<s1>)=<q1>
# 		...
# 		(<qn>,<sn>)=<q0>
#
# 		onde:
# 		<M>: nome dado ao autômato;
# 		<qi>: para 0 ≤ i ≤ n, com n ∈ N e n ≥ 0, representa um estado do autômato;
# 		<si>: para 1 ≤ i ≤ n, com n ∈ N e n ≥ 1, representa um símbolo do alfabeto da
# 			linguagem reconhecida pelo autômato;
# 		<ini>: indica o estado inicial do autômato, sendo que ini é um estado do autômato;
# 		<fi>: para 0 ≤ i ≤ n, com n ∈ N e n ≥ 0, representa um estado final do autômato,
# 			sendo que fi é um estado do autômato;
# 		(<qi>, <si>)=<qj>: descreve a função programa aplicada a um estado qi e um
# 			símbolo de entrada si que leva a computação a um estado qj.
def writeInFile(DFA, filename):
	file = open(filename, "w")

	file.write(DFA.name + '=' + '({')

	count = 0
	for state in DFA.states:
		count += 1
		string = str(state).replace(' ', "").replace(',', "").replace('[', '<').replace(']', '>').replace("'", "")
		file.write(string)
		if count < len(DFA.states):
			file.write(',')
	file.write('},{')
	count = 0
	for letter in DFA.alpha:
		count += 1
		file.write(letter)
		if count < len(DFA.alpha):
			file.write(',')
	file.write('},')
	file.write(str(DFA.initialState).replace(' ', "").replace(',', "").replace('[', '<').replace(']', '>').replace("'", ""))
	file.write(',{')
	count = 0
	for state in DFA.finalStates:
		count += 1
		string = str(state).replace(' ', "").replace(',', "").replace('[', '<').replace(']', '>').replace("'", "")
		file.write(string)
		if count < len(DFA.finalStates):
			file.write(',')
	file.write('})\n')
	file.write('Prog\n')
	for transition in DFA.program:
		file.write('(' + str(transition[0]).replace(' ', "").replace(',', "").replace('[', '<').replace(']', '>').replace("'", "") + ',' + transition[1] + ')=' + str(transition[2]).replace(' ', "").replace(',', "").replace('[', '<').replace(']', '>').replace("'", "") + '\n')




# --------------------------------------- Main ---------------------------------------
# Entradas: autômato não-determinístico (arquivo de entrada no formato ja citado e com nome de "automato.txt") e lista de palavra para teste (dada em sequência).
# Saída: autômato determinístico equivalentet ao dado na entrada (arquivo de saída com o mesmo formato do de entrada e com nome de "automatosaida.txt") e lista de booleanos referentes as palavras de testes (também dada em sequência).
# Observação: Para cada palavra dada na parte do teste de palavras, se devolver true, significa que a palavra pertence a ACEITA(Md) tal que Md é o autômato determinístico equivalente
#			ao não-determinístico dado pelo arquivo de entrada. Já, se devolver false, significa que a palavra não pertence a ACEITA(Md).
# 			  As palavras dadas para teste do automato Md são informadas pelo usuário pelo teclado.
#			  O resultado da pertinência da palavra na linguagem é informada no visor para cada palavra individualmente.
automato = automata()
aux = readFromFile(automato, "automato.txt")
if aux != 0:
	print("Erro " + str(aux) + " na leitura do arquivo.")
else:
	DFAversion = automato.convertToDFA()
	writeInFile(DFAversion, "automatosaida.txt")
	print("Teste de palavras:")
	while int(input("0-Sair\n1-Testar outra palavra\n")) != 0:
		word = input("Word: ")
		print(DFAversion.checkWord(word))



# ░░░░░▄▄▀▀▀▀▀▀▀▀▀▄▄░░░░░
# ░░░░█░░░░░░░░░░░░░█░░░░
# ░░░█░░░░░░░░░░▄▄▄░░█░░░
# ░░░█░░▄▄▄░░▄░░███░░█░░░
# ░░░▄█░▄░░░▀▀▀░░░▄░█▄░░░
# ░░░█░░▀█▀█▀█▀█▀█▀░░█░░░
# ░░░▄██▄▄▀▀▀▀▀▀▀▄▄██▄░░░
# ░▄█░█▀▀█▀▀▀█▀▀▀█▀▀█░█▄░
