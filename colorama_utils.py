def draw(x, y, text):
    print("\x1b[{};{}H".format(y, x) + text, end="")  # Move the cursor to the given coordinates and then print the text
