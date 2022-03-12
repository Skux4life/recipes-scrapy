import csv
from requests_html import HTMLSession

base_url = 'https://www.airbnb.com.au'
location = input('Enter the location: ') + '--Victoria'
checkin_date = input('Enter the checkin date (yyyy-mm-dd): ')
checkout_date = input('Enter the checkout date (yyyy-mm-dd): ')

def set_url():    
    return f'{base_url}/s/{location}/homes?checkin={checkin_date}&checkout={checkout_date}'

def get_url_list(url):
    url_list = []
    for i in range(6):
        offset = 20 * i
        url_pagination = url + f'&items_offset={offset}'
        url_list.append(url_pagination)
    return url_list

def get_html(url):
    session = HTMLSession()
    r = session.get(url)
    return r.html

def render_html(response):
    response.render(sleep=5)

def get_results_list(response):
    return response.find('div._fhph4u div.cm4lcvy[role=group]')

def write_accommodations_to_file(results_list):    
    for item in results_list:
        link = base_url + item.xpath("//a/@href")[0]
        name = item.find('div.kc26pza div span', first = True).text.encode("ascii", "ignore")
        desc = item.find('div.kc26pza div div', first = True).text
        price = item.find('div._1n700sq div span', first = True).text

        try:
            rating = item.find('div.b14n1p2a div span', first = True).attrs['aria-label']
        except KeyError:
            rating = 'Not yet rated'
        
        feature_elements = item.find('div.i1wgresd span')
        features = ''
        for feature in feature_elements:
            features += feature.text    

        accommodation = [link, name, desc, price, rating, features]
        writer.writerow(accommodation)

base_url = set_url()
url_list = get_url_list(base_url)

with open('accommodations.csv', 'a', newline ='') as file:
    writer = csv.writer(file)
    column_headers = ["link", "name", "description", "price", "rating", "features"]
    writer.writerow(column_headers)

    for url in url_list:
        response = get_html(url)
        render_html(response)
        results_list = get_results_list(response)

        write_accommodations_to_file(results_list)
    








