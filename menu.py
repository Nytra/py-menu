from colorama import init, Fore, Back, Style
import msvcrt

init(autoreset=True)

class Menu:
    def __init__(self, dimensions, fg=Fore.WHITE, bg=Back.BLUE):
        self.X_MAX,self.Y_MAX = dimensions
        self.options = {} 
        self.bg = bg 
        self.fg = fg

    def add(self, text, target):
        self.options[text] = target

    def draw(self, coords, text):
        x,y = coords 
        pos = lambda x,y: '\x1b[%d;%dH' % (y,x) # generate the ansi code for placing text at position x,y
        print(pos(x,y) + text, end = "")

    def start(self):
        while True:
            pass

if __name__ == "__main__":

    def test_function():
        print("Hello, world!")
    
    m = Menu((80,20))
    m.add("Test", target=test_function)
    m.start()
