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
    optionsMenuHeader(header)
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
            print("ERROR: Invalid input!\n")

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


def listToQuery(valuelist):
    outputstring = '"' # double quotes needed for SQL to accept them as values
    for i, detail in enumerate(valuelist):
        if i != len(valuelist)-1:  # Adds  '", "' after every input except for the last
            outputstring += str(detail) + '", "'
        else:
            outputstring += str(detail) + '"'
    return outputstring


def formatDbRow(row, attributes):
        outputstring = (20 * '=') + '\n'
        for i, userattribute in enumerate(row):
            outputstring += attributes[i] + str(userattribute) + '\n'
        return outputstring


def dbOutputToList(listoftuples):
    for i, item in enumerate(listoftuples):
        listoftuples[i] = list(item)
    return listoftuples


def prettyString(msg):
    output = f'{6*"*"}{(len(str(msg))*"*")}\n|  {msg}  |\n{6*"*"}{(len(str(msg))*"*")}\n'
    return output

def prettyPrint(msg):
    print(prettyString(msg))


def appendStrings(list_of_strings, divider='|', left_border='|'):
    output = ''
    for string in list_of_strings:
        output += str(string) + divider
    return output


def appendMultiRowStrings(list_of_string_lists, divider='  |  ', divider_margin=2):
    divider = f'{divider_margin * " "}{divider}{divider_margin * " "}'
    inverted_list = [list(row) for row in zip(*list_of_string_lists)]
    output = ''
    for string_list in inverted_list:
        output += f'{appendStrings(string_list, divider)}\n'
    return output


def nestedStringArrToStrTable(list_of_string_lists, row_titles=None, col_titles=None):
    return_string = ''
    if col_titles is None:
        max_nr_of_cols = len(list_of_string_lists)
        col_titles = [str(i) for i in range(max_nr_of_cols+1)]
    if row_titles is None:
        row_titles = [str(i+1) for i in range(len(list_of_string_lists)-1)]
        # row_titles.pop()

    title_col_length = len(max(row_titles))
    title_row_length = len(max(col_titles))

    list_of_string_lists.insert(0, row_titles)
    for i, title in enumerate(col_titles):
        list_of_string_lists[i].insert(0, title)
        return_string += separateRows(list_of_string_lists[i], title_col_length, title_row_length)
    '''
    mls = separateRows(list_of_string_lists)
    mls = appendMultiRowStrings(mls, '')
    return mls
    '''

def printNestedList(nested_list, *indices):
    print('\n'.join(str([sublist[i] for i in indices]) for sublist in nested_list))


def separateRows(string_list, title_col_length, title_row_length):
    row = ''
    for string in string_list:
        row += f'+ {(title_col_length*3)*"-"} '
    row += '+\n'
    for i, string in enumerate(string_list):
        if i == 0:
            row += '|  '
        row += string
        row += f'{title_row_length*" "}|  '
        margin = int(((title_row_length + 4) - len(string)) / 2)
        # row += f'{(margin-1)*" "}{string}{margin*" "}|'
    print(row)
    return row
