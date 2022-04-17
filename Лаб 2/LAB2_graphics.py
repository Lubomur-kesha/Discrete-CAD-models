from qt_2 import *
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
        self.distance = 0
        self.repeated_edges = []
        self.state = None
        
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
        odd_oddness, odds = self.get_odd()
        for i in range(self.size_of_matrix):
            self.ui.text_con.append("Вузол " + str(i+1) + " має " + str(odd_oddness[i]) + " степінь")
        
        if len(odds) != 0:
            self.ui.label_circle_presence.setText("Цей граф не є Ейлеровим і в ньому немає Ейлерового циклу!!!")
            self.state = False
        else:
            self.ui.label_circle_presence.setText("Цей граф є Ейлеровим і в ньому є Ейлеровий цикл!!!")
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
        odds = [i for i in range(len(degrees)) if degrees[i]%2!=0]
        #print('odds are:',odds)
        return degrees, odds
    
    def start(self):
        mat_of_distance = []
        self.ui.groupBox_1.setTitle("Матриця відстаней для кожного вузла:")
        for i in range(self.size_of_matrix):
            mat_of_distance.append(self.dijkstra_mat(i))
        self.ui.table_enter_matrix.setColumnCount(self.size_of_matrix)
        self.ui.table_enter_matrix.setRowCount(self.size_of_matrix)
        for i in range(0, self.size_of_matrix):
            for j in range(0, self.size_of_matrix):
                item = QTableWidgetItem(str(mat_of_distance[i][j]))
                item.setTextAlignment(Qt.AlignHCenter)
                if mat_of_distance[i][j] != 0:
                    item.setBackground(QColor(51,153,255))
                elif i == j:
                    item.setBackground(QColor(255,102,102))
                self.ui.table_enter_matrix.setItem(i,j, item)
        
        if self.state == False:
            self.repeated_edges = []
            res_sum,  res_pair = self.Chinese_Postman()
            
            for i in range(len(res_pair)):
                self.get_repeated_edges(res_pair[i][0]+1, res_pair[i][1]+1)
            self.ui.text_con.append("Ребра, які при обході листоноші будуть повторюватися:")
            for i in range(len(self.repeated_edges)):
                self.ui.text_con.append(str(i+1) + ") " + str(self.repeated_edges[i]) + " --> " +
                                        str(self.read_matrix[self.repeated_edges[i][0]-1][self.repeated_edges[i][1]-1]))
            
            mat_of_conection = []
            for el in self.matrix_of_conection:
                mat_of_conection.append([el[0]+1, el[1]+1])
            all_edges = mat_of_conection + self.repeated_edges
            for el in all_edges:
                if el[0] > el[1]:
                    temp = el[1]
                    el[1] = el[0]
                    el[0] = temp
            
            all_edges_tuple = []
            for el in all_edges:
                all_edges_tuple.append(tuple(el))
            #list_of_postman_tour = self.find_eulerian_tour(all_edges)
            list_of_postman_tour = self.find_eulerian_tour(all_edges_tuple)
            str_tour = ''
            for el in list_of_postman_tour:
                str_tour += str(el) + " --> "
            self.ui.text_con.append("Маршрут листоноші:")
            self.ui.text_con.append(str_tour[:-4])
            
            self.ui.text_con.append("Загальна довжина цього маршруту дорівнює: " + str(res_sum))
            
            self.ui.groupBox_2.setTitle("Модифікований граф (повторні ребра червоного кольору):")
            self.show_graph_double(mat_of_conection)
        elif self.state == True:
            mat_of_conection = []
            edges_tuple = []
            for el in self.matrix_of_conection:
                edges_tuple.append(tuple([el[0]+1, el[1]+1]))
            list_of_postman_tour = self.find_eulerian_tour(edges_tuple)
            str_tour = ''
            for el in list_of_postman_tour:
                str_tour += str(el) + " --> "
            self.ui.groupBox_3.setTitle("Ейлерів цикл:")
            self.ui.text_con.clear()
            self.ui.text_con.append("Ейлерів циклі:")
            self.ui.text_con.append(str_tour[:-4])
            self.ui.text_con.append("Загальна довжина цього маршруту дорівнює: " + str(self.sum_edges()))
            self.show_graph()
    
    def get_repeated_edges(self, start, end):
        G = nx.Graph()
        for i in range(len(self.matrix_of_conection)):
            G.add_edge(self.matrix_of_conection[i][0]+1,
                       self.matrix_of_conection[i][1]+1,
                       weight = self.read_matrix[self.matrix_of_conection[i][0]][self.matrix_of_conection[i][1]])
        min_dist = nx.shortest_path(G,source=start,target=end, weight='weight')
        for i in range(0, len(min_dist)-1):
            self.repeated_edges.append([min_dist[i], min_dist[i+1]])
        
            
    def dijkstra_mat(self, src):
        visited = []
        distance = {src: 0}
        node = list(range(len(self.read_matrix[0])))
        if src in node:
            node.remove(src)
            visited.append(src)
        else:
            return None
        for i in node:
            distance[i] = self.read_matrix[src][i]
        prefer = src
        while node:
            _distance = float('inf')
            for i in visited:
                for j in node:
                    if self.read_matrix[i][j] > 0:
                        if _distance > distance[i] + self.read_matrix[i][j]:
                            _distance = distance[j] = distance[i] + self.read_matrix[i][j]
                            prefer = j
            visited.append(prefer)
            node.remove(prefer)
        
        distance_list = []
        for i in range(0, len(distance)):
            distance_list.append(0)
        for i in distance.keys():
            distance_list[i] = int(distance[i])
        return distance_list

    def sum_edges(self):
        w_sum = 0
        l = len(self.read_matrix)
        for i in range(l):
            for j in range(i,l):
                w_sum += self.read_matrix[i][j]
        return w_sum
                    
    def dijktra(self, source, dest):
        shortest = [0 for i in range(len(self.read_matrix))]
        selected = [source]
        #print(selected)
        l = len(self.read_matrix)

        inf = 10000000
        min_sel = inf
        for i in range(l):
            if(i==source):
                shortest[source] = 0
            else:
                if(self.read_matrix[source][i]==0):
                    shortest[i] = inf
                else:
                    shortest[i] = self.read_matrix[source][i]
                    if(shortest[i] < min_sel):
                        min_sel = shortest[i]
                        ind = i
                    
        if(source==dest):
            return 0
        selected.append(ind) 
        #print(selected)
        while(ind!=dest):
            #print('ind',ind)
            for i in range(l):
                if i not in selected:
                    if(self.read_matrix[ind][i]!=0):
                        if((self.read_matrix[ind][i] + min_sel) < shortest[i]):
                            #print(min_sel)
                            #print(graph[ind][i])
                            shortest[i] = self.read_matrix[ind][i] + min_sel
            temp_min = 1000000
            #print('shortest:',shortest)
            #print('selected:',selected)
            
            for j in range(l):
                if j not in selected:
                    if(shortest[j] < temp_min):
                        temp_min = shortest[j]
                        ind = j
            min_sel = temp_min
            selected.append(ind)
        #print(shortest[dest])
        return shortest[dest]
    
    def gen_pairs(self, odds):
        pairs = []
        for i in range(len(odds)-1):
            pairs.append([])
            for j in range(i+1,len(odds)):
                pairs[i].append([odds[i],odds[j]])
            
        #print('pairs are:',pairs)
        #print('\n')
        return pairs
    
    def Chinese_Postman(self):
        degrees, odds = self.get_odd()
        if(len(odds)==0):
            return self.sum_edges()
        pairs = self.gen_pairs(odds)
        l = (len(pairs)+1)//2
        
        pairings_sum = []
        
        def get_pairs(pairs, done = [], final = []):
            
            if(pairs[0][0][0] not in done):
                done.append(pairs[0][0][0])
                
                for i in pairs[0]:
                    f = final[:]
                    val = done[:]
                    if(i[1] not in val):
                        f.append(i)
                    else:
                        continue
                    
                    if(len(f)==l):
                        pairings_sum.append(f)
                        return 
                    else:
                        val.append(i[1])
                        get_pairs(pairs[1:],val, f)
            else:
                get_pairs(pairs[1:], done, final)
        
        get_pairs(pairs)
        min_sums = []
        sum_between_pairs = []
        
        
        for i in pairings_sum:
            s = 0
            temp = []
            for j in range(len(i)):
                s += self.dijktra(i[j][0], i[j][1])
                temp.append(self.dijktra(i[j][0], i[j][1]))
            min_sums.append(s)
            sum_between_pairs.append(temp)
        #print(pairings_sum)
        #print(min_sums)
        #print(sum_between_pairs)
        self.ui.text_con.clear()
        self.ui.groupBox_3.setTitle("Кроки розв'язку за алгоритмом листоноші:")
        self.ui.text_con.append("Паросполучення та їх ваги:")
        str_temp = []
        for i in range(0, len(pairings_sum)):
            temp = str(i+1) + ") Вузли "
            for j in range(0,len(pairings_sum[i])):
                temp += "[" + str(pairings_sum[i][j][0] + 1) + "; " + str(pairings_sum[i][j][1] + 1) + "] та "
            temp = temp[:-3]
            temp += "--> "
            for j in range(0,len(pairings_sum[i])):
                temp += str(sum_between_pairs[i][j]) + " + "
            temp = temp[:-3]
            temp += " = " + str(min_sums[i])
            str_temp.append(temp)
            self.ui.text_con.append(temp)
        added_dis = min(min_sums)
        min_pair = pairings_sum[min_sums.index(added_dis)]
        self.ui.text_con.append("Вибране паросполучення:")
        self.ui.text_con.append(str_temp[min_sums.index(added_dis)])
        chinese_dis = added_dis + self.sum_edges()
        return chinese_dis, min_pair    
    
    def find_eulerian_tour(self, graph):
        '''
        S = graph[0]
        graph.remove(S)
        C = []
        while len(graph) != 0:
            for el in graph:
                if S[-1] in el:
                    temp = el
                    graph.remove(el)
                    graph = [el] + graph
                    break
            if graph[0][0] == S[-1]:
                S.append(graph[0][1])
                graph.remove(graph[0])
            elif graph[0][1] == S[-1]:
                S.append(graph[0][0])
                graph.remove(graph[0])
            elif graph[0][0] != S[-1] and  graph[0][1] != S[-1]:
                C.append(S[-1])
                S = S[:-1]
        for i in range(len(C)-1, -1, -1):
            S.append(C[i])
        return S
        
        '''
        def freqencies():
            my_list = [x for (x, y) in graph]
            
            result = [0 for i in range(max(my_list) + 1)]
            
            for i in my_list:
                result[i] += 1
            return result
            
        def find_node(tour):
            for i in tour:
                if freq[i] != 0:
                    return i
            return -1
        
        def helper(tour, next):
            find_path(tour, next)
            u = find_node(tour)
            while sum(freq) != 0:     
                sub = find_path([], u)
                
                tour = tour[:tour.index(u)] + sub + tour[tour.index(u) + 1:]  
                u = find_node(tour)
            return tour
        
        def find_path(tour, next):
            for (x, y) in graph:
                if x == next:
                    current = graph.pop(graph.index((x,y)))
                    graph.pop(graph.index((current[1], current[0])))
                    
                    tour.append(current[0])
                    
                    freq[current[0]] -= 1
                    freq[current[1]] -= 1
                    return find_path(tour, current[1])
            tour.append(next)
            return tour             
        
        graph += [(y, x) for (x, y) in graph]
        freq = freqencies()   
        
        return helper([], graph[0][0])
        

    def show_graph_double(self, mat):
        G = nx.Graph()   
        for i in range(len(mat)):
            if mat[i] in self.repeated_edges:
                G.add_edge(mat[i][0], mat[i][1], color = 'red',
                           weight = self.read_matrix[mat[i][0]-1][mat[i][1]-1])
            else:
                G.add_edge(mat[i][0], mat[i][1], color = 'black',
                           weight = self.read_matrix[mat[i][0]-1][mat[i][1]-1])
            
        plt.figure(figsize=(self.size_of_matrix+1 , self.size_of_matrix+1))
        
        color = nx.get_edge_attributes(G,'color').values()
        
        pos=nx.planar_layout(G)
        #pos = nx.random_layout(G)
        nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=1300, font_size=21,
                width=3, node_color='lime', edge_color=color)
        edge_weight = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_weight, label_pos=0.5,
                                     font_size=13, font_color='red')
        
        plt.savefig("filename.png")
        #self.scene = QtWidgets.QGraphicsScene(self)
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

