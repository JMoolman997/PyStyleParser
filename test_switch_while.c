#include <stdio.h>

int main() {
    int x = 0;
    
    while (x < 5) {
        switch (x) {
            case 0:
                printf("Zero\n");
                break;
            case 1:
                if (x % 2 == 0) {
                    printf("Even\n");
                } else {
                    printf("Odd\n");
                }
                break;
            default:
                printf("Other\n");
                break;
        }
        x++;
    }
    
    return 0;
}

