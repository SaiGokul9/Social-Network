from tkinter import *
from ast import literal_eval
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np

users = []
groups = []


class User:
    def __init__(self, id1):
        self.id = id1
        self.contact = set()
        self.messages = []
        self.messages.append("Good")
        self.images = set()
        self.grp = set()

    def add_contact(self, id2):
        self.contact.add(id2)

    def add_message(self, message):
        self.messages.append(message)

    def add_grp(self,id3):
        self.grp.add(id3)
        #print(self.grp)

    def add_image(self, image):
        self.images.add(image)




class Group:
    def __init__(self, id1):
        self.id = id1
        self.members = set()

    def add_member(self, id2):
        self.members.add(id2)


def return_index(id_2):
    list_1 = ["User", 1]
    pro=True

    for x in range(len(users)):
        if users[x].id == id_2:
            list_1[1] = x
            pro=False
            return list_1


    if(pro):
        for y in range(len(groups)):
            if groups[y].id == id_2:
                list_1[1] = y
                list_1 = "Group"
                return list_1




with open("social_network.txt", "r") as file:
    data = file.readlines()
    part_users = False
    part_groups = False

    for line in data:
        if "#users" in line:
            part_users = True
            part_groups = False
        elif "#groups" in line:
            part_groups = True
            part_users = False
        elif part_users:
            #print("found users")
            temp = User(int(line[1:line.index(':')]))
            users.append(temp)
            word = line[(line.index(':'))+2:len(line)-2]
            word1 = word.split(", ")
            for number in word1:
                #print(number)
                temp.add_contact(int(number))
        elif part_groups:
            #print("found groups")
            temp = Group(int(line[1:line.index(':')]))
            groups.append(temp)
            word = line[(line.index(':'))+2:len(line)-2]
            word1 = word.split(", ")
            for number in word1:
                temp.add_member(int(number))
                users[return_index(int(number))[1]].add_grp(temp.id)
                #print(users[return_index(int(number))[1]].grp)

print(len(users))




class Frame_1(Frame):
    def __init__(self, index, master):
        Frame.__init__(self,master,bg='light green')
        self.grid(row=0, sticky=S + N + E + W)
        master.geometry('{}x{}'.format(500, 500))
        self.contact_list = users[index].contact
        print(self.contact_list)
        self.lab1 = Label(self,text = "Contact List",width = 15,height = 4)
        self.lab1.grid(row =0 ,column=0)
        self.lab2 = Label(self,text=self.contact_list,width = 10,height=5)
        self.lab2.grid(row=0, column=1)

class Frame_2(Frame):
    def __init__(self,index,master):
        Frame.__init__(self,master,bg='yellow')
        self.grid(row=1, sticky=S + N + E + W)
        master.geometry('{}x{}'.format(500, 500))
        self.contact_list = users[index].grp
        print(users[index].grp)
        self.lab1 = Label(self,text = "Groups",width = 15,height = 4)
        self.lab1.grid(row=0, column=0)
        self.lab2 = Label(self,text = self.contact_list,width = 15,height = 5)
        self.lab2.grid(row=1, column = 1)

class Frame_3(Frame):
    def __init__(self,index,master):
        Frame.__init__(self,master,bg='light blue')
        self.grid(row=2, sticky=S + N + E + W)
       # master.geometry('{}x{}'.format(500, 500))
        self.contact_list = users[index].messages[0]
        print(users[index].messages)
        self.lab1 = Label(self,text = "Incoming Messages",width = 200,height = 40)
        self.lab1.grid(row =0 ,column=0)
        self.lab2 = Label(self,text = "Hlo",width = 150,height = 4)
        self.lab2.grid(row=0,column=1)

class Frame_4(Frame):
    def __init__(self,index,master):
        Frame.__init__(self,master,bg='red')
        self.grid(row=1, column=1, sticky=S + N + E + W)
        master.geometry('{}x{}'.format(500, 500))
        self.lab1 = Label(self, text="Message to be posted")
        self.lab1.grid(row=0, column=0)
        self.exprtext = Text(self, width=5, height=3)
        self.exprtext.insert(END, "Enter Message to be sent ")
        self.exprtext.grid(row=0, column=1, columnspan=2)

        self.lab2 = Label(self, text="Id of receiver(group/user) of the message")
        self.lab2.grid(row=1, column=0)

        self.id_receiver = Text(self, width=5, height=3)
        self.id_receiver.insert(END, "Enter ID")
        self.id_receiver.grid(row=1, column=1, columnspan=2)

        self.evaluatebutton = Button(self, text="Send", command=self.post_msg, width=10, height=2, padx=2, pady=20)
        self.evaluatebutton.grid(row=2, column=1)

    def post_msg(self):
        self.str='User'
        self.index_receiver = return_index(self.id_receiver)
        if (self.index_receiver)[0] == self.str:
            ((users[self.index_receiver[1]]).messages).append(self.exprtext)
        else:
            for x in (groups[self.index_receiver[1]].members):
                (x.messages).add(self.exprtext)


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.index = 1
        master.geometry('{}x{}'.format(1000, 1000))

        menu = Menu(self.master)
        self.master.config(menu=menu)

        user_menu = Menu(menu)
        menu.add_cascade(label="Choose User",menu=user_menu)


        for x in users:
            user_menu.add_command(label=x.id,command=self.update_index(x.id))


        master.wm_title("Social Media Network")
        self.grid(row=0, column=0, sticky="nsew")

        self.frame_1 = Frame_1(self.index, master)
        self.frame_2 = Frame_2(self.index, master)
        self.frame_3 = Frame_3(self.index, master)
        #self.frame_4 = Frame_4(self.index, master)

    def update_index(self, id_i):
        self.index = return_index(id_i)[1]




root = Tk()
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='New')
filemenu.add_command(label='Open...')
app = Window(root)

root.mainloop()
