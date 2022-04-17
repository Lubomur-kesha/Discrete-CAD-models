from qt_1 import *
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QColor, QKeySequence
from PyQt5.QtCore import Qt
import os
import sys
import numpy as np
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
        self.matrix_of_edges = []
        
        self.ui.label_txt.setFont(QtGui.QFont('SansSerif', 11))
        self.ui.file_name.setFont(QtGui.QFont('SansSerif', 11))
        self.ui.btn_choose.setFont(QtGui.QFont('Arial', 11))
        self.ui.label_MIN_MAX.setFont(QtGui.QFont('SansSerif', 11))
        self.ui.line_MIN_MAX.setFont(QtGui.QFont('SansSerif', 11))
        self.ui.btn_MIN_MAX.setFont(QtGui.QFont('Arial', 11))
        self.ui.btn_clear.setFont(QtGui.QFont('Arial', 10))
                
        self.ui.btn_choose.clicked.connect(self.read_matrix_from_file)
        self.ui.btn_MIN_MAX.clicked.connect(self.tree_way)
        self.ui.btn_clear.clicked.connect(self.clear)
        
    def clear(self):
        self.ui.file_name.clear()
        self.ui.line_MIN_MAX.clear()
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
        
        plt.figure(figsize=(8.5, 8.5))
        
        pos=nx.planar_layout(G)
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
    
    def show_tree_graph(self, pair):
        G = nx.Graph()        
        for i in range(len(self.matrix_of_conection)):
            if self.matrix_of_conection[i] in pair:
                G.add_edge(self.matrix_of_conection[i][0]+1,
                           self.matrix_of_conection[i][1]+1,
                           color = 'lime',
                           weight = self.read_matrix[self.matrix_of_conection[i][0]][self.matrix_of_conection[i][1]])
            else:
                G.add_edge(self.matrix_of_conection[i][0]+1,
                           self.matrix_of_conection[i][1]+1,
                           color = 'black',
                           weight = self.read_matrix[self.matrix_of_conection[i][0]][self.matrix_of_conection[i][1]])
            
        plt.figure(figsize=(8.5, 8.5))
        
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
        
    def combine(self, pair):
        #print(pair)
        pair0 = -1
        pair1 = -1
        for i in range(0,len(self.matrix_of_edges)):
            if pair[0] in self.matrix_of_edges[i]:
                pair0 = i
            if pair[1] in self.matrix_of_edges[i]:
                pair1 = i
        self.matrix_of_edges[pair0] += self.matrix_of_edges[pair1]
        del self.matrix_of_edges[pair1]
        #print(mat_edges)
    
    def tree_way(self):
        self.ui.text_con.clear()
        maximum = ['максимального', 'максимальні', 'максимальне', 'Максимальний']
        minimum = ['мінімального', 'мінімальні', 'мінімальне', 'Мінімальний']
        
        choosen = []
        tree = self.ui.line_MIN_MAX.text()
        if tree == "":
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Потрібно ввести MIN або MAX!!!")
            msgBox.setWindowTitle("ERROR")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            self.ui.line_MIN_MAX.clear()
            return
      
        if tree == 'MAX':
            choosen = maximum
        elif tree == 'MIN':
            choosen = minimum
        
        self.matrix_of_edges = []
        for i in range(0, self.size_of_matrix):
        	self.matrix_of_edges.append([i])
        
        np_matrix = np.array(self.read_matrix)
        weights = []
        pair_of_edges_for_result = []
        ctr = 0
        #print("Пошук " + choosen[0] + " остового дерева:")
        self.ui.groupBox_3.setTitle("Пошук " + choosen[0] + " остового дерева:")
        while (len(self.matrix_of_edges) > 1):
            edges = []
            for component in self.matrix_of_edges:
                if tree == "MIN":
                    temp = [np.amax(np_matrix)+1,[0,0]]
                    #print(temp)
                    for vertex in component:
                        for i in range(0,len(self.read_matrix[0])):
                            if i not in component and self.read_matrix[vertex][i] != 0:
                                if (temp[0] > self.read_matrix[vertex][i]):
                                    temp[0] = self.read_matrix[vertex][i]
                                    temp[1] = [vertex,i]
                    if (temp[1][0] > temp[1][1]):
                        temp[1][0], temp[1][1] =  temp[1][1], temp[1][0]
                    if (temp[1] not in edges):
                        edges.append(temp[1])
                elif tree == "MAX":
                    temp = [np.amin(np_matrix)-1,[0,0]]
                    for vertex in component:
                        for i in range(0,len(self.read_matrix[0])):
                            if i not in component and self.read_matrix[vertex][i] != 0:
                                if (temp[0] < self.read_matrix[vertex][i]):
                                    temp[0] = self.read_matrix[vertex][i]
                                    temp[1] = [vertex,i]
                    if (temp[1][1] < temp[1][0]):
                        temp[1][1], temp[1][0] =  temp[1][0], temp[1][1]
                    if (temp[1] not in edges):
                        edges.append(temp[1])
                #print(edges)
                #print(temp)
        
            for e in edges:
                self.combine(e)
            #print("Крок №" + str(ctr+1))
            self.ui.text_con.append("Крок №" + str(ctr+1))
            
            #print("Вибрані " + choosen[1] + " ребра: " + str(edges))
            prnt_edges = []
            for i in range(len(edges)):
                temp = []
                for j in range(len(edges[i])):
                    temp.append(edges[i][j]+1)
                prnt_edges.append(temp)
            self.ui.text_con.append("Вибрані " + choosen[1] + " ребра: " + str(prnt_edges))
            #print("Згруповані пари вершин: " + str(self.matrix_of_edges))
            prnt_mat_edges = []
            for i in range(len(self.matrix_of_edges)):
                temp = []
                for j in range(len(self.matrix_of_edges[i])):
                    temp.append(self.matrix_of_edges[i][j]+1)
                prnt_mat_edges.append(temp)
            
            self.ui.text_con.append("Згруповані пари вершин: " + str(prnt_mat_edges))
        
            for el in edges:
                pair_of_edges_for_result.append(el)
                weights.append(self.read_matrix[el[0]][el[1]])
            #print("Сума ваг остового дерева: " + str(sum(weights)), end="\n\n")
            self.ui.text_con.append("Сума ваг остового дерева: " + str(sum(weights)) + "\n\n")
            ctr += 1
        
        #print(mat_con)
        #print(pair_of_edges_for_result)
        
        mat_con_copy = np.array(self.matrix_of_conection)
        mat_con_copy = mat_con_copy.tolist()
        for elem in pair_of_edges_for_result:
            if elem in mat_con_copy:
                del mat_con_copy[mat_con_copy.index(elem)]
        
        matrix_of_tree_res = np.array(self.read_matrix)
        #matrix_of_tree_res = self.read_matrix
        for i in range(0, self.size_of_matrix):
            for j in range(0, self.size_of_matrix):
                for elem in mat_con_copy:
                    if elem[0] == i and elem[1] == j:
                        matrix_of_tree_res[elem[0]][elem[1]] = 0
                    elif elem[0] == j and elem[1] == i:
                        matrix_of_tree_res[elem[1]][elem[0]] = 0
        #print(matrix_of_tree_res)
        #print("Пари вершин або ребра, які утворюють " + choosen[2] + " остове дерево:")
        self.ui.text_con.append("Пари вершин або ребра, які утворюють " + choosen[2] + " остове дерево:")
        #print(pair_of_edges_for_result, end="\n\n")
        prnt_pair_edges_res = []
        for i in range(len(pair_of_edges_for_result)):
            temp = []
            for j in range(len(pair_of_edges_for_result[i])):
                temp.append(pair_of_edges_for_result[i][j]+1)
            prnt_pair_edges_res.append(temp)
        self.ui.text_con.append(str(prnt_pair_edges_res) + "\n\n")
        
        #print("Матриця " + choosen[0] + " остового дерева:")
        #print(np.array(matrix_of_tree_res), end="\n\n")
        self.ui.groupBox_1.setTitle("Матриця " + choosen[0] + " остового дерева:")
        self.show_tree_matrix(matrix_of_tree_res)
        self.ui.groupBox_2.setTitle("Графічне зображення "  + choosen[0] + " остового дерева:")
        
        #print(choosen[3] + " шлях остового дерева: ", str(sum(weights)), end="\n\n")
        self.ui.text_con.append(choosen[3] + " шлях остового дерева: " + str(sum(weights)) + "\n\n")

        self.show_tree_graph(pair_of_edges_for_result)
        
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
    
    def show_tree_matrix(self, mat):
        self.ui.table_enter_matrix.setColumnCount(self.size_of_matrix)
        self.ui.table_enter_matrix.setRowCount(self.size_of_matrix)
        for i in range(0, self.size_of_matrix):
            for j in range(0, self.size_of_matrix):
                item = QTableWidgetItem(str(mat[i][j]))
                item.setTextAlignment(Qt.AlignHCenter)
                if mat[i][j] != 0:
                    item.setBackground(QColor(51,153,255))
                elif i == j:
                    item.setBackground(QColor(255,102,102))
                self.ui.table_enter_matrix.setItem(i,j, item)
    
    def show_print_all_conection(self):
        self.ui.text_con.clear() 
        for i in range(0, len(self.matrix_of_conection)):
            self.ui.text_con.append(str(i+1) + ". [" + str(self.matrix_of_conection[i][0]+1) + 
                                    "; " + str(self.matrix_of_conection[i][1]+1) + "] --> " +
                                    str(self.read_matrix[self.matrix_of_conection[i][0]][self.matrix_of_conection[i][1]]))
          
    def read_matrix_from_file(self):
        #size_of_matrix = 0
        #read_matrix = []
        self.size_of_matrix = 0
        self.read_matrix = []
        self.matrix_of_conection = []
        self.matrix_of_edges = []
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
        self.ui.groupBox_3.setTitle("Зв'язки вхідного графа:")
        self.show_print_all_conection()
        
        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec())
    warnings.simplefilter("ignore", UserWarning)

