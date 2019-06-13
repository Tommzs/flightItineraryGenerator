import sys
import argparse
from datetime import datetime
from typing import List, Any
import copy

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
        self.destination = None
        self.source = None
        self.price = None
        self.bags_allowed = None
        self.bag_price = None
        self.prices_with_bags = []


    def to_string(self):
        out_str = "{}, {}, {}, {}, {}, {}, {}, {}, {}".format(self.source,
                                                              self.destination,
                                                              str(self.departure),
                                                              str(self.arrival),
                                                              str(self.visitedAirports),
                                                              self.bags_allowed,
                                                              self.price,
                                                              self.bag_price,
                                                              self.prices_with_bags)
        return out_str


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
        self.bag_price = bag_price


### Public functions
def read_args():
    parser = argparse.ArgumentParser(description='Generate flight itineraries from input segments.')
    parser.add_argument('-i', '--input', required=False, help='input csv with flight segments', default=None)
    parser.add_argument('-o', '--output', required=False, help='output csv with generated itineraries', default=None)
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


def generate_pseudoitinerary(start_node, curr_node, parent_dict):
    pseudoitinerary = []
    while curr_node != start_node:
        pseudoitinerary.insert(0, curr_node)
        curr_node = parent_dict[curr_node]
    return pseudoitinerary


def itineraries_from_pseudoitinerary(flight_seg, pseudoitinerary):
    prev_itinerary = flightItinerary()
    prev_itinerary.visitedAirports.append(flight_seg.source)
    prev_itinerary.visitedAirports.append(flight_seg.destination)
    prev_itinerary.arrival = flight_seg.arrival
    prev_itinerary.departure = flight_seg.departure
    prev_itinerary.source = flight_seg.source
    prev_itinerary.destination = flight_seg.destination
    prev_itinerary.price = flight_seg.price
    prev_itinerary.bag_price = flight_seg.bag_price
    prev_itinerary.bags_allowed = flight_seg.bags_allowed
    prev_itinerary.prices_with_bags = [prev_itinerary.price+(num_bags*prev_itinerary.bag_price) for num_bags in range(0, prev_itinerary.bags_allowed+1)]

    itineraries = [prev_itinerary]
    for node in pseudoitinerary:
        new_itinerary = copy.deepcopy(prev_itinerary)
        new_itinerary.visitedAirports.append(node.destination)
        new_itinerary.arrival = node.arrival
        new_itinerary.destination = node.destination
        new_itinerary.price += node.price
        new_itinerary.bag_price += node.bag_price
        new_itinerary.bags_allowed = min(prev_itinerary.bags_allowed, node.bags_allowed)
        new_itinerary.prices_with_bags = [new_itinerary.price+(num_bags*new_itinerary.bag_price) for num_bags in range(0, new_itinerary.bags_allowed+1)]
        itineraries.append(new_itinerary)
        prev_itinerary = new_itinerary
    itineraries.pop(0)

    return itineraries


def generate_itineraries(flight_seg, flight_graph):
    dsf_stack = [flight_seg]
    visited_airports = [flight_seg.source]
    parent_dict = {}
    itineraries = []
    while len(dsf_stack) > 0:
        curr_node = dsf_stack.pop()
        visited_airports.append(curr_node.destination)
        explorable = list(filter(lambda node: node.destination not in visited_airports, flight_graph[curr_node]))
        if len(explorable) > 0:
            for child_node in explorable:
                dsf_stack.append(child_node)
                parent_dict[child_node] = curr_node
        else:
            pseudoitinerary = generate_pseudoitinerary(flight_seg, curr_node, parent_dict)
            if len(pseudoitinerary) > 0:
                itineraries += itineraries_from_pseudoitinerary(flight_seg, pseudoitinerary)
    return itineraries


if __name__ == "__main__":
    # Read args, allows input file as parameter
    in_file_path, out_file_path = read_args()
    # Parse input data
    flight_segs = read_input_data(in_file_path)
    flight_graph = generate_graph(flight_segs)
    itineraries = []
    for flight_seg in flight_segs:
        itineraries += generate_itineraries(flight_seg, flight_graph)

    header = "source, destination, departure, arrival, visited_airports, " \
             "bags_allowed, price, bag_price, prices_with_bags"

    if out_file_path is None:
        print(header)
        for itinerary in itineraries:
            print(itinerary.to_string())
    else:
        with open(out_file_path, "w") as out_csv_file:
            out_csv_file.write(header+"\n")
            out_csv_file.writelines([itinerary.to_string()+"\n" for itinerary in itineraries])
