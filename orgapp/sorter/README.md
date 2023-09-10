# Sorter Application
<pre>
 .oooooo..o                        .                      
d8P'    `Y8                      .o8                      
Y88bo.       .ooooo.  oooo d8b .o888oo  .ooooo.  oooo d8b 
 `"Y8888o.  d88' `88b `888""8P   888   d88' `88b `888""8P 
     `"Y88b 888   888  888       888   888ooo888  888     
oo     .d8P 888   888  888       888 . 888    .o  888     
8""88888P'  `Y8bod8P' d888b      "888" `Y8bod8P' d888b    
</pre>

This application may work as a discrete unit or can be 
a part of a greater orgApp application.

### for sorting folder use:

command `sorter path_to_folder` or

`python3 -m sorter path_to_folder` in terminal

after installing `sorter` package

if `path_to_folder` is not given, current folder will be sorted

functions in `sorter.py` recursively scans given 'folder' and:
* adds all directories' paths to `FOLDERS`
* adds files' paths to proper lists (`IMAGES`, `VIDEO`, `DOCS`, `MUSIC`, `ARCHIVES` or `MY_OTHER`)based on file extension
* adds all encountered extensions to `KNOWN_EXTENSIONS` or `UNKNOWN_EXTENSIONS` according to `REGISTERED_EXTENSIONS`
* sorts files in the given `path_to_folder` according to the `REGISTERED_EXTENSIONS` in `sorter/sorter.py`