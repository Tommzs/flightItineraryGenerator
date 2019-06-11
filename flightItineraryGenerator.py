import sys
import argparse
from datetime import datetime
from typing import List, Any

### Constants
HOUR_IN_SECONDS = 1*60*60


### Class definitions
class flightItinerary:
    """ flightItinerary represents one flight itinerary"""
    def __init__(self):
        """ Create a new point at the origin """
        self.visitedAirports = []
        self.departure = None
        self.arrival = None
        self.price = None
        self.bags_allowed = None
        self.bag_price = None

    def get_price_with_bags(self, num_bags):
        if self.bags_allowed is None:
            print("ERROR: Bags allowed is not filled", file=sys.stderr)
            return None
        elif self.bag_price is None:
            print("ERROR: Bags price is not filled", file=sys.stderr)
            return None
        elif self.price is None:
            print("ERROR: Price is not filled", file=sys.stderr)
            return None
        elif num_bags > self.bags_allowed:
            print("ERROR: Maximum bags allowed is {} which is less than {}".format(self.bags_allowed, num_bags), file=sys.stderr)
            return None
        else:
            return self.price+num_bags*self.bag_price

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


### Public functions
def read_args():
    parser = argparse.ArgumentParser(description='Generate flight itineraries from input segments.')
    parser.add_argument('-i', '--input', required=False, help='input csv with flight segments', default='None')
    parser.add_argument('-o', '--output', required=False, help='output csv with generated itineraries', default='stdout')
    args = vars(parser.parse_args())
    return args['input'], args['output']


def str_to_datetime(time_str):
    date_str, time_str = time_str.split('T')
    year_str, month_str, day_str = date_str.split('-')
    hour_str, minute_str, second_str = time_str.split(':')
    return datetime(year=int(year_str),
                    month=int(month_str),
                    day=int(day_str),
                    hour=int(hour_str),
                    minute=int(minute_str),
                    second=int(second_str))


def process_line(line, header):
    line = line.rstrip('\n').split(',')
    dep_time_str = line[header.index('departure')]
    arr_time_str = line[header.index('arrival')]
    fl_segm = flightSegment(source=line[header.index('source')],
                           destination=line[header.index('destination')],
                           departure=str_to_datetime(dep_time_str),
                           arrival=str_to_datetime(arr_time_str),
                           price=float(line[header.index('price')]),
                           bags_allowed=int(line[header.index('bags_allowed')]),
                           bag_price=float(line[header.index('bag_price')]))
    return fl_segm


def read_input_data(file_path=None):
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

    return flight_segments


def generate_graph(segments: List[flightSegment]):
    directed_graph = dict()
    for key_flight in segments:
        directed_graph[key_flight] = set()
        for next_flight in segments:
            if key_flight.destination == next_flight.source:
                time_diff = (next_flight.departure-key_flight.arrival).seconds
                if HOUR_IN_SECONDS < time_diff < (4*HOUR_IN_SECONDS):
                    directed_graph[key_flight].add(next_flight)
    return directed_graph


def generate_itineraries(flight_segs, flight_graph):
    #TODO: Do DFS with parent map generating set of itineraries once there is nowhere to explore
    None


if __name__ == "__main__":
    # Read args, allows input file as parameter
    in_file_path, out_file_path = read_args()
    # Parse input data
    flight_segs = read_input_data(in_file_path)
    flight_graph = generate_graph(flight_segs)
    itineraries = []
    for flight_seg in flight_segs:
        generate_itineraries(flight_seg, flight_graph)