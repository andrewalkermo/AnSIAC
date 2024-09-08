import json
from datetime import datetime
import requests

from bs4 import BeautifulSoup
from config import settings

USERNAME = settings.get('siac.username')
PASSWORD = settings.get('siac.password')
BOT_TOKEN = settings.get('telegram.bot_token')
CHAT_ID = settings.get('telegram.chat_id')
def login() -> requests.Response:

  headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://siac.ufba.br',
    'Pragma': 'no-cache',
    'Referer': 'https://siac.ufba.br/SiacWWW/Logoff.do',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"'
  }

  data = {
    'cpf': USERNAME,
    'senha': PASSWORD,
    'x': '28',
    'y': '11'
  }

  login_url = 'https://siac.ufba.br/SiacWWW/LogonSubmit.do'
  response = requests.post(login_url, headers=headers, data=data)
  if response.status_code == 200:
    return response
  else:
    raise Exception('Login failed')

def get_classes():
  response = login()

  coef_url = 'https://siac.ufba.br/SiacWWW/ConsultarComponentesCurricularesCursados.do'
  response = requests.get(coef_url, cookies=response.cookies)
  semester = '2024.1'
  semester_classes = []

  if response.status_code != 200:
    raise Exception('Failed to get classes')

  soup = BeautifulSoup(response.content, 'html.parser')
  table = soup.find('table', {'class': 'corpoHistorico'})
  tr_elements = table.find_all('tr')
  found = False

  if not found:
    for index, tr in enumerate(tr_elements):
      if not found:
        td_elements = tr.find_all('td')
        for td in td_elements:
          if td.b and td.b.text.strip() == semester:
            tr_elements = tr_elements[index:len(tr_elements)-1]
            found = True
            break
  if not found:
    raise Exception('Semester not found')

  for index, tr in enumerate(tr_elements):
    td_elements = tr.find_all('td')

    name = td_elements[2].text.strip()
    grade = td_elements[6].text.strip()
    result = td_elements[7].text.strip()

    semester_classes.append({
      'name': name,
      'grade': grade,
      'result': result
    })

  return semester_classes

def verify_grades():
  semester_classes = get_classes()
  last_grades = []

  try:
    with open('grades.json', 'r') as file:
      last_grades = json.load(file)
  except:
    print('Last grades not found')
    last_grades = semester_classes
    pass

  for semester_class, last_grade in zip(semester_classes, last_grades):
    if semester_class['grade'] != '--':
      print(f"{semester_class['name']} - {semester_class['grade']} - {semester_class['result']}")
      if semester_class['grade'] != last_grade['grade']:
        print('New grade found!')
        send_telegram_message(f"Nova nota: {semester_class['name']}: {semester_class['grade']} - {semester_class['result']}")

  with open('grades.json', 'w') as file:
    json.dump(semester_classes, file)

def send_telegram_message(message):
  base_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
  payload = {
    "chat_id": CHAT_ID,
    "text": message,
  }

  requests.post(base_url, data=payload)

def get_semester():
  current_date = datetime.now()

  year = current_date.year
  semester = None

  spring_start = datetime(year, 1, 1)
  spring_end = datetime(year, 6, 30)
  fall_start = datetime(year, 7, 1)
  fall_end = datetime(year, 12, 31)

  if spring_start <= current_date <= spring_end:
    semester = "2"
  elif fall_start <= current_date <= fall_end:
    semester = "1"

  if semester:
    return f"{year}.{semester}"
  else:
    return None

if __name__ == '__main__':
  verify_grades()
