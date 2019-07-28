# Project
# Names : Michael Shriki & Or Ella
# ID : 305599417 & 203304969
# E-MAILS: Shriki001@gmail.com & Or7ella@gmail.com

from tkinter import *
from tkinter import messagebox as msg
from tkinter.ttk import Combobox
import csv
from tkinter import filedialog
from datetime import datetime

first_name = 0
last_name = 1
parameter = 2
value = 3
unit = 4
start_time = 5
transaction_time = 7
the_list = 1


class MyEntry(Entry):
    def __init__(self, master, string, row, col, pad):
        Entry.__init__(self, master, validate="key")
        self.string = string
        self.insert(0, self.string)
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self.grid(row=row, column=col, padx=pad)

    def foc_in(self, *args):
        self.delete('0', 'end')

    def foc_out(self, *args):
        if self.get() == '':
            self.insert(0, self.string)


def print_titles(root):
    Label(root, text="Client First Name", font="bold 11 underline").grid(row=3, column=0)
    Label(root, text="Client Last Name", font="bold 11 underline").grid(row=3, column=1)
    Label(root, text="Parameter Value", font="bold 11 underline").grid(row=3, column=2)
    Label(root, text="Valid Start Time", font="bold 11 underline").grid(row=3, column=3)
    Label(root, text="Transaction Time", font="bold 11 underline").grid(row=3, column=4)
    Label(root, text="Valid Data", font="bold 11 underline").grid(
        row=3, column=5)


def print_line(root, line, index, color):
    label = []
    j = 0
    to_print = 0
    last = ""
    for i in line:
        if line[8] == 'DELETED':
            color = 'red'
        if line[8] == 'UPDATED':
            color = 'green'
        if j == 2 or j == 6:
            pass

        elif j == 3:
            last = i
        elif j == 4:
            tmp = Label(root, text=last+" "+i, bg=color)
            tmp.grid(row=index, column=to_print)
            label.append(tmp)
            to_print += 1
        else:
            tmp = Label(root, text=i, bg=color)
            tmp.grid(row=index, column=to_print)
            label.append(tmp)
            to_print += 1
        j += 1
    return label


def create_list(lst, s_time, e_time):
    data = []
    for line in lst:
        the_date = datetime.strptime(line[1][start_time], '%d/%m/%Y %H:%M')
        if s_time <= the_date <= e_time:
            data.append(line)
    return data


def combo_post_command(lst):
    the_list = []
    for line in lst:
        the_list.append(line[1][parameter])
    return sorted(list(set(the_list)))


class SampleApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.attributes("-fullscreen", True)
        self.title("Doctor's Program")
        self.protocol("WM_DELETE_WINDOW", self.exitok)
        self.db_list = []
        self.db_name = ""
        img = PhotoImage(file='icon.png')
        self.tk.call('wm', 'iconphoto', self._w, img)
        self.changes = False
        self.status = Label(self, text="Welcome To The Program", bd=1, relief='sunken', anchor='w')
        self.now = '1/12/2016 00:00'
        self.container = Frame(self)
        self.firstpagemenu()
        self.container.pack(side="top", fill="both", expand=True)
        self.status.pack(side='bottom', fill='x')
        self.frames = {}
        for f in (StartPage, Page1, Page2, Page3, Page4, Page5, Page6, Page7,
                  Page8, Page9):
            page_name = f.__name__
            frame = f(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage", 0)

    def remove_line(self, index):
        i = 0
        for line in self.db_list:
            if i == index:
                self.db_list[index][8] = 'DELETED'
            i += 1

    def insert_line(self, index, line):
        self.db_list.insert(index, line)

    def update_line(self, index, val, transaction):
        self.db_list[index][value] = val
        self.db_list[index][transaction_time] = transaction
        self.db_list[index][8] = 'UPDATED'

    def set_change(self, ch):
        self.changes = ch

    def create_menu(self):
        menu = Menu(self)
        self.config(menu=menu)
        sub_menu = Menu(menu, tearoff=0)
        sub_menu2 = Menu(menu, tearoff=0)
        sub_menu3 = Menu(menu, tearoff=0)
        menu.add_cascade(label="Queries", menu=sub_menu)
        menu.add_cascade(label="DB", menu=sub_menu2)
        menu.add_cascade(label="Help", menu=sub_menu3)
        sub_menu.add_command(label="Search Client By Parameter", command=self.showsearch)
        sub_menu.add_command(label="Get Data By Date", command=self.showgetdata)
        sub_menu.add_command(label="Get Client History", command=self.showhistory)
        sub_menu.add_command(label="Remove Client Data",
                             command=self.showremove)
        sub_menu.add_command(label="Update Client Data",
                             command=self.showupdate)
        sub_menu.add_command(label="Add New Client", command=self.showaddclient)
        sub_menu.add_command(label="Chane Now Time",
                              command=self.changetime)
        sub_menu.add_command(label="Exit", command=self.exit)
        sub_menu2.add_command(label="Save Changes To DB", command=self.savetodb)
        sub_menu2.add_command(label="Open New DB File", command=self.opennewfile)
        sub_menu3.add_command(label="Readme", command=self.readme)

    def firstpagemenu(self):
        menu = Menu(self)
        self.config(menu=menu)
        sub_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=sub_menu)
        sub_menu.add_command(label="Choose Working DB",
                             command=self.showfirstpage)
        sub_menu.add_command(label="Readme", command=self.readme)
        sub_menu.add_command(label="Exit", command=self.exit)

    def showfirstpage(self):
        self.show_frame("StartPage", 0)

    def savetodb(self):
        if not self.changes:
            msg.showerror('Error', 'No Changes Has Made!')
            return

        with open(self.db_name, mode='w', newline='') as file:
            db_writer = csv.writer(file)
            for line in self.db_list:
                db_writer.writerow(line)
        self.set_change(False)
        msg.showinfo("Success!", "Data Save To DB Successfully")

    def showsearch(self):
        self.show_frame("Page1", 0)

    def showgetdata(self):
        self.show_frame("Page2", 0)

    def showhistory(self):
        self.show_frame("Page3", 0)

    def showremove(self):
        self.show_frame("Page4", 0)

    def showaddclient(self):
        self.show_frame("Page5", 0)

    def showupdate(self):
        self.show_frame("Page6", 0)

    def opennewfile(self):
        self.show_frame("Page7", 0)

    def readme(self):
        self.show_frame("Page8", 0)

    def changetime(self):
        self.show_frame("Page9", 0)

    def exit(self):
        if self.changes:
            res = msg.askyesno("Warning", "You Have Some Changes To Commit!\nClose Without Commit?")
            if res:
                self.destroy()
        else:
            self.exitok()

    def exitok(self):
        res = msg.askyesno("Exit", "Are You Sure?")
        if res:
            self.destroy()

    def getdate(self):
        return self.now

    def setdate(self, date):
        self.now = date

    def setstatus(self, string):
        self.status.destroy()
        self.status = Label(self, text=string, bd=1, relief='sunken', anchor='w')
        self.status.pack(side='bottom', fill='x')

    def get_data(self):
        new_list = list(enumerate(self.db_list))
        return new_list

    def set_data(self, lst):
        self.db_list.append(lst)

    def create_client_list(self, fname, lname, param):
        if fname == 'First Name' or lname == 'Last Name' or \
                fname == '' or lname == '':
            msg.showerror("Error", "No First Name Or Last Name!")
            return -1

        if param == 'Parameter' or param == '':
            msg.showerror("Error", "No Parameter To Check!")
            return -1
        db_lst = self.get_data()
        _list = []
        filter_list = filter(lambda line:line[1][first_name].lower() == fname.lower()\
                                         and line[1][last_name].lower() == lname.lower(), db_lst)
        for line in filter_list:
            _list.append(line)
        if len(_list) == 0:
            msg.showerror("Error", "Client "+fname.title()+" " + lname.title()+" doesn't Exist")
            return -1

        the_list = []
        filter_list = filter(lambda line: line[1][parameter].lower() == param.lower(), _list)

        for line in filter_list:
                the_list.append(line)

        if len(the_list) == 0:
            msg.showerror("Error", "No Data Of "+param+" For "\
                          +fname.title()+" "+lname.title()+"!")
            return -1
        return the_list

    def show_frame(self, page_name, filename):
        if page_name == "Page1" and filename != 0:
            try:
                with open(filename, 'r') as file:
                    self.db_list = list(csv.reader(file))
                    self.db_name = filename
            except IOError:
                msg.showerror("Error", "Cant Open File")
                return
            self.create_menu()
            self.protocol("WM_DELETE_WINDOW", self.exit)
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(Frame):
    """
           the 1st page that open the db file
        """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.filename = ""
        self.label = Label(self, text="Welcome Doctor!", font="none 32 underline", pady=20)
        self.label2 = Label(self, text="Choose DB File To Open", font="none 20", pady=20)
        self.label2.grid(row=1, columnspan=3, padx=300)
        self.label.grid(row=0, columnspan=3, padx=300)
        self.choosefile = Button(self, text="Choose File", cursor='hand2')
        self.choosefile.grid(row=2, columnspan=3)
        self.choosefile.bind("<Button-1>", self.openfile)
        self.button1 = Button(self, text="Continue", cursor='hand2')
        self.button1.bind('<Button-1>', self.click)
        self.button1.grid(row=4, columnspan=3, padx=300, pady=10)

    def openfile(self, event):
        self.opendbfile()

    def opendbfile(self):
        self.filename = filedialog.askopenfilename\
            (title="Select file", filetypes=(("csv files", "*.csv"),
                                             ("all files", "*.*")))
        Label(self, text=self.filename).grid(row=3, column=0, pady=10, padx=300)

    def click(self, event):
        if self.filename == "":
            msg.showerror("Error", "No File Was Selected!")
            return

        if not self.filename.endswith(".csv"):
            msg.showerror("Error", "Not A Supported File!")
            return

        self.controller.show_frame("Page1", self.filename)


