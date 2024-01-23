#!/bin/bash

# Create the output folder if it doesn't exist
output_folder="books"
mkdir -p "$output_folder"

log_file="process_book_portraits.log"

# Function to get HCL mean value for an image
get_hcl_mean() {
    convert -quiet "$1" -alpha off -resize '20x20>' png:- | \
        convert - -colorspace HCL -channel g -separate +channel -format "%[fx:mean]\n" info:
}

# Function to print elapsed time
print_elapsed_time() {
    echo "(Elapsed time: $(date -u -r $((SECONDS)) +'%Hh%Mm%Ss'))"
}

# Start measuring execution time
SECONDS=0

# Redirect stdout and stderr to a log file
exec > >(tee -a "$log_file") 2>&1

echo "--- PROCESSING BOOK PORTRAITS ---"

# Loop through each book folder
for book_folder in book1@800dpi book2@800dpi book3@800dpi; do

    # Get the book number from the folder name (extract digits before @ symbol)
    book_number=$(echo "$book_folder" | grep -oE '[0-9]+' | head -n 1)

    # Loop through each image in the book folder
    image_number=0

    IFS=$'\n'
    for image_path in $(ls "$book_folder"/p*.png | sort -V); do

        # Define the output filename
        output_filename="${output_folder}/book${book_number}_${image_number}.png"

        # # Check if the output file already exists, and skip processing if it does
        # if [ -e "$output_filename" ]; then
        #     echo "${image_number}: ${image_path} -> ${output_filename} already exists. Skipping."
        #     continue
        # fi

        # Get the HCL mean value for the image
        hcl_mean=$(get_hcl_mean "$image_path")

        # Choose the appropriate convert command based on HCL mean value
        if [ "$(echo "$hcl_mean < 0.08" | bc -l)" -eq 1 ]; then
            convert -quiet "$image_path" -alpha off -resize '2000x2000>' -colors 64 -auto-orient "$output_filename"
            decision="using 64 colors"
        else
            convert -quiet "$image_path" -alpha off -resize '2000x2000>' -colors 256 -auto-orient "$output_filename"
            decision="using 256 colors"
        fi

        # Output information
        echo "${image_number}: "${image_path}" -> "${output_filename}" (hcl_mean: ${hcl_mean}, ${decision})"

        # Increment image number
        ((image_number++))

    done
done

echo "Generating thumbnails..."

# Create thumbnail images.
generate_misc_thumbnails="generate_thumbnails.sh"
bash "$generate_thumbnails" "$output_folder"

unset IFS
print_elapsed_time
