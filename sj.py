import requests
import os


def get_sj(token, keyword, town, language):
    objects = []
    result_dict = {}
    count = 0
    no_agreement = 1
    count = 100
    start_page = 0
    period = 0
    more = True
    url = 'https://api.superjob.ru/2.0/vacancies'
    headers = {'X-Api-App-Id': token}
    params = {'town': town,
              'no_agreement': no_agreement,
              'count': count,
              'page': start_page,
              'period': period,
              'keyword': f'{keyword} {language}'
              }
    while more is True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        result_sj = response.json()
        vacancies = result_sj['objects']
        for vacancy in vacancies:
            result_dict['id'] = count
            result_dict['profession'] = vacancy['profession']
            result_dict['town'] = vacancy['town']['title']
            result_dict['currency'] = vacancy['currency']
            result_dict['salary_from'] = vacancy['payment_from']
            result_dict['salary_to'] = vacancy['payment_to']
            objects.append(result_dict.copy())
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
