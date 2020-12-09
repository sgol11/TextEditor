"""
Редактирование текста
Голикова Софья, МГТУ им.Баумана, ИУ7-15Б
2020
"""

# массив строк (текст)
text = [
    'У лукоморья дуб зелёный;',
    'Златая цепь на дубе том:',
    'И днём и ночью кот учёный',
    'Всё ходит по цепи кругом;',
    'Идёт направо — песнь заводит,',
    'Налево — сказку говорит.',
    'Там чудеса: там леший бродит,',
    'Русалка на ветвях сидит...',
    '',
    'Александр Сергеевич Пушкин родился в 1598/2+(500*2) году.',
    'Он провел (13%7) лет в Царскосельском лицее.'
]

sign_priority = {'(': 0, ')': 0,
                 '^': 1,
                 '*': 2, '/': 2, '%': 2, '//': 2,
                 '+': 3, '-': 3}


def max_len(current_text):

    maximum = 0
    for ln in current_text:
        ln = ln.strip()
        if len(ln) > maximum:
            maximum = len(ln)
    return maximum


def calculator(a, b, op):

    if op == '+': return a + b
    elif op == '-': return a - b
    elif op == '*': return a * b
    elif op == '/': return a / b
    elif op == '%': return a % b
    elif op == '//': return a // b
    elif op == '^': return a ** b
    else: return None


def expr_result(expression):

    tokens = []
    # добавление в tokens чисел и арифметических операций из строки выражения
    i = 0
    while i < len(expression):
        if expression[i] == '/' and i != len(expression) - 1 \
                and expression[i+1] == '/':
            tokens.append(expression[i] + expression[i+1])
            i += 1

        elif expression[i].isdigit() and i != 0 \
                and expression[i-1].isdigit():
            tokens[-1] += expression[i]

        elif expression[i].isdigit():
            tokens.append(expression[i])

        elif expression[i] in sign_priority and i != 0 \
                and expression[i-1] not in sign_priority:
            tokens.append(expression[i])

        elif expression[i] == '(' and (i == 0 or
                expression[i-1] in sign_priority):
            tokens.append(expression[i])

        else:
            return None
        i += 1

    output = []
    stack = []
    left_bracket = False
    
    for t in tokens:

        if t.isdigit():
            output.append(int(t))
            
        elif t == '(':
            stack.append(t)
            left_bracket = True
        
        elif t == ')':
            new_expr = ''
            new_expr_signs = []
            new_expr_nums = []

            sign = stack.pop()
            while stack and sign != '(':
                new_expr_signs.append(sign)
                sign = stack.pop()
            if not stack and sign != '(':
                return None

            nums_amt = len(new_expr_signs) + 1
            
            for i in range(nums_amt):
                new_expr_nums.append(str(output.pop()))

            new_expr_nums = new_expr_nums[::-1]
            new_expr_signs = new_expr_signs[::-1]

            i = -1
            for i in range(len(new_expr_signs)):
                new_expr += new_expr_nums[i] + new_expr_signs[i]
            new_expr += new_expr_nums[i+1]

            current_result = expr_result(new_expr)

            output.append(current_result)
            left_bracket = False
                    
        elif t in sign_priority:

            if not left_bracket:
                t_pr = sign_priority[t]

                while stack and t_pr >= sign_priority[stack[-1]]:
                    operator = stack.pop()
                    b = output.pop()
                    a = output.pop()
                    output.append(calculator(a, b, operator))

            stack.append(t)

    while stack:
        operator = stack.pop()
        if operator == '(':
            return None
        b = output.pop()
        a = output.pop()
        output.append(calculator(a, b, operator))

    result = output.pop()
    try:
        result = int(result)
        return result
    except ValueError:
        return result


print('Исходный текст: \n')
print(*text, sep='\n')

choice = None

