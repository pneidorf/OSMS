import math
from random import random
import numpy as np
import matplotlib.pyplot as plt

POLYNOMIAL = [1,1,0,1,1,1,1,0]  # порождающий полином
LENGTH = 5  # Последовательность Голда[длина массива]
L = 50  # длинна битов для имени и фамилии
M = len(POLYNOMIAL)-1  # длинна бит для последовательности с CRC
G = 31  # длинна бит для последовательности голда (2**5-1)
N = 6  # samples
RANDOM = N * (L + M + G)


# Функция для кодирования ASCII-символов в битовую последовательность
def encode_to_binary(input_str):
    binary_data = ''
    for char in input_str:
        ascii_code = ord(char)
        binary_data += format(ascii_code, '08b')
    return binary_data


# Функция для подсчета CRC
def calculate_crc(data, polynomial):
    data_length = len(data)
    polynomial_length = len(polynomial)

    extended_data = list(data + '0' * (polynomial_length - 1))

    for i in range(data_length):
        if extended_data[i] == '1':
            for j in range(polynomial_length):
                extended_data[i + j] = str(int(extended_data[i + j]) ^ int(polynomial[j]))

    result = ''.join(extended_data[data_length:])
    return result


# сдвиг по х
def shift_register_x(register_state_x):
    feedback = (register_state_x[2] + register_state_x[3]) % 2
    for i in range(LENGTH - 1, 0, -1):
        register_state_x[i] = register_state_x[i - 1]
    register_state_x[0] = feedback


# сдвиг по у
def shift_register_y(register_state_y):
    feedback = (register_state_y[1] + register_state_y[2]) % 2
    for i in range(LENGTH - 1, 0, -1):
        register_state_y[i] = register_state_y[i - 1]
    register_state_y[0] = feedback


# расчет последовательности голда
def Gold_sequence(register_state_x, register_state_y, length):
    result = ""
    print("Последовательность Голда равняется: ", end="")
    for _ in range(length):
        bit = (register_state_x[4] + register_state_y[4]) % 2
        print(bit, end="")

        shift_register_x(register_state_x)
        shift_register_y(register_state_y)

        result += str(bit)

    print("\n\n")
    return result

'''
def correlation(data, seq, step):
    sum_c = 0
    length = len(seq)
    for i in range(length):
        sum_c += data[i + step] * seq[i]

    return sum_c
'''

# поиск максимальной корреляции
def calculate_correlation(sequence1, sequence2, offset):
    correlation = 0.0
    length = len(sequence1)
    length2 = len(sequence2)

    if length == 0 or length2 == 0:
        return 0.0

    for i in range(length):
        correlation += int(sequence1[i]) * int(sequence2[(i + offset) % length2])

    return correlation / length


# функция для уменьшения массива на N
def decrease_sequence(input_str, length):
    return input_str[::length]

# функция для поиска аналогичных последовательностей в массиве и удаления ее
def remove_analog(input_data, find_seq):
    input_length = len(input_data)
    find_seq_length = len(find_seq)
    output_data = ""

    i = 0
    while i < input_length:
        # Сравниваем подстроку с шаблоном
        if input_data[i:i+find_seq_length] != find_seq:
            # Если не совпадает, копируем в выходной массив
            output_data += input_data[i:i+find_seq_length]
            i += find_seq_length
        else:
            i += find_seq_length

    return output_data


# функция преобразования битовой последовательности в ASCII-символы
def binary_to_ascii(binary_data, name_bit):
    ascii_result = ""
    for i in range(0, name_bit, 8):
        byte = binary_data[i:i+8]
        
        # Проверка на пустую строку
        if byte:
            byte_value = int(byte, 2)
            ascii_result += chr(byte_value)
        else:
            print("Ошибка: Некорректная длина байта.")

    return ascii_result


# функция для генерации шума по формуле
def generate_normal_noise(noise, length, mean, sigma):
    for i in range(length):
        # Генерация нормально распределенного шума
        u1 = random()
        u2 = random()
        z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)

        # Применение среднего и стандартного отклонения
        noisy_value = mean + sigma * z

        # Избегаем выхода за границы строки
        if i < len(noise):
            noise[i] = noisy_value
        else:
            break
    return noise


register_state_x = [0, 1, 1, 0, 0]  # данные которые подаются на х для расчета голда
register_state_y = [1, 0, 0, 1, 1]  # данные которые подаются на у для расчета голда

'''
register_state_x2 = [0, 1, 1, 0]  # данные которые подаются на х для расчета голда
register_state_y2 = [1, 0, 0, 1]
LENGTH = 4
'''

cons = pow(2, LENGTH) - 1
sync_start_sample = 0

first_name = input("Введите ваше имя: ")
last_name = input("Введите вашу фамилию: ")

