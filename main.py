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

    title_hh = 'Headhunter Moscow'
    vacancies_hh = (
        ('Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'),
        (hh[0]['language'], hh[0]['found'], hh[0]['processed'], hh[0]['average_salary']),
        (hh[1]['language'], hh[1]['found'], hh[1]['processed'], hh[1]['average_salary']),
        (hh[2]['language'], hh[2]['found'], hh[2]['processed'], hh[2]['average_salary']),
        (hh[3]['language'], hh[3]['found'], hh[3]['processed'], hh[3]['average_salary']),
        (hh[4]['language'], hh[4]['found'], hh[4]['processed'], hh[4]['average_salary']),
        (hh[5]['language'], hh[5]['found'], hh[5]['processed'], hh[5]['average_salary']),
        (hh[6]['language'], hh[6]['found'], hh[6]['processed'], hh[6]['average_salary']),
        (hh[7]['language'], hh[7]['found'], hh[7]['processed'], hh[7]['average_salary']),
        (hh[8]['language'], hh[8]['found'], hh[8]['processed'], hh[8]['average_salary']),
    )

    table_instance = AsciiTable(vacancies_hh, title_hh)
    table_instance.justify_columns[2] = 'right'
    print(table_instance.table)
    print()

    title_sj = 'Superjob Moscow'
    vacancies_sj = (
        ('Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'),
        (sj[0]['language'], sj[0]['found'], sj[0]['processed'], sj[0]['average_salary']),
        (sj[1]['language'], sj[1]['found'], sj[1]['processed'], sj[1]['average_salary']),
        (sj[2]['language'], sj[2]['found'], sj[2]['processed'], sj[2]['average_salary']),
        (sj[3]['language'], sj[3]['found'], sj[3]['processed'], sj[3]['average_salary']),
        (sj[4]['language'], sj[4]['found'], sj[4]['processed'], sj[4]['average_salary']),
        (sj[5]['language'], sj[5]['found'], sj[5]['processed'], sj[5]['average_salary']),
        (sj[6]['language'], sj[6]['found'], sj[6]['processed'], sj[6]['average_salary']),
        (sj[7]['language'], sj[7]['found'], sj[7]['processed'], sj[7]['average_salary']),
        (sj[8]['language'], sj[8]['found'], sj[8]['processed'], sj[8]['average_salary']),
    )

    table_instance = AsciiTable(vacancies_sj, title_sj)
    table_instance.justify_columns[2] = 'right'
    print(table_instance.table)
    print()


if __name__ == '__main__':
    main()
