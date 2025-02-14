"""
Build the static site which deploys to gar.lol/portraits via Github Pages.
"""

import os
# import minify_html
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

# Total image count for each gallery
book_count = 0
misc_count = 0
total_images = 0

# List of filenames to ignore
ignore_list = ["book1_13.png", "book1_38.png"]

# Function to get image dimensions
def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        return img.size

# Function to generate image gallery HTML code
def generate_gallery(header, folder_name, gallery_id, name_prefix):
    global ignore_list
    global total_images
    global book_count
    global misc_count

    gallery_html = f'<h2 id="{folder_name}">{header}</h2><div id="{gallery_id}">\n'
    
    # Get a sorted list of files
    files = natsorted([filename for filename in os.listdir(folder_name) \
            if filename.endswith(".png") \
                and filename not in ignore_list \
                and not filename.endswith("t.png") ])

    for filename in files:
        total_images += 1  # Increment the total_images count
        
        # Increment the appropriate counter based on prefix
        if name_prefix == "p":
            book_count += 1
            count = book_count
        else:
            misc_count += 1
            count = misc_count

        image_path = os.path.join(folder_name, filename)
        thumbnail_path = os.path.join(folder_name, filename[:-4] + "t.png")
        
        # Get image dimensions
        width, height = get_image_dimensions(image_path)
        twidth, theight = get_image_dimensions(thumbnail_path)

        next_image = f'    <a href="{image_path}" \
                                        name="{name_prefix}{count}" \
                                        data-pswp-width="{width}" \
                                        data-pswp-height="{height}" \
                                        target="_blank">\n'
        next_image += f'        <img alt="portrait #{total_images}, a portrait drawing of me" \
                                        src="{thumbnail_path}" \
                                        width="{twidth}" \
                                        height="{theight}" \
                                        />\n'
        next_image += '    </a>\n'

        # Remove excess whitespace while maintaining newlines
        next_image = '\n'.join([' '.join(line.split()) for line in next_image.split('\n')])

        gallery_html += next_image

    gallery_html += '</div>\n'
    return gallery_html

