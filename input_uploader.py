from TestCasesBot import Bot
from getpass import getpass

MAIL = input('Mail: ')
PSWD = getpass()
assignment = input('Ingresa el nombre de la Tarea: ')
part_name = input('Ingresa el nombre completo de la parte de la tarea: ')


num_testcases = int(input('Indica el número de testcases a subir (Par): '))

inputs = []
for i in range(num_testcases):
    i = str(i)
    if len(i) == 1:
        i = f'0{i}'

    with open(f'input/input{i}.txt', 'r') as f:
        testcase_text = ''
        for line in f.readlines():
            testcase_text = testcase_text + line
    inputs.append(testcase_text)

half = int(num_testcases / 2)

public = inputs[ : half]
private = inputs[half : ]

bot = Bot()
bot.login_mimir(MAIL, PSWD)
bot.enter_course()
bot.select_assignment(assignment)
bot.enter_edit_menu()

i = 1
for public_tc, private_tc in zip(public, private):
    bot.add_testcase(f'Público #{i}', 0, '', public_tc, part_name)
    bot.add_testcase(f'Secreto #{i}', 4, '', private_tc, part_name, public = False)
    i += 1

print('Todos los testcases han sido subidos con exito :)')
