import serial
import time
import matplotlib.pyplot as plt
from numpy import savetxt
from timeit import default_timer as timer

ssp = 100
string = []

ser = serial.Serial('COM3', 115200, timeout=1)
i = 0
start = timer()
print("Inicio")
while(i/ssp < 2):
    line = ser.readline()
    i = i + 1; 
    string.append(line.decode())
    print(i/ssp)   
ser.close()

end = timer()
print("tiempo: ", end - start)



IR = []


for element in string:
    values = element.split(", ")
    IR.append(float(values[0]))
    print(i / ssp)
    
plt.figure()
plt.plot(IR, 'r')
plt.grid()
plt.show()

savetxt("C:/Users/fercy/OneDrive/Escritorio/HeartBeatCam/spo2.csv", IR, delimiter=',')