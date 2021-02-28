sr        =   44100
kr        =   4410
ksmps     =   10
nchnls    =   2

;-----------------------------------------------
; Instruments 0 - 99 define a note created by adding 1 or more waveforms
;
; p4  : AMPLITUDE
; p5  : FREQUENCY
; p6  : WAVE FUNCTION
; p7  : ATTACK
; p8  : DECAY
; p9  : SUSTAIN
; p10 : RELEASE
;
; Example:
; f1 0 8192 10 1 
; \
;  \ \
;     \ \
;        \
; f2 0 1024  7  1 341 0 1  0.5 341 -0.5 1  0 340 -1
; __/\__
;       \/
;
; f3 0 1024  7  0 256 0 128  1 128 0 256  0 128 -1 128  0
;   _   _
; _| |_| |_
;         |_|
; f4 0 1024  7  0 300 0 1  1 40 1 1  0 300 0 1  1 39 1 1  0 300 0 1  -1 40 -1
;   _
; _| |_
;      \
; f5 0 1024  7  0 256 0 1  1 128 1 1  0 256 0 384  -1
;              p3  p4    p5      p6    p7    p8     p9    p10
; INSTR START  DUR AMP   FREQ    WAVE  ATT   DEC   SUS   REL
; i1    0.00   0.5 10000 111.90  1     0.10  0.13  0.32  0.200
;-----------------------------------------------

        instr      1
iatt1  = p7
idec1  = p8  
islev1 = p9
irel1  = p10
kenv1    adsr iatt1, idec1, islev1, irel1
a1       oscil    p4*kenv1, p5, p6
           out      a1, a1
        endin

        instr      2
iatt2  = p7
idec2  = p8  
islev2 = p9
irel2  = p10
kenv2    adsr iatt2, idec2, islev2, irel2
a2       oscil    p4*kenv2, p5, p6
           out      a2, a2
        endin

        instr      3
iatt3  = p7
idec3  = p8  
islev3 = p9
irel3  = p10
kenv3    adsr iatt3, idec3, islev3, irel3
a3       oscil    p4*kenv3, p5, p6
           out      a3, a3
        endin

        instr      4
iatt4  = p7
idec4  = p8  
islev4 = p9
irel4  = p10
kenv4    adsr iatt4, idec4, islev4, irel4
a4       oscil    p4*kenv4, p5, p6
           out      a4, a4
        endin

        instr      5
iatt5  = p7
idec5  = p8  
islev5 = p9
irel5  = p10
kenv5    adsr iatt5, idec5, islev5, irel5
a5       oscil    p4*kenv5, p5, p6
           out      a5, a5
        endin

        instr      6
iatt6  = p7
idec6  = p8  
islev6 = p9
irel6  = p10
kenv6    adsr iatt6, idec6, islev6, irel6
a6       oscil    p4*kenv6, p5, p6
           out      a6, a6
        endin

        instr      7
iatt7  = p7
idec7  = p8  
islev7 = p9
irel7  = p10
kenv7    mxadsr iatt7, idec7, islev7, irel7
a7       oscil    p4*kenv7, p5, p6
           out      a7, a7 * 0.1
        endin

        instr      8
iatt8  = p7
idec8  = p8  
islev8 = p9
irel8  = p10
kenv8    adsr iatt8, idec8, islev8, irel8
a8       oscil    p4*kenv8, p5, p6
           out      a8 * 0.1, a8
        endin

        instr      9
iatt9  = p7
idec9  = p8  
islev9 = p9
irel9  = p10
kenv9    adsr iatt9, idec9, islev9, irel9
a9       oscil    p4*kenv9, p5, p6
           out      a9, a9 * 0.1
        endin

        instr      10
iatt10  = p7
idec10  = p8  
islev10 = p9
irel10  = p10
kenv10    adsr iatt10, idec10, islev10, irel10
a10       oscil    p4*kenv10, p5, p6
           out      a10 * 0.1, a10
        endin

        instr      11
iatt11  = p7
idec11  = p8  
islev11 = p9
irel11  = p10
kenv11    adsr iatt11, idec11, islev11, irel11
a11       oscil    p4*kenv11, p5, p6
           out      a11, a11
        endin

        instr      12