# Function to generate the entire HTML content
def generate_html():
    global total_images
    global ignore_list
    n_ignored = len(ignore_list)

    books_gallery = generate_gallery("Sketchbook portraits", "books", "books_gallery", "p")
    misc_gallery = generate_gallery("Miscellaneous portraits", "misc", "misc_gallery", "m")

    head = f"""<!DOCTYPE html><html><head>
            <!-- Google tag (gtag.js) -->
            <script async src="https://www.googletagmanager.com/gtag/js?id=G-VSL74PME4G"></script>
            <script>
              window.dataLayer = window.dataLayer || [];
              function gtag(){{dataLayer.push(arguments);}}
              gtag('js', new Date());

              gtag('config', 'G-VSL74PME4G');
            </script>
            <title>Portraits</title>
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width,initial-scale=1"/>
            <link rel="stylesheet" href="./css/photoswipe.css">
            <link rel="stylesheet" href="./css/styles.css?{epoch}">
            <link href='http://fonts.googleapis.com/css?family=Droid+Sans' rel='stylesheet'>
            <link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400&display=swap" \
                rel="stylesheet">
            <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400&display=swap" \
                rel="stylesheet">
            <script src="./js/smartquotes.min.js"></script>
            <script>
                // Theme handling
                function getThemePreference() {{
                    return localStorage.getItem('theme') || 'auto';
                }}

                function setTheme(theme) {{
                    localStorage.setItem('theme', theme);
                    applyTheme(theme);
                }}

                function applyTheme(theme) {{
                    const isDark = theme === 'dark' || 
                        (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches);
                    document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
                    updateThemeToggle(theme);
                }}

                function updateThemeToggle(theme) {{
                    const toggle = document.getElementById('theme-toggle');
                    if (toggle) {{
                        toggle.innerHTML = theme === 'dark' ? '☀️' : '🌙';
                        toggle.setAttribute('title', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
                    }}
                }}

                // Initialize theme
                document.addEventListener('DOMContentLoaded', () => {{
                    const theme = getThemePreference();
                    applyTheme(theme);
                    
                    // Listen for system theme changes
                    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {{
                        if (getThemePreference() === 'auto') {{
                            applyTheme('auto');
                        }}
                    }});
                }});
            </script>
        </head>\n"""
    bodyopen = "<body>\n"
    menu = """<div id='menu'>
        <a id='garlol' href='/'>// gar.lol</a>
        <button id="theme-toggle" onclick="setTheme(getThemePreference() === 'dark' ? 'light' : 'dark')" 
            aria-label="Toggle dark mode">🌙</button>
    </div>\n"""
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
    The <a href="javascript:void(0)" data-pswp-open="144">earliest
    portrait</a> on this page dates to 2015. I didn't <a
    href="https://a.co/d/inhjv9j" target="_blank">get sketchbooks</a> and make
    it a project until Spring of 2017. The years 2017 and 2018 were very
    active; meanwhile, I collected only two portraits in 2020 and zero in
    2021. The portraits are listed in roughly chronological order, except for
    a set of drawings at the end, which were not scanned from my portrait
    sketchbooks — they're a <a href="#misc">miscellaneous collection</a> of
    drawings that I received from friends and strangers over the years (all
    unsolicited, iirc).
    </p>
    <!--
    <p>
    I include almost all portraits on this page. I have omitted only two
    portraits ({n_ignored}/{total_images+n_ignored}, or
    {"%1.1f" % (100*n_ignored/(total_images+n_ignored))}%), each for different
    reasons. Only in very special cases do I not include a portrait here.
    </p>
    -->
    <p>
    Some people have drawn multiple portraits. For example, the very first two
    portraits in this gallery were drawn by the same person.
    </p>
    <p>
    I always welcome new portraits. If you want to draw me, please find me
    in person and draw in my portrait book!
    </p>
    <!--
    <p>
    For details about how I processed the images and created this gallery,
    see the very bottom of the page.
    </p>
    -->
    <p>
    Click on any image to see it in higher resolution. You can link to
    any specific portrait by copying the URL after clicking on the image.
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

        if(window.location.hash) {
            // Fragment exists
            var hash = window.location.hash.slice(1);
            var pattern = /^([pm])(\\d+)$/;  // Match either p123 or m123
            var match = hash.match(pattern);
            if (match) {
                var prefix = match[1];
                var num = parseInt(match[2], 10);
                
                // Find the index in the combined gallery
                var allLinks = document.querySelectorAll('#gallery a');
                var targetIndex = Array.from(allLinks).findIndex(
                    link => link.getAttribute('name') === `${prefix}${num}`
                );
                if (targetIndex !== -1) {
                    lightbox.loadAndOpen(targetIndex, {
                        gallery: document.querySelector('#gallery')
                    });
                }
            }
        }

        // Code taken from here: https://stackoverflow.com/a/5298684
        function removeHash () { 
            var scrollV, scrollH, loc = window.location;
            if ("replaceState" in history)
                history.replaceState("", document.title, loc.pathname + loc.search);
            else {
                // Prevent scrolling by storing the page's current scroll offset
                scrollV = document.body.scrollTop;
                scrollH = document.body.scrollLeft;

                loc.hash = "";

                // Restore the scroll offset, should be flicker free
                document.body.scrollTop = scrollV;
                document.body.scrollLeft = scrollH;
            }
        }

        var elementsWithAttribute = document.querySelectorAll('[data-pswp-open]');
        elementsWithAttribute.forEach(function(element) {
            element.addEventListener('click', function() {
                var id = element.getAttribute('data-pswp-open');
                lightbox.loadAndOpen(id-1, {
                    gallery: document.querySelector('#gallery')
                });
            });
        });

        lightbox.on('change', (e) => {
            // Get the current slide's link element
            var currentSlide = lightbox.pswp.currSlide;
            if (!currentSlide) return;
            
            var currentElement = currentSlide.data.element;
            var name = currentElement.getAttribute('name');
            
            // Update URL with the current image's name (which includes the prefix)
            var curUrlNoHash = window.location.toString().split('#')[0];
            history.replaceState({}, '', curUrlNoHash + '#' + name);
        });

        lightbox.on('close', () => {
            // PhotoSwipe starts to close, unbind most events here
            removeHash();
        });
    </script>
    <script type="module">
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

:root {
    /* Light theme colors */
    --bg-color: #fff;
    --text-color: #222;
    --link-bg: #edf6fb;
    --link-color: #259;
    --menu-color: #369;
    --menu-shadow: #ccc;
    --img-bg: #ddd;
    
    /* Theme transition */
    transition: background-color 0.3s ease, color 0.3s ease;
}

/* Dark theme colors */
[data-theme="dark"] {
    --bg-color: #1a1a1a;
    --text-color: #e0e0e0;
    --link-bg: #2a3f4a;
    --link-color: #7cb4d9;
    --menu-color: #7cb4d9;
    --menu-shadow: #000;
    --img-bg: #333;
}

body {
    font-family: 'Assistant', sans-serif;
    padding: 40px;
    margin: 0;
    color: var(--text-color);
    background-color: var(--bg-color);
}

p {
    max-width: 600px;
}

p a {
    color: var(--link-color);
    text-decoration: none;
    background-color: var(--link-bg);
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

#menu {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

#theme-toggle {
    background: none;
    border: none;
    font-size: 1.5em;
    cursor: pointer;
    padding: 8px;
    border-radius: 50%;
    transition: background-color 0.3s;
}

#theme-toggle:hover {
    background-color: var(--link-bg);
}

#garlol {
    background-color: unset;
    text-decoration: none;
    color: var(--menu-color);
    text-shadow: var(--menu-shadow) 1px 0 3px;
    font-family: 'Libre Baskerville', serif;
    font-size: 1.6em;
}

#garlol span {
    font-family: "Droid Sans", sans-serif;
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
  background-color: var(--img-bg);
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

    # minified = minify_html.minify(html_content, minify_js=True)

    with open("index.html", "w") as html_file:
        html_file.write(html_content)

    with open("css/styles.css", "w") as css_file:
        css_file.write(css_content)

if __name__ == "__main__":
    main()
