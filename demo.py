import pymenu



# Now we will define some functions that our menu buttons will be linked to.
def hello(m):

    # Here we are calling the method msg() which takes a string constant as its only argument.
    # It will display this string at the top of the menu overlay and will automatically wrap the text if it's too long.
    m.msg("Hello, world!")

# This next function will create a new menu within the main menu
# (Allows you to have buttons that are linked to different menu screens)
def new_menu():

    # Here we create a new menu object with different attributes.
    newMenu = pymenu.Menu("Second Menu", "This is a separate menu", "This is some different footer text")

    # This button will be linked to the hello() function that we created earlier.
    newMenu.add("First Button", lambda: hello(newMenu))

    # We should be able to return to the previous menu
    newMenu.add("Back", newMenu.quit)

    # And now to display the new menu.
    newMenu.start()

    # Finally, we should redraw the previous menu after the new menu has closed.
    myMenu.redraw()



# Create a new menu object. Menu(Title, Description, Footer)
myMenu = pymenu.Menu("Main Menu", "This is a short description of the menu.", "This is some footer text.")

# We should display the name of our program in the bottom right. If not specified, PyMenu Vx.xx will be displayed.
# This only needs to be done once, because the program title is a global variable that is automatically applied to any
#   new menus that are created.
myMenu.set_program_title("PyMenu Demonstration")

# Add a new button to the menu. add(Text, Function Pointer)
myMenu.add("First Button", lambda: hello(myMenu))
# It is important that you do not include parentheses when typing the function name.

# We can create a button which links to another menu
myMenu.add("Next Menu", new_menu)

# We should be able to close the menu (This will end the program in this case)
myMenu.add("Exit", myMenu.quit)

# Finally, in order to display the menu, we call the start() method.
myMenu.start()