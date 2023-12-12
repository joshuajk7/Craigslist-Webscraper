# This microservice suggests filters for the Craiglist Web scraper Project
import random
import time
import zmq
import json

filter_dictionary = {}  # this will be the filter dictionary that will return the results


def suggest_distance():
    """
    suggests a search distance to apply in the cars+trucks filter
    :return: nothing
    """
    filter_dictionary["distance"] = random.randint(1, 500)


def suggest_location():
    """
    suggests a city to search for the vehicles in
    :return:
    """
    cities_dict = {
        "New York City": "10001",
        "Los Angeles": "90001",
        "Chicago": "60601",
        "Houston": "77001",
        "Phoenix": "85001",
        "Philadelphia": "19101",
        "San Antonio": "78201",
        "San Diego": "92101",
        "Dallas": "75201",
        "San Jose": "95101",
        "Austin": "73301",
        "Jacksonville": "32201",
        "San Francisco": "94101",
        "Indianapolis": "46201",
        "Columbus": "43201",
        "Fort Worth": "76101",
        "Charlotte": "28201",
        "Seattle": "98101",
        "Denver": "80201",
        "Washington, D.C.": "20001",
        "Boston": "02101",
        "El Paso": "79901",
        "Nashville": "37201",
        "Detroit": "48201",
        "Oklahoma City": "73101",
        "Portland": "97201",
        "Las Vegas": "89101",
        "Memphis": "38101",
        "Louisville": "40201",
        "Baltimore": "21201"
    }
    city = random.choice(list(cities_dict.keys()))
    zipcode = cities_dict[city]
    filter_dictionary["city"] = city
    filter_dictionary["zipcode"] = zipcode


def suggest_price():
    """
    suggests a price range to apply in the cars+trucks filter
    :return: nothing
    """
    filter_dictionary["min-price"] = random.randint(1, 10000)
    filter_dictionary["max-price"] = random.randint(10000, 50000)
    return


def suggest_make_and_model():
    """
    suggests a make and model to apply in the cars+trucks filter
    :return: nothing
    """
    make_model_dict = {
        "Toyota": ["Camry", "Corolla", "Rav4", "Highlander", "Prius"],
        "Volkswagen": ["Golf", "Passat", "Tiguan", "Jetta"],
        "Ford": ["F-150", "Escape", "Explorer", "Mustang", "Focus"],
        # "Chevrolet": ["Silverado", "Equinox", "Malibu", "Traverse", "Camaro"],
        "Honda": ["Accord", "Civic", "CR-V", "Pilot", "Odyssey"],
        "Nissan": ["Altima", "Maxima", "Rogue", "Pathfinder", "Titan", "Leaf", "Xterra"],
        "BMW": ["3 Series", "5 Series", "X3", "X5", "7 Series"],
        # "Mercedes-Benz": ["C-Class", "E-Class", "GLC", "GLE", "S-Class"],
        "Tesla": ["Model 3", "Model S", "Model X", "Model Y", "Cybertruck"],
        # "Hyundai": ["Elantra", "Tucson", "Santa Fe", "Kona", "Palisade"]
    }
    make = random.choice(list(make_model_dict.keys()))
    model = random.choice(make_model_dict[make])
    filter_dictionary["make"] = make
    filter_dictionary["model"] = model


def suggest_odometer():
    """
    suggests a odometer mileage to apply in the cars+trucks filter
    :return: nothing
    """
    filter_dictionary["min-odometer"] = random.randint(1, 100000)
    filter_dictionary["max-odometer"] = random.randint(10001, 300000)


def suggest_year():
    """
    suggests a model year to apply in the cars+trucks filter
    :return: nothing
    """
    filter_dictionary["min-year"] = random.randint(1950, 1990)
    filter_dictionary["max-year"] = random.randint(1990, 2023)


def suggest_transmission():
    """
    suggests a transission type to apply in the cars+trucks filter
    :return: nothing
    """
    transmission_list = ["manual", "automatic"]
    filter_dictionary["transmission"] = random.choice(transmission_list)


def suggest_drive():
    """
    suggests a drive type to apply in the cars+trucks filter
    :return: nothing
    """
    drive_list = ["fwd", "rwd", "4wd"]
    filter_dictionary["drive"] = random.choice(drive_list)


def suggest_condition():
    """
    suggests a vehicle condition to apply in the cars+trucks filter
    :return: nothing
    """
    condition_list = ["new", "like new", "excellent", "good", "fair", "salvage"]
    filter_dictionary["condition"] = random.choice(condition_list)


def suggest_color():
    """
    suggests a vehicle color to apply in the cars+trucks filter
    :return: nothing
    """
    colors_list = ["black", "blue", "brown", "green", "grey", "orange", "purple", "red", "silver", "white", "yellow"]
    filter_dictionary["color"] = random.choice(colors_list)


def suggest_title():
    """
    suggests a title status to apply in the cars+trucks filter
    :return: nothing
    """
    title_list = ["clean", "salvage", "rebuilt", "parts only", "lien", "missing"]
    filter_dictionary["title"] = random.choice(title_list)


def build_filter():
    """
    builds the filter dictionary
    """
    suggest_distance()
    suggest_location()
    suggest_price()
    suggest_make_and_model()
    suggest_odometer()
    suggest_year()
    suggest_transmission()
    suggest_drive()
    suggest_condition()
    suggest_color()
    suggest_title()


# execute the microservice
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5556")
print("The filter-suggestor microservice is online")
while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request for %s" % message)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    build_filter()
    filter_json_data = json.dumps(filter_dictionary)
    socket.send_string(filter_json_data)
    print("Suggested filters have been sent")
