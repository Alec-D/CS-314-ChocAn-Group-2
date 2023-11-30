# print(str)
# print(type(str))
# print(None)
# print(type(type(None)))
# print(type(""))

def terminal():
    while True:
        print("Welcome to the ChocAn Terminal System!\n")
        print("Please choose an option below by entering a number between 1 and 3")
        print("1. I am a Provider")
        print("2. I am a Manager")
        print("3. Exit")
        userInput = getInputNumberSafe(3)
        match userInput:
            case 1:
                providerTerminal()
            case 2:
                managerTerminal()
            case 3:
                return
            case _:
                print("ERROR!!!")

def providerTerminal():
    while True:
        print("Welcome to the ChocAn Provider Terminal!\n")
        print("1. Do something")
        print("2. Do something else")
        print("3. Exit to main terminal")
        userInput = getInputNumberSafe(3)
        match userInput:
            case 1:
                pass
            case 2:
                pass
            case 3:
                return
            case _:
                print("ERROR!!!")

def managerTerminal():
    while True:
        print("Welcome to the ChocAn Manager Terminal!\n")
        print("1. Do something")
        print("2. Do something else")
        print("3. Exit to main terminal")
        userInput = getInputNumberSafe(3)
        match userInput:
            case 1:
                pass
            case 2:
                pass
            case 3:
                return
            case _:
                print("ERROR!!!")

def getInputNumberSafe(numOptions: int) -> int:
    while True:
        response = input("--> ")
        print("-------------------------------------------------")
        try:
            response = int(response)
            # if response in range(1, numOptions+1):
            if response >= 1 and response <= numOptions:
                return response
        except:
            pass
        print(f"Please enter a number between 1 and {numOptions}!")

if __name__ == "__main__":
    terminal()