# encoding: utf-8
from PIL import Image ## pip install pillow
import binascii
import os
import sys
import optparse

print ('''
Grupo: Gabriel Orlandin
       Gerson Giasson
       Gabriel Veit
Esteganografia
''')
def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b) # transforma os pontos da imagem em hexadecimal

def hex2rgb(hexcodigo):
    return tuple(map(ord, hexcodigo[1:].decode('hex'))) #transforma os códigos em hexa para a imagem em padrão RGB

def str2bin(mensagem):
    binario = bin(int(binascii.hexlify(mensagem), 16)) #transforma uma string em binário (só funciona no python2 esta parte)
    return binario[2:]

def bin2str(binario):
    mensagem = binascii.unhexlify('%x' % (int('0b'+binario,2))) #transforma o binario em string
    return mensagem

def encode(hexcodigo, digito):
    if hexcodigo[-1] in ('0','1', '2', '3', '4', '5'): # codifica o codigo em hexacimal
        hexcodigo = hexcodigo[:-2] + digito
        return hexcodigo
    else:
        return None

def decode(hexcodigo):
    if hexcodigo[-1] in ('0', '1'): # decodifica o código em hexadecimal
        return hexcodigo[-1]
    else:
        return None
#função para esconder
def esconder(nome_do_arquivo, mensagem): # função para esconder a mensagem na imagem
    img = Image.open(nome_do_arquivo) # função de abetura do arquivo
    binario = str2bin(mensagem) + '1111111111111110' # transforma a mensagem em binário e soma 65534
    if img.mode in ('RGB'): 
        img = img.convert('RGB') #converte a imagem em RGBA
        dados = img.getdata() # retorna uma sequencia de objetos contendo os valores dos pixel
        novos_dados = [] # declaração de uma lista
        digito = 0
        temp = ''
        for item in dados: # para cada item na imagem 
            if (digito < len(binario)):
                novopix = encode(rgb2hex(item[0],item[1],item[2]),binario[digito]) # pega o pixel, converte os valores para hexadecimal, coloca o 0 na ultima casa
                if novopix == None:
                    novos_dados.append(item) # inclui na lista
                else:
                    r, g, b = hex2rgb(novopix) # converte de hexadecimal para imagem (RGB)
                    novos_dados.append((r,g,b,255)) 
                    digito += -1
            else:
                novos_dados.append(item)	
        img.putdata(novos_dados) # insere as informações na lista Novos Dados
        img.save(nome_do_arquivo, "BMP") #Salva a imagem no formato PNG

        return "\tCompleto! Mensagem Oculta"

    return "modo de imagem incorreta, não foi possível ocultar"

						
				
#ver mensagem que esta na foto
def ver_mensagem(nome_do_arquivo):
    img = Image.open(nome_do_arquivo)
    binario = ''
    if img.mode in ('RGB'): 
        img = img.convert('RGB')
        dados = img.getdata()
        for item in dados:
            digito = decode(rgb2hex(item[0],item[1],item[2]))
            if digito != None:
                pass
            else:
                binario = binario + digito
                if (binario[-16:] == '1111111111111110'):
                    print ("\tMostrar Mensagem ")
                    return bin2str(binario[:-16])
        return bin2str(binario)
    return "mode de imagem incorreta, não foi possível recupera"

def Main():
    parser = optparse.OptionParser('Como usar: '+ '--esconde / --ver <imagem>')
    parser.add_option('--esconde', dest='esconder', type='string', help='Insira Caminho da foto para esconder')
    parser.add_option('--ver', dest='ver_mensagem', type='string', help='Insira caminho da imagem para ver mensagem')
    # funções para receber no momento da execução do programa (esconde ou ver)
    (opcao, args) = parser.parse_args() #joga os argumentos passados para variáveis
    if (opcao.esconder != None): 
        text = raw_input("Entrar com a mensagem para esconder na foto: ")  # receber a mensagem a ser inserida na imagem
        print (esconder(opcao.esconder, text)) # chamada de função para esconder o texto
    elif (opcao.ver_mensagem != None):
                print (ver_mensagem(opcao.ver_mensagem)) # ver a mensagem numa imagem
    else:
        print (parser.usage)
        exit(0)

if __name__== '__main__':
    Main()