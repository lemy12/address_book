import ldap
import json
import re

LDAP_SERVER = 'ldap://*.*'
LDAP_LOGIN = '*@*.*'
LDAP_PASSWORD = '*****'
OBJECT_TO_SEARCH = 'objectClass=person'
ATTRIBUTES_TO_SEARCH = ['cn', 'mail', 'telephoneNumber', 'physicalDeliveryOfficeName', 'memberOf', 'userAccountControl']


def sort_for_kierownicy(personnel):                      # wyślij kierowników na górę listy
    for person in personnel:
        if "memberOf" in person.keys():
            if person["memberOf"] == ["Kierownicy"]:
                personnel.remove(person)
                personnel.insert(0, person)
    return personnel


def search_ou(dept_letters, ldap_server):                   # szukaj osób w poszczególnych działach
    search_base = 'OU=' + dept_letters + ',OU=Pracownicy,DC=pch,DC=lan'
    result_ou = ldap_server.search_s(search_base, ldap.SCOPE_SUBTREE, OBJECT_TO_SEARCH, ATTRIBUTES_TO_SEARCH)
    return dept_letters, result_ou


def dept_to_list(dept_letters, result):                     # wypisz wszystkie osoby z danego działu
    personnel_list = []
    for i in result:
        person_dict = {}
        for k, v in i[1].items():
            if k == "memberOf":
                member = re.findall(r'CN=.+?,', v[0].decode("utf-8"))
                for i in range(0, len(member)):
                    member[i] = member[i][3:-1]
                person_dict[k] = member
            else:
                person_dict[k] = v[0].decode("utf-8")
        person_dict['dept'] = dept_letters
        personnel_list.append(person_dict)
    return personnel_list


def get_dept_letters(ldap_server):
    dept_search = ldap_server.search_s('OU=Pracownicy,DC=pch,DC=lan', ldap.SCOPE_SUBTREE, 'objectClass=organizationalUnit', ['ou'])
    dept_letters_list = []
    for each in dept_search:
        dept_letters_list.append(each[1]['ou'][0].decode("utf-8"))
    dept_letters_list.remove('Pracownicy')
    return dept_letters_list


if __name__ == "__main__":
    connect = ldap.initialize(LDAP_SERVER)                 # podłączenie do serwera ldap
    connect.set_option(ldap.OPT_REFERRALS, 0)
    connect.simple_bind_s(LDAP_LOGIN, LDAP_PASSWORD)

    result = []
    for dept_letters in get_dept_letters(connect):              # wyznacz wszystkich pracowników oraz przypisz im odpowiednie
        name, result_temp = search_ou(dept_letters, connect)    # działy skrótami
        result.extend(dept_to_list(name, result_temp))

    print(result)
    print(get_dept_letters(connect))

    result = sort_for_kierownicy(result)                   # wyślij kierowników na górę listy

    with open("depts_list.json", "w", encoding='utf-8') as s:
        json.dump(result, s, ensure_ascii=False, indent=4)
