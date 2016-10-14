from colorama import init, Fore, Back, Style
import msvcrt, shutil

init(autoreset=True)

class Menu:
    def __init__(self, title="Main Menu", fg=Fore.WHITE, bg=Back.BLUE):
        self.X_MAX,self.Y_MAX = shutil.get_terminal_size((80, 20)).columns, shutil.get_terminal_size((80, 20)).lines
        self.options = []
        self.bg = bg 
        self.fg = fg
        self.title = title
        self.selected = 0 # first option

        self.option_width = self.X_MAX // 3
        self.option_height = 1

    def add(self, text, target):
        self.options.append([text,target]) 

    def put(self, coords, text):
        x,y = coords 
        pos = lambda x,y: '\x1b[%d;%dH' % (y,x) # generate the ansi code for placing text at position x,y
        print(pos(x,y) + text, end = "")

    def draw(self):
        for y in range(1, self.Y_MAX):
            for x in range(1, self.X_MAX):

                self.put([x,y], self.bg + " ")

        

        for y in range(1, self.Y_MAX):
            for x in range(1, self.X_MAX):

                if y == (self.Y_MAX // 10) and x == (self.X_MAX // 2) - (len(self.title) // 2):
                    self.put([x,y], self.bg + self.fg + self.title)




        options_drawn = 0        
        for index, option in enumerate(self.options):
            text = self.options[index][0]
                        
            option_x = (self.X_MAX//2) - (len(text)//2) # In the middle
            option_y = (self.Y_MAX//2) + options_drawn

            box_x = (self.X_MAX // 3)
            options_drawn += 1
            for x in range(box_x, self.X_MAX - box_x):
                self.put([x,option_y], Back.WHITE + " ")
            self.put([box_x,option_y], Back.WHITE + Fore.BLACK + str(index+1) + ")")
            if index == self.selected:
                bg = Back.GREEN
                fg = Fore.BLACK
            else:
                bg = Back.WHITE
                fg = Fore.BLACK
            self.put([option_x,option_y], bg + fg + text)

    def draw_buttons(self):
        options_drawn = 0        
        for index, option in enumerate(self.options):
            text = self.options[index][0]
                        
            option_x = (self.X_MAX//2) - (len(text)//2) # In the middle
            option_y = (self.Y_MAX//2) + options_drawn

            box_x = (self.X_MAX // 3)
            options_drawn += 1
            for x in range(box_x, self.X_MAX - box_x):
                self.put([x,option_y], Back.WHITE + " ")
            self.put([box_x,option_y], Back.WHITE + Fore.BLACK + str(index+1) + ")")
            if index == self.selected:
                bg = Back.GREEN
                fg = Fore.BLACK
            else:
                bg = Back.WHITE
                fg = Fore.BLACK
            self.put([option_x,option_y], bg + fg + text)

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
        self.draw()
        while True:
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
                    self.draw()

if __name__ == "__main__":

    import winsound

    def test_function():
        print("Hello, world!")
        input("Press enter to continue.")
    
    #title = input("Menu title: ")
    

    m = Menu()
    m.add("Hello World", target=test_function)
    m.add("Beep", target= lambda: winsound.Beep(500, 200))
    m.add("Exit", target= lambda: quit() )
    try:
        m.start()
    except Exception as e:
        print(e)
        input()