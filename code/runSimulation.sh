mkdir -p graphs
mkdir -p data
folder="graphs/"

python3 main.py

for file in data/*.dat
do
  formatted=$(echo $file| cut -d/ -f2)
  filename=$(echo $formatted| cut -d. -f1)
  echo "Generating graph $filename"
  outputPNG=$folder$filename".png"
  graph -T png $file > $outputPNG
done
