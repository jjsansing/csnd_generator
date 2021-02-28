#!/usr/bin/python2
#
# /file csnd_genP2.py
# CSound Score Generator Program
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
# Input Data
# - Score filename
# - Template filename
# - Note definition filename
# - Harmonic variables
#
# Output Data
# - <filename>.sco
# - <filename>.wav
#
# Functions
# - Parse command line
# - Parse template file
# - Parse note definition file
# - Create score
#   - Add fundamental note
#   - Add harmonics
#     - Modify harmonics over time
# -?? Run CSound to produce wav file (probably done in script)
#

#
# IMPORTS
#

import csnd_genobjP2
import getopt, sys

#
# GLOBAL CONSTANTS
#

# Debug: Notes = 1, Template = 2, Staffs = 4
debug = 0

csg_ver = 1.0

tfile = "csg_tmplt"
vfile = "csg_staves"
sfile = "csg.sco"
nfiles = []

note_defs = []
instrs = []
staffs = []
func_defs = []
vowel_defs = []
score = []

tempo_diff = 1.0

#
# FUNCTIONS
#

# Print function information for developers
def dev_help():
    print(parse_notes.__doc__)
    print(parse_tone.__doc__)
    print(parse_template.__doc__)
    print(parse_staffs.__doc__)
    print(create_score.__doc__)
    print(usage.__doc__)
    print(main.__doc__)


def parse_notes():
    """
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
Function: parse_notes

Description:
  Parse the notes file which contains note definitions.  The file only
  maps note names to frequencies for easy reference.  Since multiple note
  files are allowed, if there is a duplicate note name, it is ignored,
  although if the frequency is different from the existing frequency, a
  warning is issued.

  Comments are indicated by preceeding a line with '#', and blank lines
  are permitted.  The format of the note file is as follows:
    NOTE name frequency
  - name: <octave> <note> <modifier>
    - octave = 0 (A = 27.5 Hz) - 9 (A = 14080 Hz)
    - note: A - Z and a - z case sensitive
    - modifiers: 0 - 9, A - Z, and a - z case sensitive
  - frequency: double
Inputs:
  - notefn: Name of note file to parse
Outputs:
  - int: Status
    - 0 = OK
    - <0 = Error
    """

    for fn in nfiles:
        try:
            nfd = open(fn, 'r')
        except IOError as e:
            print "Error failed to open note file ", fn
            print "  ", e
            return -1

        lines = nfd.readlines()
        for line in lines:
        # Check for blank lines and comments
            if (line[0] == '#' or line[0] == '\0' or line[0] == '\n'):
                continue
            else:
                nd = line.split()
                nd2 = float(nd[2])
                ndt = (nd[1], nd2)
                note_defs.append(ndt)

        nfd.close()

    return 0


def parse_tone(line, instr):
    """
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
Function: parse_tone

Description:
  Parse tones on a single line of a note file and add them to a
  csgInstrument struct.  There are multiple formats for tones and
  each is handled separately.
Inputs:
  - line: Tone line to be parsed
  - instr: Instrument to which tones belong
Outputs:
  - int: Status
    - 0 = OK
    - <0 = Error
    """

    td = line.split(None, 5)
    FIXED = 0
    if (td[0] == "TONE" or td[0] == "TFIXED"):
        if (td[0] == "TFIXED"):
            FIXED = 1
        # Start, duration, volume, frequency, FIXED, remaining parameters
        rmparms = td[5].rstrip('\n')
        tdl = (float(td[1]), float(td[2]), float(td[3]), float(td[4]), FIXED, rmparms)
        instr.add_tone(tdl)

    elif (td[0] == "SIMP" or td[0] == "FIXED"):
        if (td[0] == "FIXED"):
            FIXED = 1
        # Start, duration, volume, frequency, FIXED, remaining parameters
        rmparms = td[5].rstrip('\n')
        tdl = (float(td[1]), float(td[2]), int(td[3]), float(td[4]), FIXED, rmparms)
        instr.add_stone(tdl)

    elif (td[0] == "FM" or td[0] == "AM" or td[0] == "WS1" or td[0] == "WS2"):
        # Start, duration, volume, frequency, FIXED, remaining parameters
        rmparms = td[5].rstrip('\n')
        tdl = (float(td[1]), float(td[2]), int(td[3]), float(td[4]), FIXED, rmparms)
        instr.add_stone(tdl)

    elif (td[0] == "VOICE"):
        # Start, duration, volume, frequency, remaining parameters
        vd = line.split(None, 5)
        rmparms = vd[5].rstrip('\n')
        vdl = (float(vd[1]), float(vd[2]), int(vd[3]), float(vd[4]), rmparms)
        instr.add_vtone(vdl)

    elif (td[0] == "SND"):
        # Start, duration, volume, frequency
        ad = line.split()
        adl = (float(ad[1]), float(ad[2]), int(ad[3]), float(ad[4]))
        instr.add_sndtone(adl)

    return 0



