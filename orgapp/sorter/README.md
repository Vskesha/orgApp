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

### To run this app use `sorter` command in terminal after installing `orgApp`.

Follow the prompts and enter the desired command and arguments.

This application may work as a discrete unit or can be 
a part of a greater orgApp application.

### for sorting folder use:

#### command `sorter path_to_folder` in terminal

if `path_to_folder` is not given, current folder will be sorted

functions in `sorter.py`: 
* recursively scans given `path_to_folder`:
* collects all directories' paths to list `FOLDERS`
* creates new subfolders (`IMAGES`, `VIDEO`, `DOCS`, `MUSIC`, `ARCHIVES` and `MY_OTHER`)
* sorts files in the given `path_to_folder` according to the `REGISTERED_EXTENSIONS`
<br>
<br>