class Page1(Frame):
    """
           search for client data by parameter
        """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        Label(self, text="Search Client", font="none 32 underline").grid(row=0, columnspan=6, pady=10, padx=50)
        self.label = []
        self.selector = []
        self.entry_1 = MyEntry(self, 'First Name', 2, 0, 10)
        self.entry_2 = MyEntry(self, 'Last Name', 2, 1, 10)
        self.entry_3 = Combobox(self, value=self.selector, height=6, postcommand=self.combo_post_command)
        self.entry_3.insert(0, 'Parameter')
        self.entry_3.grid(row=2, column=2, padx=10)
        go_btn = Button(self, text="Search", cursor='hand2')
        go_btn.bind('<Button-1>', self.click)
        go_btn.grid(row=2, column=3, padx=40)

    def combo_post_command(self):
        db_list = self.controller.get_data()
        self.entry_3['values'] = combo_post_command(db_list)

    def click(self, event):
        self.send_query(self.entry_1.get(), self.entry_2.get(), self.entry_3.get())

    def send_query(self, fname, lname, param):
        _list = self.controller.create_client_list(fname, lname, param)
        
        if _list == -1:
            return
        self.controller.setstatus("Getting " + fname + " " + lname + " " + param + " Data's")
        
        for line in self.label:
            for i in line:
                i.grid_forget()

        print_titles(self)

        i = 4
        for line in _list:
            self.label.append(print_line(self, line[1], i, self.controller.cget('bg')))
            i += 1


class Page2(Frame):
    """
           get client data by date
        """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        Label(self, text="Get Data By Date", font="none 32 underline").\
            grid(row=0, columnspan=4, pady=10, padx=50)
        self.label = []
        self.selector = []
        self.entry_1 = MyEntry(self, 'First Name', 1, 0, 10)
        self.entry_2 = MyEntry(self, 'Last Name', 1, 1, 10)
        self.entry_3 = Combobox(self, value=self.selector, height=6, postcommand=self.combo_post_command)
        self.entry_4 = MyEntry(self, 'The Date', 1, 3, 10)
        self.entry_5 = MyEntry(self, 'Doctor Ask', 1, 4, 10)
        self.entry_3.insert(0, 'Parameter')
        self.entry_3.grid(row=1, column=2, padx=10)
        go_btn2 = Button(self, text="GetData", cursor='hand2')
        go_btn2.bind('<Button-1>', self.clicktoget)
        go_btn2.grid(row=1, column=5, padx=40)

    def combo_post_command(self):
        db_list = self.controller.get_data()
        self.entry_3['values'] = combo_post_command(db_list)

    def clicktoget(self, event):
        self.send_query(self.entry_1.get(), self.entry_2.get(),
                        self.entry_3.get(), self.entry_4.get(), self.entry_5.get())

    def send_query(self, fname, lname, param, time, doctor_time):
        _list = self.controller.create_client_list(fname, lname, param)

        if time == 'The Date' or time == '' or doctor_time == 'Doctor Ask' or doctor_time == '':
            msg.showerror("Error", "No Time To Check!")
            return

        if _list == -1:
            return
        s_time = ""
        e_time = ""
        if len(time) <= 10:
            s_time = time +' 00:00'
            e_time = time +' 23:59'
        else:
            s_time = time
            e_time = time
        if len(doctor_time) <= 10:
            doctor_time += ' 23:59'

        in_s_date = datetime.strptime(s_time, '%d/%m/%Y %H:%M')
        in_e_date = datetime.strptime(e_time, '%d/%m/%Y %H:%M')
        in_doctor_date = datetime.strptime(doctor_time, '%d/%m/%Y %H:%M')
        newlist1 = []
        for line in _list:
            the_date = datetime.strptime(line[1][start_time],
                                         '%d/%m/%Y %H:%M')
            if in_s_date <= the_date <= in_e_date:
                newlist1.append(line)
        for line in newlist1:
            _list.append(line)
        self.showall(fname, lname, param, _list)
        data = []
        val = ""
        for line in _list:
            the_date = datetime.strptime(line[1][transaction_time],
                                         '%d/%m/%Y %H:%M')
            if the_date <= in_doctor_date:
                data.append(line[1][transaction_time])

        if len(data) == 0:
            msg.showinfo("Result:", "No Data!")
            return

        j = 0
        for i in sorted(data):
            val = i
            if i > time:
                val = sorted(data)[j - 1]
                break
            j += 1
        newlist = reversed(_list)
        j = 0
        for line in newlist:
            if line[1][transaction_time] == val:
                msg.showinfo("Result:", line[1][value])
                return

        msg.showinfo("Result:", _list[1][len(_list)-1][value])
        return

    def showall(self, fname, lname, param, lst):
        if lst == -1:
            return
        
        self.controller.setstatus("Getting " + fname + " " + lname + " " + param + " Data's")
        
        for line in self.label:
            for i in line:
                i.grid_forget()

        print_titles(self)
        i = 4
        for line in lst:
            self.label.append(print_line(self, line[1], i, self.controller.cget('bg')))
            i += 1


