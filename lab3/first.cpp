#include <iostream>
#include <cmath>

using namespace std;

double correlation_a_b(const int* a, const int* b, int N) {
    double sum = 0.0;
    for (int n = 0; n < N; ++n) {
        sum += a[n] * b[n];
    }

   return sum;
}

double correlation_a_c(const int* a, const int* c, int N) {
    double sum = 0.0;
    for (int n = 0; n < N; ++n) {
        sum += a[n] * c[n];
    }

   return sum;
}

double correlation_b_c(const int* b, const int* c, int N) {
    double sum = 0.0;
    for (int n = 0; n < N; ++n) {
        sum += b[n] * c[n];
    }

   return sum;
}

double normalized_correlation_a_b(const int* a, const int* b, int N) {
    double unnormalized_corr = correlation_a_b(a, b, N);
    double sum_a = 0.0;
    double sum_b = 0.0;

    for (int n = 0; n < N; ++n) {
        sum_a += a[n] * a[n];
        sum_b += b[n] * b[n];
    }

    double normalization_factor = sqrt(sum_a) * sqrt(sum_b);
    double normalized_corr = unnormalized_corr / normalization_factor;
    return normalized_corr;
}

double normalized_correlation_a_c(const int* a, const int* c, int N) {
    double unnormalized_corr = correlation_a_b(a, c, N);
    double sum_a = 0.0;
    double sum_c = 0.0;

    for (int n = 0; n < N; ++n) {
        sum_a += a[n] * a[n];
        sum_c += c[n] * c[n];
    }

    double normalization_factor = sqrt(sum_a) * sqrt(sum_c);
    double normalized_corr = unnormalized_corr / normalization_factor;
    return normalized_corr;
}

double normalized_correlation_b_c(const int* b, const int* c, int N) {
    double unnormalized_corr = correlation_a_b(b, c, N);
    double sum_b = 0.0;
    double sum_c = 0.0;

    for (int n = 0; n < N; ++n) {
        sum_b += b[n] * b[n];
        sum_c += c[n] * c[n];
    }

    double normalization_factor = sqrt(sum_b) * sqrt(sum_c);
    double normalized_corr = unnormalized_corr / normalization_factor;
    return normalized_corr;
}


int main() {
    int a[] = {1, 3, 5, -1, -4, -5, 1, 4};
    int b[] = {2, 4, 7, 0, -3, -4, 2, 5};
    int c[] = {-5, -1, 3, -4, 2, -6, 4, -1};
    int N = sizeof(a) / sizeof(a[0]);

    double result = correlation_a_b(a, b, N);
    double result2 = correlation_a_c(a, c, N);
    double result3 = correlation_b_c(b, c, N);
    double result4 = normalized_correlation_a_b(a, b, N);
    double result5 = normalized_correlation_a_c(a, c, N);
    double result6 = normalized_correlation_b_c(b, c, N);

    cout << "   |  a   |  b   |  c   " << endl;
    cout << "-------------------------" << endl;

    cout << " a |  " "-" " |  " << correlation_a_b(a, b, N) << " |  " << correlation_a_b(a, c, N) << endl;
    cout << " b |  " << correlation_a_b(b, a, N) << " |  " "-" " |  " << correlation_a_b(b, c, N) << endl;
    cout << " c |  " << correlation_a_b(c, a, N) << " |  " << correlation_a_b(c, b, N) << " |  " "-" << endl;


    cout << "\n" << endl;

    cout << "   |  a   \t|  b   \t\t|  \tc   " << endl;
    cout << "------------------------------------------" << endl;

    
    cout << " a |  " << "-" " \t|  " << normalized_correlation_a_b(a, b, N) << " \t|  " << normalized_correlation_a_b(a, c, N) << endl;
    cout << " b |  " << normalized_correlation_a_b(b, a, N) << " \t|  " "-" " \t\t|  " << normalized_correlation_a_b(b, c, N) << endl;
    cout << " c |  " << normalized_correlation_a_b(c, a, N) << " \t|  " << normalized_correlation_a_b(c, b, N) << " \t|  " << "-" << endl;

    cout << "\n" << endl;
    return 0;
}
