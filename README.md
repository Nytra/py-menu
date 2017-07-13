# PyMenu
A Python 3 based framework for creating simple and intuitive text-based menu interfaces.

---

![Main Menu](https://github.com/Nytra/PyMenu-Framework/blob/master/images/mainmenu.png)

Menus can contain a number of different elements. This one contains three buttons. Each button is linked to a specific function in the program. Pressing enter while a button is selected will execute the aforementioned function. In this case, the functions displayed here will each create a new menu instance and display it on top of the current one.

![Scrolling Buttons](https://github.com/Nytra/PyMenu-Framework/blob/master/images/scrollbuttons.png)

The framework will display a scrollbar if the number of elements is too large. In this example, I am scrolling down through a list of buttons. In the bottom right-hand corner there is a counter which displays the number of the button that is currently selected, as well as the total number of buttons.

![Scrolling Inputs](https://github.com/Nytra/PyMenu-Framework/blob/master/images/scrollinputs.png)

The same goes for inputs. 

![Scrolling Text](https://github.com/Nytra/PyMenu-Framework/blob/master/images/scrolltext.png)

Here I am scrolling through some word-wrapped text. The framework uses a custom algorithm to make sure that all words fit nicely within the boundaries of the menu.

![Inputs](https://github.com/Nytra/PyMenu-Framework/blob/master/images/inputs.png)

Here is an example of how input can be taken. There are three input fields displayed here. Two of which are standard string inputs - the final one is actually a boolean input. Pressing space while the checkbox is selected will toggle it between true and false.

![Input Feedback](https://github.com/Nytra/PyMenu-Framework/blob/master/images/inputfeedback.png)

Here the user input is being displayed in a separate menu.

![Quit Prompt](https://github.com/Nytra/PyMenu-Framework/blob/master/images/quitprompt.png)

A simple quit prompt.

![Quit Prompt Popup](https://github.com/Nytra/PyMenu-Framework/blob/master/images/quitpromptpopup.png)

The framework also supports "popup" style menus. You can see that the quit prompt is now being displayed on top of the previous menu instead of in a completely new frame.

---

Supported operating systems: Windows

Note: The msvcrt library is the only thing that is preventing this from being able to run on other operating systems.

---

Main features: 
- Can take user input in the form of strings as well as boolean checkboxes. 
- Can display information in the form of text boxes (With word-wrapping and scrolling functionality)
- Menus can contain many different buttons and inputs simultaneously. Scrolling functionality will be used if the number of elements is too large.
- Input is asynchronous (ie the program doesn't halt when an input is being taken)
- Menus are resized dynamically depending on the number and scale of the elements within them.
- Buttons are linked to existing functions within the program.
- Menus can be stacked. If one is closed then the previous one is started up again.

---

Navigation:
- Left & Right Arrow Keys: Select horizontal options.
- Up & Down Arrow Keys: Select vertical options.
- Enter: Activates the selected button.
- Space: Toggle checkboxes.
- Tab: Selects the next button/input.
- F5: Redraws the current menu.
- Escape: Closes the current menu.
- Any option highlighted in blue is currently selected.
