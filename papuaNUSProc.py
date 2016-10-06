#!/usr/bin/env python
from Tkinter import *
from tkMessageBox import askokcancel


class convertNUSBruker(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)

        self.pack()

        self.inputSER = StringVar(value='./ser')
        self.outputTEMPLATE = StringVar(value='./fid/data%03d.fid')
        self.outputSCRIPT = StringVar(value='fid.com')

        ser_entry = Entry(self, width = 20, textvariable = self.inputSER)
        ser_entry.grid(row = 0, column = 1)
        Label(self, text = "Serial File").grid(row = 0, column = 0)

        ser_entry = Entry(self, width = 20, textvariable = self.outputTEMPLATE)
        ser_entry.grid(row = 1, column = 1)
        Label(self, text = "Output Template").grid(row = 1, column = 0)

        ser_entry = Entry(self, width = 20, textvariable = self.outputSCRIPT)
        ser_entry.grid(row = 2, column = 1)
        Label(self, text = "Output Script").grid(row = 2, column = 0)

        dimNumBOX = Listbox(self)
        dimNumBOX.grid(row=3, column=0)
        dimNumBOX.insert(END, "a list entry")
        for item in ["one", "two", "three", "four"]:
            dimNumBOX.insert(END, item)
            


        Button(self, text = "Quit", command = self.myQuit).grid(row=4,column=0)

        for c in self.master.winfo_children():
            c.pack_configure(padx = 5, pady = 5)

    def calckgs(self):
        try:
            value = float(self.lbs.get())
            #print "The number of kgs is", 0.453592 * value
            self.kgs.set(0.453592 * value)
        except ValueError: pass

    def calclbs(self):
        try:
            value = float(self.kgs.get())
            #print "The number of lbs is", (1/0.453592) * value
            self.lbs.set((1/0.453592) * value)
        except ValueError: pass

    def myQuit(self):
        if askokcancel("Quit", "Do you really wish to quit?"):
            Frame.quit(self)

if __name__ == "__main__":
    convertNUSBruker().mainloop()
