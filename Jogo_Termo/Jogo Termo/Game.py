import random
import unicodedata

"""
    1.(cria_lista_palavras) Recebe uma string com o nome do arquivo e devolve uma lista contendo as palavras do arquivo.
"""

def cria_lista_palavras(nome_arquivo):
    # Abre o arquivo de texto com as palavras e converte ele para UTF-8.
    with open(nome_arquivo, 'r',encoding='utf-8' ) as file:
        # Retorna lista com as palavras sem espaço e transforma os caracteres em minusculo. 
        return [linha.strip().lower() for linha in file]

"""
    2.(checa_tentativa) Recebe a palavra secreta e o chute do usuário e devolve uma lista 'feedback' de 5 elementos
    para indicar acertos e erros. A lista 'feedback' deve conter o valor 1 (verde) se a letra
    correspondente em chute ocorre na mesma posição em palavra (letra certa no lugar certo),
    deve conter 2 se a letra em chute ocorre em outra posição em palavra (letra certa no lugar errado),
    e deve conter 0 caso contrário.
"""

def checa_tentativa(palavra, chute):
    feedback = [0] * 5
    palavraVerificada = comparar_letras(palavra)
    chuteVerificado = comparar_letras(chute)
    
    letras_disponiveis = list(palavraVerificada)
    
    for i in range(5):
        if chuteVerificado[i] == palavraVerificada[i]:
            feedback[i] = 1
            letras_disponiveis[i] = None
    
    for i in range(5):
        if feedback[i] == 0 and chuteVerificado[i] in letras_disponiveis:
            feedback[i] = 2
            letras_disponiveis[letras_disponiveis.index(chuteVerificado[i])] = None
    
    return feedback

"""
    3.(imprime_resultado) Recebe a lista de tentativas e imprime as tentativas, usando * para verde, + para amarelo
    e _ para letras que não aparecem na palavra sorteada.
    A lista de tentativas tem formato [[chute1, feedback1], [chute2, feedback2], ..., [chuten, feedbackn]].
"""

def imprime_resultado(lista_tentativas):
    # Inicia tupla com simbolos utilizados 
    simbolos = {1: '*', 2: '+', 0: '_'}
    # Percorre lista de tentativas.
    for chute, feedback in lista_tentativas:
        # Percorre a tupla 'simbolos' e atribui o valor a váriavel feedback
        resultado = ''.join(simbolos[f] for f in feedback)
        # Printa chute e resultado.
        print(f"{chute}")
        print(f"{resultado}")

"""
    4.(atualiza_teclado) Modifica teclado para que as letras marcadas como inexistentes no chute sejam substituídas por espaços.
"""

def atualiza_teclado(chute, feedback, teclado):
    chuteVerificado = comparar_letras(chute)
    for i in range(5):
        if feedback[i] == 0:
            tecla = chuteVerificado[i]
            for linha in range(len(teclado)):
                teclado[linha] = teclado[linha].replace(tecla, ' ')
"""
    5.(comparar_letras) Comparar, remover acentos e converter letras para minúsculas para verificação.
"""

def comparar_letras(texto):
    # Verifica se palavra recebida possui 'ç' e substitui por 'c'.
    texto = texto.replace('ç', 'c').replace('Ç', 'C')
    # Retorna a palavra recebida na função sem acentos.
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').lower()


"""
    6.(obter_idioma) Verifica se o usuário digitou apenas I para Ingles ou P para Portugues se nao,
    pede para ele digitar corratamente para o programa continuar.
"""

def obter_idioma():
    # Laço de repetição para verificar a resposta do usuário entre P e I, se for uma resposta inválida, refaz a pergunta.
    while True:
        idioma = input("Qual o idioma (I para inglês ou P para português)? ").strip().upper()
        if idioma in {'I', 'P'}:
            return idioma
        print("Entrada inválida! Por favor, digite 'I' para inglês ou 'P' para português.")
"""
    7.(Termo) Programa Principal
"""

def main():
    # Chama a função responsavel por perguntar qual o idioma o jogador prefere jogar (P =  Porgugues / I =  Inglês)
    idioma = obter_idioma()

    # Carrega o arquivo de texto contendo as palavras de cada lingua
    nome_arquivo = 'words.txt' if idioma == 'I' else 'palavras.txt'
    
    # Recebe as palavras existentes no arquivo txt e transfere para uma lista 'palavras_normalizadas' sem acentos e espaços.
    palavras = cria_lista_palavras(nome_arquivo)
    palavras_normalizadas = [comparar_letras(palavra) for palavra in palavras]
    
    # Sortear uma palavra da lista
    palavra_sorteada = random.choice(palavras)
    palavra_sorteada_normalizada = comparar_letras(palavra_sorteada)
    
    # Teclado inicial
    teclado = ["q w e r t y u i o p", "a s d f g h j k l ", "z x c v b n m"]
    
    # Lista de tentativas
    lista_tentativas = []
    
    # Repetir no máximo seis vezes a tarefa de solicitar uma tentativa do usuário
    for tentativa in range(6):
        print("---------------------------------------------------------------")
        print("\n".join(teclado))
        print("---------------------------------------------------------------")
        imprime_resultado(lista_tentativas)
        
        chute = input("Digite a palavra: ").strip().lower()
        chute_normalizado = comparar_letras(chute)
        
        # Verifica se a palavra recebida 'chute' tem tamanho diferente de 5 ou se a palavra 'chute' não existe na lista 'palavras_normalizadas' e devolve um 'erro'.
        if len(chute) != 5 or chute_normalizado not in palavras_normalizadas:
            print("Palavra inválida!")
            continue
        
        # Atribui a feedback a 'palavra secreta' e o 'chute'.
        feedback = checa_tentativa(palavra_sorteada_normalizada, chute_normalizado)
        # inicia uma tupla com os valores [chute, feedback].
        lista_tentativas.append([chute, feedback])
        
        # Chama a função responsável por atualizar e retirar as letras inexistentes na palavra secreta do teclado.
        atualiza_teclado(chute, feedback, teclado)
        
        # Verifica se a palavra 'chute' é igual a palavra secreta, se sim, imprime as tentativas anteriores do usuário e finaliza o jogo como vitoria.
        if chute_normalizado == palavra_sorteada_normalizada:
            imprime_resultado(lista_tentativas)
            print("PARABÉNS!")
            break
    # Caso atingir o número maximo de tentavivas e finalizar o 'for' Imprime na tela a lista de tentativas do usuário e finaliza o jogo como derrota.    
    else:
        imprime_resultado(lista_tentativas)
        print(f"Você perdeu. A palavra era {palavra_sorteada}.")

# Inicia o jogo
if __name__ == "__main__":
    main()
