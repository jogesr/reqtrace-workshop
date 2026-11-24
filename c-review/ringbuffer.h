/*
 * Ringpuffer für Messwerte – SYNTHETISCHES Workshop-Beispiel für ein Code-Review.
 * Enthält absichtlich Fehler. Nicht in echter Firmware verwenden.
 */
#ifndef RINGBUFFER_H
#define RINGBUFFER_H

#include <stdint.h>
#include <stddef.h>

#define RB_CAPACITY 8
#define RB_LABEL_LEN 16

typedef struct {
    uint16_t data[RB_CAPACITY];
    size_t head;   /* nächste Schreibposition */
    size_t tail;   /* nächste Leseposition */
    size_t count;  /* Anzahl gespeicherter Werte */
    char label[RB_LABEL_LEN];
} ringbuffer_t;

void rb_init(ringbuffer_t *rb, const char *label);

/* Legt einen Wert ab. Rückgabe 0 bei Erfolg, -1 wenn der Puffer voll ist. */
int rb_push(ringbuffer_t *rb, uint16_t value);

/* Entnimmt den ältesten Wert. Rückgabe 0 bei Erfolg, -1 wenn leer. */
int rb_pop(ringbuffer_t *rb, uint16_t *out);

/* Mittelwert aller gespeicherten Werte (ganzzahlig). */
uint16_t rb_average(const ringbuffer_t *rb);

#endif
