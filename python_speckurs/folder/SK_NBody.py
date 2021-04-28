# -*- coding: utf-8 -*-
# импортируем необходимые пакеты и  функции
import random
from mpi4py import MPI
import numpy as np

# гравитационная постоянная м^3 кг^-1 с^-2
G = 6.67408E-11 
# размер области 2L x 2L x 2L
L = 1E6
# радиус частиц
R = 5E3
# плотность
rho = 2.5E3

# функция для измерения времени выполнения
def How_Long(func, args):
    """
    Функция для измерения времени выполнения
    func - имя функции, для которой проводится измерение времени выполнения
    args - [x, y, ... , z] список аргументов функции func
    Результат работы 4 значения: часы, минуты, секунды, общее время в секундах
    """
    start = MPI.Wtime()
    func(*args)
    
    stop = MPI.Wtime()
        
    hrs = (stop - start)//(60*60)
    mns = ((stop - start) - hrs*60*60)//60
    scs = ((stop - start) - hrs*60*60 - mns*60)
    print (" {} hour {} min {} sec\n".format(hrs,mns,scs))
    
    return hrs, mns, scs, stop - start
    
# Функция создания начального состояния: LIST
def init_cond_lists(NP,crds,rds,mss,vls):
    """
    Функция создания начального состояния системы частиц
    NP   - число частиц
    crds - список координат частиц 
    rds  - список радиусов частиц
    mss  - список масс частиц
    vls  - список скоростей чпстиц
    Результат работы: списки координат, радиусов, масс и скоростей заданного числа чсатиц
    """
    for i in range(NP):
        crds.append([L - 2*L*np.random.random(),L - 2*L*np.random.random(),L - 2*L*np.random.random()])
        #crds.append([random.triangular(-L,L),random.triangular(-L,L),random.triangular(-L,L)])
        rds.append(random.randint(100,R))
        mss.append(rho*(4.0/3.0)*np.pi*rds[-1]**3)
        vls.append([0,0,0])
        
#Функция, выполняющая заданное количество шагов моделирования для задачи N-тел        
def nbody_list(NP, NT, dt, crds, vls, mss):  
    """
    Функция, выполняющая NT шагов моделирования для задачи динамики NP частиц,
    реализованная с использованием структуры данных: LIST
    NP   - число частиц
    NT   - число шагов по времени
    dt   - величинв шага по времени
    crds - координаты частиц
    vls  - скорости частиц
    mss  - массы частиц
    Результат работы: списки координат и скоростей частиц, на момент окончания моделирования
    """
    for step in range(1, NTSteps + 1, 1):
        #print "Step {}".format(step)
        for i in range(NP):
            Ax = 0.0; Ay = 0.0; Az = 0.0
            for j in range(NP):
                if j != i:
                    dx = crds[j][0] - crds[i][0]
                    dy = crds[j][1] - crds[i][1]
                    dz = crds[j][2] - crds[i][2]
                    dr2 = dx * dx + dy * dy + dz * dz
                    dr3 = dr2 * np.sqrt(dr2)
                    Ax = Ax + mss[j] * dx / dr3
                    Ay = Ay + mss[j] * dy / dr3
                    Az = Az + mss[j] * dz / dr3
                vls[i][0] = vls[i][0] + dt * G * Ax
                vls[i][1] = vls[i][1] + dt * G * Ay
                vls[i][2] = vls[i][2] + dt * G * Az
        for k in range(NP):
            crds[k][0] = crds[k][0] + vls[k][0] * dt
            crds[k][1] = crds[k][1] + vls[k][1] * dt
            crds[k][2] = crds[k][2] + vls[k][2] * dt
            
            
            
# РЕАЛИЗАЦИЯ АЛГОРИТМОВ МОДЕЛИРОВАНИЯ ЗАДАЧИ N-ТЕЛ С ИСПОЛЬЗОВАНИЕМ ПАКЕТА NumPy

# Генерация начального состояния системы частиц
def initial_cond_numpy(N, D):
    """
    Функция создания начального состояния системы частиц средствами пакета NumPy
    N - число частиц
    D - размерность пространства
    Результат работы: NumPy-массивы координат, скоростей, масс и радиусов заданного числа частиц    
    """
    x0 = np.random.uniform(-L, L, (N, D))
    v0 = np.zeros((N, D), dtype=float)
    r0 = np.random.uniform(100, R, (N))
    m = rho*(4.0/3.0)*np.pi*r0**3 #np.ones(N, dtype=float)
    return x0, v0, m, r0    

# Определение ускорения i-й частицы
def a(i, x, G, m):
    """
    Функция вычисления ускорения частицы
    i - номер частицы
    x - массив координат частиц
    G - гравитационная постоянная
    m - массив масс частиц
    Результат работы: ускорение i-й частицы
    """
    x_i = x[i]
    x_j = np.delete(x, i,axis=0)
    m_j = np.delete(m, i,axis=0)
    diff = x_j - x_i
    mag3 = np.sum(diff**2, axis=1)**1.5
    result = G * np.sum(diff * (m_j / mag3)[:,np.newaxis], axis=0)
    return result

# Вычисление новых положений и скоростей чистиц
def timestep(x0, v0, G, m, dt):
    """
    Функция вычисления положений и скоростей частиц по уже известным и шагу по времени
    x0 - массив координат частиц
    v0 - массив скоростей частиц
    G  - гравитационная постоянная
    m  - массив масс частиц
    dt   - величинв шага по времени
    Результат работы: NumPy-массивы координат, скоростей заданного числа чсатиц 
    """
    N = len(x0)
    x1 = np.empty(x0.shape, dtype=float)
    v1 = np.empty(v0.shape, dtype=float)
    for i in range(N):
        a_i0 = a(i, x0, G, m)
        v1[i] = a_i0 * dt + v0[i]
        x1[i] = a_i0 * dt**2 + v0[i] * dt + x0[i]
    return x1, v1

# Функция, выполняющая заданное количество шагов моделирования для задачи N-тел 
def nbody_numpy(NT, dt, crds, vls, mss):  
    """
    Функция, выполняющая NT шагов моделирования для задачи динамики частиц,
    реализованная с использованием структуры данных: NDARRAY
    NT   - число шагов по времени
    dt   - величинв шага по времени
    crds - координаты частиц
    vls  - скорости частиц
    mss  - массы частиц
    Результат работы: списки координат и скоростей частиц, на момент окончания моделирования
    """
    for step in range(1, NT + 1, 1):
        x, v = timestep(crds, vls, G, mss, dt)
        crds, vls = x, v
