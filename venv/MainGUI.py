import tkinter
from tkinter import ttk
from time import sleep
import threading
import producers
import upgrades

class MainGUI:

    def __init__ (self, Window_Argument):

        self.strcurrency = tkinter.StringVar()
        self.currency = 0
        self.strcurrency.set(f"{self.currency}")
        self.thread_terminator = False

        self.window = Window_Argument

        self.window.geometry("900x450")
        self.window.title("Idle Game")
        self.mainframe = ttk.Frame(self.window, padding=10)
        self.mainframe.grid(column=0, row=0, sticky="wnse")

        button = ttk.Button(self.mainframe, text="Klick!", command=self.manual_klick)
        button.grid(columnspan=5, row=1, column=0)

        self.display = ttk.Label(self.mainframe, padding=5, relief="groove", textvariable=self.strcurrency)
        self.display.grid(row=0, column=0, columnspan=5)

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.producer_frame = ttk.Frame(self.mainframe)
        self.producer_frame.grid(column=0, row=2, sticky="e")
        self.producerONE = producers.Producer(5, 0, 5)
        self.producerTWO = producers.Producer(10, 0, 10)
        self.buy_button_one = ttk.Button(self.producer_frame, text="Buy ONE", command=self.buy_producerONE,
                                         state="disabled")
        self.buy_button_one.grid(column=0, row=0)
        self.buy_button_two = ttk.Button(self.producer_frame, text="Buy TWO", command=self.buy_producerTWO,
                                         state="disabled")
        self.buy_button_two.grid(column=0, row=1)

        self.producer_one_label_strvar = tkinter.StringVar()
        self.producer_one_label_strvar.set("Current Amount: "+self.producerONE.return_amount()+
                                           " Next Upgrade for: "+self.producerONE.return_cost())
        self.producer_one_label = ttk.Label(self.producer_frame,textvariable=self.producer_one_label_strvar)
        self.producer_one_label.grid(column=1, row=0)

        self.producer_two_label_strvar = tkinter.StringVar()
        self.producer_two_label_strvar.set("Current Amount: "+self.producerTWO.return_amount()+
                                           " Next Upgrade for: "+self.producerTWO.return_cost())
        self.producer_two_label = ttk.Label(self.producer_frame, textvariable=self.producer_two_label_strvar)
        self.producer_two_label.grid(column=1, row=1)

        self.upgrades_frame = ttk.Frame(self.mainframe)
        self.upgrades_frame.grid(column=1, row=2, sticky="w")
        self.upgrade_one = upgrades.Upgrade(self.producerONE)
        self.upgrade_two = upgrades.Upgrade(self.producerTWO)
        self.upgrade_button_one = ttk.Button(self.upgrades_frame, text="Upgrade", command=self.upgrade_one.upgrade,
                                             state="disabled")
        self.upgrade_button_one.grid(column=0, row=0)
        self.upgrade_button_two = ttk.Button(self.upgrades_frame, text="Upgrade", command=self.upgrade_two.upgrade,
                                             state="disabled")
        self.upgrade_button_two.grid(column=0, row=1)

        self.update_thread = threading.Thread(target=self.update_loop, daemon=False)
        self.update_thread.start()


    def manual_klick(self):
        self.currency += 1
        self.strcurrency.set(f"{self.currency}")

    def update_loop(self):
        while not self.thread_terminator:

            if self.producerONE.attributes["cost"] <= self.currency:
                self.buy_button_one.configure(state="enabled")
            else:
                self.buy_button_one.configure(state="disabled")
            if self.producerTWO.attributes["cost"] <= self.currency:
                self.buy_button_two.configure(state="enabled")
            else:
                self.buy_button_two.configure(state="disabled")

            if self.upgrade_one.cost <= self.currency:
                self.upgrade_button_one.configure(state="enabled")
            else:
                self.upgrade_button_one.configure(state="disabled")
            if self.upgrade_two.cost <= self.currency:
                self.upgrade_button_two.configure(state="enabled")
            else:
                self.upgrade_button_two.configure(state="disabled")

            self.currency += self.producerONE.attributes["amount"] * self.producerONE.attributes["value"]
            self.currency += self.producerTWO.attributes["amount"] * self.producerTWO.attributes["value"]
            self.strcurrency.set(f"{self.currency}")
            sleep(0.5)

    def on_close(self):
        self.thread_terminator=True
        sleep(0.5)
        self.window.destroy()

    def buy_producerONE(self):
        self.producerONE.buy(1)
        self.currency -= self.producerONE.attributes["cost"]
        self.producerONE.update_cost()
        if self.producerONE.attributes["cost"] > self.currency:
            self.buy_button_one.configure(state="disabled")
        self.producer_one_label_strvar.set("Current Amount: "+self.producerONE.return_amount()+
                                           " Next Upgrade for: "+self.producerONE.return_cost())

    def buy_producerTWO(self):
        self.producerTWO.buy(1)
        self.currency -= self.producerTWO.attributes["cost"]
        self.producerTWO.update_cost()
        if self.producerTWO.attributes["cost"] > self.currency:
            self.buy_button_two.configure(state="disabled")
        self.producer_two_label_strvar.set("Current Amount: "+self.producerTWO.return_amount()+
                                           " Next Upgrade for: "+self.producerTWO.return_cost())
