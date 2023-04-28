
#Importaas funções criadas no arquivo FunçõesAssembly
import FuncoesAssembly

#Importaas funções criadas para identificar os argumentos passados por linha de comando
import sys

#Se o numero de argumentos for menor do que 2, o arquivo de entrada nao foi passado
if (len(sys.argv) < 2):
    print("Arquivo não informado por linha de comando")
    sys.exit

#Se o numero de argumentos for menor do que 4, o arquivo de saida nao foi passado
elif (len(sys.argv) < 4 and len(sys.argv) >= 2):
    texto = open(sys.argv[1], "r")
    arq_inst = texto.readlines()
    FuncoesAssembly.funcoesSemParametro(arq_inst)

#Se o numero de argumentos for igual a 4, o arquivo de saida foi passado
elif(len(sys.argv) == 4):
    texto = open(sys.argv[1], "r")
    arq_inst = texto.readlines()
    
    saida = sys.argv[len(sys.argv)-1] + ".bin"
    FuncoesAssembly.funcoesComParametro(arq_inst, saida)
