import requests
import os


def get_sj(token, keyword, town, language):
    sj_vacancies = []
    count = 0
    more = True
    url = 'https://api.superjob.ru/2.0/vacancies'
    headers = {'X-Api-App-Id': token}
    params = {'town': town,
              'no_agreement': 1,
              'count': 100,
              'page': 0,
              'period': 0,
              'keyword': f'{keyword} {language}'
              }
    while more is True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        result_sj = response.json()
        vacancies = result_sj['objects']
        for vacancy in vacancies:
            sj_vacancy = {'id': count,
                          'profession': vacancy['profession'],
                          'town': vacancy['town']['title'],
                          'currency': vacancy['currency'],
                          'salary_from': vacancy['payment_from'],
                          'salary_to': vacancy['payment_to']
                          }
            sj_vacancies.append(sj_vacancy.copy())
            count += 1
        params['page'] += 1
        more = result_sj['more']
    return sj_vacancies


def get_filtered_sj():
    objects = {}
    for language in ['Go', 'C', 'C#', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']:
        result = get_sj(os.getenv('SUPERJOBTOKEN'), 'Программист', 'Москва', language)
        objects[language] = result
    return objects
