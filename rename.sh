for file in *\ *; do
    new_name="${file// /_}"
    mv "$file" "$new_name"
done

for file in *.png; do
    new_name=$(echo "$file" | sed 's/%20/_/g')
    mv "$file" "$new_name"
done
