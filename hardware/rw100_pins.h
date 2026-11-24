/*
 * rw100_pins.h - Pinbelegung und Grenzwerte der Steuerplatine RW-100
 *
 * SYNTHETISCH - fiktives Produkt, nur fuer Schulungszwecke.
 * Hardware: Steuerplatine RW-100, HW-Rev. A
 * Bezug: HWS-RW100 (Schnittstellen-Spezifikation)
 */
#ifndef RW100_PINS_H
#define RW100_PINS_H

/* Port und Pin zu einer Nummer zusammenfassen, z.B. RW_PORT_PIN('A', 6) = PA6 */
#define RW_PORT_PIN(port, pin) ((((port) - 'A') * 16) + (pin))

/* Motor */
#define RW_PIN_MOTOR_PWM          RW_PORT_PIN('A', 6)
#define RW_PWM_FREQ_HZ            2000u
#define RW_PIN_MOTOR_EN           RW_PORT_PIN('A', 7)

/* Drehzahlerfassung */
#define RW_PIN_TACHO              RW_PORT_PIN('A', 1)
#define RW_TACHO_PULSES_PER_REV   6u

/* Strommessung und Ueberlast (REQ-006) */
#define RW_PIN_I_SENSE            RW_PORT_PIN('A', 4)
#define RW_ADC_REF_MV             3300u
#define RW_OVERCURRENT_MV         1500u   /* entspricht 1,5 A */
#define RW_OVERCURRENT_TIME_MS    300u

/* Stopp-Taste (REQ-003) */
#define RW_PIN_STOP_BTN           RW_PORT_PIN('B', 4)
#define RW_STOP_ACTIVE_LEVEL      1u
#define RW_STOP_DEBOUNCE_MS       20u

/* Display (SPI) */
#define RW_PIN_DISP_SCK           RW_PORT_PIN('B', 13)
#define RW_PIN_DISP_MOSI          RW_PORT_PIN('B', 15)
#define RW_PIN_DISP_CS            RW_PORT_PIN('B', 12)

/* USB */
#define RW_PIN_USB_DP             RW_PORT_PIN('A', 12)
#define RW_PIN_USB_DM             RW_PORT_PIN('A', 11)

/* Fehler-LED */
#define RW_PIN_LED_ERR            RW_PORT_PIN('C', 13)
#define RW_LED_ERR_ACTIVE_LEVEL   0u

#endif /* RW100_PINS_H */
