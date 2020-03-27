import argparse
import sys

from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2 import utils  # .PdfReadError

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='a terminal tool for easy PDF file spliting')
    parser.add_argument('-i', '--input', type=str,
                        help='PDF file to split', dest='input')
    parser.add_argument('-s', '--start', type=int,
                        help='PDF page to start (inclusive)', dest='start')
    parser.add_argument('-e', '--end', type=int,
                        help='PDF page to end (inclusive)', dest='end')
    parser.add_argument('-o', '--output', type=str,
                        help='name of output file', dest='output', required=False, default='out.pdf')

    args = parser.parse_args()

    if args.input is None:
        print('{}: an input file is required'.format(sys.argv[0]))
        print('usage: pcut --help')
        sys.exit(1)

    if args.start is None:
        print('{}: i don\'t know where to start cutting')
        print('usage: pcut --help')
        sys.exit(1)
    elif args.start < 0:
        print('{}: i cannot cut imaginary content!')
        print('usage: pcut --help')
        sys.exit(1)

    if args.end is None:
        print('{}: i don\'t know where to stop cutting')
        print('usage: pcut --help')
        sys.exit(1)
    elif args.end < args.start:
        print('{}: sorry, but I cannot break physics law... yet')
        print('usage: pcut --help')
        sys.exit(1)

    try:
        with open(args.input, 'rb') as pdf_file:
            file_reader = PdfFileReader(pdf_file)

            # Let's check if start and end arguments make sense.
            file_pages_number = file_reader.getNumPages()
            if args.start > file_pages_number:
                print('{}: this file only has {} pages, cannot start cutting at page {}'.format(
                    sys.argv[0], file_pages_number, args.start))
                sys.exit(1)
            elif args.end > file_pages_number:
                print('{}: this file only has {} pages, cannot end cutting at page {}'.format(
                    sys.argv[0], file_pages_number, args.end))
                sys.exit(1)

            output_pdf = PdfFileWriter()
            for i in range(args.start, args.end):
                page = file_reader.getPage(i)
                output_pdf.addPage(page)

            output_file = open(args.output, 'wb')
            output_pdf.write(output_file)
            output_file.close()
    except FileNotFoundError:
        print('{}: file \"{}\" not found'.format(sys.argv[0], args.input))
    except utils.PdfReadError:
        print('{}: that is not a PDF!'.format(sys.argv[0]))