class Page3(Frame):
    """
           get client history
        """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        Label(self, text="Get Client History", font="none 32 underline"). \
            grid(row=0, columnspan=4, pady=10, padx=50)
        self.label = []
        self.selector = []
        self.entry_1 = MyEntry(self, 'First Name', 1, 0, 10)
        self.entry_2 = MyEntry(self, 'Last Name', 1, 1, 10)
        self.entry_3 = Combobox(self, value=self.selector, height=6, postcommand=self.combo_post_command)
        self.entry_4 = MyEntry(self, 'Valid Time', 1, 3, 10)
        self.entry_5 = MyEntry(self, 'From: 01/1/2016 10:00', 1, 4, 10)
        self.entry_6 = MyEntry(self, 'To: 01/1/2016 10:00', 1, 5, 10)
        self.entry_3.insert(0, 'Parameter')
        self.entry_3.grid(row=1, column=2, padx=10)
        go_btn3 = Button(self, text="History", cursor='hand2')
        go_btn3.bind('<Button-1>', self.clicktohistory)
        go_btn3.grid(row=1, column=6)

    def clicktohistory(self, event):
        self.send_query(self.entry_1.get(), self.entry_2.get(),
                         self.entry_3.get(), self.entry_4.get(),
                        self.entry_5.get(), self.entry_6.get())

    def combo_post_command(self):
        db_list = self.controller.get_data()
        self.entry_3['values'] = combo_post_command(db_list)

    def send_query(self, fname, lname, param, valid_time, valid_start_time,
                   end_time):
        _list = self.controller.create_client_list(fname, lname, param)
        if _list == -1:
            return
        self.controller.setstatus("Getting " + fname + " " + lname + " " + param + \
                                  " Data's From " + valid_start_time + " To " + end_time)
        if valid_start_time == 'From: 01/1/2016 10:00' or end_time == 'To: 01/1/2016 10:00' or \
                valid_start_time == '' or end_time == '' or valid_time == 'Valid ' \
                                                                    'Time' or valid_time == '':
            msg.showerror("Error", "No Period Time To Check!")
            return
        valid_start = valid_time + ' 00:00'
        valid_end = valid_time + ' 23:59'
        if len(valid_start_time) <= 10:
            valid_start_time += ' 00:00'
        if len(end_time) <= 10:
            end_time += ' 23:59'

        in_date_start = datetime.strptime(valid_start_time, '%d/%m/%Y %H:%M')
        in_date_end = datetime.strptime(end_time, '%d/%m/%Y %H:%M')
        in_valid_start = datetime.strptime(valid_start, '%d/%m/%Y %H:%M')
        in_valid_end = datetime.strptime(valid_end, '%d/%m/%Y %H:%M')

        for line in self.label:
            for i in line:
                i.grid_forget()

        print_titles(self)

        searchlist = []
        for line in _list:
            the_date = datetime.strptime(line[1][start_time], '%d/%m/%Y %H:%M')
            if in_valid_start <= the_date <= in_valid_end:
                searchlist.append(line)

        data = []
        for line in searchlist:
            the_date = datetime.strptime(line[1][transaction_time], '%d/%m/%Y %H:%M')
            if in_date_start <= the_date <= in_date_end:
                data.append(line[1])

        if len(data) == 0:
            msg.showinfo("Result:", "No Data!")
            return
        i = 4
        for line in data:
            self.label.append(print_line(self, line, i, self.controller.cget('bg')))
            i += 1


