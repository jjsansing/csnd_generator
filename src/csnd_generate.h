/**
 * \file csnd_generate.h
 * <h3>CSound Score Generator header</h3>
 *
 ************************************************************************
 * <hr><p>
 * Copyright (C) 2020 Jim Sansing
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published
 * by the Free Software Foundation; either version 2.1 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 * <hr><p>
 ************************************************************************
 *
 * This file contains structures used by the CSound Score Generator program.
 *
 */

#ifndef CSND_GEN_H
#define CSND_GEN_H

#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <string.h>
#include <stdio.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>

/***** CONSTANTS *****/

#define CSG_MAX_FN          128
#define CSG_MAX_LINE        512
#define NAME_MAX            64
#define MAX_VOWEL_SZ        16

#define DFLT_SCO_FILE       "csg.sco"
#define DFLT_TMPLT_FILE     "csg_tmplt"
#define DFLT_NOTE_FILE      "csg_notes"
#define DFLT_STAFF_FILE     "csg_staves"
#define DFLT_INSTR_NAME     "csg"

#define DFLT_FUND_VOL       10000
#define DFLT_HARM_VOL       1000

#define DBL_ERROR       -99999.999

#define TONE_FIXED      0x0001         /**< Frequency is fixed */

/***** MACROS *****/

#define FIND_SPACE(line, idx, linemax) \
while ((line[idx] != ' ' && line[idx] != '\t') && idx < linemax) \
    idx++;

#define SKIP_SPACE(line, idx, linemax) \
while ((line[idx] == ' ' || line[idx] == '\t') && idx < linemax) \
    idx++;

#define SCORE_ERROR(fd, errdata, label) \
if (feof(fd)) \
{ \
    printf("Warning: did not write errdata to score\n"); \
    return 0; \
} \
else if (ferror(fd)) \
{ \
    printf("Error: failed to write errdata to score\n  %s\n", strerror(errno)); \
    goto label; \
}

/*****  DATA DEFINITIONS  *****/

/**
 * Structure:
 *   csgTone
 * 
 * Description:
 *   This structure is used to define simple tones that are waveforms in a note.
 *
 *   The input is in the following format:
 * <code>
 *              p3  p4    p5      p6    p7    p8    p9    p10
 * INSTR START  DUR AMP   FREQ    WAVE  ATT   DEC   SUS   REL
 * </code>
 */

typedef struct _csgTone {
    struct _csgTone     *next;
    double              start;         /**< Tone relative start time */
    double              durat;         /**< Tone duration */
    double              freq;          /**< Tone frequency */
    double              vol;           /**< Tone relative volume */
    char                parms[CSG_MAX_LINE]; /**< Remaining parameters */
    unsigned int        flag;
} csgTone;

/**
 * Structure:
 *   csgSimpTone
 * 
 * Description:
 *   This structure is used to define simple tones that are waveforms in a note.
 *
 *   The input is in the following format:
 * <code>
 * p1    p2     p3  p4    p5      remaining parameters
 * INSTR START  DUR AMP   FREQ
 * </code>
 */

typedef struct _csgSimpTone {
    struct _csgSimpTone     *next;
    double              start;         /**< Tone relative start time */
    double              durat;         /**< Tone duration */
    double              freq;          /**< Tone frequency */
    char                *parms;        /**< Remaining parameters */
    int                 vol;           /**< Tone relative volume */
    char                waveFunc;      /**< Wave definition function */
    unsigned int        flag;
} csgSimpTone;

/**
 * Structure:
 *   csgVowelTone
 * 
 * Description:
 *   This structure is used to define voice vowel sounds.
 *
 *   The input is in the following format:
 * <code>
 *              p3  p4    p5    p6      p7    p8         p9
 * INSTR START  DUR AMP   FREQ  (vowel) TILT  VIB_DEPTH  VIB_AMT
 * </code>
 */

typedef struct _csgVowelTone {
    struct _csgVowelTone     *next;
    double              start;         /**< Tone relative start time */
    double              durat;         /**< Tone duration */
    double              freq;          /**< Tone frequency */
    double              vibdepth;      /**< Vibrato depth */
    double              vibamt;        /**< Vibrato amount */
    int                 tilt;          /**< Spectral tilt (0 - 99) */
    int                 vol;           /**< Tone relative volume */
} csgVowelTone;

/**
 * Structure:
 *   csgSNDTone
 * 
 * Description:
 *   This structure is used to define sound files imported into CSound
 *   compositions.
 *
 *   The input is in the following format:
 * <code>
 *              p3    p4    p5
 * INSTR START  DUR   AMP   PITCH
 * </code>
 */

typedef struct _csgSNDTone {
    struct _csgSNDTone  *next;
    double              start;         /**< Tone relative start time */
    double              durat;         /**< Tone duration */
    double              pitch;         /**< Tone pitch relative to original */
    int                 vol;           /**< Tone relative volume */
} csgSNDTone;

/**
 * Structure:
 *   csgNote
 * 
 * Description:
 *   This structure is used to define notes in a score.
 */

typedef struct _csgNote {
    struct _csgNote     *next;
    double              freq;          /**< Tone frequency */
    int                 index;         /**< Index within list of notes */
    char                name[4];       /**< <octave> <note> <modifier> */
} csgNote;

/* Used to create a list of note files */
typedef struct _csgNoteFiles{
    struct _csgNoteFiles *next;
    char                 name[CSG_MAX_FN];
} csgNoteFiles;

/* Array used for binary searches */
typedef struct _csgNoteArray{
    char                name[4];
    csgNote             *note;
} csgNoteArray;

