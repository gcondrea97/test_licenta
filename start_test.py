import os
import json
import random

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from pick import pick
except ImportError:
    install('pick')
    from pick import pick

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def start_test():
    corecte = 0
    gresite = 0

    with open(os.path.join(os.getcwd(), 'intrebari.json')) as f:
        text = json.load(f)
    intrebari = text['intrebari']
    nr_questions = int(input('Nr de intrebari: '))

    for i in range(nr_questions):
        print(f"{bcolors.UNDERLINE}{bcolors.BOLD}----> Intrebarea {i+1}/{nr_questions} -------- {bcolors.OKGREEN}{corecte}{bcolors.ENDC} - {bcolors.FAIL}{gresite}{bcolors.ENDC}")
        random.shuffle(intrebari)
        intrebare = intrebari.pop(0)

        print(f"{bcolors.HEADER}{bcolors.BOLD}{intrebare['intrebare']}{bcolors.ENDC}\n")
        print(f"\tA - {intrebare['var_A']}\n")
        print(f"\tB - {intrebare['var_B']}\n")
        print(f"\tC - {intrebare['var_C']}\n")

        raspuns = input(f'{bcolors.OKBLUE}RASPUNS(A/B/C){bcolors.ENDC}: ')
        if raspuns.upper() not in ['A', 'B', 'C']:
            print(f"{bcolors.WARNING} RASPUNS INVALID!{bcolors.ENDC}\n")
            gresite+=1
            continue
        if raspuns.upper() == intrebare['var_corecta']:
            print(f"\t{bcolors.OKCYAN}{bcolors.BOLD} Corect! {bcolors.ENDC}\n")
            corecte+=1
        else:
            print(f"{bcolors.FAIL} Gresit! {bcolors.UNDERLINE} Raspuns corect: {intrebare['var_corecta']}{bcolors.ENDC}\n")
            gresite+=1

    print(f"{bcolors.BOLD}{bcolors.UNDERLINE} FINAL! \n{bcolors.ENDC}")
    print(f"\t{bcolors.BOLD}{bcolors.OKGREEN} Raspunsuri corecte: {corecte}{bcolors.ENDC}\n")
    print(f"\t{bcolors.BOLD}{bcolors.FAIL} Raspunsuri gresite: {gresite}{bcolors.ENDC}\n")

    if os.path.exists(os.path.join(os.getcwd(), 'rezultate.txt')):
        with open(os.path.join(os.getcwd(), 'rezultate.txt'), 'a') as f:
            f.write(f"Rasp corecte: {corecte} - Rasp gresite: {gresite}\n")
    else:
        with open(os.path.join(os.getcwd(), 'rezultate.txt'), 'w+') as f:
            f.write(f"Rasp corecte: {corecte} - Rasp gresite: {gresite}\n")

if __name__ == '__main__':
    while True:
        start_test()
        input("Press any key to restart")



    