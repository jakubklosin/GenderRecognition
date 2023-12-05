#!/bin/bash

# Inicjalizacja liczników
good=0
bad=0

# Pętla przez każdy plik .wav w katalogu 'train'
for file in train/*.wav; do
  # Uruchom skrypt Python i przechwyć jego wyjście
  output=$(python3 main.py "$file")

  # Pobierz literę (M/K) z nazwy pliku
  filename=$(basename "$file")
  label=${filename: -5:1}

  # Porównaj wynik skryptu z literą w nazwie pliku i zaktualizuj liczniki
  if [ "$output" = "$label" ]; then
    ((good++))
  else
    ((bad++))
  fi
done

# Obliczanie całkowitej liczby plików
total=$((good + bad))

# Obliczanie skuteczności w procentach
if [ $total -gt 0 ]; then
  accuracy=$(echo "scale=2; $good / $total * 100" | bc)
else
  accuracy=0
fi

# Wyświetl wyniki
echo "Poprawne rozpoznania: $good"
echo "Niepoprawne rozpoznania: $bad"
echo "Skuteczność programu: $accuracy%"
