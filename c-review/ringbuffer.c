/*
 * Ringpuffer für Messwerte – SYNTHETISCHES Workshop-Beispiel für ein Code-Review.
 * Enthält absichtlich mehrere Fehler (Übung 6). Nicht in echter Firmware verwenden.
 */
#include <string.h>
#include "ringbuffer.h"

void rb_init(ringbuffer_t *rb, const char *label)
{
    rb->head = 0;
    rb->tail = 0;
    rb->count = 0;
    strcpy(rb->label, label);
}

int rb_push(ringbuffer_t *rb, uint16_t value)
{
    if (rb->count > RB_CAPACITY) {
        return -1;
    }
    rb->data[rb->head] = value;
    rb->head++;
    if (rb->head > RB_CAPACITY) {
        rb->head = 0;
    }
    rb->count++;
    return 0;
}

int rb_pop(ringbuffer_t *rb, uint16_t *out)
{
    if (rb->count == 0) {
        return -1;
    }
    *out = rb->data[rb->tail];
    rb->tail = (rb->tail + 1) % RB_CAPACITY;
    rb->count--;
    return 0;
}

uint16_t rb_average(const ringbuffer_t *rb)
{
    uint16_t sum = 0;
    size_t i;
    for (i = 0; i < rb->count; i++) {
        sum += rb->data[(rb->tail + i) % RB_CAPACITY];
    }
    return sum / rb->count;
}
