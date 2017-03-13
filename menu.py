from colorama import *
from colorama_utils import *
import msvcrt, time, os
init()

class Menu:

    compatibility_mode = True # when enabled: maintains a 80x24 screen size. may cause interface scaling issues if disabled

    version = "0.8"

    ctime = time.time() # current time, updates whenever a new menu is created.

    instance_num = 0
    menu_being_displayed = 0 # the id of the menu which is currently being displayed

    staffid = ""
    program_title = "Morriston Manufacturing and Logistics"
    debug_message = ""

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

    #X_MAX = 119
    #Y_MAX = 30

    try:
        if not compatibility_mode:
            X_MAX, Y_MAX = os.get_terminal_size().columns - 1, os.get_terminal_size().lines - 1  # Python 3.3+ is required for this to work
        else:
            X_MAX = 80
            Y_MAX = 24
    except:
        X_MAX = 80 # 80x24 is the smallest terminal size that is still in use today, i'm using it here for compatibility reasons.
        Y_MAX = 24

    def __init__(self, title, description="", footer="[Arrow Keys - Select] [Enter - Activate] [Space - Toggle Checkbox] [F1 - Redraw]"):
        self.uid = Menu.instance_num
        Menu.instance_num += 1

        Menu.ctime = time.time()

        self.title = title
        self.desc = description
        self.footer = footer

        self.buttons = []
        self.inputs = []
        self.button_index = 0 # stores the index of the button that is currently selected
        self.input_index = 0 # stores the index of the input that is currently selected

        self.timeout = 0
        self.slow_draw = False

        self.is_active = True
        self.is_prompt = False
        self.prompt_msg = ""
        self.is_popup = False

        self.kb_chars = "abcdefghijklmnopqrstuvwxyz,./?!\"\'£;:$%^&*()[]{}@#~/\\<>|-_=+¬`¦1234567890 "

        self.option_width = Menu.X_MAX // 3
        self.option_height = 1
        self.title_x = (Menu.X_MAX // 2) - (len(self.title) // 2)
        self.title_y = 1#(Menu.Y_MAX // 10)

        self.cursor_x = 0
        self.cursor_y = 0

        self.update_dimensions()

    def set_timeout(self, seconds):
        self.timeout = seconds

    def add_button(self, text, target):
        # Target is a function pointer
        self.buttons.append([text, target])

    def add_input(self, text, default=""):
        self.is_prompt = True
        self.inputs.append([text, default]) # the second element in the list will store keyboard input

    def add_checkbox(self, text, default=False): # add a boolean input that can be toggled by pressing space while it is selected
        self.is_prompt = True
        self.inputs.append([text, default])

    def get_inputs(self):
        data = []
        for i in self.inputs:
            data.append(i[1])
        return data

    def clear_inputs(self):
        for inp in self.inputs:
            if isinstance(inp[1], bool):
                inp[1] = False
            else:
                inp[1] = ""

    def set_desc(self, text):
        self.desc = text

    def set_footer(self, text):
        self.footer = text

    def set_popup(self):
        self.is_popup = True

    def set_program_title(self, text):
        Menu.program_title = text

    def update_dimensions(self):

        try:
            if not Menu.compatibility_mode:
                Menu.X_MAX, Menu.Y_MAX = os.get_terminal_size().columns - 1, os.get_terminal_size().lines - 1  # Python 3.3+ is required for this to work
            else:
                Menu.X_MAX = 80
                Menu.Y_MAX = 24
        except:
            Menu.X_MAX = 80
            Menu.Y_MAX = 24

        if self.is_prompt:
            wrapped = self.word_wrapped_text(self.prompt_msg)
            self.overlay_height = len(wrapped) + 4 + int(len(self.inputs) + 0)
            if len(self.inputs) > 0:
                self.overlay_height += 1

            if not self.is_popup:
                self.overlay_width = int(Menu.X_MAX * 0.8)  # len(wrapped[0]) + 4
            else:
                self.overlay_width = Menu.X_MAX // 2
        else:
            if not self.is_popup:
                self.overlay_width = int(Menu.X_MAX * 0.8)
            else:
                self.overlay_width = Menu.X_MAX // 2
            self.overlay_height = Menu.Y_MAX // 2

        self.overlay_top = (Menu.Y_MAX // 2) - (self.overlay_height // 2) # top y coord
        self.overlay_left = (Menu.X_MAX // 2) - (self.overlay_width // 2) # leftmost x coord

        self.desc_x = self.overlay_left + 1
        self.desc_y = self.overlay_top

        self.msg_x = self.overlay_left + 1
        self.msg_y = self.overlay_top + 1

        self.input_x = (Menu.X_MAX // 2) - (self.overlay_width // 4)
        if len(self.inputs) > 0:
            self.input_x = (Menu.X_MAX // 2) - (self.overlay_width // 4) - (max(list(len(i[0]) for i in self.inputs)) // 4)
            self.input_y = (self.overlay_top + (self.overlay_height // 2)) - (len(self.inputs) // 2)

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
        self.draw_buttons()

        if self.slow_draw:
            time.sleep(0.5)
        self.draw_inputs()

        if self.slow_draw:
            time.sleep(0.5)
        self.draw_debug_message()

    def draw_debug_message(self):
        if Menu.debug_message:
            draw(1, Menu.Y_MAX - 1, Menu.debug_bg + Menu.debug_fg + Menu.debug_style + Menu.debug_message)
            draw(1, Menu.Y_MAX - 2, Menu.debug_bg + Menu.debug_fg + Menu.debug_style + "button_index: " + str(self.button_index))
            draw(1, Menu.Y_MAX - 3, Menu.debug_bg + Menu.debug_fg + Menu.debug_style + "input_index: " + str(self.input_index))
            draw(1, Menu.Y_MAX - 4, Menu.debug_bg + Menu.debug_fg + Menu.debug_style + "menu_id: " + str(self.uid))

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

        # ===== Draw session username
        staffid = Menu.staffid
        if staffid:
            draw(1, title_y, Menu.outer_bg + Menu.outer_fg + Menu.outer_style + "Staff ID: " + staffid)

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

        if self.is_prompt:
            wrapped = self.word_wrapped_text(self.prompt_msg)
            for i, line in enumerate(wrapped):
                if self.slow_draw:
                    time.sleep(0.1)
                draw(self.msg_x, self.msg_y + i,
                     Menu.overlay_bg + Menu.overlay_fg + Menu.overlay_style + line)


    def draw_buttons(self):  # Redraw only the menu buttons
        self.update_dimensions()

        options_drawn = 0
        for index, option in enumerate(self.buttons):
            if self.slow_draw:
                time.sleep(0.1)
            text = self.buttons[index][0]

            if self.is_prompt:
                option_x = self.overlay_left + ((self.overlay_width // (len(self.buttons) + 1)) * (index + 1)) - (
                    len(text) // 2)  # (Menu.X_MAX // 2) - (len(text) // 2)  # In the middle
                option_y = self.overlay_top + self.overlay_height - 2
            else:
                option_x = (Menu.X_MAX // 2) - (len(text) // 2)  # In the middle
                option_y = (Menu.Y_MAX // 2 - (len(self.buttons) // 2) + options_drawn)

            box_x = (Menu.X_MAX // 2) - (self.overlay_width // 2)
            options_drawn += 1

            if index == self.button_index:
                if not self.is_prompt and not self.timeout:
                    draw(box_x + 1, option_y,
                         Menu.selected_bg + Menu.selected_fg + Menu.selected_style + "(" + str(
                                 index + 1) + ")")
                draw(option_x, option_y, Menu.selected_bg + Menu.selected_fg + Menu.selected_style + text)
            else:
                if not self.is_prompt and not self.timeout:
                    draw(box_x + 1, option_y,
                         Menu.overlay_bg + Menu.overlay_fg + Menu.overlay_style + "(" + str(index + 1) + ")")
                draw(option_x, option_y, Menu.overlay_bg + Menu.overlay_fg + Menu.overlay_style + text)

    def draw_inputs(self):
        self.update_dimensions()

        inputs_drawn = 0
        for index, inp in enumerate(self.inputs):
            if self.slow_draw:
                time.sleep(0.1)
            text = self.inputs[index][0]

            inputs_drawn += 1

            if index == self.input_index:
                draw(self.input_x, self.input_y + inputs_drawn - 1, Menu.selected_bg + Menu.selected_fg + Menu.selected_style + text)
            else:
                draw(self.input_x, self.input_y + inputs_drawn - 1, Menu.overlay_bg + Menu.overlay_fg + Menu.overlay_style + text)

            if "password" not in inp[0].lower():
                if isinstance(inp[1], bool):
                    if inp[1] == True:
                        draw(self.input_x + len(text) + 1, self.input_y + inputs_drawn - 1,
                         Menu.input_bg + Menu.input_fg + Menu.input_style + "[X]")
                    else:
                        draw(self.input_x + len(text) + 1, self.input_y + inputs_drawn - 1,
                             Menu.input_bg + Menu.input_fg + Menu.input_style + "[ ]")


                else:
                    draw(self.input_x + len(text) + 1, self.input_y + inputs_drawn - 1, Menu.input_bg + Menu.input_fg + Menu.input_style + inp[1])
            else: # obfuscate password input fields
                draw(self.input_x + len(text) + 1, self.input_y + inputs_drawn - 1,
                     Menu.input_bg + Menu.input_fg + Menu.input_style + "*"*len(inp[1]))

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

    def start(self):
        if self.timeout:
            self.draw_buttons()
            time.sleep(self.timeout)
            self.quit()

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
                    if key == 59:  # F1
                        self.draw_menu()
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
                    elif str(chr(key)).lower() in self.kb_chars and len(self.inputs) > 0:
                        if isinstance(self.inputs[self.input_index][1], bool) and key == 32:
                            self.inputs[self.input_index][1] = not self.inputs[self.input_index][1]
                            self.draw_inputs()
                        elif not isinstance(self.inputs[self.input_index][1], bool) and self.input_x + len(self.inputs[self.input_index][1]) + len(self.inputs[self.input_index][0]) + 1 < self.overlay_left + self.overlay_width - 2:
                            char = str(chr(key))
                            self.inputs[self.input_index][1] += char
                            self.draw_inputs()
                    elif key == 8: # backspace (this code removes characters by drawing a space over them)
                        if not isinstance(self.inputs[self.input_index][1], bool) and len(self.inputs[self.input_index][1]) > 0:
                            self.inputs[self.input_index][1] = self.inputs[self.input_index][1][:-1]

                            x = (Menu.X_MAX // 2) - (self.overlay_width // 4) - (
                                max(list(len(i[0]) for i in self.inputs)) // 4) + len(self.inputs[self.input_index][1]) + len(self.inputs[self.input_index][0]) + 1
                            y = self.input_y + self.input_index
                            draw(x, y, Menu.overlay_bg + " ")

                            self.draw_inputs()
                    elif key == 9: # tab
                        self.move_down_input()
                        self.draw_inputs()
                self.draw_debug_message()

        self.is_active = True

    def quit(self):
        self.is_active = False

    def add_text(self, text):
        self.is_prompt = True
        self.prompt_msg += text + r"\n"

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
                if len(line + " " + word) >= self.overlay_width - 2:
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

        # for each word in the text
        # if the line + a space + the word is too long
        # place the word on a new line
        # otherwise add the space + word to the end of the line