binary_data = encode_to_binary(first_name) + encode_to_binary(last_name)
name_bit = len(first_name) * 8
print("Битовая последовательность:", binary_data, "\n")
binary_array = np.array([int(bit) for bit in binary_data])

random_sequence = Gold_sequence(register_state_x, register_state_y, cons)
result_fourth = random_sequence + binary_data
crc_result = calculate_crc(binary_data, POLYNOMIAL)
print("CRC:", crc_result, "\n")

result_fourth += crc_result
print("Битовая последовательность с последовательностью голда:", result_fourth, "\n")
binary_fourth = np.array([int(bit) for bit in result_fourth])


#t = np.arange(float(len(result_fourth)))

t = np.arange(0,len(binary_array))
plt.figure(figsize=(13, 20))
plt.subplot(4, 1, 1)

plt.plot(t, binary_array)
plt.xlabel('элемент массива')
plt.ylabel('значение')
plt.title("data")

t = np.arange(0,len(binary_fourth))
plt.figure(2,figsize=(13, 20))
plt.subplot(4, 1, 1)

plt.plot(t, binary_fourth)
plt.xlabel('элемент массива')
plt.ylabel('значение')
plt.title("Gold + data + crc")



samples = []
for i in range(len(result_fourth)):
    result_fifth=result_fourth[i]*N
    samples += result_fifth
#result_fifth = result_fourth * N
print("Samples:", samples)

t = np.arange(0,len(samples))
plt.figure(3,figsize=(13, 20))
plt.subplot(4, 1, 1)

plt.plot(t, samples)
plt.xlabel('элемент массива')
plt.ylabel('значение')
plt.title("Samples")

element = int(input("Введите число от 0 до {}: ".format(RANDOM)))
if element < 0 or element >= RANDOM:
    print("Введенное число не входит в заданный диапазон")
        
#6 пункт
result_sixth = [0] * element
for i in range (len(samples)):
    result_six = result_sixth + samples
check = RANDOM*2 - len(result_six)
check2 = [0] * check
final_result = result_six + check2
#print("Начало от :", final_result) ####################

t = np.arange(0,len(final_result))
plt.figure(5,figsize=(13, 20))
plt.subplot(4, 1, 1)

plt.plot(t, final_result)
plt.xlabel('элемент массива')
plt.ylabel('значение')
plt.title("Vstavka")

#7 пункт
mean = 0.0
sigma = 0.1
#noise = generate_normal_noise([0.0] * (RANDOM * 2), RANDOM * 2, mean, sigma)
noise = np.random.normal(0,sigma,(RANDOM*2))
result_seventh = ""
noisy_value = [0] * (2*RANDOM)
for i in range(2*RANDOM):
    noisy_value[i] = float(final_result[i]) + float(noise[i])
    #print(noisy_value)
    if noisy_value[i] < 0:
        noisy_value[i] = 0
    elif noisy_value[i] > 0.5:
        noisy_value[i] = 1
    result_seventh += str(int(noisy_value[i]))
 
#print(noisy_value)
#print(result_seventh) ################################

t4 = np.arange(0, len(noisy_value))
plt.figure(6,figsize=(13, 20))
plt.subplot(4, 1, 1)
plt.plot(t4, noisy_value)
plt.xlabel('элемент массива')
plt.ylabel('значение')
plt.title("Noise") 

# 8 пункт

random_seq = [RANDOM]
res_rnd = 0
index_rnd = 0

while index_rnd < len(random_sequence):
    for i in range(N):
        # Проверка, что индекс не превышает длину списка random_seq
        if res_rnd < len(random_seq):
            random_seq[res_rnd] = random_sequence[index_rnd]
            res_rnd += 1
        else:
            # Если random_seq заполнен, выход из цикла
            break
    index_rnd += 1

'''
for i in range(len(random_sequence)):
    result_fifth=random_sequence[i]*N
    random_seq += result_fifth

'''

max_Corr = -1.0
sync_start_sample = 0
for offset in range(2*RANDOM):   
    correlation_val=calculate_correlation(random_seq, result_seventh, offset)
    if (correlation_val > max_Corr):
        max_Corr = correlation_val
        sync_start_sample = offset
        
print("Начальный семпл синхросигнала:", sync_start_sample)

'''
data_Corr = []
max_Corr = -1.0
sync_start_sample = 0
binary_seven = np.array([int(bit) for bit in result_seventh])
binary_seq = np.array([int(bit) for bit in random_seq]) 

for offset in range(2*RANDOM):   
    if offset >= len(binary_seven) - len(binary_seq):
        break
    #correlation_val = []
    correlation_val=correlation(binary_seven,binary_seq,offset)
    data_Corr.append(correlation_val)
    if (correlation_val > max_Corr):
        max_Corr = correlation_val
        sync_start_sample = offset
    
        
t4 = np.arange(0, len(data_Corr))
plt.figure(7, figsize=(20, 10))
plt.suptitle("Синхро сигнал в начале")
plt.subplot(2, 1, 1)
plt.title("Корреляция")
plt.plot(t4, data_Corr)
'''
eight_mass = result_seventh[sync_start_sample:]
#result_seventh = result_seventh[:sync_start_sample]
#print("Удаление шума:",eight_mass) ###############################################

