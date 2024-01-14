import requests
import time
import sys

# Retrieve all waybackmachine pages from a twitter profile.
# Usage: waybacktwitter.py USERNAME

if len(sys.argv) == 2:
    print(f"Run: python script.py {sys.argv[1]}")
    username = sys.argv[1]
else:
    username = input("Add username: ")

fichier_name = f"{username}.csv"
current_timestamp = int(time.time() * 1000)

url_template = 'https://web.archive.org/web/timemap/?url=https%3A%2F%2Ftwitter.com%2F{username}%2F&matchType=prefix&collapse=urlkey&output=json&fl=original%2Cmimetype%2Ctimestamp%2Cendtimestamp%2Cgroupcount%2Cuniqcount&filter=!statuscode%3A%5B45%5D..&limit=100000&_={current_timestamp}'
url = url_template.format(username=username, current_timestamp=current_timestamp)

reponse = requests.get(url)
donnees_traitees_liste = reponse.text.replace('"', '').replace('[', '').replace(']', '')

if reponse.status_code == 200:
    with open(fichier_name, mode='w', encoding='utf-8') as file:
        data = donnees_traitees_liste.split('\n')
        new_cols =f'webarchive_url,{data[0]}'
        file.write(f'{new_cols}\n')
        for row in data[1:]:
            new_url=f'https://web.archive.org/web/*/{row.split(",")[0]},{row}'
            current_data = f'{new_url}\n'
            file.write(current_data)

elif reponse.status_code != 200:
    print(f"Error code : {reponse.status_code}")
    exit(-1)

exit()
