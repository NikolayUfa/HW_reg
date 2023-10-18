import csv
import re
from pprint import pprint
from difflib import SequenceMatcher



def format_phone(phone_num):
    phone_num = phone_num.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    if len(phone_num) == 10:
        return f"+7({phone_num[:3]}){phone_num[3:6]}-{phone_num[6:8]}-{phone_num[8:]}"
    elif len(phone_num) == 11:
        return f"+7({phone_num[1:4]}){phone_num[4:7]}-{phone_num[7:9]}-{phone_num[9:]}"
    else:
        return phone_num

def similar_name(name1, name2):
    ratio = SequenceMatcher(None, name1, name2).ratio()
    return ratio >= 0.7

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

header = contacts_list.pop(0)

contacts_dict = {}

for contact in contacts_list:
    # Объединяем номер телефона и email в одну строку
    contact[5] = format_phone(contact[5])
    contact[6] = contact[6].strip()

    # Объединяем ФИО в одну строку, учитывая пустые значения
    full_name = " ".join(part for part in contact[:3] if part.strip())
    match = re.match(r"(\S+)\s+(\S+)\s+(\S+)", full_name)
    if match:
        lastname, firstname, surname = match.groups()
    else:

        lastname, firstname, surname = contact[0], contact[1], contact[2]


    similar_contact_id = None
    for person_id, existing_contact in contacts_dict.items():
        existing_full_name = " ".join(part for part in existing_contact[:3] if part.strip())
        if similar_name(full_name, existing_full_name):
            similar_contact_id = person_id
            break


    if similar_contact_id:
        existing_contact = contacts_dict[similar_contact_id]

        for i in range(len(existing_contact)):
            if not existing_contact[i] and contact[i]:
                existing_contact[i] = contact[i]
    else:

        contacts_dict[(lastname, firstname)] = [lastname, firstname, surname, contact[3], contact[4], contact[5], contact[6]]

new_contacts_list = [header] + list(contacts_dict.values())

pprint(new_contacts_list)

with open("phone_book_new.csv", "w", newline='', encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(new_contacts_list)