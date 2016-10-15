import pymenu

# Initialise Colorama
pymenu.init()



# Now we will define some functions that our menu buttons will be linked to.
def hello():
    print("Hello, world!")

# This next function will create a new menu within the main menu (Allows you to have buttons that bring up different menu screens)
def new_menu():
    newMenu = pymenu.Menu("Second Menu", "This is a separate menu", "This is some different footer text")

    newMenu.set_program_title("PyMenu Demonstration") # Again we should set the program title

    newMenu.add("First Button", hello)
    newMenu.add("Back", newMenu.quit) # We should be able to return to the previous menu
    newMenu.start()

    # Finally, we should redraw the previous menu after the new menu has closed.
    myMenu.redraw()



# Create a new menu object. Menu(Title, Description, Footer)
myMenu = pymenu.Menu("Main Menu", "This is a short description of the menu.", "This is some footer text.")

myMenu.set_program_title("PyMenu Demonstration") # We should display the name of our program in the bottom right.

# Add a new button to the menu. add(Text, Function Pointer)
myMenu.add("First Button", hello)
# NOTE: It is important that you do not include parentheses when typing the function name.

# We can create a new menu from within another one
myMenu.add("Next Menu", new_menu)

myMenu.add("Exit", myMenu.quit) # We should be able to close the menu (This will end the program in this case)
myMenu.start()
