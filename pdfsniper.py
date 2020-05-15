#!/usr/bin/python3

'''
    pdfsniper.py - PDF to text.

    | EXTRACT | CRACK | ENCRYPT | READ

    Author: catx0rr

    SEE: Usage below.

    !! DEPENDECIES !!
    pdfsniper pdftotext module:
        Linux: libpoppler
               - sudo apt-get install libpoppler-cpp-dev
        Windows: Microsoft Visual C++ 14.0
               - Get it with "Microsoft Visual C++ Build Tools": https://visualstudio.microsoft.com/downloads/
        Python3: PyPDF2, getpass, pikepdf, re and sys modules.

    !! ISSUES !!
    Decrypt option: Some of encryption algorithm is not supported as per PyPDF2
        NotImplementedError: only algorithm code 1 and 2 are supported.

    Note: Tried on some encrypted pdf and used a well known passwordlist, worked as it should be.

    SEE: Issues on these pages.
        github: https://github.com/mstamy2/PyPDF2/issues/53
                https://github.com/mstamy2/PyPDF2/issues/378

        stackoverflow:
                https://stackoverflow.com/questions/50751267/only-algorithm-code-1-and-2-are-supported


    !! DOCUMENTATIONS !!
        PyPDF2: https://pythonhosted.org/PyPDF2/PdfFileReader.html
        pdftotext: https://pypi.org/project/pdftotext/

'''

import argparse
import getpass
import pdftotext
import pikepdf
import PyPDF2
import re
import sys


FAILED = '\033[31m[-]\033[0;0m'
SUCCESS = '\033[32m[+]\033[0;0m'
PROMPT = '\033[36m[>]\033[0;0m'
WORKING = '\033[33m[*]\033[0;0m'

file_gex = re.compile(r'[a-zA-Z0-9._-]+\.[a-zA-Z]')

page_break = '\n\n------------------------------------//  P A  G  E    B  R  E  A  K  //------------------------------------\n\n'

