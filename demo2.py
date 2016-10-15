from pymenu import *

if __name__ == "__main__": # A simple menu demonstration will run whenever this program is directly executed

    try:
        import winsound
        sound = True
    except:
        sound = False

    def test_function():
        m.msg(" ".join("Hello, world!" for x in range(6)))

    def dummy():
        pass

    def inc_pitch(val):
        global pitch, bm
        pitch += val
        #bm.write([bm.msg_x, bm.msg_y],"Pitch: %d" % pitch)
        bm.msg("Pitch: %d" % pitch)

    def dec_pitch(val):
        global pitch, bm
        if pitch <= val:
            pass
        else:
            pitch -= val
        #bm.draw_overlay()
        #bm.write([bm.msg_x, bm.msg_y], "Pitch: %d" % pitch)
        bm.msg("Pitch: %d" % pitch)

    def beep():
        global pitch, duration
        if sound:
            winsound.Beep(pitch, duration)
        else:
            #bm.write([bm.msg_x, bm.msg_y], "Sound is disabled on this platform.")
            bm.msg("Sound is disabled on this platform.")

    def beep_menu():
        global pitch, duration, bm
        bm = Menu("Beeping", "Use The Options To Control The Pitch Of The Beep")
        bm.overlay_bg = global_overlay_bg
        bm.add("Beep", beep)
        bm.add("Increase Pitch", lambda: inc_pitch(100))
        bm.add("Decrease Pitch", lambda: dec_pitch(100))
        bm.add("Back", bm.quit)
        bm.start()
        m.redraw()

    def sys_config():

        def change_outbg():
            c = Menu("Change Outer Background", "Select A Colour")

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
            c = Menu("Change Outer Background", "Select A Colour")

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

        sc = Menu("Colour Settings", "Give Your Menu A New Coat Of Paint!")
        sc.overlay_bg = global_overlay_bg
        sc.add("Outer Background", change_outbg)
        sc.add("Overlay Background", change_overbg)
        sc.add("Back", sc.quit)
        sc.start()
        m.redraw()


    def dialog_demo():
        pm = Menu("Dialog Boxes", "Examples of Dialog Boxes")

        def alice():
            tm = Menu("Alice in Wonderland", "Alice's Adventures in Wonderland")
            tm.set_dialog_msg(
                "There was nothing so very remarkable in that; nor did Alice think it so very much out of the way to hear the Rabbit say to itself \"Oh dear! Oh dear! I shall be too late!\" (when she thought it over afterwards it occurred to her that she ought to have wondered at this, but at the time it all seemed quite natural); but, when the Rabbit actually took a watch out of its waistcoat-pocket, and looked at it, and then hurried on, Alice started to her feet, for it flashed across her mind that she had never before seen a rabbit with either a waistcoat-pocket, or a watch to take out of it, and burning with curiosity, she ran across the field after it, and was just in time to see it pop down a large rabbit-hole under the hedge.")
            tm.add("OK", tm.quit)
            #tm.add("Cancel", self.quit)
            tm.start()
            pm.redraw()

        def error_msg():
            tm = Menu("ERROR", "CODE: A322", "")
            tm.set_dialog_msg(
                "An error occurred while trying to set power efficacy for Generator 7 in Zone 6. Recommend manual intervention."
            )
            tm.add("OK", tm.quit)
            #tm.add("Cancel", self.quit)
            tm.start()
            pm.redraw()

        def short_msg():
            tm = Menu("Small Dialog Box", ":)", "")
            tm.set_dialog_msg(
                "Blah"
            )
            tm.add("OK", tm.quit)
            tm.add("\"Blah\" to you, too.", tm.quit)
            #tm.add("Cancel", self.quit)
            tm.start()
            pm.redraw()

        def choice():
            tm = Menu("Multiple Choice", "Make A Decision", "")
            tm.set_dialog_msg(
                "Are you sure you want to proceed?"
            )
            tm.add("OK", tm.quit)
            tm.add("Cancel", tm.quit)
            tm.start()
            pm.redraw()

        def colours():

            def set_colour(colour):
                tm.outer_bg = colour
                tm.quit()

            tm = Menu("Colour Choice", "Make A Decision", "")
            tm.set_dialog_msg(
                "Choose a colour from the selection below."
            )
            tm.add("Green", lambda: set_colour(Back.GREEN))
            tm.add("Magenta", lambda: set_colour(Back.MAGENTA))
            tm.add("White", lambda: set_colour(Back.WHITE))
            tm.add("Blue", lambda: set_colour(Back.BLUE))
            tm.add("Cancel", tm.quit)
            tm.start()
            pm.redraw()

        pm.add("Alice in Wonderland", alice)
        pm.add("Error Message", error_msg)
        pm.add("Small Dialog Box", short_msg)
        pm.add("Confirmation Dialog Box", choice)
        pm.add("Colour Selection", colours)
        pm.add("Back", pm.quit)
        pm.start()
        m.redraw()

    #title = input("Menu title: ")

    pitch = 400
    duration = 600
    global_outer_bg = Back.BLUE
    global_overlay_bg = Back.WHITE

    m = Menu("Main Menu", "Choose An Option")
    m.overlay_bg = global_overlay_bg
    m.add("Hello World", target=test_function)
    m.add("Dialog Boxes", target=dialog_demo)
    m.add("Beeping", target= beep_menu)
    m.add("Colour Settings", target=sys_config)
    m.add("Exit", target= lambda: quit() )
    try:
        m.start()
    except Exception as e:
        print(e)
        input()