while choice != '0':
    print(
        '''
Меню:

1 - Выравнивание текста по левому краю
2 - Выравнивание текста по правому краю
3 - Выравнивание текста по ширине
4 - Удаление заданного слова
5 - Замена одного слова другим во всем тексте
6 - Вычисление арифметических выражений в тексте
7 - Строка с максимальным количеством слов,
    начинающихся на заданную букву
0 - Выход
        ''')

    choice = input('Выбор: ')
    print()

    if choice == '0':
        print('Выход')
        break

    elif choice == '1':
        print('Выравнивание по левому краю:\n')

        if not len(text):
            print('')
        else:
            for i, line in enumerate(text):
                line = line.strip()
                if not len(line):
                    print('')
                else:
                    # удаление лишних пробелов между словами
                    changed_text = line[0]
                    for j in range(1, len(line)):
                        if line[j] == ' ' and line[j-1] == ' ':
                            continue
                        else:
                            changed_text += line[j]
                    line = changed_text
            
                    text[i] = line.ljust(max_len(text))
                    print(text[i])

    elif choice == '2':
        print('Выравнивание по правому краю:\n')

        if not len(text):
            print('')
        else:
            for i, line in enumerate(text):
                line = line.strip()
                if not len(line):
                    print('')
                else:
                    # удаление лишних пробелов между словами
                    changed_text = line[0]
                    for j in range(1, len(line)):
                        if line[j] == ' ' and line[j - 1] == ' ':
                            continue
                        else:
                            changed_text += line[j]
                    line = changed_text

                    text[i] = line.rjust(max_len(text))
                    print(text[i])
                  
    elif choice == '3':
        print('Выравнивание по ширине:\n')

        for i in range(len(text)):
            text[i] = text[i].strip()
            length = len(text[i])

            # список индексов пробелов между словами
            spaces = []
            for j in range(1, length):
                if text[i][j] == ' ' and text[i][j-1] != ' ':
                    spaces.append(j)
                    
            if not spaces:
                # если в строке одно слово, выравнивание по левому краю
                text[i] = text[i].ljust(max_len(text))
            else:
                # количество добавляемых пробелов
                added_spaces = max_len(text) - length
                for j in range(added_spaces):
                    idx = spaces[j % len(spaces)]
                    text[i] = text[i][:idx] + ' ' + text[i][idx:]
                    
                    for k in range(j % len(spaces), len(spaces)):
                        spaces[k] += 1
                    
            print(text[i])
            
    elif choice == '4' or choice == '5':
        
        word = input('Введите слово для {}: '.format('удаления'
                    if choice == '4' else 'замены'))
        
        new_word = ''
        if choice == '5':
            new_word = input('Введите слово, на которое необходимо заменить: ')

        text = [line.replace(word.strip(), new_word.strip()) for line in text]
        
        print('\nПолученный текст: \n')
        print(*text, sep='\n')

    elif choice == '6':
        # арифметические выражения с ответами в виде словаря
        all_expr = {}
        # текущее арифметическое выражение
        math_expr = ''
        
        for i, line in enumerate(text):
            changed_line = ''
            start = False
            
            for symbol in line:
                
                if symbol.isdigit() or symbol in sign_priority:
                    math_expr += symbol
                    start = True

                elif symbol != ' ' and math_expr != '':
                    answer = expr_result(math_expr)
                    if answer is not None:
                        answer = round(answer, 4)
                        changed_line += str(answer) + ' '
                        all_expr[math_expr] = answer
                    else:
                        changed_line += math_expr + ' '
                    changed_line += symbol
                    math_expr = ''
                    start = False

                elif symbol == ' ' and start:
                    continue

                else:
                    changed_line += symbol
                    
            if math_expr != '':
                answer = expr_result(math_expr)
                if answer is not None:
                    answer = round(answer, 4)
                    changed_line += str(answer) + ' '
                    all_expr[math_expr] = answer
                else:
                    changed_line += math_expr + ' '
                math_expr = ''
                start = False

            text[i] = changed_line

        for key in all_expr:
            print(key.replace(' ', ''), '=', all_expr[key])
            
        print('\nПолученный текст: \n')
        print(*text, sep='\n')

    elif choice == '7':
        letter = input('Введите букву: ')
        max_amt = 0; max_idx = 0

        for num, line in enumerate(text):
            count = 0
            for i, symbol in enumerate(line):
                if symbol == letter and (line[i-1] == ' ' or i == 0):
                    count += 1
            if count > max_amt:
                max_amt = count
                max_idx = num
                
        if max_amt == 0:
            print('Слов, начинающихся с заданной буквы, нет')
        else:
            print('Искомая первая найденная строка: \n"',
                  text[max_idx], '"', sep='')

    # Неверная команда
    else:
        print('Введенного номера команды', choice, 'нет')
