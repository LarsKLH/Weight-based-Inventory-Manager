import sqlite3
from datetime import datetime as dt
from datetime import timedelta
import customtkinter as ctk
from CTkTable import *
import tkinter as tk
#from tkcalendar import Calendar
from CTkMessagebox import CTkMessagebox
from CTkListbox import *
from PIL import Image, ImageTk
import os

import Systemlogger_module as slog



"""
Hovedfil for programmet. 
Her lages klassene for de ulike vinduene og funksjonene for å oppdatere dataene.

"""


def datetime_to_string(datetime):
    return datetime.strftime(date_format)

def string_to_datetime(string):
    return dt.strptime(string, date_format)


class dataHandling():
    """
    Klasse brukt for datahåndtering.
    """
    def __init__(self):
        """
        Initialiserer klassen.
        
        """
        log.addp("Fetching data from database.")

        self.fetch_data()
        

        self.now_datetime = dt.now()
        self.now_string = datetime_to_string(self.now_datetime)

        #Creating a list of dates from now to the last date in the calendar
        current_date = self.now_datetime
        self.dates = []
        while current_date <= self.calendar[-1][0]:
            current_date += timedelta(days=1)
            self.dates.append(datetime_to_string(current_date)[:10])

        log.addp("Analyzing data.")
        self.estimate_delivery_time()
        self.estimate_delivery_dates()
        self.calculate_future_storage()
        self.analyze_storage()
        
    def fetch_data(self):
        #fetches all data from the database

        
        with sqlite3.connect('Storage_solution_DB.db') as conn:
            
            cursor = conn.cursor()
            #fetches the storage data
            cursor.execute("SELECT * FROM Storage;")
            self.storage = {i[0] : int(i[1]/i[2]) for i in cursor.fetchall()}
    

            #fetches the operations data
            cursor.execute("SELECT * FROM Operations;")
            self.operations = {i[0] : [] for i in cursor.fetchall()}
            
            for o in self.operations.keys():
                cursor.execute(f"SELECT * FROM Operation_Storage_map WHERE operation_id = \"{o}\";")
                self.operations[o] = [(i[2], i[3]) for i in cursor.fetchall()]

        
            #fetches the calendar data
            cursor.execute("SELECT * FROM Calendar;")
            self.calendar = sorted([(string_to_datetime(i[0]), i[1]) for i in cursor.fetchall()])
        
    
            #fetches the orders data
            cursor.execute("SELECT * FROM Orders;")
            self.orders = sorted(cursor.fetchall(), key=lambda x: string_to_datetime(x[3]))
            print(self.orders)

    def estimate_delivery_dates(self):
        self.estimated_delivery_dates = {}
        for order in self.orders:
            item = order[1]
            order_date = order[3]
            if item in self.estimated_delivery_time:
                self.estimated_delivery_dates[order[0]] = datetime_to_string(string_to_datetime(order_date)+self.estimated_delivery_time[item])

        self.order_status = {}
        self.order_message = {}
        for order in self.orders:
            order_id = order[0]
            item = order[1]
            quantity = order[2]
            order_date = order[3]
            delivery_date = order[-1]
            #print(order_id, item, quantity, order_date, delivery_date)
            if string_to_datetime(order_date) > self.now_datetime:
                self.order_status[order_id] = "to be ordered"
                self.order_message[order_id] = f"{quantity} {item} is to be done on {order_date}. It is estimated to be delivered on {self.estimated_delivery_dates[order_id]} based on delivery time of previous orders."
            elif delivery_date == "not recived":
                if self.now_datetime > string_to_datetime(self.estimated_delivery_dates[order_id]):
                    self.order_status[order_id] = "not recived, overdue"
                    self.order_message[order_id] = f"{quantity} {item} was ordered on {order_date} and was estimated to be delivered on {self.estimated_delivery_dates[order_id]}, but has not been recived yet."
                else:
                    self.order_status[order_id] = "not recived, in transit"
                    self.order_message[order_id] = f"{quantity} {item} was ordered on {order_date} and is estimated to be delivered on {self.estimated_delivery_dates[order_id]}."

            else:
                self.order_status[order_id] = "recived"
                self.order_message[order_id] = f"{quantity} {item} was ordered on {order_date} and was delivered on {delivery_date}."
               
    def estimate_delivery_time(self):
        temp_estimated_delivery_time = {item : [] for item in self.storage.keys()}
        max_delivery_time = timedelta(days=0)
        for order in self.orders:
            item = order[1]
            delivery_date = order[-1]
            if delivery_date != "not recived":
                delivery_time = string_to_datetime(order[4]) - string_to_datetime(order[3])
                if delivery_time > max_delivery_time:
                    max_delivery_time = delivery_time
                temp_estimated_delivery_time[item].append(delivery_time)

        self.estimated_delivery_time = {}
        for item in temp_estimated_delivery_time.keys():
            if len(temp_estimated_delivery_time[item]) > 0:
                self.estimated_delivery_time[item] = sum(temp_estimated_delivery_time[item], timedelta(0))/len(temp_estimated_delivery_time[item])
            elif len(temp_estimated_delivery_time[item]) == 0: #if the order has not been recived, the estimated delivery time is set to the max delivery time of all items
                self.estimated_delivery_time[item] = max_delivery_time

    def calculate_future_storage(self):
        self.future_storage = {}
        for date in self.dates:
            temp_future_storage = self.storage.copy()
            future = [i for i in self.calendar if (i[0] > self.now_datetime) and (i[0] < string_to_datetime(date + " 00:00:00"))]
            
            for f in future:
                for item in self.operations[f[1]]:
                    temp_future_storage[item[0]] -= item[1]
            self.future_storage[date] = temp_future_storage

        for order in self.orders:
            estim_date = order[-2][:10]
            recived_date = order[-1]
            item = order[1]
            quantity = order[2]
            if (recived_date == "not recived") and (estim_date != "unknown") and (estim_date in self.future_storage.keys()):
                self.future_storage[estim_date][item] += quantity

    def analyze_storage(self):
        self.notifications = {}
        self.notificationurgency = {}
        #print(self.future_storage)

        for date in self.future_storage.keys():
            for item in self.future_storage[date].keys():
                if (self.future_storage[date][item] < 10) and (item not in self.notifications):
                    when_to_order = string_to_datetime(date + " 00:00:00")-self.estimated_delivery_time[item]
                    print(string_to_datetime(date + " 00:00:00"))
                    print(self.estimated_delivery_time[item])
                    print(when_to_order)
                    self.notifications[item] = f"Order {item} on {datetime_to_string(when_to_order)[:10]} to avoid running out on {date}"
                    urgency = when_to_order - self.now_datetime
                    if urgency < timedelta(days=1):
                        self.notificationurgency[item] = "red"
                    elif urgency < timedelta(days=4):
                        self.notificationurgency[item] = "yellow"
                    else:
                        self.notificationurgency[item] = "green"
        print(self.notificationurgency)

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        log.addp("Starting the main application.")
        super().__init__(*args, **kwargs)
        self.geometry("1000x800")
        #self.eval('tk::PlaceWindow . center')
        self.title("Storage Solution")
        
        #Tabs
        self.tab = ctk.CTkTabview(master=self.master, width=800, height=500)
        self.storageTab = self.tab.add("Storage")
        self.calendarTab = self.tab.add("Calendar")
        self.orderTab = self.tab.add("Orders")

        #Frames
        self.storage = Storage(self.storageTab)
        self.calendar = Calendar(self.calendarTab)
        self.order = Order(self.orderTab)

        self.notif_center = NotificationCenter(self)

        self.toolbar = toolbar(self)

        self.layout()

    def refresh(self):
        #self.destroy()
        #self.__init__(self.master)
        #self.layout()

        self.storage.refresh()
        self.calendar.refresh()
        self.order.refresh()
        self.notif_center.refresh()

    def layout(self):
        self.tab.grid(row=0, column=0)
        
        
