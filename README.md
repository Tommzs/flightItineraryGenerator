# Flight Itinerary Generator
Flight itinerary generator as entry task for KIWI Python Weekend 2019

# Description
You have data about flights (segments). This script finds all combinations of flights having 1 to 4 hours for each transfer between flights. Output can be filtered out to see only flights which allows to travel with any number of bags (only 1,2 in example data).

The columns in table of input data are explained bellow:
- source, destination are the code of airport the flight is departing from and arriving to
- departure, arrival are times of departure and arrival
- price is the price of flight per person (without baggage)
- bags_allowed the number of bags passenger is allowed to take with them
- bag_price additional price per each bag passenger would like to take with them
- flight_number is the unique identifier of each flight


# Output
- CSV table with headers
- source, destination, departure, arrival
- visited airports, number of allowed bags
- price, bag price and list of prices with bags, where index corresponds to the number of bags

# Usage
Input data can be fed through stdin so it si possible to run it in command line via a command such as cat input.csv | find_combinations.py. 
It is also possible to give path to input file using parameter -i/--input.

The output is printed to stdout or to csv file if given -o/--output parameter
