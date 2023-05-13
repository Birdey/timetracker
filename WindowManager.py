"""
This module is responsible for creating and rendering the main window.

Classes:
    WindowManager
"""
import tkinter as tk


class WindowManager:
    """
    This class is responsible for creating and rendering the main window.
    """

    window = None

    window_name: str
    window_width: int
    window_height: int

    last_text_input: tk.Entry

    def __init__(self, window_name: str, window_size: tuple[int]) -> None:
        """
        Create the main window

            Parameters:
                window_name (str): The name of the window
                window_size (tuple[int]): The size of the window
        """
        self.window_name = window_name
        self.window_width, self.window_height = window_size

        self._create_window()

    def _create_window(self) -> tk.Tk:
        """
        Create the main window
        """
        window = tk.Tk()
        window.title(self.window_name)
        window.geometry(f"{self.window_width}x{self.window_height}")
        window.resizable(False, False)

        self.window = window

        return self.window

    def update_window(self) -> None:
        """
        Update the main window
        """
        self.window.update()

    def add_text(self, text: str, pos: tuple[int]) -> None:
        """
        Show text on the main window

            Parameters:
                text (str): The text to show
                pos (tuple[int]): The position of the text
        """
        label = tk.Label(self.window, text=text)
        label.place(x=pos[0], y=pos[1])

    def add_button(
        self, text: str, pos: tuple[int], size: tuple[int], callback: callable
    ) -> None:
        """
        Add a button to the main window

            Parameters:
                text (str): The text to show
                pos (tuple[int]): The position of the button
                size (tuple[int]): The size of the button
        """
        button = tk.Button(self.window, text=text)
        button.place(x=pos[0], y=pos[1], width=size[0], height=size[1])
        button.bind("<Button-1>", callback)
        # button.register(func=callback)
        print(f"Added button: {button} with callback: {callback}")
        return button

    def show_button(self, text: str, pos: tuple[int], size: tuple[int], callback):
        """
        Show a button on the main window

            Parameters:
                text (str): The text to show
                pos (tuple[int]): The position of the button
                size (tuple[int]): The size of the button
        """
        button = tk.Button(self.window, text=text)
        button.place(x=pos[0], y=pos[1], width=size[0], height=size[1])
        button.bind("<Button-1>", callback)

    def show_image(self, image_path: str, pos: tuple[int]):
        """
        Show an image on the main window

            Parameters:
                image_path (str): The path to the image file
                pos (tuple[int]): The position of the image
        """
        image = tk.PhotoImage(file=image_path)
        label = tk.Label(self.window, image=image)
        label.place(x=pos[0], y=pos[1])

    def show_text_input(self, text: str, pos: tuple[int], size: tuple[int]):
        """
        Show a text input on the main window

            Parameters:
                text (str): The text to show
                pos (tuple[int]): The position of the text input
                size (tuple[int]): The size of the text input
        """
        input = tk.Entry(self.window)
        input.insert(0, text)
        input.place(x=pos[0], y=pos[1], width=size[0], height=size[1])
        self.last_text_input = input

    def show_dropdown_menu(
        self, options: list[str], default: str, pos: tuple[int], size: tuple[int]
    ):
        """
        Show a dropdown menu on the main window

            Parameters:
                options (list[str]): The options
                default (str): The default option
                pos (tuple[int]): The position of the dropdown menu
                size (tuple[int]): The size of the dropdown menu
        """
        var = tk.StringVar(self.window)
        var.set(default)
        dropdown_menu = tk.OptionMenu(
            master=self.window, variable=var, value=default, values=enumerate(options)
        )
        dropdown_menu.place(x=pos[0], y=pos[1], width=size[0], height=size[1])

    def show_checkbox(self, pos: tuple[int], size: tuple[int]):
        """
        Show a checkbox on the main window

            Parameters:
                pos (tuple[int]): The position of the checkbox
                size (tuple[int]): The size of the checkbox
        """
        checkbox = tk.Checkbutton(self.window)
        checkbox.place(x=pos[0], y=pos[1], width=size[0], height=size[1])

    def show_text_box(self, pos: tuple[int], size: tuple[int]):
        """
        Show a text box on the main window

            Parameters:
                pos (tuple[int]): The position of the text box
                size (tuple[int]): The size of the text box
        """
        text_box = tk.Text(self.window)
        text_box.place(x=pos[0], y=pos[1], width=size[0], height=size[1])

    def close_window(self):
        """
        Close the main window
        """
        if self.window is not None:
            self.window.withdraw()
            self.window.destroy()

    def show(self):
        """
        Show the main window
        """
        try:
            self.window.mainloop()
        except SystemExit:
            self.window.destroy()

    def hide(self):
        """
        Hide the main window
        """
        self.window.withdraw()

    def unhide(self):
        """
        Unhide the main window
        """
        self.window.deiconify()

    def clear(self):
        """
        Clear the main window
        """
        self.window.destroy()
        self._create_window()

    def update(self):
        """
        Update the main window
        """
        self.window.update()
