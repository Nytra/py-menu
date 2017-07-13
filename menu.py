from colorama import *
import msvcrt, time, os
init()

__author__ = "Sam Scott <samueltscott@gmail.com>"

def draw(x, y, text):
    print("\x1b[{};{}H".format(y, x) + text, end="")  # Move the cursor to the given coordinates and then print the text

class Menu:

    compatibility_mode = True # when True: maintains a 80x24 interface size.
                              # when False: the interface will scale dynamically according to the size of the terminal window.
                              # i recommend keeping this set to True as the scaling system isn't perfect and draw speeds could be extremely slow on large displays (like 1 or 2 seconds which is far too long)

    instance_num = 0
    menu_being_displayed = 0 # the id of the menu which is currently being displayed (ie top of the menu stack)

    bindings = {} # stores keybindings and function pointers

    # Keycode constants are defined below (Just the function keys 1-10)

    KB_F1 = 59
    KB_F2 = 60
    KB_F3 = 61
    KB_F4 = 62
    #KB_F5 = 63 # Note: F5 is used to redraw the current menu and thus cannot be bound to any other functions
    KB_F6 = 64
    KB_F7 = 65
    KB_F8 = 66
    KB_F9 = 67
    KB_F10 = 68

    program_title = "" # Appears at the very top of the menu.
    debug_message = "" # Only displayed if draw_debug_messages is set to True.
    draw_debug_messages = False

    # Interface colours and styles are defined below

    outer_bg = Back.BLUE
    outer_fg = Fore.WHITE
    outer_style = Style.BRIGHT

    overlay_bg = Back.WHITE
    overlay_fg = Fore.BLACK
    overlay_style = Style.NORMAL

    desc_bg = Back.WHITE
    desc_fg = Fore.BLUE
    desc_style = Style.NORMAL

    selected_bg = Back.BLUE
    selected_fg = Fore.WHITE
    selected_style = Style.BRIGHT

    debug_bg = Back.BLACK
    debug_fg = Fore.RED
    debug_style = Style.NORMAL

    input_bg = overlay_bg
    input_fg = Fore.BLUE
    input_style = overlay_style

    shadow_bg = Back.BLACK

    accent_fg = overlay_fg
    accent_bg = overlay_bg
    accent_style = overlay_style
    accent_alt_style = Style.BRIGHT

    # You can mess around with the values below if you like.
    # On a 1920x1080p display, the values X_MAX = 119, Y_MAX = 30 seem to work quite well (on my own PC at least).
    # The values 80, 24 will work on all kinds of displays, which is why they are being used here.

    DEFAULT_X_MAX = 80
    DEFAULT_Y_MAX = 24

    try:
        if not compatibility_mode:
            X_MAX, Y_MAX = os.get_terminal_size().columns - 1, os.get_terminal_size().lines - 1  # Python 3.3+ is required for this to work
        else:
            X_MAX = DEFAULT_X_MAX
            Y_MAX = DEFAULT_Y_MAX
    except:
        X_MAX = DEFAULT_X_MAX
        Y_MAX = DEFAULT_Y_MAX

    @classmethod # this is called a decorator, it tells Python that the next function is going to be a class method and not an instance method
    def bind(cls, key, func): # allows you to bind specific keys to specific functions in the main program. defined as a class method so that it applies to all menu objects that are created
        # cls references the class as a whole
        cls.bindings[key] = func
        # pressing the key when the main program is running will execute the function

    def __init__(self, title, description="", footer=""):
        # this is the class constructor, it is executed automatically whenever a new Menu object is created.
        # 'self' refers to the unique Menu instance/object as opposed to the class as a whole
        # for example, below there is self.title, self.desc etc, these are the object's attributes

        # 'Menu' refers to the class as a whole. Below I am incrementing the Class' instance number by 1
        # There are also some local variables defined below that are just used temporarily, for example in the get_inputs() function, there is a locally defined list called 'data' that is used to return the inputs

        self.uid = Menu.instance_num # uid = Unique ID, Menu.instance_num = the number of menu instances that have been created since the program was started.
        Menu.instance_num += 1 # increase the instance number

        self.title = title
        self.desc = description
        self.footer = footer

        self.buttons = []
        self.inputs = []
        self.button_index = 0 # stores the index of the button that is currently selected
        self.input_index = 0 # stores the index of the input that is currently selected
        self.line_index = 0 # stores the index of the line of text that is currently selected in a prompt-style menu with no inputs

        self.timeout = 0 # time in seconds that the menu will be displayed for. only works if the value is greater than 0
        self.slow_draw = False # sets a time delay between each draw call

        # some flags that control the type of menu that will be displayed:

        self.is_active = True
        self.is_prompt = False
        self.prompt_msg = ""
        self.is_popup = False

        self.kb_chars = "abcdefghijklmnopqrstuvwxyz,./?!\"\'£;:$%^&*()[]{}@#~/\\<>|-_=+¬`¦1234567890 " # constant list of keyboard characters than can be entered as text

        # constant interface dimensions:

        self.option_width = Menu.X_MAX // 3
        self.option_height = 1
        self.title_x = (Menu.X_MAX // 2) - (len(self.title) // 2)
        self.title_y = 1#(Menu.Y_MAX // 10)
        self.overlay_max_height = (Menu.Y_MAX // 2) + 4

        self.prev_scrollbar_ypos = None # used in the draw_scrollbar function

        self.cursor_x = 0 # unused
        self.cursor_y = 0 # also unused

        self.update_dimensions() # does what it says on the tin

    def set_timeout(self, seconds):
        self.timeout = seconds

    def add_button(self, text, target):
        # Target is a function pointer
        self.buttons.append([text, target])
        #self.prev_b = [text, target]

    def add_input(self, text, default=""):
        self.is_prompt = True
        self.inputs.append([text, default]) # the second element in the list will store keyboard input

    def add_checkbox(self, text, default=False): # add a boolean input that can be toggled by pressing space while it is selected
        self.is_prompt = True
        self.inputs.append([text, default])

    def get_inputs(self):
        data = []
        for i in self.inputs:
            if isinstance(i[1], bool):
                data.append(i[1])
            else:
                data.append(i[1].strip()) # each list in self.inputs has two elements: an input name and the actual user input. Here I am just storing the actual user input in the 'data' list.
        return data

    def clear_inputs(self): # Reset each input
        for inp in self.inputs:
            if isinstance(inp[1], bool):
                inp[1] = False
            else:
                inp[1] = ""

    def set_desc(self, text): # not used in the main program. this just adds an additional line of information at the top of the overlay.
        self.desc = text

    def set_footer(self, text): # sets the line of text that appears at the bottom of the interface
        self.footer = text

    def set_popup(self, value): # value should be a boolean. controls whether or not the menu is a 'popup' (background not drawn, title not drawn etc)
        self.is_popup = value

    def set_program_title(self, text): # sets the program title
        Menu.program_title = text

    def update_dimensions(self):

        # this stuff is very finicky
        # lots of +n and -n everywhere to make the interface look nicer on the screen

        try:
            if not Menu.compatibility_mode:
                Menu.X_MAX, Menu.Y_MAX = os.get_terminal_size().columns - 1, os.get_terminal_size().lines - 1  # Python 3.3+ is required for this to work
            else:
                Menu.X_MAX = Menu.DEFAULT_X_MAX
                Menu.Y_MAX = Menu.DEFAULT_Y_MAX
        except:
            Menu.X_MAX = Menu.DEFAULT_X_MAX
            Menu.Y_MAX = Menu.DEFAULT_Y_MAX

        if self.is_prompt:
            wrapped = self.word_wrapped_text(self.prompt_msg)
            self.overlay_height = len(wrapped) + 4 + int(len(self.inputs) + 0)
            if self.overlay_height > self.overlay_max_height:
                self.overlay_height = self.overlay_max_height

            self.max_vertical_elements = self.overlay_height - 4 # - int(len(self.inputs) + 0)
            if self.max_vertical_elements <= 0:  # no vertical inputs or buttons but possibly text
                self.max_vertical_elements = len(wrapped)

            if len(self.inputs) > 0:
                self.overlay_height += 1
            else:
                #self.max_vertical_elements += 1
                pass

            if not self.is_popup:
                self.overlay_width = int(Menu.X_MAX * 0.8)  # len(wrapped[0]) + 4
            else:
                self.overlay_width = Menu.X_MAX // 2 + self.if_pos(max(list(len(line) for line in wrapped)) - (Menu.X_MAX // 2)) + 4
                self.max_vertical_elements = self.overlay_height - 4

        else:

            if not self.is_popup:
                self.overlay_width = int(Menu.X_MAX * 0.8)
            else:
                self.overlay_width = Menu.X_MAX // 2

            self.overlay_height = Menu.Y_MAX // 2
            self.max_vertical_elements = self.overlay_height - 2

        self.overlay_top = (Menu.Y_MAX // 2) - (self.overlay_height // 2) # top y coord
        self.overlay_left = (Menu.X_MAX // 2) - (self.overlay_width // 2) # leftmost x coord

        self.desc_x = self.overlay_left + 1
        self.desc_y = self.overlay_top

        self.msg_x = self.overlay_left + 1
        self.msg_y = self.overlay_top + 1

        self.input_x = (Menu.X_MAX // 2) - (self.overlay_width // 4)
        if len(self.inputs) > 0:
            self.input_x = (Menu.X_MAX // 2) - (self.overlay_width // 4) - (max(list(len(i[0]) for i in self.inputs)) // 4)
            self.input_y = (self.overlay_top + (self.overlay_height // 4))# - (len(self.inputs) // 2)

    def if_pos(self, n):
        # if n is positive, return it. Otherwise return 0.
        if n > 0:
            return n
        else:
            return 0

    def draw_menu(self):

        if not self.is_active:
            return

        Menu.menu_being_displayed = self.uid

        self.update_dimensions()

        # ===== Draw the background
        if not self.is_popup:
            for y in range(1, Menu.Y_MAX + 1):
                if self.slow_draw:
                    time.sleep(0.1)
                draw(1, y, Menu.outer_bg + " " * Menu.X_MAX)

        if self.slow_draw:
            time.sleep(0.5)

        if not self.is_popup:
            # ===== Draw the footer text
            draw(1, Menu.Y_MAX, Menu.outer_bg + Menu.outer_fg + Menu.outer_style + self.footer)

        if self.slow_draw:
            time.sleep(0.5)

        if not self.is_popup:
            self.draw_menu_title()

        if self.slow_draw:
            time.sleep(0.5)

        if not self.is_popup:
            self.draw_program_title()

        if self.slow_draw:
            time.sleep(0.5)
        self.draw_overlay()

        if self.slow_draw:
            time.sleep(0.5)
        self.draw_prompt()

        if self.slow_draw:
            time.sleep(0.5)
        self.draw_buttons()

        if self.slow_draw:
            time.sleep(0.5)
        self.draw_inputs()

        if self.slow_draw:
            time.sleep(0.5)
        self.draw_debug_message()

    def draw_debug_message(self):
        if Menu.draw_debug_messages:
            if Menu.debug_message:
                draw(1, Menu.Y_MAX - 1, Menu.debug_bg + Menu.debug_fg + Menu.debug_style + Menu.debug_message)
            if self.button_index < 10:
                bttn_index = str(self.button_index) + " "
            else:
                bttn_index = str(self.button_index)
            if self.input_index < 10:
                input_index = str(self.input_index) + " "
            else:
                input_index = str(self.input_index)
            if self.uid < 10:
                menu_index = str(self.uid) + " "
            else:
                menu_index = str(self.uid)
            draw(1, Menu.Y_MAX - 2, Menu.debug_bg + Menu.debug_fg + Menu.debug_style + "button_index: " + bttn_index)
            draw(1, Menu.Y_MAX - 3, Menu.debug_bg + Menu.debug_fg + Menu.debug_style + "input_index: " + input_index)
            draw(1, Menu.Y_MAX - 4, Menu.debug_bg + Menu.debug_fg + Menu.debug_style + "menu_id: " + menu_index)

    def draw_program_title(self):
        draw(Menu.X_MAX // 2 - len(Menu.program_title) // 2, 1,
             Menu.outer_bg + Menu.outer_fg + Menu.outer_style + Menu.program_title)

    def draw_menu_title(self):
        # ===== Draw the menu title at the top
        title_x = (Menu.X_MAX // 2) - (len(self.title) // 2)
        title_y = (Menu.Y_MAX // 10)
        draw(1, title_y - 1, Menu.outer_bg + Menu.outer_fg + Menu.outer_style + "─" * Menu.X_MAX)
        draw(title_x, title_y, Menu.outer_bg + Menu.outer_fg + Menu.outer_style + self.title)
        draw(1, title_y + 1, Menu.outer_bg + Menu.outer_fg + Menu.outer_style + "─" * Menu.X_MAX)

    def draw_overlay(self):
        self.update_dimensions()

        # ===== Draw the menu overlay
        for y in range(self.overlay_top, self.overlay_top + self.overlay_height):
            if self.slow_draw:
                time.sleep(0.1)
            draw(self.overlay_left, y, Menu.overlay_bg + " " * self.overlay_width)

        if not self.is_popup:
            # ===== Draw the menu overlay shadow
            for y in range(self.overlay_top + 1, self.overlay_top + self.overlay_height):
                if self.slow_draw:
                    time.sleep(0.1)
                draw(self.overlay_left + self.overlay_width, y, Menu.shadow_bg + " ")
            #for x in range(self.overlay_left + 1, self.overlay_left + self.overlay_width + 1):
                #draw(x, self.overlay_top + self.overlay_height, Back.BLACK + " ")
            draw(self.overlay_left + 1, self.overlay_top + self.overlay_height, Menu.shadow_bg + " " * self.overlay_width)

        # Draw fancy menu stuff
        for x in range(self.overlay_left + 1, self.overlay_left + self.overlay_width):
            draw(x, self.overlay_top + self.overlay_height - 1, Menu.accent_bg + Menu.accent_fg + Menu.accent_style + "─")
            draw(x, self.overlay_top, Menu.accent_bg + Menu.accent_fg + Menu.accent_alt_style + "─")
        for y in range(self.overlay_top + 1, self.overlay_top + self.overlay_height - 1):
            draw(self.overlay_left + self.overlay_width - 1, y, Menu.accent_bg + Menu.accent_fg + Menu.accent_style + "│")
            draw(self.overlay_left, y, Menu.accent_bg + Menu.accent_fg + Menu.accent_alt_style + "│")
            draw(self.overlay_left + self.overlay_width - 1, self.overlay_top + self.overlay_height - 1,
                 Menu.accent_bg + Menu.accent_fg + Menu.accent_style + "┘")
        draw(self.overlay_left + self.overlay_width - 1, self.overlay_top, Menu.accent_bg + Menu.accent_fg + Menu.accent_style + "┐")
        draw(self.overlay_left, self.overlay_top + self.overlay_height - 1, Menu.accent_bg + Menu.accent_fg + Menu.accent_alt_style + "└")
        draw(self.overlay_left, self.overlay_top, Menu.accent_bg + Menu.accent_fg + Menu.accent_alt_style + "┌")

        # Draw the description at the top of the overlay box
        if len(self.desc) > self.overlay_width:
            half = len(self.desc.split()) // 2
            first_line = " ".join(word for word in self.desc.split()[:half])
            second_line = " ".join(word for word in self.desc.split()[half:])
            draw(self.desc_x, self.desc_y, Menu.desc_bg + Menu.desc_fg + Menu.desc_style + first_line)
            draw(self.desc_x, self.desc_y, Menu.desc_bg + Menu.desc_fg + Menu.desc_style + second_line)
        else:
            draw(self.desc_x, self.desc_y, Menu.desc_bg + Menu.desc_fg + Menu.desc_style + self.desc)

    def draw_prompt(self):
        lines_drawn = 0
        wrapped = self.word_wrapped_text(self.prompt_msg)

        # print(wrapped)
        # print(self.max_vertical_elements)
        # input()

        if len(wrapped) > self.max_vertical_elements:
            if self.line_index > self.max_vertical_elements - 1:
                lines_visible = wrapped[self.line_index - (self.max_vertical_elements - 1):self.line_index + 1]
            else:
                lines_visible = wrapped[:self.max_vertical_elements]
        else:
            lines_visible = wrapped

        self.draw_scrollbar(wrapped, self.line_index)

        for i, line in enumerate(lines_visible):
            if self.slow_draw:
                time.sleep(0.1)
            draw(self.msg_x, self.msg_y + i, Menu.overlay_bg + " " * int(self.overlay_width - 4))
            draw(self.msg_x, self.msg_y + i, Menu.overlay_bg + Menu.overlay_fg + Menu.overlay_style + line)

    def draw_buttons(self):  # Redraw only the menu buttons

        self.update_dimensions()
        options_drawn = 0

        if len(self.buttons) == 0:
            return

        if not self.is_prompt:
            if len(self.buttons) > self.max_vertical_elements:
                if self.button_index > self.max_vertical_elements - 1:
                    buttons_visible = self.buttons[self.button_index - (self.max_vertical_elements - 1):self.button_index+1]
                else:
                    buttons_visible = self.buttons[:self.max_vertical_elements]
            else:
                buttons_visible = self.buttons
        else:
            buttons_visible = self.buttons

        #if not self.is_prompt:
            #print(buttons_visible)
            #self.title=str(list(self.buttons.index(b) for b in buttons_visible))
            #self.draw_menu_title()

        if not self.is_prompt and len(self.buttons) > self.max_vertical_elements:
            self.draw_scrollbar(self.buttons, self.button_index)

        for i, b in enumerate(buttons_visible):

            text = b[0]

            if self.is_prompt:
                bx = self.overlay_left + ((self.overlay_width // (len(buttons_visible) + 1)) * (i + 1)) - (len(text) // 2)
                by = self.overlay_top + self.overlay_height - 2
            else:
                bx = (Menu.X_MAX // 2) - (len(text) // 2)
                by = (Menu.Y_MAX // 2 - (len(buttons_visible) // 2) + options_drawn)
                if not self.timeout:
                    draw((Menu.X_MAX // 2) - (max(list(len(bttn[0]) for bttn in self.buttons)) // 2), by, Menu.overlay_bg + " " * (max(list(len(bttn[0]) for bttn in self.buttons))))
                    draw(self.overlay_left + 1, by, Menu.overlay_bg + " " * 4)

            #self.prev_text = list(bttn[0] for bttn in buttons_visible)
            self.prev_b = b
            options_drawn += 1

            if self.buttons.index(b) == self.button_index:
                if not self.is_prompt and not self.timeout:
                    draw(self.overlay_left + 1, by, Menu.overlay_bg + Menu.overlay_fg + Menu.overlay_style + "(" + str(self.buttons.index(b) + 1) + ")")
                draw(bx, by, Menu.selected_bg + Menu.selected_fg + Menu.selected_style + text)
            else:
                if not self.is_prompt and not self.timeout:
                    draw(self.overlay_left + 1, by, Menu.overlay_bg + Menu.overlay_fg + Menu.overlay_style + "(" + str(self.buttons.index(b) + 1) + ")")
                draw(bx, by, Menu.overlay_bg + Menu.overlay_fg + Menu.overlay_style + text)

    def draw_scrollbar(self, elements, element_index):
        if len(elements) > self.max_vertical_elements:
            draw(self.overlay_left + self.overlay_width - 3, self.overlay_top + 1,
                 Menu.overlay_bg + Menu.overlay_fg + Menu.overlay_style + "/\\")

            # if not self.prev_scrollbar_ypos:
            #     for y in range(self.overlay_top + 2, self.overlay_top + self.overlay_height - 2):
            #         draw(self.overlay_left + self.overlay_width - 3, y,
            #              Menu.overlay_bg + Menu.overlay_fg + Menu.overlay_style + "▒▒")  ██

            if elements == self.word_wrapped_text(self.prompt_msg):

                element_index = self.line_index - self.max_vertical_elements + 1
                scroll_info = "({}/{})".format(self.zero_pad(element_index + 1), self.zero_pad(len(elements) - self.max_vertical_elements + 1))
                elements = elements[self.max_vertical_elements - 1:]
                #print(self.line_index)
                #input()
            else:
                scroll_info = "({}/{})".format(self.zero_pad(element_index + 1), self.zero_pad(len(elements)))
            scroll_percentage = element_index / (len(elements) - 1) # calculate the position of the selected option relative to the rest of the options as a percentage
            if scroll_percentage > 1:
                scroll_percentage = 1
            elif scroll_percentage < 0:
                scroll_percentage = 0
            scrollbar_yvalues = list(range(self.overlay_top + 2, self.overlay_top + self.overlay_height - 2)) # get a list of the scrollbar's Y values on the interface
            scroll_index = int((len(scrollbar_yvalues)-1) * scroll_percentage) # find the scrollbar's Y coordinate's approximate index using the percentage that we just calculated
            scrollbar_ypos = scrollbar_yvalues[scroll_index] # obtain the correct Y value using the scroll_index
            draw(self.overlay_left + self.overlay_width - 3, scrollbar_ypos,
                 Menu.overlay_bg + Menu.overlay_fg + Menu.overlay_style + "██")
            if self.prev_scrollbar_ypos != scrollbar_ypos and self.prev_scrollbar_ypos != None:
                draw(self.overlay_left + self.overlay_width - 3, self.prev_scrollbar_ypos,
                    Menu.overlay_bg + Menu.overlay_fg + Menu.overlay_style + "  ")
            draw(self.overlay_left + self.overlay_width - 3, self.overlay_top + self.overlay_height - 2,
                 Menu.overlay_bg + Menu.overlay_fg + Menu.overlay_style + "\/")
            self.prev_scrollbar_ypos = scrollbar_ypos

            draw(self.overlay_left + self.overlay_width - len(scroll_info), self.overlay_top + self.overlay_height - 1, Menu.overlay_bg + Menu.overlay_fg + Menu.overlay_style + scroll_info)

    def zero_pad(self, n):
        # add a leading zero if n is less than 10
        if n < 10:
            return "0" + str(n)
        else:
            return str(n)

    def draw_inputs(self):

        self.update_dimensions()
        selected_index = None
        inputs_drawn = 0

        if len(self.inputs) == 0:
            return

        if len(self.inputs) > self.max_vertical_elements:
            if self.input_index > self.max_vertical_elements - 1:
                inputs_visible = self.inputs[self.input_index - (self.max_vertical_elements - 1):self.input_index + 1]
            else:
                inputs_visible = self.inputs[:self.max_vertical_elements]
        else:
            inputs_visible = self.inputs

        #self.title = str(list(self.inputs.index(i) for i in inputs_visible))
        #self.draw_menu_title()

        self.draw_scrollbar(self.inputs, self.input_index)

        for i, inp in enumerate(inputs_visible):
            text = inp[0]
            inpy = (Menu.Y_MAX // 2 - (len(inputs_visible) // 2))
            inputs_drawn += 1

            draw(self.overlay_left + 1, inpy + inputs_drawn - 1, Menu.overlay_bg + " " * (self.overlay_width - 4))

            if self.inputs.index(inp) == self.input_index:
                selected_index = inputs_drawn
                selected_text = text
                selected_input = inp[1]
                draw(self.input_x, inpy + inputs_drawn - 1, Menu.selected_bg + Menu.selected_fg + Menu.selected_style + text)
            else:
                draw(self.input_x, inpy + inputs_drawn - 1, Menu.overlay_bg + Menu.overlay_fg + Menu.overlay_style + text)



            if "password" not in text.lower():
                if isinstance(inp[1], bool):
                    if inp[1] == True:
                        draw(self.input_x + len(text) + 1, inpy + inputs_drawn - 1, Menu.input_bg + Menu.input_fg + Menu.input_style + "[X]")
                    else:
                        draw(self.input_x + len(text) + 1, inpy + inputs_drawn - 1, Menu.input_bg + Menu.input_fg + Menu.input_style + "[ ]")
                else:
                    draw(self.input_x + len(text) + 1, inpy + inputs_drawn - 1, Menu.input_bg + Menu.input_fg + Menu.input_style + inp[1])
            else:  # obfuscate password input fields
                draw(self.input_x + len(text) + 1, inpy + inputs_drawn - 1, Menu.input_bg + Menu.input_fg + Menu.input_style + "*" * len(inp[1]))

        if selected_index != None:
            if "password" not in selected_text.lower():
                if not isinstance(selected_input, bool):
                    draw(self.input_x + len(selected_text) + 1, inpy + selected_index - 1, Menu.input_bg + Menu.input_fg + Menu.input_style + selected_input)
            else:
                draw(self.input_x + len(selected_text) + 1, inpy + selected_index - 1, Menu.input_bg + Menu.input_fg + Menu.input_style + "*" * len(selected_input))

    def move_down_button(self):
        if len(self.buttons) > 1:
            if self.button_index >= len(self.buttons) - 1:
                self.button_index = 0
            else:
                self.button_index += 1

    def move_up_button(self):
        if len(self.buttons) > 1:
            if self.button_index <= 0:
                self.button_index = len(self.buttons) - 1
            else:
                self.button_index -= 1

    def move_down_input(self):
        if len(self.inputs) > 1:
            if self.input_index >= len(self.inputs) - 1:
                self.input_index = 0
            else:
                self.input_index += 1

    def move_up_input(self):
        if len(self.inputs) > 1:
            if self.input_index <= 0:
                self.input_index = len(self.inputs) - 1
            else:
                self.input_index -= 1

    def move_down_line(self):
        lines = len(self.word_wrapped_text(self.prompt_msg))
        if lines > 1:
            if self.line_index > lines - 2:
                if lines > self.max_vertical_elements:
                    self.line_index = self.max_vertical_elements - 1
                else:
                    self.line_index = lines - 1
            else:
                self.line_index += 1

    def move_up_line(self):
        lines = len(self.word_wrapped_text(self.prompt_msg))
        if lines > 1:

            if lines > self.max_vertical_elements:
                if self.line_index < self.max_vertical_elements:# - 1:
                    self.line_index = lines - 1
                else:
                    self.line_index -= 1
            else:
                self.line_index = lines - 1

    def start(self):
        if self.timeout:
            self.draw_buttons()
            time.sleep(self.timeout)
            self.quit()

        lines = len(self.word_wrapped_text(self.prompt_msg))
        if lines > self.max_vertical_elements:
            self.line_index = self.max_vertical_elements + 1
        else:
            self.line_index = lines - 1

        self.draw_menu()

        while self.is_active:

            try:
                if not Menu.compatibility_mode and [Menu.X_MAX, Menu.Y_MAX] != [os.get_terminal_size().columns - 1, os.get_terminal_size().lines - 1]:
                    self.draw_menu()
            except:
                pass

            if self.uid != Menu.menu_being_displayed:
                self.draw_menu()
                Menu.menu_being_displayed = self.uid

            if msvcrt.kbhit(): # This section deals with all of the keyboard input stuff
                key = ord(msvcrt.getch())

                if key == 13: # enter key
                    f = self.buttons[self.button_index][1] # get the function that is linked to the selected button
                    f() # execute the function

                elif key == 27: # escape
                    self.quit() # close the current menu

                elif key == 0: # function key
                    key = ord(msvcrt.getch())
                    if key == 63:  # F5
                        self.draw_menu()
                        continue
                    elif key in list(Menu.bindings.keys()):
                        Menu.bindings[key]()
                        continue

                if not self.is_prompt: # ie the menu has its buttons arranged vertically
                    if key == 224: # arrow key
                        key = ord(msvcrt.getch())
                        if key == 80: # down
                            self.move_down_button()
                            self.draw_buttons()
                        elif key == 72: # up
                            self.move_up_button()
                            self.draw_buttons()
                    elif key == 9: # tab
                        self.move_down_button()
                        self.draw_buttons()
                else:
                    if key == 224:  # arrow key
                        key = ord(msvcrt.getch())
                        if key == 75:  # left
                            self.move_up_button()
                            self.draw_buttons()
                        elif key == 77:  # right
                            self.move_down_button()
                            self.draw_buttons()
                        if len(self.inputs) > 0:
                            if key == 80: # down or tab
                                self.move_down_input()
                                self.draw_inputs()
                            elif key == 72: # up
                                self.move_up_input()
                                self.draw_inputs()
                        elif len(self.word_wrapped_text(self.prompt_msg)) > self.max_vertical_elements:
                            if key == 80: # down or tab
                                self.move_down_line()
                                self.draw_prompt()
                            elif key == 72: # up
                                self.move_up_line()
                                self.draw_prompt()
                        self.draw_inputs()
                    elif str(chr(key)).lower() in self.kb_chars and len(self.inputs) > 0:
                        if isinstance(self.inputs[self.input_index][1], bool) and key == 32:
                            self.inputs[self.input_index][1] = not self.inputs[self.input_index][1]
                            self.draw_inputs()
                        elif not isinstance(self.inputs[self.input_index][1], bool) and self.input_x + len(self.inputs[self.input_index][1]) + len(self.inputs[self.input_index][0]) + 1 < self.overlay_left + self.overlay_width - 3:
                            char = str(chr(key))
                            self.inputs[self.input_index][1] += char
                            self.draw_inputs()
                    elif key == 8: # backspace (this code removes characters by drawing a space over them)
                        if len(self.inputs) > 0:
                            if not isinstance(self.inputs[self.input_index][1], bool) and len(self.inputs[self.input_index][1]) > 0:
                                self.inputs[self.input_index][1] = self.inputs[self.input_index][1][:-1]

                                x = (Menu.X_MAX // 2) - (self.overlay_width // 4) - (
                                    max(list(len(i[0]) for i in self.inputs)) // 4) + len(self.inputs[self.input_index][1]) + len(self.inputs[self.input_index][0]) + 1
                                if self.input_index > self.max_vertical_elements - 2: # THIS IS BROKEN
                                    y = self.input_y + (self.input_index - self.max_vertical_elements)
                                else:
                                    y = self.input_y + self.input_index
                                draw(x, y, Menu.overlay_bg + " ")

                                self.draw_inputs()
                    elif key == 9: # tab
                        self.move_down_input()
                        self.draw_inputs()
                self.draw_debug_message()

        self.is_active = True # this line is required for menus to be 'restarted' after they have been closed

    def quit(self):
        self.is_active = False

    def add_text(self, text):
        self.is_prompt = True
        self.prompt_msg += text + r"\n" # word_wrapped_text() handles the newline stuff

    def set_prompt(self, msg):
        self.is_prompt = True
        self.prompt_msg = msg

    def word_wrapped_text(self, text):
        wrapped_lines = []
        line = ""
        n_words = len(text.split(" "))

        if len(text.split(r"\n")) > 1:
            for words in text.split(r"\n"):
                wrapped_lines.append(words)
        else:
            for i, word in enumerate(text.split()):
                if len(line + " " + word) >= self.overlay_width - 3:
                    wrapped_lines.append(line)
                    line = word
                else:
                    if not line:
                        line = word
                    else:
                        line += " " + word
                if i + 1 == n_words:
                    wrapped_lines.append(line)

        return wrapped_lines
        #return list(line for line in wrapped_lines if line.strip() != "")

        # for each word in the text
        # if the line + a space + the word is too long
        # place the word on a new line
        # otherwise add the space + word to the end of the line
