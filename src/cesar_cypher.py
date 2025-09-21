def criptografa(msg, descolamento, tam_alfabeto):
    msg_cript = ""
    for char in msg:
        # Necessário converter o char para ASCII
        codigo = (ord(char) + descolamento) % tam_alfabeto
        msg_cript += chr(codigo)
    return msg_cript

def descriptografa(msg_cript, descolamento, tam_alfabeto):
    msg_decript = ""
    for char in msg_cript:
        # Necessário converter o char para ASCII
        codigo = (ord(char) - descolamento) % tam_alfabeto
        msg_decript += chr(codigo)
    return msg_decript

if __name__ == "__main__":
    ##### PARÂMETROS #####
    deslocamento = 5
    tam_alfabeto = 256
    
    ##### MENSAGENS #####
    msg_to_cript = "Burning Love"
    
    ##### RESULTADOS #####
    
    # Criptografia 
    print(f"Mensagem original:\n{msg_to_cript}\n")
    msg_criptografada = criptografa(msg_to_cript, deslocamento, tam_alfabeto)
    print(f"Mensagem criptografada:\n{msg_criptografada}\n")
    
    # Descriptografia 
    msg_descriptografada = descriptografa(msg_criptografada, deslocamento, tam_alfabeto)
    print(f"Mensagem descriptografada:\n{msg_descriptografada}")