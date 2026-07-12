import random
import time
import os

# 1. Get the absolute path of the directory where THIS file (gametools.py) lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class GT:
    def name_gen(firstname='', lastname='', gender='none'):
        if gender == 'none':
            gender = random.choice(['male', 'female'])
            
        # 2. Point to the files dynamically using BASE_DIR
        if gender == 'male':
            file_path = os.path.join(BASE_DIR, 'male_f_names.txt')
        elif gender == 'female':
            file_path = os.path.join(BASE_DIR, 'female_f_names.txt')
            
        file = open(file_path, 'r')
        raw_firstnames = file.readlines()
        file.close()
        
        # Clean the newlines properly into a fresh list
        firstnames = [name.strip('\n') for name in raw_firstnames]
        
        # 3. Do the same for the last names file
        l_names_path = os.path.join(BASE_DIR, 'l_names.txt')
        file = open(l_names_path, 'r')            
        raw_lastnames = file.readlines()
        file.close()
        
        lastnames = [name.strip('\n') for name in raw_lastnames]
        
        if firstname == '':
            firstname = random.choice(firstnames)
        if lastname == '':
            lastname = random.choice(lastnames)
        
        return [firstname, lastname]
        
    def stock_name_generator():
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        formats = ['l&l', 'abc', 'abc123', 'abc12', 'abcd']
        code = 'code not found'
        chosen_format = random.choice(formats)
        if chosen_format == 'l&l':
            code = random.choice(letters)+'&'+random.choice(letters)
        elif chosen_format == 'abc':
            code = random.choice(letters)+random.choice(letters)+random.choice(letters)
        elif chosen_format == 'abc123':
            code = random.choice(letters)+random.choice(letters)+random.choice(letters)+f"{random.randint(100,999)}"
        elif chosen_format == 'abc12':
            code = random.choice(letters)+random.choice(letters)+random.choice(letters)+f"{random.randint(10,99)}"
        elif chosen_format == 'abcd':
            code = random.choice(letters)+random.choice(letters)+random.choice(letters)+random.choice(letters)
        return code