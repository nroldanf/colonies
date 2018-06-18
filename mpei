.include "xc.inc"
.equ __33FJ128MC802, 1
.macro IMP_CHAR LETRA
    BSET LCD_control_port,#LCD_RS
    BCLR LCD_control_port,#LCD_RW
    MOV \LETRA,W0
    MOV W0,W1
    ;***NIBBLE MÁS SIGNIFICATIVO***
    AND #0x00F0,W1;valor para la mascara
    SL W1,#4,W1
    MOV W1,LCD_data_port
    CALL P_E
    ;***NIBBLE MENOS SIGNITICATIVO***
    AND #0x000F,W0
    SL W0,#8,W0
    MOV W0,LCD_data_port
    CALL P_E
    CALL delay_150us
.endm
.macro ROTAR 
    IMP_COT #0x18
    CALL delay_1s
.endm
.macro IMP_NUM NUMERO
    BSET LCD_control_port,#LCD_RS
    BCLR LCD_control_port,#LCD_RW
    MOV #0X0300,W0
    ;***NIBBLE MÁS SIGNIFICATIVO***
    MOV W0,LCD_data_port
    CALL P_E
    ;***NIBBLE MENOS SIGNITICATIVO***
    MOV \NUMERO,W0
    AND #0x000F,W0
    SL W0,#8,W0
    MOV W0,LCD_data_port
    CALL P_E
    CALL delay_150us
.endm
    
.macro IMP_COT LETRA
    BCLR LCD_control_port,#LCD_RS
    BCLR LCD_control_port,#LCD_RW
    MOV \LETRA,W0
    MOV W0,W1
    ;***NIBBLE MÁS SIGNIFICATIVO***
    AND #0x00F0,W1;valor para la mascara
    SL W1,#4,W1
    MOV W1,LCD_data_port
    CALL P_E
    ;***NIBBLE MENOS SIGNITICATIVO***
    AND #0x000F,W0
    SL W0,#8,W0
    MOV W0,LCD_data_port
    CALL P_E
    CALL delay_150us
.endm    
;constantes
.equ LCD_EN, RA0
.equ LCD_RS, RA1
.equ LCD_RW, RA2
.equ LCD_control_port, LATA
.equ LCD_data_port, LATB
.equ AA,W4;W5
.equ BB,W6;W7
.equ RESPDEC,W8
.equ RESPDECH,W9
.equ RESPUESTA,W10;W11
.equ RESPUESTAH,W11
.equ CHAR_OP,W12
.equ BANDERA,W13
.equ CONTADOR,W14
.equ OP_OK,0
.equ AA_BB_OK,1
.equ FINISH,2
.equ numeneg,3

;delays
.equ K_10us, 11
.equ K_150us, 183
.equ K_10ms, 66
.equ K_1s,6605
.equ K_2s, 13210  
.global _main
config __FOSC, OSCIOFNC_ON
.text
    
_main:
    MOV #0xFFF8,W0;salidas RA0-RA4
    MOV W0,TRISA;PORT
    MOV #0xF00F,W0
    MOV W0,TRISB
    SETM AD1PCFGL
    MOV #0x00F0,W0
    MOV W0,CNPU1
    MOV W0,CNEN1
    CALL init_LCD
    CALL LCD_reset
    CALL mensaje
    CALL delay_2s
    CALL LCD_reset
    CALL mensaje2
    CALL delay_1s
    MOV #80,W3
ROT:
    ROTAR
    DEC W3,W3
    BRA NZ,ROT
    CALL delay_2s
    CALL LCD_reset
WAT:    
    BRA WAT
    
    
    ;%%%%%%%%%%%%%%% espere
LOOP:
    CLR LATB
    BCLR IFS1,#CNIF
SLEEEP:
    BTSS IFS1,#CNIF
    BRA SLEEEP
    CALL delay_10ms
    CALL LECTURA_DISP
    MOV #'*',W0
    CP W2,W0
    BRA Z,REINICIO
    BTSC BANDERA,#FINISH
    BRA REINICIO
    CP W2,#0
    BRA NZ,GOP
    BRA NUMERO
    
;SUBRUTINAS    

GOP:;GUARDA LA OPERACION A REALIZAR SI W7[3]ES 0 Y W2 ES DIFERENTE DE '=', DE SER IGUAL SALTA A OPERACION
    MOV #'=',W0
    CP W0,W2
    BRA Z, OPERACION
    BTSC BANDERA,#OP_OK
    CLR CONTADOR
    BRA ANTIRREBOTE
    MOV W2,CHAR_OP
    BSET BANDERA,#OP_OK
    IMP_CHAR CHAR_OP
    BRA ANTIRREBOTE

