#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "RENDERING 25-MINUTE MASTERCLASS: THE MODULAR EMERGENCE PARADOX"
echo "=========================================================="

cd /Users/samreedhbhuyan/Desktop/Win_C/youtube_videos/self_adapting_ai/remotion_studio

echo "Bundling latest code to build/..."
npx remotion bundle src/index.ts build

# Clean any existing intermediate chapter files
rm -f ../output/chap*.mp4
rm -f ../output/master_concat_list.txt

CHAPTERS=(
  "Chapter01-TheMonolith:chap01.mp4"
  "Chapter02-TheBiologicalDream:chap02.mp4"
  "Chapter03-SelfOrganizingHypothesis:chap03.mp4"
  "Chapter04-TheParadox:chap04.mp4"
  "Chapter05-Theorem1-RankCollapse:chap05.mp4"
  "Chapter06-Theorem2-RoutingBounds:chap06.mp4"
  "Chapter07-Theorem3-HardwareBarrier:chap07.mp4"
  "Chapter08-EmpiricalBenchmarks:chap08.mp4"
  "Chapter09-FrontierLabs:chap09.mp4"
  "Chapter10-The10YearFrontier:chap10.mp4"
)

CONCAT_FILE="../output/master_concat_list.txt"
> "$CONCAT_FILE"

for item in "${CHAPTERS[@]}"; do
  comp_id="${item%%:*}"
  filename="${item##*:}"
  out_path="../output/$filename"
  
  echo ""
  echo ">>> Rendering [$comp_id] -> $out_path ..."
  npx remotion render build "$comp_id" "$out_path" --concurrency=8 --gl=angle
  
  echo "file '$filename'" >> "$CONCAT_FILE"
done

echo ""
echo "=========================================================="
echo "STITCHING COMPLETE MASTERCLASS VIDEO VIA FFMPEG"
echo "=========================================================="
cd ../output

ffmpeg -y -f concat -safe 0 -i master_concat_list.txt -c copy masterclass_25min_complete.mp4

echo "Cleaning intermediate chapter files to maintain single-file output constraint..."
rm -f chap*.mp4
rm -f Chapter01_TheMonolith_remotion.mp4
rm -f master_concat_list.txt
rm -f concat_list*.txt
rm -f *.png
rm -f test_*.mp4

echo ""
echo "=========================================================="
echo "VERIFYING FINAL MASTER VIDEO METADATA"
echo "=========================================================="
ffprobe -v error -show_entries format=duration,size,bit_rate -show_entries stream=codec_name,width,height,r_frame_rate -of json masterclass_25min_complete.mp4

echo ""
echo ">>> MASTERCLASS RENDER SUCCESS: output/masterclass_25min_complete.mp4"