iatt12  = p7
idec12  = p8  
islev12 = p9
irel12  = p10
kenv12    adsr iatt12, idec12, islev12, irel12
a12       oscil    p4*kenv12, p5, p6
           out      a12, a12
        endin

        instr      13
iatt13  = p7
idec13  = p8  
islev13 = p9
irel13  = p10
kenv13    adsr iatt13, idec13, islev13, irel13
a13       oscil    p4*kenv13, p5, p6
           out      a13, a13
        endin

        instr      14
iatt14  = p7
idec14  = p8  
islev14 = p9
irel14  = p10
kenv14    adsr iatt14, idec14, islev14, irel14
a14       oscil    p4*kenv14, p5, p6
           out      a14, a14
        endin

        instr      15
iatt15  = p7
idec15  = p8  
islev15 = p9
irel15  = p10
kenv15    adsr iatt15, idec15, islev15, irel15
a15       oscil    p4*kenv15, p5, p6
           out      a15, a15
        endin

        instr      16
iatt16  = p7
idec16  = p8  
islev16 = p9
irel16  = p10
kenv16    adsr iatt16, idec16, islev16, irel16
a16       oscil    p4*kenv16, p5, p6
           out      a16, a16
        endin

        instr      17
iatt17  = p7
idec17  = p8  
islev17 = p9
irel17  = p10
kenv17    adsr iatt17, idec17, islev17, irel17
a17       oscil    p4*kenv17, p5, p6
           out      a17, a17
        endin

        instr      18
iatt18  = p7
idec18  = p8  
islev18 = p9
irel18  = p10
kenv18    adsr iatt18, idec18, islev18, irel18
a18       oscil    p4*kenv18, p5, p6
           out      a18, a18
        endin

        instr      19
iatt19  = p7
idec19  = p8  
islev19 = p9
irel19  = p10
kenv19    adsr iatt19, idec19, islev19, irel19
a19       oscil    p4*kenv19, p5, p6
           out      a19, a19
        endin

        instr      20
iatt20  = p7
idec20  = p8  
islev20 = p9
irel20  = p10
kenv20    adsr iatt20, idec20, islev20, irel20
a20       oscil    p4*kenv20, p5, p6
           out      a20, a20
        endin

;-----------------------------------------------
; Instruments 100 - 199 use a modulator against a carrier frequency
; for Frequency Modulation (FM)
;
; p4  : AMPLITUDE IN DECIBELS
; p5  : FREQUENCY
; p6  : CARRIER WAVE FUNCTION
; p7  : MODULATOR FREQUENCY (VERY LOW)
; p8  : LOW SIDEBAND
; p9  : HIGH SIDEBAND
; p10 : INITIAL PHASE OF WAVEFORM
;
; Example:
; f1 0 16384 10 1
;              p3   p4   p5   p6   p7     p8   p9   p10
; INSTR START  DUR  AMP  FREQ WAVE MFREQ  LSB  HSB  IPHS
; i100  0      9.5  0.6  440  1    0.04   0    10   0.3
;-----------------------------------------------

        instr      100
ka100   = dbamp(p4)
kamp100 = ka100 * (ka100 * 0.5)
kcps100 = p5
ifn100  = p6
kmod100 = p7
;INTENSITY SIDEBANDS
kndx100 line p8, p3, p9
iphs100 = p10
kenv100  adsr  0.01, 1.0, 1.0, 0.1
asig foscili kenv100 *kamp100, kcps100, 1, kmod100, kndx100, ifn100, iphs100
     outs asig, asig
endin

        instr      101
kamp101 = dbamp(p4) ^ 2
;ka101   = dbamp(p4)
;kamp101 = ka101 * (ka101 * 0.5)
kcps101 = p5
ifn101  = p6
kmod101 = p7
;INTENSITY SIDEBANDS
kndx101 line p8, p3, p9
iphs101 = p10
kenv101  adsr  0.01, 1.0, 1.0, 0.1
asig foscili kenv101 *kamp101, kcps101, 1, kmod101, kndx101, ifn101, iphs101
     outs asig, asig
endin



