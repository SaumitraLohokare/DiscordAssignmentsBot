import mechanize
import lxml
from bs4 import BeautifulSoup

url = 'https://lms.vit.ac.in/login/index.php'

async def getAssignments(username, password) -> str:
    br = mechanize.Browser()
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    
    r = br.open(url)
    html = r.read()
    soup = BeautifulSoup(html, 'lxml')

    br.select_form(nr=0)
    br.form['username'] = username
    br.form['password'] = password
    logintoken = br.form['logintoken']

    response = br.submit()
    x = br.open(response.geturl())
    mainpage = x.read()
    soup = BeautifulSoup(mainpage, 'lxml')

    max_title = 0
    max_day = 0
    max_time = 0

    elements = [item for item in soup.find_all(attrs={'data-region': True}) if item['data-region'] == 'event-item']
    assignments = []
    for item in elements:
        title = item.a.text
        if len(title) > max_title:
            max_title = len(title)
        day = item.div.a.text
        if len(day) > max_day:
            max_day = len(day)
        time = item.div.text.split(', ')[-1]
        if len(time) > max_time:
            max_time = len(time)
        assignments.append([title, day, time])

    msg = ''
    for assignment in assignments:
        msg = msg + f'\n{assignment[0][:30]:30s} | {assignment[1]:20s} | {assignment[2]:10s}'
    if msg.strip() == '':
        return 'Incorrect Username or Password.\nOr No upcoming assignments.'
    msg = '```\n' + msg + '\n```'
    return msg