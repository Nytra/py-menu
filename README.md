# PyMenu-Framework
A Python3 based framework for creating simple but intuitive text-based menu interfaces.

---

##How To Use The Py-Menu Framework
Create a new menu object and initialise it with a title, description and optional footer.
Buttons can be added to the menu by calling the .add method and passing it a name and a function pointer.
For example:

- myMenu = pymenu.Menu("Main Menu", "Choose An Option", "Some random footer text")
- myMenu.add("A button", some_function)
- myMenu.add("Another button", lambda: print("Hello, world"))

Once you have added all of your buttons, you can activate the menu by calling the start method.

- myMenu.start()

Other useful methods include redraw(), quit() and set_program_title().

---
