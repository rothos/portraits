"""
Build the static site which deploys to gar.lol/portraits via Github Pages.
"""

import os
from bs4 import BeautifulSoup as bs         # for prettifying HTML
from bs4 import formatter as bs_formatter   # also for prettifying
from natsort import natsorted               # to sort filenames
from PIL import Image                       # to get image dimensions
from datetime import datetime               # to print the date in human-readable format
import time                                 # to get epoch time

# Get current date and time info (printed in a comment at the end of the page)
current_local_time = datetime.now()
local_timezone_name = current_local_time.astimezone().tzname()
formatted_time = current_local_time.strftime("%Y-%m-%d %H:%M:%S %Z") \
               + f"({local_timezone_name})"

# For ensuring files aren't cached.
epoch = int(time.time())

# Total image count
total_images = 0

# List of filenames to ignore
ignore_list = ["book1_13.png", "book1_38.png"]

# Function to get image dimensions
def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        return img.size

# Function to generate image gallery HTML code
def generate_gallery(header, folder_name, gallery_id):
    global ignore_list
    global total_images

    gallery_html = f'<h2>{header}</h2><div id="{gallery_id}">\n'
    
    # Get a sorted list of files
    files = natsorted([filename for filename in os.listdir(folder_name) \
            if filename.endswith(".png") \
                and filename not in ignore_list \
                and not filename.endswith("t.png") ])

    for filename in files:
        total_images += 1  # Increment the total_images count

        image_path = os.path.join(folder_name, filename)
        thumbnail_path = os.path.join(folder_name, filename[:-4] + "t.png")
        
        # Get image dimensions
        width, height = get_image_dimensions(image_path)
        twidth, theight = get_image_dimensions(thumbnail_path)

        gallery_html += f'    <a href="{image_path}" \
                                        data-pswp-width="{width}" \
                                        data-pswp-height="{height}" \
                                        target="_blank">\n'
        gallery_html += f'        <img alt="portrait #{total_images}, a portrait drawing of me" \
                                        src="{thumbnail_path}" \
                                        width="{twidth}" \
                                        height="{theight}" \
                                        />\n'
        gallery_html += '    </a>\n'

    gallery_html += '</div>\n'
    return gallery_html

