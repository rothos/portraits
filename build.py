"""
Build the static site which deploys to gar.lol/portraits via Github Pages.
"""

import os
from natsort import natsorted

# Total image count
total_images = 0

# List of filenames to ignore
ignore_list = ["book1_13.png", "book1_38.png"]

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
        
        gallery_html += f'    <a href="{image_path}">\n'
        gallery_html += f'        <img alt="{image_path}, a portrait drawing of me" src="{thumbnail_path}"/>\n'
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

    header = '<h1>Portraits</h1>\n'
    top_text = f"""<p>
        As an ongoing art project, I sometimes ask people to draw me. This
        project has undergone long periods of stagnation, but I haven't ever
        given up on it. Currently, I have a total of {total_images} portraits
        collected on this page.
        </p>
        <p>
        I welcome any portraits you want to send me, and I will almost
        definitely include them on this page. (I have omitted a total of two
        portraits from this page ({n_ignored}/{total_images+n_ignored}, or
        {"%1.1f" % (100*n_ignored/(total_images+n_ignored))}%), for different
        reasons. Only in very special cases do I not include a portrait.)
        </p>
        <p>
        For details about how I processed the images and created this gallery,
        see the very bottom of the page.
        </p>\n"""
    bottom_text = '<p>[details]</p>\n'

    html_content = header + top_text + books_gallery + misc_gallery + bottom_text
    return html_content

# Function to generate CSS styling
def generate_css():
    css_content = '/* Add your CSS styling here */\n'
    return css_content

# Main function to generate HTML, CSS, and write to files
def main():
    html_content = generate_html()
    css_content = generate_css()

    with open("index.html", "w") as html_file:
        html_file.write(html_content)

    with open("styles.css", "w") as css_file:
        css_file.write(css_content)

if __name__ == "__main__":
    main()
