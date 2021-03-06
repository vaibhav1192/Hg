#!/usr/bin/env python
# encoding: utf-8

"""A simple script to turn a normal PDF file into a booklet.

Usage:
    - write_booklet.py original.pdf booklet.pdf

Requirements:
   - pyPdf (http://pybrary.net/pyPdf/)
   - pdfjam (http://www.warwick.ac.uk/go/pdfjam)

Ideas: 
   - rename to pdf2booklet.py
   - Accompanying skripts: create release
	* add the license and the charsheet to the PDF as online-release
	* add the license and charsheet into the middle of the PDF and turn it into a booklet

current process for creating a release booklet: 
    pdfnup ../../releases/ews-dok-2.3.6.pdf --nup 1x1 --pages 1-24 --outfile part1.pdf ; pdfnup ../../releases/ews-dok-2.3.6.pdf --nup 1x1 --pages 25-48 --outfile part2.pdf ; pdfnup ../GPLv3.pdf --nup 1x1 --pages 1-2 --outfile gpl-1.pdf; pdfnup ../GPLv3.pdf --nup 1x1 --pages 3-4 --outfile gpl-2.pdf; pdfnup ../../releases/charheft-vobsy.pdf --nup 1x1 --pages 2,3,4,1 --outfile charheft.pdf ; pdfjoin part1.pdf gpl-1.pdf charheft.pdf gpl-2.pdf part2.pdf --outfile test.pdf
    
    ./write_booklet_pdfjam.py test.pdf booklet.pdf

current prcess for creating a release PDF for screen viewing: 
    pdfjoin ../../releases/release.pdf ../GPLv3.pdf ../../releases/charheft-vobsy.pdf --outfile release.pdf

"""

__copyright__ = """write booklet - Turn a pdf file into a booklet for printing. 

    Copyright © 2009 Arne Babenhauserheide
 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

# First we need to parse the commandline arguments
from sys import argv
# If the user requests help or doesn't provide enough commandline arguments
# We output the docstring as help and short usage info. 
if "--help" in argv or not argv[2:]:
    print __doc__
    exit()

# check for options
if "--double-size" in argv:
    double_size = True
    argv.remove("--double-size")
else:
    double_size = False

#: The infile PDF
infile = argv[-2]
#: The booklet to be
outfile = argv[-1]

# Also we need to be able to call programs 
from subprocess import call

# and the pyPDF library (for the number of pages)
from pyPdf import PdfFileWriter, PdfFileReader

# Read the file
input1 = PdfFileReader(file(infile, "rb"))

#: The number of pages
num_pages = input1.numPages

# They _must_ be divisible by 4!
assert(not num_pages % 4)

# Now out job is sorting the pages
#: The page numbers how they should appear in the final pdf
page_order = []
# First we need the last and the first page. 
page_order.append(num_pages - 1)
page_order.append(0)

# Now we need to add the _middle_ pages in batches of 4 pages
for quad in range(num_pages / 4 - 1):
    page_order.append(2*quad + 1)
    page_order.append(num_pages - quad*2 - 2)
    page_order.append(num_pages - quad*2 - 3)
    page_order.append(2*quad + 2)

# And add the middle pages
page_order.append(num_pages / 2 - 1)
page_order.append(num_pages / 2)

# Since pdfjam counts from 1 onwards, we need to increase allpage numbers by one
page_order = [i+1 for i in page_order]

# Also we turn them to strings
page_order = [str(i) for i in page_order]

# And create our pages string
pages_string = ",".join(page_order)

# Now we only need to compile the pdfnup call string.

call_list = ["pdfnup", "--nup", "2x1", "--paper", "a4paper", "--outfile", outfile, "--", infile, pages_string]

# print call_list

call(call_list)