/* Array used for frequency searches */
typedef struct _csgNoteFreqArray{
    csgNote             *note;
    double              freq;
} csgNoteFreqArray;

/**
 * Structure:
 *   csgVowel
 * 
 * Description:
 *   This structure is used to define vowels to be sung in a score.
 */

typedef struct _csgVowel {
    struct _csgVowel    *next;
    int                 id;            /**< CSound ID for fmvoice opcode */
    char                name[8];       /**< Freeform */
} csgVowel;

/* Array used for binary searches */
typedef struct _csgVowelArray{
    char                name[MAX_VOWEL_SZ];
    csgVowel            *vowel;
} csgVowelArray;

/**
 * Structure:
 *   csgInstrument
 * 
 * Description:
 *   This structure is the information to define instruments, which is
 *   essentially multipliers for tones.
 */

typedef struct _csgInstrument {
    struct _csgInstrument *next;
    char               name[NAME_MAX];  /**< Number of notes */
    csgTone            *tones;          /**< Generic tones */
    csgTone            *ttail;          /**< End of list pointer */
    csgSimpTone        *stones;         /**< Simple tones */
    csgSimpTone        *sttail;         /**< End of list pointer */
    csgVowelTone       *vtones;         /**< Vowel tones */
    csgVowelTone       *vttail;         /**< End of list pointer */
    csgSNDTone         *sndtones;       /**< Waveshaped tones with envelope */
    csgSNDTone         *sndttail;       /**< End of list pointer */
    double             volchange;       /**< Volume change in each octave of harmonics */
    double             attchange;       /**< Attack change in each octave of harmonics */
    double             decchange;       /**< Decay change in each octave of harmonics */
    double             suschange;       /**< Sustain change in each octave of harmonics */
    double             relchange;       /**< Release change in each octave of harmonics */
    unsigned int       flag;
#define SCALEHARM      0x0001           /**< Use scale frequencies for harmonics */
} csgInstrument;

/**
 * Structure:
 *   csgFunction
 * 
 * Description:
 *   This structure is the information to create a CSound waveshape
 *   function definition.  The data is copied as is from the template file
 *   into the score file.
 */

typedef struct _csgFunction {
    struct _csgFunction    *next;
    char                    parms[CSG_MAX_LINE];  /**< Parameter string */
} csgFunction;

/**
 * Structure:
 *   csgStaffNote
 * 
 * Description:
 *   This structure defines how a note is used in the score.
 */

typedef struct _csgStaffNote {
    struct _csgStaffNote *next;
    csgNote              *note;        /**< Note in staff */
    double               start;        /**< Note start time */
    double               durat;        /**< Note duration */
    int                  vol;          /**< Note volume */
    int                  vid;          /**< Vowel ID */
} csgStaffNote;

/**
 * Structure:
 *   csgStaff
 * 
 * Description:
 *   This structure is used to define staffs in a score which may be
 *   one or more notes.
 */

typedef struct _csgStaff {
    struct _csgStaff    *next;
    struct _csgStaff    *prev;
    char                name[NAME_MAX]; /**< Staff name: freeform */
    csgInstrument       *instr;         /**< Instrument playing staff */
    csgStaffNote        *notes;         /**< List of notes in staff */
    csgStaffNote        *ntail;         /**< End of list of notes */
    double              period;         /**< Seconds between note repetition */
    double              pdchange;       /**< +/- change in period */
    double              divisor;        /**< For REPEATV and REPEATP */
    double              panr_st;        /**< Pan right start */
    double              panr_fn;        /**< Pan right finish */
    double              panl_st;        /**< Pan left start */
    double              panl_fn;        /**< Pan left finish */
    int                 repeat;         /**< Number of repetitions */
    int                 volchange;      /**< +/- change in volume */
    unsigned int        flag;
#define REPEATGRP       0x0001          /**< Repeat special type is group */
#define REPEATV         0x0002          /**< Repeat special type is volume */
#define REPEATP         0x0004          /**< Repeat special type is period */
} csgStaff;

/**
 * Structure:
 *   csgRepeatGroup
 * 
 * Description:
 *   This structure is used to generate repetitions of a group of staffs.
 */

typedef struct _csgRepeatGroup {
#define MAXCH           64              /**< Maximum number of staffs in group */
    csgStaff            *staffs[MAXCH]; /**< Vector of staffs in group */
    double              period;         /**< Seconds between repetitions */
    double              pdchange;       /**< +/- change in period */
    int                 chcount;        /**< Number of staffs */
    int                 repeat;         /**< Number of repetitions */
} csgRepeatGroup;

/**
 * Structure:
 *   csgScore
 * 
 * Description:
 *   This structure contains all of the information to create a
 *   CSound score (*.sco) file.
 */

typedef struct _csgScore {
    int                 notesz;        /**< Number of notes */
    int                 vowelsz;       /**< Number of vowels */
    csgNote             *notes;        /**< Note list */
    csgNoteFiles        *nfiles;       /**< List of note files */
    csgNoteArray        *narray;       /**< Note array for binary searches */
    csgNoteFreqArray    *nfrqarr;      /**< Note array in frequency order */
    csgVowel            *vowels;       /**< Vowel list */
    csgVowelArray       *varray;       /**< Vowel array for binary searches */
    csgInstrument       *instruments;  /**< Instrument list */
    csgFunction         *functions;    /**< Function list */
    csgStaff            *staffs;       /**< Staff list */
    csgStaff            *ctail;        /**< End of Staff list */
} csgScore;


#endif /* CSND_GEN_H */

