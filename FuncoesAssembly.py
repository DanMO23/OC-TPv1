import sys

#Dicionário para armazenamento dos rótulos de instruções
Rotulos = {}

Opcode = {
    'R':"0110011",
    'I':"0000011",
    'S':"0100011",
    'SB':"1100011"
    }

func3 = {
    'add':"000",
    'xor':"100",
    'sll':"001",
    'addi': "000",
    'lw': "010",
    'sw':"010",
    'bne':"001"
}

func7 ={
    'add':"0000000",
    'xor':"0000000",
    'sll':"0000000"

}

#Função usada quando há rotulos no programa
#Definido 2000 como endereço inicial do programa incrementando em 4 a cada linha de instrução
def AdicionarRotulo(Var_rotulo, numInstrucao):
    
    label = Var_rotulo.split()[0]
    if(label[len(label)-1] ==':'):
        label = label[:-1]
    Rotulos[label] = 2000 + (numInstrucao * 4)

def funcoesSemParametro(arq_inst):
    for i in range(0, len(arq_inst)):
        if (arq_inst[i][0] == "\n" or arq_inst[i][0:1] == " \n"):
            continue
        else:
            assemblyBin = DefinirInstrucao(arq_inst, i)
        if(assemblyBin != 0):
            print(assemblyBin)

def funcoesComParametro(arq_inst, saida):
    Rotulos = []
    for i in range(0, len(arq_inst)):
        if (arq_inst[i][0] == "\n" or arq_inst[i][0:1] == " \n"):
            continue
        else:
            if (DefinirInstrucao(arq_inst, i) == type(list)):
                Rotulos += DefinirInstrucao(arq_inst, i)
            else:
                assemblyBin = DefinirInstrucao(arq_inst, i)

            if (i == 0):
                arqsaida = open(saida, "w")
            else:
                arqsaida = open(saida, "a")
            if (i == len(arq_inst)):
                if(assemblyBin != 0):
                    arqsaida.write(assemblyBin)
            else:
                if(assemblyBin != 0):
                    arqsaida.write(str(assemblyBin) + "\n")
            arqsaida.close

def DefinirInstrucao(arq_inst, i):
    
    if (arq_inst[i][0:4] == "bne "):
        assemblyBin = OpBne(arq_inst[i])
    elif (arq_inst[i][0:3] == "sw "):
        assemblyBin = OpSw(arq_inst[i])
    elif (arq_inst[i][0:4] == "addi"):
        assemblyBin = OpAddi(arq_inst[i])
    elif (arq_inst[i][0:3] == "lw "):
        assemblyBin = OpLw(arq_inst[i])
    elif (arq_inst[i][0:4] == "sll "):
        assemblyBin = OpSll(arq_inst[i])
    elif (arq_inst[i][0:4] == "add "):
        assemblyBin = OpAdd(arq_inst[i])
    elif (arq_inst[i][0:4] == "xor "):
        assemblyBin = OpXor(arq_inst[i])

    #Funcao usada quando há rotulos
    elif(':' in arq_inst[i]):
        AdicionarRotulo(arq_inst[i], i)
        return 0

    else:
        assemblyBin = "Instrução não localizada."

    return assemblyBin

def DefinirTamanho(arq_inst):
    tam = arq_inst.find(" ") 
    tam = int(tam) +2
    

    return tam 
        


def FormatR(arq_inst, func3, func7, tam_int):
    j, rd, rs1, rs2 = tam_int, '', '', ''
    #j = tamanho da instrução + 2
    while (arq_inst[j] != ','):
        rd = rd + arq_inst[j]
        j += 1
    j += 3
    while (arq_inst[j] != ','):
        rs1 = rs1 + arq_inst[j]
        j += 1
    j += 3
    while (j != len(arq_inst)):
        rs2 = rs2 + arq_inst[j]
        j += 1
    rd = int(rd)
    rd = "{0:05b}".format(rd)
    rs1 = int(rs1)
    rs1 = "{0:05b}".format(rs1)
    rs2 = int(rs2)
    rs2 = "{0:05b}".format(rs2)

    
    assemblyBin = func7 + rs2 + rs1 + func3 + rd + Opcode["R"]
    
    return assemblyBin

