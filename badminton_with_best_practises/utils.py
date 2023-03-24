# utils.py
def print_seperator_tilda():
    print("~" * 80)

def print_seperator_star():
    print("*" * 80)

def print_seperator_plus():
    print("+" * 80)

def print_error(message):
    print (" ")
    print_seperator_plus ()
    print(f"Error : {message}")
    print_seperator_plus ()
    print (" ")

def print_title(message):
    print (" ")
    print (" ")
    print_seperator_tilda ()
    print(f"{message}")
    print_seperator_tilda ()

def print_info(message):
    print (" ")
    print_seperator_star ()
    print(f"Info  : {message}")
    print_seperator_star ()