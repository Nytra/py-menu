import pymenu

# Now we will define some functions that our menu buttons will be linked to.
def hello():
    print("Hello, world!")

# This next function will create a new menu within the main menu (Allows you to have buttons that bring up different menu screens)
def new_menu():

    # Here we create a new menu object with different attributes.
    newMenu = pymenu.Menu("Second Menu", "This is a separate menu", "This is some different footer text")

    # Again we should set the program title.
    newMenu.set_program_title("PyMenu Demonstration")

    newMenu.add("First Button", hello)

    # We should be able to return to the previous menu
    newMenu.add("Back", newMenu.quit)

    # And now to display the new menu.
    newMenu.start()

    # Finally, we should redraw the previous menu after the new menu has closed.
    myMenu.redraw()



# Create a new menu object. Menu(Title, Description, Footer)
myMenu = pymenu.Menu("Main Menu", "This is a short description of the menu.", "This is some footer text.")

# We should display the name of our program in the bottom right. If not specified, PyMenu VX will be displayed.
myMenu.set_program_title("PyMenu Demonstration")

# Add a new button to the menu. add(Text, Function Pointer)
myMenu.add("First Button", hello)
# It is important that you do not include parentheses when typing the function name.

# We can create a button which links to another menu
myMenu.add("Next Menu", new_menu)

# We should be able to close the menu (This will end the program in this case)
myMenu.add("Exit", myMenu.quit)

# Finally, in order to display the menu, we call the start() method.
myMenu.start()