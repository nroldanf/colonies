;*******************************************************************************
;                                                                              *
;    Filename:  calculadora_news.s                                             *
;    Date:      20/06/2018                                                     *
;    File Version: v1                                                          *
;    Author:    	Andres Moreno, Nicolas Roldan, Natalia Suarez          *
;    Company:   	Escuela Colombiana de Ingenieria Julio Garavito        *
;    Description:  Calculadora en assembler de 2 numeros de 3 digitos sin signo*
;                  Se usa el teclado matricial 4*4 donde las teclas            *
;		   A,B,C,D,#,*  seran suma,resta,multiplicacion,divicion,igual *
;		   y C/CE respectivamente				       *
;*******************************************************************************

;*******************************************************************************
; Processor Inclusion
;*******************************************************************************
.include "P33FJ128MC802.inc"
.equ __33FJ128MC802, 1
    
;*******************************************************************************
; Configuration Word Setup
;*******************************************************************************
config __FOSC, OSCIOFNC_ON
config __FWDT, FWDTEN_OFF  
config __FICD, ICS_PGD2 & JTAGEN_OFF;simular en caliente (con las entradas desde el sdpic sin stimulus)
;*******************************************************************************
; Macros
;*******************************************************************************
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
;*******************************************************************************
;Program Specific Constants
;*******************************************************************************

.equ LCD_EN, RA0
.equ LCD_RS, RA1
.equ LCD_RW, RA2
.equ LCD_control_port, LATA
.equ LCD_data_port, LATB
.equ AA,W4
.equ AAH,W5
.equ BB,W6
.equ BBH,W7
.equ RESPDEC,W8
.equ RESPDECH,W9
.equ RESPUESTA,W10
.equ RESPUESTAH,W11
.equ CHAR_OP,W12
.equ BANDERA,W13
.equ CONTADOR,W14
.equ OP_OK,0
.equ AA_BB_OK,1
.equ FINISH,2
.equ numeneg,3
.equ RESP_CEROS,4  
.equ AAXD,5

;delays
.equ K_10us, 11
.equ K_150us, 183
.equ K_10ms, 66
.equ K_1s,6605
.equ K_2s, 13210  
;*******************************************************************************
;Global Declarations:
;*******************************************************************************

.global _main
;*******************************************************************************
;Code Section in Program Memory
;*******************************************************************************

.text
    
_main:
    MOV #0xFFF8,W0;salidas RA0-RA4 (RA3 INTERRUPTOR)
    MOV W0,TRISA
    MOV #0xF00F,W0
    MOV W0,TRISB
    SETM AD1PCFGL
    MOV #0x00F0,W0
    MOV W0,CNPU1
    MOV W0,CNEN1
    CALL init_LCD
    CALL LCD_reset
    CLR CONTADOR
    BTSC PORTA,#3
    BRA LOOP
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

    
    
    ; INICIA LA CALCULADORA
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
    
;*******************************************************************************
;Subroutines
;*******************************************************************************


GOP:;GUARDA LA OPERACION A REALIZAR SI OP_OK ES 0 Y W2 ES DIFERENTE DE '=', DE SER IGUAL SALTA A OPERACION
    MOV #'=',W0
    CP W0,W2
    BRA Z, OPERACION
    BTSC BANDERA,#OP_OK
    BRA ANTIRREBOTE
    CLR CONTADOR
    MOV W2,CHAR_OP
    BSET BANDERA,#OP_OK
    BCLR BANDERA,#AA_BB_OK
    IMP_CHAR CHAR_OP
    BRA ANTIRREBOTE

OPERACION:
    BSET BANDERA,#FINISH
    
    CP0 CHAR_OP
    BRA Z,IGUAL 
    
    CP0 CONTADOR
    BRA Z,SYNTAX_ERROR 
    
    MOV #'+',W0
    CP W0,CHAR_OP
    BRA Z,SUMA
    
    MOV #'-',W0
    CP W0,CHAR_OP
    BRA Z,RESTA
    
    BTSS BANDERA,#AAXD
    BRA SYNTAX_ERROR 
    
    MOV #'x',W0
    CP W0,CHAR_OP
    BRA Z,MULTI
    
    MOV #'/',W0
    CP W0,CHAR_OP
    BRA Z,DIVI
    
    
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
    INC RESPUESTA,RESPUESTA
    RETURN
