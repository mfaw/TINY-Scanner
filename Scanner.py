class scanner():
    def __init__(self, code_input: str = ""):
        self.code_input = str(code_input)
        self.type = {}
        self.tokens_list = []

    def scan(self):
        state = "start"
        token = ""
        special_chars = ['+', '-', '*', '/', '=', ';', '<', '>', '<=', '>=', '(', ')']
        reserved = ["if", "then", "else", "end", "repeat", "until", "read", "write"]
        end = ['\n', ';', ' ', '', "{"]
        i = 0
        while i < len(self.code_input):
            if state == "DONE":
                token = ""
                state = "start"
                token = token + self.code_input[i]
            else:
                token = token + self.code_input[i]

            if state == "start" or state == "nDONE":
                tokenZ = ""
                e = ''
                e2 = ''
                if i + 1 < len(self.code_input):
                    tokenZ = token + self.code_input[i + 1]
                    e = self.code_input[i + 1]

                if i + 2 < len(self.code_input):
                    e2 = self.code_input[i + 1] + self.code_input[i + 2]

                if tokenZ in special_chars:
                    state = "DONE"
                    self.tokens_list.append(tokenZ)
                    self.type[tokenZ] = "special symbol"
                    i = i + 1

                elif token in special_chars:
                    state = "DONE"
                    self.tokens_list.append(token)
                    self.type[token] = "special symbol"

                elif token in reserved and (e in end or e in special_chars or e2 == ":="):
                    state = "DONE"
                    self.tokens_list.append(token)
                    self.type[token] = "reserved word"

                elif token.isdigit() and (e in end or e in special_chars or e2 == ":="):
                    state = "DONE"
                    self.tokens_list.append(token)
                    self.type[token] = "INNUM"

                elif token.isalpha() and (e in end or e in special_chars or e2 == ":="):
                    state = "DONE"
                    self.tokens_list.append(token)
                    self.type[token] = "INID"

                elif token == ":=":
                    state = "DONE"
                    self.tokens_list.append(token)
                    self.type[token] = "Assign"

                elif self.code_input[i] == " " or self.code_input[i] == "\n":
                    state = "DONE"
                    if len(token) > 1:
                        self.tokens_list.append(token[:len(token) - 1])
                        self.type[token[:len(token) - 1]] = "UNKOWN"

                elif self.code_input[i] == ';' :
                    state = "DONE"
                    if len(token) > 1:
                        self.tokens_list.append(token[:len(token) - 1])
                        self.type[token[:len(token) - 1]] = "UNKOWN"
                    i = i - 1

                elif self.code_input[i] == "{":
                    state = "comment"

                elif self.code_input[i] == "}":
                    state = "start"
                    self.tokens_list.append(token[:len(token) - 1])
                    self.type[token[:len(token) - 1]] = "UNKOWN"
                    self.tokens_list.append(token)
                    self.type[token] = "unopened {}"
                    token = ""

                elif e == ''or e == ":":
                    state = "DONE"
                    if len(token) > 1:
                        self.tokens_list.append(token)
                        self.type[token] = "UNKOWN"
                else:
                    state = "nDONE"

            elif state == "comment":
                if token[len(token) - 1] == "}":
                    state = "start"
                    token = ""
                else:
                    i = i + 1
                    continue
            i = i + 1


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if len(self._data) == 0:
                return
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        if len(self._data) == 0:
            return 1
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return 2


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1090, 840)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout.addWidget(self.plainTextEdit)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(lambda: self.cliked())
        self.verticalLayout.addWidget(self.pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1090, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.l = []

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Scanner"))
        self.pushButton.setText(_translate("MainWindow", "Scan"))

    def cliked(self):
        s = scanner()
        s.code_input = self.plainTextEdit.toPlainText()
        s.scan()
        self.l = []
        # print(s.tokens_list)
        # print(s.type)
        for t in s.tokens_list:
            if t != "":
                self.l.append([t, s.type[t]])
        # print(self.l)
        self.m = TableModel(self.l)
        self.tableView.setModel(self.m)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