def parse_template():
    """
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
Function: parse_template

Description:
  Parse the template file which contains the following data:
  - Wave function definitions
  - Instrument definitions
    - Tone templates
Inputs:
  - None
Outputs:
  - int: Status
    - 0 = OK
    - <0 = Error
    """

    iname = ""
    instr = []

    try:
        tfd = open(tfile, 'r')
    except IOError as e:
        print "Error failed to open template file ", tfile
        print "  ", e
        return -1

    td = ""
    lines = tfd.readlines()
    for line in lines:
    # Check for blank lines and comments
        if (line[0] == '#' or line[0] == '\0' or line[0] == '\n'):
            continue
        else:
            td = line.split()

        if (td[0] == "FUNC"):
            fd = line.split(None, 1)
            fdt = (fd[1])
            func_defs.append(fdt)

        elif (td[0] == "VOWEL"):
            vdt = (td[1], td[2])
            vowel_defs.append(vdt)

        elif (td[0] == "INSTR"):
            iname = "i" + td[1]
            instr = csnd_genobjP2.csgInstrument(iname)
            instrs.append(instr)

        elif (td[0] == "SCALEHARM"):
            if (instr != []):
                instr.SCALEHARM = 1

        else:
            if (instr == []):
                print "Error: no instrument for definition"
                print "  ", line
                tfd.close
                return -1
            if (parse_tone(line, instr) != 0):
                tfd.close()
                return -1

    tfd.close()
    return 0



def parse_staffs():
    """
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
Function: parse_staffs

Description:
  Parse the staves file which contains the following staff parameters:
  - Instrument
  - Notes
  - Start and Duration
  - Volume
  A staff is one or more notes played by a single instrument.  Two or more
  staves may be played at the same start time.  The staff information is
  multiplied by the template data for the instrument to create a score.
Inputs:
  - None
Outputs:
  - int: Status
    - 0 = OK
    - <0 = Error
    """

    global tempo_diff

    try:
        vfd = open(vfile, 'r')
    except IOError as e:
        print "Error failed to open staves file ", vfile
        print "  ", e
        return -1

    staff = []
    lines = vfd.readlines()
    for line in lines:
    # Check for blank lines and comments
        if (line[0] == '#' or line[0] == '\0' or line[0] == '\n'):
            continue

        cd = line.split(None, 2)
        if (cd[0] == "TEMPO"):
            tempo_diff = float(cd[1])

        elif (cd[0] == "STAFF"):
            cname = cd[1]
            staff = csnd_genobjP2.csgStaff(cname)
            staffs.append(staff)

        elif (cd[0] == "INSTR"):
            rd = line.split()
            if (staff == []):
                print "Error: No staff for instrument: ", rd[1]
                vfd.close()
                return -1
            for cinstr in instrs:
                iname = "i" + rd[1]
                if (cinstr.name == iname):
                    staff.add_instr(cinstr)
                    break

        elif (cd[0] == "REPEAT"):
            if (staff == []):
                print "Error: No staff for repeat: ", line
                vfd.close()
                return -1
            rd = line.split()
            # Count, period, volume_change, period_change
            rdt = (int(rd[1]), float(rd[2]), int(rd[3]), float(rd[4]))
            staff.add_repeat(rdt)

        elif (cd[0] == "FUND"):
            if (staff == []):
                print "Error: No staff for note definition: ", line
                vfd.close()
                return -1
            fd = line.split()
            fdt = (fd[1], float(fd[2]), float(fd[3]), int(fd[4]))
            staff.add_fund(fdt)

        elif (cd[0] == "VFUND"):
            if (staff == []):
                print "Error: No staff for note definition: ", line
                vfd.close()
                return -1
            fd = line.split()
            fdt = (fd[1], float(fd[2]), float(fd[3]), int(fd[4]), fd[5])
            staff.add_fund(fdt)

        else:
            cdt = line.split('=')
            if (cdt[0] == "TEMPO"):
                tempo_diff = float(cdt[1])


    vfd.close()
    return 0

