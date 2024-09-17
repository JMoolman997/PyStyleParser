#include <stdio.h>
#include <string.h>

#define MAX_SIZE 100

// Simple data structure with pointers
struct Person {
    char name[50];
    int age;
    struct Person *best_friend;
};

// Function that uses pointer arithmetic
void manipulate_array(int *arr, int size) {
    int *ptr ;
    int i ;
    i= 0;
    ptr = arr;
    while (i < size) {
        *ptr = i * 2;
        ptr++;  // Pointer arithmetic
        i++;
    }
}

// Function that manipulates structs with pointer arithmetic
void manipulate_struct(struct Person *p) {
    if (p->best_friend != NULL) {
        printf("%s's best friend is %s\n", p->name, p->best_friend->name);
    } else {
        printf("%s has no best friend.\n", p->name);
    }
}

// Function with deeply nested control flow
void process_array(int *arr, int size) {
    int i, j, k;
    for (i = 0; i < size; i++) {
        if (arr[i] % 2 == 0) {
            for (j = 0; j < i; j++) {
                if (arr[j] > 5) {
                    printf("arr[%d] = %d, arr[%d] = %d\n", i, arr[i], j, arr[j]);
                } else {
                    if (arr[j] == 0) {
                        printf("Zero encountered at index %d\n", j);
                    }
                }
            }
        } else {
            if (i > 10) {
                k = 0;
                while (k < 3) {
                    if (arr[k] == 0) {
                        printf("Nested zero at index %d\n", k);
                    }
                    k++;
                }
            }
        }
    }
}

// Main function to demonstrate nested statements, pointer arithmetic, and structs
int main() {
    int array[MAX_SIZE];
    int i;
    manipulate_array(array, MAX_SIZE);

    // Nested struct manipulations
    struct Person john, jane;
    strcpy(john.name, "John");
    strcpy(jane.name, "Jane");
    john.age = 25;
    jane.age = 24;
    john.best_friend = &jane;
    jane.best_friend = NULL;

    manipulate_struct(&john);
    manipulate_struct(&jane);

    // Nested control flows and array processing
    process_array(array, 20);

    return 0;
}

