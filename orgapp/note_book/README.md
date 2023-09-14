# NoteBook Application
Welcome to your note-taking app!

<pre>
                          .                     
                        .o8                     
ooo. .oo.    .ooooo.  .o888oo  .ooooo.   
`888P"Y88b  d88' `88b   888   d88' `88b   
 888   888  888   888   888   888ooo888    
 888   888  888   888   888 . 888    .o  
o888o o888o `Y8bod8P'   "888" `Y8bod8P'  
 .o8                           oooo
"888                           `888
 888oooo.   .ooooo.   .ooooo.   888  oooo
 d88' `88b d88' `88b d88' `88b  888 .8P'
 888   888 888   888 888   888  888888.
 888   888 888   888 888   888  888 `88b.
 `Y8bod8P' `Y8bod8P' `Y8bod8P' o888o o888o
</pre>

### To run this app use `notebook` or `abk` in terminal after installing `orgApp`.

Follow the prompts and enter the desired command and arguments.

 Available commands:

| Commands                       | Action                                  |
|:-------------------------------|:----------------------------------------|
| add, plus                      | adds note to your NoteBook              |
| add_tags                       | add tag to note                         |
| add_fake_notes                 | adds fdke data to the notebook          |
| all, all_notes, view           | displays all notes.                     |
| edit                           | edit a note content in the NoteBook     |
| bye, close, exit, goodbye      | exits the program                       |
| delete                         | deletes note from NoteBook              |
| delete_tag                     | deletes tag from note in NoteBook       |
| tag, find_tag, search_tag      | returns notes with given tags           |
| help                           | outputs this list of commands           |
| load                           | loads notes from the given file         |
| save                           | saves notes to file                     |
| find, search                   | returns notes with given keyword        |


This is a simple console bot for managing notebook
Enter one of the listed commands followed by arguments

`command` `args`. Values must be separated with space.

This application may work as a discrete unit or can be 
a part of a greater orgApp application.


### Simple example of using:

`>>> add<br>
Enter note title: Love<br>
Enter note text: This is a wonderful and amazing feeling!<br>
Enter note tags: life happy<br>
Note added successfully.<br>

`>>> delete<br>
Enter note title: Yesterday<br>
Note deleted successfully.<br>

`>>> all<br>
 All notes:

  1. Title: Today<br>
     Content: Some text<br>
     Tags: a, b, c


  2. Title: Love<br>
     Content: This is a wonderful and amazing feeling!<br>
     Tags: life, happy<br>
<br>
<br>