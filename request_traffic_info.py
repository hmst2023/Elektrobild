import requests
from bs4 import BeautifulSoup


URL = "https://www.verkehrsinformation.de/A9"
try:
    page = requests.get(URL, timeout=2)
except requests.exceptions.RequestException as e:
    raise SystemExit(e)

soup = BeautifulSoup(page.content, "html.parser")
result = []
findlings = soup.find_all(class_="line-clamp-20 w-full mb-4")
for i in findlings:
    if i.text:
        result.append(i.text.replace('Ä','Ae').replace('ä','ae').replace('Ü','ue').replace('ü','ue')
                      .replace('Ö','Oe').replace('ö', 'oe').replace('ß','ss'))
if result:
    with open(r'test.txt', 'w') as file:
        for i in result:
            file.write(i+'\n')
    file.close()


print(result)
