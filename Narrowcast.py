import sys
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.dialogs import Querybox
from Helpers import *
from AddLibrary import *
from Cast import *

VERSION = '0.0.1'

class Block:
    def __init__(self, show, order):
        self.show = show
        self.order = order

class Channel:
    def __init__(self, name, block=30):
        self.name = name
        self.block = block
        self.blocks = {}
        self.channelConfig()

    def channelConfig(self):
            # If more block times are added, come up with a better solution here.
            t = []
            for i in range(48):
                placeholder = Block(Show("None", "/place/holder/path"), False)
                t.append(placeholder)

            if(self.block == 60):
                self.blocks = {'0:00': t[0], '1:00': t[1], '2:00': t[2], '3:00': t[3], '4:00': t[4],
                               '5:00': t[5], '6:00': t[6], '7:00': t[7], '8:00': t[8], '9:00': t[9],
                               '10:00': t[10], '11:00': t[11], '12:00': t[12], '13:00': t[13], '14:00': t[14],
                               '15:00': t[15], '16:00': t[16], '17:00': t[17], '18:00': t[18], '19:00': t[19],
                               '20:00': t[20], '21:00': t[21], '22:00': t[22], '23:00': t[23]}
            elif(self.block == 30):
                self.blocks = {'0:00': t[0], '0:30': t[1], '1:00': t[2], '1:30': t[3], '2:00': t[4],
                               '2:30': t[5], '3:00': t[6], '3:30': t[7], '4:00': t[8], '4:30': t[9],
                               '5:00': t[10], '5:30': t[11], '6:00': t[12], '6:30': t[13], '7:00': t[14],
                               '7:30': t[15], '8:00': t[16], '8:30': t[17], '9:00': t[18], '9:30': t[19],
                               '10:00': t[20], '10:30': t[21], '11:00': t[22], '11:30': t[23], '12:00': t[24],
                               '12:30': t[25], '13:00': t[26], '13:30': t[27], '14:00': t[28], '14:30': t[29],
                               '15:00': t[30], '15:30': t[31], '16:00': t[32], '16:30': t[33], '17:00': t[34],
                               '17:30': t[35], '18:00': t[36], '18:30': t[37], '19:00': t[38], '19:30': t[39],
                               '20:00': t[40], '20:30': t[41], '21:00': t[42], '21:30': t[43], '22:00': t[44],
                               '22:30': t[45], '23:00': t[46], '23:30': t[47]}

