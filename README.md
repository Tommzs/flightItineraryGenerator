# Flight Itinerary Generator
Flight itinerary generator as entry task for KIWI Python Weekend 2019

# Description
You have data about flights (segments). Your task is to find all combinations of flights for passengers with no bags, one bag or two bags are able to travel, having 1 to 4 hours for each transfer between flights. The columns in table of input data are explained bellow:

- source, destination are the code of airport the flight is departing from and arriving to
- departure, arrival are times of departure and arrival
- price is the price of flight per person (without baggage)
- bags_allowed the number of bags passenger is allowed to take with them
- bag_price additional price per each bag passenger would like to take with them
- flight_number is the unique identifier of each flight

For easy navigation in offered flight combinations (itineraries), it would be nice to show total prices to passengers that already include the additional price for bags, given they input how many bags they wish to take when they search for flights.

# Output
- Output data should be in a format that is suitable for further processing
- Don't make passengers travel trough the same cities in same trip:
  - A->B->A->B is not a valid combination
  - A->B->A is a valid combination

# Usage
Input data will be fed into your program through stdin so it should be possible to run it in command line via a command such as cat input.csv | find_combinations.py. The output of your program will be printed to stdout and any errors will go to stderr.
