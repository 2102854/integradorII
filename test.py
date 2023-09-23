
import re 
import random
import string

class test():
    def generate_password():        
        number_char_generator = random.choice([8, 9, 10, 11, 12])
        n = number_char_generator - 4
        
        # Garante pelo menos um dos tipos de critérios para senha
        l = random.choice(string.ascii_lowercase)
        u = random.choice(string.ascii_uppercase)
        n = random.choice(string.digits)
        p = random.choice(string.punctuation)

        # Gera Caracteres Aleatórios
        characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        random_characters = ''.join(random.choice(characters) for i in range(n))
        random_characters = random_characters.join(l).join(u).join(n).join(p)
        password = ''.join(random.choice(random_characters) for i in range(number_char_generator))
        
        print("Random password is:", password)
        return password