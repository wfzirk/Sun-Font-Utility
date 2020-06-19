rem must change system language locale to utf-8
rem https://www.bing.com/search?q=administrative+language+setting+win+10&form=WNSGPH&qs=AS&cvid=7b4667c3e2804c078bbfa20f11d7eb9f&pq=administrative+language+s&cc=US&setlang=en-US&nclid=5DAC70C3F9718B3FD01438C3459AFE25&ts=1581894742795&wsso=Moderate
:: requirements
:: english primary from sfd
:: backfont from primary
:: english dictionary from kmn
:: language backfont and dictionary from primary words
::  kmn from dictionary
:: all language primary merged from Language dictionary and english primary
:: languagedictionaries sorted by name or language name.
:: problems found:
::  	duplicate words in language dictionaries different unicodes
::			Use first word in list
::		unicodes with o instead of 0
::			manually fixed
::		unicode miscompares with down level dictionaries
::			use unicodes from english primary list
::		words with spaces
:: 			replace with '_' (underscore)
:::SETLOCAL
Setlocal EnableDelayedExpansion
:: get running environment
:: cmd /c fontforge -script doall.py
call doEnv.bat
goto doit
::set sfd="SUN7_6.sfd"
::set kmn="SUN7_6.kmn"
::set ver=76
::set ttffont=times.ttf
::set alias=EN
::goto doit

::set langIn="Translators Dictionary_Portuguese.ods"
::set ver=76
::set ttffont=times.ttf
::set alias=PT
::set langOut=SUNBF%ver%_%alias%.csv

:doit
:: sets up config file
:: cmd /c fontforge -quiet -script bfConfig.py %alias% %langIn% %ver% %ttffont% %langOut% 

::if %1.==. (goto dolang)
if %1.== all (goto dolang)

set docmd=%1
echo docmd set
goto %docmd%


:dolang

if %docmd% == all (goto backfont) else (goto %docmd%)
echo "shouldn't be here"
goto end
:all
:backfont
rem sequence of commands to build backfont file

:sfd2csv
if %alias% == EN (
	cmd /c fontforge -quiet -script sfd2csv.py %sfd% dist/pw%ver%_%alias%.csv
	if ERRORLEVEL 1 (goto errorexit)
)
:langpri
if NOT %alias% == EN (
	cmd /c fontforge -quiet -script langpri.py dist/pw%ver%_EN.csv %langIn% dist/pw%ver%_%alias%.csv 
	if ERRORLEVEL 1 (goto errorexit)
)
if %docmd%  NEQ all (goto end)

:kmn2csv
if %alias% == EN (
	cmd /c fontforge -quiet -script kmn2csv.py %kmn% dist/kmn%ver%_%alias%.csv
	if ERRORLEVEL 1 (goto errorexit)
)
if %docmd%  NEQ all (goto end)

:csv2kmn
if NOT %alias% == EN (
	cmd /c fontforge -quiet -script csv2kmn.py dist/pw%ver%_%alias%.csv %ver% %alias%  dist\sun%ver%_%alias%.kmn
	if ERRORLEVEL 1 (goto errorexit)
)
if %docmd%  NEQ all (goto end)

:csv2svg
cmd /c fontforge -quiet -script csv2svg.py dist/pw%ver%_%alias%.csv %ttffont%
if ERRORLEVEL 1 (goto errorexit)
if %docmd%  NEQ all (goto end)

:svg2font
cmd /c fontforge -quiet -script svg2Font.py dist/pw%ver%_%alias%.csv %ttffont% %alias% dist/SUNBF%ver%_%alias%
if ERRORLEVEL 1 (goto errorexit)
if %docmd%  NEQ all (goto end)

rem following are for documentation and verification
:back2doc
cmd /c fontforge -quiet -script back2doc.py dist/pw%ver%_%alias%.csv dist/back%ver%_%alias%.txt 
if ERRORLEVEL 1 (goto errorexit)
if %docmd%  NEQ all (goto end)

:compact
cmd /c fontforge -quiet -script compact4x16.py dist/pw%ver%_%alias%.csv dist/compact%ver%_%alias%.pdf
if ERRORLEVEL 1 (goto errorexit)
if %docmd%  NEQ all (goto end)

:bfzip
cmd /c fontforge -quiet -script bfZip.py
if ERRORLEVEL 1 (goto errorexit)
if %docmd%  NEQ all (goto end)

goto end

:errorexit
echo quit because of errors
echo quit with error = %errorlevel%
goto end

rem zipit.bat
rem start /i /b /wait python -c "import util; util.printhi('someInput')"
rem cmd /c python -c "import util; util.zipdir("", %ver%)
:end
echo Done


