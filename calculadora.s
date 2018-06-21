
;*******************************************************************************
;                                                                              *
;    Filename:  calculadora_news.s                                             *
;    Date:      21/06/2018                                                     *
;    File Version: v1                                                          *
;    Author:    	Andres Moreno, Nicolas Roldan, Natalia Suarez          *
;    Company:   	Escuela Colombiana de Ingeniería Julio Garavito        *
;    Description:  Calculadora en assembler de 2 numeros de 3 digitos sin signo*
;                  Se usa el teclado matricial 4*4 donde las teclas            *
;		   A,B,C,D,#,*  seran suma,resta,multiplicacion,división,igual *
;		   y C/CE respectivamente.				       *
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
config __FWDT, FWDTEN_OFF	; Deshabilitar modulo wathdog para que no se
				; reinicie el dsPIC luego de un tiempo.
;config __FICD, ICS_PGD2 & JTAGEN_OFF	; Simular en caliente (con las entradas 
					; desde el dsPIC sin stimulus).
    
;*******************************************************************************
; Macros
;*******************************************************************************
;***LCD_WRITE_DATA***
.macro IMP_CHAR LETRA
    BSET LCD_control_port,#LCD_RS
    BCLR LCD_control_port,#LCD_RW
    MOV \LETRA,W0
    MOV W0,W1
    ;***NIBBLE MÁS SIGNIFICATIVO***
    AND #0x00F0,W1		; valor para la mascara
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
    IMP_COT #0x18		; Cursor/Shift Display
    CALL delay_1s
.endm

.macro IMP_NUM NUMERO
    BSET LCD_control_port,#LCD_RS
    BCLR LCD_control_port,#LCD_RW
    MOV #0X0300,W0;*** El nibble más significativo siempre es 3***
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
;***ADDRESS SET***  
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
;***************************************************************
;***Constantes***
.equ LCD_EN, RA0
.equ LCD_RS, RA1
.equ LCD_RW, RA2
.equ LCD_control_port, LATA
.equ LCD_data_port, LATB
.equ AA,W4;
.equ BB,W6;
.equ BBH,W7
.equ RESPDEC,W8
.equ RESPDECH,W9
.equ RESPUESTA,W10
.equ RESPUESTAH,W11
.equ CHAR_OP,W12
.equ BANDERA,W13
.equ CONTADOR,W14	    ; Contador para # de números A y B
.equ OP_OK,0
.equ AA_BB_OK,1
.equ FINISH,2
.equ numeneg,3
.equ RESP_CEROS,4  
.equ AAXD,5

;Constantes para los delays
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
    ;**********Configuración de las entradas y salidas*************
    ;LCD
    MOV #0xFFF8,W0		; Control del LCD e interruptor.
    MOV W0,TRISA
    ;LCD data (RB11-RB8) y teclado (RB7-RB0)
    MOV #0xF00F,W0
    MOV W0,TRISB
    SETM AD1PCFGL		; Configuración de entradas como digitales
    ;***CN4-CN7***
    MOV #0x00F0,W0
    MOV W0,CNPU1		; Pull-up activados.
    MOV W0,CNEN1		; Habilitación de los pins interrupt enable.
    
    CALL init_LCD		; Inicialización del LCD.
    CALL LCD_reset		; Reinicio del LCD.
    CLR CONTADOR		; Reinicio de los WREG
    
    BTSC PORTA,#3		; Omite los mensajes si el interruptor
    BRA LOOP			; está encendido.
    ;***Mensaje***
    CALL mensaje		; Muestra el mensaje estático
    CALL delay_2s		; por 2 segundos.
    CALL LCD_reset		; CLR display.
    CALL mensaje2		; 
    CALL delay_1s		; Muestra el mensaje por 1 segundo
    MOV #80,W3			; para luego rotarlo 80 veces.
ROT:
    ROTAR
    DEC W3,W3
    BRA NZ,ROT
    CALL delay_2s		; Muestra el mensaje por 2 segundos y
    CALL LCD_reset		; CLR display.
    
    
LOOP:
    CLR LATB
    BCLR IFS1,#CNIF		; Reinicia bit de interrupción
