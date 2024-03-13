from Resources.graph_search import bfs, dfs
from Resources.vc_metro import vc_metro
from Resources.vc_landmarks import vc_landmarks
from Resources.landmark_choices import landmark_choices

####################
landmark_string = ""
for letter, landmark in landmark_choices.items():
  landmark_string += "{0} - {1}\n".format(letter, landmark)

# For further use
stations_under_construction = []
####################
def greet():
  print("\n\nHi there and welcome to SkyRoute!")
  print("\n\nWe'll help you find the shortest route between the following Vancouver landmarks:\n\n" + landmark_string)



# Main function
def skyroute():
  greet()
  new_route()
  goodbye()


# It will update graph of metro stations (vc_metro.py) according to (stations_under_construction)
def get_active_stations():
  updated_metro = vc_metro
  for station_under_construction in stations_under_construction:
    for current_station, neighboring_stations in vc_metro.items():
      if current_station != station_under_construction:
        updated_metro[current_station] -= set(stations_under_construction)
      else:
        updated_metro[current_station] = set([])
  return updated_metro

# This will handle setting the selected origin and destination points
def set_start_and_end(start_point, end_point):
  if start_point is not None:
    # If it does, we already have an origin and destination, but the user wants to make a change
    change_point = input("What would you like to change? You can enter 'o' for 'origin', 'd' for 'destination', or 'b' for 'both': ")

    if change_point == "b":
      start_point = get_start()
      end_point = get_end()
    elif change_point == "o":
      start_point = get_start()
    elif change_point == "d":
      end_point = get_end()
    else:
      print("Oops, that isn't 'o', 'd', or 'b'...")
      set_start_and_end(start_point, end_point)

  else:
    start_point = get_start()
    end_point = get_end()
  return start_point, end_point



# It will be used to request an origin from the user
def get_start():
  start_point_letter = input("Where are you coming from? Type in the corresponding letter: ")
  if start_point_letter in landmark_choices.keys():
    start_point = landmark_choices[start_point_letter]
    return start_point
  else:
    print("Sorry, that's not a landmark we have data on. Let's try this again...")
    get_start()



# It will be used to request a destination from the user
def get_end():
  end_point_letter = input("Ok, where are you headed? Type in the corresponding letter: ")
  if end_point_letter in landmark_choices.keys():
    end_point = landmark_choices[end_point_letter]
    return end_point
  else:
    print("Sorry, that's not a landmark we have data on. Let's try this again...")
    get_end()


# Takes the shortest route and prints it in friendly form
def new_route(start_point=None, end_point=None):
  start_point, end_point = set_start_and_end(start_point, end_point)
  shortest_route = get_route(start_point, end_point)
  
  if shortest_route:
    shortest_route_string = "\n".join(shortest_route)
    print("\n\nThe shortest metro route from {0} to {1} is:\n{2}".format(start_point, end_point,  shortest_route_string))
  else:
    print("\n\nUnfortunately, there is currently no path between {0} and {1} due to maintenance.".format(start_point, end_point))

  again = input("\n\nWould you like to see another route? Enter y/n: ")
  if again == "y":
    show_landmarks()
    new_route(start_point, end_point)


# Option for refreshing the landmarks to choose from
def show_landmarks():
  see_landmarks = input("\n\nWould you like to see the list of landmarks again? Enter y/n: ")
  if see_landmarks == "y":
    print(landmark_string)


# Calculates shortest route between metro stations located nearby chosen landmarks
def get_route(start_point, end_point):
  start_stations = vc_landmarks[start_point]
  end_stations = vc_landmarks[end_point]
  routes = []
  for start_station in start_stations:
    for end_station in end_stations:
      metro_system = get_active_stations() if stations_under_construction else vc_metro
      if stations_under_construction:
        possible_route = dfs(metro_system, start_station, end_station)
        if not possible_route:
          continue
      route = bfs(metro_system, start_station, end_station)
      if route:
        routes.append(route)
  if routes:
    shortest_route = min(routes, key=len)
    return shortest_route

def goodbye():
  print("\n\nThanks for using SkyRoute!")


skyroute()
