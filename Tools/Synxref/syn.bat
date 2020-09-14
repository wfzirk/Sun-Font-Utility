
set kmn="kmnSUN7_6.csv"

rem print("\nsyntax: fontforge -script synonyms.py ")
rem print("   creates "syn.csv" - list of synonyms in the kmn file")

fontforge -quiet -script synonyms.py %kmn%