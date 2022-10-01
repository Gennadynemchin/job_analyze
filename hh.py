import requests


# get role ID for requested vacancy
def get_role_hh(text):
    url = 'https://api.hh.ru/suggests/professional_roles'
    params = {'text': text}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['items'][0]['id']


def get_hh(role, language):
    objects = []
    result_dict = {}
    count = 0
    pages = 20
    url = 'https://api.hh.ru/vacancies'
    params = {'text': language,
              'area': 1,
              'period': 10,
              'per_page': 100,
              'page': 0,
              'only_with_salary': 'true',
              'currency': 'RUR',
              'professional_role': role}
    while pages > params['page']:
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()
        vacancies = result['items']
        for vacancy in vacancies:
            result_dict['id'] = count
            result_dict['profession'] = vacancy['name']
            result_dict['town'] = vacancy['area']['name']
            result_dict['currency'] = vacancy['salary']['currency']
            result_dict['salary_from'] = vacancy['salary']['from']
            result_dict['salary_to'] = vacancy['salary']['to']
            objects.append(result_dict.copy())
            count += 1
        params['page'] += 1
    return objects


def get_filtered_hh():
    objects = {}
    language_list = ['Go', 'C', 'C#', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']
    for language in language_list:
        result = get_hh(get_role_hh('Программист'), language)
        objects[language] = result
    return objects
