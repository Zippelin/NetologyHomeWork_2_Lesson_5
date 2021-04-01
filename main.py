import csv
import re

class FixPhoneBook:
    def __init__(self, file_path):
        with open(file_path, 'r', encoding="utf8") as f:
            #self.raw_phone_book = list(csv.reader(f, delimiter=","))
            self.raw_phone_book = f.readlines()

    def fix_it(self, save_path):
        pattern = re.compile(
            r'^([А-я]+)[\s|,]?([А-я]+)[\s|,]?([А-я]*),+([А-я]*),?([А-яa-z –-]*),?\+?[7|8]?\s?\(?(\d{3})?\)?[, -]?'
            r'(\d{3})?[ -]?(\d{2})?[ -]?(\d{2})?(\s)?\(?(доб.)?\s?(\d{4})?\)?,([A-z.\d]+@[A-z.]+)?'
        )

        header = self.raw_phone_book[0]
        header = header.lower().rstrip().split(',')
        phone_book_dicts_list = {}
        self.raw_phone_book = self.raw_phone_book[1:]
        for line in self.raw_phone_book:
            fixed_string = pattern.sub(r"\1,\2,\3,\4,\5,+7(\6)\7-\8-\9\10\11\12,\13", line).lower().rstrip().split(',')
            if phone_book_dicts_list.get(fixed_string[0] + fixed_string[1]):
                if not phone_book_dicts_list[fixed_string[0] + fixed_string[1]]['email']:
                    phone_book_dicts_list[fixed_string[0] + fixed_string[1]]['email'] = fixed_string[6]
                if not phone_book_dicts_list[fixed_string[0] + fixed_string[1]]['organization']:
                    phone_book_dicts_list[fixed_string[0] + fixed_string[1]]['organization'] = fixed_string[3]
                if not phone_book_dicts_list[fixed_string[0] + fixed_string[1]]['phone']:
                    phone_book_dicts_list[fixed_string[0] + fixed_string[1]]['phone'] = fixed_string[5]
                if not phone_book_dicts_list[fixed_string[0] + fixed_string[1]]['position']:
                    phone_book_dicts_list[fixed_string[0] + fixed_string[1]]['position'] = fixed_string[4]
            else:
                phone_book_dicts_list[fixed_string[0] + fixed_string[1]] = dict(zip(header, fixed_string))
        phone_book_dicts_list = list(phone_book_dicts_list.values())
        with open(save_path, "w", encoding="utf8", newline='') as f:
            datawriter = csv.DictWriter(f, phone_book_dicts_list[0].keys())
            datawriter.writeheader()
            datawriter.writerows(phone_book_dicts_list)


if __name__ == '__main__':
    phone_book_fixer = FixPhoneBook('phone_book.csv')
    phone_book_fixer.fix_it('phonebook.csv')

