#include <stdio.h>

struct Rectangle {
    struct Point {
        int x;
        int y;
    } topLeft, bottomRight;
};

int main() {
    struct Rectangle rect;
    rect.topLeft.x = 0;
    rect.topLeft.y = 10;
    rect.bottomRight.x = 10;
    rect.bottomRight.y = 0;

    printf("Top Left: (%d, %d)\n", rect.topLeft.x, rect.topLeft.y);
    printf("Bottom Right: (%d, %d)\n", rect.bottomRight.x, rect.bottomRight.y);

    return 0;
}