def create_score():
    """
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
Function: create_score

Description:
  Create a CSound score (*.sco) file

  The CSound scores created by this program have a function area followed
  by the tones definitions. The function fields are defined in the Template
  file and used as is.  The notes are created by combining the Note,
  Template, and Staff data as follows:
  - Note data: This is simply the frequency in Hz of the fundamental
  - Template data: The Instrument definition is a list of tones that
    work as harmonics to the fundamental.  They are calculated based on
    the frequency of the fundamental.
  - Staff data: This is a list of notes with the start time and duration,
    and the volume at the time the staff is played.
Inputs:
  - None
Outputs:
  - int: Status
    - 0 = OK
    - <0 = Error
    """

    s = 0
    d = 1
    v = 2
    f = 3
    F = 4
    r = 5

    try:
        sfd = open(sfile, 'w')
    except IOError as e:
        print "Error failed to open score file ", sfile
        print "  ", e
        return -1
    sfd.write(";This score was generated by the CSound Generator\n\n")

    for fd in func_defs:
        fstr = fd + "\n"
        sfd.write(fstr)

    idx = 0
    while (idx < len(staffs)):
        ch = staffs[idx]
        chname = ";   " + ch.name + "\n"
        sfd.write(chname)
        for nt in ch.notes:
            ntnm = nt[0]
            try:
                ntdef = notes.getnote(ntnm, 0, notes.notesz-1)
            except Exception as e:
                print e
                return -1

            # Generic tones
            for gt in ch.instr.tones:
                # Start, duration, volume, frequency, FIXED, remaining parameters
                start = (gt[s] + nt[1]) * tempo_diff
                durat = (gt[d] * nt[2]) * tempo_diff
                vol = float(gt[v]) * float(nt[3])
                if (ch.instr.SCALEHARM == 1):
                    x = int(ntdef[2]) + int(gt[f])
                    if (x < notes.notesz):
                        freq = notes.notes[x][1]
                else:
                    if (gt[F] == 1):
                        freq = float(gt[f])
                    else:
                        freq = float(ntdef[1]) * float(gt[f])
                wstr = ch.instr.name + "  " + str(start) + "  " + str(durat) + "  " + str(vol) + "  " + str(freq) + "  " + gt[r] + "\n"
                sfd.write(wstr)

            # Simple tones
            for st in ch.instr.stones:
                # Start, duration, volume, frequency, FIXED, remaining parameters
                start = (st[s] + nt[1]) * tempo_diff
                durat = (st[d] * nt[2]) * tempo_diff
                vol = float((int(st[v]) * int(nt[3])) / 1000)
                if (ch.instr.SCALEHARM == 1):
                    x = int(ntdef[2]) + int(st[f])
                    if (x < notes.notesz):
                        freq = notes.notes[x][1]
                else:
                    if (st[F] == 1):
                        freq = float(st[f])
                    else:
                        freq = float(ntdef[1]) * float(st[f])
                wstr = ch.instr.name + "  " + str(start) + "  " + str(durat) + "  " + str(vol) + "  " + str(freq) + "  " + str(st[F+1]) + "\n"
                sfd.write(wstr)

            # Vowel tones
            for vt in ch.instr.vtones:
                # Start, duration, volume, frequency, vowel_id, remaining parameters
                start = (vt[s] + nt[1]) * tempo_diff
                durat = (vt[d] * nt[2]) * tempo_diff
                vol = float((int(vt[v]) * int(nt[3])) / 1000)
                freq = float(ntdef[1]) * float(vt[f])
                try:
                    vowel = vowels.getvowel(nt[4], 0, vowels.vowelsz-1)
                except Exception as e:
                    print e
                    return -1
                wstr = ch.instr.name + "  " + str(start) + "  " + str(durat) + "  " + str(vol) + "  " + str(freq) + "  " + str(vowel) + "  " + str(vt[f+1]) + "\n"
                sfd.write(wstr)

            # Sound files
            for st in ch.instr.sndtones:
                # Start, duration, volume, frequency
                start = (st[s] + nt[1]) * tempo_diff
                durat = (st[d] * nt[2]) * tempo_diff
                vol = float((int(st[v]) * int(nt[3])) / 1000)
                freq = float(ntdef[1]) * float(st[f])
                wstr = ch.instr.name + "  " + str(start) + "  " + str(durat) + "  " + str(vol) + "  " + str(freq) + "\n"
                sfd.write(wstr)

            if (ch.repeat > 0):
                # Count, period, volume_change, period_change
                nidx = ch.notes.index(nt)
                ntvol = nt[3] + ch.volchange
                if (ntvol < 0):
                    ntvol = 0
                t = nt[0], nt[1] + ch.period, nt[2], ntvol
                ch.notes[nidx] = t

        if (ch.repeat > 0):
            ch.repeat -= 1
            ch.period += ch.pdchange
            if (ch.period < 0):
                ch.period = 0
            cidx = staffs.index(ch)
            chnew = staffs.pop(cidx)
            max = len(staffs)
            while (cidx < max):
                if (cidx == (max - 1)):
                    staffs.append(chnew)
                elif (staffs[cidx].notes[0][1] > chnew.notes[0][1]):
                    staffs.insert(cidx, chnew)
                    break
                cidx += 1
        else:
            idx += 1

    sfd.close()
    return 0