class Page4(Frame):
    """
           delete client data
        """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        Label(self, text="Delete Client Data's", font="none 32 underline"). \
            grid(row=0, columnspan=4, pady=10, padx=40)
        self.label = []
        self.selector = []
        self.entry_1 = MyEntry(self, 'First Name', 1, 0, 10)
        self.entry_2 = MyEntry(self, 'Last Name', 1, 1, 10)
        self.entry_3 = Combobox(self, value=self.selector, height=6, postcommand=self.combo_post_command)
        self.entry_4 = MyEntry(self, 'e.g: 01/1/2016 10:00', 1, 3, 10)
        self.entry_3.insert(0, 'Parameter')
        self.entry_3.grid(row=1, column=2, padx=10)
        go_btn = Button(self, text="Search", cursor='hand2')
        go_btn.bind('<Button-1>', self.click)
        go_btn.grid(row=1, column=4, padx=10)
        go_btn4 = Button(self, text="Remove", cursor='hand2')
        go_btn4.bind('<Button-1>', self.clicktoremove)
        go_btn4.grid(row=1, column=5)

    def combo_post_command(self):
        db_list = self.controller.get_data()
        self.entry_3['values'] = combo_post_command(db_list)

    def click(self, event):
        self.showall(self.entry_1.get(), self.entry_2.get(), self.entry_3.get())

    def clicktoremove(self, event):
        self.send_query(self.entry_1.get(), self.entry_2.get(), \
                         self.entry_3.get(), self.entry_4.get())

    def send_query(self, fname, lname, param, time):
        _list = self.controller.create_client_list(fname, lname, param)
        if _list == -1:
            return
        self.controller.setstatus("Removing " + fname + " " + lname + " " + param + " Data's From " + time)
        if time == 'e.g: 01/1/2016 10:00' or time == '':
            msg.showerror("Error", "No Time To Remove!")
            return

        time_start = time + ' 00:00'
        time_end = time + ' 23:59'

        in_date_start = datetime.strptime(time_start, '%d/%m/%Y %H:%M')
        in_date_end = datetime.strptime(time_end, '%d/%m/%Y %H:%M')

        for line in self.label:
            for i in line:
                i.grid_forget()

        filter_list = filter(lambda line:\
                                 in_date_start <=\
                datetime.strptime(line[1][start_time], '%d/%m/%Y %H:%M') <=\
                             in_date_end, _list)
        data = []
        for line in filter_list:
            data.append(list(line))

        if len(data) == 0:
            msg.showinfo("Result:", "No Data!")
            return
        res = msg.askyesno("Warning", "You'r About To Delete Line... Continue?")
        if res:
            self.controller.set_change(True)
            print_titles(self)
            i = 4
            for line in data:
                self.label.append(print_line(self, line[1], i, "yellow"))
                i += 1
            to_remove = data[len(data)-1][0]
            self.controller.remove_line(to_remove)

            i += 1
            tmplb = []
            for j in range(5):
                lb = Label(self, text="------------------------")
                lb.grid(row=i, column=j)
                tmplb.append(lb)
            self.label.append(tmplb)
            i += 1
            for line in data:
                if line[0] == to_remove:
                    continue
                self.label.append(print_line(self, line[1], i, "white"))
                i += 1

    def showall(self, fname, lname, param):
        _list = self.controller.create_client_list(fname, lname, param)
        if _list == -1:
            return
        self.controller.setstatus("Getting " + fname + " " + lname + " " + param + " Data's")
        for line in self.label:
            for i in line:
                i.grid_forget()

        print_titles(self)
        i = 4
        for line in _list:
            self.label.append(print_line(self, line[1], i, self.controller.cget('bg')))
            i += 1


class Page5(Frame):
    """
           add new client
        """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        Label(self, text="Add New Client", font="none 32 underline"). \
            grid(row=0, columnspan=4, pady=10, padx=50)
        self.label = []
        self.selector = []
        self.entry_1 = MyEntry(self, 'First Name', 1, 0, 10)
        self.entry_2 = MyEntry(self, 'Last Name', 2, 0, 10)
        self.entry_3 = MyEntry(self, 'Parameter', 1, 1, 10)
        self.entry_4 = MyEntry(self, 'Value', 2, 1, 10)
        self.entry_5 = MyEntry(self, 'Unit', 3, 1, 10)
        self.entry_6 = MyEntry(self, 'Valid Start Time', 1, 2, 10)
        self.entry_7 = MyEntry(self, 'Valid Stop Time', 2, 2, 10)
        self.entry_5.grid(pady=5)
        go_btn = Button(self, text="Add Client", cursor='hand2')
        go_btn.bind('<Button-1>', self.click)
        go_btn.grid(row=1, column=3, padx=10)

    def click(self, event):
        self.send_query(self.entry_1.get(), self.entry_2.get(), self.entry_3.get(),\
                        self.entry_4.get(), self.entry_5.get(), self.entry_6.get(), self.entry_7.get())

    def send_query(self, fname, lname, param, val, unit, start_time, stop_time):
        if fname == 'First Name' or lname == 'Last Name' or \
                fname == '' or lname == '':
            msg.showerror("Error", "No First Name Or Last Name!")
            return -1

        if param == 'Parameter' or param == '':
            msg.showerror("Error", "No Parameter To Check!")
            return -1

        if val == 'Parameter' or param == '':
            msg.showerror("Error", "No Parameter To Check!")
            return -1

        if unit == 'Parameter' or param == '':
            msg.showerror("Error", "No Parameter To Check!")
            return -1

        if start_time == 'Valid Start Time' or start_time == '':
            msg.showerror("Error", "No Start Time!")
            return -1

        if stop_time == 'Valid Stop Time' or stop_time == '':
            msg.showerror("Error", "No Stop Time!")
            return -1
        self.controller.setstatus("Adding New Client")
        newdata = [fname, lname, param, val, unit, start_time, stop_time, self.controller.getdate()]

        res = msg.askyesno("Warning", "You'r About To Add New Client... Continue?")
        if res:
            self.controller.set_data(newdata)
            self.controller.set_change(True)
        msg.showinfo("Success!", "Client Added Successfully!")


