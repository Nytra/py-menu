import pymenu

# This is an example of how a dialog box is created using PyMenu.

m = pymenu.Menu("Dialog Box Demo", "This is a dialog box", "This is some footer text")
m.set_program_title("Dialog Box Demo")

# Here we must specify what text will appear in the dialog box. This step is essential.
m.set_dialog_msg("Are you sure you want to continue?")

# We should add some buttons to give the user some choice.
m.add("Yes", m.quit)
m.add("No", m.quit)

# And now we display the interface.
m.start()