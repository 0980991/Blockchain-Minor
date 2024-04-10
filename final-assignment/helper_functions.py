import os
# from numpy import append
class HelperFunctions:
    def __init__(self):
        self.prompt = "(guest)> "


    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')


    def optionsMenu(self, header, options, clear=True):
        # Input: List of options
        # Output: Index + 1 of the option that the user selected
        # Output: -1 if the user wants to go back in the menu
        # Makes sure that invalid input gets cancelled
        if clear:
            self.clear()
        self.optionsMenuHeader(header)
        for i, option in enumerate(options):
            print(f"{i+1}. {option[1]}")
        print("\n")
        choice = input(self.prompt)
        if choice == 'b':
            return -1
        try:
            while int(choice) not in range(len(options)+1) or int(choice) == 0:
                print(f"\nInvalid option. Please try again. (1 - {len(options)})")
                choice = input(self.prompt)
        except ValueError:
            print(f"\nInvalid option. Please try again. (1 - {len(options)})")
            choice = input(self.prompt)
        return int(choice) - 1


    def yesNoInput(self, question='', default_yes=True, clear=True):
        if clear:
            self.clear()

        if default_yes:
            question += ' (Y/n)\n'
        else:
            question += ' (y/N)\n'
        user_input = input(question)

        while user_input not in ['Y', 'N', 'y', 'n', '']:
            user_input = input('Invalid input please enter y or n\n')

        if user_input == 'Y' or user_input == 'y' or (user_input == '' and default_yes):
            return True
        return False


    def readUserInput(self, questionList, clear=True):
        if clear:
            self.clear()
        user_input = []
        for i, question in enumerate(questionList):
            user_input.append(input(question + "\n" + "(Press b to cancel)\n\n" + self.prompt)) ## The char escape functie zou hier aangeroepen kunnen worden
            while user_input[i] == '':
                print('This field cannot be empty')
                user_input.pop() # Removes the empty space added to list
                user_input.append(input(question + "\n" + "(Press b to cancel)\n\n" + self.prompt)) ## The char escape functie zou hier aangeroepen kunnen worden
            if user_input[i] == 'b':
                return []
        return user_input

    def readUserInput2(self, clear=True):
        while True:
            user_input = input("Enter 'b' or 'cancel x' (where x is a transaction id): ").strip().lower()
            if user_input == 'b':
                return 'b'
            elif user_input.startswith('cancel'):
                args = user_input.split()
                if len(args) == 2 and args[1].isdigit():
                    return int(args[1])
                else:
                    print("Invalid input. Please enter 'b' or 'cancel x' where x is an integer.")
            else:
                print("Invalid input. Please enter 'b' or 'cancel x' where x is an integer.")

    def enterToContinue(self, message=''):
        input(message + '\nPlease press enter to continue...')


    def pageHeader(self, text):
        print(f'*{(len(text)*"=")}*\n|{text}|\n*{(len(text)*"-")}*\n')


    def optionsMenuHeader(self, text):
        print(f'{text}\n{len(text) * "-"}')


    def listToQuery(self, valuelist):
        outputstring = '"' # double quotes needed for SQL to accept them as values
        for i, detail in enumerate(valuelist):
            if i != len(valuelist)-1:  # Adds  '", "' after every input except for the last
                outputstring += str(detail) + '", "'
            else:
                outputstring += str(detail) + '"'
        return outputstring


    def formatDbRow(self, row, attributes):
            outputstring = (20 * '=') + '\n'
            for i, userattribute in enumerate(row):
                outputstring += attributes[i] + str(userattribute) + '\n'
            return outputstring


    def dbOutputToList(self, listoftuples):
        for i, item in enumerate(listoftuples):
            listoftuples[i] = list(item)
        return listoftuples


    def prettyString(self, msg):
        output = f'{6*"*"}{(len(msg)*"*")}\n|  {msg}  |\n{6*"*"}{(len(msg)*"*")}\n'
        return output


    def prettyPrint(self, msg):
        print(prettyString(msg))


    def appendStrings(self, list_of_strings, divider='|', left_border='|'):
        output = ''
        for string in list_of_strings:
            output += str(string) + divider
        return output


    def appendMultiRowStrings(self, list_of_string_lists, divider='  |  ', divider_margin=2):
        divider = f'{divider_margin * " "}{divider}{divider_margin * " "}'
        inverted_list = [list(row) for row in zip(*list_of_string_lists)]
        output = ''
        for string_list in inverted_list:
            output += f'{appendStrings(string_list, divider)}\n'
        return output


    def nestedStringArrToStrTable(self, list_of_string_lists, row_titles=None, col_titles=None):
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

    def separateRows(self, string_list, title_col_length, title_row_length):
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