# Function to generate the entire HTML content
def generate_html():
    global total_images
    global ignore_list
    n_ignored = len(ignore_list)

    books_gallery = generate_gallery("Sketchbook portraits", "books", "books_gallery")
    misc_gallery = generate_gallery("Miscellaneous portraits", "misc", "misc_gallery")

    head = f"""<!DOCTYPE html><html><head>
            <title>Portraits</title>
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width,initial-scale=1"/>
            <link rel="stylesheet" href="./css/photoswipe.css">
            <link rel="stylesheet" href="./css/styles.css?{epoch}">
            <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400&display=swap" \
                rel="stylesheet">
            <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400&display=swap" \
                rel="stylesheet">
            <script src="./js/smartquotes.min.js"></script>
        </head>\n"""
    bodyopen = "<body>\n"
    menu = "<div id='menu'><a id='garlol' href='/'>Ꙩ gar.lol</a></div>\n"
    header = '<h1>Portraits</h1>\n'
    top_text = f"""<p>
    As an ongoing art project, I sometimes ask people if they'd like to to
    draw me. I like to know how people perceive me, and how they express that
    perception. I see a lot of myself, and a lot of the artists, in the
    drawings below. It's not always clear which is which.
    </p>
    <p>
    This project occasionally undergoes long periods of stagnation,
    but it's never dead, or complete. Currently, I have a total of
    {total_images} portraits collected on this page.
    </p>
    <p>
    The earliest portrait on this page dates to 2015. I didn't get sketchbooks
    and make it a project until Spring of 2017. The years 2017 and 2018 were
    very active; meanwhile, I collected only two portraits in 2020 and zero in
    2021. The portraits are listed in roughly chronological order, except for
    a set of drawings at the end, which were not scanned from my portrait
    sketchbooks — they're a miscellaneous collection of drawings that I
    received from friends and strangers, solicited or not, over the years.
    </p>
    <p>
    I welcome any portraits you want to send me, and I will almost
    definitely include them on this page. (I have omitted a total of two
    portraits from this page ({n_ignored}/{total_images+n_ignored}, or
    {"%1.1f" % (100*n_ignored/(total_images+n_ignored))}%), for different
    reasons. Only in very special cases do I not include a portrait.) Some
    people have drawn multiple portraits (for example, the very first two
    portraits in this gallery were drawn by the same person).
    </p>
    <!--
    <p>
    For details about how I processed the images and created this gallery,
    see the very bottom of the page.
    </p>
    -->
    <p>
    Click on any portrait to see it in higher resolution.
    </p>\n"""
    gallerytag = '<div id="gallery">\n'
    galleryendtag = '</div>\n'
    bottom_text = """\
    <!--
    <h2>Notes on the making of this gallery</h2>\
    <p>[notes to be added]</p>\
    -->\
    """
    bodyclose = """
    <script type="module">
        import PhotoSwipeLightbox from './js/photoswipe-lightbox.esm.min.js';
        const lightbox = new PhotoSwipeLightbox({
            gallery: '#gallery',
            children: 'a',
            pswpModule: () => import('./js/photoswipe.esm.min.js')
        });
        lightbox.init();
    </script>
    <script>
        // Enable smart quotes
        document.addEventListener('DOMContentLoaded', function() {
            smartquotes();
        });
    </script>
    <!--
    Last updated: %s
    -->
</body></html>""" % formatted_time

    html_content = head + bodyopen + menu + header + top_text \
                 + gallerytag \
                 + books_gallery + misc_gallery \
                 + galleryendtag \
                 + bottom_text + bodyclose
    return html_content

# Function to generate CSS styling
def generate_css():
    css_content = """/*
styles.css
*/

body {
    font-family: 'Assistant', sans-serif;
    padding: 40px;
    margin: 0;
    color: #222;
}

p {
    max-width: 800px;
}

h1, h2 {
    font-family: 'Libre Baskerville', serif;
    margin-bottom: 10px;
    font-weight: normal;
}

h2 {
    margin-top: 28px;
}

p {
    margin-bottom: 15px;
}

#menu {}

#garlol {
    text-decoration: none;
    color: #369;
    text-shadow: #ccc 1px 0 3px;
    font-family: 'Libre Baskerville', serif;
    font-size: 1.6em;
}

#gallery {
    margin-bottom: 3em;
}

#books_gallery, #misc_gallery {
    max-width: 1200px;
    display: flex;
    flex-wrap: wrap;
    margin: 0 -10px;
}

#books_gallery a, #misc_gallery a {
  margin: 10px;
}

#books_gallery a img, #misc_gallery a img {
  background-color: #ddd;
}

@media only screen and (max-width: 800px) {
    body {
      padding: 24px;
    }
    #books_gallery a, #misc_gallery a {
      margin: 6px;
    }

    #books_gallery a img, #misc_gallery a img {
      height: 190px;
      width: auto;
    }
}

@media only screen and (max-width: 600px) {
    body {
      padding: 18px;
    }
    #books_gallery a, #misc_gallery a {
      margin: 4px;
    }

    #books_gallery a img, #misc_gallery a img {
      height: 150px;
      width: auto;
    }
}
"""
    return css_content

# Main function to generate HTML, CSS, and write to files
def main():
    html_content = generate_html()
    css_content = generate_css()

    soup = bs(html_content, features="html.parser")
    formatter = bs_formatter.HTMLFormatter(indent=2)
    prettyHTML = soup.prettify(formatter=formatter)

    with open("index.html", "w") as html_file:
        html_file.write(prettyHTML)

    with open("css/styles.css", "w") as css_file:
        css_file.write(css_content)

if __name__ == "__main__":
    main()
