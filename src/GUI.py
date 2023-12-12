"""
GUI for the MMS HS 23 Program
@author: ooemperor
"""

import tkinter as tk
from Execution import Execution


class Window(tk.Tk):
    """
    Main Window class which displays all the frames.
    """

    def __init__(self):
        """
        Constructor of the main window
        """

        tk.Tk.__init__(self)

        self.current_page = None

        self.DEBUG = True

        self._styling()  # apply styling

        container = tk.Frame(self)
        container.grid()  # container in which the frames will be rendered

        self.pages = {}
        # add all the used windows to the dict
        for page in (HomeWindow, SettingsWindow):
            _page = page(container, self)
            self.pages[page] = _page

        # render the first page
        self.render_page(HomeWindow)

    def _styling(self):
        """
        Apply Styling to the window
        @return:
        """
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.title('MMS HS23')
        self.geometry('400x400')

    def render_page(self, window):
        """
        Render a given Page.
        @param window: The window/page that shall be display
        @type window: tkinter.Frame
        @return: No return since it renders the frame
        """
        if self.current_page is not None:
            self.current_page.grid_forget()

        page = self.pages[window]
        self.current_page = page
        page.grid(row=0, column=0)
        page.controller.configure(background=page.background)
        page.tkraise()

    def get_settings(self):
        """
        Getting the values set in the SettingsWindow
        @return: The settings value in a JSON
        @rtype: dict
        """
        settings_page = self.pages[SettingsWindow]
        return settings_page.get_values()


class HomeWindow(tk.Frame):
    """
    Home Window
    The first windows to be displayed within the UI
    """

    def __init__(self, parent, controller):
        """
        Constructor of the home Window
        @param parent: The parent in which it will be display
        @type parent: tk.Frame
        @param controller: The controller window
        @type controller: tkinter.Tk
        """

        self.background = '#ADD8E6'
        tk.Frame.__init__(self, parent, background=self.background)
        self.controller = controller

        self._styling()

        self.columnconfigure(1, pad=20)
        self.rowconfigure(1, pad=40)
        self.rowconfigure(3, pad=40)

        # Creates all the Buttons and Widgets

        button_start = tk.Button(self, text='Start', width=30,
                                 command=lambda: self._execute())  # ,command = tbd
        button_start.grid(column=1, row=1)

        button_settings = tk.Button(self, text='Settings', width=30,
                                    command=lambda: controller.render_page(SettingsWindow))  # ,command = tbd
        button_settings.grid(column=1, row=3)

    def _styling(self):
        """
        Apply the styling to the frame
        @return: No return value
        """
        self.configure(background=self.background)

    def _execute(self):
        """
        Starting the Execution Service
        """
        data = self.controller.get_settings()
        head = data["head"]
        eye = data["eye"]
        hand = data["hand"]

        if self.controller.DEBUG: print(print(f"Running with Parameters: \nHAND: {hand}\nHEAD: {head}\nEYE: {eye}")
        )


        Execution(head=head, hand=hand, eye=eye).run()


class SettingsWindow(tk.Frame):
    """
    Class for the settings window
    """

    def __init__(self, parent, controller):
        """
        Constructor of the home Window
        @param parent: The parent in which it will be display
        @type parent: tk.Frame
        @param controller: The controller window
        @type controller: tkinter.Tk
        """
        self.background = '#ADD8E6'
        tk.Frame.__init__(self, parent, background=self.background)
        self.controller = controller

        self._styling()

        self.columnconfigure(1, pad=20)
        self.columnconfigure(2, pad=20)
        self.columnconfigure(3, pad=20)

        self.rowconfigure(1, pad=40)
        self.rowconfigure(3, pad=40)
        self.rowconfigure(4, pad=40)

        self.use_eye = tk.IntVar(value=0)
        self.use_hand = tk.IntVar(value=1)
        self.use_head = tk.IntVar(value=1)
        check_1 = tk.Checkbutton(self, text='Eye Tracking', background=self.background, width=20, anchor='w',
                                 variable=self.use_eye, onvalue=1, offvalue=0)
        check_1.grid(column=0, row=1)
        check_2 = tk.Checkbutton(self, text='Hand Tracking', background=self.background, width=20, anchor='w',
                                 variable=self.use_hand, onvalue=1, offvalue=0)
        check_2.grid(column=0, row=2)
        check_3 = tk.Checkbutton(self, text='Head Tracking', background=self.background, width=20, anchor='w',
                                 variable=self.use_head, onvalue=1, offvalue=0)
        check_3.grid(column=0, row=3)

        button_apply = tk.Button(self, text='Apply', command=lambda: controller.render_page(HomeWindow))
        button_apply.grid(column=2, row=4)

        button_cancel = tk.Button(self, text='Cancel', command=lambda: controller.render_page(HomeWindow),
                                  background='#FF7F7F')
        button_cancel.grid(column=3, row=4)

    def get_values(self):
        """
        Getting the values of the checkboxes out of the settings app
        @return: A dictionary of all the values for the checkboxes
        @rtype: dict
        """

        data = dict()
        data["eye"] = self.use_eye.get()
        data["hand"] = self.use_hand.get()
        data["head"] = self.use_head.get()

        assert data is not None
        return data

    def _styling(self):
        """
        Apply the styling to the frame
        @return: No return value
        """
        self.configure(background=self.background)


if __name__ == '__main__':
    screen = Window()
    screen.mainloop()