class ChannelGUI(ttk.Frame):
    def __init__(self, args):
        super().__init__(args)
        self.pack(fill=BOTH, expand=YES)
        self.libraries = []
        self.channels = []
        self.tabs = {}
        self.chosen = ""
        self.choices = []
        self.slotboxes = []
        self.schedules = {}

        def about():
            Messagebox.ok(message='NarrowCast version: %s' % VERSION)

        def newLibrary():
            name = Querybox.get_string(prompt='Enter Library Name', title='New Channel')
            path = Querybox.get_string(prompt='Enter Library Path', title='New Channel')
            library = addNewLibrary(name, path)
            self.libraries.append(library)
            save_object(self.libraries, 'libraries.pkl')
            refreshLibraries()

        def delLibrary():
            pass

        def refreshLibraries():
            for lib in self.libraries:
                try:
                    libtv.insert('', END, iid=lib.name, values=[lib.name])
                except:
                    pass
                for show in lib.shows:
                    try:
                        libtv.insert(lib.name, END, iid=show.name, values=[show.name])
                    except:
                        pass

        def getShowsFromLibrary(name):
            for lib in self.libraries:
                if(lib.name == name):
                    ret = []
                    for show in lib.shows:
                        ret.append(show.name)
                    return ret
            return "Library not found."

        def newChannel():
            name = Querybox.get_string(prompt='Enter Channel Name', title='New Channel')
            self.channels.append(Channel(name))
            refreshChannels()

        def editChannel():
            edit = ttk.Toplevel(title='Edit Channels')
            selected = ttk.StringVar()
            r = 0
            for channel in self.channels:
                ttk.Radiobutton(edit, text=channel.name, value=channel.name, variable=selected).grid(row=r, column=0, sticky=W)
                r += 1

            btn = ttk.Button(master=edit, text='Delete', compound=LEFT, command=lambda: [delChannel(selected.get()), edit.destroy()])
            btn.grid(row=0, column=1)
            btn = ttk.Button(master=edit, text='OK', compound=LEFT, command=lambda: edit.destroy())
            btn.grid(row=2, column=1)

        def delChannel(name):
            self.tabs[name].destroy()
            del self.tabs[name]
            try:
                del self.channels[self.channels.index(getChannel(name))]
            except:
                print(name + " not found in Channels.")
            refreshChannels()

        def refreshChannels():
            for channel in self.channels:
                if(channel.name not in self.tabs):
                    uiDic = {}
                    tv = ttk.Frame(notebook)
                    notebook.add(tv, text=[channel.name])
                    i = 0
                    j = 0
                    for slot, show in channel.blocks.items():
                        lbl = ttk.Label(tv, text=slot).grid(row=j, column=i)
                        slotted = ttk.Combobox(tv, width = 20, state=READONLY)
                        slotted.grid(row=j+1, column=i)
                        self.slotboxes.append(slotted)
                        shuf = ttk.IntVar()
                        chk = ttk.Checkbutton(tv, text="Shuffled", variable=shuf).grid(row=j+2, column=i)
                        uiDic[slot] = (slotted, shuf)
                        i = i + 1
                        if(i == 6):
                            i = 0
                            j = j + 3

                    ttk.Button(master=tv, text='Save Schedule', command=lambda: saveSchedule(channel, uiDic)).grid(row=j+1, column=6)
                    self.tabs[channel.name] = tv
            save_object(self.channels, 'channels.pkl')

        def getChannel(name):
            for channel in self.channels:
                if(channel.name == name):
                    return channel
            return

        def saveSchedule(channel, uiDic):
            schedule = {}
            for slot, show in channel.blocks.items():
                name = uiDic[slot][0].get()
                shuf = uiDic[slot][1].get()
                done = False
                for lib in self.libraries:
                    for s in lib.shows:
                        if(s.name == name):
                            schedule[slot] = (s, shuf)
                            done = True
                        if(done):
                            break
                    if(done):
                        break
                if(done == False):
                    print("Show not found")

            self.schedules[channel] = schedule
            save_object(self.schedules, 'schedules.pkl')

        def onTreeSelect(event):
            self.chosen = libtv.selection()[0]
            getUpdateData()

        def getUpdateData():
            self.choices = getShowsFromLibrary(self.chosen)
            for box in self.slotboxes:
                box['values'] = self.choices

        def narrowCast():
            cast(self.schedules, "G:\Cartoons\Shorts and Station IDs")

        # buttonbar
        buttonbar = ttk.Frame(self, style='primary.TFrame')
        buttonbar.pack(fill=X, pady=1, side=TOP)

        btn = ttk.Button(master=buttonbar, text='Add New Channel', compound=LEFT, command=newChannel)
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        btn = ttk.Button(master=buttonbar, text='Edit Channels', compound=LEFT, command=editChannel)
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        btn = ttk.Button(master=buttonbar, text='Add New Library', compound=LEFT, command=newLibrary)
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        btn = ttk.Button(master=buttonbar, text='Remove Library', compound=LEFT, command=delLibrary)
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        btn = ttk.Button(master=buttonbar, text='About', compound=LEFT, command=about)
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        btn = ttk.Button(master=buttonbar, text='NarrowCast!', compound=LEFT, command=narrowCast)
        btn.pack(side=RIGHT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        #Library Frame
        left_panel = ttk.Frame(self)
        left_panel.pack(side=LEFT, fill=Y)

        libFrame = ttk.Frame(left_panel)
        libFrame.pack()

        libtv = ttk.Treeview(libFrame, columns=(('Libraries')), selectmode='browse', show='tree', padding=1)
        libtv.column('#0', width=1)
        libtv.bind("<<TreeviewSelect>>", onTreeSelect)

        libtv.pack()

        ##Channel Frame
        right_panel = ttk.Frame(self, padding=(2, 1))
        right_panel.pack(side=RIGHT, fill=BOTH, expand=YES)

        notebook = ttk.Notebook(right_panel)
        notebook.pack()

        try:
            with open('libraries.pkl', 'rb') as libs:
                self.libraries = pickle.load(libs)
            refreshLibraries()
        except:
            print('No libraries.pkl file detected.')

        try:
            with open('channels.pkl', 'rb') as chns:
                self.channels = pickle.load(chns)
            refreshChannels()
        except:
            print('No channels.pkl file detected.')

        try:
            with open('schedules.pkl', 'rb') as dic:
                self.schedules = pickle.load(dic)
        except:
            print('Schedules not loaded.')

if __name__ == '__main__':
    root = ttk.Window(title='NarrowCast', iconphoto='icon.png')
    ChannelGUI(root)
    root.mainloop()
