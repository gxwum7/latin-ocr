# Latin OCR
This is my attempt to fine-tune the Tesseract Latin model to work better, particularly with macrons, as the current official model does not work very well on my targeted scanned books.
My best models are provided in the 'best' directory on this repository.

The training data for the fine-tune is generated from fonts, so although some noise and distortion will be added to account for lower quality scans, this method will probably not work on very badly scanned books or on handwritten manuscripts (I am working on a way to OCR those).

The generate script is a small modification of a script made by r2d4 in this [repository](https://github.com/r2d4/osrs-ocr).

## Guide
Fine-tuning your own model is pretty easy to do, you just need to have all the requirements and follow the steps bellow (with some modifications to suit your particular case). Keep in mind that I only did on Linux (specifically Arch), so even though it might be possible to do on Windows and Mac (with Msys2 or Cygwin on Windows), I have not tested it and it will probably be easier to use a VM if Linux is not available.

If you encounter any problem in any of the steps, please open an issue and I'll try to help as soon as possible.

### Requirements
- A text file with base text seperated into different lines (an example is the ceasar.txt file with the first paragraph of Caesar's De Bello Gallico) - used to generate the training data together with the fonts.
- Fonts, all the fonts you intend to use should be downloaded and inside a fonts directory in this repository, the fonts also need to be installed on your system (you can use your package manager for that) - used to generate the training material and so should be similar to the font of your target book (you should use as many fonts as possible for better results, though don't just put hundreds of random fonts as the generating script will take a lot of time).
- Tesseract - you'll need Tesseract installed for this to work, you should consult the installation intructions of Tesseract to learn how to achieve this.

### Configuring
The [Tesstrain]() repository should be cloned in here.

You need to add your chosen fonts' names in the 'fonts' list in the generate.py file. To find out the names of the fonts you can use the program ```text2image``` that comes with Tesseract:
```# text2image --list_available_fonts --fonts_dir=./fonts```

Run this command in the Tesstrain repository:
```# make tesseract-langdata```

You also need to create a ```usr/share/tessdata/``` directories in the directory of the repository and put the base model that will be fine tuned, they can be found in the [tessdata_best](https://github.com/tesseract-ocr/tessdata_best) repository.

### Generating the training data
Generating the training data is as simple as running the ```generate.py``` script. Keep in mind that it could take some time, depending on the amount of text and fonts. It will also eat your entire cpu, there probably is a way to limit its use of resources, but I haven't bothered as it does not work for that long (a half hour perhaps).

After everything is generated rename the ```out``` directory with the data to a ```data/[MODEL_NAME]-ground-truth``` in the Tesstrain repository.

### Fine-tune the model
This stage will take the longest, here we actually train the model, so if you can leave it running overnight it would be best, though you can stop and continue the training whenever you like, as it regularly saves checkpoints. You also could just start the training and continue using the computer regularly, as it doesn't consume too much resources.

This command will start the fine-tuning:
```# make -r training START_MODEL=lat TESSDATA=usr/share/tessdata/ MAX_ITERATIONS=5000000 MODEL_NAME=lat_new RATIO_TRAIN=0.99```

To get to an actually good model it will probably take close to a day (maybe more), but you could test it anytime you want.
To test the current best model you need to build the .traineddata file from the checkpoints with this command:
```# make traineddata MODEL_NAME=[name]```

And use the generated file as the model for OCRing like you would normally do with the Tesseract program.

### OCRing
To actually OCR the pdf I have used [OCRmypdf](https://github.com/ocrmypdf/OCRmyPDF) which uses Tesseract in the background, as Tesseract itself does not support inputing a pdf and writing a script for that would have been redundent. You could use OCRmypdf to generate a text file directly, though I prefer having it generate the HOCR files which would be used in the next stage for proofreading (an HOCR file keeps the position of the OCRed text on the pdf and the confidence of the OCR on particular lines as well as the actual text, so they are useful for the proofreading program).

OCRmypdf does not actually have a direct option to export to HOCR, so we need to specify to it to keep its temporary files (as it uses HOCR as an intermediary step) so we could use them:
```# ocrmypdf --force-ocr --keep-temporary-files [input].pdf out.pdf```

Then it's just a matter of finding the temporary directory (usually in /tmp) and copying the .hocr and image files of each page of the pdf.

### Proofreading
The last stage is proofreading - you can't rely on the OCR to be 100% accurate (though it is pretty good on scans of good quality), so there is still need to proofread the results.
I like the [Scribeocr](https://github.com/scribeocr/scribeocr) program, as it makes it very convenient (one of my aims is to rewrite this program to work better) to proofread. You can use the web version and when selecting files select all the hocr and image files generated in the previous step.
