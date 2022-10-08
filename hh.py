import requests


# get role ID for requested vacancy
def get_role_hh(text):
    url = 'https://api.hh.ru/suggests/professional_roles'
    params = {'text': text}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['items'][0]['id']


def get_hh_vacancies(role, language):
    hh_vacancies = []
    count = 0
    pages = 20
    area = 1
    period = 10
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
        hh_response = response.json()
        vacancies = hh_response['items']
        for vacancy in vacancies:
            hh_vacancy = {'id': count,
                          'currency': vacancy['salary']['currency'],
                          'salary_from': vacancy['salary']['from'],
                          'salary_to': vacancy['salary']['to']
                          }
            hh_vacancies.append(hh_vacancy.copy())
            count += 1
        params['page'] += 1
    return hh_vacancies


def get_filtered_hh():
    filtered_vacancies = {}
    role_id = get_role_hh('Программист')
    for language in ['Go', 'C', 'C#', 'C++', 'PHP', 'Ruby', 'Python', 'Java', 'JavaScript']:
        filtered_result = get_hh_vacancies(role_id, language)
        filtered_vacancies[language] = filtered_result
    return filtered_vacancies
