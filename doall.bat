rem must change system language locale to utf-8
rem https://www.bing.com/search?q=administrative+language+setting+win+10&form=WNSGPH&qs=AS&cvid=7b4667c3e2804c078bbfa20f11d7eb9f&pq=administrative+language+s&cc=US&setlang=en-US&nclid=5DAC70C3F9718B3FD01438C3459AFE25&ts=1581894742795&wsso=Moderate

Setlocal EnableDelayedExpansion

call doEnv.bat

if %alias% == EN set engalias=EN
if %alias% == eng set engalias=EN

:doit

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
@echo off
:kmn2csv
if %engalias% == EN (
	@echo on
	cmd /c fontforge -quiet -script kmn2csv.py "%kmn%" dist/kmn%ver%_%alias%.csv
	@echo off
	if ERRORLEVEL 1 (goto errorexit)
)
if %docmd%  NEQ all (goto end)

:sfd2csv
if %engalias% == EN (
	@echo on
	cmd /c fontforge -quiet -script sfd2csv.py "%sfd%" dist/kmn%ver%_%alias%.csv dist/pw%ver%_%alias%.csv
	@echo off
	if ERRORLEVEL 1 (goto errorexit)
)
:langpri
if NOT %engalias% == EN (
	@echo on
	cmd /c fontforge -quiet -script langpri.py dist/pw%ver%_%alias%.csv %langIn% dist/pw%ver%_%alias%.csv 
	@echo off
	if ERRORLEVEL 1 (goto errorexit)
)
if %docmd%  NEQ all (goto end)

:csv2kmn
if NOT %engalias% == EN (
	@echo on
	cmd /c fontforge -quiet -script csv2kmn.py dist/pw%ver%_%alias%.csv %ver% %alias%  dist\sun%ver%_%alias%.kmn
	@echo off
	if ERRORLEVEL 1 (goto errorexit)
)
if %docmd%  NEQ all (goto end)

:csv2svg
	@echo on
	cmd /c fontforge -quiet -script csv2svg.py dist/pw%ver%_%alias%.csv %ttffont%
	@echo off
	if ERRORLEVEL 1 (goto errorexit)
	
if %docmd%  NEQ all (goto end)

:svg2font
	@echo on
	cmd /c fontforge -quiet -script svg2Font.py dist/pw%ver%_%alias%.csv %ttffont% %alias% dist/SUNBF%ver%_%alias%
	@echo off
	if ERRORLEVEL 1 (goto errorexit)
if %docmd%  NEQ all (goto end)

rem following are for documentation and verification
:back2doc
	@echo on
	cmd /c fontforge -quiet -script back2doc.py dist/pw%ver%_%alias%.csv dist/back%ver%_%alias%.txt 
	@echo off
	if ERRORLEVEL 1 (goto errorexit)
if %docmd%  NEQ all (goto end)

:compact
	@echo on
	cmd /c fontforge -quiet -script compact4x16.py dist/pw%ver%_%alias%.csv dist/compact%ver%_%alias%.pdf
	if ERRORLEVEL 1 (goto errorexit)	
	@echo off
if %docmd%  NEQ all (goto end)

:bfzip
	@echo on
	cmd /c fontforge -quiet -script bfZip.py
	@echo off
	if ERRORLEVEL 1 (goto errorexit)
if %docmd%  NEQ all (goto end)

goto end

:errorexit
@echo on
echo quit because of errors
echo quit with error = %errorlevel%
goto end

rem zipit.bat
rem start /i /b /wait python -c "import util; util.printhi('someInput')"
rem cmd /c python -c "import util; util.zipdir("", %ver%)
:end

echo Done


