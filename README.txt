SCANNING SKETCHES
-----------------

I scan the sketches on an EPSON V600 photo scanner.

I don't remember all of the settings I used for the first round of scans,
except that I did them all at 800dpi.

    Resolution: 800dpi
    Image size: ?
    Name: p
    Format: JPEG

The first time I scanned I think I used PNG, but the file sizes are enormous,
and it's not necessary to have such huge lossless files.

When scanning, I put a few sheets of printer paper inserted into the book
behind the page I'm scanning, to give it a white background.




PROCESSING PHOTOS: BOOK PORTRAITS AND MISC PORTRAITS
---–-------------–------------------–-------------–-

As of now, there are two "types" of portraits: ones in my sketchbooks, and
miscellaneous ones. The important difference is that sketchbook portraits
were all scanned at 800dpi on an EPSON photo scanner, while the miscellaneous
portraits are often crappy photos taken on a smart phone that need to be
seriously edited.

Book portraits are, once scanned, first manually rotated (can rotate using
e.g. Finder in MacOS even though it only changes the metadata to include a
rotation, because the script that comes next accounts for that), then the
script process_book_portraits.sh is run, which reduces resolution, filesize,
and color depth; and renames the file and saves a copy of it to the
books/ folder.

Miscellaneous portraits are, first dumped into the folder
misc_portraits_raw/0_photodump (there is a clone of this folder on Google
photos -- all Google Photos albums mentioned have the same name as the
corresponding folder on my computer, in this
case "misc_portraits_raw/0_photodump"). Then, because there are some
duplicates there, a selection of unique portraits is copied to the folder
misc_portraits_raw/1_selection. Next, I upload all the selected photos to
Google Photos. I edit the photos on my phone using SnapSeed, and then save
them to a new album called "misc_portraits_raw/2_edited". Then, I download
the edited photos onto my computer and put them into the
misc_portraits_raw/2_edited folder here. Finally, I use the script called
process_misc_portraits.sh to resize the images, make some edits, and copy
them to the folder misc/.



REDUCING IMAGE SIZE BY LOWERING BIT DEPTH
-----------------------------------------

Colorspaces include: HCL HCLp HSI HSB HSL

DON'T use HSL for testing average saturation on nearly-grayscale images.
It will give spurious results.

See: https://legacy.imagemagick.org/discourse-server/viewtopic.php?t=29781
     https://archive.is/XRNHt

Some test images and their mean saturations:

    convert "book1@800dpi/p 0.png" -resize '1600x1600>' -colors 255 +dither -auto-orient books/tests/testA.png
    convert "book1@800dpi/p 23.png" -resize '1600x1600>' -colors 255 +dither -auto-orient books/tests/testB.png
    convert "book1@800dpi/p 11.png" -resize '1600x1600>' -colors 255 +dither -auto-orient books/tests/testC.png
    convert "book2@800dpi/p 1.png" -resize '1600x1600>' -colors 255 +dither -auto-orient books/tests/testD.png
    convert "book1@800dpi/p 14.png" -resize '1600x1600>' -colors 255 +dither -auto-orient books/tests/testE.png

    convert "books/tests/testA.png" -colorspace HCL -channel g -separate +channel -format "%M: %[fx:mean]\n" info:
    convert "books/tests/testB.png" -colorspace HCL -channel g -separate +channel -format "%M: %[fx:mean]\n" info:
    convert "books/tests/testC.png" -colorspace HCL -channel g -separate +channel -format "%M: %[fx:mean]\n" info:
    convert "books/tests/testD.png" -colorspace HCL -channel g -separate +channel -format "%M: %[fx:mean]\n" info:
    convert "books/tests/testE.png" -colorspace HCL -channel g -separate +channel -format "%M: %[fx:mean]\n" info:

> books/testA.png: 0.0238151
> books/testB.png: 0.050264
> books/testC.png: 0.11977
> books/testD.png: 0.0184644
> books/testE.png: 0.223645

This prints the average saturation ("colorfulness") of each image. The two
more colorful images (testC.png and testE.png) give significantly higher
numbers than the more grayscale-like images. An interesting case is
testB.png, which is drawn in red colored pencil. The average saturation is an
in-between number. For the purposes of reducing image size by lowering bit
depth, it seems like putting a threshold at around 0.08 is appropriate.
(Meaning, I will reduce bit depth on images whose average saturation is less
than 0.08, but not on those whose average saturation is higher than 0.08.)

In the actual script that edits the images, combining the two commands above
into one doesn't seem to work, so I had to pipe them:

    convert "book1@800dpi/p 0.png" -alpha off -resize '20x20>' png:- | \
        convert - -colorspace HCL -channel g -separate +channel -format "%[fx:mean]\n" info:



SCRATCH NOTES OF OTHER COMMANDS I HAVE USED
-------------------------------------------

find . -maxdepth 1 -type f -name "*.png" -exec magick {} -quality 85 {}.jpeg \;
for f in *.png.jpeg; do mv "$f" "${f%.png.jpeg}.jpeg"; done

find . -maxdepth 1 -type f -name "*.jpeg" -exec magick {} -quality 85 {}.png \;
for f in *.jpeg.png; do mv "$f" "${f%.jpeg.png}.png"; done