from colorama import Fore


def log(level, text):
    if level == 0:
        print(f"{Fore.RED}FATAL:{Fore.RESET} {text}")
    elif level == 1:
        print(f"{Fore.LIGHTRED_EX}Error:{Fore.RESET} {text}")
    elif level == 2:
        print(f"{Fore.YELLOW}Warning:{Fore.RESET} {text}")
    elif level == 3:
        print(f"{Fore.LIGHTBLUE_EX}INFO:{Fore.RESET} {text}")
    elif level == 4:
        print(f"{Fore.GREEN}Success:{Fore.RESET} {text}")
