;*******************************************************************************
;                                                                              *
;    Filename:  main.s                                                  *
;    Date:      06/09/2016                                                     *
;    File Version: v1                                                          *
;    Author:    	Nicolás Mosquera S                                         *
;    Company:   	Escuela Colombiana de Ingebieria                           *
;    Description:  ejemplo timer interrupt                                                 *
;                                                                              *
;*******************************************************************************

;*******************************************************************************
; Processor Inclusion
;*******************************************************************************

.equ __33FJ128MC802, 1 			;select the 33FJ128MC802 as processor
; include the processor definitions
;.include "xc.inc" 				;generic definition.
.include "p33FJ128MC802.inc"			 

;*******************************************************************************
; Configuration Word Setup
;*******************************************************************************

config __FOSCSEL, FNOSC_FRC & IESO_ON ; FRC Oscillator at start-up then switch to Internal Fast RC (FRC)
config __FOSC, FCKSM_CSECMD & OSCIOFNC_ON  & POSCMD_NONE    ;Clock Switching is enabled and Fail Safe Clock Monitor is disabled
							    ;OSC2 Pin Function: OSC2 digital I/O function
							    ;Primary Oscillator DisabledClock Switching is enabled and Fail Safe Clock Monitor is disabled
config __FWDT, FWDTEN_OFF		                    ;Watchdog timer enabled/disabled by user software

config __FICD, ICS_PGD1 & JTAGEN_OFF	;Communicate on PGC1/EMUC1 and PGD1/EMUD1
					;JTAG is Disabled		 
			 
;*******************************************************************************
;Program Specific Constants
;*******************************************************************************

;procressor constants					
.equ Fosc, 7370000	;FRC Frecuency
.equ PLL,   1					
.equ Fcy, (Fosc*PLL/2)	;Instruction Frecuency 	
;					
;;Timer Constants					
.equ FREQ_T1,		1000	;F =(1/T)=1kHz T=1ms 
.equ T1_PRESCALER,	1	; Preescaler 8
.equ TIMER1_PERIOD,	(Fcy / (T1_PRESCALER * FREQ_T1)) - 1;  46061	
					
;*******************************************************************************
;Global Declarations:
;*******************************************************************************

.global _main            ;The label for the first line of code. If the
			 ;assembler encounters "_main", it invokes the
			 ;start-up code that initializes data sections

.global __T1Interrupt    ;Declare Timer 1 ISR name global
			 
.global __DefaultInterrupt ;

;*******************************************************************************
;Constants stored in Program space & progrm memory
;*******************************************************************************
.data
cont: .int 0
;*******************************************************************************
;Code Section in Program Memory
;*******************************************************************************

.text 

_main:
    CALL wreg_init ;Call _wreg_init subroutine
    call config_IO
    call config_TMR1
loop:	
    call proc_async
    BRA loop

config_IO:	
    SETM ADPCFG
    MOV #0xFFEF, W0	    ;PortB (1 - input, 0 - output) // b4 and b5 as out
    MOV W0,TRISB		
    RETURN
config_TMR1:
    ; Se asigna la prioridad por defecto.
    MOV #0x8000, W0		;Timer1 w/ prescaler 1:8
    MOV W0, T1CON
    MOV #TIMER1_PERIOD, W0  ;Timer1 period
    MOV W0, PR1
    CLR TMR1
    BCLR IFS0, #T1IF	;3) Clear Timer 1 interrupt flag
    BSET IEC0, #T1IE	;4) Enable Timer 1 interrupt
    BSET T1CON, #TON
    RETURN
reinicio:
    BTG LATB, #RB4		; Toggle al bit de salida hacia el LED.
    CLR cont			; Reinicia la variable en memoria.
    RETURN
proc_async:
    MOV cont, W0		; Mueve la variable en memoria cont a W0.
    MOV #100 ,W1		; Luego si ya ha llegado a 100 va a reinicio
    CPSNE W0, W1		; hace el Toggle del LED y reinicia el cont.
    CALL reinicio
    RETURN
wreg_init:
    CLR W0			; Subrutina que reinicia todos los registros
    MOV W0, W14			; de trabajo (WREG0-WREG14)
    REPEAT #12
    MOV W0, [++W14]
    CLR W14
    RETURN		
;*******************************************************************************
;    Interrupt Service Routines
;*******************************************************************************
__T1Interrupt:
    BCLR IFS0, #T1IF           ;Clear the Timer1 Interrupt flag Status bit.
    INC cont			; Incrementa el contador.
    RETFIE                     ;Return from Interrupt Service routine
;***************************End of All Code Sections****************************
.end                               ;End of program code in this file


