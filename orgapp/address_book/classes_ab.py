"""
Андрій сюди скопіюй класи для адресної книги
По можливості додай typehints для методів класу і докстрінги (якщо не знаєш що це
то скидай як є і потім якось доробимо)
"""
# #АДРЕСНА КНИГА

from collections import UserDict
from datetime import datetime, timedelta
import calendar
import re
import json

class AddressBook(UserDict):
    def add_record(self, record):
        if self.validate_record(record):
            key = record.name.value
            self.data[key] = record
            return True
        else:
            return False

    def remove_record(self, name):
        if name in self.data:
            del self.data[name]
            return True
        else:
            return False

    def find_records(self, **search_criteria):
        result = []
        found = False
        for record in self.data.values():
            if 'name' in search_criteria and len(search_criteria['name']) >= 2 and search_criteria[
                'name'] in record.name.value:
                result.append(record)
                found = True
            if 'phones' in search_criteria and len(search_criteria['phones']) >= 5:
                for phone in record.phones:
                    if search_criteria['phones'] in phone.value:
                        result.append(record)
                        found = True
                        break
        if not found:
            print("Немає контакту, що відповідає заданим критеріям пошуку")
        return result


    def validate_record(self, record):
        valid_phones = all(isinstance(phone, Phone) and phone.validate(phone.value) for phone in record.phones)
        valid_name = isinstance(record.name, Name)

        if record.birthday:
            valid_birthday = isinstance(record.birthday, Birthday) and record.birthday.validate(record.birthday.value)
        else:
            valid_birthday = True

        if record.email:
            valid_email = isinstance(record.email, Email) and record.email.validate(record.email.value)
        else:
            valid_email = True

        if not valid_phones:
            print("Номери телефонів не валідні.")
        if not valid_name:
            print("Ім'я не валідне.")
        if not valid_birthday:
            print("Дата народження не валідна.")
        if not valid_email:
            print("Пошта не валідна.")

        return valid_phones and valid_name and valid_birthday and valid_email

    def get_record_by_name(self, name):
        for record in self.data.values():
            if record.name.value == name:
                return record
        return None

    def get_birthdays_per_week(self, num):
        to_day = datetime.now().date()
        new_date = to_day + timedelta(days=num)

        happy_birthday = []
        for record in self.data.values():
            if record.birthday:
                birthdate = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
                if birthdate.day == new_date.day and birthdate.month == new_date.month:
                    happy_birthday.append(record.name.value)

        print(f'Cписок іменнинників, яких треба вітати через {num} дні(ів): {happy_birthday}')
        return happy_birthday


    def get_all_records(self):
        all_contacts = []
        header = '{:<20} {:<20} {:<20} {:<15}'.format('Ім\'я', 'Телефон', 'День народження', 'Ел. пошта')
        separator = '-' * len(header)
        all_contacts.append(header)
        all_contacts.append(separator)

        if self.data:
            for record in self.data.values():
                record_str = '{:<20} {:<20} {:<20} {:<15}'.format(
                    record.name.value,
                    ', '.join(phone.value for phone in record.phones),
                    record.birthday.value if record.birthday else '-',
                    record.email.value if record.email else '-'
                )
                all_contacts.append(record_str)
        else:
            all_contacts.append("Адресна книга порожня")

        return '\n'.join(all_contacts)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.data):
            record = list(self.data.values())[self.index]
            self.index += 1
            return record
        else:
            raise StopIteration

    def iterator(self, n):
        return (list(self.data.values())[i:i + n] for i in range(0, len(self.data), n))


    def __str__(self):
        book_str = "\n".join(f"{name}: {record}" for name, record in self.data.items())
        return book_str


