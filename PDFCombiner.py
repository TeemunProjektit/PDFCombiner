import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import os
from PIL import ImageTk,Image

class PDFCombiner:

    def __init__(self, master):
        #New frame with "master frame" parameter
        #All instance variables (self), individual to each instance of a class

        canvas = tk.Canvas(master, width=500, height=600)
        self.image = ImageTk.PhotoImage(Image.open(r'..\\PDFCombiner\Images\tausta.png'))

        canvas.create_image(0, 0, anchor='nw', image=self.image)
        canvas.pack()

        upper_frame = tk.Frame(master, borderwidth=4, highlightbackground='green', highlightcolor='green', highlightthickness=5)
        upper_frame.place(x=250,y=220, anchor='center')#relx=0.5, rely=0.2, relwidth=0.85, relheight=0.3, anchor='n')

        master.geometry('500x600')
        master.title('PDF-Combiner')
        master.resizable(False, False)

        self.otsikko1 = tk.Label(upper_frame, text="Original PDF:")
        self.otsikko1.grid(row=1,column=1,sticky='W')

        self.entry = tk.Entry(upper_frame, width='40')
        self.entry.grid(row=1, column=2, pady=20)

        self.button1 = tk.Button(upper_frame, text="Browse", command=self.browseSource)
        self.button1.grid(row=1, column=3, padx=10)

        self.otsikko2 = tk.Label(upper_frame, text="Add PDF:")
        self.otsikko2.grid(row=2, column=1, sticky='E')

        self.entry2 = tk.Entry(upper_frame, width='40')
        self.entry2.grid(row=2, column=2, pady=10)

        self.button2 = tk.Button(upper_frame, text="Browse", command=self.browseTarget)
        self.button2.grid(row=2, column=3, padx=10)

        self.button3 = tk.Button(upper_frame, text="COMBINE",font=('Helvetica', 16, 'bold'), bg='green',fg='white', command=self.combineSourceTarget)
        self.button3.grid(row=3, column=2, padx=10, pady=10, sticky="NWES")

        self.menu = tk.Menu(master)
        self.submenu = tk.Menu(self.menu, tearoff=False)
        self.submenu2 = tk.Menu(self.menu, tearoff=False)
        self.submenu.add_command(label="Exit", command=master.quit)
        self.submenu2.add_command(label="About")
        self.menu.add_cascade(label="File", menu=self.submenu)
        self.menu.add_cascade(label="Help", menu=self.submenu2)

        master.config(menu=self.menu)

    def browseSource(self):
        self.tiedosto = filedialog.askopenfilename(filetypes=[('PDF Files', '*.pdf')])
        self.entry.delete(0, tk.END)
        self.entry.insert(0,self.tiedosto)

    def browseTarget(self):
        self.tiedosto2 = filedialog.askopenfilename(filetypes=[('PDF Files', '*.pdf')])
        self.entry2.delete(0, tk.END)
        self.entry2.insert(0, self.tiedosto2)

    def combineSourceTarget(self):

        try:
            sourcePath = self.entry.get()
            targetPath = self.entry2.get()

            pdf1 = open(sourcePath.strip(r'",'), 'rb')
            pdf2 = open(targetPath.strip(r'",'), 'rb')

            pdfReader1 = PyPDF2.PdfFileReader(pdf1)
            pdfReader2 = PyPDF2.PdfFileReader(pdf2)
            pdfWriter = PyPDF2.PdfFileWriter()

            for pageNum in range(pdfReader1.numPages):
                pageObj = pdfReader1.getPage(pageNum)
                pdfWriter.addPage(pageObj)

            for pageNum in range(pdfReader2.numPages):
                pageObj = pdfReader2.getPage(pageNum)
                pdfWriter.addPage(pageObj)

            pdfOutputFile = open(os.path.splitext(pdf1.name)[0] + '_combined.pdf', 'wb')
            pdfWriter.write(pdfOutputFile)
            pdfOutputFile.close()
            pdf1.close()
            pdf2.close()
            self.entry.delete(0, tk.END)
            self.entry2.delete(0, tk.END)
            messagebox.showinfo('OK', 'PDFs combined!')

        except FileNotFoundError:
            tk.messagebox.showerror('Error', 'Cannot combine PDFs!')
            print('VIRHE')

#Root Window is created
root = tk.Tk()
#PDCCombiner object is created and root window passed as an argument
application = PDFCombiner(root)

root.mainloop()



