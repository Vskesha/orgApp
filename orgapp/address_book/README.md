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

### To run this app use `addressbook` or `abk` in terminal after installing `orgApp`.

Follow the prompts and enter the desired command and arguments.


 Available commands:

| Commands             | Description                                |
|:---------------------|:-------------------------------------------|
| add_email            | add an email                               |
| add_phone            | add a phone number                         |
| add                  | add contact to AdressBook                  |
| change_email         | change an email                            |
| change_phone         | change phone number                        |
| when_birthday        | return days until birthday                 |
| exit                 | exit from AdressBook                       |
| find                 | find contact in AdressBook                 |
| all                  | display all contacts                       |
| get_list             | return list of birthdays                   |
| load                 | load information about contacts from file  |
| remove_email         | remove an email                            |
| remove_phone         | remove phone number                        |
| remove               | remove contact from AdressBook             |
| save                 | save information about contacts to file    |
| help                 | display help                               |



This application may be used as a standalone unit for managing your address book 
or can be integrated into a larger organizing application.
###
#### Simple examples of using:

`>>> add_record<br>
Enter contact details:<br>
Name: John Doe<br>
Phone Number (+380________): +380123456789<br>
Birthday (dd.mm.yyyy): 01.01.1990<br>
Email: johndoe@example.com<br>

`>>> add_email<br>
Enter contact name: John Doe<br>
Enter a new email address: johndoe@example.com<br>
Email address successfully added to John Doe's contact.

#### Example Usage for "add_phone_number":

`>>> add_phone_number<br>
Enter contact name: Jane Smith<br>
Enter a new phone number (+380________): +380987654321<br>
Phone number successfully added to Jane Smith's contact.<br>

#### Example Usage for "find_records":

`>>> find_records<br>
Search by criteria:<br>
1.Search by name<br>
2.Search by phone number<br>
Select an option (1 or 2): 1<br>
Enter the name to search for (at least 2 characters): John<br>

Contacts found matching the name "John":<br>
1.John Doe (+380123456789)<br> 
2.Johnny Johnson (+380987654321)<br>
###
#### Example Usage for "get_birthdays_per_week":

`>>> get_birthdays_per_week<br>
Enter the number of days to look ahead: 7<br>
Upcoming birthdays in the next 7 days:<br> 
1.Jane Smith - 04.09.1995<br> 
2.Michael Johnson - 09.09.1988<br>

These examples demonstrate how users can interact with your console bot for various commands. 
<br>
<br>