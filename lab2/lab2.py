import math
import matplotlib.pyplot as plt
import numpy as np

# Входные данные
transmitter_power_BS_dBm = 46  #Мощность передатчика базовой станции BS
number_of_sectors_BS = 3  # Число секторов на одной BS
transmitter_power_AT_dBm = 24  # Мощность передатчика пользовательского терминала UE
antenna_gain_BS_dBi = 21  # Коэффициент усиления антенны BS в децибелах изотропного излучателя
wall_penetration_loss_dB = 15  # Запас мощности сигнала на проникновения сквозь стены 
IM_dB = 1  #Запас мощности на интерференцию (Interference Margin)
receiver_noise_coefficient_BS_dB = 2.4  # Коэффициент шума приемника BS
receiver_noise_coefficient_UE_dB = 6  # Коэффициент шума приемника пользователя 
required_SINR_DL_dB = 2  # Требуемое отношение сигнал-шум-интерференция (SINR) для downlink
required_SINR_UL_dB = 4  # Требуемое отношение SINR для uplink
antennas_per_BS = 2  # Число приемо-передающих антенн на BS (MIMO)
area_of_shopping_centers_sqm = 4  # Площадь торговых и бизнес центров (квадратные метры)
frequency_range_GHz = 1.8  # Диапазон частот
UL_bandwidth_MHz = 10 * 10**6 # Полоса частот в uplink (Мегагерцы)
DL_bandwidth_MHz = 20 * 10**6  # Полоса частот в downlink (Мегагерцы)

MIMO_Gain = 3 #выигрыш за счет использования MIMO, дБ
feederloss = 2 #Уровень потерь сигнала при прохождении через фидер дБ
d = np.arange(1,6000)

Thermal_N_DL = -174 + 10*np.log10(DL_bandwidth_MHz)
Thermal_N_UL = -174 + 10*np.log10(UL_bandwidth_MHz)
Rx_Sens_BS = Thermal_N_DL + required_SINR_DL_dB + receiver_noise_coefficient_BS_dB
Rx_Sens_AT = Thermal_N_UL + required_SINR_UL_dB + receiver_noise_coefficient_UE_dB 


MAPL_UL_dB = transmitter_power_AT_dBm - feederloss +  antenna_gain_BS_dBi + MIMO_Gain - wall_penetration_loss_dB - IM_dB - Rx_Sens_BS 

MAPL_DL_dB = transmitter_power_BS_dBm - feederloss + antenna_gain_BS_dBi + MIMO_Gain - wall_penetration_loss_dB - IM_dB - Rx_Sens_AT


def a(hms):
    a_hms = 3.2 * (np.log10(11.75*hms)) ** 2 - 4.97
    return a_hms

def s(d):
    hBS = 69
    if d>=1:
        s = 44.9 - 6.55 * np.log10(frequency_range_GHz*1000)
    else:
        s = (47.88 + 13.9 * np.log10(frequency_range_GHz*1000)-13.9*np.log10(hBS)) * 1/np.log10(50)
    
    return s



def UMiNLOS():
    d = np.arange(1,6000)
    pl_d=[]
    for i in range(len(d)):
        pl_d.append(26 * np.log10(frequency_range_GHz) + 22.7 + 36.7 * np.log10(d[i])) 

    return pl_d
def COST231():
    d = np.arange(1,6000)
    A = 46.3
    B = 33.9
    hBS = 65
    hms = 5
    Pl_d = []
        
    Lclutter = 3 # для DU
    #Lclutter = 0 # для U
    #Lclutter = -(2*(np.log10(frequency_range_GHz*1000/28))**2 + 5.4) # для SU
    #Lclutter = -(4.78 * np.log10(frequency_range_GHz*1000) ** 2 - 18.33 * np.log10(frequency_range_GHz*1000) + 40.94) # для RURAL
    #Lclutter = -(4.78 * np.log10(frequency_range_GHz*1000) ** 2 - 18.33 * np.log10(frequency_range_GHz*1000) + 35.94) # для ROAD
    for i in range(len(d)):
        Pl_d.append(A + B * np.log10(frequency_range_GHz*1000) - 13.82*np.log10(hBS) - a(hms) + s(d[i]/1000) * np.log10(d[i]/1000) + Lclutter)
    
    return Pl_d

def Walfish_Ikegami():
    d = np.arange(1,6000)
    L_los = []
    for i in range(len(d)):
        L_los.append(42.6 + 20*np.log10(frequency_range_GHz*1000) + 26*np.log10(d[i]/1000))
        
    return L_los

def loss_radiosignal():
    d = np.arange(1,6000)
    
    PLd_umi = 26 * np.log10(frequency_range_GHz) + 22.7 + 36.7 * np.log10(d)
    PLd_wal = 42.6 + 20 * np.log10(frequency_range_GHz*10**3) + 26*np.log10(d*10**-3)
    

    Lclutter = 3
    A = 46.3
    B = 33.9 
    hBS = 65
    hms = 5
    PLd_cost = []

    for i in range(len(d)):
        PLd_cost.append(A + B * np.log10(frequency_range_GHz*10**3) - 13.82 * np.log10(hBS) - a(hms) + s(d[i]/1000) * np.log10(d[i]/1000) + Lclutter)
    for i in range(1,len(d)-1):
        if PLd_cost[i-1] < MAPL_UL_dB and PLd_cost[i+1] > MAPL_UL_dB:
            R_c = i*10**-3
        if PLd_umi[i-1] < MAPL_UL_dB and PLd_umi[i+1]>MAPL_UL_dB:
            R_u = i*10**-3
        if PLd_wal[i-1] < MAPL_UL_dB and PLd_wal[i+1]>MAPL_UL_dB:
            R_w = i*10**-3
            
    return [R_c, R_u, R_w]

