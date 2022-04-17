from qt_3 import *
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QColor, QKeySequence
from PyQt5.QtCore import Qt
import os
import sys
import numpy as np
import math
import warnings
import networkx as nx
import matplotlib.pyplot as plt

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        
        self.size_of_matrix = 0
        self.read_matrix = []
        self.matrix_of_conection = []
        self.state = None
        self.final_path = []
        self.visited = []
        self.final_res = 0
        
        self.ui.label_txt.setFont(QtGui.QFont('SansSerif', 11))
        self.ui.file_name.setFont(QtGui.QFont('SansSerif', 11))
        self.ui.btn_choose.setFont(QtGui.QFont('Arial', 11))
        self.ui.btn_count.setFont(QtGui.QFont('Arial', 11))
        self.ui.btn_clear.setFont(QtGui.QFont('Arial', 11))
                
        self.ui.btn_choose.clicked.connect(self.read_matrix_from_file)
        self.ui.btn_count.clicked.connect(self.start)
        self.ui.btn_clear.clicked.connect(self.clear)
        
    def clear(self):
        self.ui.file_name.clear()
        self.ui.table_enter_matrix.setRowCount(0)
        self.ui.table_enter_matrix.setColumnCount(0)
        self.ui.text_con.clear()
        self.scene.clear()
        self.ui.graphicsView.items().clear()
    
    def show_graph(self):
        G = nx.Graph()
        for i in range(len(self.matrix_of_conection)):
            G.add_edge(self.matrix_of_conection[i][0]+1,
                       self.matrix_of_conection[i][1]+1,
                       weight = self.read_matrix[self.matrix_of_conection[i][0]][self.matrix_of_conection[i][1]])
        
        plt.figure(figsize=(self.size_of_matrix+1 , self.size_of_matrix+1))
        
        pos=nx.planar_layout(G)
        #pos = nx.random_layout(G)
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=1300, font_size=21,
                width=3, node_color='lime')
        edge_weight = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weight, label_pos=0.5,
                                     font_size=13, font_color='red')
        #plt.show()
        plt.savefig("filename.png")
        #self.scene = QtWidgets.QGraphicsScene(self)
        pixmap = QPixmap("filename.png")
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.scene.addItem(item)
        self.ui.graphicsView.setScene(self.scene)
                
    def show_read_matrix(self):
        self.ui.table_enter_matrix.setColumnCount(self.size_of_matrix)
        self.ui.table_enter_matrix.setRowCount(self.size_of_matrix)
        for i in range(0, self.size_of_matrix):
            for j in range(0, self.size_of_matrix):
                item = QTableWidgetItem(str(self.read_matrix[i][j]))
                item.setTextAlignment(Qt.AlignHCenter)
                if self.read_matrix[i][j] != 0:
                    item.setBackground(QColor(51,153,255))
                elif i == j:
                    item.setBackground(QColor(255,102,102))
                self.ui.table_enter_matrix.setItem(i,j, item)
     
    def show_print_all_conection(self):
        self.ui.text_con.clear() 
        self.ui.text_con.append("Усі зв'язки графа:")
        for i in range(0, len(self.matrix_of_conection)):
            self.ui.text_con.append(str(i+1) + ". [" + str(self.matrix_of_conection[i][0]+1) + 
                                    "; " + str(self.matrix_of_conection[i][1]+1) + "] --> " +
                                    str(self.read_matrix[self.matrix_of_conection[i][0]][self.matrix_of_conection[i][1]]))
        self.ui.text_con.append("\nСтепені вузлів:")
        odd_oddness = self.get_odd()
        #print(odd_oddness)
        for i in range(self.size_of_matrix):
            self.ui.text_con.append("Вузол " + str(i+1) + " має " + str(odd_oddness[i]) + " степінь")
        
        temp_state = []
        for el in odd_oddness:
            if el > 1:
                temp_state.append(True)
            else:
                temp_state.append(False)        
        if all(temp_state) == False or self.size_of_matrix < 3:
            self.ui.label_circle_presence.setText("В графі немає Гамільтонового циклу!!!")
            self.state = False
        else:
            self.ui.label_circle_presence.setText("В графі є Гамільтоновий цикл!!!")
            self.state = True
        
    def read_matrix_from_file(self):
        self.size_of_matrix = 0
        self.read_matrix = []
        self.matrix_of_conection = []
        name = self.ui.file_name.text()
        if name == "":
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Потрібно ввести назву вхідного файлу")
            msgBox.setWindowTitle("ERROR")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            self.ui.file_name.clear()
            return
        try:
            with open(name + '.txt') as file:
                for n, line in enumerate(file):
                    if n == 0:
                        self.size_of_matrix = int(line.strip())
                    else:
                        b = line.strip()
                        b = b.split(' ')
                        b = [int(i) for i in b]
                        self.read_matrix.append(b)
        except FileNotFoundError:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Такого файлу немає в кореневій папці!!!")
            msgBox.setWindowTitle("ERROR")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            self.ui.file_name.clear()
            return
        #matrix_of_conection = []
        for i in range(0, self.size_of_matrix):
            for j in range(i, self.size_of_matrix):
                if self.read_matrix[i][j] != 0:
                    self.matrix_of_conection.append([i, j])
        #print(matrix_of_conection)
        
        self.ui.groupBox_1.setTitle("Матриця суміжності вхідного графа:")
        self.show_read_matrix()
        self.ui.groupBox_2.setTitle("Графічне зображення вхідного графа:")
        self.show_graph()
        self.ui.groupBox_3.setTitle("Зв'язки вхідного графа та парність вузлів:")
        self.show_print_all_conection()

    def get_odd(self):
        degrees = [0 for i in range(len(self.read_matrix))]
        for i in range(len(self.read_matrix)):
            for j in range(len(self.read_matrix)):
                    if(self.read_matrix[i][j]!=0):
                        degrees[i]+=1
        #print(degrees)
        return degrees
    
    def start(self):
        if self.state == True:            
            self.final_path = [None] * (self.size_of_matrix + 1)
            self.visited = [False] * self.size_of_matrix
            self.final_res = float('inf')
            
            self.TSP()            
            final_path_nodes = []
            for i in range(len(self.final_path)-1):
                final_path_nodes.append([self.final_path[i], self.final_path[i+1]])
            
            self.ui.groupBox_1.setTitle("Матриця Гамільтонового циклу:")
            self.show_cicle_matrix(final_path_nodes)

            self.ui.groupBox_2.setTitle("Графічне відображення Гамільтонового циклу(червоні ребра):")            
            self.show_cicle_graph(final_path_nodes)
            
            temp = ''
            for i in range(len(self.final_path)):
                temp += str(self.final_path[i]+1) + ' --> '
            temp = temp[:-5]
            #rint(temp)            
            self.ui.groupBox_3.setTitle("Результати знаходження Гамільтонового цикл:")
            self.ui.text_con.clear()
            self.ui.text_con.append("Гамільтоновоий цикл:")
            self.ui.text_con.append(temp)
            self.ui.text_con.append("Сума ребер Гамільтонового циклу: " + str(self.final_res))             
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("У цьому графі відсутній гамільтоновий цикл, змініть граф!!!")
            msgBox.setWindowTitle("ERROR")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            return

    def show_cicle_matrix(self, mat):
        mat_res_nodes = np.zeros([self.size_of_matrix, self.size_of_matrix], dtype=int)
        for i in range(0, self.size_of_matrix):
            for j in range(0, self.size_of_matrix):
                for elem in mat:
                    if elem[0] == i and elem[1] == j:
                        mat_res_nodes[elem[0]][elem[1]] = self.read_matrix[i][j]
                    elif elem[0] == j and elem[1] == i:
                        mat_res_nodes[elem[1]][elem[0]] = self.read_matrix[i][j]

        self.ui.table_enter_matrix.setColumnCount(self.size_of_matrix)
        self.ui.table_enter_matrix.setRowCount(self.size_of_matrix)
        for i in range(0, self.size_of_matrix):
            for j in range(0, self.size_of_matrix):
                item = QTableWidgetItem(str(mat_res_nodes[i][j]))
                item.setTextAlignment(Qt.AlignHCenter)
                if mat_res_nodes[i][j] != 0:
                    item.setBackground(QColor(51,153,255))
                elif i == j:
                    item.setBackground(QColor(255,102,102))
                self.ui.table_enter_matrix.setItem(i,j, item)
    
    def show_cicle_graph(self, pair):
        for el in pair:
            temp = 0
            if el[0] > el[1]:
                temp = el[0]
                el[0] = el[1]
                el[1] = temp
        G = nx.Graph()        
        for i in range(len(self.matrix_of_conection)):
            if self.matrix_of_conection[i] in pair:
                G.add_edge(self.matrix_of_conection[i][0]+1,
                           self.matrix_of_conection[i][1]+1,
                           color = 'red',
                           weight = self.read_matrix[self.matrix_of_conection[i][0]][self.matrix_of_conection[i][1]])
            else:
                G.add_edge(self.matrix_of_conection[i][0]+1,
                           self.matrix_of_conection[i][1]+1,
                           color = 'black',
                           weight = self.read_matrix[self.matrix_of_conection[i][0]][self.matrix_of_conection[i][1]])
            
        plt.figure(figsize=(self.size_of_matrix+1 , self.size_of_matrix+1))
        
        color = nx.get_edge_attributes(G,'color').values()
        
        pos=nx.planar_layout(G)
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=1300, font_size=21,
                width=3, node_color='lime', edge_color=color)
        edge_weight = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weight, label_pos=0.5,
                                     font_size=13, font_color='red')
        #plt.show()
        plt.savefig("filename.png")
        #self.scene = QtWidgets.QGraphicsScene(self)
        pixmap = QPixmap("filename.png")
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.scene.addItem(item)
        self.ui.graphicsView.setScene(self.scene)
    
    def copyToFinal(self, curr_path):
        self.final_path[:self.size_of_matrix + 1] = curr_path[:]
        self.final_path[self.size_of_matrix] = curr_path[0]
      
    def firstMin(self, i):
        min = float('inf')
        for k in range(self.size_of_matrix):
            if self.read_matrix[i][k] < min and i != k:
                min = self.read_matrix[i][k]      
        return min
      
    def secondMin(self, i):
        first, second = float('inf'), float('inf')
        for j in range(self.size_of_matrix):
            if i == j:
                continue
            if self.read_matrix[i][j] <= first:
                second = first
                first = self.read_matrix[i][j]
      
            elif(self.read_matrix[i][j] <= second and 
                 self.read_matrix[i][j] != first):
                second = self.read_matrix[i][j]      
        return second
      
    def TSPRec(self, curr_bound, curr_weight, level, curr_path):
        if level == self.size_of_matrix:
            if self.read_matrix[curr_path[level - 1]][curr_path[0]] != 0:
                curr_res = curr_weight + self.read_matrix[curr_path[level - 1]]\
                                            [curr_path[0]]
                if curr_res < self.final_res:
                    self.copyToFinal(curr_path)
                    self.final_res = curr_res
            return
      
        for i in range(self.size_of_matrix):
            if (self.read_matrix[curr_path[level-1]][i] != 0 and
                                self.visited[i] == False):
                temp = curr_bound
                curr_weight += self.read_matrix[curr_path[level - 1]][i]
      
                if level == 1:
                    curr_bound -= ((self.firstMin(curr_path[level - 1]) + 
                                    self.firstMin(i)) / 2)
                else:
                    curr_bound -= ((self.secondMin(curr_path[level - 1]) +
                                     self.firstMin(i)) / 2)
      
                if curr_bound + curr_weight < self.final_res:
                    curr_path[level] = i
                    self.visited[i] = True
                      
                    self.TSPRec(curr_bound, curr_weight, level + 1, curr_path)
      
                curr_weight -= self.read_matrix[curr_path[level - 1]][i]
                curr_bound = temp
      
                self.visited = [False] * len(self.visited)
                for j in range(level):
                    if curr_path[j] != -1:
                        self.visited[curr_path[j]] = True
      
    def TSP(self):
        curr_bound = 0
        curr_path = [-1] * (self.size_of_matrix + 1)
        self.visited = [False] * self.size_of_matrix
      
        for i in range(self.size_of_matrix):
            curr_bound += (self.firstMin(i) + 
                           self.secondMin(i))
      
        curr_bound = math.ceil(curr_bound / 2)
      
        self.visited[0] = True
        curr_path[0] = 0
      
        self.TSPRec(curr_bound, 0, 1, curr_path)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec())
    warnings.simplefilter("ignore", UserWarning)