MULTI:
    MUL.UU AA,BB,RESPUESTA
    CALL LINEA2
    CALL CONV_BCD
    BRA ANTIRREBOTE
DIVI:
    CP0 BB
    BRA Z,MATH_ERROR
    REPEAT #17
    DIV.U AA,BB
    MOV W0,RESPUESTA
    MOV #1000,W0
    MUL.UU W1,W0,AA
    REPEAT #17
    DIV.U AA,BB
    MOV W0,RESPDEC
    CALL LINEA2
    CALL CONV_BCD
    CP0 RESPDEC
    BRA Z,ANTIRREBOTE
    IMP_CHAR #','
    ;SE VA A GUARDAR EN W2 DECIMAS,W3 CENTESIMAS,W4 MILESIMAS
    CLR W4
    CLR W3
    MOV #0X0064,W2
DECIMAS:
    CP RESPDEC,W2
    BRA C,ARREGLAR_DECIMAS 
    MOV #0X000A,W2
CENTESIMAS: 
    CP RESPDEC,W2
    BRA C,ARREGLAR_CENTESIMAS
    CLR W2
MILESIMAS:
    CP RESPDEC,#0X0001
    BRA C,ARREGLAR_MILESIMAS
    BRA IMPDECIMAS
ARREGLAR_MILESIMAS:
    INC W2,W2
    DEC RESPDEC,RESPDEC
    BRA MILESIMAS
ARREGLAR_CENTESIMAS: 
    INC W3,W3
    SUB RESPDEC,W2,RESPDEC
    BRA CENTESIMAS
ARREGLAR_DECIMAS:
    INC W4,W4
    SUB RESPDEC,W2,RESPDEC
    BRA DECIMAS
IMPDECIMAS:
    IMP_NUM W4
    IMP_NUM W3
    IMP_NUM W2   
    BRA ANTIRREBOTE
IGUAL:
    CP0 CONTADOR 
    BRA Z,ANTIRREBOTE
    MOV AA,RESPUESTA
    CALL LINEA2
    CALL CONV_BCD
    BRA ANTIRREBOTE
NUMERO: 
    BTSC BANDERA,#AA_BB_OK
    BRA	 ANTIRREBOTE
    BTSC BANDERA,#OP_OK
    BRA NUMB
    BSET BANDERA,#AAXD
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
WAIT_ANTIREBOTE:
    CALL delay_10ms
    CALL delay_10ms
    MOV PORTB,W0
    MOV #0X000F,W1
    AND W1,W0,W0
    CP W1,W0
    BRA NZ, WAIT_ANTIREBOTE
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
SYNTAX_ERROR:
    CALL LCD_reset
    IMP_CHAR #'S'
    IMP_CHAR #'Y'
    IMP_CHAR #'N'
    IMP_CHAR #'T'
    IMP_CHAR #'A'
    IMP_CHAR #'X'
    IMP_CHAR #' '
    IMP_CHAR #'E'
    IMP_CHAR #'R'
    IMP_CHAR #'R'
    IMP_CHAR #'O'
    IMP_CHAR #'R'
    BRA ANTIRREBOTE
CONV_BCD:
    MOV #14,W0
CLR_REG_BCD:
;se usara el algoritmo Conversi󮠤e fuerza bruta,este VA REALIZANDO UNA DIVICION EN BASE 10  
;SE VA A GUARDAR EN W2 UNIDADES,W3 DECENAS,W4 CENTENAS,W5 MILESIMAS, W6 DECENAS DE MIL,W7 CENTENAS DE MIL
    CLR [W0]
    DEC2 W0,W0
    BRA NZ, CLR_REG_BCD
    MOV #0X86A0,W2
