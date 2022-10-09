from __future__ import print_function
import os
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


def get_processed_vacancies(filtered_vacancies):
    objects = []
    salaries = []
    for language_name, language_info in filtered_vacancies.items():
        nonecount = 0
        for salary in language_info:
            salary['predicted'] = predict_rub_salary(salary)
            if not salary['predicted']:
                nonecount += 1
            else:
                salaries.append(salary['predicted'])
        summary = {'language': language_name,
                   'found': len(language_info),
                   'processed': len(language_info) - nonecount
                   }
        try:
            summary['average_salary'] = (int(sum(salaries)/len(salaries)))
        except ZeroDivisionError:
            summary['average_salary'] = 0
        objects.append(summary.copy())
    return objects


def creating_table(title_name, vacancies_for_table):
    column_titles = ['Язык программирования',
                     'Вакансий найдено',
                     'Вакансий обработано',
                     'Средняя зарплата']
    table_vacancies = [column_titles]
    for vacancy in vacancies_for_table:
        table_vacancies.append([vacancy['language'],
                                vacancy['found'],
                                vacancy['processed'],
                                vacancy['average_salary']])
    created_table = AsciiTable(table_vacancies, title_name)
    return created_table.table


def main():
    load_dotenv()
    superjob_token = os.getenv('SUPERJOBTOKEN')
    hh_vacancies = get_processed_vacancies(get_filtered_hh())
    sj_vacancies = get_processed_vacancies(get_filtered_sj(superjob_token))

    print(creating_table('HH Moscow', hh_vacancies))
    print(creating_table('Superjob Moscow', sj_vacancies))


if __name__ == '__main__':
    main()
