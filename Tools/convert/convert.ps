#
#
#ImageMagick Recursive Powershell Script with Progress display
#This script will execute a command recursively on all folders and 
subfolders
#This script will display the filename of every file processed
#set the source folder for the images
$srcfolder = "C:\temp"
#set the destination folder for the images
$destfolder = "C:\temp"
#set the ImageMagick command
$im_convert_exe = "magick"
#set the source image format (wildcard must be specified)
$src_filter = "*.png"
#set the destination (output) image format
$dest_ext = "bmp"
#set the ImageMagick command options
$options = "-colorspace rgb -density 300 -depth 8 -alpha off"
#set the log file path and name
$logfile = "C:\temp\convert.log"
$fp = New-Item -ItemType file $logfile -force
#The following lines allow the display of all files that are being 
processed
$count=0
foreach ($srcitem in $(Get-ChildItem $srcfolder -include $src_filter - 
recurse))
{
$srcname = $srcitem.fullname
$partial = $srcitem.FullName.Substring( $srcfolder.Length )
$destname = $destfolder + $partial
$destname= [System.IO.Path]::ChangeExtension( $destname , $dest_ext )
$destpath = [System.IO.Path]::GetDirectoryName( $destname )

if (-not (test-path $destpath))
{
    New-Item $destpath -type directory | Out-Null
}
#the following line defines the contents of the convert command line
$cmdline =  $im_convert_exe + " `"" + $srcname  + "`"" + $options + " `"" 
+ $destname + "`" " 
#the following line runs the command
invoke-expression -command $cmdline  
$destitem = Get-item $destname
$info = [string]::Format( "{0} `t {1} `t {2} `t {3} `t {4} `t {5}", 
$count, 
$partial, $srcname, $destname, $srcitem.Length ,  $destitem.Length)
echo $info
Add-Content $fp $info
$count=$count+1
} 