class Page6(Frame):
    """
            update client data
        """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        Label(self, text="Update Client Data's", font="none 32 underline"). \
            grid(row=0, columnspan=4, pady=10, padx=40)
        self.label = []
        self.selector = []
        self.entry_1 = MyEntry(self, 'First Name', 1, 0, 10)
        self.entry_2 = MyEntry(self, 'Last Name', 1, 1, 10)
        self.entry_3 = Combobox(self, value=self.selector, height=6, postcommand=self.combo_post_command)
        self.entry_4 = MyEntry(self, 'Value', 1, 3, 10)
        self.entry_5 = MyEntry(self, 'e.g: 01/1/2016 10:00', 1, 4, 10)
        self.entry_6 = MyEntry(self, 'Doctor Time', 1, 5, 10)
        self.entry_3.insert(0, 'Parameter')
        self.entry_3.grid(row=1, column=2, padx=10)
        go_btn = Button(self, text="Update", cursor='hand2')
        go_btn.bind('<Button-1>', self.click)
        go_btn.grid(row=1, column=6, padx=10)

    def combo_post_command(self):
        db_list = self.controller.get_data()
        self.entry_3['values'] = combo_post_command(db_list)

    def click(self, event):
        self.send_query(self.entry_1.get(), self.entry_2.get(), \
                         self.entry_3.get(), self.entry_4.get(),
                        self.entry_5.get(), self.entry_6.get())

    def send_query(self, fname, lname, param, val, time, doctor_time):
        _list = self.controller.create_client_list(fname, lname, param)
        if _list == -1:
            return

        if val == 'Value' or val == '':
            msg.showerror("Error", "Value Cannot Be Empty!")
            return

        if time == 'e.g: 01/1/2016 10:00' or time == '':
            msg.showerror("Error", "No Time To Update!")
            return

        if len(time) < 10:
            time += ' 00:00'

        if doctor_time == 'Doctor Time' or doctor_time == '':
            msg.showinfo("Note", "Doctor Time Will Be The Now Time!\n\n" +
                         self.controller.getdate())
            doctor_time = self.controller.getdate()

        self.controller.setstatus("Updating " + fname + " " + lname + " " + param + " Data's From " + time)

        in_date = datetime.strptime(time, '%d/%m/%Y %H:%M')
        for line in self.label:
            for i in line:
                i.grid_forget()

        filter_list = filter(lambda line:\
                datetime.strptime(line[1][start_time], '%d/%m/%Y %H:%M') ==\
                             in_date, _list)
        data = []
        for line in reversed(list(filter_list)):
            data.append(list(line))
            break

        if len(data) == 0:
            msg.showinfo("Result:", "No Data!")
            return
        res = msg.askyesno("Warning", "You'r About To Update Line... Continue?")
        if res:
            self.controller.set_change(True)
            print_titles(self)
            i = 4
            for line in data:
                self.label.append(print_line(self, line[1], i, "yellow"))
                i += 1
            to_update = data[len(data)-1][0]
            self.controller.update_line(to_update, val, doctor_time)

            i += 1
            tmplb = []
            for j in range(5):
                lb = Label(self, text="------------------------")
                lb.grid(row=i, column=j)
                tmplb.append(lb)
            self.label.append(tmplb)
            i += 1
            for line in data:
                if line[0] == to_update:
                    line[1][value] = val
                    line[1][transaction_time] = doctor_time
                    self.label.append(print_line(self, line[1], i, "white"))
                i += 1


