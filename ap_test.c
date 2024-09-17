#include <stdio.h>

// Macro definition
#define MAX_SIZE 100
#define SQUARE(x) ((x) * (x))

// Simple data structure (struct)
struct Point {
    int x;
    int y;
};

// Function to manipulate array and pointer arithmetic
void manipulate_array(int *arr, int size) {
    int *ptr = arr;
    for (int i = 0; i < size; i++) {
        *ptr = i * 2;  // Pointer arithmetic
        ptr++;
    }
}

// Main function demonstrating multiple features
int main() {
    // Array initialization
    int array[MAX_SIZE];
    manipulate_array(array, MAX_SIZE);

    // Nested while loops
    int i = 0;
    while (i < 10) {
        int j = 0;
        while (j < 5) {
            printf("i: %d, j: %d\n", i, j);
            j++;
        }
        i++;
    }

    // Switch statement example
    int x = 2;
    switch (x) {
        case 1:
            printf("One\n");
            break;
        case 2:
            printf("Two\n");
            break;
        case 3:
            printf("Three\n");
            break;
        default:
            printf("Default\n");
            break;
    }

    // Working with struct and array of structs
    struct Point points[5];
    for (i = 0; i < 5; i++) {
        points[i].x = SQUARE(i);
        points[i].y = i + 10;
    }

    // Display points
    for (i = 0; i < 5; i++) {
        printf("Point %d: (%d, %d)\n", i, points[i].x, points[i].y);
    }

    return 0;
}

