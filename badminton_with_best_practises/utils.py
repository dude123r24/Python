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
    print(f"Error: {message}")
    print_seperator_plus ()
    print (" ")