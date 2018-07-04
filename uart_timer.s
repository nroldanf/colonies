;*******************************************************************************
; Inclusión del procesador (DSC o MCU)
;*******************************************************************************
.include "P33FJ128MC802.inc"
.equ __33FJ128MC802,1
;*******************************************************************************
; Configuration Word Setup
;*******************************************************************************
config __FOSC, OSCIOFNC_ON
config __FWDT, FWDTEN_OFF	; Deshabilitar modulo wathdog
;*******************************************************************************
;Global Declarations:
;*******************************************************************************
.global _main
;.global __T1Interrupt    ;Declare Timer 1 ISR name global
;.global __reset		 ; resest vector			 
;.global __DefaultInterrupt ;
    
;*******************************************************************************
;Constants stored in Program space & progrm memory
;*******************************************************************************
;.section .pbss,persist ; persistent data storage
;count: .space 2 ; count of unexpected interrupts
;.global FaultCount ; is not affected by reset
;FaultCount: .space 2 ; count of unexpected interrupts
;*******************************************************************************
; Constantes y variables en memoria
;*******************************************************************************
;.equ K1, 1227	    	;Delay constant 1mS
;.equ K2, 249		;Delay constant 20mS
;;procressor constants					
;.equ Fosc, 7370000	;FRC Frecuency
;.equ PLL,   1					
;.equ Fcy, (Fosc*PLL/2)	;Instruction Frecuency 	
;;Timer Constants					
;.equ FREQ_T1,		1	;F =(1/T)=1kHz T=1ms 
;.equ T1_PRESCALER,	64	; Preescaler 8
;.equ TIMER1_PERIOD,	(Fcy / (T1_PRESCALER * FREQ_T1)) - 1;  46061	
;*******************************************************************************
;Code Section in Program Memory
;*******************************************************************************
.text

_main:
    CALL config_IO
    call config_U1
loop:
    call rx_dato
    call tx_dato
    bra loop
config_IO:
    SETM AD1PCFGL		; Pines analogos como digitales.
    MOV #0xFF7F,W0		; Rx: RB6, Tx: RB7
    MOV W0,TRISB
    ; Desbloqueo del periferico (IOLOCK = 0)
    MOV #0xBF,W0
    AND OSCCONL; Byte menos significativo
    NOP			    ; Espera según el datasheet
    NOP
    ;Remapeo de la entrada (Rx)
    MOV #0x1F06,W0
    MOV W0,RPINR18
    ;Remapeo de las salidas (Tx)
    MOV #0x0300,W0
    IOR RPOR3
    
    ;Bloqueo (IOLOCK = 1 )
    MOV #0x40,W0
    IOR OSCCONL
    NOP			    ; Espera según el datasheet
    NOP
    
    RETURN 

config_U1:
    ; Configuración de módulo UART
    MOV #0xA008,W0		; Registro de modo (Bit de Alta velocidad en SET)
    MOV W0,U1MODE		; 8N1
    MOV #0x0400,W0		; Registro de estado y control.
    MOV W0,U1STA		; 
    MOV #2,W0			; Configuración del Baud Rate (Generator)
    MOV W0,U1BRG		; U1BRG = (Fcy/(4*Baud Rate)) - 1 
				; 4: High V. 16: Normal
    RETURN
    
rx_dato:
    NOP				; Retardo
    BTSS U1STA,#URXDA		; ¿Ya hay disponible un bit?
    BRA rx_dato			; ¿Sí?, reciba, sino quedese esperando.
    ;
    MOV U1RXREG,W1		; Lee el registro FIFO
    BCLR U1STA,#URXDA	; Limpie la bandera
    RETURN
tx_dato:
    NOP						; Retardo
    BTSC U1STA,#UTXBF		; ¿Buffer de transmisión vacio?
    BRA tx_dato				; ¿No?, siga transmitiendo hasta que este vacio
    MOV W1,U1TXREG			; ¿Sí?, mueva el dato que se va a transmitir
    
    RETURN			

.end
    