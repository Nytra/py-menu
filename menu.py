from colorama import init, Fore, Back, Style
import msvcrt, os

# A Python Framework for the Creation of Text-Based Menu Interfaces
# Created and developed by Sam Scott, aged 17 years and 7 months
# 13-10-2016

# GitHub Repo: https://github.com/Nytra/py-menu
# Here you'll be able to find all of the latest updates as soon as they're available

init(autoreset=True)

class Menu:
    def __init__(self, title="Main Menu", desc="Choose an option:", footer_text="Use the arrow keys to highlight an option and then press enter to select it.", fg=Fore.WHITE, bg=Back.BLUE):
        self.options = []

        self.outer_bg = bg
        self.outer_fg = fg
        self.overlay_bg = Back.WHITE
        self.overlay_fg = Fore.BLACK
        self.selected_bg = Back.BLUE
        self.selected_fg = Fore.WHITE
        self.shadow_bg = Back.BLACK
        self.option_fg = Fore.BLUE
        self.selected_style = Style.BRIGHT
        self.button_style = Style.NORMAL

        self.title = title # The menu title
        self.title_style = Style.BRIGHT
        self.prog_title = "PyMenu V0.7"

        self.footer_text = footer_text

        self.selected = 0 # The index of the option that is currently selected
        self.desc = desc # A simple description of the menu
        self.alive = True

        self.update_dimensions()

    def set_program_title(self, name):
        self.prog_title = name

    def update_dimensions(self):

        # Get the latest terminal dimensions

        #self.X_MAX, self.Y_MAX = shutil.get_terminal_size((80, 20)).columns, shutil.get_terminal_size((80, 20)).lines + 1
        self.X_MAX, self.Y_MAX = os.get_terminal_size().columns, os.get_terminal_size().lines + 1

        self.option_width = self.X_MAX // 3
        self.option_height = 1

        self.overlay_width = self.X_MAX // 2
        self.overlay_height = self.Y_MAX // 2

        self.overlay_top = (self.Y_MAX // 2) - (self.overlay_height // 2) # top y coord
        self.overlay_bottom = self.Y_MAX - (self.overlay_height // 2) # bottom y coord

        self.overlay_left = (self.X_MAX // 2) - (self.overlay_width // 2) # leftmost x coord
        self.overlay_right = self.X_MAX - (self.overlay_width // 2) # rightmost x coord

        self.title_x = (self.X_MAX // 2) - (len(self.title) // 2)
        self.title_y = (self.Y_MAX // 10)

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
        self.put([self.title_x, self.title_y], self.outer_bg + self.outer_fg + self.title_style + self.title)

        # Draw the white overlay background
        for y in range(self.overlay_top, self.overlay_bottom):
            for x in range(self.overlay_left, self.overlay_right):
                self.put([x, y], self.overlay_bg + " ")

        # Draw the overlay shadow
        for y in range(self.overlay_top + 1, self.overlay_bottom):
            self.put([self.overlay_right, y], self.shadow_bg + " ")
        for x in range(self.overlay_left + 1, self.overlay_right + 1):
            self.put([x, self.overlay_bottom], self.shadow_bg + " ")

        # Draw the description at the top of the overlay box
        if len(self.desc) > self.overlay_width:
            half = len(self.desc.split()) // 2
            first_line = " ".join(word for word in self.desc.split()[:half])
            second_line = " ".join(word for word in self.desc.split()[half:])
            self.put([self.overlay_left, self.overlay_top], self.overlay_bg + self.overlay_fg + first_line)
            self.put([self.overlay_left, self.overlay_top+1], self.overlay_bg + self.overlay_fg + second_line)
        else:
            self.put([self.overlay_left, self.overlay_top], self.overlay_bg + self.overlay_fg + self.desc)

        # Draw the footer text
        self.put([1, self.Y_MAX-1], self.outer_bg + self.outer_fg + self.title_style + self.footer_text)

        # Draw the program title in the top left
        self.put([1, 1], self.outer_bg + self.outer_fg + self.title_style + self.prog_title)

        # Draw the buttons just in case something needs to be changed
        self.draw_buttons()


    def draw_buttons(self): # Redraw only the menu buttons
        self.update_dimensions()
        
        options_drawn = 0        
        for index, option in enumerate(self.options):
            text = self.options[index][0]
                        
            option_x = (self.X_MAX // 2) - (len(text)//2) # In the middle
            option_y = (self.Y_MAX // 2 - (len(self.options) // 2) + options_drawn)

            box_x = (self.X_MAX // 2) - (self.overlay_width // 2)
            options_drawn += 1

            if index == self.selected:
                self.put([box_x, option_y], self.overlay_bg + " " + self.selected_bg + self.selected_fg + self.selected_style + "(" + str(index + 1) + ")")
                self.put([option_x, option_y], self.selected_bg + self.selected_fg + self.selected_style + text)
            else:
                self.put([box_x, option_y], self.overlay_bg + self.option_fg + " (" + str(index + 1) + ")")
                self.put([option_x, option_y], self.overlay_bg + self.overlay_fg + self.button_style + text)

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

                if key == 224: # arrow key
                    key = ord(msvcrt.getch())
                    if key == 80:
                        self.move_down()
                        self.draw_buttons()
                    elif key == 72:
                        self.move_up()
                        self.draw_buttons()

                elif key == 13: # enter key
                    self.put([1,1], "")
                    f = self.options[self.selected][1]
                    f()


    def quit(self):
        self.alive = False

    def write(self, coords, text):

        x,y = coords

        for j in range(self.overlay_left, self.overlay_right):
            self.put([j, y], self.overlay_bg + " ")

        self.put([x, y], self.overlay_bg + self.overlay_fg + text)

if __name__ == "__main__": # A simple menu demonstration will run whenever this program is directly executed

    import winsound

    def test_function():
        m.write([m.overlay_left, m.overlay_top+1], "Hello, world!")

    def dummy():
        pass

    def inc_pitch(val):
        global pitch, bm
        pitch += val
        bm.write([bm.overlay_left, bm.overlay_top+1],"Pitch: %d" % pitch)

    def dec_pitch(val):
        global pitch, bm
        if pitch <= val:
            pass
        else:
            pitch -= val
        #bm.draw_overlay()
        bm.write([bm.overlay_left, bm.overlay_top + 1], "Pitch: %d" % pitch)

    def beep():
        global pitch, duration
        winsound.Beep(pitch, duration)

    def beep_menu():
        global pitch, duration, bm
        bm = Menu("Beep Menu", "Use the options to control the pitch of the beep.", bg=global_outer_bg)
        bm.overlay_bg = global_overlay_bg
        bm.add("Beep", beep)
        bm.add("Increase Pitch", lambda: inc_pitch(100))
        bm.add("Decrease Pitch", lambda: dec_pitch(100))
        bm.add("Back", bm.quit)
        bm.start()
        m.redraw()

    def sys_config():

        def change_outbg():
            c = Menu("Change Outer Background", "Please select a colour.", bg=global_outer_bg)

            def set(colour):
                global global_outer_bg
                c.outer_bg = colour
                m.outer_bg = colour
                sc.outer_bg = colour
                global_outer_bg = colour
                c.redraw()

            c.overlay_bg = global_overlay_bg
            c.add("Red", lambda: set(Back.RED))
            c.add("Blue", lambda: set(Back.BLUE))
            c.add("Yellow", lambda: set(Back.YELLOW))
            c.add("Green", lambda: set(Back.GREEN))
            c.add("Magenta", lambda: set(Back.MAGENTA))
            c.add("White", lambda: set(Back.WHITE))
            c.add("Black", lambda: set(Back.BLACK))
            c.add("Back", c.quit)
            c.start()
            sc.redraw()

        def change_overbg():
            c = Menu("Change Outer Background", "Please select a colour.", bg=global_outer_bg)

            def set(colour):
                global global_overlay_bg
                c.overlay_bg = colour
                m.overlay_bg = colour
                sc.overlay_bg = colour
                global_overlay_bg = colour
                c.redraw()

            c.overlay_bg = global_overlay_bg
            c.add("Red", lambda: set(Back.RED))
            c.add("Blue", lambda: set(Back.BLUE))
            c.add("Yellow", lambda: set(Back.YELLOW))
            c.add("Green", lambda: set(Back.GREEN))
            c.add("Magenta", lambda: set(Back.MAGENTA))
            c.add("White", lambda: set(Back.WHITE))
            c.add("Black", lambda: set(Back.BLACK))
            c.add("Back", c.quit)
            c.start()
            sc.redraw()

        sc = Menu("System Configuration", "Modify system settings.", bg=global_outer_bg)
        sc.overlay_bg = global_overlay_bg
        sc.add("Outer Background", change_outbg)
        sc.add("Overlay Background", change_overbg)
        sc.add("Back", sc.quit)
        sc.start()
        m.redraw()


    def power_mon():
        pass

    #title = input("Menu title: ")

    pitch = 400
    duration = 600
    global_outer_bg = Back.BLUE
    global_overlay_bg = Back.WHITE

    m = Menu(bg=global_outer_bg)
    m.overlay_bg = global_overlay_bg
    m.add("Hello World", target=test_function)
    m.add("Power Monitoring", target=power_mon)
    m.add("Beep Menu", target= beep_menu)
    m.add("Settings", target=sys_config)
    m.add("Exit", target= lambda: quit() )
    try:
        m.start()
    except Exception as e:
        print(e)
        input()