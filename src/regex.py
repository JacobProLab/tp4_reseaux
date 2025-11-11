import re
from pprint import pprint

patterns = [
    r"World",                   
    r".",                       
    r"^.?$",                    
    r"\d{3}",                   
    r"[a-zA-Z0-9]{3-12}",       
    r"[TWHQ]ello",              
    r"foo|bar|ello",            
    r"^(Hello)",                
    r"!!![0-9]{3}$",            
    r"^H.*[0-9]{3}$"            
]

# patterns_LUT = {index: pattern for index, pattern in zip(range(len(patterns)), patterns)}

patterns_LUT = {
    '0': 'World',                   # verifie si `text` contient le mot `World`
    '1': '.',                       # verifie si `text` contient un `caractere unique`
    '2': '^.?$',                    # ^.?$ = (START)(caractere unique)(zero ou un)(END)
    '3': '\\d{3}',                  # \d{3} = exactement 3 chiffres
    '4': '[a-zA-Z0-9]{3-12}',       # [alphanumerique]{between 3 and 12} = `text` contient entre 3 et 12 caracteres alphanumeriques
    '5': '[TWHQ]ello',              # [...]ello = `text` contient [T, W, H, Q] + 'ello'
    '6': 'foo|bar|ello',            # `text` contient foo, bar, ou ello
    '7': '^(Hello)',                # `text` commence par Hello
    '8': '!!![0-9]{3}$',            # `text` se termine par !!! suivi de 3 chiffres (e.g. Salut, comment vas tu??!!!234)
    '9': '^H.*[0-9]{3}$'            # `text` commence par un H et se termine par 3 chiffres
 }


text: str = """
    Hello World!

    Today was a calm day.  
    I woke up, stretched, and stared at the ceiling for a bit.

    Then I remembered: I had 123 unread messages!  
    So I logged in as Username123 to check them.

    Tello, my cat, jumped on the desk and stared at me like I owed him breakfast.  
    "foo," I said, pretending to cast a spell to make him move — it didn’t work.

    At 10:00, I wrote "!!!123" on my whiteboard as a secret code.  
    It looked mysterious, but it really meant nothing.

    Finally, before sleeping, I whispered:  
    "Hello something 999"
"""

text = "Salut?"

for pattern in patterns:
    match = re.search(pattern, text)
    print(match)
    


