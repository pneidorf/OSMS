#include <stdio.h>
#include <math.h>

#define SIZE 5

// Функция для сдвига элементов регистра register_x вправо
void shift_x(int *register_x) {
    int res_x = (register_x[2] + register_x[3]) % 2; // Операция XOR для конкретных элементов
    for (int i = SIZE - 1; i > 0; i--) {
        register_x[i] = register_x[i - 1]; // Сдвиг элементов вправо
    }
    register_x[0] = res_x; // Обновление первого элемента
}

// Функция для сдвига элементов регистра register_y вправо
void shift_y(int *register_y) {
    int res_y = (register_y[1] + register_y[2]) % 2; // Операция XOR для конкретных элементов
    for (int i = SIZE - 1; i > 0; i--) {
        register_y[i] = register_y[i - 1]; // Сдвиг элементов вправо
    }
    register_y[0] = res_y; // Обновление первого элемента
}

// Функция для генерации последовательности Голда
void Gold_sequence(int *sequence, int *register_x, int *register_y, int length) {
    printf("\nGold's sequence equals:  ");
    for (int i = 0; i < length; i++) {
        sequence[i] = (register_x[4] + register_y[4]) % 2; // Операция XOR для конкретных элементов
        printf("%d", sequence[i]); // Вывод сгенерированной последовательности
        shift_x(register_x); // Сдвиг регистра register_x
        shift_y(register_y); // Сдвиг регистра register_y
    }
    printf("\n\n");
}

// Функция для выполнения циклического сдвига последовательности
void cyclic_shift(int *sequence, int size) {
    int res = sequence[size - 1];
    for (int i = size - 1; i > 0; i--) {
        sequence[i] = sequence[i - 1]; // Сдвиг элементов вправо
    }
    sequence[0] = res; // Обновление первого элемента
}

// Функция для вычисления автокорреляции между двумя последовательностями
double autocorrelation(int *sequence1, int *sequence2, int length) {
    int res = 0;
    for (int i = 0; i < length; i++) {
        if (sequence1[i] == sequence2[i]) {
            res += 1; // Инкремент, если элементы равны
        } else {
            res += -1; // Декремент, если элементы не равны
        }
    }
    return res;
}

// Функция для вычисления кросс-корреляции между двумя последовательностями
double crosscorrelation(int *sequence1, int *sequence2, int length) {
    double res = 0;
    for (int i = 0; i < length; i++) {
        res += sequence1[i] * sequence2[i]; // Умножение соответствующих элементов и накопление
    }
    return res;
}

// Функция для вычисления нормализованной корреляции между двумя последовательностями
double normalized_correlation(int *sequence1, int *sequence2, int length) {
    double unnormalized_corr = crosscorrelation(sequence1, sequence2, length);
    double sum_a = 0.0;
    double sum_b = 0.0;

    for (int n = 0; n < length; ++n) {
        sum_a += sequence1[n] * sequence1[n]; // Накопление квадратов элементов в sequence1
        sum_b += sequence2[n] * sequence2[n]; // Накопление квадратов элементов в sequence2
    }

    double normalization_factor = sqrt(sum_a) * sqrt(sum_b);
    double normalized_corr = unnormalized_corr / normalization_factor;
    return normalized_corr;
}

int main() {
    // Определение длины последовательности
    int length_seq = pow(2, SIZE) - 1;
    int random_sequence[length_seq];
    int modified_sequence[length_seq];
    
    // Инициализация регистров для первой последовательности Голда
    int register_x[SIZE] = {0, 1, 1, 0, 0};
    int register_y[SIZE] = {1, 0, 0, 1, 1};

    // Инициализация регистров для второй последовательности Голда
    int register_x1[SIZE] = {0, 1, 1, 0, 1};
    int register_y1[SIZE] = {0, 1, 1, 1, 0};
    
    // Генерация и вывод первой последовательности Голда
    printf("\nFirst Gold's sequence (x = 12, y = 12+7=19):\n");
    Gold_sequence(random_sequence, register_x, register_y, length_seq);

    // Генерация и вывод второй последовательности Голда
    printf("Second Gold's sequence (x = 12+1, y = 19 - 5 = 14):\n");
    Gold_sequence(modified_sequence, register_x1, register_y1, length_seq);
    
    printf("\n");
    
    int shifted_sequence[length_seq];
    printf("Shift |1 |2 |3 |4 |5 |6 |7 |8 |9 |10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31|Autocorrelation\n");

    // Выполнение циклических сдвигов и вычисление автокорреляции
    for (int shift = 0; shift < length_seq + 1; shift++) {
        printf(" %5d|", shift);
        for (int i = 0; i < length_seq; i++) {
            shifted_sequence[i] = random_sequence[(i + shift) % length_seq];
            printf("%2d|", shifted_sequence[i]);
        }
        double autocorrelation_res = autocorrelation(random_sequence, shifted_sequence, length_seq);
        printf("%.3f", (autocorrelation_res / (double)31) );
        printf("\n");
    }
    
    printf("\n");

    double crosscorrelation_res = 0;
    double normalized_correlation_res = 0;

    // Вычисление кросс-корреляции и нормализованной корреляции для разных сдвигов
    for (int shift = 0; shift < length_seq; shift++) {
        crosscorrelation_res = crosscorrelation(random_sequence, modified_sequence, length_seq);
        normalized_correlation_res = normalized_correlation(random_sequence, modified_sequence, length_seq);
    }

    // Вывод результатов
    printf("The cross-correlation of two gold sequences is equal to: %.0f\n", crosscorrelation_res);
    printf("The normalized_correlation of two gold sequences is equal to: %.0f\n", normalized_correlation_res);
    return 0;
}


// что происходит с голосом , как он превращает в радиосигнал/синхронизация + как синхронизируются... (добавить в отчет + рассказать) + комменты в программах