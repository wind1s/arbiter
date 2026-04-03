#!/bin/bash

# Define the output file name
OUTPUT_FILE="combined_python.txt"

# Clear the output file if it exists
> "$OUTPUT_FILE"

# Use 'find' to locate all .py files recursively
# -type f: look for files only
# -name "*.py": look for python files
find . -type f -name "*.py" | while read -r file; do
    # Remove the './' prefix for a cleaner header
    clean_name="${file#./}"

    # Append the START header
    echo "START $clean_name:" >> "$OUTPUT_FILE"

    # Append the content of the file
    cat "$file" >> "$OUTPUT_FILE"

    # Append the END footer with spacing
    echo -e "\nEND $clean_name.\n" >> "$OUTPUT_FILE"
done

echo "Success! All files from this directory and subdirectories are in $OUTPUT_FILE"