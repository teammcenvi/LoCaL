
# Python Version

Python 3.6.8

# Python environment with a requirements.txt

The `requirements.txt` file should list all Python libraries that your notebooks
depend on, and they will be installed using:

```
pip install -r requirements.txt
```

# Tesseract OCR

This need to install within the OS or a container where the python pytesseract are installed.
This package contains an OCR engine - libtesseract and a command line program - tesseract. Tesseract 4 adds a new neural net (LSTM) based OCR engine which is focused on line recognition, but also still supports the legacy Tesseract OCR engine of Tesseract 3 which works by recognizing character patterns. Compatibility with Tesseract 3 is enabled by using the Legacy OCR Engine mode (--oem 0). It also needs traineddata files which support the legacy engine, for example those from the tessdata repository.

# About the Sample_Product_Images

The product images will be used to upload sample food products that the LoCaL App will process.  This is part of the proof of concept.
