#!/usr/bin/python3
#
# \file csnd_snobjP3.py
# CSound Scale Notes Generator header
#
#**********************************************************************
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
#**********************************************************************
#
# This file contains structures used by the CSound Score Generator program.
#
#

# CONSTANTS

SN_MAX_FN = 128
SN_MAX_LINE = 512
NAME_MAX = 64

DFLT_STAFF_FILE = "csg_staves"
DFLT_NOTE_FILE = "sn_notes"
DFLT_SCALE_FILE = "sn_scale"
DFLT_SCALE_LEN = 7
DFLT_INTERVAL = 4
MAX_SCALES = 8192
MAX_INTERVAL = 25
MAX_SCALE_LEN = 99


# CLASS DEFINITIONS

#
# Class: snScale
#
# Description:
#   This class defines how a note is used in the score.
#
# Data:
#   scale: Scale list
#   idx: Scale note indexes
#

class snScale(object):
    def __init__(self):
        self.scales = []
        self.idx = []

    def add_scale(self, s, i):
        self.scales.append(s)
        self.idx.append(i)

    def get_idx(self, s):
        si = self.scales.index(s)
        return self.idx[si]

    def find_dupe(self, pat):
        for sc in self.scales:
            if (sc in pat):
                return 1
        return 0

    def print_data(self):
        for s in self.scales:
            i = self.scales.index(s)
            print(self.idx[i], " :: ", str(s))


#
# Class: snStaff
#
# Description:
#   This class is used to define staffs in a score which may be
#   one or more notes.
#
# Data:
#   name: Staff name: freeform
#   instr: Instrument playing staff
#   notes: List of notes in staff
#   next: Time interval of scales when file groups are used
#

class snStaff(object):
    def __init__(self, cname):
        self.staff = cname
        self.instr = ""
        self.notes = []
        self.next = 1.0

    def add_instr(self, iname):
        self.instr = iname

    def add_fund(self, fund):
        self.notes.append(fund)

    def add_next(self, nxt):
        self.next = float(nxt)

    def print_data(self):
        print(self.staff)
        print(self.instr)
        for nt in self.notes:
            print(nt)


# Pattern list element */
#
# Class: snPattern
#
# Input:
#   pattern: String containing pattern
#   ptype: Type of pattern
#   - x = String
#
# Description:
#   This class maintains the list of patterns to be excluded from scales
#
# Data:
#   xpat: List of string patterns
#

class snPattern(object):

    def __init__(self):
        self.xpat = []

    def add_pat(self, pattern):
        self.xpat.append(pattern)

    def print_data(self):
        if (self.xpat != []):
            print("Exclude patterns:")
            for xp in self.xpat:
                print(xp)


