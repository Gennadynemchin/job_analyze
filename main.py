from __future__ import print_function
from dotenv import load_dotenv
from hh import get_filtered_hh
from sj import get_filtered_sj
from terminaltables import AsciiTable


def predict_rub_salary(vacancy):
    if vacancy['currency'] not in ['rub', 'RUR']:
        result = None
    elif vacancy['salary_from'] and vacancy['salary_to']:
        result = (int(vacancy['salary_from']) + int(vacancy['salary_to'])) / 2
    elif not vacancy['salary_to']:
        result = (int(vacancy['salary_from'])) * 1.2
    elif not vacancy['salary_from']:
        result = (int(vacancy['salary_to'])) * 0.8
    return result


def get_summary(filtered_vacancies):
    objects = []
    salaries = []
    summary = {}
    for language, language_info in filtered_vacancies.items():
        nonecount = 0
        for salary in language_info:
            salary['predicted'] = predict_rub_salary(salary)
            if not salary['predicted']:
                nonecount += 1
            else:
                salaries.append(salary['predicted'])
        summary = {'language': language,
                   'found': len(language_info),
                   'processed': len(language_info) - nonecount
                   }
        try:
            summary['average_salary'] = (int(sum(salaries)/len(salaries)))
        except ZeroDivisionError:
            summary['average_salary'] = 0
        objects.append(summary.copy())
    return objects


def main():
    load_dotenv()
    hh = get_summary(get_filtered_hh())
    sj = get_summary(get_filtered_sj())

    title_hh = 'HH Moscow'
    table_data_hh = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    for lang in hh:
        table_data_hh.append([lang['language'], lang['found'], lang['processed'], lang['average_salary']])
    table_hh = AsciiTable(table_data_hh, title_hh)
    print(table_hh.table)

    title_sj = 'Superjob Moscow'
    table_data_sj = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    for lang in sj:
        table_data_sj.append([lang['language'], lang['found'], lang['processed'], lang['average_salary']])
    table_sj = AsciiTable(table_data_sj, title_sj)
    print(table_sj.table)


if __name__ == '__main__':
    main()
