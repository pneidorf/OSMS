#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define DATA_SIZE 250  // Количество бит в данных
#define POLYNOMIAL "11011110"  // Порождающий полином

// Функция генерации рандомных данных
void Random_Data(char *data, int data_size) {
    srand(time(NULL));  // Инициализация генератора случайных чисел

    for (int i = 0; i < data_size; i++) {
        data[i] = rand() % 2 + '0';  // Генерация случайного бита (0 или 1)
    }
    data[data_size] = '\0';  // Добавляем символ конца строки
}

// Функция для вычисления CRC
void calculateCRC(const char *data, const char *polynomial, char *result) {
    int data_length = strlen(data);
    int polynomial_length = strlen(polynomial);

    // Выделяем память под расширенные данные (данные + (polynomial_length - 1) нулей)
    char extended_Data[data_length + polynomial_length - 1];
    strcpy(extended_Data, data);
    strcat(extended_Data, "0000000");  // Добавляем нули в конец расширенных данных

    for (int i = 0; i < data_length; i++) {
        if (extended_Data[i] == '1') {
            for (int j = 0; j < polynomial_length; j++) {
                extended_Data[i + j] ^= polynomial[j] - '0';  // Выполняем XOR с соответствующим битом полинома
            }
        }
    }

    // Получаем CRC, который представляет собой последние data_length бит расширенных данных
    strncpy(result, extended_Data + data_length, data_length);
    result[data_length] = '\0';
}

int main() {
    char data[DATA_SIZE + 1];  // Данные
    char crc_Result[DATA_SIZE + 1];  // Результат CRC
    char extnd_CRC_Result[DATA_SIZE + 1];  // Расширенный CRC

    Random_Data(data, DATA_SIZE);

    printf("Generated data: %s\n", data);

    calculateCRC(data, POLYNOMIAL, crc_Result);

    printf("Calculated CRC value: %s\n", crc_Result);

    int detected_Errors = 0;
    int undetected_Errors = 0;

    for (int change_bit = 0; change_bit < DATA_SIZE + strlen(crc_Result); change_bit++) {
        char failed_data[DATA_SIZE + 1];
        strcpy(failed_data, data);

        if (change_bit < DATA_SIZE) {
            // Искажаем бит в данных
           if (failed_data[change_bit] == '0') {
            failed_data[change_bit] = '1';
            } else {
                failed_data[change_bit] = '0';
            }
        } else {
            
        }

        //calculateExtendedCRC(failed_data, POLYNOMIAL, extnd_CRC_Result);
        calculateCRC(failed_data, POLYNOMIAL, crc_Result);

        int errors = 0;
        for (int i = 0; i < strlen(crc_Result); i++) {
            if (crc_Result[i] != '0') {
                errors = 1;
                break;
            }
        }

        if (errors) {
            detected_Errors++;
        } else {
            undetected_Errors++;
        }
    }

    printf("Errors found: %d\n", detected_Errors);
    printf("NO errors found: %d\n", undetected_Errors);

    return 0;
}
