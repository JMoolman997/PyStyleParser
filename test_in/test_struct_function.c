#include <stdio.h>
#include <string.h>

struct Person {
    char name[20];
    int age;
};

void printPerson(struct Person p) {
    printf("Name: %s, Age: %d\n", p.name, p.age);
}

int main() {
    struct Person john;
    strcpy(john.name, "John Doe");
    john.age = 30;

    printPerson(john);

    return 0;
}

