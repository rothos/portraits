"""
Build the static site which deploys to gar.lol/portraits via Github Pages.
"""

import os
from bs4 import BeautifulSoup as bs         # for prettifying HTML
from bs4 import formatter as bs_formatter   # also for prettifying
from natsort import natsorted               # to sort filenames
from PIL import Image                       # to get image dimensions

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

        gallery_html += f'    <a href="{image_path}" data-pswp-width="{width}" data-pswp-height="{height}" target="_blank">\n'
        gallery_html += f'        <img alt="portrait #{total_images}, a portrait drawing of me" src="{thumbnail_path}"/>\n'
        gallery_html += '    </a>\n'

    gallery_html += '<span></span></div>\n'
    return gallery_html

# Function to generate the entire HTML content
def generate_html():
    global total_images
    global ignore_list
    n_ignored = len(ignore_list)

    books_gallery = generate_gallery("Sketchbook portraits", "books", "books_gallery")
    misc_gallery = generate_gallery("Miscellaneous portraits", "misc", "misc_gallery")

    head = """<!DOCTYPE html><html><head>
            <title>Portraits</title>
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width,initial-scale=1"/>
            <link rel="stylesheet" href="./css/photoswipe.css">
            <link rel="stylesheet" href="./css/styles.css">
            <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400&display=swap" rel="stylesheet">
            <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400&display=swap" rel="stylesheet">
            <script src="./js/smartquotes.min.js"></script>
        </head>\n"""
    bodyopen = "<body>\n"
    header = '<h1>Portraits</h1>\n'
    top_text = f"""<p>
    As an ongoing art project, I sometimes ask people if they'd like to to
    draw me. This project occasionally undergoes long periods of stagnation,
    but it's never dead, or complete. Currently, I have a total of
    {total_images} portraits collected on this page.
    </p>
    <p>
    The first portraits on this page were drawn in Spring of 2017. The years
    2017 and 2018 were very active; meanwhile, I collected only two portraits
    in 2020 and zero in 2021. The portraits are listed in roughly
    chronological order, except for a set of drawings at the end, which were
    not scanned from my portrait sketchbooks &emdash; they're a miscellaneous
    assortment of drawings that I got from friends and strangers, solicited or
    not, over the years.
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
    <p>
    For details about how I processed the images and created this gallery,
    see the very bottom of the page.
    </p>
    <p>
    Click on any portrait to see it in higher resolution.
    </p>\n"""
    gallerytag = '<div id="gallery">\n'
    galleryendtag = '</div>\n'
    bottom_text = '<h2>Notes on the making of this gallery</h2><p>[notes to be added]</p>\n'
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
    References:
        https://css-tricks.com/adaptive-photo-layout-with-flexbox/
    -->
</body></html>"""

    html_content = head + bodyopen + header + top_text \
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
}

p {
    margin-bottom: 15px;
}

#books_gallery, #misc_gallery {
    max-width: 1200px;
    display: flex;
    flex-wrap: wrap;
}

#books_gallery a, #misc_gallery a, #books_gallery span {
  margin: 10px;
}

@media only screen and (max-width: 600px) {
    body {
      padding: 18px;
    }
    #books_gallery a, #misc_gallery a, #books_gallery span {
      margin: 4px;
    }

    #books_gallery a img, #misc_gallery a img, #books_gallery span {
      height: 150px;
    }
}


/*
#books_gallery, #misc_gallery {
  display: flex;
  flex-wrap: wrap;
}

#books_gallery a, #misc_gallery a, #books_gallery span {
  height: 300px;
  flex-grow: 1;
  margin: 10px;
}

#books_gallery span:last-child, #misc_gallery span:last-child {
  flex-grow: 12;
}

#books_gallery a img, #misc_gallery a img {
  max-height: 100%;
  min-width: 100%;
  object-fit: cover;
  vertical-align: middle;
}
*/
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
