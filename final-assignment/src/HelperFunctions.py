import os
# from numpy import append
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def optionsMenu(header, options, clear=False, prompt="> "):
    # Input: List of options
    # Output: Index + 1 of the option that the user selected
    # Output: -1 if the user wants to go back in the menu
    if clear:
        clear()
    print(header)
    print(60*"-")
    for i, option in enumerate(options):
        print(f"{i+1}. {option[1]}")
    print("\n")
    while True:
        choice = input(prompt).strip()
        if choice == 'b':
            return -1
        try:
            choice = int(choice)
            if choice in range(1, len(options)+1):
                return choice - 1
            else:
                print(f"\nInvalid option. Please try again. (1 - {len(options)})")
        except ValueError:
            print(f"\nInvalid option. Please try again. (1 - {len(options)})")


def yesNoInput(question='', default_yes=True, clear=False):
    if clear:
        clear()

    if default_yes:
        suffix = ' (Y/n)'
        question += suffix + '\n'
    else:
        suffix = ' (y/N)'
        question += suffix + '\n'
    user_input = input(question).strip()

    while user_input not in ['Y', 'N', 'y', 'n', '']:
        user_input = input(f'Invalid input please enter {suffix}\n').strip()

    if user_input == 'Y' or user_input == 'y' or (user_input == '' and default_yes):
        return True
    return False


def readUserInput(questionList, clear=False, prompt="> "):
    if clear:
        clear()
    user_input = []
    for i, question in enumerate(questionList):
        user_input.append(input(question + "\n" + "(Press b to cancel)\n\n" + prompt).strip()) ## The char escape functie zou hier aangeroepen kunnen worden
        while user_input[i] == '':
            print('This field cannot be empty')
            user_input.pop() # Removes the empty space added to list
            user_input.append(input(question + "\n" + "(Press b to cancel)\n\n" + prompt)) ## The char escape functie zou hier aangeroepen kunnen worden
        if user_input[i] == 'b':
            return []
    return user_input

def readUserInput2(message, clear=False, prompt="> "):
    while True:
        user_input = input(message + "\n" + prompt).strip().lower()
        if user_input == 'b':
            return 'b'
        elif user_input.startswith('cancel'):
            args = user_input.split()
            return args[1]
        else:
            print("ERROR [!]: Invalid input!\n")

def readUserInput3(message, clear=False, prompt="> "):
    while True:
        user_input = input(message + "\n" + prompt).strip().lower()
        if user_input == 'b':
            return 'b'
        elif user_input == "changepw":
            result = readUserInput(["Enter a new password:", "Re-enter your password to confirm"], prompt=prompt)
            new_pw, new_pw_confirmed = result[0], result[1]
            try_again = True
            while try_again:
                if new_pw == new_pw_confirmed:
                    return new_pw
                try_again = yesNoInput("Passwords did not match!\nWould you like to try again?")
                if try_again:
                    new_pw, new_pw_confirmed = readUserInput(["Enter a new password:", "Re-enter your password to confirm" ])
            return ""
        else:
            print("ERROR [!]: Invalid input!\n")

def logEvent(log_message):
    with open("hash_log.txt", "a") as f:
        f.write(log_message)
        f.write("\n")

def enterToContinue(message=''):
    input(str(message) + '\nPlease press enter to continue...')


def pageHeader(text):
    print(f'*{(len(text)*"=")}*\n|{text}|\n*{(len(text)*"-")}*\n')


def optionsMenuHeader(text):
    print(f'{text}\n{len(text) * "-"}')


def formatDbRow(row, attributes):
        outputstring = (20 * '=') + '\n'
        for i, userattribute in enumerate(row):
            outputstring += attributes[i] + str(userattribute) + '\n'
        return outputstring


def prettyString(msg):
    output = f'{6*"*"}{(len(str(msg))*"*")}\n|  {msg}  |\n{6*"*"}{(len(str(msg))*"*")}\n'
    return output

def prettyPrint(msg):
    print(prettyString(msg))
