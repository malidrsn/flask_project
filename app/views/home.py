import logging
import requests
from flask import Flask, render_template, request, Blueprint
from shapely.geometry import Polygon, Point
from math import sqrt, cos
from lxml import etree
from ..const import mkad_points, developer_key

bp = Blueprint("home", __name__, template_folder="../templates")


@bp.route("/")
def index():
    """Main page for app.

        this function returns the main page

        Returns: template as html page
            str: [html page as str]
        """

    return render_template("index.html")


@bp.route("/calc", methods=["POST", "GET"])
def Calculate() -> str:
    """Calculate the distance.

    this function makes request as POST and based on incoming values
    and it return to the pages with parameters they have own

    Returns: template as html page
        str: html page as str
    """

    if request.method == "POST":
        address = request.form['address']
        output = make_a_request(address)
        logging.basicConfig(filename='log.log', level=logging.INFO)
        logging.info('Entered address --->' + address)
        logging.info('Received answer' + output)
        return render_template('result.html', output=output)
    return render_template('main.html')


def make_a_request(address: str) -> str:
    """Make request as HTTP.

    this function takes address which entered by user from HTTP request
    return just a message to get user know, Also function uses Point and Polygon from
    Shapely.geometry to search point to show message inside MKAD or not

    Args:
        address (str): this parameter is used to get the address coordinates to make a request

    Returns:
        str: return messages as response between address parameters and MKAD point
    """

    try:
        coordinates = get_coordinates(create_parameters(address))
        mkad_polygon = Polygon(tuple(mkad_points))
        if mkad_polygon.contains(Point(coordinates)):
            message = 'The Address that you entered is in MKAD-area'
        else:
            min_distance = count_minimum_distance(coordinates)
            message = 'The Address that you entered is ' + str(round(min_distance, 3)) + \
                      'km away from MKAD'
    except Exception:
        message = "Something Gone Wrong, Try Again"
    return message


def count_minimum_distance(coordinates: tuple) -> float:
    """Minimum distance calculation.

    this function takes coordinates as parameter and longitude and latitude as a tuple
    and than counting the minimum distance between MKAD and the point which given as kilometers

    Args:
        coordinates (tuple): this parameter is used to get coordinates to calculate distance

    Returns:
        float: Return minimum distance calculation for address.
        Between 2 points given as parameters and MKAD points
    """

    min_distance = 0
    for longitude, latitude in mkad_points:
        average_latitude = (latitude + coordinates[1]) / 2
        distance = sqrt(((longitude - coordinates[0]) ** 2) *
                        (111.32137777 ** 2) * cos(average_latitude) +
                        ((latitude - coordinates[1]) ** 2) *
                        (111.134861111 ** 2))
        if distance < min_distance or min_distance == 0:
            min_distance = distance
    return min_distance


def get_coordinates(parameters: dict) -> tuple:
    """Get coordinates for an address

    this function takes the parameters and having request to geocoder to
    coordinates and return the coordinates for address

    Args:
        parameters (dict): parameters of the given address

    Returns:
        tuple: returns the coordinates of the given address
    """

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 ('
                      'KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'accept': '*/*'}
    r = requests.get('https://geocode-maps.yandex.ru/1.x/', headers=headers,
                     params=parameters)
    root = etree.fromstring(bytes(r.text, encoding='utf-8'))
    longitude, latitude = tuple(root[0][1][0][4][0].text.split(' '))
    coordinates = (float(longitude), float(latitude))
    return coordinates


def create_parameters(address: str) -> dict:
    """Create parameters for address.

    this function create parameters for having request from geocoder
    and than return dictionary of parameters

    Args:
        address (str): the address for create parameters

    Returns:
        dict: takes the api key and Geocode from an other class and returns the dictionary
    """

    address_to_string = address.replace(" ", "+")
    params = {'apikey': developer_key,
              'geocode': address_to_string}
    return params
