from os import mkdir, getcwd
from os.path import isdir, join
from shutil import rmtree
from sys import argv
from utilities import printf

files_path = join(getcwd(), "files")
if isdir(files_path):
    rmtree(files_path)
mkdir(files_path)

if len(argv) > 1:
    test_number = int(argv[1])
else:
    test_number = 50

def generate_test():
    printf(parts = [1, 2, 3, 4, 5, 6, 7], new_testcase = True, filename="input.txt")

    """
    ==========================================================================================================
                                            Create/Load Utilities
    ==========================================================================================================                          
    """
    # testcase_input -> Input for testcase
    testcase_input = []

    """
    ==========================================================================================================
                                    Generate Data required for the assignment
    ==========================================================================================================                          
    """

    ## PARTE 1
    from main_parts.main_1 import generate_main_p1, generate_input_p1
    main_py = generate_main_p1()
    input_txt = generate_input_p1()
    printf(parts = [1], data = main_py, filename = "main.py")
    printf(parts = [1], data = input_txt, filename = "input.txt")

    ## PARTE 2
    from main_parts.main_2 import generate_main_p2, generate_input_p2
    main_py = generate_main_p2()
    input_txt = generate_input_p2()
    printf(parts = [2], data = main_py, filename = "main.py")
    printf(parts = [2], data = input_txt, filename = "input.txt")

    ## PARTE 3
    from main_parts.main_3 import generate_main_p3, generate_input_p3
    main_py = generate_main_p3()
    input_txt = generate_input_p3()
    printf(parts = [3], data = main_py, filename = "main.py")
    printf(parts = [3], data = input_txt, filename = "input.txt")


    ## PARTE 4
    from main_parts.main_4 import generate_input_p4, generate_main_p4
    
    input_txt = generate_input_p4()
    printf(parts = [4], data = input_txt, filename = "input.txt")

    main_py = generate_main_p4()
    printf(parts = [4], data = main_py, filename = "main.py")


    # PARTE 5
    from main_parts.main_5 import generate_main_p5, generate_input_p5
    
    input_txt = generate_input_p5()
    printf(parts = [5], data = input_txt, filename = "input.txt")

    main_py = generate_main_p5()
    printf(parts = [5], data = main_py, filename = "main.py")


    # PARTE 6
    from main_parts.main_6 import generate_input_p6, generate_main_p6
    input_txt = generate_input_p6()
    printf(parts = [6], data = input_txt, filename = "input.txt")

    main_py = generate_main_p6()
    printf(parts = [6], data = main_py, filename = "main.py")


    # PARTE 7
    from main_parts.main_7 import generate_input_p7, generate_main_p7
    input_txt = generate_input_p7()
    printf(parts = [7], data = input_txt, filename = "input.txt")

    main_py = generate_main_p7()
    printf(parts = [7], data = main_py, filename = "main.py")
    


for t in range(test_number):
    generate_test()
