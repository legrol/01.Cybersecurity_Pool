#include <stdio.h>
#include <string.h>

int main(void)
{
    char input[108];
    const char expected[] = "__stack_check";

    printf("Please enter key: ");
    if (scanf("%107s", input) != 1)
    {
        printf("Nope.\n");
        return 0;
    }

    if (strcmp(input, expected) == 0)
    {
        printf("Good job.\n");
    }
    else
    {
        printf("Nope.\n");
    }

    return 0;
}
