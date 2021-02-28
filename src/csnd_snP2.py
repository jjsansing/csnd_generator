#!/usr/bin/python
#
# /file csnd_snP2.py
# CSound Scale Notes Generator Program
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
# - Staves filename (default = sn_staffs.<scalename>)
#   - Scale names are the steps where:
#     h = half tone, w = whole tone, m = minor 3rd, M = major 3rd, f = fourth,
#     d = diminished fifth, F = fifth, a = augmented fifth, s = sixth,
#     A = augmented sixth, S = seventh, j = major seventh, e = eighth,
#     n = diminished ninth, N = ninth, t = diminished tenth, T = tenth,
#     v = diminished eleventh, V = eleventh, l = diminished twelfth, L = twelfth,
#     r = diminished thirteenth, R = thirteenth, o = diminished fourteenth, O = fourteenth
# - Note definition filename
#   - Definitions must include octave 0:  NOTE 0A 29.49
# - Scale staffs example filename (default = sn_example)
# - Number of notes in a scale (excluding octave)
# - Maximum number of steps (default = 4 : major 3rd, maximum = 25 : fourteenth)
# - First scale to generate (default = 1)
# - Maximum number of scales to generate (default = all)
# - Number of scales to group in 1 file
#
# Output Data
# - csg_staves.<filename>


#
# IMPORTS
#

import csnd_snobjP2
import getopt
import array
import sys

#
# GLOBAL CONSTANTS
#

sn_ver = 1.0

vfile = "csg_staves"
nfile = "sn_notes"
sfile = "sn_scale"

note_defs = []
staffs = []
scales = csnd_snobjP2.snScale()
xpat_defs = []

sn_first_scale = 1
sn_group_size = 1
sn_max_interval = 4
sn_max_scales = 8192
sn_scale_len = 7

scalesz = 0
sn_tuning_size = 0

sn_intervals = " hwmMfdFasASjenNtTvVlLrRoO"

#
# FUNCTIONS
#

# Print function information for developers
def dev_help():
    print(parse_notes.__doc__)
    print(get_unique_scales.__doc__)
    print(parse_staffs.__doc__)
    print(modify_staffnote.__doc__)
    print(create_stafffile.__doc__)
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
  - None
Outputs:
  - int: Status
    - 0 = OK
    - <0 = Error
    """

    global sn_tuning_size

    try:
        nfd = open(nfile, 'r')
    except IOError as e:
        print "Error failed to open note file ", nfile
        print "  ", e
        return -1

    lines = nfd.readlines()
    for line in lines:
    # Check for blank lines and comments
        if (line[0] == '#' or line[0] == '\0' or line[0] == '\n'):
            continue
        else:
            nd = line.split()
            note_defs.append(nd[1])
            sn_tuning_size += 1

    nfd.close()

    return 0


def get_unique_scales():
    """
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
Function: get_unique_scales

Description:
  Calculate the list of unique scales based on the tuning and scale criteria.
Inputs:
  - None
Outputs:
 - int: Status
   - 0 = OK
   - <0 = Error
    """

    global scalesz

    # Get variables: tuning_size, scale_len, max_interval
    # Find first scale: array[scale_len] = {1,1,1,...}
    scale_arr = array.array('B')
    scale_arr2 = array.array('B')
    scale_steps = array.array('c')
    idx = 0
    while (idx < sn_scale_len):
        scale_arr.append(1)
        scale_arr2.append(1)
        scale_arr2.append(1)
        scale_steps.append('a')
        scale_steps.append('a')
        idx += 1

    # Add all intervals, (if = tuning_size) test for dupes, (if unique) keep
    done = 0
    scale_cnt = 1
    scale_ucnt = 0
    first_time = 1
    newscale = []
    newidx = []
    loopcnt = 0
    print "Get unique scales: ",
    while (done == 0):
        if ((loopcnt & 0xfff) == 0):
            print ".",
            sys.stdout.flush()
        loopcnt += 1
        interval_total = 0
        unique = 1
        idx = 0
        while (idx < sn_scale_len):
            interval_total += int(scale_arr[idx])
            idx += 1
        if (interval_total == sn_tuning_size):
            scale_cnt += 1
            # Use scale copy to test for duplicates starting at
            # different points in the scale
            idx = 0
            while (idx < sn_scale_len):
                scale_arr2[idx] = scale_arr[idx]
                scale_arr2[idx + sn_scale_len] = scale_arr[idx]
                scale_steps[idx] = sn_intervals[scale_arr[idx]]
                scale_steps[idx + sn_scale_len] = scale_steps[idx]
                idx += 1
            # Test for exclude patterns */
            if (xpat != []):
                idx = 0
                for pat in xpat.xpat:
                    if (str(pat) in str(scale_steps)):
                        unique = 0
                        break
            # Test for duplicates */
            if (unique == 1):
                dscale = ""
                idx = 0
                while (idx < 2 *sn_scale_len):
                    dscale += scale_steps[idx]
                    idx += 1
                if (scales.find_dupe(dscale) == 1):
                    unique = 0
            # Add to list of scales */
            if (unique == 1):
                if (scale_cnt >= sn_first_scale):
                    scale_ucnt += 1
                    jdx = 0
                    idx = 0
                    while (idx < sn_scale_len):
                        if (first_time == 1):
                            newscale.append(scale_steps[idx])
                            newidx.append(jdx)
                        else:
                            newidx[idx] = jdx
                            newscale[idx] = scale_steps[idx]
                        jdx += scale_arr[idx]
                        idx += 1
                    first_time = 0
                    # Add to scale list */
                    ns = newscale[:]
                    ni = newidx[:]
                    scales.add_scale(''.join(ns), ni)
                    scalesz += 1

        # Increment last element, if greater than max_interval, increment
        # previous and reset current to 1
        idx = sn_scale_len - 1
        while (idx >= 0):
            if (idx == 0 and scale_arr[idx] == sn_max_interval):
                done = 1
                break
            elif (scale_arr[idx] < sn_max_interval):
                scale_arr[idx] += 1
                break
            else:
                scale_arr[idx] = 1
            idx -= 1
        if (scale_ucnt == sn_max_scales):
            done = 1

    print "."
    sys.stdout.flush()
    return 0


def parse_staffs():
    """
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
Function: parse_staffs
Description:
  Parse the scale example file which contains the following staff parameters:
  - Instrument
  - Notes
  - Start and Duration
  - Volume

  The scale example file is used to produce multiple staff files for different
  scales which can then be compared.