CENTENAS_DE_MIL:
    CP RESPUESTA,W2
    CPB RESPUESTAH,#1
    BRA C ,ARREGLAR_CENTENAS_DE_MIL 
    MOV #0X2710,W2
DECENAS_DE_MIL:
    CP RESPUESTA,W2
    CPB RESPUESTAH,#0
    BRA C,ARREGLAR_DECENAS_DE_MIL
    MOV #0X03E8,W2
MILES:
    CP RESPUESTA,W2
    CPB RESPUESTAH,#0
    BRA C,ARREGLAR_MILES
    MOV #0X0064,W2
CENTENAS:
    CP RESPUESTA,W2
    BRA C,ARREGLAR_CENTENAS
    MOV #0X000A,W2
DECENAS: 
    CP RESPUESTA,W2
    BRA C,ARREGLAR_DECENAS
    CLR W2
UNIDADES:
    CP RESPUESTA,#0X0001
    BRA C,ARREGLAR_UNIDADES
    
    
    CP0 W7
    BRA Z,IMP_DECENAS_DE_MIL
IMP_CENTENAS_DE_MIL:  
    BSET BANDERA,#RESP_CEROS
    IMP_NUM W7
IMP_DECENAS_DE_MIL:
    CP0 W6
    BTSS BANDERA,#RESP_CEROS
    BRA Z,IMP_MILES
    BSET BANDERA,#RESP_CEROS
    IMP_NUM W6
IMP_MILES:   
    CP0 W5
    BTSS BANDERA,#RESP_CEROS
    BRA Z,IMP_CENTENAS
    BSET BANDERA,#RESP_CEROS
    IMP_NUM W5
IMP_CENTENAS:
    CP0 W4
    BTSS BANDERA,#RESP_CEROS
    BRA Z,IMP_DECENAS
    BSET BANDERA,#RESP_CEROS
    IMP_NUM W4
IMP_DECENAS: 
    CP0 W3
    BTSS BANDERA,#RESP_CEROS
    BRA Z,IMP_UNIDADES
    IMP_NUM W3
IMP_UNIDADES:
    BCLR BANDERA,#RESP_CEROS
    IMP_NUM W2
    
    RETURN


ARREGLAR_UNIDADES:
    INC W2,W2
    DEC RESPUESTA,RESPUESTA
    BRA UNIDADES
ARREGLAR_DECENAS: 
    INC W3,W3
    SUB RESPUESTA,W2,RESPUESTA
    BRA DECENAS 
ARREGLAR_CENTENAS:
    INC W4,W4
    SUB RESPUESTA,W2,RESPUESTA
    BRA CENTENAS 
ARREGLAR_MILES:
    INC W5,W5
    SUB RESPUESTA,W2,RESPUESTA
    BRA MILES 
ARREGLAR_DECENAS_DE_MIL:
    INC W6,W6
    SUB RESPUESTA,W2,RESPUESTA
    SUBB #0,RESPUESTAH
    BRA DECENAS_DE_MIL 
ARREGLAR_CENTENAS_DE_MIL:
    INC W7,W7
    SUB RESPUESTA,W2,RESPUESTA
    SUBB #1,RESPUESTAH
    BRA CENTENAS_DE_MIL  
    
    
LECTURA_DISP:
    
    CLR W1
    CLR W2
    MOV #0X000F,W3

    
    MOV #0X00E0,W0
    MOV W0,LATB
    NOP
    MOV PORTB,W0
    AND W0,W3,W0
    BTSS W0,#0
    MOV #1,W1
    BTSS W0,#1
    MOV #4,W1
    BTSS W0,#2
    MOV #7,W1
    BTSS W0,#3
    MOV #'*',W2
    
    MOV #0X00D0,W0
    MOV W0,LATB
    NOP
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
    
    MOV #0X00B0,W0
    MOV W0,LATB
    NOP
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
    
    MOV #0X0070,W0
    MOV W0,LATB
    NOP
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
    BRA NZ, BORRANDO
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
;    IMP_COT #0x0006
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
    

;***************************End of All Code Sections****************************
.end                               ;End of program code in this file
