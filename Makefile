#
# Makefile for CSound Generator and CSound Scale Notes
#
# Copyright 2021 Jim Sansing
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
#

VER = 1.0

SRC_DIR=./src

CSG_SRCS = csnd_generate.c

CSG_OBJS = csnd_generate.o

CSG_PROGRAM = csnd_gen

SN_SRCS = csnd_scale_notes.c

SN_OBJS = csnd_scale_notes.o

SN_PROGRAM = csnd_sn

CC = gcc

CFLAGS = -O2 -Wall

DFLAGS = -g -Wall

UID=`id -u`

all: csnd_gen csnd_sn

$(CSG_PROGRAM):
	cd $(SRC_DIR) && $(CC) $(CFLAGS) -o $(CSG_PROGRAM) $(CSG_SRCS) && mv $(CSG_PROGRAM) ../.
	chmod 755 csnd_gen

$(SN_PROGRAM):
	cd $(SRC_DIR) && $(CC) $(CFLAGS) -o $(SN_PROGRAM) $(SN_SRCS) && mv $(SN_PROGRAM) ../.
	chmod 755 csnd_sn

debug:
	cd $(SRC_DIR) && $(CC) $(DFLAGS) -o $(CSG_PROGRAM).debug $(CSG_SRCS) && mv $(CSG_PROGRAM).debug ../.
	cd $(SRC_DIR) && $(CC) $(DFLAGS) -o $(SN_PROGRAM).debug $(SN_SRCS) && mv $(SN_PROGRAM).debug ../.

clean:
	rm -f *.o *.debug $(CSG_PROGRAM) $(SN_PROGRAM)

install: $(CSG_PROGRAM) $(SN_PROGRAM)
	@if [ $(UID) != 0 ]; then\
	  echo "This must be run by superuser" ;\
	  exit 1 ;\
	fi
	cp csnd_gen /usr/bin/csnd_gen-$(VER)
	ln -s /usr/bin/csnd_gen-$(VER) /usr/bin/csnd_gen
	cp csnd_sn /usr/bin/csnd_sn-$(VER)
	ln -s /usr/bin/csnd_sn-$(VER) /usr/bin/csnd_sn
	@if [ -d /usr/share/man ]; then\
		cp csnd_gen.8.gz csnd_sn.8.gz /usr/share/man/man8/. ;\
	fi
clean_install:
	@if [ $(UID) != 0 ]; then\
	  echo "This must be run by superuser" ;\
	  exit 1 ;\
	fi
	rm /usr/bin/csnd_gen /usr/bin/csnd_gen-$(VER)
	rm /usr/bin/csnd_sn /usr/bin/csnd_sn-$(VER)
	@if [ -f /usr/share/man/man8/csnd_gen.8.gz ]; then\
		rm /usr/share/man/man8/csnd_gen.8.gz /usr/share/man/man8/csnd_sn.8.gz ;\
	fi



