from colorama import init, Fore, Back, Style
import msvcrt, os

# A Python Framework for the Creation of Text-Based Menu Interfaces
# Created and developed by Sam Scott, aged 17 years and 7 months
# 13-10-2016

# GitHub Repo: https://github.com/Nytra/py-menu
# Here you'll be able to find all of the latest updates as soon as they're available

init(autoreset=True)

class Menu:

    prog_title = "PyMenu V0.94a"

    overlay_bg = Back.WHITE
    overlay_fg = Fore.BLACK
    overlay_style = Style.NORMAL

    outer_bg = Back.BLUE
    outer_fg = Fore.WHITE
    outer_style = Style.BRIGHT

    def __init__(self, title="", desc="", footer_text="Use the arrow keys to highlight an option and then press enter to select it."):
        self.options = []

        self.msg_style = Style.NORMAL

        self.shadow_bg = Back.BLACK
        self.shadow_fg = Fore.WHITE
        self.shadow_style = Style.BRIGHT

        self.option_style = Style.NORMAL

        self.selected_bg = Back.BLUE
        self.selected_fg = Fore.WHITE
        self.selected_style = Style.BRIGHT

        self.title_fg = Fore.WHITE
        self.title_style = Style.BRIGHT

        self.footer_fg = Fore.WHITE
        self.footer_style = Style.BRIGHT

        self.desc_style = Style.NORMAL
        self.desc_fg = Fore.BLUE

        self.accent_fg = Fore.WHITE
        self.accent_style = Style.BRIGHT

        self.title = title # The menu title

        self.footer_text = footer_text

        self.selected = 0 # The index of the option that is currently selected
        self.desc = desc # A simple description of the menu
        self.alive = True

        self.ok_dialog = False
        self.text_box = False
        self.dialog_msg = ""
        #self.buffer = "" # keyboard buffer

        self.get_kb_input = False

        self.lines = [] # used for the text editor

        self.update_dimensions()

        self.cursor_x = self.msg_x
        self.cursor_y = self.msg_y

    def set_program_title(self, name):
        Menu.prog_title = name

    def update_dimensions(self):

        self.outer_bg = Menu.outer_bg
        self.outer_fg = Menu.outer_fg
        self.outer_style = Menu.outer_style
        self.overlay_bg = Menu.overlay_bg
        self.overlay_fg = Menu.overlay_fg
        self.overlay_style = Menu.overlay_style

        # Get the latest terminal dimensions

        #self.X_MAX, self.Y_MAX = shutil.get_terminal_size((80, 20)).columns, shutil.get_terminal_size((80, 20)).lines + 1
        self.X_MAX, self.Y_MAX = os.get_terminal_size().columns, os.get_terminal_size().lines + 1

        #os.system('mode con: cols=%d lines=%d' % (self.X_MAX, self.Y_MAX))

        self.option_width = self.X_MAX // 3
        self.option_height = 1

        if self.ok_dialog:
            wrapped = self.word_wrapped_text(self.dialog_msg)
            self.overlay_height = len(wrapped) + 4
            self.overlay_width = self.X_MAX // 2  # len(wrapped[0]) + 4
            # for line in wrapped:
            # if len(line) > self.overlay_width - 2:
            # self.overlay_width = len(line) + 2
        elif self.text_box:
            self.overlay_width = self.X_MAX - 8
            self.overlay_height = self.Y_MAX - 10
        else:
            self.overlay_width = self.X_MAX // 2
            self.overlay_height = self.Y_MAX // 2

        self.overlay_top = (self.Y_MAX // 2) - (self.overlay_height // 2) # top y coord
        self.overlay_bottom = self.overlay_top + self.overlay_height # bottom y coord

        self.overlay_left = (self.X_MAX // 2) - (self.overlay_width // 2) # leftmost x coord
        #self.overlay_right = self.X_MAX - (self.overlay_width // 2) # rightmost x coord
        self.overlay_right = self.overlay_left + self.overlay_width

        self.title_x = (self.X_MAX // 2) - (len(self.title) // 2)
        self.title_y = (self.Y_MAX // 10)

        self.desc_x = self.overlay_left + 1#self.overlay_right - (self.overlay_width // 2) - (len(self.desc) // 2)#(self.X_MAX // 2) - (len(self.desc) // 2)
        self.desc_y = self.overlay_top #// 2 + self.title_y // 2

        self.msg_x = self.overlay_left + 1
        self.msg_y = self.overlay_top + 1

        #self.buffer = []
        #for y in range(self.overlay_top + 1, self.overlay_bottom - 2):
            #self.buffer.append([0]*self.overlay_width-2)

    def add(self, text, target):

        # Target is a function pointer
        self.options.append([text,target])

    def put(self, coords, text):

        # Generate the ANSI code for placing text at position x,y
        x,y = coords 
        pos = lambda x,y: '\x1b[%d;%dH' % (y,x)

        # Display the text at position x,y
        print(pos(x,y) + text, end = "")

    def redraw(self): # redraw the whole menu

        if not self.alive:
            return

        self.update_dimensions()

        for y in range(1, self.Y_MAX):
            #for x in range(1, self.X_MAX):
            self.put([1,y], self.outer_bg + " " * (self.X_MAX - 1))

        self.draw_overlay()
        self.draw_buttons()

    def draw_overlay(self): # redraw only the menu overlay and skip the outer background
        self.update_dimensions()

        # Draw the menu title at the top
        self.put([self.title_x, self.title_y], self.outer_bg + self.title_fg + self.title_style + self.title)

        # Draw the white overlay background
        for y in range(self.overlay_top, self.overlay_bottom):
            #for x in range(self.overlay_left, self.overlay_right):
            self.put([self.overlay_left, y], self.overlay_bg + " " * self.overlay_width)

        # Draw the overlay shadow
        for y in range(self.overlay_top + 1, self.overlay_bottom):
            self.put([self.overlay_right, y], self.shadow_bg + " ")
        for x in range(self.overlay_left + 1, self.overlay_right + 1):
            self.put([x, self.overlay_bottom], self.shadow_bg + " ")

        # Draw the footer text
        self.put([1, self.Y_MAX-1], self.outer_bg + self.footer_fg + self.footer_style + self.footer_text)

        # Draw the program title in the top left
        self.put([self.X_MAX - len(self.prog_title), self.Y_MAX - 1], self.outer_bg + self.title_fg + self.title_style + Menu.prog_title)

        # Draw accenting
        #for x in range(1, self.X_MAX):
            #self.put([x, 2], self.outer_bg + self.accent_fg + self.accent_style + "═")
        #for x in range(1, self.X_MAX):
            #self.put([x, self.title_y + 2], self.outer_bg + self.accent_fg + self.accent_style + "═")
        for x in range(self.overlay_left + 1, self.overlay_right):
            self.put([x, self.overlay_bottom - 1], self.overlay_bg + Fore.BLACK + Style.NORMAL + "─")
            self.put([x, self.overlay_top], self.overlay_bg + Fore.BLACK + Style.BRIGHT + "─")
        for y in range(self.overlay_top + 1, self.overlay_bottom - 1):
            self.put([self.overlay_right - 1, y], self.overlay_bg + Fore.BLACK + Style.NORMAL + "│")
            self.put([self.overlay_left, y], self.overlay_bg + Fore.BLACK + Style.BRIGHT + "│")
        self.put([self.overlay_right - 1, self.overlay_bottom - 1], self.overlay_bg + Fore.BLACK + Style.NORMAL + "┘")
        self.put([self.overlay_right - 1, self.overlay_top], self.overlay_bg + Fore.BLACK + Style.NORMAL + "┐")
        self.put([self.overlay_left, self.overlay_bottom - 1], self.overlay_bg + Fore.BLACK + Style.BRIGHT + "└")
        self.put([self.overlay_left, self.overlay_top], self.overlay_bg + Fore.BLACK + Style.BRIGHT + "┌")

        # Draw the description at the top of the overlay box
        if len(self.desc) > self.overlay_width:
            half = len(self.desc.split()) // 2
            first_line = " ".join(word for word in self.desc.split()[:half])
            second_line = " ".join(word for word in self.desc.split()[half:])
            self.put([self.desc_x, self.desc_y], self.overlay_bg + self.desc_fg + self.desc_style + first_line)
            self.put([self.desc_x, self.desc_y], self.overlay_bg + self.desc_fg + self.desc_style + second_line)
        else:
            self.put([self.desc_x, self.desc_y], self.overlay_bg + self.desc_fg + self.desc_style + self.desc)

        if self.dialog_msg:

            wrapped = self.word_wrapped_text(self.dialog_msg)
            for i, line in enumerate(wrapped):
                self.put([self.msg_x, self.msg_y + i],
                         self.overlay_bg + self.overlay_fg + Style.NORMAL + line)

        # Draw the footer text
        self.put([1, self.Y_MAX - 1], self.outer_bg + self.footer_fg + self.footer_style + self.footer_text)

        # Draw the buttons just in case something needs to be changed
        self.draw_buttons()


    def draw_buttons(self): # Redraw only the menu buttons
        self.update_dimensions()
        
        options_drawn = 0        
        for index, option in enumerate(self.options):
            text = self.options[index][0]

            if self.ok_dialog:
                option_x = self.overlay_left + ((self.overlay_width // (len(self.options) + 1)) * (index + 1)) - (
                len(text) // 2)  # (self.X_MAX // 2) - (len(text) // 2)  # In the middle
                option_y = self.overlay_bottom - 2
            elif self.text_box:
                pass
            else:
                option_x = (self.X_MAX // 2) - (len(text) // 2)  # In the middle
                option_y = (self.Y_MAX // 2 - (len(self.options) // 2) + options_drawn)

            box_x = (self.X_MAX // 2) - (self.overlay_width // 2)
            options_drawn += 1

            if not self.text_box:
                if index == self.selected:
                    if not self.ok_dialog:
                        self.put([box_x + 1, option_y], self.selected_bg + self.selected_fg + self.selected_style + "(" + str(index + 1) + ")")
                    self.put([option_x, option_y], self.selected_bg + self.selected_fg + self.selected_style + text)
                else:
                    if not self.ok_dialog:
                        self.put([box_x + 1, option_y], self.overlay_bg + self.overlay_fg + "(" + str(index + 1) + ")")
                    self.put([option_x, option_y], self.overlay_bg + self.overlay_fg + self.option_style + text)

    def move_down(self):
        if len(self.options) > 1:
            if self.selected >= len(self.options) - 1:
                self.selected = 0
            else:
                self.selected += 1

    def move_up(self):
        if len(self.options) > 1:
            if self.selected <= 0:
                self.selected = len(self.options) - 1
            else:
                self.selected -= 1

    def key_buffer(self, char):
        #self.buffer[self.cursor_y - self.overlay_top + 1][self.cursor_x - self.overlay_left + 1] = char
        #self.msg(self.buffer)

        #x = self.msg_x
        #y = self.msg_y

        #for c in self.buffer:

        c = char

        if self.cursor_x > self.overlay_right - 2:
            if self.cursor_y != self.overlay_bottom - 2:
                self.cursor_x = self.msg_x
                self.cursor_y += 1
            else:
                self.cursor_x -= 1 # THIS IS HACKY I DONT LIKE IT

            #if self.cursor_y >= self.overlay_bottom - 1:
                #self.cursor_y = self.overlay_bottom - 2

        self.put([self.cursor_x, self.cursor_y], self.overlay_bg + self.overlay_fg + c)
        self.cursor_x += 1

    def backspace(self):
        self.cursor_x -= 1
        if self.cursor_x <= self.overlay_left:

            if self.cursor_y == self.msg_y:
                self.cursor_x = self.msg_x
            else:
                self.cursor_x = self.overlay_right - 2
                self.cursor_y -= 1

                if self.cursor_y <= self.overlay_top:
                    self.cursor_y = self.overlay_top + 1

        self.put([self.cursor_x, self.cursor_y], self.overlay_bg + " ")
        self.put([self.cursor_x, self.cursor_y], self.overlay_bg + "")

    def start(self):
        self.redraw()
        while self.alive:

            if [self.X_MAX, self.Y_MAX] != [os.get_terminal_size().columns, os.get_terminal_size().lines + 1]: #[shutil.get_terminal_size((80, 20)).columns, shutil.get_terminal_size((80, 20)).lines + 1]:
                self.redraw()

                self.cursor_x = self.msg_x
                self.cursor_y = self.msg_y

            if msvcrt.kbhit():
                key = ord(msvcrt.getch())

            # BEGIN TEXT ENTRY CODE

                if self.get_kb_input:
                    if key == 8: # Backspace
                        #self.buffer = self.buffer[:-1] # Remove a character from the buffer
                        #self.msg(self.buffer)
                        self.backspace()
                    if str(chr(key)).lower() in "abcdefghijklmnopqrstuvwxyz,./?!\"\'£;:$%^&*()[]{}@#~/\\<>|-_=+¬`¦1234567890 ":
                        char = str(chr(key))
                        self.key_buffer(char)
                    if key == 156: # 156 = £
                        self.key_buffer("£")
                    if key == 27:
                        self.quit()
                    if key == 13: # enter, go to next line
                        #self.move_cursor_down()
                        if self.cursor_y != self.overlay_bottom - 2:
                            self.cursor_y += 1
                            self.cursor_x = self.msg_x
                        if self.cursor_y >= self.overlay_bottom - 1:
                            self.cursor_y = self.overlay_bottom - 2
                        self.move_cursor_to([self.cursor_x, self.cursor_y])
                    if key == 0: # function key
                        key = ord(msvcrt.getch())
                        if key == 59: # F1
                            pass # save file

            # END TEXT ENTRY CODE

                if key == 13 and not self.text_box:  # enter key
                    # self.put([1, 1], "")
                    f = self.options[self.selected][1]
                    f()

                if not self.ok_dialog:
                    if key == 224: # arrow key
                        key = ord(msvcrt.getch())
                        if key == 80: # down
                            self.move_down()
                            self.draw_buttons()
                        elif key == 72: # up
                            self.move_up()
                            self.draw_buttons()
                else:
                    if key == 224:  # arrow key
                        key = ord(msvcrt.getch())
                        if key == 75:  # left
                            self.move_up()
                            self.draw_buttons()
                        elif key == 77:  # right
                            self.move_down()
                            self.draw_buttons()

    def quit(self):
        self.alive = False

    def set_dialog_msg(self, msg):
        self.ok_dialog = True
        self.dialog_msg = msg

    def set_outer_bg(self, c):
        Menu.outer_bg = c
        self.redraw()

    def set_overlay_bg(self, c):
        Menu.overlay_bg = c
        self.redraw()

    def set_title(self, title):
        self.title = title
        self.redraw()

    def set_desc(self, desc):
        self.desc = desc
        self.redraw()

    def set_footer(self, text):
        self.footer_text = text
        self.redraw()

    def word_wrapped_text(self, text):
        wrapped_lines = []
        line = ""
        #lines_done = 0
        words = len(text.split())
        for index, word in enumerate(text.split()):
            word = word.strip()
            if len(line + word + " ") >= self.overlay_width - 2:
                wrapped_lines.append(line)
                line = word + " "
                #lines_done += 1
            elif index + 1 == words:
                line += word + " "
                wrapped_lines.append(line)
            else:
                line += word + " "
        return wrapped_lines

    def set_text_box(self):
        self.text_box = True
        self.get_kb_input = True
        self.update_dimensions()
        self.cursor_x = self.msg_x
        self.cursor_y = self.msg_y

    def move_cursor_up(self, n=1):
        code = lambda n: '\x1b[%dA' % n
        print(code(n), end="")

    def move_cursor_down(self, n=1):
        code = lambda n: '\x1b[%dB' % n
        print(code(n), end="")

    def move_cursor_back(self, n=1):
        code = lambda n: '\x1b[%dD' % n
        print(code(n), end = "")

    def move_cursor_right(self, n=1):
        code = lambda n: '\x1b[%dC' % n
        print(code(n), end="")

    def move_cursor_to(self, coords):
        x,y = coords
        pos = lambda x, y: '\x1b[%d;%dH' % (y, x)
        print(pos(x,y), end="")

    def msg(self, text):
        x,y = self.msg_x, self.msg_y

        if len(text) > self.overlay_width - 2:

            wrapped_text = self.word_wrapped_text(text)
            if len(wrapped_text) > 1:
                for i, line in enumerate(wrapped_text):
                    for j in range(self.overlay_left + 1, self.overlay_right - 1):
                        self.put([j, y + i], self.overlay_bg + " ")
                    self.put([x, y + i], self.overlay_bg + self.overlay_fg + self.msg_style + line)
            else:
                clean = False
                for char in text:
                    if y > self.msg_y and not clean:
                        clean = True
                        for j in range(self.overlay_left + 1, self.overlay_right - 1):
                            self.put([j, y], self.overlay_bg + " ")
                    if x > self.overlay_width - 1:
                        y += 1
                        clean = False
                        x = self.msg_x
                        for j in range(self.overlay_left + 1, self.overlay_right - 1):
                            self.put([j, y], self.overlay_bg + " ")
                    self.put([x, y], self.overlay_bg + self.overlay_fg + self.msg_style + char)
                    x += 1

            #wrapped_text = self.word_wrapped_text(text)

        else:
            for j in range(self.overlay_left + 1, self.overlay_right - 1):
                self.put([j, y], self.overlay_bg + " ")

            self.put([x, y], self.overlay_bg + self.overlay_fg + self.msg_style + text)


























