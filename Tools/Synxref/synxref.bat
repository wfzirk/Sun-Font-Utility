
set primary=pw7_8_EN.csv
set xrefin=synxref77.810.csv
set kmn="kmn7_8_EN.csv"
set outfile=synxref7_8.csv

pause besure %kmn% is sorted by unicode

cmd /c fontforge -quiet -script xref.py %xrefin%
::cmd /c fontforge -quiet -script verseref.py %kmn%

:syn
cmd /c fontforge -quiet -script synonyms.py %kmn%

cmd /c fontforge -script synxref.py %primary% xref.csv syn.csv  %outfile%
:end