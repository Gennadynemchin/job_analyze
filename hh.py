import requests


# get role ID for requested vacancy
def get_role_hh(text):
    url = 'https://api.hh.ru/suggests/professional_roles'
    params = {'text': text}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['items'][0]['id']


def get_hh_vacancies(role, language):
    objects = []
    results = {}
    count = 0
    pages = 20
    area = 1
    period = 1  # 10
    per_page = 100
    start_page = 0
    url = 'https://api.hh.ru/vacancies'
    params = {'text': language,
              'area': area,
              'period': period,
              'per_page': per_page,
              'page': start_page,
              'only_with_salary': 'true',
              'currency': 'RUR',
              'professional_role': role}
    while pages > params['page']:
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()
        vacancies = result['items']
        for vacancy in vacancies:
            results['id'] = count
            results['profession'] = vacancy['name']
            results['town'] = vacancy['area']['name']
            results['currency'] = vacancy['salary']['currency']
            results['salary_from'] = vacancy['salary']['from']
            results['salary_to'] = vacancy['salary']['to']
            objects.append(results.copy())
            count += 1
        params['page'] += 1
    return objects


def get_filtered_hh():
    filtered_vacancies = {}
    role_id = get_role_hh('Программист')
    for language in ['Go', 'C', 'C#', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']:
        result = get_hh_vacancies(role_id, language)
        filtered_vacancies[language] = result
    return filtered_vacancies
