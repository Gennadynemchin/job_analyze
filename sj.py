import requests
import os


def get_sj_vacancies(token, keyword, town, language):
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
    while more:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        sj_response = response.json()
        vacancies = sj_response['objects']
        for vacancy in vacancies:
            sj_vacancy = {'id': count,
                          'currency': vacancy['currency'],
                          'salary_from': vacancy['payment_from'],
                          'salary_to': vacancy['payment_to']
                          }
            sj_vacancies.append(sj_vacancy.copy())
            count += 1
        params['page'] += 1
        more = sj_response['more']
    return sj_vacancies


def get_filtered_sj():
    objects = {}
    for language in ['Go', 'C', 'C#', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']:
        result = get_sj_vacancies(os.getenv('SUPERJOBTOKEN'), 'Программист', 'Москва', language)
        objects[language] = result
    return objects
