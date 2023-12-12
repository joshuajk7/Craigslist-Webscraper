import requests
import time
import json
from bs4 import BeautifulSoup
import zmq
import pandas as pd


def suggest_filter():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5556")
    socket.setsockopt(zmq.RCVTIMEO, 2000)

    # Send a request for filters
    socket.send_string("Send a package of car filters")

    # Wait for the reply from the microservice
    try:
        filters_json_data = socket.recv_string()
    except zmq.error.Again as e:
        return print(f'No suggestion made. Make sure filter-suggestor.py is running and try again. ')

    filters = json.loads(filters_json_data)
    # year_brand_model = (f"{filters['max-year']} {filters['make']} {filters['model']}")
    year_brand_model = f"{filters['make']} {filters['model']}"
    car_price_min = filters['min-price']
    car_price_max = filters['max-price']
    location = ''

    filters = {
        'title': year_brand_model,
        'price': [car_price_min, car_price_max],
        'location': location
    }

    return filters


def grabListings():
    total_pages = 1
    base_url = 'https://seattle.craigslist.org/search/cta?auto_title_status=1&hasPic=1#search=1~list~{}'

    car_listings = []

    with requests.Session() as session:
        for page in range(0, total_pages):
            page_url = base_url.format(page)
            page_response = session.get(page_url)

            html_soup = BeautifulSoup(page_response.text, 'html.parser')

            # get individual cars&trucks posts
            posts = html_soup.find_all('li', {"class": "cl-static-search-result"})

            for post in posts:
                car_info = {'title': post.find('div', class_='title').text.strip(),
                            'price': post.find('div', class_='price').text.strip(),
                            'details': post.find('div', class_='details').text.strip(),
                            'location': post.find('div', class_='location').text.strip()}
                get_link = post.find('a', href=True)
                car_info['link'] = get_link['href']
                if car_info not in car_listings:
                    car_listings.append(car_info)

            page_response.close()

        return mainSearch(car_listings)


def mainSearch(car_listings):
    print('SEATTLE CRAIGSLIST CARS&AUTO WEBSCRAPER')
    print('Car Year Brand Model | minimum car price - maximum car price | location\n')

    print('Specify your Car Search. Press Enter key to skip.\n')  # Search Cars and Specify filters
    user_input = input(
        '-Select the Car Year Brand Model you would like to search for (e.g. 2018 Toyota Camry)\n-Or Suggest a Car! ('
        'suggest) ')
    if user_input == 'suggest':
        # Implement microservice
        filters = suggest_filter()

    else:
        year_brand_model = user_input

        car_price_min = input("Filter by minimum car price: ")

        car_price_max = input("Filter by maximum car price: ")

        location = input('Filter by location: ')

        filters = {
            'title': year_brand_model,
            'price': [car_price_min, car_price_max],
            'location': location
        }

    filterCars(car_listings, filters)


def editFilter(car_listings, filters):
    print('Type which filter you would like to edit.')
    change = input('title | min price | max price | location\n')
    if change == 'title':
        filters['title'] = input(
            'Select the Car Year Brand Model you would like to search for (e.g. 2018 Toyota Camry): ')

    elif change == 'min price':
        filters['price'][0] = input("Filter by minimum car price: ")

    elif change == 'max price':
        filters['price'][1] = input("Filter by maximum car price: ")

    elif change == 'location':
        filters['location'] = input('Filter by location: ')

    else:
        print("Sorry, I didn't catch that. Try again.")
    return filterCars(car_listings, filters)