class Record:
    def __init__(self, name, phone=None, birthday=None, email=None):
        self.birthday = Birthday(birthday) if birthday is not None else None
        self.email = Email(email) if email is not None else None
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone is not None else []


    def add_email(self, email_value):
        if email_value:
            self.email = Email(email_value)
            return True
        return False

    def remove_email(self, del_email):
        if self.email and self.email.value == del_email:
            self.email = None
            return True
        return False

    def change_email(self, email, new_email_value):
        if self.email is not None and self.email.value == email:
            if self.email.validate(new_email_value):
                self.email = Email(new_email_value)
                return True
        return False

    def add_phone_number(self, number):
        phone = Phone(number)
        if phone.validate(number):
            self.phones.append(phone)
            return True
        else:
            return False

    def remove_phone_number(self, number):
        if any(phone.value == number for phone in self.phones):
            new_phones = [phone for phone in self.phones if phone.value != number]
            self.phones = new_phones
            return True
        return False

    def change_phone_number(self, number, new_number):
        for index, phone in enumerate(self.phones):
            if phone.value == number:
                self.phones[index] = Phone(new_number)
                return True
        return False

    def days_to_birthday(self):
        if self.birthday and self.birthday.validate(self.birthday.value):
            parsed_date = datetime.strptime(self.birthday.value, '%d.%m.%Y').date()
            date_now = datetime.now().date()
            date_now_year = date_now.year
            next_year = date_now.year + 1
            parsed_date = parsed_date.replace(year=date_now_year)

            if parsed_date <= date_now:
                if calendar.isleap(next_year):
                    time_delta = (parsed_date - date_now + timedelta(days=366)).days
                else:
                    time_delta = (parsed_date - date_now + timedelta(days=365)).days
            else:
                time_delta = (parsed_date - date_now).days
            return time_delta
        else:
            return None

    def __str__(self):
        phones_str = ', '.join(str(phone) for phone in self.phones)
        if not phones_str:
            phones_str = "None"
        if not self.birthday:
            birthday_str = "None"
        else:
            birthday_str = self.birthday.value
        if not self.email:
            email_str = "None"
        else:
            email_str = self.email.value
        return f"Name: {self.name.value}, Phones: {phones_str}, Email: {email_str}, Birthday: {birthday_str}"

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    def validate(self, new_value):
        return True

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


    def __str__(self):
        return str(self.value)


class Phone(Field):
    def __init__(self, value=None):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value):
        if self.validate(new_value):
            Field.value.fset(self, new_value)
        else:
            print(f'Номер телефону {new_value} не можна призначити, оскільки він не валідний')

    def validate(self, number):
        if number is None:
            return False
        try:
            phone_format = r'\+380\d{9}'
            if not re.match(phone_format, number):
                return False
            return True
        except ValueError:
            return False

class Email(Field):
    def __init__(self, value=None):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value):
        if self.validate(new_value):
            Field.value.fset(self, new_value)
        else:
            print(f'Пошту {new_value} не можна призначити, вона не валідна')

    def validate(self, email):
        if email is None:
            return False
        try:
            email_format = r'\b(?![A-Za-z0-9._%+-]*a@t[A-Za-z0-9._%+-]*)\b(?![0-9]{2})[A-Za-z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
            if not re.match(email_format, email):
                return False
            return True
        except ValueError:
            return False


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value):
        if self.validate(new_value):
            Field.value.fset(self, new_value)
        else:
            print(f'Дату дня народження {new_value} не можна призначити, оскільки вона не валідна')

    def validate(self, new_value):
        try:
            parsed_date = datetime.strptime(new_value, '%d.%m.%Y').date()
            today = datetime.now().date()
            if parsed_date > today:
                return False
            return True
        except ValueError:
            return False
        except TypeError:
            return False


class AddressBookFileHandler:
    def __init__(self, file_name):
        self.file_name = file_name

    def save_to_file(self, address_book):
        with open(self.file_name, 'w') as file:
            json.dump(address_book.data, file, default=self._serialize_record, indent=4)

    def _deserialize_record(self, contact_data):
        print(f"Спроба десеріалізації: {contact_data}")

        if isinstance(contact_data, str):
            return None

        name = contact_data.get('name')
        phones = contact_data.get('phones', [])
        birthday = contact_data.get('birthday')
        email = contact_data.get('email')


        return Record(name, phones[0] if phones else None, birthday, email)

    def load_from_file(self):
        try:
            with open(self.file_name, 'r') as file:
                file_contents = file.read()
                print(f"Зчитані дані з файлу: {file_contents}")

                if not file_contents.strip():
                    print("Файл порожній. Повертаємо порожню адресну книгу.")
                    return AddressBook()

                try:
                    data = json.loads(file_contents)
                    if data is not None:
                        address_book = AddressBook()
                        address_book.data = data
                        print(f"Deserialized data: {data}")
                        return address_book
                    else:
                        print("Помилка: Не вдалося розпізнати дані з файлу.")
                        return None
                except json.JSONDecodeError as e:
                    print(f"Помилка: Не вдалося розпізнати дані з файлу. Помилка JSON: {e}")
                    return None

        except FileNotFoundError:
            with open(self.file_name, 'w') as file:
                file.write("{}")
            return AddressBook()

    def _serialize_record(self, record):
        return {
            'name': record.name.value,
            'phones': [phone.value for phone in record.phones],
            'birthday': record.birthday.value if record.birthday else None,
            'email': record.email.value if record.email else None
        }


if __name__ == "__main__":
    pass
