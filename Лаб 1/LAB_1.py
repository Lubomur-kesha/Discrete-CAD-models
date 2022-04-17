import numpy as np

def combine(pair):
    #print(pair)
    pair0 = -1
    pair1 = -1
    for i in range(0,len(matrix_of_edges)):
        if pair[0] in matrix_of_edges[i]:
            pair0 = i
        if pair[1] in matrix_of_edges[i]:
            pair1 = i
    matrix_of_edges[pair0] += matrix_of_edges[pair1]
    del matrix_of_edges[pair1]
    #print(matrix_of_edges)

def tree_way(mat, mat_edge, mat_con, size, tree):
    maximum = ['максимального', 'максимальні', 'максимальне', 'Максимальний']
    minimum = ['мінімального', 'мінімальні', 'мінімальне', 'Мінімальний']
    
    choosen = []
    if tree == 'MAX':
        choosen = maximum
    elif tree == 'MIN':
        choosen = minimum
    
    np_matrix = np.array(mat)
    weights = []
    pair_of_edges_for_result = []
    ctr = 0
    print("Пошук " + choosen[0] + " остового дерева:")
    while (len(mat_edge) > 1):
        edges = []
        for component in mat_edge:
            if tree == "MIN":
                temp = [np.amax(np_matrix)+1,[0,0]]
                #print(temp)
                for vertex in component:
                    for i in range(0,len(mat[0])):
                        if i not in component and mat[vertex][i] != 0:
                            if (temp[0] > mat[vertex][i]):
                                temp[0] = mat[vertex][i]
                                temp[1] = [vertex,i]
                if (temp[1][0] > temp[1][1]):
                    temp[1][0], temp[1][1] =  temp[1][1], temp[1][0]
                if (temp[1] not in edges):
                    edges.append(temp[1])
            elif tree == "MAX":
                temp = [np.amin(np_matrix)-1,[0,0]]
                for vertex in component:
                    for i in range(0,len(mat[0])):
                        if i not in component and mat[vertex][i] != 0:
                            if (temp[0] < mat[vertex][i]):
                                temp[0] = mat[vertex][i]
                                temp[1] = [vertex,i]
                if (temp[1][1] < temp[1][0]):
                    temp[1][1], temp[1][0] =  temp[1][0], temp[1][1]
                if (temp[1] not in edges):
                    edges.append(temp[1])
            #print(edges)
            #print(temp)
    
        for e in edges:
            combine(e)
        print("Крок №" + str(ctr+1))
        print("Вибрані " + choosen[1] + " ребра: " + str(edges))
        print("Згруповані пари вершин: " + str(mat_edge))
    
        for el in edges:
            pair_of_edges_for_result.append(el)
            weights.append(mat[el[0]][el[1]])
        print("Сума ваг остового дерева: " + str(sum(weights)), end="\n\n")
        ctr += 1
    
    #print(mat_con)
    #print(pair_of_edges_for_result)
    
    for elem in pair_of_edges_for_result:
        if elem in mat_con:
            del mat_con[mat_con.index(elem)]
    
    matrix_of_tree_res = mat.copy()
    for i in range(0, size):
        for j in range(0, size):
            for elem in mat_con:
                if elem[0] == i and elem[1] == j:
                    matrix_of_tree_res[elem[0]][elem[1]] = 0
                elif elem[0] == j and elem[1] == i:
                    matrix_of_tree_res[elem[1]][elem[0]] = 0
    print("Пари вершин або ребра, які утворюють " + choosen[2] + " остове дерево:")
    print(pair_of_edges_for_result, end="\n\n")
    
    print("Матриця " + choosen[0] + " остового дерева:")
    print(np.array(matrix_of_tree_res), end="\n\n")
    
    print(choosen[3] + " шлях остового дерева: ", str(sum(weights)), end="\n\n")

size_of_matrix = 0
read_matrix = []
with open('l1_3.txt') as file:
    for n, line in enumerate(file):
        if n == 0:
            size_of_matrix = int(line.strip())
        else:
            b = line.strip()
            b = b.split(' ')
            b = [int(i) for i in b]
            read_matrix.append(b)

print("Зчитана матриця:")
print(np.array(read_matrix), end="\n\n")

matrix_of_conection = []
for i in range(0, size_of_matrix):
    for j in range(i, size_of_matrix):
        if read_matrix[i][j] != 0:
            matrix_of_conection.append([i, j])
#print(matrix_of_conection)
            
matrix_of_edges = []
for i in range(0, size_of_matrix):
	matrix_of_edges.append([i])

tree_way(read_matrix, matrix_of_edges, matrix_of_conection, size_of_matrix, "MIN")