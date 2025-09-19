from tkinter import *

# GUI settings ----------------------------------------------------------

gridSize = 16             # define the number of squares in the grid
squareSize = 60           # define the size of individual squares
squareHeight = 40
canvasBorder = 6          # define the border size between canvas and main window
canvasVBorder = 60        # define the vertical border
canvasWidth = (gridSize * squareSize) + canvasBorder
windowSize = canvasWidth + canvasBorder
winSizeString = str(windowSize) + "x" + str(squareSize+100+canvasVBorder)
highlightWidth = 4
green = "#aaffaa"

# Algorithm initial settings ----------------------------------------------------------

# inputArray = [0] * gridSize
boxArray = [0] * gridSize
textArray = [0] * gridSize

inputArray = [4, 76, 29, 1234, 5209, 0, 0, 0, 7777, 9999, 9876, 29, 11, 22, 223, 444]   # default array values -- can be changed
inputIndex = 0
inputIndexLast = inputIndex
outputArray = inputArray.copy()
outputArrayLast = outputArray.copy()
running = True

solving = False
solved = False
pointer, pointer2 = 0, 0

# Functions ----------------------------------------------------------

def redrawArray():
    left = canvasBorder
    top = canvasVBorder
    bottom = top + squareHeight
    for i in range(gridSize):
        right = left + squareSize
        mainGrid.itemconfig(boxArray[i], fill="white")
        mainGrid.coords(boxArray[i], left, top, right, bottom)
        mainGrid.itemconfig(textArray[i], text=str(outputArray[i]))
        left += squareSize

def swapPair(a, b):
    global outputArray, inputArray, boxArray, textArray, solving
    speed = 4
    vSteps = int(squareHeight / speed)
    hSteps = int(squareSize * (b - a) / speed)
    mainGrid.itemconfig(boxArray[a], fill="cyan")
    mainGrid.itemconfig(boxArray[b], fill=green)
    for i in range(vSteps):
        mainGrid.move(boxArray[a], 0, -speed)
        mainGrid.move(textArray[a], 0, -speed)
        mainGrid.move(boxArray[b], 0, speed)
        mainGrid.move(textArray[b], 0, speed)
        window.update()
    for i in range(hSteps):
        mainGrid.move(boxArray[a], speed, 0)
        mainGrid.move(textArray[a], speed, 0)
        mainGrid.move(boxArray[b], -speed, 0)
        mainGrid.move(textArray[b], -speed, 0)
        window.update()
    for i in range(vSteps):
        mainGrid.move(boxArray[a], 0, speed)
        mainGrid.move(textArray[a], 0, speed)
        mainGrid.move(boxArray[b], 0, -speed)
        mainGrid.move(textArray[b], 0, -speed)
        window.update()
    mainGrid.itemconfig(boxArray[a], fill="white")
    mainGrid.itemconfig(boxArray[b], fill="white")
    outputArray[a], outputArray[b] = outputArray[b], outputArray[a]
    boxArray[a], boxArray[b] = boxArray[b], boxArray[a]
    textArray[a], textArray[b] = textArray[b], textArray[a]
    if not solving:
        outputArray = inputArray.copy()             # makes sure the output array is properly reset if interrupted by Reset command

def solve():            # Trigger the solving algorithm and initialise all relevant variables
    global solving, solved, pointer, outputArray, inputArray, inputSquare
    if not solving and not solved:
        inputArray = outputArray.copy()
        solving, solved, pointer = True, False, 0
        mainGrid.coords(inputSquare, 0,0,0,0)
        mainGrid.itemconfig(inputSquare, fill="white")

def reset():
    global solving, solved, outputArray, inputArray, inputIndexLast
    solving, solved = False, False
    outputArray = inputArray.copy()
    inputIndexLast = -1                 # since this no longer matches inputIndex, the input square is redrawn
    for i in range(gridSize):
        mainGrid.itemconfig(boxArray[i], fill="white")
        mainGrid.itemconfig(textArray[i], text=str(outputArray[i]))
    mainGrid.itemconfig(resultText, text="")

def clear():
    global inputArray
    inputArray = [0] * gridSize
    reset()

def leftClick(event):                   # selects a box for editing
    global inputIndex, solving
    if not solving and not solved:
        yCo = event.y
        if yCo >= canvasVBorder and yCo <= canvasVBorder + squareHeight:
            inputIndex = int(event.x / squareSize)

def keyInput(event):
    global inputIndex, outputArray, solving
    if not solving and not solved:
        num = event.keysym
        length = len(str(outputArray[inputIndex]))
        if num == "BackSpace":
            if length > 1:
                newVal = str(outputArray[inputIndex])
                newVal = newVal[0:length-1]
                outputArray[inputIndex] = int(newVal)
            else:
                outputArray[inputIndex] = 0
        elif num == "Left":
            if inputIndex > 0:
                inputIndex -= 1
        elif num == "Right":
            if inputIndex < gridSize - 1:
                inputIndex += 1
        elif num == "Up":
            outputArray[inputIndex] += 1
            if outputArray[inputIndex] > 9999:
                outputArray[inputIndex] = 9999
        elif num == "Down":
            outputArray[inputIndex] -= 1
            if outputArray[inputIndex] < 0:
                outputArray[inputIndex] = 0
        else:
            try:
                if length < 4:
                    outputArray[inputIndex] = int(str(outputArray[inputIndex]) + str(num))
            except:
                print("Please enter a number. No other characters allowed.")

