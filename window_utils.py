import pygetwindow as gw


def fake_resize_and_move_window(window_title, window_width, window_height, window_x, window_y):
    try:
        windows = gw.getWindowsWithTitle(window_title)
        for win in windows:
            if win.title.upper() == window_title.upper():
                window = win
                break
        if windows is None:
            print("can't find window")
        window.resizeTo(window_width, window_height)
        window.moveTo(window_x, window_y)
        window.restore()
        window.activate()
        print("sucessfully resized windows")
        return True
    except Exception as e:
        print(e)


def setup_emulator_window_main():
    emulators = ["window_1", "window_2"]
    width = 440
    height = 800

    try:
        i = 0
        for emulator in emulators:
            x_coord = width*i
            result = fake_resize_and_move_window(
                emulator,
                width,
                height,
                x_coord,
                0
            )
            i += 1
    except Exception as e:
        print(e)