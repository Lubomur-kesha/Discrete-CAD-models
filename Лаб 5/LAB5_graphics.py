from qt_5 import *
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QColor, QKeySequence
from PyQt5.QtCore import Qt
import os
import sys
import numpy as np
import math
import itertools
import warnings
import networkx as nx
import matplotlib.pyplot as plt

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
                
        self.size_of_matrix_left, self.size_of_matrix_right = 0, 0
        self.read_matrix_left, self.read_matrix_right = [], []
        self.matrix_of_conection_left, self.matrix_of_conection_right = [], []
        self.scene_left, self.scene_right = None, None
        self.state = None
        
        self.ui.btn_choose_left.clicked.connect(self.read_matrix_left_from_file)
        self.ui.btn_choose_right.clicked.connect(self.read_matrix_right_from_file)
        
        self.ui.btn_count.clicked.connect(self.start)
        self.ui.btn_clear.clicked.connect(self.clear)
        
    def clear(self):
        self.ui.file_name_left.clear()
        self.ui.table_enter_matrix_left.setRowCount(0)
        self.ui.table_enter_matrix_left.setColumnCount(0)
        self.scene_left.clear()
        self.ui.graphicsView_left.items().clear()
        
        self.ui.file_name_right.clear()
        self.ui.table_enter_matrix_right.setRowCount(0)
        self.ui.table_enter_matrix_right.setColumnCount(0)
        self.scene_right.clear()
        self.ui.graphicsView_right.items().clear()
        
        self.ui.text_con.clear()
    
    def show_graph_left(self):
        G = nx.Graph()
        for i in range(len(self.matrix_of_conection_left)):
            if self.read_matrix_left[self.matrix_of_conection_left[i][0]][self.matrix_of_conection_left[i][1]] == 1:
                            G.add_edge(self.matrix_of_conection_left[i][0]+1,
                                       self.matrix_of_conection_left[i][1]+1)
            else:
                G.add_edge(self.matrix_of_conection_left[i][0]+1,
                           self.matrix_of_conection_left[i][1]+1,
                           weight = self.read_matrix_left[self.matrix_of_conection_left[i][0]][self.matrix_of_conection_left[i][1]])
        
        plt.figure(figsize=(self.size_of_matrix_left+1, self.size_of_matrix_left+1))
        
        pos = nx.spring_layout(G, scale=3)
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=1000, font_size=21,
                width=3, node_color='lime')
        edge_weight = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weight, label_pos=0.5,
                                     font_size=13, font_color='red')
        plt.savefig("filename.png")
        pixmap = QPixmap("filename.png")
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        self.scene_left = QtWidgets.QGraphicsScene(self)
        self.scene_left.addItem(item)
        self.ui.graphicsView_left.setScene(self.scene_left)
                
    def show_read_matrix_left(self):
        self.ui.table_enter_matrix_left.setColumnCount(self.size_of_matrix_left)
        self.ui.table_enter_matrix_left.setRowCount(self.size_of_matrix_left)
        for i in range(0, self.size_of_matrix_left):
            for j in range(0, self.size_of_matrix_left):
                item = QTableWidgetItem(str(self.read_matrix_left[i][j]))
                item.setTextAlignment(Qt.AlignHCenter)
                if self.read_matrix_left[i][j] != 0:
                    item.setBackground(QColor(51,153,255))
                elif i == j:
                    item.setBackground(QColor(255,102,102))
                self.ui.table_enter_matrix_left.setItem(i,j, item)
                
    def read_matrix_left_from_file(self):
        self.size_of_matrix_left = 0
        self.read_matrix_left = []
        self.matrix_of_conection_left = []
        name = self.ui.file_name_left.text()
        if name == "":
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Потрібно ввести назву вхідного файлу")
            msgBox.setWindowTitle("ERROR")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            self.ui.file_name_left.clear()
            return
        try:
            with open(name + '.txt') as file:
                for n, line in enumerate(file):
                    if n == 0:
                        self.size_of_matrix_left = int(line.strip())
                    else:
                        b = line.strip()
                        b = b.split(' ')
                        b = [int(i) for i in b]
                        self.read_matrix_left.append(b)
            self.graph = np.array(self.read_matrix_left).tolist()
        except FileNotFoundError:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Такого файлу немає в кореневій папці!!!")
            msgBox.setWindowTitle("ERROR")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            self.ui.file_name_left.clear()
            return
        
        for i in range(0, self.size_of_matrix_left):
            for j in range(i, self.size_of_matrix_left):
                if self.read_matrix_left[i][j] != 0:
                    self.matrix_of_conection_left.append([i, j])
        
        self.ui.label_left.setText("Матриця суміжності графа ліворуч:")
        self.show_read_matrix_left()
        self.ui.groupBox_left.setTitle("Графічне зображення Першого графа:")
        self.show_graph_left()
       
    def show_graph_right(self):
        G = nx.Graph()
        for i in range(len(self.matrix_of_conection_right)):
            if self.read_matrix_right[self.matrix_of_conection_right[i][0]][self.matrix_of_conection_right[i][1]] == 1:
                G.add_edge(self.matrix_of_conection_right[i][0]+1,
                           self.matrix_of_conection_right[i][1]+1)
            else:
                G.add_edge(self.matrix_of_conection_right[i][0]+1,
                           self.matrix_of_conection_right[i][1]+1,
                           weight = self.read_matrix_right[self.matrix_of_conection_right[i][0]][self.matrix_of_conection_right[i][1]])
        
        plt.figure(figsize=(self.size_of_matrix_right+1, self.size_of_matrix_right+1))
        
        pos = nx.circular_layout(G, scale=3)
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=1000, font_size=21,
                width=3, node_color='lime')
        edge_weight = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weight, label_pos=0.5,
                                     font_size=13, font_color='red')
        plt.savefig("filename1.png")
        pixmap = QPixmap("filename1.png")
        item = QtWidgets.QGraphicsPixmapItem(pixmap)
        self.scene_right = QtWidgets.QGraphicsScene(self)
        self.scene_right.addItem(item)
        self.ui.graphicsView_right.setScene(self.scene_right)
                
    def show_read_matrix_right(self):
        self.ui.table_enter_matrix_right.setColumnCount(self.size_of_matrix_right)
        self.ui.table_enter_matrix_right.setRowCount(self.size_of_matrix_right)
        for i in range(0, self.size_of_matrix_right):
            for j in range(0, self.size_of_matrix_right):
                item = QTableWidgetItem(str(self.read_matrix_right[i][j]))
                item.setTextAlignment(Qt.AlignHCenter)
                if self.read_matrix_right[i][j] != 0:
                    item.setBackground(QColor(51,153,255))
                elif i == j:
                    item.setBackground(QColor(255,102,102))
                self.ui.table_enter_matrix_right.setItem(i,j, item)
         
    def read_matrix_right_from_file(self):
        self.size_of_matrix_right = 0
        self.read_matrix_right = []
        self.matrix_of_conection_right = []
        name = self.ui.file_name_right.text()
        if name == "":
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Потрібно ввести назву вхідного файлу")
            msgBox.setWindowTitle("ERROR")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            self.ui.file_name_right.clear()
            return
        try:
            with open(name + '.txt') as file:
                for n, line in enumerate(file):
                    if n == 0:
                        self.size_of_matrix_right = int(line.strip())
                    else:
                        b = line.strip()
                        b = b.split(' ')
                        b = [int(i) for i in b]
                        self.read_matrix_right.append(b)
        except FileNotFoundError:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Такого файлу немає в кореневій папці!!!")
            msgBox.setWindowTitle("ERROR")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            self.ui.file_name_right.clear()
            return
        
        for i in range(0, self.size_of_matrix_right):
            for j in range(i, self.size_of_matrix_right):
                if self.read_matrix_right[i][j] != 0:
                    self.matrix_of_conection_right.append([i, j])
        
        self.ui.label_right.setText("Матриця суміжності графа праворуч:")
        self.show_read_matrix_right()
        self.ui.groupBox_right.setTitle("Графічне зображення Другого графа:")
        self.show_graph_right()
    
    def start(self):
        if not self.read_matrix_left:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Ви не зчитали Лівий граф!!!")
            msgBox.setWindowTitle("ERROR")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            return
        elif not self.read_matrix_right:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Ви не зчитали Правий граф!!!")
            msgBox.setWindowTitle("ERROR")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            return
            
        A1 = np.array(self.read_matrix_left)
        A2 = np.array(self.read_matrix_right)
        
        self.state = self.brute_force_test_graph_isomporphism(A1, A2)
        if self.state == False:
            #print("Графи не є ізоморфними!!!")
            self.ui.text_con.append("Графи не є ізоморфними!!!")
    
    def get_graph_order(self, adj_matrix):
        if len(adj_matrix) != len(adj_matrix[0]):
            return -1
        else:
            return len(adj_matrix)
    
    def edge_set(self, adj_matrix):
        edge_set = []
        for row in range(len(adj_matrix)):
            for col in range(len(adj_matrix[0])):
                if (list(np.sort([row, col])) not in edge_set):
                    if adj_matrix[row][col] == 1:
                        edge_set.append(list(np.sort([row, col])))
        return sorted(edge_set)
    
    # Function that receives a vertex permutation and edge set and returns the corresponding edge permutation
    def edge_permutation(self, vertex_perm, original_edge_set):
        edge_set_perm = []
        for edge in original_edge_set:
            edge_set_perm.append(edge.copy())
        for edge in edge_set_perm:
            edge[0] = vertex_perm[edge[0]]
            edge[1] = vertex_perm[edge[1]]
        return [original_edge_set, edge_set_perm]
    
    
    def get_all_vertex_permutations(self, adj_matrix):
        if self.get_graph_order(adj_matrix) > 8:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Ця програма занадто неефективна для графа, \n в якому більше 8 вузлів")
            msgBox.setWindowTitle("ERROR")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
            return
        all_adj_matrix = []
        original_edge_set = self.edge_set(adj_matrix)
        idx = list(range(len(adj_matrix)))
        possible_idx_combinations = [
            list(i) for i in itertools.permutations(idx, len(idx))
        ]
        for idx_comb in possible_idx_combinations:
            a = adj_matrix
            a = a[idx_comb]
            a = np.transpose(np.transpose(a)[idx_comb])
            all_adj_matrix.append({
                "perm_vertex":
                idx_comb,
                "perm_edge":
                self.edge_permutation(idx_comb, original_edge_set),
                "adj_matrix":
                a
            })       
        return all_adj_matrix
      
    def first_idx_unseen(self, seen_array):
        for i in range(len(seen_array)):
            if seen_array[i] == False:
                return i
    
    def order_cycle(self, cycle):
        min_value_idx = cycle.index(min(cycle))
        return cycle[min_value_idx:] + cycle[:min_value_idx]
    
    def cycle_notation(self, permutation):
        result = []
        cycle = []
        idx = 0
        idx_to_check = len(permutation)
        seen = [False] * len(permutation)
    
        while idx_to_check > 0:
            while (seen[idx] == False):
                cycle.append(permutation[idx])
                seen[idx] = True
                idx = permutation[idx] - 1
                idx_to_check -= 1
            result.append(order_cycle(cycle))
            cycle = []
            idx = first_idx_unseen(seen)
        return result
    
    def get_degree_sequence(self, adj_matrix):
        degree_sequence = []
        for vertex in range(len(adj_matrix)):
            degree_sequence.append(sum(adj_matrix[vertex]))
        degree_sequence.sort(reverse=True)
        return degree_sequence
    
    def get_odd(self, adj_matrix):
        degrees = [0 for i in range(len(adj_matrix))]
        for i in range(len(adj_matrix)):
            for j in range(len(adj_matrix)):
                if(adj_matrix[i][j]!=0):
                    degrees[i]+=1
        return degrees
    
    def brute_force_test_graph_isomporphism(self, adj_1, adj_2):
        self.ui.text_con.clear()
        degree_sequence_1 = self.get_odd(adj_1)
        self.ui.text_con.append("Список впорядкованих степенів для графа ліворуч:")
        self.ui.text_con.append(str(sorted(degree_sequence_1)))
        #print(degree_sequence_1)
        degree_sequence_2 = self.get_odd(adj_2)
        self.ui.text_con.append("Список впорядкованих степенів для графа правору:")
        self.ui.text_con.append(str(sorted(degree_sequence_2)))
        #print(degree_sequence_2)
        if self.get_graph_order(adj_1) != self.get_graph_order(adj_1):
            return False
        elif np.array_equal(sorted(degree_sequence_1), sorted(degree_sequence_2)) == False:
            return False
        else:
            res = None
            for adj_matrix in list(
                    map(lambda matrix: matrix["adj_matrix"],
                        self.get_all_vertex_permutations(adj_2))):
                if np.array_equal(adj_1, adj_matrix) == True:
                    self.ui.text_con.append("")
                    self.ui.text_con.append("Відповідність вершин графа:")                    
                    c = self.get_all_vertex_permutations(adj_2)
                    for dictionary in c:
                        if np.array_equal(dictionary["adj_matrix"], adj_matrix):
                            res = dictionary["perm_vertex"]
                    for i in range(len(res)):
                        self.ui.text_con.append("Вершина лівого графа " + str(i+1) + " це вершина правого графа " + str(res[i]+1))
                    #print(res)
                    return True
        return False

        
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec())
    warnings.simplefilter("ignore", UserWarning)

