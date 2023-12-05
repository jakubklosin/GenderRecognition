#!/bin/bash

# Inicjalizacja liczników
good=0
bad=0

# Iterating through all files in train folder
for file in train/*.wav; do
  # Uruchom skrypt Python i przechwyć jego wyjście
  output=$(python3 main.py "$file")

  # Get letter M/K from file name
  filename=$(basename "$file")
  label=${filename: -5:1}

  # Compare taken letter with programme output and increase counter
  if [ "$output" = "$label" ]; then
    ((good++))
  else
    ((bad++))
  fi
done

# total number of files
total=$((good + bad))

# Counting accuracy
if [ $total -gt 0 ]; then
  accuracy=$(echo "scale=2; $good / $total * 100" | bc)
else
  accuracy=0
fi

# Printing results
echo "Poprawne rozpoznania: $good"
echo "Niepoprawne rozpoznania: $bad"
echo "Skuteczność programu: $accuracy%"
