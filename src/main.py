import mechanize
import lxml
from bs4 import BeautifulSoup

url = 'https://lms.vit.ac.in/login/index.php'

def getAssignments() -> [str]:
    br = mechanize.Browser()
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    
    r = br.open(url)
    html = r.read()
    soup = BeautifulSoup(html, 'lxml')

    br.select_form(nr=0)
    br.form['username'] = "19BCE1276"
    br.form['password'] = "Vitcc@9996"
    logintoken = br.form['logintoken']

    response = br.submit()
    x = br.open(response.geturl())
    mainpage = x.read()
    soup = BeautifulSoup(mainpage, 'lxml')

    elements = [item for item in soup.find_all(attrs={'data-region': True}) if item['data-region'] == 'event-item']
    assignments = []
    for item in elements:
        title = item.a.text
        day = item.div.a.text
        time = item.div.text.split(', ')[-1]
        assignments.append(" ".join([title, day, time]))
    
    print(assignments)
    return assignments



if __name__ == '__main__':
    getAssignments()