OPERACION:
    BSET BANDERA,#FINISH
    
    MOV #'+',W0
    CP W0,CHAR_OP
    BRA Z,SUMA
    
    MOV #'-',W0
    CP W0,CHAR_OP
    BRA Z,RESTA
    
    MOV #'x',W0
    CP W0,CHAR_OP
    BRA Z,MULTI
    
    MOV #'/',W0
    CP W0,CHAR_OP
    BRA Z,DIVI
    
    MOV #0,W0
    CP W0,CHAR_OP
    BRA Z,IGUAL
SUMA:
    ADD AA,BB,RESPUESTA
    CALL LINEA2
    CALL CONV_BCD
    BRA ANTIRREBOTE
RESTA:
    SUB AA,BB,RESPUESTA
    BTSC SR,#N
    BSET BANDERA,#numeneg
    BTSC BANDERA,#numeneg
    CALL NUMNEG
    BTSS BANDERA,#numeneg
    CALL LINEA2
    CALL CONV_BCD
    BRA ANTIRREBOTE
NUMNEG:
    CALL LINEA2
    IMP_CHAR #'-'
    COM RESPUESTA,RESPUESTA
    DEC RESPUESTA,RESPUESTA
    RETURN
MULTI:
    MUL.UU AA,BB,RESPUESTA
    CALL LINEA2
    CALL CONV_BCD
    BRA ANTIRREBOTE
DIVI:
    CP BB,#0
    BRA Z,MATH_ERROR
    REPEAT #17
    DIV.U AA,BB
    MOV.D W0,RESPUESTA
    MOV #1000,W0
    MUL.UU RESPUESTAH,W0,AA
    REPEAT #17
    DIV.U AA,BB
    MOV.D W0,RESPDEC
    CALL LINEA2
    CALL CONV_BCD
    IMP_CHAR #','
    ;SE VA A GUARDAR EN W2 DECIMAS,W3 CENTESIMAS,W4 MILESIMAS
MILESIMAS:
    MOV RESPDEC,W2
    MOV #0X000F,W0
    AND W0,W2,W2
    CP W2,#10
    BRA NC,ARREGLAR_MILESIMAS
CENTESIMAS: 
    MOV RESPDEC,W3
    MOV #0X00F0,W0
    AND W0,W3,W3
    LSR W3,#4,W3
    CP W3,#10
    BRA NC,ARREGLAR_CENTESIMAS
DECIMAS:
    MOV RESPDEC,W4
    MOV #0X0F00,W0
    AND W0,W4,W4
    LSR W4,#8,W4
    CP W4,#10
    BRA NC,ARREGLAR_DECIMAS
ARREGLAR_MILESIMAS:
    ADD #6,RESPDEC
    BRA UNIDADES
ARREGLAR_CENTESIMAS: 
    ADD #0X0060,RESPDEC
    BRA DECENAS
ARREGLAR_DECIMAS:
    MOV #0X0600,W0
    ADD W0,RESPDEC,RESPDEC
    BRA CENTENAS
    IMP_NUM W4
    IMP_NUM W3
    IMP_NUM W2   
    BRA ANTIRREBOTE
IGUAL:
    MOV AA,RESPUESTA
    CALL CONV_BCD
    BRA ANTIRREBOTE
NUMERO: 
    BTSC BANDERA,#AA_BB_OK
    BRA ANTIRREBOTE
    BTSC BANDERA,#OP_OK
    BRA NUMB
    MUL.UU AA,#10,AA
    ADD W1,AA,AA
    INC CONTADOR,CONTADOR
    CP CONTADOR,#3
    BRA Z, BANDERA_ON
    BRA IMPRIMIR_NUM
BANDERA_ON:
    BSET BANDERA,#AA_BB_OK
IMPRIMIR_NUM:
    IMP_NUM W1
    BRA ANTIRREBOTE
NUMB:
    MUL.UU BB,#10,BB
    ADD W1,BB,BB
    INC CONTADOR,CONTADOR
    CP CONTADOR,#3
    BRA Z, BANDERA_ON
    BRA IMPRIMIR_NUM
ANTIRREBOTE:    
    CLR LATB
    BCLR IFS1,#CNIF
WAIT_ANTIREBOTE:
    CALL delay_10ms
    BTSS IFS1,#CNIF
    BRA WAIT_ANTIREBOTE
    BRA LOOP
MATH_ERROR:
    CALL LCD_reset
    IMP_CHAR #'M'
    IMP_CHAR #'A'
    IMP_CHAR #'T'
    IMP_CHAR #'H'
    IMP_CHAR #' '
    IMP_CHAR #'E'
    IMP_CHAR #'R'
    IMP_CHAR #'R'
    IMP_CHAR #'O'
    IMP_CHAR #'R'
    BRA ANTIRREBOTE
