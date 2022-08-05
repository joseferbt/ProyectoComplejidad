from minizinc import Instance, Model, Solver
import subprocess
import sys
import time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, \
    QLabel, QTextEdit, QSpinBox, QFileDialog, QHBoxLayout


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
        y = subprocess.run(["minizinc", "--solver", "Gecode", "Universidad.mzn", path], capture_output=True,text=True)
        time_start = time.time() - time_start
        print(y.stdout[0], "\n")
        xtext.setText(y.stdout[0])
        ytext.setText(y.stdout[2])
        ttext.setText(str(format(time_start,".3f"))+"Sg")


def solve():
    model = Model("./Universidad.mzn")
    # Find the MiniZinc solver configuration for Gecode
    solver = Solver.lookup("gecode") #COIN_BC / gecode
    # Create an Instance of the n-Queens model for Gecode
    instance = Instance(solver, model)
    # Assign 4 to n
    instance["n"] = ntext.value()
    instance["m"] = mtext.value()
    #instance["c"] = [[1,1],[3,2],[5,5]] # la entrada de tipo [[1,2],[2,1]...]|1,2|3|
    instance["c"] = formatArray(ctext.toPlainText(),ntext.value())
    time_start = time.time()
    result = instance.solve()
    time_start = time.time() - time_start
    # Output the array q
    xtext.setText(str(result["x"]))
    ytext.setText(str(result["y"]))
    ttext.setText(str(format(time_start,".3f"))+"Sg")



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

    # Layout
    hbox = QHBoxLayout()
    grid = QGridLayout(w)
    grid.addWidget(nLabel, 0, 0)
    grid.addWidget(ntext, 0, 1)
    grid.addWidget(mLabel, 1, 0)
    grid.addWidget(mtext, 1, 1)
    grid.addWidget(cLabel, 2, 0)
    grid.addWidget(ctext, 2, 1)
    grid.addWidget(sbtn, 3, 1)
    grid.addWidget(cbtn, 3, 0)
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
# Load n-Queens model from file



"""
y = subprocess.run(["minizinc", "--solver" ,"Gecode", "Universidad.mzn" ,"data1.dzn"], capture_output=True,text=True)
print(y.stdout, "\n")
print(y.stdout[0]," ",y.stdout[2])

"""
text = "muchas cosas en un escrito con numeros 1 2 3 4 5 6 8 77"
x= text.split()
print(x)
for i in x:
    try:
        if isinstance(int(i), int):
            print(i)
    except:
        continue
"""
        
#print(formatArray("1 1 \n 1 1 1 1 1 1 \n 1 1 1 1",55),"[]")
#"""
