import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.io.wavfile import write
from scipy import signal

def myConv(valueX,valueY,x,y):
    arr = []
    if x == y:
        for i in range(1,y+1):
            arr.append(i)
        arr = arr + arr[::-1]
        arr.pop((len(arr)//2))
    else:
        if x<y:
            for i in range(1,x+1):
                arr.append(i)
        elif x>y:
            for i in range(1,y+1):
                arr.append(i)
        arr2 = arr[::-1]
        for i in range(0,abs((y-x))):
            arr.append(arr[-1])
        arr = arr + arr2
        arr.pop((len(arr)//2)) 
    valueConv = [0] * len(arr)
    indis = 0
    for i in range(0,len(arr)):
        if i >= x :
            indis+=1
        else:
            indis = 0
        for j in range(0,arr[i]):
            valueConv[i] += valueY[abs(indis+(j))] * valueX[i-indis-j]
    valueConv.insert(0,0)
    valueConv.insert(0,0)
    valueConv.append(0)
    valueConv.append(0)
    return valueConv
menu = int(input("""1 - Convolution Functions
2 - Convolution On Voice
Make Your Choice:"""))
if(menu == 1):
    x = int(input("x dizisinin uzunluğunu giriniz :"))
    y = int(input("y dizisinin uzunluğunu giriniz :"))
    valueX = []
    indexX = []
    valueY = []
    indexY = []
    xZero = -100
    yZero = -100
    for i in range(0,x):
        valueX.append(float(input("x dizisinin {}. değerini giriniz :".format(i+1)))) 
    for i in range(0,x):
        a = int(input("x dizisinin {}. indisini giriniz :".format(i+1)))
        indexX.append(a)
        if a == 0:
            xZero = i+1
    if(xZero == -100):
        while True:
            xZero = int(input("x dizisinin sıfır noktasını giriniz: "))
            if(xZero in indexX):
                break
    for i in range(0,y):
        valueY.append(float(input("y dizisinin {}. değerini giriniz :".format(i+1))))
    for i in range(0,y):
        a = int(input("y dizisinin {}. indisini giriniz :".format(i+1)))
        indexY.append(a)
        if a == 0:
            yZero = i+1
    if(yZero == -100):
        while True:
            yZero = int(input("y dizisinin sıfır noktasını giriniz: "))
            if(yZero in indexY):
                break
    convIndex=[]
    for i in range(0,(x+y-1)+4):
        convIndex.append(indexX[0]+i-2)
    valueConv = myConv(valueX,valueY,x,y)
    print("\n\n")
    print("x[n] : "+str(valueX)+ '\n')
    print("y[m] : "+str(valueY)+ '\n')
    print("MyConv() Convolution Vector : " + str(valueConv) + '\n')
    pyConvValue = signal.convolve(valueX, valueY, mode='full')    #HAZIR FONKSİYON
    print("Conv() Convolution Vector: " + str(pyConvValue) + '\n')
    
#   MyConv Grafiği Yazma
    son = (convIndex[-1])+1
    bas = convIndex[0]
    n = np.arange(bas, son, 1)
    d = valueConv
    plt.stem(n, d)
    plt.xlabel('n')
    plt.xticks(np.arange(bas, son, 1))
    plt.yticks(np.arange(min(valueConv),max(valueConv)+1,1))
    plt.ylabel('x[n] * y[n]')
    plt.title('myConv() Convolution Func')
    plt.savefig("MyConv_Convolution.png")
#   MyConv Grafiği Yazma
    plt.clf()
#   Hazır Conv Grafiği Yazma
    son = (convIndex[-1])-1
    bas = convIndex[0]+2
    n = np.arange(bas, son, 1)
    d = pyConvValue
    plt.stem(n, d)
    plt.xlabel('n')
    plt.xticks(np.arange(bas, son, 1))
    plt.yticks(np.arange(min(pyConvValue),max(pyConvValue)+1,1))
    plt.ylabel('x[n] * y[n]')
    plt.title('Conv() Convolution Func')
    plt.savefig("Conv_Convolution.png")
#   Hazır Conv Grafiği Yazma
    plt.clf()
#   x[n] Grafiği Yazma
    son = (indexX[-1])+1
    bas = indexX[0]
    n = np.arange(bas, son, 1)
    d = valueX
    plt.stem(n, d)
    plt.xlabel('n')
    plt.xticks(np.arange(bas, son, 1))
    plt.yticks(np.arange(min(valueX),max(valueX)+1,1))
    plt.ylabel('x[n]')
    plt.title('x[n] Grafiği')
    plt.savefig("xn.png")
#   x[n] Grafiği Yazma
    plt.clf()
#   y[n] Grafiği Yazma
    son = (indexY[-1])+1
    bas = indexY[0]
    n = np.arange(bas, son, 1)
    d = valueY
    plt.stem(n, d)
    plt.xlabel('m')
    plt.xticks(np.arange(bas, son, 1))
    plt.yticks(np.arange(min(valueY),max(valueY)+1,1))
    plt.ylabel('y[m]')
    plt.title('y[m] Grafiği')
    plt.savefig("ym.png")
#   y[n] Grafiği Yazma
elif(menu == 2):
    freq = 44100
#   Ses Kaydı Başlangıcı
    duration = int(input("5 Saniyelik mi 10 Saniyelik mi Ses Kaydetmek İstiyorsunuz ? : "))
    print("{} Saniyelik Ses Kaydı Başladı...".format(duration))
    recording = sd.rec(int(duration * freq),samplerate=freq, channels=2)
    sd.wait(),
    write('original_audio.wav',freq,recording)
    recordingOneD = []
    for i in range(0,(int(duration/5)*220500)):
        recordingOneD.append(recording[i][1])
    recordingOneD = np.array(recordingOneD)
#   Ses Kaydı Bitişi

#   h[n] Dizisini Oluşturma Başlangıcı
    M = int(input("M Değerini Giriniz ( 2/3/4 ) :"))
    h = []
    zeroArr = []
    valueArr = []
    for i in range(0,400):
        zeroArr.append(0)
    h.append(1)
    for i in range(1,5):
        valueArr.append((0.4)*i)
    for i in range(0,M):
        h.extend(zeroArr)
        if i == 2:
            h.append(1.2)
        else:
            h.append(valueArr[i])
    h = np.array(h)
#   h[n] Dizisini Oluşturma Bitişi

#   Hazır Konvolüsyon Fonksiyonu İle İşlem Yapma Başlangıcı
    pyConvValue = signal.convolve(recordingOneD, h, mode='full')  #HAZIR FONKSİYON
    print(pyConvValue)    
    pyConvValue = np.array(pyConvValue)
    pyConvValue = np.float32(pyConvValue)
    print("Hazır Konvolüsyon Fonksiyonunun Çıktısı Seslendiriliyor...")
    sd.play(pyConvValue, blocking=True)
#   Hazır Konvolüsyon Fonksiyonu İle İşlem Yapma Bitişi

#   Kendi Yazdığım Konvolüsyon İle İşlem Yapma Başlangıcı
    print("Kendi Yazdığım Konvolüsyon Fonksiyonunun Çıktısı Hazırlanıyor")
    myConvValue = myConv(recordingOneD,h,len(recording),len(h))
    myConvValue = np.array(myConvValue)
    myConvValue = np.float32(myConvValue)
    print("Kendi Yazdığım Konvolüsyon Fonksiyonunun Çıktısı Seslendiriliyor...")
    sd.play(myConvValue, blocking=True)
#   Kendi Yazdığım Konvolüsyonun Çıktısını Kaydediyorum
    write('MyConv.wav',freq,pyConvValue)
#   Hazır Konvolüsyonun Çıktısını Kaydediyorum
    write('HazırConv.wav',freq,pyConvValue)
else:
    pass