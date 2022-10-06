import requests
import os


def get_sj(token, keyword, town, language):
    objects = []
    results = {}
    count = 0
    more = True
    url = 'https://api.superjob.ru/2.0/vacancies'
    headers = {'X-Api-App-Id': token}
    params = {'town': town,
              'no_agreement': 1,
              'count': 100,
              'page': 0,
              'period': 1,  # 0
              'keyword': f'{keyword} {language}'
              }
    while more is True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        result_sj = response.json()
        vacancies = result_sj['objects']
        for vacancy in vacancies:
            results['id'] = count
            results['profession'] = vacancy['profession']
            results['town'] = vacancy['town']['title']
            results['currency'] = vacancy['currency']
            results['salary_from'] = vacancy['payment_from']
            results['salary_to'] = vacancy['payment_to']
            objects.append(results.copy())
            count += 1
        params['page'] += 1
        more = result_sj['more']
    return objects


def get_filtered_sj():
    objects = {}
    for language in ['Go', 'C', 'C#', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']:
        result = get_sj(os.getenv('SUPERJOBTOKEN'), 'Программист', 'Москва', language)
        objects[language] = result
    return objects
