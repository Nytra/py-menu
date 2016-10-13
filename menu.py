from colorama import init, Fore, Back, Style
import msvcrt

init(autoreset=True)

class Menu:
    def __init__(self, dimensions, title="Test Menu", fg=Fore.WHITE, bg=Back.BLUE):
        self.X_MAX,self.Y_MAX = dimensions
        self.options = []
        self.bg = bg 
        self.fg = fg
        self.title = title
        self.selected = 0 # first option

        self.option_width = self.X_MAX // 3
        self.option_height = self.Y_MAX // 10
        
        self.option_zone_x = (self.X_MAX//2) - (self.option_width//2) # In the middle
        self.option_zone_y = (self.Y_MAX//2) + (self.option_height//2) # In the middle but also pushed slightly towards the bottom

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

                if y >= self.option_zone_y and y < self.Y_MAX - (self.Y_MAX - self.option_zone_y):


                    n = len(self.options)
                    for index, option in enumerate(self.options):
                        text = self.options[index][0]
                        ox = (self.X_MAX // 2) - (len(text) // 2)

                        if x == ox and y == oy:
                            self.put([x,y], self.bg + self.fg + text)

    def move_down(self):
        if self.selected >= len(self.options-1):
            self.selected = 0
        else:
            self.selected += 1

    def move_up(self):
        if self.selected <= 0:
            self.selected = len(self.options-1)
        else:
            self.selected -= 1

    def start(self):
        index = 0
        self.draw()
        while True:
            if msvcrt.kbhit():
                key = ord(msvcrt.getch())
                if key == 224: # arrow key
                    key = ord(msvcrt.getch())
                    if key == 80:
                        self.move_down()
                        self.draw()
                    elif key == 72:
                        self.move_up()
                        self.draw()

if __name__ == "__main__":

    def test_function():
        print("Hello, world!")
    
    m = Menu([80,20])
    m.add("Test", target=test_function)
    m.start()
