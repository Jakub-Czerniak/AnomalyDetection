import datetime
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt

def calculate_mean_delta(dat, date,  num):
    iterator = num
    data_out = []
    date_out = []
    while iterator < len(dat):
        data_out.append(dat[iterator] - dat[iterator-num])
        date_out.append(date[iterator])
        iterator = iterator + num
    return data_out, date_out

#   Funkcja interpolujaca
# Przyjmuje tablice z wczytanymi danymi, tablice z wczytanymi datami
# dat - dane (nie przyrosty, tylko pomiary)
# date - daty
# Zwraca: tablice z interpolowanymi danymi i datami
def date_interpolation(dat, date):
    data_out = []
    date_out = []

    deltaT_15 = datetime.timedelta(minutes=15)
    deltaT_5 = datetime.timedelta(minutes=5)
    i = 1

    delta_cal = date[i] - date[i - 1]
    if deltaT_15 - deltaT_5 < delta_cal < deltaT_15 + deltaT_5:
        print()
    else:
        i = i + 1

    while i < len(dat):
        delta_cal = date[i] - date[i - 1]
        if deltaT_15 - deltaT_5 < delta_cal < deltaT_15 + deltaT_5:
            data_out.append(dat[i])
            date_out.append(date[i])
        else:
            if delta_cal < deltaT_5:    # jesli roznica jest mala pomija jeden pomiar
                data_out[len(data_out)-1] = dat[i]
                date_out[len(date_out)-1] = date[i]
            else:
                delta_cal = round(delta_cal / deltaT_15)
                tmp_date = date_out[len(date_out)-1]
                if delta_cal != 0:
                    tmp_increase = (dat[i] - dat[i-1])/delta_cal
                else:
                    tmp_increase = 0
                j = 0
                while j < delta_cal:
                    tmp_date = tmp_date + deltaT_15     # nastepny uzupelniony pomiar
                    data_out.append(dat[i-1] + j*tmp_increase)
                    date_out.append(tmp_date)
                    j = j + 1
        i = i + 1
    return data_out, date_out

file_name = './data/24713573.txt'
data = pd.read_csv(file_name, ';')  # wczytanie pliku
X = data.values[:, 1]  # wczytanie pomiarow

X_time = []
for t in data.values[:, 0]:
    X_time.append(dt.strptime(t, '%Y-%m-%d %H:%M:%S')) # wczytanie formatu czasu

X1, Y1 = date_interpolation(X, X_time)

X1, Y1 = calculate_mean_delta(X1, Y1, 1)


delta_usage = plt.figure(figsize=(10, 5))
# plt.plot_date(anomaliesX, anomaliesY, 'ro', markersize=5)  # wyswietlanie annomalii
plt.plot_date(Y1, X1, markersize=0.5, linestyle='solid')
plt.xlabel("date")
plt.ylabel("Δ water usage")
plt.tight_layout()

usage = plt.figure(figsize=(10, 5))
plt.plot_date(X_time, X, markersize=0.5, linestyle='solid')
plt.xlabel("date")
plt.ylabel("water usage")
plt.tight_layout()
plt.show()

