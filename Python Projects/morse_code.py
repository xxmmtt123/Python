from morse_code_data import morse_code_rules

# Using code(text) makes the function more reliable and reusable by passing the input directly,
# instead of relying on a global variable.
def code(text):
    morse_list = []

    for t in text:
        text_lower = t.lower()
        if text_lower in morse_code_rules:
            morse_list.append(morse_code_rules[text_lower])

    code_result = ' '.join(morse_list)
    print(code_result)

def decode(text):
    morse_to_letter = {v: k for k, v in morse_code_rules.items()}

    morse_list = text.split(" ")
    text_list = []
    for t in morse_list:
        if t in morse_to_letter:
            text_list.append(morse_to_letter[t])

    code_result = ' '.join(text_list).capitalize()
    print(code_result)


continue_code = True

while continue_code:
    to_do = input('Do want to code or decode? '
                  'Type "c" to code, type "d" to decode, and type "q" to quit. \n')

    if to_do == 'c':
        text = input('The text you would like to convert:\n')
        code(text)

    elif to_do == 'd':
        text = input('The text you would like to convert:\n')
        decode(text)

    elif to_do == 'q':
        continue_code = False

    else:
        print('Incorrect input. Please retype')
        to_do

