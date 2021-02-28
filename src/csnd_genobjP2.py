#!/usr/bin/python
#
# \file csnd_genobjP2.py
# CSound Score Generator classes
#
#***********************************************************************
# Copyright (C) 2020 Jim Sansing
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 2.1
# as published by the Free Software Foundation; either version 3 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#***********************************************************************
#
# This file contains classes used by the CSound Score Generator program.
#
#

# IMPORTS

import numpy

def sort2(L):
    return L[1]

#
#  Class: csgNote
#
#  Description:
#    This class is used to define notes in a score.
#
#  Data;
#    notes : List sorted by notes
#    freqs: List sorted by frequency for getting SCALEHARM frequencies
#    notesz: Number of notes
#

class csgNote:

    def __init__(self, note_defs):
        note_defs.sort(None, key=sort2)
        self.freqs = numpy.array(note_defs)    # List sorted by frequencies
        note_defs.sort()
        i = 0
        while (i < len(note_defs)):
            j = 0
            while (j < len(self.freqs)):
                if (note_defs[i][0] == self.freqs[j][0]):
                    t = note_defs[i][0], note_defs[i][1], j
                    note_defs[i] = t
                    break
                else:
                    j += 1
            i += 1
        self.notes = numpy.array(note_defs)    # List sorted by notes
        self.notesz = len(self.notes)           # Length of note lists

    # Recursive binary search on notes
    def getnote(self, notename, gnmin, gnmax):
        if (gnmax >= gnmin):
            gnmid = gnmin + ((gnmax - gnmin) >> 1)
            if (self.notes[gnmid][0] == notename):
                return self.notes[gnmid]

            elif (self.notes[gnmid][0] > notename):
                return self.getnote(notename, gnmin, gnmid - 1)

            elif (self.notes[gnmid][0] < notename):
                return self.getnote(notename, gnmid + 1, gnmax)

        raise Exception("Error: Note was not found: ", notename)

    def print_data(self):
        i = 0
        while (i < self.notesz):
            print self.notes[i], " :: ", self.freqs[i]
            i += 1

### End of class csgNote

#
#  Class: csgVowel
#
#  Description:
#    This class is used to define vowels to be sung in a score.
#
#  Data:
#    ids : List sorted by ID of vowel
#

class csgVowel:

    def __init__(self, vowel_defs):
        vowel_defs.sort(None, key=sort2)
        self.ids = numpy.array(vowel_defs)
        self.vowelsz = len(self.ids)       # Length of vowel list

    # Recursive binary search on vowels
    def getvowel(self, vowelname, gnmin, gnmax):
        if (gnmax >= gnmin):
            gnmid = gnmin + ((gnmax - gnmin) >> 1)
            if (self.ids[gnmid][1] == vowelname):
                return self.ids[gnmid][0]

            elif (self.ids[gnmid][1] > vowelname):
                return self.getvowel(vowelname, gnmin, gnmid - 1)

            elif (self.ids[gnmid][1] < vowelname):
                return self.getvowel(vowelname, gnmid + 1, gnmax)

        raise Exception("Error: Vowel was not found: ", vowelname)

    def print_data(self):
        print "Vowels", self.vowelsz
        print self.ids

### End of class csgVowel


#
#  Class: csgInstrument
#
#  Description:
#    This class is the information to define instruments, which is
#    essentially multipliers for tones.
#
#  Data:
#    name: Instrument ID 1 - 999999
#    tones, stone: List of Generic or Simple Tones
#       Fields: Start, duration, volume, frequency, FIXED,
#          where <next> = (tones) remaining parameters, or (stones) waveform, ADSR
#    vtones, sndtones: List of Vowel or Sound Tones
#    volchange, attchange, decchange, suschange, relchange: Volume or ADSR change
#      in each octave
#    SCALEHARM: If 1, use scale harmonics
#

class csgInstrument:

    def __init__(self, iname):
        self.name = iname            # Instrument ID
        self.tones = []              # List of Tones
        self.stones = []             # List of SimpTones
        self.vtones = []             # List of VowelTones
        self.sndtones = []           # List of SNDTones
        self.volchange = 0.0         # Volume change in each octave of harmonics
        self.attchange = 0.0         # Attack change in each octave of harmonics
        self.decchange = 0.0         # Decay change in each octave of harmonics
        self.suschange = 0.0         # Sustain change in each octave of harmonics
        self.relchange = 0.0         # Release change in each octave of harmonics
        self.SCALEHARM = 0

    def add_tone(self, tone):
        self.tones.append(tone)

    def add_stone(self, tone):
        self.stones.append(tone)

    def add_vtone(self, tone):
        self.vtones.append(tone)

    def add_sndtone(self, tone):
        self.sndtones.append(tone)

    def print_data(self):
        print "Instrument", self.name, self.SCALEHARM
        for t in self.tones:
            print t
        for t in self.stones:
            print t
        for t in self.vtones:
            print t
        for t in self.sndtones:
            print t

### End of class csgInstrument


#
#  Class: csgStaff
#
#  Description:
#    This class is used to define staves in a score which may be
#    one or more notes.
#
#  Data:
#    name: Staff name, freeform
#    instr: Instrument object to use for the staff
#    notes, vnotes: List of notes or vowels to be played
#    repeat, period, volchange, pdchange: REPEAT parameters
#

class csgStaff:

    def __init__(self, cname):
        ### Bidirectional list struct _csgStaff    *prev
        self.name = cname       # Staff name: freeform
        self.notes = []         # List of note definitions
        self.vnotes = []        # List of vocal note definitions
        self.repeat = 0         # Number of repetitions
        self.period = 0.0       # Seconds between note repetition
        self.volchange = 0      # +/- change in volume
        self.pdchange = 0.0     # +/- change in period
        ##  Not yet implemented
        ## self.divisor = 0.0      # For REPEATV and REPEATP
        ## self.REPEATGRP = 0
        ## self.REPEATV = 0
        ## self.REPEATP = 0
        ## self.panr_st = 0.0      # Pan right start
        ## self.panr_fn = 0.0      # Pan right finish
        ## self.panl_st = 0.0      # Pan left start
        ## self.panl_fn = 0.0      # Pan left finish

    def add_instr(self, cinstr):
        self.instr = cinstr

    def add_repeat(self, rpt):
        self.repeat = int(rpt[0])
        self.period = float(rpt[1])
        self.volchange = int(rpt[2])
        self.pdchange = float(rpt[3])

    def add_fund(self, fdt):
        self.notes.append(fdt)

    def add_vfund(self, fdt):
        self.vnotes.append(fdt)

    # Recursive binary search on vowel notes
    def getvnote(self, notename, gnmin, gnmax):
        if (gnmax >= gnmin):
            gnmid = gnmin + ((gnmax - gnmin) >> 1)
            if (self.vnotes[gnmid][0] == notename):
                return self.vnotes[gnmid]

            elif (self.vnotes[gnmid][0] > notename):
                return self.getvnote(notename, gnmin, gnmid - 1)

            elif (self.vnotes[gnmid][0] < notename):
                return self.getvnote(notename, gnmid + 1, gnmax)

        raise Exception("Error: Vocal note was not found: ", notename)

    def print_data(self):
        print "Staff", self.name, "Instrument", self.instr.name
        if (self.repeat > 0):
            print "  REPEAT", self.repeat, self.period, self.volchange, self.pdchange
        for n in self.notes:
            print n
        for n in self.vnotes:
            print n

### End of class csgStaff


