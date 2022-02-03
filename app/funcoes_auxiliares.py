
# Limita a quantidade de caracteres de uma string em 200 caracteres
def truncar_texto(texto):

    # Se a string possuir mais de 200 caracteres
    if len(texto) > 200:
        
        # Fatie os primeiros 200 caracteres da string e adicione "..." no final
        texto = texto[0:200] + '...'

    # Retorne a string truncado
    return texto
