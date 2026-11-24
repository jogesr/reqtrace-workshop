# Schnittstellen-Spezifikation Steuerplatine RW-100

> SYNTHETISCH – fiktives Produkt, nur für Schulungszwecke.

Dokument-ID: HWS-RW100 · Version 0.3 · Stand 2026-10-08 · Hardware-Rev. B
Bezug: SPEC-RW100 Version 0.3

## 1 Mikrocontroller

- MCU-X32 (fiktiv), Versorgung 3,3 V, ADC 12 bit, ADC-Referenz 3,3 V
- Pinbezeichnung: Port und Nummer, z.B. `PA6` = Port A, Pin 6

## 2 Pinbelegung

| Signal | MCU-Pin | Richtung | Elektrisch | Bezug | Bemerkung |
|---|---|---|---|---|---|
| MOTOR_PWM | PA6 | Ausgang | PWM 20 kHz, 3,3 V | REQ-001, REQ-002 | an Motortreiber U3, Eingang IN1 |
| MOTOR_EN | PA7 | Ausgang | aktiv high | REQ-003, REQ-006 | Low sperrt den Motortreiber |
| TACHO | PA1 | Eingang | Hall-Sensor, Open-Drain, Pull-up 10 kΩ (R10), 6 Impulse pro Umdrehung | REQ-002, REQ-004 | Stecker J4 |
| I_SENSE | PA4 | Analog | Shunt 0,1 Ω (R20), Strommessverstärker U5 mit Verstärkung 20 | REQ-006 | |
| STOP_BTN | PB3 | Eingang | aktiv low, Pull-up 10 kΩ (R12), Entprellung 20 ms in der Firmware | REQ-003 | Taster SW1 |
| BUZZER | PA8 | Ausgang | aktiv high, Treiber Q2, Summer BZ1 | REQ-005 | |
| DISP_SCK | PB13 | Ausgang | SPI | REQ-004 | Display U6 |
| DISP_MOSI | PB15 | Ausgang | SPI | REQ-004 | Display U6 |
| DISP_CS | PB12 | Ausgang | aktiv low | REQ-004 | Display U6 |
| USB_DM | PA11 | bidirektional | USB Full Speed | REQ-010, REQ-012 | Buchse J1 |
| USB_DP | PA12 | bidirektional | USB Full Speed | REQ-010, REQ-012 | Buchse J1 |
| LED_ERR | PC13 | Ausgang | aktiv low | REQ-006 | LED D5 |

## 3 Grenzwerte

| Grösse | Wert | Herleitung | Bezug |
|---|---|---|---|
| Überlast-Schwelle Strom | 1,5 A | aus REQ-006 | REQ-006 |
| Überlast-Schwelle am ADC-Eingang | 3,0 V | 1,5 A × 0,1 Ω × 20 | REQ-006 |
| Überlast-Dauer bis Abschaltung | 3 s | aus REQ-006 | REQ-006 |
| Stillstand nach Stopp | ≤ 1 s | aus REQ-003; MOTOR_EN wird sofort auf Low gesetzt | REQ-003 |

## 4 Offene Punkte

- Display-Aktualisierungsrate (REQ-004) wird in der Firmware festgelegt, nicht in dieser Spezifikation.
