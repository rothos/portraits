#!/bin/bash

# Input folder containing images (default to "books")
input_folder=${1:-"books"}

# Flag to skip existing thumbnails
skip_existing=true

log_file="generate_thumbnails.log"

# Function to print elapsed time
print_elapsed_time() {
    echo "(Elapsed time: $(date -u -r $((SECONDS)) +'%Hh%Mm%Ss'))"
}

# Start measuring execution time
SECONDS=0

# Redirect stdout and stderr to a log file
exec > >(tee -a "$log_file") 2>&1

echo "--- GENERATING THUMBNAILS FOR $input_folder ---"

IFS=$'\n'

# Loop through each file in the input folder
for image_path in $(ls "$input_folder"/* | grep -v 't.png' | sort -V); do
    # Check if the file is a regular file
    if [ -f "$image_path" ]; then
        thumbnail_path="${image_path%.*}t.png"
        
        # Skip if thumbnail exists and skip_existing is true
        if [ "$skip_existing" = true ] && [ -f "$thumbnail_path" ]; then
            echo "Skipping existing thumbnail: $thumbnail_path"
            continue
        fi

        # Create a thumbnail with 300px height
        magick -quiet "$image_path" -resize x300 -sharpen 0x1 "$thumbnail_path"
        echo "Thumbnail created: $thumbnail_path"
    fi
done

unset IFS
print_elapsed_time
