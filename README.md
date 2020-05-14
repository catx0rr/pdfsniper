# PDF Sniper 🏹

## Extract | Crack | Encrypt | Read 

---

## NOTES

Feel free to use and modify this file. Documentations are listed [below](### DOCUMENTATIONS)

### DEPENDECIES

#### pdftotext module:

Linux: libpoppler

- ```$ sudo apt-get install libpoppler-cpp-dev```
        
Windows: Microsoft Visual C++ 14.0
- [Get it with Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/downloads/)

Python:
- Required dependencies:
    - ```pip3 install PyPDF2```
    - ```pip3 install pdftotext```
    - ```pip3 install pikepdf```
    - ```pip3 install getpass```

For Installation Issues in pikepdf:
- Donwload Fix / Upgrade pip:
    - ```python3 -m pip install --upgrade pip```
    - ```python3 -m pip install pikepdf```

---

### UPDATES
- Added some `colors` for more interactive result.
- Added `readpage` function to continuously read on a pdf as text.
- Added `strip` function to unprotect pdf file using the correct password.

```strip  -- Strips the password on the pdf file. A password is needed in fourth argument.```

---

### BUGFIX
- `IndexError` on readpage and read functions

---

### ISSUES / LIMITATIONS
Decrypt option: 

- Some of encryption algorithm is not supported as per PyPDF2 module.     

Note: 
- Tried on most encrypted pdf and used a well known passwordlist, worked as it should be.

SEE: Issues on these pages.
- github: [PyPDF2 Issue on Github 53](https://github.com/mstamy2/PyPDF2/issues/53) | [PyPDF2 Issue on Github 378](https://github.com/mstamy2/PyPDF2/issues/378)

stackoverflow:
- [Stackoverflow Algorithm code 1 and 2](https://stackoverflow.com/questions/50751267/only-algorithm-code-1-and-2-are-supported)

---

### DOCUMENTATIONS

- [PyPDF2](https://pythonhosted.org/PyPDF2/PdfFileReader.html)
- [pdftotext](https://pypi.org/project/pdftotext/)
- [pikepdf](https://pypi.org/project/pikepdf/)


---

### EXAMPLES

Sample of decrypting a pdf using dictionary
![decrypt sample](https://github.com/catx0rr/python-scripts/blob/master/pdfsniper/images/decrypt.PNG)

Password has been decrypted using a well known dictionary
![decrypted sample](https://github.com/catx0rr/python-scripts/blob/master/pdfsniper/images/decrypted.PNG)

Sample of readpage function as reading session inside the pdf file
![extracted sample](https://github.com/catx0rr/python-scripts/blob/master/pdfsniper/images/readpage.PNG)

---

### FUTURE UPDATES 

~~Will add a password remover so the text can be extracted on the pdf file.~~ Done.