pl_d = UMiNLOS()
L_los = Walfish_Ikegami()
Pl_d = COST231()

#Walfish
PL_Walfish = []
for i in range(len(d)):
    PL_Walfish.append(42.6 + 20* math.log10(frequency_range_GHz*1000) + 26 * math.log10(d[i]/1000))
    
#walfish nlos
h = 30
fi = 58
hBuild = 30
hBS = 50
PL_Walfish_Nloss = []

for i in range(1,len(d)+1):    
    path_long=i
    L0=32.44+20*math.log10(1.9)+20*math.log10(i)    
    if ((fi <35)&(fi>0)):
        qoef=-10+0.354*fi    
    elif ((fi <55)&(fi>=35)):
        qoef=2.5 + 0.075 * fi    
    elif ((fi <90) & (fi>=55)):
        qoef=4.0 - 0.114 * fi
    L2=-16.9-10 * math.log10(20)+10*math.log10(1.9)+20*math.log10(hBuild-3)+qoef    
    if (hBS > hBuild):
        L1_1=-18 * math.log10(1+hBS-hBuild)        
        kD=18
    elif (hBS <= hBuild):        
        L1_1=0
        kD=18-15*((hBS-hBuild)/hBuild)    
    if ((hBS <= hBuild) & (path_long>500)):
        kA=54-0.8*(hBS-hBuild)
    elif ((hBS <= hBuild) & (path_long<=500)):        
        kA=54-0.8*(hBS-hBuild) * path_long/0.5
    elif (hBS>hBuild):        
        kA=54
        kF=-4+0.7*(1.9/925 - 1)    
        L1=L1_1+kA+kD*math.log10(path_long)+kF*math.log10(1.9)-9*math.log10(20)
    if(L1+L2>0):        
        Llnos=L0+L1+L2
    elif(L1+L2<=0):        
        Llnos=L0
    PL_Walfish_Nloss.append(Llnos)
    
    MAPL_DL_G = [MAPL_DL_dB] * len(d)
    MAPL_UL_G = [MAPL_UL_dB] * len(d)


    Wall_Cross_Nloss_UL = -1
for i in range(1,len(pl_d)-1):
        
    if PL_Walfish_Nloss[i-1] < MAPL_UL_dB and PL_Walfish_Nloss[i+1] >= MAPL_UL_dB:
       Wall_Cross_Nloss_UL = i
        
Wall_Cross_Nloss_DL = -1
for i in range(1,len(pl_d)-1):
    if PL_Walfish_Nloss[i-1] < MAPL_UL_dB and PL_Walfish_Nloss[i+1] >= MAPL_UL_dB:
       Wall_Cross_Nloss_DL = i




plt.figure(figsize=(10, 6))
plt.plot(d, pl_d, label='UMiNLOS', linestyle='-',color = 'gray')
plt.plot(d, Pl_d, label='COST231', linestyle='-', color = 'blue')
plt.plot(d, L_los, label='Walfish_Ikegami', linestyle='-', color = 'red')
plt.plot(d, PL_Walfish, label='Walfish', linestyle='-',color = 'y')
plt.axhline (y=MAPL_DL_dB, color='g', linestyle='--')
plt.axhline (y=MAPL_UL_dB, color='g', linestyle='--')
plt.plot(d,PL_Walfish_Nloss, label='Wallfish:Nloss',linestyle='dashed', color='m')
plt.xlabel('Расстояние между приемником и передатчиком (метры)')
plt.ylabel('Входные потери радиосигнала (дБ)')
plt.title('Зависимость входных потерь радиосигнала от расстояния')
plt.legend()
plt.grid(True)
plt.show()

Radius = loss_radiosignal()

print(f"Максимально допустимые потери сигнала (MAPL_UL): {MAPL_UL_dB} дБ")

print(f"Максимально допустимые потери сигнала (MAPL_DL): {MAPL_DL_dB} дБ")

S_cost = 1.95 * Radius[0]**2
S_UMi = 1.95 * Radius[1]**2
S_Wall = 1.95 * Radius[2]**2

print("Радиус Базовой станции для модели UMiNLOS = ",Radius[1], "км" )

print("Радиус Базовой станции для модели COST_231 = ",Radius[0], "км" )

print("Радиус Базовой станции для модели Wallfish = ",Radius[2], "км" )

print("Радиус Базовой станции для модели Wallfish_NLOSS = ",Wall_Cross_Nloss_UL, "м" )

print("Площадь одной базовой станции для модели UMiNLOS = ", S_UMi, "км кв" )

print("Площадь одной базовой станции для модели COST_231 = ", S_cost, "км кв" )

print("Площадь одной базовой станции для модели Wallfish = ", S_Wall, "км кв" )

S_usl_1 = 100 #100 кв.км
S_usl_2 = 4 #4 кв.км

count_sait_U= S_usl_2/S_UMi
count_sait_cost= S_usl_1/S_cost
print("Требуемое количество базовых станций (сайтов), необходимое для обеспечения непрерывного покрытия на этой территории (UMiNLOS) = ",math.ceil(count_sait_U) )

print("Требуемое количество базовых станций (сайтов), необходимое для обеспечения непрерывного покрытия на этой территории (COST_231) = ",math.ceil(count_sait_cost) )