#!/bin/bash
for file in house_query/*.sh;
do
	sed -i 's/\r//' "$file";
	sbatch "$file"
done;