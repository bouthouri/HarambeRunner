from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image, ImageTk
import os

# Variables
margin = 150
ratio = 1
filePath = "/Users/MacBook/offlineDesktop/python/HarambeRunner/actual.png"
rawImage = None
img = None
canvasImgWidth = None
canvasImgHeight = None
mouseX = 0
mouseY = 0
mouseCoor = []

# Functions
def loadImage():
	global rawImage
	global img
	rawImage.close()
	rawImage = Image.open(filePath)
	#resizing the image to fit the screen with the new ratio
	rawImage = rawImage.resize((int(canvasImgWidth), int(canvasImgHeight)) ,Image.ANTIALIAS)
	img = ImageTk.PhotoImage(rawImage)
	#refresh the image
	canvas.itemconfig(canvasImageRef, image=img)

def initImage():
	global rawImage
	global img
	global root
	rawImage = Image.open(filePath)
	# resizing the image to fit the screen with the new ratio
	canvasImgWidth = rawImage.width
	canvasImgHeight = rawImage.height

	if canvasImgWidth > (root.winfo_screenwidth() - margin):
		ratio = float(float(root.winfo_screenwidth() - margin) / float(canvasImgWidth))
		canvasImgWidth *= ratio
		canvasImgHeight *= ratio

	if canvasImgHeight > (root.winfo_screenheight() - margin):
		ratio = float(float(root.winfo_screenheight() - margin) / float(canvasImgHeight))
		canvasImgWidth *= ratio
		canvasImgHeight *= ratio

	rawImage = rawImage.resize((int(canvasImgWidth), int(canvasImgHeight)), Image.ANTIALIAS)
	img = ImageTk.PhotoImage(rawImage)
	# refresh the image
	canvas.itemconfig(canvasImageRef, image=img)

def printcoords(event):
	global mouseX
	global mouseY

	#normalise the coordinate by dividing by the ration
	mouseX = int( float(event.x) / float(ratio) )
	mouseY = int( float(event.y) / float(ratio) )
	coordLabel.config(text="Coor ("+str(mouseX)+","+str(mouseY)+")")

def executeOrder(event):
	global mouseX
	global mouseY
	os.system("monkeyrunner HarambeBridge.py " + str(mouseX) + " " + str(mouseY) + " " +str(float(delayEntry.get())) )
	loadImage()

def getSnapshot():
	os.system("monkeyrunner HarambeBridge.py ")
	initImage()

def refreshScreen(event):
	getSnapshot()

def storeAction(event):

	global mouseX
	global mouseY
	global logText
	global mouseCoor

	mouseCoor.append([str(mouseX), str(mouseY)])
	logText.delete('1.0', END)
	textToInsert = ""
	for id,coor in enumerate(mouseCoor):
		textToInsert += "myCoords[ point"+str(id)+" ] = [ "+str(coor[0])+"," +str(coor[1])+" ]\n"

	logText.insert(END, textToInsert)



def generateVariable(text):
	global logText
	if text is not None:
		logText.insert(0, str(text))
	else:
		text = str

root = Tk()
os.system("monkeyrunner HarambeBridge.py ")
rawImage = Image.open(filePath)

# Adapting img to screen

canvasImgWidth = rawImage.width
canvasImgHeight = rawImage.height

if canvasImgWidth > (root.winfo_screenwidth() - margin):
	ratio = float( float(root.winfo_screenwidth() - margin) / float(canvasImgWidth) )
	canvasImgWidth *= ratio
	canvasImgHeight *= ratio

if canvasImgHeight > (root.winfo_screenheight() - margin):
	ratio = float( float(root.winfo_screenheight() - margin) / float(canvasImgHeight) )
	canvasImgWidth *= ratio
	canvasImgHeight *= ratio

#resizing the image to fit the screen with the new ratio
rawImage = rawImage.resize((int(canvasImgWidth), int(canvasImgHeight)) ,Image.ANTIALIAS)
img = ImageTk.PhotoImage(rawImage)

canvas = Canvas(root, bd=0, width=canvasImgWidth, height=canvasImgHeight)
canvas.grid(row=0, column=0, rowspan=8)
canvasImageRef = canvas.create_image(0,0,image=img, anchor="nw")

coordLabel = Label(root, text="Coord (0,0)")
coordLabel.grid(row=0, column=1, sticky=W)

delayLabel = Label(root, text="Delay")
delayLabel.grid(row=1, column=1, sticky=W)

delayEntry = Entry(root)
delayEntry.grid(row=1, column=2)
delayEntry.insert(0,"1")

refreshButton = Button(root, text="Refresh")
refreshButton.grid(row=2, column=1)
refreshButton.bind("<Button 1>", refreshScreen)

nextButton = Button(root, text="Next")
nextButton.grid(row=2, column=2)
nextButton.bind("<Button 1>", storeAction)

executeButton = Button(root, text="Execute")
executeButton.grid(row=2, column=3)
executeButton.bind("<Button 1>", executeOrder)

logLabel = Label(root, text="Log :")
logLabel.grid(row=3, column=1, sticky=W)

logText = Text(root)
logText.grid(row=4, column=1, columnspan=4 , sticky=W+E+N+S)
logText.insert(END, "il vaut mieux avoir affaire a dieu qua ses saints")

#mouseclick event
canvas.bind("<Button 1>",printcoords)


root.mainloop()