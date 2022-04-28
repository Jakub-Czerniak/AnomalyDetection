import pandas as pd
from statsmodels.tsa.seasonal import STL
import matplotlib.pyplot as plt
from datetime import datetime

test_data = pd.read_csv('data.txt', ';')  # wczytywanie danych
arr = test_data.values  # zamiana wczytanego obiektu na tablice bo inaczej nie dzialalo xD
i = 0

while i < arr.size/2:
    arr[i][0] = i  # zamiast dat i godzin sa cyfry od 0 do liczby danych, tu do ogarniecia ten czas jeszcze
    i += 1
plt.plot(arr[:, 0], arr[:, 1])
plt.show()
