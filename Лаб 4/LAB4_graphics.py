from qt_4 import *
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
        self.graph = []
        self.ROW = 0
        
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
        G = nx.DiGraph()
        for i in range(len(self.matrix_of_conection)):
            G.add_edge(self.matrix_of_conection[i][0]+1,
                       self.matrix_of_conection[i][1]+1,
                       weight = self.read_matrix[self.matrix_of_conection[i][0]][self.matrix_of_conection[i][1]])
        
        plt.figure(figsize=(self.size_of_matrix+1, self.size_of_matrix+1))
        
        pos=nx.planar_layout(G)
        #pos = nx.random_layout(G)
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=1000, font_size=21,
                width=3, node_color='lime')
        edge_weight = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weight, label_pos=0.5,
                                     font_size=13, font_color='red')
        nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=17)
        plt.savefig("filename.png")
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
            
        self.graph = np.array(self.read_matrix).tolist()
        self.ROW = len(self.graph)
        parent = [-1] * (self.ROW)
        if self.searching_algo_BFS(0, len(self.graph)-1, parent) == True:
            self.ui.label_circle_presence.setText("В графі є потік з вершини 1 в вершину " +
                                                  str(self.size_of_matrix) + ":)")
            self.state = True
        else:
            self.ui.label_circle_presence.setText("В графі немає потоку з вершини 1 в вершину " +
                                                  str(self.size_of_matrix) + ", змініть граф!!!")
            self.state = False
        
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
            self.graph = np.array(self.read_matrix).tolist()
        except FileNotFoundError:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Такого файлу немає в кореневій папці!!!")
            msgBox.setWindowTitle("ERROR")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            self.ui.file_name.clear()
            return
        
        for i in range(0, self.size_of_matrix):
            for j in range(0, self.size_of_matrix):
                if self.read_matrix[i][j] != 0:
                    self.matrix_of_conection.append([i, j])
        
        self.ui.groupBox_1.setTitle("Матриця суміжності вхідного графа:")
        self.show_read_matrix()
        self.ui.groupBox_2.setTitle("Графічне зображення вхідного графа:")
        self.show_graph()
        self.ui.groupBox_3.setTitle("Зв'язки вхідного графа:")
        self.show_print_all_conection()
    
    def start(self):
        if self.state == True:
            self.ui.text_con.clear()
            self.graph = np.array(self.read_matrix).tolist()
            self.ROW = len(self.graph)
            self.ui.groupBox_3.setTitle("Результати знаходження максимального потоку: ")
            self.ford_fulkerson(0, self.size_of_matrix-1)
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("У цьому графі відсутній потік, з вершини 1 в вершину " +
                           str(self.size_of_matrix) + ", змініть граф!!!")
            msgBox.setWindowTitle("ERROR")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            return
    
    def searching_algo_BFS(self, s, t, parent):
        visited = [False] * (self.ROW)
        queue = []

        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.pop(0)
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
        return True if visited[t] else False

    def ford_fulkerson(self, source, destination):
        parent = [-1] * (self.ROW)
        max_flow = 0

        ctr = 1
        while self.searching_algo_BFS(source, destination, parent):
            path_flow = float("Inf")
            s = destination
            path = []
            path_weight = []
            while(s != source):
                #print(str(parent[s]+1) + "; " + str(s+1), end=" ")
                path.append([parent[s]+1, s+1])
                #print(self.graph[parent[s]][s])
                path_weight.append(self.graph[parent[s]][s])
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]
            
            temp = "1"
            for i in range(len(path)-1, -1, -1):
                temp += " - (" + str(path_weight[i]) + ") - " + str(path[i][1])
            temp += " - Мінімальне: " + str(path_flow)
            #print(temp)
            self.ui.text_con.append("Потік №" + str(ctr) + ": ")
            self.ui.text_con.append("  " + temp)
            
            max_flow += path_flow
            ctr += 1
            
            v = destination
            while(v != source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]
        #print(max_flow)
        self.ui.text_con.append("\n Значення максимального потоку: " + str(max_flow))
        
        flow_mat = []
        for i in range(len(self.graph)):
            temp = []
            for j in range(0, len(self.graph[i])):
                if [i, j] in self.matrix_of_conection:
                    temp.append(str(self.graph[i][j]) + "/" + str(self.graph[j][i]))
                else:
                    temp.append(str(0))
            flow_mat.append(temp)

        self.ui.groupBox_1.setTitle("Матриця потоків:")
        self.show_flow_matrix(flow_mat)

        self.ui.groupBox_2.setTitle("Графічне зображення потоків графа:")        
        self.show_flow_graph(flow_mat)

    
    def show_flow_matrix(self, flow):
        self.ui.table_enter_matrix.setColumnCount(self.size_of_matrix)
        self.ui.table_enter_matrix.setRowCount(self.size_of_matrix)
        for i in range(0, self.size_of_matrix):
            for j in range(0, self.size_of_matrix):
                item = QTableWidgetItem(str(flow[i][j]))
                item.setTextAlignment(Qt.AlignHCenter)
                if flow[i][j] != str(0):
                    item.setBackground(QColor(51,153,255))
                elif i == j:
                    item.setBackground(QColor(255,102,102))
                self.ui.table_enter_matrix.setItem(i,j, item)
    
    def show_flow_graph(self, flow):
        G = nx.DiGraph()
        for i in range(len(self.matrix_of_conection)):
            if self.graph[self.matrix_of_conection[i][0]][self.matrix_of_conection[i][1]] != self.read_matrix[self.matrix_of_conection[i][0]][self.matrix_of_conection[i][1]]:
                G.add_edge(self.matrix_of_conection[i][0]+1,
                           self.matrix_of_conection[i][1]+1,
                           color = "red",
                           weight = flow[self.matrix_of_conection[i][0]][self.matrix_of_conection[i][1]])
            else:
                G.add_edge(self.matrix_of_conection[i][0]+1,
                           self.matrix_of_conection[i][1]+1,
                           color = "black",
                           weight = flow[self.matrix_of_conection[i][0]][self.matrix_of_conection[i][1]])
            
        plt.figure(figsize=(self.size_of_matrix+1, self.size_of_matrix+1))

        color = nx.get_edge_attributes(G,'color').values()
        
        pos=nx.planar_layout(G)
        #pos = nx.random_layout(G)
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=1000, font_size=21,
                width=3, node_color='lime', edge_color=color)
        edge_weight = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weight, label_pos=0.5,
                                     font_size=13, font_color='red')
        nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=17)
        plt.savefig("filename.png")
        pixmap = QPixmap("filename.png")
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        self.scene = QtWidgets.QGraphicsScene(self)
        self.scene.addItem(item)
        self.ui.graphicsView.setScene(self.scene)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec())
    warnings.simplefilter("ignore", UserWarning)