def filterCars(car_listings, filters):
    """Takes a parameter all car_listings and filters and makes new sorted_cars list."""

    sorted_cars = []

    if filters['title'] == '':
        sorted_cars = car_listings
    else:
        for car in car_listings:  # add cars from car_listings[{},{}] into sorted_cars if name is the same, else sorted_cars = car_listings
            if filters['title'] in car['title']:
                sorted_cars.append(car)

    for car in sorted_cars:
        car_price_int = car['price']
        car_price_int = int(car_price_int.replace('$', '').replace(',', ''))  # int(car['price'][1:])

        if (filters['price'][0] != '') and (int(filters['price'][0]) > car_price_int):
            car['title'] = 'skip'
        elif (filters['price'][1] != '') and (int(filters['price'][1]) < car_price_int):
            car['title'] = 'skip'
        elif filters['location'] != car['location'] and filters['location'] != '':
            car['title'] = 'skip'
    final_sort = [car for car in sorted_cars if car['title'] != 'skip']
    return showResults(filters, final_sort, car_listings)


def showResults(filters, final_sort, car_listings):
    print(
        f"\nCar Year Brand Model: {filters['title']} | Min Car Price: {filters['price'][0]} - Max Car Price: {filters['price'][1]} | Location: {filters['location']}")
    print(f'Searching {len(final_sort)} results out of {len(car_listings)}...\n')  # print number of listings

    if len(final_sort) == 0:
        time.sleep(1)
        print('There were no cars in your search. Try searching with different parameters.')
        time.sleep(1)
        return nextStep(car_listings, filters, final_sort)

    else:
        for i in range(len(final_sort)):
            print(f'Listing Number {i + 1}: \n{final_sort[i]["title"]}')
            print(f'Price: {final_sort[i]["price"]}\nLocation: {final_sort[i]["location"]}\n{final_sort[i]["link"]}\n')

    print(f'End of {len(final_sort)} results...\n')  # print number of listings

    return nextStep(car_listings, filters, final_sort)


def nextStep(car_listings, filters, final_sort):
    while True:
        user_next = input(f'\n\nGo Back to Search (back)\nEdit Filter (edit)\nSort Filter by (sort)\n'
                          f'Export Listing (export)\nHelp (help)\nQuit (quit)\n')
        if user_next == 'back':
            print('\n\n')
            return mainSearch(car_listings)
        elif user_next == 'edit':
            return editFilter(car_listings, filters)
        elif user_next == 'sort':
            return sortPrice(car_listings, filters, final_sort)
        elif user_next == 'export':
            exportListings(final_sort)
        elif user_next == 'help':
            explanations()

        elif user_next == 'quit':
            while True:
                user_input = input(f'Are you sure you want to quit? (y/n)')
                if user_input == 'y':
                    return print("Goodbye!")
                elif user_input == 'n':
                    break
                else:
                    print("Sorry, I didn't catch that. Try again.")


def sortPrice(car_listings, filters, final_sort):
    """Sorts the filtered listings by price in either ascending or descending order"""
    while True:
        sort = input(f'Filter car prices from low to high, or high to low. (asc or desc): ')
        if sort == 'asc':
            sorted_list_ascending = sorted(final_sort, key=lambda x: int(x['price'].replace('$', '').replace(',', '')))
            return showResults(filters, sorted_list_ascending, car_listings)

        elif sort == 'desc':
            # Sort by descending order
            sorted_list_descending = sorted(final_sort, key=lambda x: int(x['price'].replace('$', '').replace(',', '')),
                                            reverse=True)
            return showResults(filters, sorted_list_descending, car_listings)
        else:
            print("There seems to be an error. Please try again.")


def exportListings(final_sort):
    """Exports the filtered listings into an .xlsx file. openpyxl mut be installed"""
    export_name = input("Name your export file: ")
    try:
        df = pd.DataFrame(final_sort)
        df.to_excel(f"{export_name}.xlsx", index=False)
        print(f'Exported as {export_name} ')
    except PermissionError:
        print(f'Error: File {export_name} already exists.')


def explanations():
    print(
        f'(back): Takes you back to the starting search CLI.\n(edit): Lets you edit a filter.\n(sort): Sort the '
        f'listings by either ascending or descending price.\n(export): Export your listings into an .xlsx file ('
        f'excel)\n(quit): Quit the Program. ')
    return


grabListings()
