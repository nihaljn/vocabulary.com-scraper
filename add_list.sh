while read line; do
    python3 add_word.py --word $line
done < $1