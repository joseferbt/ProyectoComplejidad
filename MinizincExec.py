from minizinc import Instance, Model, Solver
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, \
    QLabel, QPlainTextEdit, QSpinBox

def formatArray(text):
    array = []
    count = 0
    for i in text :
        if i :
            if count==2:
                count = 0
                array.push([i])
            else:
                array[-1][count] = i
                ++count


def clear():
    ntext.setValue(0)
    mtext.setValue(0)
    ctext.insertPlainText("")
def solve():
    nqueens = Model("./Universidad.mzn")
    # Find the MiniZinc solver configuration for Gecode
    gecode = Solver.lookup("gecode")
    # Create an Instance of the n-Queens model for Gecode
    instance = Instance(gecode, nqueens)
    # Assign 4 to n
    instance["n"] = ntext.value
    instance["m"] = mtext.value
    instance["c"] = formatArray(ctext.toPlainText())
    result = instance.solve()
    # Output the array q
    print(result["X"])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = QWidget()
    w.setWindowTitle("University GUI")

#labels
    nLabel = QLabel(w)
    nLabel.setText("n =")
    mLabel = QLabel(w)
    mLabel.setText("m =")
    cLabel = QLabel(w)
    cLabel.setText("Cities =")

#text file
    ntext = QSpinBox()
    mtext = QSpinBox()
    ctext = QPlainTextEdit()



# Boton

    sbtn = QPushButton(w)
    sbtn.setText('Solve')
    sbtn.clicked.connect(solve)
    cbtn = QPushButton(w)
    cbtn.setText('Clear')
    cbtn.clicked.connect(clear)


#Layout
    grid = QGridLayout(w)
    grid.addWidget(nLabel, 0, 0)
    grid.addWidget(ntext, 0, 1)
    grid.addWidget(mLabel,1, 0)
    grid.addWidget(mtext, 1, 1)
    grid.addWidget(cLabel, 2, 0)
    grid.addWidget(ctext, 2, 1)
    grid.addWidget(sbtn, 3, 1)
    grid.addWidget(cbtn, 3, 0)



    w.show()
    sys.exit(app.exec_())
# Load n-Queens model from file
print(5)