class Scrolling_Area(Frame, object):
    def __init__(self, master, width=None, anchor=N, height=None,
                 mousewheel_speed=2, scroll_horizontally=True, xscrollbar=None,
                 scroll_vertically=True, yscrollbar=None, background=None,
                 inner_frame=Frame, **kw):
        Frame.__init__(self, master, class_="Scrolling_Area",
                       background=background)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._width = width
        self._height = height

        self.canvas = Canvas(self, background=background, highlightthickness=0,
                             width=650, height=500)
        self.canvas.grid(row=0, column=0, sticky=N + E + W + S)

        if scroll_vertically:
            if yscrollbar is not None:
                self.yscrollbar = yscrollbar
            else:
                self.yscrollbar = Scrollbar(self, orient=VERTICAL)
                self.yscrollbar.grid(row=0, column=1, sticky=N + S)

            self.canvas.configure(yscrollcommand=self.yscrollbar.set)
            self.yscrollbar['command'] = self.canvas.yview
        else:
            self.yscrollbar = None

        if scroll_horizontally:
            if xscrollbar is not None:
                self.xscrollbar = xscrollbar
            else:
                self.xscrollbar = Scrollbar(self, orient=HORIZONTAL)
                self.xscrollbar.grid(row=1, column=0, sticky=E + W)

            self.canvas.configure(xscrollcommand=self.xscrollbar.set)
            self.xscrollbar['command'] = self.canvas.xview
        else:
            self.xscrollbar = None

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.innerframe = inner_frame(self.canvas, **kw)
        self.innerframe.pack(anchor=anchor)

        self.canvas.create_window(0, 0, window=self.innerframe, anchor='nw',
                                  tags="inner_frame")

        self.canvas.bind('<Configure>', self._on_canvas_configure)

        # Mousewheel_Support(self).add_support_to(self.canvas,
        #                                         xscrollbar=self.xscrollbar,
        #                                         yscrollbar=self.yscrollbar)

    @property
    def width(self):
        return self.canvas.winfo_width()

    @width.setter
    def width(self, width):
        self.canvas.configure(width=width)

    @property
    def height(self):
        return self.canvas.winfo_height()

    @height.setter
    def height(self, height):
        self.canvas.configure(height=height)

    def set_size(self, width, height):
        self.canvas.configure(width=width, height=height)

    def _on_canvas_configure(self, event):
        width = max(self.innerframe.winfo_reqwidth(), event.width)
        height = max(self.innerframe.winfo_reqheight(), event.height)

        self.canvas.configure(scrollregion="0 0 %s %s" % (width, height))
        self.canvas.itemconfigure("inner_frame", width=width, height=height)

    def update_viewport(self):
        self.update()

        window_width = self.innerframe.winfo_reqwidth()
        window_height = self.innerframe.winfo_reqheight()

        if self._width is None:
            canvas_width = window_width
        else:
            canvas_width = min(self._width, window_width)

        if self._height is None:
            canvas_height = window_height
        else:
            canvas_height = min(self._height, window_height)

        self.canvas.configure(
            scrollregion="0 0 %s %s" % (window_width, window_height),
            width=canvas_width, height=canvas_height)
        self.canvas.itemconfigure("inner_frame", width=window_width,
                                  height=window_height)


