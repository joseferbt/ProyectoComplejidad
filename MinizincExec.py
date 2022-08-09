from minizinc import Instance, Model, Solver
import subprocess
import matplotlib.pyplot as plt
import sys
import time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, \
    QLabel, QTextEdit, QSpinBox, QFileDialog, QHBoxLayout, QComboBox


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
        time_start = time.time()
        if (cbox.currentText() == "gecode"):
            solver = Solver.lookup("gecode")  # COIN_BC / gecode
            modelo = "UvInt.mzn"
        else:
            solver = Solver.lookup("coin-bc")
            modelo = "UvFloat.mzn"

        y = subprocess.run(["minizinc", "--solver", solver, modelo, path], capture_output=True,text=True)
        time_start = time.time() - time_start
        print(y.stdout, "\n")
        xtext.setText(y.stdout[0])
        ytext.setText(y.stdout[2])
        ttext.setText(str(format(time_start,".3f"))+"Sg")

def dznFormat(array):
    text ="[|"
    for i in array:
        text+= str(i[0])+","+str(i[1])+"|"
    text+="]"
    return text

def solve():
    f = open("data_.dzn", "w")
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
    f.write("n = " + str(n)+ ";\nm= "+str(m)+" ;\n"+"c= "+dznFormat(c)+";")
    f.close()
    time_start = time.time()
    result = instance.solve()
    time_start = time.time() - time_start
    # Output the array q
    xtext.setText(str(format(result["x"],".3f")))
    ytext.setText(str(format(result["y"],".3f")))
    ttext.setText(str(format(time_start,".3f"))+"Sg")
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')
    plt.axis([0, 6, 0, 20])
    plt.show()



if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = QWidget()
    w.setWindowTitle("University GUI")

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