SLEEEP:
    BTSS IFS1,#CNIF
    BRA SLEEEP			; Espera hasta que haya un cambio (tecla pulsada).
    CALL delay_10ms;
    CALL LECTURA_DISP;		; W1:números,W2:CHAR
    
    MOV #'*',W0			; Verifica si se ha hecho un C/CE
    CP W2,W0			; y acorde a ello reinicia los WREG.
    BRA Z,REINICIO		;
    
    BTSC BANDERA,#FINISH	; Si está en SET ya hizo la operación
    BRA REINICIO		; por ende, reinicia (borra el display y WREG.)
    
    CP0 W2			; Si está en cero es porque lo han reiniciado.
    
    BRA NZ,GOP			; Salta si han ingresado por lo menos 1 número,
				; a ejecutar la operación.
    BRA NUMERO			; De otra forma, va a 

;*******************************************************************************
;Subroutines
;*******************************************************************************
GOP:
    MOV #'=',W0			; Va a ejecutar la operación sólo sí se ha
    CP W0,W2			; ingresado un =, de otra forma, guarda la  
    BRA Z, OPERACION		; operación a realizar en CHAR_OP.
    
    BTSC BANDERA,#OP_OK		; Si ya se ingreso la operación, se va esperar
    BRA ANTIRREBOTE		; a que ingresen algo diferente de char(+,-,/,*).
				
    CLR CONTADOR		; Reinicio del contador de los números
				; que han sido ingresados para el B (segundo).
				
    MOV W2,CHAR_OP		; Guarda la operación en CHAR_OP.
    BSET BANDERA,#OP_OK		; Ya se ha ingresado una operación.
    BCLR BANDERA,#AA_BB_OK	; 
    IMP_CHAR CHAR_OP		; Imprime en el LCD el símbolo de la operación.
    BRA ANTIRREBOTE		; Espera a que dejen de oprimir y luego
				; a que ingresen algo de nuevo.

OPERACION:
    BSET BANDERA,#FINISH	; La operación ya ha sido realizada.
    
    CP0 CHAR_OP			; Revisa el registro que guarda la operación.
    BRA Z,IGUAL			; Si es 0,imprime los digitos de A que ya hayan
				; sido ingresados.
    
    CP0 CONTADOR		; Si han ingresado una operación primero,
    BRA Z,SYNTAX_ERROR		;
    
    MOV #'+',W0			; Va y realiza la suma.
    CP W0,CHAR_OP
    BRA Z,SUMA
    
    MOV #'-',W0			; Va y realiza la resta.
    CP W0,CHAR_OP
    BRA Z,RESTA
    
    MOV #'x',W0			; Va y realiza la multiplicación
    CP W0,CHAR_OP
    BRA Z,MULTI
    
    MOV #'/',W0			; Va y realiza la división.
    CP W0,CHAR_OP
    BRA Z,DIVI
    
    
;***** SUBRUTINAS PARA LAS OPERACIONES *******    
SUMA:
    ADD AA,BB,RESPUESTA		; Suma del primer y segundo número, AA y BB.
    CALL LINEA2			; Colocar el cursor en la segunda línea.
    CALL CONV_BCD		; 
    BRA ANTIRREBOTE
RESTA:
    SUB AA,BB,RESPUESTA		; Resta del primer y segundo número, AA y BB. 
    
    BTSC SR,#N			; Verifica si el número es negativo.
    BSET BANDERA,#numeneg	; Si es negativo, coloca en SET la #numeneg
    BTSC BANDERA,#numeneg	; Dado el caso de ser negativo, imprime "-"
    CALL NUMNEG			; y calcula el complemento a 2.
    
    BTSS BANDERA,#numeneg	; Sino fue negativo, la respuesta se mantiene
    CALL LINEA2			; y es impresa en la segunda línea.
    CALL CONV_BCD
    BRA ANTIRREBOTE
NUMNEG:
    CALL LINEA2			; Va a la segunda línea del LCD e imprime en 
    IMP_CHAR #'-'		; primer lugar "-".
    ;**COMPLEMENTO A 2**
    COM RESPUESTA,RESPUESTA	; Complemento a 1.
    INC RESPUESTA,RESPUESTA	; Complemento a 2.
    ;**********************
    RETURN
MULTI:
    MUL.UU AA,BB,RESPUESTA	; Multiplicación entre enteros unsigned.
				; El resultado de 32 bits es guardado en
				; registros sucesivos RESPUESTA(LSW) 
				; y RESPUESTA+1 (MSW) o RESPUESTAH.
    CALL LINEA2			; Va a la segunda linea e imprime.
    CALL CONV_BCD
    BRA ANTIRREBOTE