;-----------------------------------------------
; Instruments 200 - 299 use a modulator against a carrier frequency
; for Amplitude Modulation (AM)
;
; p4  : AMPLITUDE
; p5  : CARRIER FREQUENCY
; p6  : CARRIER WAVE FUNCTION
; p7  : MODULATOR FREQUENCY 
; p8  : MODULATOR WAVE FUNCTION
; p9  : ATTACK
; p10 : DECAY
;
; Example:
; f1 0 8192 10 1 
; MODULATOR WAVEFORM
; ,-'`-.
;       `-'`-.-.
;               `-'`-.        .-
;                     `-'`\__/
; f2 0 8192 10 1 .8 .7 .6 .5
;              p3  p4     p5    p6    p7     p8    p9   p10
; INSTR START  DUR AMP    FREQ  WAVE  MFREQ  MFUNC ATT  DEC
; i200  0      2   15000  300   1     300    2     0.3  0.4
;-----------------------------------------------

        instr      200
kenv200    linen   p4,p9,p3,p10
; CARRIER
acarr200   oscil   1,p5,p6
; MODULATOR
amod200    oscil   1,p7,p8
aoutm200   =       acarr200*amod200
           out     kenv200*aoutm200, kenv200*aoutm200
           endin

        instr      201
kenv201    linen   p4,p9,p3,p10
; CARRIER
acarr201   oscil   1,p5,p6
; MODULATOR
amod201    oscil   1,p7,p8
aoutm201   =       acarr201*amod201
           out     kenv201*aoutm201, kenv201*aoutm201
           endin


;-----------------------------------------------
; Instruments 300 - 399 use a modulator against a carrier frequency
; for Waveshaping
;
; p4  : AMPLITUDE
; p5  : FREQUENCY
; p6  : CARRIER WAVE FUNCTION 
; p7  : WAVESHAPING FUNCTION
; p8  : ATTACK   
; p9  : DECAY    
;
; Example:
; f1 0 8192 10 1 
; NO DISTORTION (LINEAR)
;   /
;  /
; /
; f2 0 8192 7 -1 8192  1
; CLOSE TO LINEAR FUNCTION (SECOND HALF OF COSINE)
;         __
;       -
;     /
; __-
; f3 0 8192 9 0.5 1 270
; HEAVIER DISTORTION (DISCONTINUOUS FUNCTION)
;             ----
;     `-._   _
;         .-'
; ----
; f4 0 8192 7 -1 2048 -1 0 0.3 2048 0 0 -0.5 2048 0 0 0.8 2048 0.8
;              p3   p4    p5    p6   p7     p8     p9
; INSTR START  DUR  AMP   FREQ  WAVE WSHAPE ATTACK DECAY
; i300  0      1    20000 440   1    2      0.1    0.2
; i300  1.5    1    .     .     1    3      0.1    0.3
; i300  3      1    .     .     1    4      0.4    0.1
;-----------------------------------------------

        instr      300
ioff300 =       ftlen(p7)/2-1
kenv300 linen   p4, p8, p3, p9
ain300  oscil   ioff300, p5, p6
; WAVESHAPING VALUE
awsh300 tablei  ain300,p7,0,ioff300
        out     kenv300*awsh300, kenv300*awsh300
        endin

        instr      301
ioff301 =       ftlen(p7)/2-1
kenv301 linen   p4, p8, p3, p9
ain301  oscil   ioff301, p5, p6
; WAVESHAPING VALUE
awsh301 tablei  ain301,p7,0,ioff301
        out     kenv301*awsh301, kenv301*awsh301
        endin


;-----------------------------------------------
; Instruments 400 - 499 use 2 modulators against a carrier frequency
; for Waveshaping
;
; p4  : AMPLITUDE
; p5  : FREQUENCY
; p6  : CARRIER WAVE FUNCTION 
; p7  : WAVESHAPING FUNCTION
; p8  : ENVELOPE (DISTORTION INDEX) FUNCTION
; p9  : OFFSET
; p10 : PROPORTION OF BEATING OSCILLATOR
; p11 : PROPORTION OF NON-BEATING OSCILLATOR
;
; Example:
; f1  0 8192  10 1 
; WAVESHAPER     
; -.
;   `-__--.
;          `\_/
; f2  0 8192  13 0.5 1 0 1 .7 .8 .3 .1 .8 .9 1 1
; DISTORTION INDEX FUNCTION (ENVELOPE)
;       .-'`--..__..__
;    .-'              `-.
; .-'                    `-._
; f3  0 512   7 0 96 1 96 .8 96 .84 96  0.77 32  0.6 96  0
;    /'`-.-._
;   /        ``--..__
; ./                 ``--._
; f4  0 512   7 0 32 1 32 .8 64 .9  128 0.6  128 0.4 100 0.25 28 0
;              p3    p4    p5    p6   p7     p8    p9     p10   p11
; INSTR START  DUR   AMP   FREQ  WAVE WSHAPE ENV   OFFSET BEAT  NO-BEAT
; i400  0      2     5000  110   1    2      1     .5     .2    .8
; i400  2.5    2     6500  350   .    .      3     .4     .5    .5
; i400  5      2     5500  580   .    .      4     .2     .8    .2
;-----------------------------------------------

        instr      400
