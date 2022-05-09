from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os, sys, pathlib, tempfile
import zipfile
from pathlib import Path
import glob



root = tk.Tk()
root.title('TriTechne KML to CSV converter')
root.resizable(False, False)
root.geometry('300x150')
fileName = "C:/Users/AlastorBloode/Downloads/nz026Converted.csv"
outputPath = ""
fields = ['Latitude', 'Longitude']
rows = []

def WriteKML():
    f = fd.asksaveasfile(title = "Save converted CSV='.csv'", mode='w', defaultextension=".csv") 
    if f is None:
        return
    with f as csvfile:
        csvwriter = csv.writer(csvfile, lineterminator = '\n')
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

def ConvertKML(path):
    with open(path, 'r') as f:
        soup = BeautifulSoup(f, 'xml')

        poles = soup.find_all('Placemark')
        for data in poles:
            id = data.get('id')
            if id != None:
                if 'Pole' in id:
                    c = data.find('coordinates')
                    cords = c.get_text().split(',')
                    lon = cords[0]
                    lat = cords[1]
                    rows.append([lat, lon])
        showinfo(title='Selected File',
        message="Converted {0} poles".format(len(rows))
        )
        WriteKML()

def kmz2kml(path):
    d = os.path.dirname(path)
    n = os.path.basename(path)
    print(n)
    tmpdir = tempfile.mkdtemp()
    os.rename(path, '{0}/temp.zip'.format(d))
    f = '{0}/temp.zip'.format(d)
    with zipfile.ZipFile(f, 'r') as archive:
        archive.extractall(path=tmpdir)
        for file in os.listdir(tmpdir):
            if file.endswith(".kml"):
                p = "{0}\{1}".format(tmpdir, file)
                ConvertKML(p)
    os.rename('{0}/temp.zip'.format(d), "{0}/{1}".format(d, n))

def select_file():
    filetypes = (('Google Earth Document', '*.kml'),
                 ('Google Earth Document', '*.kmz')
                 )

    filename = fd.askopenfilename(
        title='Open file',
        initialdir='/',
        filetypes=filetypes)

    ext = pathlib.Path(filename).suffix
    if ext == '.kmz':
        kmz2kml(filename)
    else:
        ConvertKML(filename)

open_button = ttk.Button(root, text = 'Open KML', command=select_file)

open_button.pack(expand=True)

root.mainloop()
