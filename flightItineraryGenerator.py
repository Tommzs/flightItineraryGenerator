import sys
import argparse

### Class definitions
from typing import List, Any


class flightItinerary:
    """ flightItinerary represents one flight itinerary"""
    def __init__(self):
        """ Create a new point at the origin """
        self.visitedAirports = []
        self.departure = None
        self.arrival = None
        self.prices = None
        self.bags_allowed = None
        self.bags_prices = None

class flightSegment:
    """ flightSegment represents one flight segment"""
    def __init__(self, source, destination, departure, arrival, price, bags_allowed, bag_price):
        """ Create a new point at the origin """
        self.source = source
        self.destination = destination
        self.departure = departure
        self.arrival = arrival
        self.price = price
        self.bags_allowed = bags_allowed
        self.bags_price = bag_price


### public functions
def read_args():
    parser = argparse.ArgumentParser(description='Generate flight itineraries from input segments.')
    parser.add_argument('-i', '--input', required=False, help='input csv with flight segments', default='None')
    parser.add_argument('-o', '--output', required=False, help='output csv with generated itineraries', default='stdout')
    args = vars(parser.parse_args())
    return args['input'], args['output']


def process_line(line, header):
    line = line.rstrip('\n').split(',')
    # TODO: Parse departure and arrival to extract date and time
    fl_segm = flightSegment(line[header.index('source')],
                           line[header.index('destination')],
                           line[header.index('departure')],
                           line[header.index('arrival')],
                           float(line[header.index('price')]),
                           int(line[header.index('bags_allowed')]),
                           float(line[header.index('bag_price')]))
    return fl_segm


def read_input_data(file_path=None):
    header: List[str] = []
    flight_segments: List[flightSegment] = []

    if file_path is None:
        header = (sys.stdin.readline()).rstrip('\n').split(',')
        for line in iter(sys.stdin.readline, ''):
            flight_segments.append(process_line(line, header))
    else:
        with open(file_path) as in_file:
            header = next(in_file).rstrip('\n').split(',')
            for line in in_file:
                flight_segments.append(process_line(line, header))

    return flight_segments, header


if __name__ == "__main__":
    # Read args, allows input file as parameter
    in_file_path, out_file_path = read_args()
    # Parse input data
    flight_segments, header = read_input_data(in_file_path)