def usage():
    """
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
Function: usage

Description:
  Explain the command line arguments.
Inputs:
  - None
Outputs:
  - int: Status
    - 0 = OK
    """

    print '\n'
    print '  csnd_genP2.py Version', csg_ver
    print '\n'
    print '  csnd_genP2.py [arguments]:'
    print '  -D: Display developer information, main is described at the end'
    print '  -d: debug code: Note = 1, Template = 2, Staff = 4'
    print '      Values can be ORed for multiple printouts'
    print '  -n: note_file: Name of note files, enter -n for each'
    print '  -s: sco_file: Name of sco file'
    print '      Default: ', sfile
    print '  -t: template_file: Name of template file'
    print '      Default: ', tfile
    print '  -v: staves_file: Name of staves file'
    print '      Default: ', vfile
    print '\n'
    sys.exit(0)


def main():
    """
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
Function: main

Description:
  The command line arguments are checked.  Then the configuration file parsers
  are called and the score is created.
Inputs:
  - See command line arguments
Outputs:
  - int: Status
    - 0 = OK
    - 1 = Error
    """

if __name__ == '__main__':
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'd:n:s:t:v:D')
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(1)

    # Parse command line arguments
    for opt, optarg in opts:
        if opt in ['-v']:
            vfile = optarg
        elif opt in ['-d']:
            debug = int(optarg)
        elif opt in ['-n']:
            nfiles.append(optarg)
        elif opt in ['-s']:
            sfile = optarg
        elif opt in ['-t']:
            tfile = optarg
        elif opt in ['-D']:
            dev_help()
            sys.exit(0)

    print "\nStarting CSound Generator\n"

    if parse_notes() != 0:
        sys.exit(1)
    else:
        notes = csnd_genobjP2.csgNote(note_defs)
    if (debug & 1 == 1):
        print "Note definitions"
        notes.print_data()

    if parse_template() != 0:
        sys.exit(1)
    else:
        vowels = csnd_genobjP2.csgVowel(vowel_defs)
    if (debug & 2 == 2):
        print "Template definitions"
        for fd in func_defs:
            print fd,
        vowels.print_data()
        for instr in instrs:
            instr.print_data()
        print " "

    if parse_staffs() != 0:
        sys.exit(1)
    if (debug & 4 == 4):
        print "Staff definitions"
        for staff in staffs:
            staff.print_data()
        print " "

    if create_score() != 0:
        sys.exit(1)

    print "Completed CSound Generator using score file", sfile, "\n"