class Page7(Frame):
    """
            open new db file for margin to our db
        """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.localdb = []
        self.lables = []
        self.scrolling_area = Scrolling_Area(self)
        self.rowFrame = Frame(self.scrolling_area.innerframe)
        self.filename = ""
        Label(self, text="Open New DB File", font="none 32 underline"). \
            grid(row=0, columnspan=4, pady=10, padx=50)
        self.go_btn = Button(self, text="Choose File", cursor='hand2')
        self.go_btn.bind('<Button-1>', self.clicktoopen)
        self.go_btn.grid(row=1, column=1, padx=10)

    def clicktoopen(self, event):
        self.filename = filedialog.askopenfilename \
            (title="Select file", filetypes=(("csv files", "*.csv"),
                                             ("all files", "*.*")))
        Label(self, text=self.filename).grid(row=2, column=0, columnspan=2,
                                             pady=10)
        self.openfile()
        self.controller.setstatus("Open New DB File")

    def openfile(self):
        if self.filename == '':
            msg.showerror('Error', 'No File Was Selected!')
            return
        if not self.filename.endswith(".csv"):
            msg.showerror("Error", "Not A Supported File!")
            return
        for line in self.localdb:
            self.localdb.remove(line)
        try:
            with open(self.filename, 'r') as file:
                csv_file = csv.reader(file)
                next(csv_file)
                for line in csv_file:
                    self.localdb.append(line)
        except IOError:
            msg.showerror("Error", "No Such Database")
            return
        for i in self.lables:
            i.grid_forget()

        self.scrolling_area.grid_forget()
        self.rowFrame.grid_forget()

        data = list(enumerate(self.localdb))
        self.scrolling_area = Scrolling_Area(self)
        self.scrolling_area.grid(row=6, rowspan=10, column=1, columnspan=5,
                            sticky='w', pady=20)

        txt = ""
        i = 7
        for line in data:
            if line[1][0] == '' and line[1][1] == "":
                continue
            txt = "\t"+str(line[0]) + ':  ' + line[1][
                first_name]+"\t"+line[1][
                last_name]+"\t"+line[1][
                parameter]+"\t"+line[1][
                value]+" "+line[1][unit]+"\t"+line[1][
                start_time]+"\t\t"+line[1][transaction_time]
            self.rowFrame = Frame(self.scrolling_area.innerframe)
            self.rowFrame.grid(row=i, column=0, sticky='w')
            tmp = Label(self.rowFrame, text=txt)
            tmp.grid(row=i, column=0, sticky='w')
            self.lables.append(tmp)
            i += 1
        self.entry_2 = MyEntry(self, 'e.g: 1', 3, 0, 10)
        self.entry_3 = MyEntry(self, 'db row e.g: 1', 3, 1, 10)
        go_btn = Button(self, text="Marge part", cursor='hand2')
        go_btn.bind('<Button-1>', self.click)
        go_btn.grid(row=3, column=2, padx=10)
        go_btn2 = Button(self, text="Marge All", cursor='hand2')
        go_btn2.bind('<Button-1>', self.margeall)
        go_btn2.grid(row=3, column=3, padx=10)
        go_btn2 = Button(self, text="Replace Line", cursor='hand2')
        go_btn2.bind('<Button-1>', self.replaceline)
        go_btn2.grid(row=3, column=4, padx=10)

    def click(self, event):
        self.margepart(self.entry_2.get())

    def replaceline(self, event):
        self.replace(self.entry_2.get(), self.entry_3.get())

    def margeall(self, event):
        self.margealldb()

    def margealldb(self):
        res = msg.askyesno("Warning", "You'r About To Merge 2 DB Files... Continue?")
        if res:
            self.controller.setstatus("Merge Data's")
            self.controller.set_change(True)
            for line in self.localdb:
                self.controller.set_data(line)
            msg.showinfo("Info", 'DB Merged Successfully!')

    def margepart(self, data):
        if data == 'e.g: 1' or data == '':
            msg.showerror("Error", "No Line Was Choose")
            return
        res = msg.askyesno("Warning", "You'r About To Append line "\
                               + data + " From This DB File... Continue?")
        if res:
            self.controller.setstatus("Merg Data's")
            self.controller.set_change(True)
            i = 0
            for line in self.localdb:
                if i == int(data):
                    self.controller.set_data(line)
                    break
            msg.showinfo("Success", "Line Added Successfully!")

    def replace(self, data, row):
        if data == 'e.g: 1' or data == '' or row == 'db row e.g: 1' or row == '':
            msg.showerror("Error", "No Line Was Choose")
            return
        res = msg.askyesno("Warning", "You'r About To Replace line "\
                               + data + " From This DB File... Continue?")
        if res:
            self.controller.setstatus("Replace Data's")
            self.controller.set_change(True)
            i = 0
            for line in self.localdb:
                if i == int(data):
                    self.controller.remove_line(row)
                    self.controller.insert_line(row, line)
                    break
            msg.showinfo("Success", "Line Replaced Successfully!")


class Page8(Frame):
    """
        README
        """
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        Label(self, text="ReadMe!", font="none 32 underline"). \
            grid(row=0, columnspan=4, pady=10, padx=70)
        Label(self, text="This Program Created By Michael Shriki And Or Ella", font="none 22"). \
            grid(row=1, columnspan=4, pady=10, padx=50)
        Label(self, text="ID:", font="none 20"). \
            grid(row=2, column=0, pady=10)
        Label(self, text="eMail:", font="none 20"). \
            grid(row=3, column=0, pady=10)
        Label(self, text="Shriki001@gmail.com", font="none 20"). \
            grid(row=3, column=1, pady=10)
        Label(self, text="Or7ella@gmail.com", font="none 20"). \
            grid(row=3, column=2, pady=10)
        Label(self, text="© 2019 All Rights Reserved", font="none 18"). \
            grid(row=4, columnspan=4, pady=10, padx=50)


class Page9(Frame):
    """
        Change the now time
        """

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        Label(self, text="Change Now Time", font="none 32 underline"). \
            grid(row=0, columnspan=4, pady=10, padx=70)
        self.e1 = MyEntry(self, 'e.g: 1/12/2016 00:00', 1, 1, 40)
        go_btn = Button(self, text="Change", cursor='hand2')
        go_btn.bind('<Button-1>', self.click)
        go_btn.grid(row=2, column=1, padx=40, pady=40)

    def click(self, event):
        self.dotask(self.e1.get())

    def dotask(self, time):
        if time == 'e.g: 1/12/2016 00:00' or time == '':
            msg.showerror('Error', 'No Time To Change')
            return
        self.controller.setdate(time)
        msg.showinfo('Info', 'Time Change Succssefully To\n\n' + time)


app = SampleApp()
app.mainloop()
