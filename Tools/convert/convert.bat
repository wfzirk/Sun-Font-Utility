:: https://stackoverflow.com/questions/30414346/batch-command-for-imagemagick-to-convert-all-files-in-a-directory-and-sub-direct
::D:\Documents\WA-SUN\Scripts\SFU_7_8\Svg
::D:\Documents\WA-SUN\Scripts\Tools\convert
set src=D:\Documents\WA-SUN\Scripts\SFU_7_8\Svg
set dst=D:\Documents\WA-SUN\Scripts\Tools\convert\jpg1
::FOR %%a in (%src%\*.svg) DO magick convert %%a -resize 620x620 "%dst%\%%a" 
FOR %%a in (%src%\*.svg) DO echo %%a 

FOR /R %%a IN (*.svg) DO convert "%%~a" "%%~dpna.jpg"