# Create interface ----------------------------------------------------------------

window = Tk()
window.title("Sorting Algorithms")
window.geometry(winSizeString)

# Create main grid
mainGrid = Canvas(window, width=canvasWidth, height=squareHeight+2*canvasVBorder, bg="white", border=True)
mainGrid.pack(pady=10)

# Create key and mouse-button bindings
mainGrid.bind("<Button-1>", leftClick)      # left mouse click
window.bind("<Key>", keyInput)              # key input

# Initialise result text:
textFont = ("Helvetica", "14", "bold")
resultText = mainGrid.create_text(windowSize/2, canvasVBorder*2.5, font=textFont, text="")

# Draw grid
left = canvasBorder
top = canvasVBorder
bottom = top + squareHeight
for i in range(gridSize):
    right = left + squareSize
    boxArray[i] = mainGrid.create_rectangle(left, top, right, bottom, width=2)
    left += squareSize

# Create initial input box lines
inputSquare = mainGrid.create_rectangle(canvasBorder, top, canvasBorder+squareSize, bottom, width=4, outline="green")

# Create initial array of zeroes
for i in range(len(outputArray)):
    xCo = ((i % gridSize) * squareSize) + (squareSize / 2) + canvasBorder
    yCo = (int(i / gridSize) * squareSize) + (squareHeight / 2) + canvasVBorder
    numFont = ("Helvetica", "16", "bold")
    textArray[i] = mainGrid.create_text(xCo, yCo, text=str(outputArray[i]), fill="black", font=numFont)

# Create frame for buttons
bottomFrame = Frame(window, height=20)
bottomFrame.pack(side=LEFT)

# Create buttons
solveButton = Button(bottomFrame, text="Sort", command=solve)
solveButton.grid(row=0, column=0)
resetButton = Button(bottomFrame, text="Reset", command=reset)
resetButton.grid(row=0, column=1)
clearButton = Button(bottomFrame, text="Clear", command=clear)
clearButton.grid(row=0, column=2)

# Create algorithm selection menu
algorithms = ("Selection Sort", "Bubble Sort", "Insertion Sort", "Quick Sort")
sortMenu = Spinbox(bottomFrame, from_=0, to=3, values=algorithms)
sortMenu.grid(row=0, column=3)


# Main program loop ---------------------------------------------------------------------------

while running:
    # Update highlighted input square
    if inputIndex != inputIndexLast:
        left = (inputIndex * squareSize) + canvasBorder
        top = canvasVBorder
        right = left + squareSize
        bottom = top + squareHeight
        mainGrid.coords(inputSquare, left, top, right, bottom)
    inputIndexLast = inputIndex
    # Update numbers on screen
    if not solving:
        redrawArray()
    # Solving algorithms
    if solving:

        if sortMenu.get() == "Selection Sort":
            minimum = outputArray[pointer]
            minIndex = pointer
            for i in range(pointer, gridSize):
                if outputArray[i] < minimum:
                    minimum = outputArray[i]
                    minIndex = i
            swapPair(pointer, minIndex)
            pointer += 1
            if pointer == gridSize:
                solved, solving = True, False

        elif sortMenu.get() == "Bubble Sort":
            if pointer == 0:
                solved = True
                mainGrid.itemconfig(boxArray[gridSize-1], fill="white")
            i = pointer
            if outputArray[i] > outputArray[i + 1]:
                swapPair(i, i+1)
                solved = False
            mainGrid.itemconfig(boxArray[pointer], fill="white")
            pointer += 1
            mainGrid.itemconfig(boxArray[pointer], fill="cyan")
            if pointer >= gridSize - 1:
                pointer = 0
            for delay in range(500):
                window.update()
            if solved and pointer == 0:
                solving = False

        elif sortMenu.get() == "Insertion Sort":
            if pointer == 0:
                pointer = 1                     # initialise the pointer at the second square
            mainGrid.itemconfig(boxArray[pointer], fill="cyan")
            for i in range(pointer, 0, -1):
                if outputArray[i] < outputArray[i - 1]:
                    swapPair(i - 1, i)
            mainGrid.itemconfig(boxArray[pointer], fill="cyan")
            for delay in range(500):
                window.update()
            mainGrid.itemconfig(boxArray[pointer], fill="white")
            pointer += 1
            if pointer >= gridSize:
                solved, solving = True, False

        elif sortMenu.get() == "Quick Sort":
            # Requires its own specific function as it uses recursion
            def quickSort(array, start, end):
                if end <= start: return                 # Base case (for recursion)
                pivot = array[end]
                i = start - 1
                for j in range(start, end):
                    if array[j] < pivot:
                        i += 1
                        swapPair(i, j)
                pivot = i + 1
                swapPair(pivot, end)
                quickSort(array, start, pivot - 1)      # recursion part 1
                quickSort(array, pivot + 1, end)        # recursion part 2
                return
            quickSort(outputArray, 0, len(outputArray) - 1)
            solved, solving = True, False


        if solved and not solving:
            mainGrid.itemconfig(resultText, text="The array has been sorted.")


    window.update()


window.mainloop()
