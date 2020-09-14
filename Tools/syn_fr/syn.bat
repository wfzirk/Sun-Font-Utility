
set kmn="fr_614.csv"

rem print("\nsyntax: fontforge -script syn_fr.py ")
rem print("   creates "syn.csv" - list of synonyms from french dictionary")

fontforge -quiet -script syn_fr.py %kmn%