CONV_BCD:
    NOP;SE VA A GUARDAR EN W2 UNIDADES,W3 DECENAS,W4 CENTENAS,W5 MILESIMAS, W6 DECENAS DE MIL,W7 CENTENAS DE MIL
UNIDADES:
    MOV RESPUESTA,W2
    MOV #0X000F,W0
    AND W0,W2,W2
    CP W2,#10
    BRA NC,ARREGLAR_UNIDADES
DECENAS: 
    MOV RESPUESTA,W3
    MOV #0X00F0,W0
    AND W0,W3,W3
    LSR W3,#4,W3
    CP W3,#10
    BRA NC,ARREGLAR_DECENAS
CENTENAS:
    MOV RESPUESTA,W4
    MOV #0X0F00,W0
    AND W0,W4,W4
    LSR W4,#8,W4
    CP W4,#10
    BRA NC,ARREGLAR_CENTENAS
MILES:
    MOV RESPUESTA,W5
    MOV #0XF000,W0
    AND W0,W5,W5
    LSR W5,#12,W5
    CP W5,#10
    BRA NC,ARREGLAR_MILES
DECENAS_DE_MIL:
    MOV RESPUESTAH,W6
    MOV #0X000F,W0
    AND W0,W6,W6
    CP W6,#10
    BRA NC,ARREGLAR_DECENAS_DE_MIL
CENTENAS_DE_MIL:
    MOV RESPUESTAH,W7
    MOV #0X00F0,W0
    AND W0,W7,W7
    LSR W7,#4,W7
    CP W7,#10
    BRA NC,ARREGLAR_CENTENAS_DE_MIL
    IMP_NUM W7
    IMP_NUM W6
    IMP_NUM W5
    IMP_NUM W4
    IMP_NUM W3
    IMP_NUM W2

    RETURN
ARREGLAR_UNIDADES:
    ADD #6,RESPUESTA
    ADDC #0,RESPUESTAH
    BRA UNIDADES
ARREGLAR_DECENAS: 
    ADD #0X0060,RESPUESTA
    ADDC #0,RESPUESTAH
    BRA DECENAS
ARREGLAR_CENTENAS:
    MOV #0X0600,W0
    ADD W0,RESPUESTA,RESPUESTA
    ADDC #0,RESPUESTAH
    BRA CENTENAS
ARREGLAR_MILES:
    MOV #0X6000,W0
    ADD W0,RESPUESTA,RESPUESTA
    ADDC #0,RESPUESTAH
    BRA MILES
ARREGLAR_DECENAS_DE_MIL:
    ADD #0X0006,RESPUESTAH
    BRA DECENAS_DE_MIL
ARREGLAR_CENTENAS_DE_MIL:
    ADD #0X0060,RESPUESTAH
    BRA CENTENAS_DE_MIL
    
    
    
LECTURA_DISP:
    
    BCLR IFS1,#CNIF
    MOV #0,W1
    MOV #0,W2
    
    
    MOV #0X0010,W0
    MOV W0,LATB
    MOV PORTB,W0
    MOV #0X000F,W3
    AND W0,W3,W0
    BTSS W0,#0
    MOV #1,W1
    BTSS W0,#1
    MOV #4,W1
    BTSS W0,#2
    MOV #7,W1
    BTSS W0,#3
    MOV #'*',W2
    
    MOV #0X0020,W0
    MOV W0,LATB
    MOV PORTB,W0
    AND W0,W3,W0
    BTSS W0,#0
    MOV #2,W1
    BTSS W0,#1
    MOV #5,W1
    BTSS W0,#2
    MOV #8,W1
    BTSS W0,#3
    MOV #0,W1
    
    MOV #0X0040,W0
    MOV W0,LATB
    MOV PORTB,W0
    AND W0,W3,W0
    BTSS W0,#0
    MOV #3,W1
    BTSS W0,#1
    MOV #6,W1
    BTSS W0,#2
    MOV #9,W1
    BTSS W0,#3
    MOV #'=',W2
    
    MOV #0X0080,W0
    MOV W0,LATB
    MOV PORTB,W0
    AND W0,W3,W0
    BTSS W0,#0
    MOV #'+',W2
    BTSS W0,#1
    MOV #'-',W2
    BTSS W0,#2
    MOV #'x',W2
    BTSS W0,#3
    MOV #'/',W2
    
    RETURN
REINICIO:
    MOV #28,W0
BORRANDO:
    CLR [W0]
    DEC2 W0,W0
    BRA NZ, REINICIO
    CLR W0
    CALL LCD_reset;BORRAR DISPLAY
    BRA ANTIRREBOTE
    