length_five = len(samples)
nine_mass = eight_mass[:length_five]
#print("Без нулей:", nine_mass) #########################

# 9 пункт
result_ninth = decrease_sequence(nine_mass, N)
#print("Удаление отсчетов:",result_ninth) ########################


# 10 пункт
result_tenth = remove_analog(result_ninth, random_sequence)
print("Результат данных после удаления последовательности голда:", result_tenth)

crc_result2 = calculate_crc(result_tenth, POLYNOMIAL)
print()
print("CRC (зануленные):", crc_result2, "\n")


del_len = len(binary_data)
delete_crc = result_tenth[:del_len]

#delete_crc = remove_analog(result_tenth, crc_result)
print("После удаления CRC", delete_crc)
# 12 пункт
ascii_result_name = binary_to_ascii(delete_crc, name_bit)

# Вывод расшифровки только первых name_bit бит
print()
print("Расшифрованное имя:", ascii_result_name)

all_bit = len(delete_crc)
lastname_bit = all_bit - name_bit

name_ascii_result_rest = binary_to_ascii(delete_crc[name_bit:], lastname_bit)

# Вывод оставшейся части в ASCII
print("Расшифрованная фамилия:", name_ascii_result_rest)

#13 пункт
samples_4N = []
for i in range(len(result_fourth)):
    result_fifth=result_fourth[i]*4
    samples_4N += result_fifth
#result_fifth = result_fourth * N

samples_8N = []
for i in range(len(result_fourth)):
    result_fifth=result_fourth[i]*8
    samples_8N += result_fifth

# Повторить каждый элемент из result_fourth 16 раз
#samples_16N = result_fourth * 16
samples_16N = []
for i in range(len(result_fourth)):
    result_fifth=result_fourth[i]*16
    samples_16N += result_fifth

noisy_value_4N = [float(0)] * (2 * 4 * (L + M + G))
noisy_value_8N = [float(0)] * (2 * 8 * (L + M + G))
noisy_value_16N = [float(0)] * (2 * 16 * (L + M + G))

for i in range(0, len(samples_4N)):
    noisy_value_4N[i]=samples_4N[i]
for i in range(0, len(samples_8N)):
    noisy_value_8N[i]=samples_8N[i]
for i in range(0, len(samples_16N)):
    noisy_value_16N[i]=samples_16N[i]
    
spect_signal_4N = np.fft.fft(noisy_value_4N) 
spect_signal_8N = np.fft.fft(noisy_value_8N) 
spect_signal_16N = np.fft.fft(noisy_value_16N)

noise = np.random.normal(0, sigma, len(noisy_value_4N))
for i in range(len(noisy_value_4N)):
    noisy_value_4N[i] = float(noisy_value_4N[i]) + noise[i]
    
noise = np.random.normal(0, sigma, len(noisy_value_8N))
for i in range(len(noisy_value_8N)):
    noisy_value_8N[i] = float(noisy_value_8N[i]) + noise[i]

noise = np.random.normal(0, sigma, len(noisy_value_16N))
for i in range(len(noisy_value_16N)):
    noisy_value_16N[i] = float(noisy_value_16N[i]) + noise[i]
    
spect_noise_signal_4N = np.fft.fft(noisy_value_4N)
spect_noise_signal_8N = np.fft.fft(noisy_value_8N)
spect_noise_signal_16N = np.fft.fft(noisy_value_16N)

shift_spect4 = np.fft.fftshift(spect_noise_signal_4N)
shift_spect8 = np.fft.fftshift(spect_noise_signal_8N)
shift_spect16 = np.fft.fftshift(spect_noise_signal_16N)

t2 = np.arange(0,len(spect_noise_signal_4N))
t3 = np.arange(0,len(spect_noise_signal_8N))
t4 = np.arange(0,len(spect_noise_signal_16N))

plt.figure(4,figsize=(13, 20))   
plt.subplot(4, 1, 1)
plt.plot(t4, spect_signal_16N, color='blue')
plt.plot(t3, spect_signal_8N, color='brown')
plt.plot(t2, spect_signal_4N, color='green')
plt.xlabel('элемент массива')
plt.ylabel('амплитуда')
plt.title("Спектр передаваемого сигнала с N=4, N=8, N=16")

plt.subplot(4, 1, 2)
plt.plot(t4, shift_spect16, color='blue')
plt.plot(t3, shift_spect8, color='brown')
plt.plot(t2, shift_spect4, color='green')



plt.xlabel('элемент массива')
plt.ylabel('амплитуда')
plt.title("Спектр принимаемого сигнала с шумом и N=4, N=8, N=16")