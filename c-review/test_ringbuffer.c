/*
 * Minimale Tests für den Ringpuffer (nur "Happy Path").
 * Übersetzen und ausführen:
 *   gcc -std=c99 -Wall -Wextra -o test_rb ringbuffer.c test_ringbuffer.c && ./test_rb
 */
#include <stdio.h>
#include "ringbuffer.h"

static int failures = 0;

#define CHECK(cond) do { \
    if (!(cond)) { printf("FEHLER %s:%d: %s\n", __FILE__, __LINE__, #cond); failures++; } \
} while (0)

static void test_push_pop_order(void)
{
    ringbuffer_t rb;
    uint16_t v = 0;
    rb_init(&rb, "strom");
    CHECK(rb_push(&rb, 10) == 0);
    CHECK(rb_push(&rb, 20) == 0);
    CHECK(rb_pop(&rb, &v) == 0 && v == 10);
    CHECK(rb_pop(&rb, &v) == 0 && v == 20);
    CHECK(rb_pop(&rb, &v) == -1);
}

static void test_average_small_values(void)
{
    ringbuffer_t rb;
    rb_init(&rb, "strom");
    rb_push(&rb, 100);
    rb_push(&rb, 200);
    rb_push(&rb, 300);
    CHECK(rb_average(&rb) == 200);
}

/* Übung 6: Tests ergänzen, die die Review-Befunde belegen oder widerlegen. */

int main(void)
{
    test_push_pop_order();
    test_average_small_values();
    if (failures == 0) {
        printf("Alle Tests bestanden.\n");
        return 0;
    }
    printf("%d Test(s) fehlgeschlagen.\n", failures);
    return 1;
}
