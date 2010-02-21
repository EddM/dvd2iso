#!/usr/bin/env python

"""
  You know when you want to just write a quick script to
  speed-up a monotonous task you're doing, but the developer
  in you makes you want to turn it into a full-blown application?
  
  This is one of those applications.
  
  (c) 2010 Edd Morgan - www.trquadrant.com
  
  
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from Tkinter import *
import tkFileDialog, tkMessageBox, subprocess

class App(Frame):
    def __init__(self, master = None):
      Frame.__init__(self, master)
      self.pack()
      self.renderControls()
      self.beginInteraction()
  
    def renderControls(self):
      self.master.title("Friendly UDF DVD Converter")
      self.master.geometry("300x90")
      self.master.resizable(False, False)
      self.lblName = Label(root, text = "Volume Name:").pack()
      self.txtName = Entry(root).pack()
      self.btnCreate = Button(root, text = "Build ISO File", command = self.saveToISO).pack()
      
    def beginInteraction(self):
      while not self.promptForInputFolder().endswith("/VIDEO_TS"):
        if not tkMessageBox.askretrycancel("Error", "Please select a VIDEO_TS folder."):
          sys.exit(0)
        else:
          self.folder = self.promptForInputFolder()
      
    def pickTargetFile(self):
      self.targetFileName = tkFileDialog.asksaveasfilename(parent = root, filetypes = [('ISO File','*.iso')], title = "Save the ISO as ...", initialdir = "~/Desktop", initialfile = ("%s.iso" % self.txtName.get()))
      return self.targetFileName

    def promptForInputFolder(self):
      self.folder = tkFileDialog.askdirectory(parent = root, initialdir = "/",title = 'Select VIDEO_TS folder', mustexist = True)
      return self.folder

    def saveToISO(self):
      if len(self.txtName.get()) > 0:
        if len(self.pickTargetFile()) > 0:
          proc = subprocess.call("hdiutil makehybrid -udf -o \"%(target_name)s.iso\" -udf-volume-name %(img_name)s \"%(folder_name)s\"" % {"target_name" : self.targetFileName, "img_name" : self.txtName.get().upper().replace(" ", "_"), "folder_name" : self.folder[0:-9]}, shell=True)
          if proc == 0:
            tkMessageBox.showinfo("Done", "DVD ISO file created at %s" % self.targetFileName)
            sys.exit(0)
          else:
            tkMessageBox.showerror("Error", "ISO creation failed with status code %s" % str(proc))
        else:
          tkMessageBox.showerror("Error", "Please enter a target filename.")
      else:
        tkMessageBox.showerror("Error", "Please enter a name for the new volume.")

root = Tk()
app = App(master = root)
app.mainloop()
root.destroy