init_LCD:   
    CALL delay_10ms
    CALL delay_10ms                  ;1
    BCLR LCD_control_port,#LCD_RS
    BCLR LCD_control_port,#LCD_RW
    MOV #0x0300,W0
    MOV W0,LCD_data_port
    CALL P_E
    CALL delay_10us
    CALL P_E
    CALL delay_150us
    CALL P_E
    CALL delay_150us
    CALL P_E
    CALL delay_150us
    ;MODO: function set que yo desee
    IMP_COT #0x0028
    IMP_COT #0x000C
    RETURN
LCD_reset:
    IMP_COT #0x0001
    CALL delay_10ms
    RETURN

P_E: 
    BSET LCD_control_port,#LCD_EN
    CALL delay_500ns
    BCLR LCD_control_port,#LCD_EN
    CALL delay_500ns
    RETURN
    
LINEA2:
    IMP_COT #0xC0
    return
    
mensaje:
    IMP_CHAR #'C'
    IMP_CHAR #'a'
    IMP_CHAR #'l'
    IMP_CHAR #'c'
    IMP_CHAR #'u'
    IMP_CHAR #'l'
    IMP_CHAR #'a'
    IMP_CHAR #'d'
    IMP_CHAR #'o'
    IMP_CHAR #'r'
    IMP_CHAR #'a'
    IMP_CHAR #' '
    IMP_CHAR #'e'
    IMP_CHAR #'n'
    CALL LINEA2
    IMP_CHAR #'a'
    IMP_CHAR #'s'
    IMP_CHAR #'s'
    IMP_CHAR #'e'
    IMP_CHAR #'m'
    IMP_CHAR #'b'
    IMP_CHAR #'l'
    IMP_CHAR #'e'
    IMP_CHAR #'r'
    RETURN
mensaje2:
    IMP_CHAR #'A'
    IMP_CHAR #'n'
    IMP_CHAR #'d'
    IMP_CHAR #'r'
    IMP_CHAR #'e'
    IMP_CHAR #'s'
    IMP_CHAR #' '
    IMP_CHAR #'M'
    IMP_CHAR #'/'
    IMP_CHAR #'N'
    IMP_CHAR #'a'
    IMP_CHAR #'t'
    IMP_CHAR #'a'
    IMP_CHAR #'l'
    IMP_CHAR #'i'
    IMP_CHAR #'a'
    IMP_CHAR #' '
    IMP_CHAR #'S'
    IMP_CHAR #'/'
    IMP_CHAR #'N'
    IMP_CHAR #'i'
    IMP_CHAR #'c'
    IMP_CHAR #'o'
    IMP_CHAR #'l'
    IMP_CHAR #'a'
    IMP_CHAR #'s'
    IMP_CHAR #' '
    IMP_CHAR #'R'
    CALL LINEA2
    IMP_CHAR #'I'
    IMP_CHAR #'E'
    IMP_CHAR #'L'
    IMP_CHAR #'C'
    IMP_CHAR #' '
    IMP_CHAR #'5'
    IMP_CHAR #'i'
    IMP_CHAR #' '
    IMP_CHAR #'/'
    IMP_CHAR #'I'
    IMP_CHAR #'B'
    IMP_CHAR #'I'
    IMP_CHAR #'O'
    IMP_CHAR #' '
    IMP_CHAR #'7'
    IMP_CHAR #'i'
    IMP_CHAR #' '
    IMP_CHAR #' '
    IMP_CHAR #'/'
    IMP_CHAR #'I'
    IMP_CHAR #'B'
    IMP_CHAR #'I'
    IMP_CHAR #'O'
    IMP_CHAR #' '
    IMP_CHAR #'8'
    IMP_CHAR #'i'
    return
    
    
    ;************************** DELAYS *******************************************


delay_500ns:
    NOP
    RETURN

delay_10us:
    MOV #K_10us, W0
wait_10us:
    DEC W0,W0
    BRA NZ, wait_10us
    RETURN
delay_150us:
    MOV #K_150us, W0
wait_150us:
    DEC W0,W0;1
    BRA NZ,wait_150us;1(2)
    RETURN;(2 o 3)
delay_10ms:
    MOV #K_10ms,W0
wait_10ms:
    PUSH W0
    CALL delay_150us
    POP W0
    DEC W0,W0
    BRA NZ,wait_10ms
    RETURN
delay_1s:
    MOV #K_1s,W0
wait_1s:
    PUSH W0
    CALL delay_150us
    POP W0
    DEC W0,W0
    BRA NZ,wait_1s
    RETURN
delay_2s:
    MOV #K_2s,W0
wait_2s:
    PUSH W0
    CALL delay_150us
    POP W0
    DEC W0,W0
    BRA NZ,wait_2s
    RETURN
    
.end   
    
