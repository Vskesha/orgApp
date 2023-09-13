# AdressBook Application
Welcome to your adress-taking app!

<pre>
                .o8
               "888
 .oooo.    .oooo888  oooo d8b  .ooooo.   .oooo.o  .oooo.o
`P  )88b  d88' `888  `888""8P d88' `88b d88(  "8 d88(  "8
 .oP"888  888   888   888     888ooo888 `"Y88b.  `"Y88b.
d8(  888  888   888   888     888    .o o.  )88b o.  )88b
`Y888""8o `Y8bod88P" d888b    `Y8bod8P' 8""888P' 8""888P'

"888                           `888
 888oooo.   .ooooo.   .ooooo.   888  oooo
 d88' `88b d88' `88b d88' `88b  888 .8P'
 888   888 888   888 888   888  888888.
 888   888 888   888 888   888  888 `88b.
 `Y8bod8P' `Y8bod8P' `Y8bod8P' o888o o888o
</pre>

 Available commands:

|           Commands             |     Action                               |
|:-------------------------------|:---------------------------------------- |
|  add                           | add contact to AdressBook                |
|  add_email                     | add an email                             |
|  add_phone                     | add phone number                         |
|  all                           | display all contacts                     |
|  change_email                  | change an email                          |
|  change_phone                  | change phone number                      |
|  exit                          | exit from AdressBook                     |
|  find                          | find contact in AdressBook               |
|  get_list                      | return list of birthdays                 |
|  load                          | load information about contacts from file|
|  remove_email                  | remove email address                     |
|  remove_phone                  | remove phone number                      |
|  remove_email                  | remove contact from AdressBook           |
|  remove_email                  | save information about contacts to file  |
|  when_birthday                 | return days until birthday               |
|  help                          | display help               |


This application can function as a standalone unit for managing your address book or can be integrated into a larger organizational application.

Usage:
Run the script.
Follow the prompts and enter the desired command and arguments.

Simple examples of using:

>>> add_record
Enter contact details:
Name: John Doe
Phone Number (+380________): +380123456789
Birthday (dd.mm.yyyy): 01.01.1990
Email: johndoe@example.com

>>> add_email
Enter contact name: John Doe
Enter a new email address: johndoe@example.com
Email address successfully added to John Doe's contact.
Example Usage for "add_phone_number":

>>> add_phone_number
Enter contact name: Jane Smith
Enter a new phone number (+380________): +380987654321
Phone number successfully added to Jane Smith's contact.
Example Usage for "find_records":

>>> find_records
Search by criteria:
1. Search by name
2. Search by phone number
Select an option (1 or 2): 1
Enter the name to search for (at least 2 characters): John
Contacts found matching the name "John":
1. John Doe (+380123456789)
2. Johnny Johnson (+380987654321)
Example Usage for "get_birthdays_per_week":

>>> get_birthdays_per_week
Enter the number of days to look ahead: 7
Upcoming birthdays in the next 7 days:
1. Jane Smith - 04.09.1995
2. Michael Johnson - 09.09.1988

These examples demonstrate how users can interact with your console bot for various commands. 
