#!/bin/bash

# Input folder containing raw images
input_folder="misc_portraits_raw/2_edited"

# Create the output folder if it doesn't exist
output_folder="misc"
mkdir -p "$output_folder"

log_file="process_misc_portraits.log"

# Function to get HCL mean value for an image
get_hcl_mean() {
    convert -quiet "$1" -resize '20x20>' -format png png:- | \
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

echo "--- PROCESSING MISC PORTRAITS ---"

# OVERRIDES: Array of filenames to always use 64 colors
f64=("misc_3.jpeg")

# OVERRIDES: Array of filenames to always use 256 colors
f256=("misc_7.jpeg")

IFS=$'\n'

# Loop through each file in the input folder
for image_path in $(ls "$input_folder"/* | sort -V); do
    # Check if the file is a regular file
    if [ -f "$image_path" ]; then

        # Get the HCL mean value for the image
        hcl_mean=$(get_hcl_mean "$image_path")

        # Process and save the image
        output_filename="$output_folder/$(basename "${image_path%.*}").png"

        # Check if the filename is in the f64 array
        if [[ " ${f64[@]} " =~ " $(basename "$image_path") " ]]; then
            convert -quiet "$image_path" -resize '2000x2000>' -colors 64 \
                -auto-orient -format png -alpha off "$output_filename"
            decision="using 64 colors (overridden)"
        # Check if the filename is in the f256 array
        elif [[ " ${f256[@]} " =~ " $(basename "$image_path") " ]]; then
            convert -quiet "$image_path" -resize '2000x2000>' -colors 256 \
                -auto-orient -format png -alpha off "$output_filename"
            decision="using 256 colors (overridden)"
        else
            # Choose the appropriate convert command based on HCL mean value
            if [ "$(echo "$hcl_mean < 0.08" | bc -l)" -eq 1 ]; then
                convert -quiet "$image_path" -resize '2000x2000>' -colors 64 \
                    -auto-orient -format png -alpha off "$output_filename"
                decision="using 64 colors"
            else
                convert -quiet "$image_path" -resize '2000x2000>' -colors 256 \
                    -auto-orient -format png -alpha off "$output_filename"
                decision="using 256 colors"
            fi
        fi

        echo "Processed: $image_path -> $output_filename (hcl_mean: ${hcl_mean}, ${decision})"
    fi
done

unset IFS
print_elapsed_time