DIVI:
    CP0 BB			; Si el segundo número es 0,
    BRA Z,MATH_ERROR		; imprime MATH ERROR
    
    REPEAT #17			; División iterativa.
    DIV.U AA,BB			; Cociente -> W0, Residuo -> W1.
    MOV W0,RESPUESTA
    ; PARTE DECIMAL
    MOV #1000,W0		; Multiplica el residuo por #1000
    MUL.UU W1,W0,AA		; y lo guarda en AA (LSW) y en BB (MSW).
    
    REPEAT #17			; Realiza de nuevo la división iterativa.
    DIV.U AA,BB			; MSW/LSW
    MOV W0,RESPDEC		; Guarda la parte decimal.
    CALL LINEA2			; Va a la segunda línea e imprime.
    CALL CONV_BCD
    IMP_CHAR #','		;
    ;SE VA A GUARDAR EN W2 DECIMAS,W3 CENTESIMAS,W4 MILESIMAS
    CLR W4			    ; 
    CLR W3			    ;
    MOV #0x0064,W2		    ; 100 en decimal.
DECIMAS:
    CP RESPDEC,W2		    ; Compara con 100.
    BRA C,ARREGLAR_DECIMAS	    ; Si el carry = 1, le suma 1 al acumulador
				    ; de decimas (W4) y le resta #100 a RESPDEC.
				    ; hasta que carry sea 0.
    MOV #0X000A,W2		    ; 10 en decimal.
CENTESIMAS: 
    CP RESPDEC,W2		    ; Compara con #10.
    BRA C,ARREGLAR_CENTESIMAS	    ; Si el carry = 1, le suma 1 al acumulador
    CLR W2			    ; de centesimas (W3) y le resta #10 a RESPDEC
				    ; hasta que carry sea 0.
MILESIMAS:
    CP RESPDEC,#0X0001		    ; Compara con 1.
    BRA C,ARREGLAR_MILESIMAS	    ; Si el carry = 1, le suma 1 al acumulador
    BRA IMPDECIMAS		    ; de centesimas (W2) y le resta #10 a RESPDEC
    
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
    ; IMPRIME LOS ACUMULADORES EN ORDEN (DECIMAS CENTESIMAS MILESIMAS)
    IMP_NUM W4			    ; Decimas.	    
    IMP_NUM W3			    ; Centesimas.
    IMP_NUM W2			    ; Milesimas.
    BRA ANTIRREBOTE
;*********************************************
IGUAL:
    CP0 CONTADOR		    ; Si no han ingresado un número, sigue
    BRA Z,ANTIRREBOTE		    ; esperando a que lo ingresen.
    
    MOV AA,RESPUESTA		    ; Si ya lo ingresaron, lo imprime.
    CALL LINEA2			    
    CALL CONV_BCD
    BRA ANTIRREBOTE
  
NUMERO: 
    BTSC BANDERA,#AA_BB_OK	    ; Verifica 2 banderas: Sí 3 digitos no han
    BRA	 ANTIRREBOTE		    ; sido ingresados, va a esperar a que 
    BTSC BANDERA,#OP_OK		    ; ingresen por lo menos 3, caso contrario 
    BRA NUMB			    ; (ya los ingresaron), verifica si han 
				    ; ingresado la operación,y va a ordenar el
				    ; segundo número, B, en NUMB, de otra forma
				    ; aún deben estar ingresando B.
				    
    MUL.UU AA,#10,AA		    ; Multiplica lo que haya en ese momento en
				    ; AA, ya sea que no hayan ingresando
				    ; un número, o que ya vayan 2 o 3.
				    ; AA es el acumulador del número de 3 cifras
				    ; como máximo.
				    
    ADD W1,AA,AA		    ; Luego, para ordenar unidades, decenas y
				    ; centenas, acorde al orden en que hayan
				    ; sido ingresadas, se suma el número que
				    ; acaben de ingresar con el acumulador.
				    
    INC CONTADOR,CONTADOR	    ; Se incrementa el contador de digitos.
    CP CONTADOR,#3		    ; Si llega a 3, la bandera que verifica 
    BRA Z, BANDERA_ON		    ; si han ingresado 3 números se pone SET
    BRA IMPRIMIR_NUM		    ; e imprime el número. De otra forma,
				    ; el número simplemente se imprime.
				    
