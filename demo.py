from menu import *
import string, random

def dummy():
    pass

def quit_prompt():
    m = Menu("Quit Prompt")
    m.set_prompt("Are you sure you want to quit?")
    m.add_button("Yes", quit)
    m.add_button("No", m.quit)
    m.start()

def inputs():

    def submit(details):
        m = Menu("Input Feedback")
        for i, value in enumerate(details):
            m.add_text(str(value))
        m.add_button("OK", m.quit)
        m.start()

    m = Menu("Inputs")
    m.set_prompt("Enter some information in the fields below.")
    m.add_input("Forename:")
    m.add_input("Age:")
    m.add_checkbox("Sign up for our monthly newsletter?")
    m.add_button("Submit", lambda: submit(m.get_inputs())) # lambda can be used if you need to pass an argument to a function
    m.add_button("Back", m.quit)
    m.start()

def scrolling():

    def buttons():
        m = Menu("Scrolling Buttons")
        for i in range(30):
            m.add_button("".join(random.choice(string.ascii_letters) for l in range(5)), dummy)
        m.add_button("Back", m.quit)
        m.start()

    def inputs():
        m = Menu("Scrolling Inputs")
        m.set_prompt("Scrolling Inputs.")
        for i in range(30):
            m.add_input("".join(random.choice(string.ascii_letters) for l in range(5)) + ":")
        m.add_button("Back", m.quit)
        m.start()

    def text():
        m = Menu("Scrolling Text")
        m.set_prompt("I suppose it was just a temporal accident that the year I turned teenage two pivotal gay"
                     " figureheads appeared on Top of the Pops and the front cover of Smash Hits. But to a mind "
                     "spiralling with the possibility of what life had to offer outside a grey, rainy world that "
                     "pivoted on Saturday afternoons spent leafing through the vinyl at Wythenshawe library's "
                     "record department, it felt exactly like magic."
                     " There was a point somewhere between the angry, sad falsetto of Jimmy Somerville and the"
                     " mischievous sex of Holly Johnson that felt like a perfect distillation of a gay adult life."
                     " There were other figures seeming to support their contention in more clandestine terms, not"
                     " yet ready to talk transparently about their differences. But the clues were all there.")
        m.add_button("Back", m.quit)
        m.start()

    m = Menu("Scrolling")
    m.add_button("Buttons", buttons)
    m.add_button("Inputs", inputs)
    m.add_button("Text", text)
    m.add_button("Back", m.quit)
    m.start()

m = Menu("Main Menu")
m.set_footer("")
m.set_program_title("")
m.add_button("Scrolling", scrolling)
m.add_button("Inputs", inputs)
m.add_button("Quit", quit_prompt)
m.start()
