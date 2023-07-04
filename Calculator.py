#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is a program to write equations into a text file
  or to retrieve equations from a text file.
"""

# This is the third version of this program. I think I have solved all the problems
# indicated in the first two reviews by coding menus for every step. I know there are
# many things to improve, so please, feel free to give me any advice that you
# consider appropriate.


def inputs(string):
    """Display all the inputs in the program, depending on the string argument."""
    variable = input(f"\n{string}. (Enter '..' if you wish to exit): > ").strip(" '")
    return variable


def get_num(opt):
    """Input the numbers to create an equation. Opt is an integer to choose
    between the first or second number. Return the number inputted."""
    # There are two calls to this function in the main part of the script, one for
    # the first number and another for the second one.
    if opt is True:
        string = "Enter the first number of the equation"
    else:
        string = "Enter the second number of the equation"
    user_input = ""
    while user_input != "..":
        user_input = inputs(string)
        if user_input == "..":
            print("\nReturning to the main menu.")
        else:
            # Defensive programming in case the input is not a number
            try:
                num = float(user_input)
                print("\n.... Number added to memory .....")
                return num
            # If it's not possible to convert the input to float, a new input is required
            except ValueError:
                print("\nYou have not entered a number. Try again.")


def choose_op(num1, num2):
    """Allow to choose an operator and perform the operation on the numbers previously inputted."""
    operator = ""
    result = None
    while operator != "..":
        operator = inputs(
            "Enter the operation to perform on the numbers (+, -, *,  / or ** (exp))")
        if operator == "+":
            result = num1 + num2
            break
        elif operator == "-":
            result = num1 - num2
            break
        elif operator == "*":
            result = num1 * num2
            break
        elif operator == "/":
            try:
                result = num1 / num2
                break
            except ZeroDivisionError:
                print("\nYou are trying to divide by 0."
                      "The result is not a number. Try again.")
                return
        elif operator == "**":
            try:
                result = num1 ** num2
                break
            except OverflowError:
                print("\nThe result number is above the limits for this processor."
                      "The result is not a number. Try again.")
                return
        elif operator == "..":
            print("\nNo equation inputted. Deleting numbers and exiting...")
        else:
            print("\nNot a valid operator. Try again.")
    if result is None:
        return
    else:
        return f"{num1} {operator} {num2} = {result:.2f}"


def wrong_input(counter):
    """Warnings to let the user know that is not entering a correct input. Counter is
    an integer to count the number of wrong inputs."""
    print("\nNot a valid input. Try again.\n")
    if counter > 6 and counter < 10:
        print(f"\nYou couldn't enter a valid option. {10-counter} tries left.")
        return False
    elif counter == 10:
        print("""\nReturning to the menu""")
        return True


def input_file(opt=True):
    """Input the file to store the equation in, or retrieve the equations from
    (depending on opt), and check if is a text file. Return the name inputted."""
    if opt is True:
        string1 = "Enter a name for the text file where the equation will be stored"
        string2 = "Save File Menu"
    else:
        string1 = "Enter a text file to retrieve the equations from"
        string2 = "Retrieval Menu"
    named_file = ""
    counter = 0
    while named_file != "..":
        named_file = inputs(f"\n{string1} (with the extension .txt)")
        if named_file.endswith(".txt"):
            return named_file
        elif named_file == "..":
            print(f"\nReturning to the {string2}")
            return
        else:
            warning = wrong_input(counter)
            counter += 1
            if warning is True:
                return
            else:
                continue


def default_option(file, opt=False):
    '''Once an equation has already been stored, give a quicker option to save the
    new equation or to retrive the equation(s). Return True, False or None depending
    on the answer.

    Keyword arguments:
    file -- name of the file where the equations has been or will be stored
    opt -- boolean, False for saving the equation, True for retrieving (default False) 
    '''
    choose = ""
    counter = 0
    if opt is False:
        string = ("Would you like to save the equation in the same file"
                  f" ('{file}') as before?")
    else:
        string = ("Would you like to retrieve the equations from the last file"
                  f" ('{file}') where you stored your last equation?")
    while choose != "..":
        choose = inputs(f"\n{string} (yes[y]/no[n])").lower()
        if choose == "yes" or choose == "y":
            return True
        elif choose == "no" or choose == "n":
            return False
        elif choose == "..":
            print("\nReturning to the menu")
            return
        else:
            warning = wrong_input(counter)
            counter += 1
            if warning is True:
                return
            else:
                continue


def saver(equation, counter, file_name=None):
    """ Main function to save the equation into a file, managing unexpected events.

    Keyword arguments:
    equation -- equation inputted as string
    counter  -- global boolean to check if an equation has already been stored
    file_name -- name of the file where the new equation will be stored (default None) 
    """
    def save_file(equation, file):
        """Save the equation into the file returning the file used."""
        file_txt = open(f"{file}", 'a')
        file_txt.write(equation + "\n")
        print(f"\nEquation '{equation}' succesfully saved in '{file}'")
        file_txt.close()
        return file

    def save_menu(equation):
        """Menu with the different options to save the equation. Return the equation saved."""
        choose = ""
        default_file = 'Equations.txt'
        while choose != "3":
            print("\nSave File Menu --------------\n\n"
                  "1. Store the equation into 'Equations.txt'\n\n"
                  "2. Input a file name to store the equation\n\n"
                  "3. Exit this menu and return to the Main Menu")
            # 4. Exit the program      New feature to include
            choose = input("\nChoose 1, 2 or 3: ")
            if choose == "1":
                return save_file(equation, default_file)
            elif choose == "2":
                name = input_file()
                if name is None:
                    continue
                else:
                    return save_file(equation, name)
            elif choose == "3":
                print("\nDeleting numbers and returning to the Main Menu")
            else:
                print("Not a valid option. Try again")

    if counter is True and file_name is not None:
        opt = default_option(file_name)
        if opt is True:
            return save_file(equation, file_name)
        else:   # False or None
            # Give the chance to store it in Equations.txt instead than having to enter the name
            if file_name != "Equations.txt" or opt is None:
                return save_menu(equation)
            else:
                # If previous file was Equations.txt, or opt is False, no need to go to the menu.
                file = input_file()
                if file is None:
                    return save_menu(equation)
                else:
                    return save_file(equation, file)
    else:
        return save_menu(equation)


def retrieve_eq(counter, file=None):
    """Includes all functions to retrieve equations from a file.

    Keyword arguments:
    counter -- global boolean to check if an equation has already been stored
    file -- name of the file where the last equation was stored (default None)
    """
    def extract(file_retrieved='Equations.txt'):
        """Return the equations stored in the file and the file used."""
        file = None
        list_equations = []
        try:
            file = open(f"{file_retrieved}", 'r')
            list_equations = file.readlines()
        except FileNotFoundError as error:
            # Displaying the error that Python is giving us
            print(f"\nThe file does not exist. Try again.\n{error}")
        # To terminate the file after it has been used whether or not the exception has occurred
        finally:
            if file is not None:
                file.close()
        return file, list_equations

    def print_eq(list_equations):
        """Display the already retrieved equations."""
        print("\nThese are the equations stored in the file:\n")
        for i, equations in enumerate(list_equations):
            print(f"Equation number {i+1}: {equations}")

    def manage_output(file='Equations.txt'):
        """Check if there are no equations in the file. If there are, print them."""
        file_name, equations_retrieved = extract(file)
        if equations_retrieved == []:
            if file_name is not None:
                print("\nNo equations found in the file")
            return False
        else:
            print_eq(equations_retrieved)
            return True

    def retrieve_menu():
        """Menu with the different options to retrieve the equations. Returns the equations (if any)."""
        choose = ""
        while choose != "3":
            print("\nRetrieval Menu ---------\n"
                  "\n1. Retrieve equations from default file 'Equations.txt'\n"
                  "\n2. Input a file name to retrieve equations from\n"
                  "\n3. Exit and return to Main Menu")
            choose = input("\nChoose 1, 2 or 3: ")
            if choose == "1":
                out = manage_output()
                if out is False:
                    continue
                else:
                    break
            elif choose == "2":
                name = input_file(False)
                if name is None:
                    continue
                else:
                    out = manage_output(name)
                    if out is False:
                        continue
                    else:
                        break
            elif choose == "3":
                print("\nReturning to the Main Menu")
            else:
                print("Not a valid option, try again")

    if counter is True and file is not None and not counter2:
        chosen = default_option(file, True)
        if chosen is True:
            file_name, equations = extract(file)
            print_eq(equations)
        else:
            # To give the chance to extract eq. easily from Equations.txt instead than having to enter the name
            if file != "Equations.txt" or chosen is None:
                return retrieve_menu()
            else:  # If previous file was Equations.txt, or chosen is False, no need to come back to the menu.
                file = input_file()
                if file is None:
                    return retrieve_menu()
                else:
                    manage_output(file)
    else:
        return retrieve_menu()


# Main part of the script
print("\n--- Welcome to the calculator program --- \n".center(40))
option = ""
counter = False  # No equation has been saved yet
counter2 = True   # Go to the Retrieval Menu strightaway and not default_option
while option != "3":
    print("\nMain Menu ---------------\n\n"
          "1. Input an equation and store it into a file\n\n"
          "2. Retrieve equations from a file\n\n"
          "3. Exit")
    option = input("\nChoose 1, 2 or 3: ")
    if option == "1":
        num1 = get_num(True)
        if num1 is None:
            continue
        num2 = get_num(False)
        if num2 is None:
            continue
        result = choose_op(num1, num2)
        if result is None:
            continue
        else:
            print(f"\nThe equation created is: {result}")
        if counter is False:
            name = saver(result, counter)
            counter = True
            counter2 = False
        else:
            name = saver(result, counter, name)
            counter2 = False
    elif option == "2":
        if counter is False:
            retrieve_eq(counter)
        else:
            retrieve_eq(counter, name)
            counter2 = True
    elif option == "3":
        print("\nGoodbye!")
    else:
        print("\nNot a valid option, try again.")