def FormatI(arq_inst, func3,  tam_int):
    j, rd, rs1, immediate = tam_int, '', '', ''
    #j = tamanho da instrução + 2

    #caso seja addi
    if(arq_inst[0:(tam_int-2)] == "addi"):
        negativo = False
        while (arq_inst[j] != ','):
            rd = rd + arq_inst[j]
            j += 1
        j += 3
        while (arq_inst[j] != ','):
            rs1 = rs1 + arq_inst[j]
            j += 1
        j += 2
        if (arq_inst[j] == '-'):
            negativo = True
            j += 1
        while (j != len(arq_inst)):
            immediate = immediate + arq_inst[j]
            j += 1
        rd = int(rd)
        rd = "{0:05b}".format(rd)
        rs1 = int(rs1)
        rs1 = "{0:05b}".format(rs1)
        immediate = int(immediate)
        if (negativo and immediate > 2048):
            assemblyBin = "Valor do imediato inferior a -2048"
            return assemblyBin
        elif (immediate > 2047):
            assemblyBin = "Valor do imediato superior a 2047"
            return assemblyBin
        if (negativo):
            immediate = (pow(2, 12) - immediate)
        immediate = "{0:012b}".format(immediate)
        assemblyBin = immediate + rs1 + func3 + rd + Opcode["I"]
        return assemblyBin

    #caso nao seja addi
    while (arq_inst[j] != ','):
        rd = rd + arq_inst[j]
        j += 1
    j += 2
    while (arq_inst[j] != '('):
        immediate = immediate + arq_inst[j]
        j += 1
    j += 2
    while (arq_inst[j] != ')'):
        rs1 = rs1 + arq_inst[j]
        j += 1
    rd = int(rd)
    rd = "{0:05b}".format(rd)
    rs1 = int(rs1)
    rs1 = "{0:05b}".format(rs1)
    immediate = int(immediate)
    immediate = "{0:012b}".format(immediate)
    assemblyBin = immediate + rs1 + func3 + rd + Opcode["I"]
    return assemblyBin
    
def FormatS(arq_inst,  func3, tam_int):
    
    j, rs2, rs1, immediate = tam_int, '', '', ''
    while (arq_inst[j] != ','):
        rs2 = rs2 + arq_inst[j]
        j += 1
    j += 2
    while (arq_inst[j] != '('):
        immediate = immediate + arq_inst[j]
        j += 1
    j += 2
    while (arq_inst[j] != ')'):
        rs1 = rs1 + arq_inst[j]
        j += 1
    rs2 = int(rs2)
    rs2 = "{0:05b}".format(rs2)
    rs1 = int(rs1)
    rs1 = "{0:05b}".format(rs1)
    immediate = int(immediate)
    immediate = "{0:012b}".format(immediate)
    assemblyBin = immediate[0:7] + rs2 + rs1 + func3 + immediate[7:12] + Opcode["S"]
    return assemblyBin


def FormatSB(arq_inst,  func3, tam_int):
    
    j, rs2, rs1, immediate = tam_int, '', '', ''

    
    while (arq_inst[j] != ','):
        rs1 = rs1 + arq_inst[j]
        j += 1
    j += 3
    while (arq_inst[j] != ','):
        rs2 = rs2 + arq_inst[j]
        j += 1
    j += 2
    if (arq_inst[j:len(arq_inst)] in Rotulos):
        immediate = Rotulos[arq_inst[j:len(arq_inst)]]
    else:
        while (j != len(arq_inst)):
            immediate = immediate + arq_inst[j]
            j += 1
    rs2 = int(rs2)
    rs2 = "{0:05b}".format(rs2)
    rs1 = int(rs1)
    rs1 = "{0:05b}".format(rs1)
    immediate = int(immediate)
    immediate = "{0:012b}".format(immediate)
    assemblyBin = immediate[0:7] + rs2 + rs1 + func3 + immediate[7:12] + Opcode["SB"]
    return assemblyBin


#Bne - Instrução no formato SB
def OpBne(arq_inst):
    
    assemblyBin = FormatSB(arq_inst, func3["bne"], DefinirTamanho(arq_inst))
    return assemblyBin

#Sw - Instrução no formato S
def OpSw(arq_inst):
    
    assemblyBin = FormatS(arq_inst,func3["sw"], DefinirTamanho(arq_inst))
    return assemblyBin

#Addi - Instrução no formato I
def OpAddi(arq_inst):
    assemblyBin = FormatI(arq_inst, func3["addi"], DefinirTamanho(arq_inst))
    return assemblyBin

#Lw - Instrução no formato I
def OpLw(arq_inst):
    assemblyBin = FormatI(arq_inst, func3["lw"], DefinirTamanho(arq_inst))
    return assemblyBin

#Sll - Instrução no formato R
def OpSll(arq_inst):
    
    assemblyBin = FormatR(arq_inst, func3["sll"], func7["sll"], DefinirTamanho(arq_inst))
    return assemblyBin

#Add - Instrução no formato R
def OpAdd(arq_inst):
   
    assemblyBin = FormatR(arq_inst, func3["add"], func7["add"], DefinirTamanho(arq_inst))
    return assemblyBin

#Xor - Instrução no formato R
def OpXor(arq_inst):
    
    assemblyBin = FormatR(arq_inst, func3["xor"], func7["xor"], DefinirTamanho(arq_inst))
    return assemblyBin
