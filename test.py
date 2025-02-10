from GUI import Window

win = Window("Main")
win.setup_frame_and_canvas("Main")

i = 0
def OpenSub(root):
    global i
    i += 1
    root.setup_subwindow(f"Sub{i}")
    now_win = root.SubWindow(f"Sub{i}")
    now_win.txt_button(
        "OpenSub",
        lambda :OpenSub(now_win),
        f"master: {root.title()}",
        10, 10,
        150, 150
    )

win.txt_button(
    "OpenSub",
    lambda :OpenSub(win),
    "Main",
    "Main",
    10, 10,
    150, 150
)
win.first_window("Main")
win.mainloop()