ioff400    =       p9
ibt400     =       p10
inobt400   =       p11
; BEGIN AND END VALUES OF BEATING FREQUENCY
ibtfb400   =       1.01*p5
ibtff400   =       0.99*p5
; WAVESHAPING
kfreq400   line    ibtfb400, p3, ibtff400
kenv400    oscil1i 0,1,p3,p8
; FIRST OSCILLATOR
ainA400    oscili  ioff400,p5,p6
awshA400   tablei  kenv400*ainA400,p7,1,ioff400
; SECOND OSCILLATOR
ainB400    oscili  ioff400, kfreq400, p6
awshB400   tablei  kenv400*ainB400,p7,1,ioff400
asig400    =       kenv400*p4*(inobt400*awshA400+ibt400*awshB400)
           out     asig400, asig400
           endin

        instr      401
ioff401    =       p9
ibt401     =       p10
inobt401   =       p11
; BEGIN AND END VALUES OF BEATING FREQUENCY
ibtfb401   =       1.01*p5
ibtff401   =       0.99*p5
; WAVESHAPING
kfreq401   line    ibtfb401, p3, ibtff401
kenv401    oscil1i 0,1,p3,p8
; FIRST OSCILLATOR
ainA401    oscili  ioff401,p5,p6
awshA401   tablei  kenv401*ainA401,p7,1,ioff401
; SECOND OSCILLATOR
ainB401    oscili  ioff401, kfreq401, p6
awshB401   tablei  kenv401*ainB401,p7,1,ioff401
asig401    =       kenv401*p4*(inobt401*awshA401+ibt401*awshB401)
           out     asig401, asig401
           endin


;-----------------------------------------------
; Instruments 800 - 899 import a sound file
; Note that the filename is entered in the orc file and that the location
; of a sound directory needs to be set in the SSDIR environment variable;
; The current sound directory is:
;
;   export SSDIR=/home/jim/data/music/csound/sounds/drumkit/
;
; p4  : AMPLITUDE
; p5  : PITCH
;
; Example:
;   Play an octave below original sound
;              p3  p4     p5
; INSTR START  DUR AMP    PITCH
; i800  0      2   15000  0.5
;-----------------------------------------------

            instr 800
ichn800     filenchnls  "kick.wav"
idur800     =       p3
iamp800     =       p4 / 10000
kpch800     =       p5
kenv800     linen   iamp800, 0.01, idur800, 0.01
if (ichn800 == 1) then
ain800      diskin2 "kick.wav", kpch800
            outs    (kenv800 * ain800), (kenv800 * ain800)
else
aR800, aL800 diskin2 "kick.wav", kpch800
            outs    (kenv800 * aR800), (kenv800 * aL800)
endif
            endin

            instr 801
ichn801     filenchnls  "TomFlatLowHard.wav"
idur801     =       p3
iamp801     =       p4 / 10000
kpch801     =       p5
kenv801     linen   iamp801, 0.01, idur801, 0.01
if (ichn801 == 1) then
ain801      diskin2 "TomFlatLowHard.wav", kpch801
            outs    (kenv801 * ain801), (kenv801 * ain801)
else
aR801, aL801 diskin2 "TomFlatLowHard.wav", kpch801
            outs    (kenv801 * aR801), (kenv801 * aL801)
