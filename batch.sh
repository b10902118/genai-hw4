#!/bin/bash

for ((i=1; i<=10; i++))
do
    # Run the Python script
	echo $i
    python3 pressure.py

    # Create a new directory
    mkdir $i

    # Move the .pkl files and accuracy.txt to the new directory
    mv ./to_eval/*.pkl ./to_eval/accuracy.txt $i
	sleep 60
done