Inputs:
  - None
Outputs:
  - int: Status
    - 0 = OK
    - <0 = Error
    """

    global staffs

    try:
        sfd = open(sfile, 'r')
    except IOError as e:
        print "Error failed to open staff examples file ", sfile
        print "  ", e
        return -1

    lines = sfd.readlines()
    for line in lines:
    # Check for blank lines and comments
        if (line[0] == '#' or line[0] == '\0' or line[0] == '\n'):
            continue
        else:
            nd = line.split()

        if (nd[0] == "STAFF"):
            newstaff = csnd_snobjP2.snStaff(line.rstrip('\n'))
            staffs.append(newstaff)
        elif (nd[0] == "INSTR"):
            if (newstaff == []):
                print "Error: No staff for instrument: ", line
                return -1
            newstaff.add_instr(line.rstrip('\n'))
        elif (nd[0] == "FUND"):
            fund_def = (nd[1], nd[2], nd[3], nd[4])
            newstaff.add_fund(fund_def)
        elif (nd[0] == "NEXT"):
            newstaff.add_next(nd[1])

    sfd.close()

    return 0


def modify_staffnote(notecode, sidx):
    """
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
Function: modify_staffnote
Description:
  Parse a note code and return the note name.
Inputs:
  - notecode: <octave>:<noteidx>
    - octave: 0 - 9
    - noteidx: 0 - 999
Outputs:
  - String
    - Note name: 1 or 2 characters
    - Error message
    """

    if (len(notecode) == 3):
        ntidx = notecode[2]
    elif (len(notecode) == 4):
        ntidx = notecode[2] + notecode[3]
    elif (len(notecode) == 5):
        ntidx = notecode[2] + notecode[3] + notecode[4]
    else:
        rtnerr = "Error: Invalid note code: " + notecode
        return rtnerr

    noteidx = int(ntidx)
    if (type(noteidx) != int):
        rtnerr = "Error converting note code: " + notecode
        return rtnerr
    newnt = note_defs[sidx[noteidx]]

    return newnt


def create_stafffile():
    """
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
Function: create_stafffile
Description:
  Using the example file data create a csg_staves file for every scale
  generated by the get_unique_scales function.
Inputs:
  - None