def count(file):

    # Read pdf, read as binary ('rb') and output how many pages. Uses PyPDF2 module.

    try:
        with open(file, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            print('%s %s page(s) count: %s' % (SUCCESS, file, pdf_reader.numPages))

        pdf_file.close()

    except PyPDF2.utils.PdfReadError:
        print('%s Unable to count %s Please check if the file is encrypted.' % (FAILED, file))

    except FileNotFoundError:
        print('%s %s not found.' % (FAILED, file))


def read(file, page):

    # Read every page supplied by the page number using pdftotext module. Index of zero.

    prompt = '%s Opened to page: %s'

    try:
        with open(file, 'rb') as pdf_file:
            pdf_reader = pdftotext.PDF(pdf_file)

            print(pdf_reader[int(page)] + '\n\n' + prompt % (SUCCESS, page))

        pdf_file.close()

    except pdftotext.Error:
        print('%s Unable to read %s Please check if the file is encrypted.' % (FAILED, file))

    except IndexError:
        print('%s Page %s not found.' % (FAILED, page))

    except FileNotFoundError:
        print('%s %s not found.' % (FAILED, file)) - 9


def read_page(file):

    # Read continously per page. Uses pdftotext module.

    page = 0

    prompt = '%s Turned to page: %s'
    prompt += '\n%s Type \'quit\' to end reading session'
    prompt += '\n%s Type a page number to jump or (n/p) to turn next or previous page: '

    try:
        with open(file, 'rb') as pdf_file:
            pdf_reader = pdftotext.PDF(pdf_file)

            while True:
                try:
                    print(page_break + pdf_reader[page])

                    # Check for page events
                    page_num = input(prompt % (SUCCESS, page, PROMPT, PROMPT))

                    if page_num == 'n' or page_num == 'a':
                        page += 1
                        continue

                    elif page_num == 'p' or page_num == 's':
                        page -= 1
                        continue

                    elif page_num.isdigit():
                        page = int(page_num)
                        continue

                    elif page_num == 'quit' or page_num == 'exit' or page_num == 'q':
                        break

                    else:
                        print('%s Incorrect option. press \'n\' or \'p\'.' % (FAILED))
                        continue

                except IndexError:
                    print('%s Page %s not found.' % (FAILED, page))

    except pdftotext.Error:
        print('%s Unable to read %s Please check if the file is encrypted.' % (FAILED, file))

    except FileNotFoundError:
        print('%s %s not found.' % (FAILED, file))


def read_all(file):

    # Read all the pages of pdf file using pdftotext module.

    try:
        with open(file, 'rb') as pdf_file:
            pdf_reader = pdftotext.PDF(pdf_file)

            # Iterate over the pages and print on the terminal
            for pdf_page in pdf_reader:
                print(pdf_page + page_break)

        pdf_file.close()

    except pdftotext.Error:
        print('%s Unable to read %s Please check if the file is encrypted.' % (FAILED, file))

    except FileNotFoundError:
        print('%s %s not found.' % (FAILED, file))


def extract(file):

    # Extracts all text in the pdf file. pdftotext module is required.

    name_text = file.replace('.pdf', '.txt')

    print('%s Working on %s file..' % (WORKING, file))

    try:
        with open(file, 'rb') as pdf_file, open(name_text, 'a') as text_file:
            pdf_reader = pdftotext.PDF(pdf_file)

            # Iterate and write on a file
            for pdf_page in pdf_reader:
                text_file.write(pdf_page + page_break)

        pdf_file.close()
        text_file.close()
        print('%s %s has been extracted to %s.' % (SUCCESS, file, name_text))

    except pdftotext.Error:
        print('%s Unable to extract %s Please check if the file is encrypted.' % (FAILED, file))

    except FileNotFoundError:
        print('%s %s not found.' % (FAILED, file))


def check_crypt(file):

    # Check if the file is password protected. PyPDF2 module is needed.

    try:
        with open(file, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)

            if pdf_reader.isEncrypted:
                print('%s %s is password protected.' % (SUCCESS, file))

            else:
                print('%s %s is not encrypted.' % (SUCCESS, file))

        pdf_file.close()

    except FileNotFoundError:
        print('%s %s not found.' % (FAILED, file))


def bin_extract(file):

    # Extracts the binary target pdf file and output it into a text file uses PYPDF2.

    name_text = file.replace('.pdf', '_bin.txt')

    print('%s Working on %s pdf file..' % (WORKING, file))

    try:
        with open(file, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)

            # Create an writer object to add pages of current pdf file
            pdf_writer = PyPDF2.PdfFileWriter()

            # iterate on the pages of current pdf file
            for page_num in range(pdf_reader.numPages):
                page_object = pdf_reader.getPage(page_num)

                pdf_writer.addPage(page_object)

        # Create a empty text file and write the pages from current pdf file
        with open(name_text, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
            print('%s %s extracted to %s file.' % (SUCCESS, file, name_text))

        output_pdf.close()
        pdf_file.close()

    except PyPDF2.utils.PdfReadError:
        print('%s Unable to extract %s Please check if the file is encrypted.' % (FAILED, file))

    except FileNotFoundError:
        print('%s %s not found.' % (FAILED, file))


def decrypt(file, passwd_file):

    # Open the pdf file and the password file and check for passwords inside using PyPDF2 module.

    pass_found = None

    try:
        pdf_reader = PyPDF2.PdfFileReader(open(file, 'rb'))
        with open(passwd_file, 'r') as pass_file:

            # Iterate in every line of the opened password list and list the index and the password if found.
            for index, line in enumerate(pass_file):

                password = line.strip()
                if pdf_reader.decrypt(password) == 1:
                    pass_found = password
                    break

                else:
                    print('%s Line: %s No match found..' % (WORKING, index))

            # Check if pass_found has a value

            if not pass_found:
                print('%s Done: None match on %s file.' % (FAILED, passwd_file))

            else:
                print('%s Done: %s Password Found: %s' % (SUCCESS, index, pass_found))

        pass_file.close()

    except KeyError:
        print('%s %s not encrypted.' % (FAILED, file))

    except FileNotFoundError:
        print('%s PDF or password file not found.' % (FAILED))

    except NotImplementedError:
        print('%s ERROR: Password Hash not supported. Please see issues.' % (FAILED))


def encrypt(file, password):

    # Encrypts the pdf using PyPDF2 module

    try:

        name_pdf = file.replace('.pdf', '_encrypted.pdf')

        # Load the pdf writer and reader
        pdf_reader = PyPDF2.PdfFileReader(file)
        pdf_writer = PyPDF2.PdfFileWriter()
        pdf_pages = pdf_reader.getNumPages()

        print('%s Working on %s pdf file..' % (WORKING, file))

        # Get the page of loaded pdf file
        for page in range(pdf_pages):
            pdf_writer.addPage(pdf_reader.getPage(page))

        # Encrypt the password with the passed argument
        pdf_writer.encrypt(user_pwd=password, owner_pwd=None, use_128bit=True)

        # Output the encrypted product pdf
        with open(name_pdf, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

        output_pdf.close()
        print('%s Done. %s saved on current working directory.' % (SUCCESS, name_pdf))

    except PyPDF2.utils.PdfReadError:
        print('%s Unable to encrypt %s You cannot encrypt an unencrypted file.' % (FAILED, file))

    except FileNotFoundError:
        print('%s %s not found.' % (FAILED, file))


def strip(file, password):

    # Removes the password of pdf using pikepdf module

    try:

        name_pdf = file.replace('.pdf', '_decrypted.pdf')

        print('%s Working on %s file..' % (WORKING, file))

        with pikepdf.open(file, password) as pdf_clean:
            pdf_clean.save(name_pdf)

            print('%s Successfully removed password. Saved as %s' % (SUCCESS, name_pdf))
            pdf_clean.close()

    except pikepdf._qpdf.PasswordError:
        print('%s Unable to remove protection. Invalid password.' % (FAILED))

    except FileNotFoundError:
        print('%s %s not found.' % (FAILED, file))


def check_pass(file):

    while True:
        passwd = getpass.getpass('%s Enter password for %s: ' % (PROMPT, file))
        re_passwd = getpass.getpass('%s Confirm password for %s: ' % (PROMPT, file))

        if not passwd:
            print('%s Password must not be empty.' % (FAILED))
            continue

        if not re_passwd:
            print('%s Password must not be empty.' % (FAILED))
            continue

        if passwd == re_passwd:
            if len(passwd) < 4:
                print('%s Password must be at least 4 characters.' % (FAILED))
                continue

            return passwd
            break

        else:
            print('%s Passwords did not match.' % (FAILED))


def check_pwfile(pwfile):

    try:
        if file_gex.search(pwfile).group():
            return pwfile

    except AttributeError:
        print('%s Invalid password file.' % (FAILED))
        sys.exit(1)


def main():

    # Create a parser
    parser = argparse.ArgumentParser(
        description='Work with pdf files using the terminal. Extract text files, read continuosly on the page, encrypt files, decrypt and strip the password of the pdf file.',
        allow_abbrev=False
    )

    # Create group of arguments for usage
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        '-c', '--count',
        metavar='',
        help='Count the number of pages of the selected pdf file.')

    group.add_argument(
        '-r', '--read',
        nargs=2,
        metavar='',
        help='Read and prints the pdf page in the terminal. A password is required as fourth argument. ')

    group.add_argument(
        '-p', '--read-page',
        dest='readpage', metavar='',
        help='Creates a session and read the pdf continously on the terminal.')

    group.add_argument(
        '-a', '--read-all',
        dest='readall',
        metavar='',
        help='Read and prints all page content on the terminal.')

    group.add_argument(
        '-x', '--extract',
        metavar='',
        help='Extracts all text in the pdf file and writes it in a .txt file.')

    group.add_argument(
        '-t', '--check-crypt',
        dest='checkcrypt',
        metavar='',
        help='Check if the file is encrypted.')

    group.add_argument(
        '-b', '--extract-binary',
        dest='extbinary',
        metavar='',
        help='Extracts pdf binaries to work with.')

    group.add_argument(
        '-e', '--encrypt',
        metavar='',
        help='Encrypts an unencrypted pdf file with a desired password.')

    group.add_argument(
        '-d', '--decrypt',
        metavar='',
        nargs=2,
        help='Performs a brute force attack to the pdf file using a password list as fourth argument.')

    group.add_argument(
        '-s', '--strip',
        metavar='',
        nargs=2,
        help='Strips the password on the pdf file. A password is required as fourth argument.')

    args = parser.parse_args()

    # Check for parsed arguments

    if args.count:
        count(args.count)
        sys.exit(0)

    if args.read:
        read(args.read[0], args.read[1])
        sys.exit(0)

    if args.readpage:
        read_page(args.readpage)
        sys.exit(0)

    if args.readall:
        read_all(args.readall)
        sys.exit(0)

    if args.extract:
        extract(args.extract)
        sys.exit(0)

    if args.checkcrypt:
        check_crypt(args.checkcrypt)
        sys.exit(0)

    if args.extbinary:
        bin_extract(args.extbinary)
        sys.exit(0)

    if args.encrypt:
        encrypt(args.encrypt, check_pass(args.encrypt))

    if args.decrypt:
        decrypt(args.decrypt[0], check_pwfile(args.decrypt[1]))
        sys.exit(0)

    if args.strip:
        strip(args.strip[0], args.strip[1])
        sys.exit(0)


if __name__ == '__main__':
    main()
