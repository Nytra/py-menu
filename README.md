# PyMenu-Framework
A Python (3.1+) based framework for creating simple and intuitive graphical menu interfaces.

Supported operating systems: Windows (Linux support will not be difficult to implement but is not a huge concern at the moment)

Main features: 
- Can take user input in the form of strings as well as boolean checkboxes. 
- Can display information in the form of text boxes (With word-wrapping functionality)
- Menus can contain many different buttons and inputs simultaneously.
- Input is asynchronous (ie the program doesn't halt when an input is being taken)
- Menus are resized dynamically depending on the number and scale of the elements within them.
- Buttons are linked to existing functions within the program.
- Menus can be stacked. If one is closed then the previous one is started up again.

---

![Image of PyMenu](https://github.com/Nytra/PyMenu-Framework/blob/master/images/main_menu.PNG)

PyMenu is capable of displaying many different buttons on the screen with each one linked to a specific function.

---

![Image of a Dialog Box](https://github.com/Nytra/PyMenu-Framework/blob/master/images/dialog.png)

PyMenu can display dialog boxes which contain text. The text will be automatically word wrapped to fit on the screen, no matter the screen dimensions.

---

![Image of Dialog Box Options](https://github.com/Nytra/PyMenu-Framework/blob/master/images/dialog_choices.png)

Dialog boxes are capable of containing many different buttons as well as multiple types of inputs.

---

![Image of Dynamic Resizing](https://github.com/Nytra/PyMenu-Framework/blob/master/images/resize.png)

The framework will automatically detect when the terminal dimensions have changed and it will resize the interface accordingly.

---

