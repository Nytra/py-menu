from colorama import init, Fore, Back, Style
import msvcrt, os

# A Python Framework for the Creation of Text-Based Menu Interfaces
# Created and developed by Sam Scott, aged 17 years and 7 months
# 13-10-2016

# GitHub Repo: https://github.com/Nytra/py-menu
# Here you'll be able to find all of the latest updates as soon as they're available

init(autoreset=True)

class Menu:
    def __init__(self, title="", desc="", footer_text="Use the arrow keys to highlight an option and then press enter to select it."):
        self.options = []

        self.outer_bg = Back.BLUE
        self.outer_fg = Fore.WHITE
        self.outer_style = Style.BRIGHT

        self.overlay_bg = Back.WHITE
        self.overlay_fg = Fore.BLACK
        self.overlay_style = Style.BRIGHT

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

        self.accent_fg = Fore.WHITE
        self.accent_style = Style.BRIGHT

        self.title = title # The menu title
        self.prog_title = "PyMenu V0.86a"

        self.footer_text = footer_text

        self.selected = 0 # The index of the option that is currently selected
        self.desc = desc # A simple description of the menu
        self.alive = True

        self.ok_dialog = False
        self.dialog_msg = ""

        self.update_dimensions()

    def set_program_title(self, name):
        self.prog_title = name

    def update_dimensions(self):

        # Get the latest terminal dimensions

        #self.X_MAX, self.Y_MAX = shutil.get_terminal_size((80, 20)).columns, shutil.get_terminal_size((80, 20)).lines + 1
        self.X_MAX, self.Y_MAX = os.get_terminal_size().columns, os.get_terminal_size().lines + 1

        self.option_width = self.X_MAX // 3
        self.option_height = 1

        if not self.ok_dialog:
            self.overlay_width = self.X_MAX // 2
            self.overlay_height = self.Y_MAX // 2
        else:
            wrapped = self.word_wrapped_text(self.dialog_msg)
            self.overlay_height = len(wrapped) +  4
            self.overlay_width = len(wrapped[0]) + 4
            for line in wrapped:
                if len(line) > self.overlay_width - 2:
                    self.overlay_width = len(line) + 2

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
        self.update_dimensions()

        for y in range(1, self.Y_MAX):
            for x in range(1, self.X_MAX):

                self.put([x,y], self.outer_bg + " ")

        self.draw_overlay()
        self.draw_buttons()

    def draw_overlay(self): # redraw only the menu overlay and skip the outer background
        self.update_dimensions()

        # Draw the menu title at the top
        self.put([self.title_x, self.title_y], self.outer_bg + self.title_fg + self.title_style + self.title)

        # Draw the white overlay background
        for y in range(self.overlay_top, self.overlay_bottom):
            for x in range(self.overlay_left, self.overlay_right):
                self.put([x, y], self.overlay_bg + " ")

        # Draw the overlay shadow
        for y in range(self.overlay_top + 1, self.overlay_bottom):
            self.put([self.overlay_right, y], self.shadow_bg + " ")
        for x in range(self.overlay_left + 1, self.overlay_right + 1):
            self.put([x, self.overlay_bottom], self.shadow_bg + " ")

        # Draw the footer text
        self.put([1, self.Y_MAX-1], self.outer_bg + self.footer_fg + self.footer_style + self.footer_text)

        # Draw the program title in the top left
        self.put([self.X_MAX - len(self.prog_title), self.Y_MAX - 1], self.outer_bg + self.title_fg + self.title_style + self.prog_title)

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
            self.put([self.desc_x, self.desc_y], self.overlay_bg + self.overlay_fg + self.desc_style + first_line)
            self.put([self.desc_x, self.desc_y], self.overlay_bg + self.overlay_fg + self.desc_style + second_line)
        else:
            self.put([self.desc_x, self.desc_y], self.overlay_bg + self.overlay_fg + self.desc_style + self.desc)

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

            option_x = (self.X_MAX // 2) - (len(text) // 2)  # In the middle
            if not self.ok_dialog:
                option_y = (self.Y_MAX // 2 - (len(self.options) // 2) + options_drawn)
            else:
                option_y = self.overlay_bottom - 2

            box_x = (self.X_MAX // 2) - (self.overlay_width // 2)
            options_drawn += 1

            if index == self.selected:
                if not self.ok_dialog:
                    self.put([box_x + 1, option_y], self.selected_bg + self.selected_fg + self.selected_style + "(" + str(index + 1) + ")")
                self.put([option_x, option_y], self.selected_bg + self.selected_fg + self.selected_style + text)
            else:
                if not self.ok_dialog:
                    self.put([box_x + 1, option_y], self.overlay_bg + self.overlay_fg + "(" + str(index + 1) + ")")
                self.put([option_x, option_y], self.overlay_bg + self.overlay_fg + self.option_style + text)

    def is_ok_dialog(self):
        self.ok_dialog = True
        self.options = [["OK", self.quit]]

    def move_down(self):
        if self.selected >= len(self.options) - 1:
            self.selected = 0
        else:
            self.selected += 1

    def move_up(self):
        if self.selected <= 0:
            self.selected = len(self.options) - 1
        else:
            self.selected -= 1

    def start(self):
        self.redraw()
        while self.alive:

            if [self.X_MAX, self.Y_MAX] != [os.get_terminal_size().columns, os.get_terminal_size().lines + 1]: #[shutil.get_terminal_size((80, 20)).columns, shutil.get_terminal_size((80, 20)).lines + 1]:
                self.redraw()

            if msvcrt.kbhit():
                key = ord(msvcrt.getch())

                if not self.ok_dialog:
                    if key == 224: # arrow key
                        key = ord(msvcrt.getch())

                        if key == 80: # down
                            self.move_down()
                            self.draw_buttons()
                        elif key == 72: # up
                            self.move_up()
                            self.draw_buttons()

                        elif key == 75: # left
                            pass
                        elif key == 77: # right
                            pass

                    elif key == 13: # enter key
                        self.put([1,1], "")
                        f = self.options[self.selected][1]
                        f()
                else:
                    if key == 13: # enter key
                        self.put([1,1], "")
                        f = self.options[self.selected][1]
                        f()

    def quit(self):
        self.alive = False

    def set_dialog_msg(self, msg):
        self.is_ok_dialog()
        self.dialog_msg = msg

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

    def msg(self, text):
        x,y = self.msg_x, self.msg_y

        if len(text) > self.overlay_width - 2:

            wrapped_text = self.word_wrapped_text(text)
            for i, line in enumerate(wrapped_text):
                for j in range(self.overlay_left + 1, self.overlay_right - 1):
                    self.put([j, y + i], self.overlay_bg + " ")
                self.put([x, y + i], self.overlay_bg + self.overlay_fg + self.msg_style + line)

            #wrapped_text = self.word_wrapped_text(text)

        else:
            for j in range(self.overlay_left + 1, self.overlay_right - 1):
                self.put([j, y], self.overlay_bg + " ")

            self.put([x, y], self.overlay_bg + self.overlay_fg + self.msg_style + text)


























