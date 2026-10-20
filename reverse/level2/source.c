#include <stdio.h>
#include <string.h>
#include <stdlib.h>

static void no(void)
{
    puts("Nope.");
    exit(1);
}

static void ok(void)
{
    puts("Good job.");
}

int main(void)
{
    char input[24];
    char out[9];
    char block[4];
    int i;
    int j;

    printf("Please enter key: ");
    if (scanf("%23s", input) != 1)
        no();

    if (input[0] != '0')
        no();
    if (input[1] != '0')
        no();

    fflush(stdin);

    memset(out, 0, 9);
    out[0] = 'd';
    i = 2;
    j = 1;

    while (strlen(out) < 8 && i + 2 < (int)strlen(input))
    {
        block[0] = input[i];
        block[1] = input[i + 1];
        block[2] = input[i + 2];
        block[3] = '\0';

        out[j] = (char)atoi(block);
        i += 3;
        j += 1;
    }

    out[j] = '\0';

    if (strcmp(out, "delabere") == 0)
        ok();
    else
        no();

    return 0;
}