class Storage(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.title = ctk.CTkLabel(self, text="Storage")
        titlefont = ("Arial", 45, "bold")
        self.title.configure(font = titlefont)

        self.table = ctk.CTkFrame(master=self)
        table_header_font = ("Arial", 15, "bold")
        self.table_header = [ctk.CTkLabel(self.table, text=i) for i in ["Item", "Quantity", "Picture"]]
        for i, cell in enumerate(self.table_header):
            cell.configure(font = table_header_font)
        table_values = [[i, dh.storage[i]] for i in dh.storage.keys()]
        self.table_widgets = [[ctk.CTkLabel(self.table, text=i) for i in v] + [ctk.CTkButton(self.table, text = "show", command=lambda arg = v[0]: self.show_picture(arg))] for v in table_values]
        
        #self.table = CTkTable(master=self, row=len(dh.storage)+1, column=2, values=[self.table_header] + table_values)

        optionmenu_var = ctk.StringVar(value=dh.now_string[:10])
        self.optionmenu = ctk.CTkOptionMenu(master=self, values=dh.dates, command=self.future_storage, variable=optionmenu_var)

        self.toplevel_window = None

        self.layout()

    def future_storage(self, choice):
        s = dh.future_storage[choice]          
        #new_values = [[i, s[i]] for i in s.keys()]
        #self.table.update_values([self.table_header] + new_values)
        self.table_widgets = [[ctk.CTkLabel(self.table, text=i) for i in v] for v in [[i, s[i]] for i in s.keys()]]
        self.layout()

    def show_picture(self, item):
        try:
            my_image = ctk.CTkImage(light_image=Image.open(os.path.abspath(f"Images/{item}.jpg")), dark_image=Image.open(os.path.abspath(f"Images/{item}.jpg")), size=(400, 400))
        except:
            return CTkMessagebox(message="No image found.", icon="warning").get()
        
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ctk.CTkToplevel(self)
        else:
            self.toplevel_window.focus()  # if window exists focus it
        self.toplevel_window.title(f"Image of {item}")

        bildebox = ctk.CTkLabel(self.toplevel_window, text="", image=my_image)
        bildebox.pack(padx=0, pady=0)

        iwidth = 400
        iheight = 400
        xpos = self.toplevel_window.winfo_screenwidth() - iwidth
        ypos = self.toplevel_window.winfo_screenheight() - iheight
        self.toplevel_window.geometry(f"400x400+{xpos}+{ypos}")
        self.toplevel_window.wait_visibility()
        self.toplevel_window.grab_set()
        self.toplevel_window.overrideredirect(True)
    

        self.toplevel_window.after(2000, self.toplevel_window.destroy)

    def refresh(self):
        self.destroy()
        self.__init__(self.master)
        self.layout()

    def layout(self):
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.title.pack(padx=20, pady=20, side="top")

        self.optionmenu.pack(padx=20, pady=20, side="top")
        self.table.pack(padx=20, pady=20, side="top")
        self.table.grid_rowconfigure(1, weight=1)
        self.table.grid_columnconfigure(1, weight=1)
        for i, cell in enumerate(self.table_header):
            cell.grid(row=0, column=i, padx=20, pady=5)
        for i, row in enumerate(self.table_widgets):
            for j, cell in enumerate(row):
                cell.grid(row=i+1, column=j, padx=20, pady=5)
        

class Calendar(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.title = ctk.CTkLabel(self, text="Calendar")
        titlefont = ("Arial", 45, "bold")
        self.title.configure(font = titlefont)

        self.table = ctk.CTkFrame(master=self)
        table_header_font = ("Arial", 15, "bold")
        self.table_header = [ctk.CTkLabel(self.table, text=i) for i in ["Date", "Operation", "Delete"]]
        for i, cell in enumerate(self.table_header):
            cell.configure(font = table_header_font)
        table_values = [[datetime_to_string(i[0]), i[1]] for i in dh.calendar]
        self.table_widgets = [[ctk.CTkLabel(self.table, text=i) for i in v] + [ctk.CTkButton(master=self.table, text="Delete", command=lambda row=i: self.delete_calendar_entry(row))] for i, v in enumerate(table_values)]

        self.add_button = ctk.CTkButton(master=self, text="Add to calendar", command=self.add_calendar)

        self.toplevel_window = None

        self.layout()

    def add_calendar(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = AddCalendarWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it
        return self.toplevel_window

    def delete_calendar_entry(self, row_index):
        confirmation = CTkMessagebox(message="Are you sure you want to delete this entry?", icon="question", option_1="No", option_2="Yes").get()
        if confirmation == "Yes":
            with sqlite3.connect('Storage_solution_DB.db') as conn:
                cursor = conn.cursor()
                action = f"""DELETE FROM Calendar WHERE datetime_id = \"{datetime_to_string(dh.calendar[row_index][0])}\";"""
                cursor.execute(action)
            dh.calendar.pop(row_index)
            self.refresh()
    

    def layout(self):
        self.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
    
        self.title.pack(padx=20, pady=20, side="top")

        #self.table.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.table.pack(padx=20, pady=20, side="top")
        self.table.grid_rowconfigure(1, weight=1)
        self.table.grid_columnconfigure(1, weight=1)
        for i, cell in enumerate(self.table_header):
            cell.grid(row=0, column=i, padx=20, pady=5)
        for i, row in enumerate(self.table_widgets):
            for j, cell in enumerate(row):
                cell.grid(row=i+1, column=j, padx=20, pady=5)
        
        self.add_button.pack(padx=20, pady=20, side="left")

    def refresh(self):
        self.destroy()
        self.__init__(self.master)
        self.layout()

class AddCalendarWindow(ctk.CTkToplevel):
    def __init__(self, calendarframe_instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x400")

        self.calendarframe_instance = calendarframe_instance

        self.calendar_date_entry = None
        self.calendar_operation_entry = None

        self.day_label = ctk.CTkLabel(self, text="Day (dd)")
        self.month_label = ctk.CTkLabel(self, text="Month (mm)")
        self.year_label = ctk.CTkLabel(self, text="Year (yyyy)")
        self.hour_label = ctk.CTkLabel(self, text="Hour (hh)")

        self.day_feild = ctk.CTkEntry(self)
        self.month_feild = ctk.CTkEntry(self)
        self.year_feild = ctk.CTkEntry(self)
        self.hour_feild = ctk.CTkEntry(self)

        self.operation_label = ctk.CTkLabel(self, text="Operation")
        operation_feild_var = ctk.StringVar(value="Operation")
        self.operation_feild = ctk.CTkOptionMenu(self, values=list(dh.operations.keys()), variable=operation_feild_var)

        self.submit_button = ctk.CTkButton(self, text="Add", command=self.calendar_add_entry)
        
        self.layout()

    def layout(self):
        # Day
        self.day_label.grid(row=0, column=0, padx=5, pady=10)
        self.day_feild.grid(row=1, column=0, padx=5, pady=10)

        # Month
        self.month_label.grid(row=0, column=1, padx=5, pady=10)
        self.month_feild.grid(row=1, column=1, padx=5, pady=10)

        # Year
        self.year_label.grid(row=0, column=2, padx=5, pady=10)
        self.year_feild.grid(row=1, column=2, padx=5, pady=10)

        # Hour
        self.hour_label.grid(row=0, column=3, padx=5, pady=10)
        self.hour_feild.grid(row=1, column=3, padx=5, pady=10)

        # Operation
        self.operation_feild.grid(row=1, column=4, columnspan=4, padx=5, pady=10)

        # Submit Button
        self.submit_button.grid(row=2, column=0, columnspan=4, padx=5, pady=10)

    def calendar_add_entry(self):
        day = self.day_feild.get()
        month = self.month_feild.get()
        year = self.year_feild.get()
        hour = self.hour_feild.get()
        minute = "00"
        second = "00"
        self.calendar_date_entry = f"{day}/{month}/{year} {hour}:{minute}:{second}"
        self.calendar_operation_entry = self.operation_feild.get()
        if (self.calendar_date_entry is None) or (self.calendar_operation_entry is None):
            return None
        entry = (self.calendar_date_entry, self.calendar_operation_entry)
        with sqlite3.connect('Storage_solution_DB.db') as conn:
            cursor = conn.cursor()
            action = f"""INSERT INTO Calendar (datetime_id, operation_id)
                VALUES
                {entry};"""
            cursor.execute(action)
        dh.calendar.append((string_to_datetime(entry[0]), entry[1]))
        dh.calendar.sort()
        #new_values = [[datetime_to_string(i[0]), i[1]] for i in calendar]
        #self.calendar_table.update_values(new_values)
        self.calendarframe_instance.refresh()
        self.destroy()

class Order(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.title = ctk.CTkLabel(self, text="Orders")
        titlefont = ("Arial", 45, "bold")
        self.title.configure(font = titlefont)

        
        #self.table = CTkTable(master=self, row=len(dh.orders)+1, column=len(self.table_header), values=[self.table_header] + table_values)
        self.table = ctk.CTkFrame(master=self)
        table_header_font = ("Arial", 15, "bold")
        self.table_header = [ctk.CTkLabel(self.table, text=i) for i in ["Item", "Quantity", "Status", "Options"]]
        for i, cell in enumerate(self.table_header):
            cell.configure(font = table_header_font)
        table_values = [list(i)[:3] + [dh.order_status[i[0]]] for i in dh.orders]
        self.table_widgets = [[ctk.CTkLabel(self.table, text=i) for i in v[1:]] + [ctk.CTkButton(self.table, text="Info", command=self.give_info(v[0])), ctk.CTkButton(self.table, text="Options", command=lambda arg=v[0]: self.options(arg))] for v in table_values]

        self.add_order_button = ctk.CTkButton(master=self, text="Make order", command=self.add_order)
        self.layout()

        self.toplevel_window = None

    def add_order(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = AddOrderWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it
        return self.toplevel_window
    
    def options(self, order_id):
        if dh.order_status[order_id] == "to be ordered":
            answer = CTkMessagebox(message=f"This order is to be sent out on {dh.orders[3]}", icon="question", option_1="Order now", option_2="Delete order").get()
        elif dh.order_status[order_id] == "not recived, overdue" or dh.order_status[order_id] == "not recived, in transit":
            answer = CTkMessagebox(message=f"This order is {dh.order_status[order_id]}", icon="question", option_1="Mark as recived", option_2="Delete order").get()
        else:
            return CTkMessagebox(message="This order has already been recived.", icon="info").get()
        
        if answer == "Order now":
            self.order_now(order_id)
        elif answer == "Delete order":
            self.delete_order(order_id)
        elif answer == "Mark as recived":
            self.mark_recived(order_id)


    def delete_order(self, order_id):
        confirmation = CTkMessagebox(message="Are you sure you want to delete this entry?", icon="question", option_1="No", option_2="Yes").get()
        if confirmation == "Yes":
            with sqlite3.connect('Storage_solution_DB.db') as conn:
                cursor = conn.cursor()
                action = f"""DELETE FROM Orders WHERE order_id = \"{order_id}\";"""
                cursor.execute(action)
            dh.orders = [i for i in dh.orders if i[0] != order_id]
            self.refresh()

    def give_info(self, order_id):
        return lambda: CTkMessagebox(message=dh.order_message[order_id], icon="info").get()
    
    def mark_recived(self, order_id):
        with sqlite3.connect('Storage_solution_DB.db') as conn:
            cursor = conn.cursor()
            action = f"""UPDATE Orders SET received_date = \"{datetime_to_string(dt.now())}\" WHERE order_id = \"{order_id}\";"""
            cursor.execute(action)
        #print(order_id)
        dh.__init__()
        self.refresh()
    
    def order_now(self, order_id):
        with sqlite3.connect('Storage_solution_DB.db') as conn:
            cursor = conn.cursor()
            action = f"""UPDATE Orders SET order_date = \"{dh.now_string}\" WHERE order_id = \"{order_id}\";"""
            cursor.execute(action)
        dh.__init__()
        self.refresh()

    def refresh(self):
        self.destroy()
        self.__init__(self.master)
        self.layout()

    def layout(self):
        self.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        self.title.pack(padx=20, pady=20, side="top")

        #self.table.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        self.table.pack(padx=20, pady=20, side="top")
        self.table.grid_rowconfigure(1, weight=1)
        self.table.grid_columnconfigure(1, weight=1)
        for i, cell in enumerate(self.table_header):
            cell.grid(row=0, column=i, padx=20, pady=5)
        for i, row in enumerate(self.table_widgets):
            for j, cell in enumerate(row):
                cell.grid(row=i+1, column=j, padx=20, pady=5)

        self.add_order_button.pack(padx=20, pady=20, side="left")

class AddOrderWindow(ctk.CTkToplevel):
    def __init__(self, app_instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x400")

        self.app_instance = app_instance

        self.order_item_entry = None
        self.order_quantity_entry = None

        self.item_label = ctk.CTkLabel(self, text="Item")
        self.quantity_label = ctk.CTkLabel(self, text="Quantity")

        self.item_feild = ctk.CTkOptionMenu(self, values=list(dh.storage.keys()))
        self.quantity_feild = ctk.CTkEntry(self)

        self.submit_button = ctk.CTkButton(self, text="Add", command=self.add_order)
        
        self.layout()

    def layout(self):
        # Item
        self.item_label.grid(row=0, column=0, padx=5, pady=10)
        self.item_feild.grid(row=1, column=0, padx=5, pady=10)

        # Quantity
        self.quantity_label.grid(row=0, column=1, padx=5, pady=10)
        self.quantity_feild.grid(row=1, column=1, padx=5, pady=10)

        # Submit Button
        self.submit_button.grid(row=2, column=0, columnspan=4, padx=5, pady=10)

    def add_order(self):
        item = self.item_feild.get()
        quantity = self.quantity_feild.get()
        if (item is None) or (quantity is None):
            return None
        #entry = (item, quantity)
        with sqlite3.connect('Storage_solution_DB.db') as conn:
            cursor = conn.cursor()
            action = f"""INSERT INTO Orders (storage_id, quantity, order_date, estimated_delivery_date, received_date)
                VALUES
                (\"{item}\", {quantity}, \"{dh.now_string}\", \"unknown\", \"not recived\");"""
            cursor.execute(action)
        dh.orders.append((cursor.lastrowid, item, quantity, dh.now_string, "unknown", "not recived"))
        #new_values = [list(i)[1:] for i in orders]
        #self.order_table.update_values(new_values)
        self.app_instance.refresh()
        self.destroy()

class NotificationCenter(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.title = ctk.CTkLabel(self, text="Notification Center")

        self.notifications = CTkListbox(self, command=self.notif_info)
        for n, N in enumerate(dh.notifications.keys()):
            self.notifications.insert(n, N)
        
        self.colorcode()
        
        #self.notifications.insert("END", "")
        self.layout()

    def notif_info(self, event):
        message = dh.notifications[event]
        answer = CTkMessagebox(message=message, icon="info", option_1="Ok", option_2="Place order").get()
        if answer == "Place order":
            self.master.tab.set("Orders")
            self.master.order.add_order()

        self.colorcode()
    
    def colorcode(self):
        for n, N in enumerate(dh.notifications.keys()):
            self.notifications.buttons[n].configure(fg_color = dh.notificationurgency[N])
    
    def refresh(self):
        self.destroy()
        self.__init__(self.master)
        self.layout()

    def layout(self):
        self.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.title.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.notifications.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

class toolbar(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.refresh_button = ctk.CTkButton(self, text="Refresh", command=self.refresh_app)

        self.layout()
    
    def refresh_app(self):
        log.addp("Refreshing the application.")
        dh.__init__()
        self.master.refresh() 

    def layout(self):
        self.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)  # configure grid system
        self.grid_columnconfigure(1, weight=1)
        
        self.refresh_button.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    
if __name__ == "__main__":
    logname = "Datasystemlog"
    filename = "Tkinter.py"
    log = slog.logger(logname + ".log")
    log.add(filename + " started " + dt.now().strftime('%Y-%m-%d %H.%M.%S'))
    log.add(60*"-")
    ctk.set_appearance_mode("Dark")

    date_format = '%d/%m/%Y %H:%M:%S'

    dh = dataHandling()
    app = App()
    app.mainloop()
    log.addp("Application closed.")