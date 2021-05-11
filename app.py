from flask import Flask, render_template, request, redirect, send_file
from bs4 import BeautifulSoup
import requests

def getCovidData():
    source = requests.get('https://www.mohfw.gov.in/').text
    soup = BeautifulSoup(source, features="html.parser")

    value = soup.find_all('strong', class_='mob-hide')

    aux = list(value[1].text)
    active_cases = ''
    for i in aux:
        if i == '\xa0': break
        active_cases+=i
    #print(active_cases)

    aux = list(value[3].text)
    cured_cases = ''
    for i in aux:
        if i == '\xa0': break
        cured_cases+=i
    #print(cured_cases)

    aux = list(value[5].text)
    death_count = ''
    for i in aux:
        if i == '\xa0': break
        death_count+=i
    #print(death_count)

    value = soup.find('span', class_='coviddata').text
    vacinated = ''
    for i in value:
        if i!=' ' and i!=',': vacinated+=i
    #print(vacinated)

    value = soup.find('div', class_='status-update')
    aux = value.h5.span.text
    aux = list(aux[8:])
    last_updated = ''
    for i in aux:
        if i=='(' or i=='\n': break
        last_updated+=i
    #print(last_updated)

    value = soup.find_all('div', class_='update-box')
    updates = []
    for i in value: updates.append([i.p.strong.text, i.p.a.text, i.p.a['href']])
    for i in updates: i[1]=i[1][:i[1].index('\n')]
    #print(updates)

    return active_cases, cured_cases, death_count, vacinated, last_updated, updates


app = Flask(__name__) 

@app.after_request
def add_header(r):
    # this function is to emulate the Developer Option -> Network -> Disable Cache
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/', methods=['GET', 'POST'])
def main():
	active, cured, deaths, vaccinated, last_updated, updates = getCovidData()
	return render_template('index.html', _active_=active, _cured_=cured, _deaths_=deaths, _vaccinated_=vaccinated,
						   _updated_=last_updated, _notice_=updates)  

if(__name__ == '__main__'):
	#app.run(debug = False, host='0.0.0.0')
	app.run(debug = False)
