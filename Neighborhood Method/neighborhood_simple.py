import csv
import math
import numpy as np

rating = []
testing = []
s = 0
n1 = 0
n2 = 0
user = 0
movie = 0
L = 2
RMSE = 0

# file = open('u1.csv', 'r')
file = open('training.csv', 'r')
lines = csv.reader(file)

for line in lines:
    rating.append([eval(line[0]) - 1, eval(line[1]) - 1, eval(line[2])])
    if rating[n1][0] > user:
        user = rating[n1][0]
    if rating[n1][1] > movie:
        movie = rating[n1][1]
    s += rating[n1][2]
    n1 += 1
user += 1
movie += 1

file.close()

# file = open('u1test.csv', 'r')
file = open('testing.csv', 'r')
lines = csv.reader(file)

for line in lines:
    testing.append([eval(line[0]) - 1, eval(line[1]) - 1, eval(line[2])])
    n2 += 1

file.close()
R = np.zeros([user, movie], dtype=float)
R1 = np.empty([user, movie], dtype=float)
Re = np.zeros([user, movie], dtype=float)
R2 = np.zeros([user, movie], dtype=float)
c = np.empty([n1, 1], dtype=float)
A = np.zeros([n1, user + movie], dtype=float)
D = np.zeros([movie, movie], dtype=list)
aver = s / n1

for rec in rating:
    R[rec[0]][rec[1]] = rec[2]

for i in range(n1):
    c[i][0] = rating[i][2] - aver
    A[i][rating[i][0]] = 1
    A[i][rating[i][1] + user] = 1

tmp = np.linalg.pinv(np.dot(A.T, A))
b = np.dot(tmp, np.dot(A.T, c))

for i in range(user):
    for j in range(movie):
        Re[i][j] = 6

for i in range(n1):
    u = rating[i][0]
    m = rating[i][1]
    R1[u][m] = b[u] + b[user + m] + aver
    if R1[u][m] < 1:
        R1[u][m] = 1
    if R1[u][m] > 5:
        R1[u][m] = 5
    Re[u][m] = R[u][m] - R1[u][m]

for i in range(movie - 1):
    for j in range(i + 1, movie):
        down1 = 0
        down2 = 0
        up = 0
        for k in range(user):
            if Re[k][i] != 6 and Re[k][j] != 6:
                up += Re[k][i] * Re[k][j]
                down1 += Re[k][i] * Re[k][i]
                down2 += Re[k][j] * Re[k][j]
        if not down1 * down2 == 0:
            d = up / (math.sqrt(down1) * math.sqrt(down2))
        else:
            d = 0
        if d > 0:
            k = 1
        else:
            k = -1
        D[i][j] = [abs(d), k, j]
        D[j][i] = [abs(d), k, i]

for i in range(movie):
    D[i][i] = [0, 1, i]
    D[i].sort()

for i in range(n2):
    u = testing[i][0]
    m = testing[i][1]
    up = 0
    down = 0
    R2[u][m] = b[u] + b[user + m] + aver
    for j in range(L):
        if Re[u][D[m][movie - j - 1][2]] != 6:
            up += D[m][movie - j - 1][0] * D[m][movie - j - 1][1] * Re[u][D[m][movie - j - 1][2]]
            down += D[m][movie - j - 1][0]
    if not down == 0:
        R2[u][m] += up / down
    if R2[u][m] < 1:
        R2[u][m] = 1
    if R2[u][m] > 5:
        R2[u][m] = 5

for i in range(n2):
    u = testing[i][0]
    m = testing[i][1]
    RMSE += (testing[i][2] - R2[u][m]) * (testing[i][2] - R2[u][m])

RMSE = math.sqrt(RMSE / n2)

print(f'user: {user}\nmovie: {movie}\n')
print("bi: [", end=" ")
for i in range(user):
    print(round(b[i][0], 3), end=" ")
print("]\nbu: [", end=" ")
for i in range(movie):
    print(round(b[user + i][0], 3), end=" ")
print("]\n")
print("Prediction:\n", R2, "\n")
print(f"RMSE: {round(RMSE, 4)}")
