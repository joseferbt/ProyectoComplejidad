import self as self
from minizinc import Instance, Model, Solver
import subprocess
import numpy
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import sys
import time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, \
    QLabel, QTextEdit, QSpinBox, QFileDialog, QHBoxLayout, QComboBox, QMessageBox



class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.canva = MplCanvas(self, width=5, height=4, dpi=100)
        grid = QGridLayout()
        label = QLabel("Another Window asdasdasdasdasd")
        toolbar = NavigationToolbar(self.canva, self)
        grid.addWidget(toolbar,0,0)
        grid.addWidget(self.canva,1,0)
        self.setLayout(grid)

    def set(self,xVals,yVals,x,y):
        self.canva.axes.clear()

        # plot the new data
        self.canva.axes.plot(xVals, yVals, 'ro')
        self.canva.axes.plot(x, y, 'bo')

        # call the draw method on your canvas
        self.canva.draw()



def formatArray(text,max):
    art = text.split()
    array = [[]]
    count = 0
    for i in art:
        try:
            i = int(i)
            if i <= max:
                if count == 2:
                    count = 1
                    array.append([i])
                else:
                    array[-1].append(i)
                    count=count+1
            else:
                return 1
        except:
            continue
    return array


def clear():
    ntext.setValue(0)
    mtext.setValue(0)
    xtext.setText("")
    ytext.setText("")
    ttext.setText("")
    ctext.clear()

def openfile():
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(w, "QFileDialog.getOpenFileName()", "",
                                              "data Files (*.dzn)", options=options)
    if fileName:
        path = fileName
        datos = numpy.transpose(readDznfile(path))
        xVals = datos[0]
        yVals = datos[1]

        time_start = time.time()
        if (cbox.currentText() == "gecode"):
            solver = "gecode" # COIN_BC / gecode
            modelo = "UvInt.mzn"
        else:
            solver = "coin-bc"
            modelo = "UvFloat.mzn"

        y = subprocess.run(["minizinc", "--solver", solver, modelo, path], capture_output=True,text=True)
        time_start = time.time() - time_start

        out = y.stdout.split()

        xtext.setText(out[0])
        ytext.setText(out[1])
        ttext.setText(str(format(time_start,".3f"))+"Sg")
        plot.set(xVals,yVals, [float(out[0])],[float(out[1])])
        plot.show()

def readDznfile(file):
    f = open(file, "r")
    aux=""
    array= []
    cont = f.read()
    for i in range(cont.index("[|")+2,cont.index("|]")):
        aux += cont[i]
    arAux=aux.split("|")
    for i in range(len(arAux)):
        arAux[i] = arAux[i].split(",")
    for i in arAux:
        for j in range(2):
            i[j] = int(i[j])
    return arAux




def dznFormat(array):
    text ="[|"
    for i in array:
        text+= str(i[0])+","+str(i[1])+"|"
    text+="]"
    return text

def solve():
    f = open("instacias/data_.dzn", "w")
# Find the MiniZinc solver configuration for Gecode
    if(cbox.currentText()=="gecode"):
        solver = Solver.lookup("gecode") #COIN_BC / gecode
        model = Model("UvInt.mzn")
    else:
        solver = Solver.lookup("coin-bc")
        model = Model("UvFloat.mzn")
    # Create an Instance of the n-Queens model for Gecode
    instance = Instance(solver, model)
    # Assign 4 to n
    n = ntext.value()
    m = mtext.value()
    c = formatArray(ctext.toPlainText(),ntext.value())
    instance["n"] = n
    instance["m"] = m
    #instance["c"] = [[1,1],[3,2],[5,5]] # la entrada de tipo [[1,2],[2,1]...]|1,2|3|
    instance["c"] = c
    ctrans = numpy.transpose(c)
    xVals = ctrans[0]
    yVals = ctrans[1]
    f.write("n = " + str(n)+ ";\nm= "+str(m)+" ;\n"+"c= "+dznFormat(c)+";")
    f.close()
    time_start = time.time()
    result = instance.solve()
    time_start = time.time() - time_start
    # Output the array q
    xtext.setText(str(format(result["x"],".3f")))
    ytext.setText(str(format(result["y"],".3f")))
    ttext.setText(str(format(time_start,".3f"))+"Sg")
    plot.set(xVals, yVals, [result["x"]], [result["y"]])
    plot.show()


if __name__ == "__main__":
    yVals = []
    xVals = []
    app = QApplication(sys.argv)
    w = QWidget()
    w.setWindowTitle("University GUI")

    #plot
    plot = AnotherWindow()


    #messageBox
    msg = QMessageBox(w)

    # labels
    uLabel = QLabel(w)
    uLabel.setText("La ubicación de la universidad es :")
    nLabel = QLabel(w)
    nLabel.setText("n =")
    mLabel = QLabel(w)
    mLabel.setText("m =")
    xLabel = QLabel(w)
    xLabel.setText("x =")
    yLabel = QLabel(w)
    yLabel.setText("y =")
    cLabel = QLabel(w)
    cLabel.setText("Cities =")
    tLabel = QLabel(w)
    tLabel.setText("Time =")

    # text file
    ntext = QSpinBox()
    mtext = QSpinBox()
    ytext = QLabel()
    xtext = QLabel()
    ttext = QLabel()
    ctext = QTextEdit()

    # Boton
    filebtn = QPushButton(w)
    filebtn.setText('select .dzn file')
    filebtn.clicked.connect(openfile)
    sbtn = QPushButton(w)
    sbtn.setText('Solve')
    sbtn.clicked.connect(solve)
    cbtn = QPushButton(w)
    cbtn.setText('Clear')
    cbtn.clicked.connect(clear)

    #select
    cbox = QComboBox(w)
    cbox.addItem("coin-bc")
    cbox.addItem("gecode")

    # Layout
    hbox = QHBoxLayout()
    grid = QGridLayout(w)
    grid.addWidget(nLabel, 0, 0)
    grid.addWidget(ntext, 0, 1)
    grid.addWidget(mLabel, 1, 0)
    grid.addWidget(mtext, 1, 1)
    grid.addWidget(cLabel, 2, 0)
    grid.addWidget(ctext, 2, 1)
    grid.addWidget(sbtn, 3, 2)
    grid.addWidget(cbtn, 3, 0)
    grid.addWidget(cbox,3,1)
    grid.addWidget(filebtn,4,1)
    grid.addLayout(hbox,5,0,5,2,Qt.AlignHCenter)
    hbox.addWidget(uLabel)
    hbox.addWidget(xLabel)
    hbox.addWidget(xtext)
    hbox.addWidget(yLabel)
    hbox.addWidget(ytext)
    hbox.addWidget(tLabel)
    hbox.addWidget(ttext)

    w.show()
    sys.exit(app.exec_())


