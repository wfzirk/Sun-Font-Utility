set version=7_8
set primary=pw7_8_EN.csv
set kmn=kmn7_8_EN.csv
set out=compare%version%.txt
fontforge -script compare.py %primary% %kmn% %out% 