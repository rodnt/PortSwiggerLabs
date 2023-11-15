#!/bin/bash

# Renaming files with spaces by replacing spaces with underscores
for file in *\ *; do
    new_name="${file// /_}"
    mv "$file" "$new_name"
done

# Renaming PNG files with '%20' by replacing '%20' with underscores
for file in *.png; do
    new_name=$(echo "$file" | sed 's/%20/_/g')
    mv "$file" "$new_name"
done