;**** Ingreso de 3 digitos e impresión del número****
BANDERA_ON:
    BSET BANDERA,#AA_BB_OK
IMPRIMIR_NUM:
    IMP_NUM W1
    BRA ANTIRREBOTE
;**************************************************

;*******SUBRUTINA PARA GUARDAR E IMPRIMIR EL SEGUNDO NÚMERO B******
NUMB:
    MUL.UU BB,#10,BB
    ADD W1,BB,BB
    INC CONTADOR,CONTADOR
    CP CONTADOR,#3
    BRA Z, BANDERA_ON
    BRA IMPRIMIR_NUM
;****************************************************************

;**** SUBRUTINA PARA ESPERAR A QUE EL USUARIO DEJE DE PRESIONAR EL TECLADO****
ANTIRREBOTE:    
    CLR LATB		    ; Coloca en 0 las salidas hacia el teclado.
WAIT_ANTIREBOTE:
    CALL delay_10ms
    CALL delay_10ms
    MOV PORTB,W0	    ; Lee las entradas del teclado
    MOV #0X000F,W1	    ; el nibble menos significativo (RB4-RB0)
    AND W1,W0,W0
    CP W1,W0		    ; Si da cero, es que no han presionado nada y
    BRA NZ, WAIT_ANTIREBOTE ; espera por si siguen oprimiendo.
    BRA LOOP		    ; Sale y espera a que alguien lo oprima de nuevo.
			    ; Resetea: IFS1,salidas al TECLADO.
			    
;********************************************************************
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

; Conversión a BCD
;**************************************************************************
;se usa el algoritmo Conversión de fuerza bruta,este VA REALIZANDO UNA 
;DIVISIÓN EN BASE 10.  
;SE GUARDAN: W2 UNIDADES,W3 DECENAS,W4 CENTENAS,W5 MILESIMAS, W6 DECENAS DE MIL,W7 CENTENAS DE MIL
    
CONV_BCD:
    MOV #14,W0			; Dirección de W7 (0x0814)
CLR_REG_BCD:
    CLR [W0]			; Reinicia los WREG (W7 a W0).
    DEC2 W0,W0
    BRA NZ, CLR_REG_BCD	    
    MOV #0X86A0,W2		;  
CENTENAS_DE_MIL:
    CP RESPUESTA,W2		; 
    CPB RESPUESTAH,#1		; Compara con 1 con el Borrow.
    BRA C ,ARREGLAR_CENTENAS_DE_MIL; 
    MOV #0X2710,W2		; 
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
    CP0 W7			; Verifica que haya centenas de mil.
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
    BCLR IFS1,#CNIF;Reinicia el bit
    MOV #0,W1;Para guardar los números.
    MOV #0,W2;Para guardar los simbólos.
    MOV #0X000F,W3
;***BARRIDO***
    ;***PRIMERA COLUMNA***
    MOV #0X00E0,W0
    MOV W0,LATB
    NOP
    MOV PORTB,W0	    ; Lectura de las entradas desde el teclado
    AND W0,W3,W0	    ; de acuerdo a lo que haya sido pulsado.
    BTSS W0,#0
    MOV #1,W1
    BTSS W0,#1
    MOV #4,W1
    BTSS W0,#2
    MOV #7,W1
    BTSS W0,#3
    MOV #'*',W2
    ;***SEGUNDA COLUMNA***    
    MOV #0X00D0,W0;
    MOV W0,LATB
    NOP			    ; Tiempo de espera necesario entre Read y Write.
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
    ;***TERCERA COLUMNA***    
    MOV #0X00B0,W0
    MOV W0,LATB
    NOP			    ; Tiempo de espera necesario entre Read y Write.
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
    ;***CUARTA COLUMNA***    
    MOV #0X0070,W0
    MOV W0,LATB
    NOP			    ; Tiempo de espera necesario entre Read y Write.
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

;************** SUBRUTINA PARA REINICIAR TODOS LOS WREG **************
REINICIO:
    MOV #28,W0
BORRANDO:
    CLR [W0]
    DEC2 W0,W0
    BRA NZ, BORRANDO
    CLR W0
    CALL LCD_reset		; BORRAR DISPLAY
    BRA ANTIRREBOTE;	    
;*****************************************
    
    
;**********RUTINAS DE INICIALIZACIÓN Y ENVIO DE MENSAJES AL LCD****************
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
    IMP_COT #0x0006
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


