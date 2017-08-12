import operator
from PySide.QtCore import QAbstractTableModel, Qt, SIGNAL, Signal
from PySide.QtGui import QWidget, QVBoxLayout, QTableView, QFont, QHBoxLayout, QPushButton, QLayout


class TableWindow(QWidget):

    export_top_x_clicked = Signal(int)

    def __init__(self, data_list, header, *args):
        QWidget.__init__(self, *args)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(300, 200, 570, 450)
        self.setWindowTitle("Click on column title to sort")
        self.table_model = TableModel(self, data_list, header)
        self.table_view = self._init_table_view(self.table_model)
        button_row = self._init_button_row()

        layout = QVBoxLayout(self)
        layout.addWidget(self.table_view)
        layout.addLayout(button_row)
        self.setLayout(layout)

    def _init_table_view(self, model):
        table_view = QTableView()
        table_view.setModel(model)
        # set font
        font = QFont("Courier New", 14)
        table_view.setFont(font)
        # set column width to fit contents (set font first!)
        table_view.resizeColumnsToContents()
        # enable sorting
        table_view.setSortingEnabled(True)
        return table_view

    def _init_button_row(self):
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self._init_export_x_button(10))
        hbox.addWidget(self._init_export_x_button(25))
        hbox.addWidget(self._init_export_x_button(50))
        hbox.addStretch(1)
        hbox.setSizeConstraint(QLayout.SetFixedSize)
        return hbox

    def _init_export_x_button(self, x):
        button = QPushButton('Export Top {}'.format(x), self)
        button.clicked.connect(lambda: self._on_click(x))
        return button

    def _on_click(self, x):
        self.export_top_x_clicked.emit(x)

    def update(self, data_list):
        self.table_model.update(data_list)
        self.table_view.resizeColumnsToContents()


class TableModel(QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header
        self.current_sort_order = Qt.DescendingOrder
        self.current_sort_column = 0

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        return len(self.mylist[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))

        self.mylist = sorted(self.mylist,
            key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.mylist.reverse()

        self.current_sort_column = col
        self.current_sort_order = order

        self.emit(SIGNAL("layoutChanged()"))

    def update(self, mylist):
        self.mylist = mylist
        self.sort(self.current_sort_column, self.current_sort_order)
