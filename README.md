# py-menu
A Python 3 based framework for creating simple text-based menus.

---

To use it, simply create a new Menu object and initialise it with (title, fg, bg)
- title is a string
- fg and bg use colorama's colours. For example, if you wanted red you would use Fore.RED or Back.RED

Menu objects have a method called add which is used to add new menu options.
- add(button_name, function_pointer). For example, m.add("Button 1", some_function).
- lambda can also be used to pass in arguments. For example, m.add("Button 1", lambda: print("Hello, world"))

To display the menu, use start().
