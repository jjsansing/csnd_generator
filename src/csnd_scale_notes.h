/**
 * \file csnd_scale_notes.h
 * <h3>CSound Scale Notes Generator header</h3>
 *
 ************************************************************************
 * <hr><p>
 * Copyright (C) 2020 Jim Sansing
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published
 *  bythe Free Software Foundation; either version 2.1 of the License, or
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

#ifndef SCALE_NOTES_H
#define SCALE_NOTES_H

#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <string.h>
#include <stdio.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>

/***** CONSTANTS *****/

#define SN_MAX_FN           128
#define SN_MAX_LINE         512
#define NAME_MAX            64

#define DFLT_STAFF_FILE     "csg_staves"
#define DFLT_NOTE_FILE      "sn_notes"
#define DFLT_SCALE_FILE     "sn_scale"
#define DFLT_SCALE_LEN      7
#define DFLT_INTERVAL       4
#define MAX_SCALES          8192
#define MAX_INTERVAL        25
#define MAX_SCALE_LEN       99

#define DBL_ERROR       -99999.999

/***** MACROS *****/

#define FIND_SPACE(line, idx, linemax) \
while ((line[idx] != ' ' && line[idx] != '\t') && idx < linemax) \
    idx++;

#define SKIP_SPACE(line, idx, linemax) \
while ((line[idx] == ' ' || line[idx] == '\t') && idx < linemax) \
    idx++;

#define CFILE_ERROR(fd, errdata, filenm, label) \
if (feof(fd)) \
{ \
    printf("Warning: did not write %s to %s\n", errdata, filenm); \
    return 0; \
} \
else if (ferror(fd)) \
{ \
    printf("Error: failed to write %s to %s\n  %s\n", errdata, filenm, strerror(errno)); \
    goto label; \
}

/*****  DATA DEFINITIONS  *****/

/**
 * Structure:
 *   snNote
 * 
 * Description:
 *   This structure is used to define notes in a tuning.
 */

typedef struct _snNote {
    struct _snNote     *next;
    int                 index;         /**< Index within list of notes */
    char                name[4];       /**< <octave> <note> <modifier> */
#define NminOctave      0              /**< A = 27.5 Hz */
#define NmaxOctave      9              /**< A = 14080 Hz */
} snNote;

/* Array used for binary searches */
typedef struct _snNoteArray{
    char                name[4];
    snNote             *note;
} snNoteArray;

/**
 * Structure:
 *   snScale
 * 
 * Description:
 *   This structure defines how a note is used in the score.
 */

typedef struct _snScale {
    struct _snScale     *next;
    char                scale[MAX_SCALE_LEN+2]; /**< Scale list */
    char                idx[MAX_SCALE_LEN+2];   /**< Scale note indexes */
    char                name[MAX_SCALE_LEN+2];  /**< Scale string name */
} snScale;

/**
 * Structure:
 *   snStaffNote
 * 
 * Description:
 *   This structure defines how a note is used in the score.
 */

typedef struct _snStaffNote {
    struct _snStaffNote *next;
    char                 line[SN_MAX_LINE]; /**< Note definition */
    unsigned int         flag;
#define SIMP_COMMENT     0x0001         /**< Simple comment */
#define MOD_COMMENT      0x0002         /**< Modifiable comment */
} snStaffNote;

/**
 * Structure:
 *   snStaff
 * 
 * Description:
 *   This structure is used to define staffs in a score which may be
 *   one or more notes.
 */

typedef struct _snStaff {
    struct _snStaff    *next;
    struct _snStaff    *prev;
    char               name[NAME_MAX];  /**< Staff name: freeform */
    char               instr[NAME_MAX]; /**< Instrument playing staff */
    double             new_scale;       /**< Time interval of scale */
    snStaffNote        *notes;          /**< List of notes in staff */
    snStaffNote        *ntail;          /**< End of list of notes */
} snStaff;

/* Pattern list element */
typedef struct _snPattern {
    struct _snPattern *next;
    int                len;                 /**< Length of pattern */
    char               pat[MAX_SCALE_LEN];  /**< Pattern: freeform */
} snPattern;

/**
 * Structure:
 *   snHeader
 * 
 * Description:
 *   This is a list of comments at the beginning of the staff template file.
 */

typedef struct _snHeader {
    struct _snHeader    *next;
    char                 line[SN_MAX_LINE]; /**< Header comment */
} snHeader;


/**
 * Structure:
 *   snMain
 * 
 * Description:
 *   This structure is used to define staffs in a score which may be
 *   one or more notes.
 */

typedef struct _snMain {
    int                 notesz;         /**< Number of notes */
    int                 scalesz;        /**< Number of notes */
    snNote              *notes;         /**< List of notes */
    snNote              *ntail;         /**< End of list of notes */
    snNoteArray         *narray;        /**< Note array for binary searches */
    snPattern           *xpat;          /**< Exclude pattern (-x"hhh") */
    snScale             *scales;        /**< Scale list */
    snScale             *stail;         /**< End of scale list */
    snHeader            *headers;       /**< Header comment list */
    snHeader            *htail;         /**< End of header comment list */
    snStaff             *staffs;        /**< Staff list */
    snStaff             *ctail;         /**< End of staff list */
} snMain;




#endif /* SCALE_NOTES_H */

