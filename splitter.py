import os
import sys
import tempfile

tempfile.mkdtemp

chapter = sys.argv[1].split(".")[0]
print("splitting:")
print(chapter)

tick = 0
contents_i = []
with open(chapter + ".md", encoding='utf-8') as file:
    for line in file:
        if line == "---\n":
            tick += 1
            continue
        if line == "# References\n":
        	break
        if tick == 2:
            contents_i.append(line)
chapter_short = chapter + "_short.md"
if not os.path.exists(chapter_short):
    with open(chapter_short, "w+", encoding="utf-8") as file:
        for line in contents_i:
            file.write(line)
