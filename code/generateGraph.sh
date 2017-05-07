mkdir -p graphs
folder="graphs/"

for file in data/*.dat
do
  formatted=$(echo $file| cut -d/ -f2)
  filename=$(echo $formatted| cut -d. -f1)
  echo $filename
  outputPNG=$folder$filename".png"
  graph -T png $file > $outputPNG
done