endif
            endin

            instr 802
ichn802     filenchnls  "snare.wav"
idur802     =       p3
iamp802     =       p4 / 10000
kpch802     =       p5
kenv802     linen   iamp802, 0.01, idur802, 0.01
if (ichn802 == 1) then
ain802      diskin2 "snare.wav", kpch802
            outs    (kenv802 * ain802), (kenv802 * ain802)
else
aR802, aL802 diskin2 "snare.wav", kpch802
            outs    (kenv802 * aR802), (kenv802 * aL802)
endif
            endin

            instr 803
ichn803     filenchnls  "hihat_open.wav"
idur803     =       p3
iamp803     =       p4 / 10000
kpch803     =       p5
kenv803     linen   iamp803, 0.01, idur803, 0.01
if (ichn803 == 1) then
ain803      diskin2 "hihat_open.wav", kpch803
            outs    (kenv803 * ain803), (kenv803 * ain803)
else
aR803, aL803 diskin2 "hihat_open.wav", kpch803
            outs    (kenv803 * aR803), (kenv803 * aL803)
endif
            endin

            instr 804
ichn804     filenchnls  "hihat_closed.wav"
idur804     =       p3
iamp804     =       p4 / 10000
kpch804     =       p5
kenv804     linen   iamp804, 0.01, idur804, 0.01
if (ichn804 == 1) then
ain804      diskin2 "hihat_closed.wav", kpch804
            outs    (kenv804 * ain804), (kenv804 * ain804)
else
aR804, aL804 diskin2 "hihat_closed.wav", kpch804
            outs    (kenv804 * aR804), (kenv804 * aL804)
endif
            endin

            instr 805
ichn805     filenchnls  "TomFullMidHard.wav"
idur805     =       p3
iamp805     =       p4 / 10000
kpch805     =       p5
kenv805     linen   iamp805, 0.01, idur805, 0.01
if (ichn805 == 1) then
ain805      diskin2 "TomFullMidHard.wav", kpch805
            outs    (kenv805 * ain805), (kenv805 * ain805)
else
aR805, aL805 diskin2 "TomFullMidHard.wav", kpch805
            outs    (kenv805 * aR805), (kenv805 * aL805)
endif
            endin

            instr 806
ichn806     filenchnls  "TomHighHard.wav"
idur806     =       p3
iamp806     =       p4 / 10000
kpch806     =       p5
kenv806     linen   iamp806, 0.01, idur806, 0.01
if (ichn806 == 1) then
ain806      diskin2 "TomHighHard.wav", kpch806
            outs    (kenv806 * ain806), (kenv806 * ain806)
else
aR806, aL806 diskin2 "TomHighHard.wav", kpch806
            outs    (kenv806 * aR806), (kenv806 * aL806)
endif
            endin

            instr 807
ichn807     filenchnls  "cymbal_sustain.wav"
idur807     =       p3
iamp807     =       p4 / 10000
kpch807     =       p5
kenv807     linen   iamp807, 0.01, idur807, 0.01
if (ichn807 == 1) then
ain807      diskin2 "cymbal_sustain.wav", kpch807
            outs    (kenv807 * ain807), (kenv807 * ain807)
else
aR807, aL807 diskin2 "cymbal_sustain.wav", kpch807
            outs    (kenv807 * aR807), (kenv807 * aL807)
endif
            endin

;-----------------------------------------------
; Instruments 900 - 999 are for miscellaneous capabilities
; These must be explicitly synced to the orchestra file
;-----------------------------------------------

            instr 900
; Example:
;   Sing the vowel 'ahh'
;              p3  p4     p5    p6    p7   p8       p9
; INSTR START  DUR AMP    PITCH VOWEL TILT VIBR_AMT VIBRATE
; i900  0      2   6000   220   4     90   0.01     5.0

kamp900     =  p4
kfreq900    =  p5
kvowel900   =  p6   ; (0 - 64)
ktilt900    =  p7
kvibamt900  =  p8
kvibrate900 =  p9
asig900 fmvoice kamp900, kfreq900, kvowel900, ktilt900, kvibamt900, kvibrate900
            outs asig900, asig900
            endin 



