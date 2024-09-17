#include <stdio.h>
#define MAX_SIZE 100

/* Function prototypes */
int addNumbers(int a, int b);
void printArray(int arr[], int size);
int factorial(int n);

int main() {
    int result;
    int array[MAX_SIZE];
    int i;

    /* Initialize array */
    for (i = 0; i < MAX_SIZE; i++) {
        array[i] = i + 1;
    }

    /* Compute sum */
    result = addNumbers(5, 10);
    printf("Sum: %d\n", result);

    /* Print array */
    printArray(array, MAX_SIZE);

    /* Compute factorial */
    result = factorial(5);
    printf("Factorial: %d\n", result);

    return 0;
}

int addNumbers(int a, int b) {
    int sum;
    sum = a + b;
    return sum;
}

void printArray(int arr[], int size) {
    int i;
    printf("Array elements:\n");
    for (i = 0; i < size; i++) {
        if (i % 10 == 0)  {
            printf("\n");
		}
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int factorial(int n) {
    if (n == 0) {
        return 1;
	}
    else {
        int result;
        result = n * factorial(n - 1);
        return result;
    }
}