Outputs:
  - int: Status
    - 0 = OK
    - <0 = Error
    """

    loopcnt = 0
    gsz = sn_group_size
    sn_group_interval = 0.0
    stime = 0.0
    print "Creating staff files: ",
    for sc in scales.scales:
        if ((loopcnt & 0xfff) == 0):
            print ".",
            sys.stdout.flush()
        loopcnt += 1
        if (gsz >= sn_group_size):
            gsz = 1
            sn_group_interval = 0.0
            try:
                chfile = vfile + "." + str(sc)
                vfd = open(chfile, 'w')
            except IOError as e:
                print "."
                print "Error failed to open csg_staves file ", chfile
                print "  ", e
                return -1
            vfd.write("# These staff definitions were generated by the Scale Notes Generator\n\n")
        else:
            gsz += 1

        for chd in staffs:
            chline = '\n' + chd.staff + '_' + sc + '\n'
            vfd.write(chline)
            chline = chd.instr + '\n'
            vfd.write(chline)
            si = scales.get_idx(sc)
            for nt in chd.notes:
                ntname = modify_staffnote(nt[0], si)
                if (len(ntname) > 3):
                    # Notename is error message
                    print "."
                    print ntname
                    return -1
                stime = float(nt[1]) + sn_group_interval
                chfund = "FUND  " + nt[0][0] + ntname + "  " + str(stime) + "  " + nt[2] + "  " + nt[3] + '\n'
                vfd.write(chfund)
            sn_group_interval += chd.next

        if (gsz >= sn_group_size):
            vfd.close()

    print "."
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
    print '  csnd_snP2.py Version', sn_ver
    print '\n'
    print '  csnd_snP2.py [arguments]:'
    print '  -n: note_file: Name of note file'
    print '      Default: ', nfile
    print '  -s: scale_file: Name of scale example file'
    print '      Default: ', sfile
    print '  -v: staff_file: Name of staff file'
    print '      Default: ', vfile
    print '  -l: number: Length of scale (excluding octave)'
    print '      Range: 1 - 99, Default: ', sn_scale_len
    print '  -i: number: Maximum interval'
    print '      Default: ', sn_max_interval, '(major 3rd), maximum: 25 (fourteenth)'
    print '  -f: number: First scale to generate'
    print '      Default: 1, maximum: ', sn_max_scales
    print '  -m: number: Maximum number of scales to generate'
    print '      Default: all, maximum : ', sn_max_scales
    print '  -x: string: Step pattern to exclude may be entered multiple times'
    print '      Examples: -x\"hhh\" -x\"whw\"'
    print '  -g: number: Number of scales to group in a staves file'
    print '      Default: 1'
    print '  -k: Skip staff file generation'
    print '  -d: debug code: Note = 1, Scales = 2, Staff = 4, Patterns = 8'
    print '      Values can be ORed for multiple printouts'
    print '  -D: Display developer information, main is described at the end'
    print '  Note: Patterns are tested in the order entered, so it is more'
    print '        efficient to enter frequently used patterns first'
    print '\n'
    print '  NOTE: Scale names are the list of intervals where:'
    print '    h = half tone, w = whole tone, m = minor 3rd, M = major 3rd, f = fourth,'
    print '    d = diminished fifth, F = fifth, a = augmented fifth, s = sixth,'
    print '    A = augmented sixth, S = seventh, j = major seventh, e = eighth,'
    print '    n = diminished ninth, N = ninth, t = diminished tenth, T = tenth,'
    print '    v = diminished eleventh, V = eleventh, l = diminished twelfth, L = twelfth,'
    print '    r = diminished thirteenth, R = thirteenth, o = diminished fourteenth, O = fourteenth'
    print '    Example: csg_staves.whMhmww'

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
        opts, args = getopt.gnu_getopt (sys.argv[1:], 'd:Ds:n:v:f:g:i:km:l:x:')
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(1)

    # Debug: Notes = 1, Template = 2, Staffs = 4
    debug = 0
    skip_staffs = 0

    # Parse command line arguments
    for opt, optarg in opts:
        if opt in ['-v']:
            vfile = optarg
        elif opt in ['-k']:
            skip_staffs = 1
        elif opt in ['-d']:
            debug = int(optarg)
        elif opt in ['-s']:
            sfile = optarg
        elif opt in ['-n']:
            nfile = optarg
        elif opt in ['-f']:
            sn_first_scale = int(optarg)
        elif opt in ['-g']:
            sn_group_size = int(optarg)
        elif opt in ['-i']:
            sn_max_interval = int(optarg)
            if (sn_max_interval > 25):
                print "Error: invalid interval size: ", optarg
                sys.exit(0)
        elif opt in ['-m']:
            sn_max_scales = int(optarg)
        elif opt in ['-l']:
            sn_scale_len = int(optarg)
            if (sn_scale_len < 0 or sn_scale_len > 512):
                print "Error: invalid scale length: ", optarg
                sys.exit(0)
        elif opt in ['-x']:
            xpat_defs.append(optarg)
        elif opt in ['-D']:
            dev_help()
            sys.exit(0)

    print "\nStarting CSound Scale Notes Generator\n"

    xpat = csnd_snobjP2.snPattern()
    for xp in xpat_defs:
        xpat.add_pat(xp)

    if (parse_notes() != 0):
        sys.exit(1)
    if (debug & 1 == 1):
        print "Note definitions"
        print note_defs

    if (get_unique_scales() != 0):
        sys.exit(1)
    if (debug & 2 == 2):
        print "Exclude patterns: "
        xpat.print_data()
        print "Scale definitions: ", scalesz
        scales.print_data()

    if (skip_staffs == 0):

        if (parse_staffs() != 0):
            sys.exit(1)
        if (debug & 4 == 4):
            print "Staff definitions: "
            for chdef in staffs:
                chdef.print_data()

        if (create_stafffile() != 0):
            sys.exit(1)

    print "\nCompleted CSound Scale Notes Generator for ", len(scales.scales), " scales\n"


