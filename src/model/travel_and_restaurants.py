from math import radians, sin, cos, sqrt, atan2

import pandas as pd

data = pd.read_csv("./src/data/airbnbs.csv")  # airbnb_data
data_2 = pd.read_csv("./src/data/restaurants.csv")  # restaurant_data
data_3 = pd.read_csv("./src/data/food_orders.csv")  # food_data


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * \
        cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c  # Distance in kilometers
    return distance


def define_name(name):
    for idx, listing_name in enumerate(data["name"].values()):
        if str(listing_name).lower() == str(name).lower():
            return data["host_name"][idx]
    return "Host name not found"


def define_nights(name):
    for idx, listing_name in enumerate(data["name"].values()):
        if listing_name.lower() == name.lower():
            return data["minimum_nights"][idx]
    return "Min nights not found"


def define_price(name):
    for idx, listing_name in enumerate(data["name"].values()):
        if listing_name.lower() == name.lower():
            return data["price"][idx]
    return "Price not found"


def define_nr_reviews(name):
    for idx, listing_name in enumerate(data["name"].values()):
        if listing_name.lower() == name.lower():
            return data["number_of_reviews"][idx]
    return "Number of reviews not found"


def define_neighbourhood_group(name):
    for idx, listing_name in enumerate(data["name"].values()):
        if str(listing_name).lower() == str(name).lower():
            return data["neighbourhood_group"][idx]
    return "Neighbourhood group not found"


def define_name_by_neighbourhood_group(neighbourhood_group):
    list_data = []
    for idx, listing_name in enumerate(data["neighbourhood_group"].values()):
        if listing_name.lower() == neighbourhood_group.lower():
            list_data.append(data["name"][idx])
    return list_data  # Return the populated list


def define_name_by_price(price):
    name_data = []
    for idx, listing_price in enumerate(data["price"].values()):
        if listing_price == price:
            name_data.append(data["name"][idx])
    return name_data  # Return the populated list

    return "Listing names not found"


def define_listings_by_frequency(nr, data):
    reviews = data['number_of_reviews']
    names = data['name']
    sorted_reviews = dict(
        sorted(reviews.items(), key=lambda item: item[1], reverse=True))

    top_entries = {}
    for key, value in list(sorted_reviews.items())[:nr]:
        if key in names:
            top_entries[names[key]] = value

    if top_entries:
        return list(top_entries.keys())
    else:
        return "Listing names not found"


def define_airbnb_by_latitude_longitude(latitude, longitude, max_distance=4.0):
    closeby_airbnbs = []

    for idx in range(len(data)):
        listing_latitude = data["latitude"][idx]
        listing_longitude = data["longitude"][idx]
        listing_name = data["name"][idx]

        # Calculate the distance between the given coordinates and the Airbnb listing
        distance = haversine(latitude, longitude,
                             listing_latitude, listing_longitude)

        # If the distance is within the specified maximum distance, add the listing to the result
        if distance <= max_distance:
            closeby_airbnbs.append({
                "name": listing_name,
                "distance": distance
            })

    if closeby_airbnbs:
        return closeby_airbnbs
    else:
        return "No closeby Airbnb listings found"


def define_name_by_lower_price(price):
    name_data = []
    for idx, listing_price in enumerate(data["price"].values()):
        if listing_price <= price:
            name_data.append(data["name"][idx])
    return name_data

    return "Listing names not found"


def define_name_by_price_and_neighbourhood_group(price, neighbourhood_group):
    name_data = []
    for idx, listing_neighbourhood in enumerate(data["neighbourhood_group"].values()):
        if listing_neighbourhood.lower() <= neighbourhood_group.lower():
            for idx, listing_price in enumerate(data["price"].values()):
                if listing_price <= price:
                    name_data.append(data["name"][idx])
    return name_data

    return "Listing names not found"


def define_name_by_price_min_nights_and_neighbourhood_group(price, min_nights, neighbourhood_group):
    name_data = []

    for idx, listing_name in enumerate(data["name"]):
        listing_neighbourhood = data["neighbourhood_group"][idx].lower()
        listing_price = data["price"][idx]
        minimum_nights = data["minimum_nights"][idx]

        if (
            listing_neighbourhood <= neighbourhood_group.lower()
            and listing_price <= price
            and minimum_nights <= min_nights
        ):
            name_data.append(data["name"][idx])

    return name_data


def define_name_by_neighbourhood_group_room_type_and_date(neighbourhood_group, room_type, last_review_date):
    name_data = []

    for idx, listing_name in enumerate(data["name"]):
        listing_neighbourhood = data["neighbourhood_group"][idx].lower()
        listing_room_type = data["room_type"][idx]
        listing_last_review_date = data["last_review"][idx]

        if (
            listing_neighbourhood.lower() <= neighbourhood_group.lower()
            and listing_room_type.lower() <= room_type.lower()
            and listing_last_review_date == last_review_date
        ):
            name_data.append(data["name"][idx])

    return name_data


def define_name_by_price_range_and_neighbourhood_group(min_price, max_price, neighbourhood_group):
    name_data = []

    for idx, listing_name in enumerate(data["name"]):
        listing_neighbourhood = data["neighbourhood_group"][idx].lower()
        listing_price = data["price"][idx]

        if (
            listing_neighbourhood.lower() == neighbourhood_group.lower()
            and listing_price <= max_price
            and listing_price >= min_price
        ):
            name_data.append(data["name"][idx])

    return name_data


def define_popularity_by_neighbourhood_group_room_type(popularity, neighbourhood_group, room_type, data):
    filtered_listings = []

    for idx in range(len(data['name'])):
        listing_neighbourhood = data["neighbourhood_group"][idx].lower()
        listing_room_type = data["room_type"][idx].lower()
        num_reviews = data["number_of_reviews"][idx]
        listing_name = data["name"][idx]

        if (
            listing_neighbourhood.lower() == neighbourhood_group.lower()
            and listing_room_type.lower() == room_type.lower()
        ):
            filtered_listings.append((listing_name, num_reviews))

    # Sort the filtered listings by the number of reviews in descending order
    sorted_listings = sorted(
        filtered_listings, key=lambda x: x[1], reverse=True)

    # Get the top 'popularity' number of listings based on reviews
    top_entries = {}
    for name, reviews in sorted_listings[:popularity]:
        top_entries[name] = reviews

    if top_entries:
        return list(top_entries.keys())
    else:
        return "No listings found"


def get_min_cost_by_neighbourhood_group_room_type_min_nights(nr_requests, neighbourhood_group, room_type, min_nights, data):
    selected_listings = []

    for idx in range(len(data['name'])):
        listing_neighbourhood = data["neighbourhood_group"][idx].lower()
        listing_room_type = data["room_type"][idx].lower()
        listing_minimum_nights = data["minimum_nights"][idx]
        listing_price = data["price"][idx]
        listing_name = data["name"][idx]

        if (
            listing_neighbourhood.lower() == neighbourhood_group.lower()
            and listing_room_type.lower() == room_type.lower()
            and listing_minimum_nights <= min_nights
        ):
            selected_listings.append(
                (listing_name, listing_price, listing_minimum_nights))

    # Filter the selected listings based on the specified minimum nights
    filtered_listings = []
    for name, price, nights in selected_listings:
        if nights <= min_nights:
            filtered_listings.append((name, price))

    # Sort the filtered listings by price
    sorted_listings = sorted(filtered_listings, key=lambda x: x[1])

    if sorted_listings:
        return [name for name, _ in sorted_listings[:nr_requests]]
    else:
        return "No listings found"


def define_average_price_by_neighbourhood_group_room_type(neighbourhood_group, room_type, data):
    total_price = 0
    count = 0

    for idx in range(len(data['name'])):
        listing_neighbourhood = data["neighbourhood_group"][idx].lower()
        listing_room_type = data["room_type"][idx].lower()
        listing_price = data["price"][idx]

        if (
            listing_neighbourhood.lower() == neighbourhood_group.lower()
            and listing_room_type.lower() == room_type.lower()
        ):
            total_price += listing_price
            count += 1

    if count > 0:
        return total_price / count
    else:
        return "No listings found"


def define_name_by_room_type(room_type):
    list_data = []
    for idx, listing_name in enumerate(data["room_type"].values()):
        if listing_name.lower() == room_type.lower():
            list_data.append(data["name"][idx])
    return list_data


def define_name_by_date_review(last_review_date):
    list_data = []
    for idx, listing_name in enumerate(data["last_review"].values()):
        if listing_name == last_review_date:
            list_data.append(data["name"][idx])
    return list_data


def define_name_by_min_nights(minimum_nights):
    list_data = []
    for idx, listing_name in enumerate(data["minimum_nights"].values()):
        if listing_name == minimum_nights:
            list_data.append(data["name"][idx])
    return list_data


def define_restaurants_by_cuisine(cuisine):
    restaurant_data = []
    for idx, restaurant in enumerate(data_2["cuisine"].values()):
        restaurant_str = str(restaurant)
        if restaurant_str.lower() == cuisine.lower():
            restaurant_data.append(data_2["DBA"][idx])
    return restaurant_data

    return "Restaurants not found"


def define_borough(restaurant):
    for idx, borough in enumerate(data_2["DBA"].values()):
        if borough.lower() == restaurant.lower():
            return data_2["BORO"][idx]
    return "Borough not found"


def define_cuisine(restaurant):
    for idx, cuisine in enumerate(data_2["DBA"].values()):
        if cuisine.lower() == restaurant.lower():
            return data_3["cuisine"][idx]
    return "Cuisine not found"


def define_phone_by_name_neighbourhood_cuisine(restaurant, neighbourhood_group, cuisine):
    name_data = []

    for idx, listing_name in enumerate(data_2["DBA"]):
        listing_restaurant = data_2["DBA"][idx].lower()
        listing_neighbourhood_group = data_2["BORO"][idx]
        listing_cuisine = data_2["cuisine"][idx]

        if (
            listing_neighbourhood_group.lower() == neighbourhood_group.lower()
            and listing_restaurant.lower() == restaurant.lower()
            and listing_cuisine.lower() == cuisine.lower()
        ):
            name_data.append(data_2["PHONE"][idx])

    return name_data


def define_restaurant_by_cuisine_borough(cuisine, borough):
    name_data = []

    for idx, listing_name in enumerate(data_2["DBA"]):
        listing_borough = data_2["BORO"][idx]
        listing_cuisine = str(data_2["cuisine"][idx])

        if (
            listing_cuisine.lower() == cuisine.lower()
            and listing_borough.lower() == borough.lower()
        ):
            name_data.append(data_2["DBA"][idx])

    return name_data


def define_restaurant_by_zipcode_cuisine_borough_phone(zip_code, cuisine, borough, phone):
    name_data = []

    for idx, listing_name in enumerate(data_2["DBA"]):
        listing_zipcode = data_2["ZIPCODE"][idx]
        listing_borough = data_2["BORO"][idx]
        listing_cuisine = data_2["cuisine"][idx]
        listing_phone = data_2["PHONE"][idx]

        if (
            listing_zipcode == zip_code
            and listing_borough.lower() == borough.lower()
            and listing_cuisine.lower() == cuisine.lower()
            and listing_phone == phone
        ):
            name_data.append(data_2["DBA"][idx])

    return name_data


def define_restaurant_lat_long_by_zipcode_cuisine_borough_phone(zip_code, cuisine, borough, phone):
    name_data = []

    for idx, listing_name in enumerate(data_2["DBA"]):
        listing_zipcode = data_2["ZIPCODE"][idx]
        listing_borough = data_2["BORO"][idx]
        listing_cuisine = data_2["cuisine"][idx]
        listing_phone = data_2["PHONE"][idx]
        latitude = data_2["Latitude"][idx]
        longitude = data_2["Longitude"][idx]

        if (
            listing_zipcode == zip_code
            and listing_borough.lower() == borough.lower()
            and listing_cuisine.lower() == cuisine.lower()
            and listing_phone == phone
        ):
            data = {
                "latitude": f"{float(latitude)}",
                "longitude": f"{float(longitude)}"
            }
            name_data.append(data)

    return name_data


def define_info_by_restaurant_cuisine_borough_phone(restaurant, cuisine, borough, phone):
    name_data = []

    for idx, listing_name in enumerate(data_2["DBA"]):
        listing_restaurant = data_2["DBA"][idx]
        listing_borough = data_2["BORO"][idx]
        listing_cuisine = data_2["cuisine"][idx]
        listing_phone = data_2["PHONE"][idx]

        if (
            listing_restaurant.lower() == restaurant.lower()
            and listing_borough.lower() == borough.lower()
            and listing_cuisine.lower() == cuisine.lower()
            and listing_phone == phone
        ):
            data = f"{data_2['STREET'][idx]} {data_2['BUILDING'][idx]} {int(data_2['ZIPCODE'][idx])}"
            name_data.append(data)

    return name_data


def define_lat_long_by_restaurant_street(restaurant, street):
    prox_data = []

    for idx, listing_name in enumerate(data_2["DBA"]):
        listing_restaurant = data_2["DBA"][idx]
        listing_street = data_2["STREET"][idx]
        listing_lat = data_2["Latitude"][idx]
        listing_long = data_2["Longitude"][idx]

        if (
            listing_restaurant.lower() == restaurant.lower()
            and listing_street.lower() == street.lower()
        ):
            data = {
                "latitude": f"{float(listing_lat)}",
                "longitude": f"{float(listing_long)}"
            }
            prox_data.append(data)

    return prox_data


def define_lat_long_by_listing(listing):
    prox_data = []

    for idx, listing_airbnb in enumerate(data["name"].values()):
        listing_airbnb = str(data["name"][idx])
        listing_lat = data["latitude"][idx]
        listing_long = data["longitude"][idx]

        if (
            str(listing_airbnb.lower()) == str(listing.lower())
        ):
            data1 = {
                "latitude": f"{float(listing_lat)}",
                "longitude": f"{float(listing_long)}"
            }
            prox_data.append(data1)

    return prox_data


def define_closest_airbnb_address(latitude, longitude):
    closest_airbnb = None
    min_distance = float('inf')  # Initialize with positive infinity

    for idx in range(len(data_2)):
        listing_latitude = data_2["Latitude"][idx]
        listing_longitude = data_2["Longitude"][idx]
        listing_address = data_2["STREET"][idx]

        # Calculate the distance between the given coordinates and the Airbnb listing
        distance = haversine(latitude, longitude,
                             listing_latitude, listing_longitude)

        # If the distance is less than the current minimum distance, update the closest Airbnb
        if distance < min_distance:
            min_distance = distance
            closest_airbnb = {
                "listing_address": listing_address,
                "distance": distance
            }

    if closest_airbnb:
        return closest_airbnb
    else:
        return "No nearby Airbnb found"


def define_closest_restaurant_by_airbnb(latitude, longitude, max_distance=5.0):
    closest_restaurants = []
    min_distance = float('inf')  # Initialize with positive infinity

    for idx in range(len(data_2)):
        listing_latitude = data_2["Latitude"][idx]
        listing_longitude = data_2["Longitude"][idx]
        restaurant_name = data_2["DBA"][idx]

        # Calculate the distance between the given coordinates and the restaurant listing
        distance = haversine(latitude, longitude,
                             listing_latitude, listing_longitude)

        # If the distance is within the specified maximum distance, add the restaurant to the result
        if distance <= max_distance:
            closest_restaurants.append({
                "restaurant_name": restaurant_name,
                "distance": distance
            })

    if closest_restaurants:
        return closest_restaurants
    else:
        return "No nearby restaurant found"


def define_restaurant_info_zipcode_street_building(latitude, longitude, max_distance=5.0):
    closest_restaurants = []
    min_distance = float('inf')  # Initialize with positive infinity

    for idx in range(len(data_2)):
        listing_latitude = data_2["Latitude"][idx]
        listing_longitude = data_2["Longitude"][idx]
        restaurant_name = data_2["DBA"][idx]
        restaurant_street = data_2["STREET"][idx]
        restaurant_zip = data_2["ZIPCODE"][idx]
        restaurant_phone = data_2["PHONE"][idx]
        restaurant_building = data_2["BUILDING"][idx]

        # Calculate the distance between the given coordinates and the restaurant listing
        distance = haversine(latitude, longitude,
                             listing_latitude, listing_longitude)

        # If the distance is within the specified maximum distance, add the restaurant to the result
        if distance <= max_distance:
            closest_restaurants.append({
                "restaurant_name": restaurant_name,
                "restaurant_street": restaurant_street,
                "restaurant_zip": restaurant_zip,
                "restaurant_phone": restaurant_phone,
                "restaurant_building": restaurant_building,
                "distance": distance
            })

    if closest_restaurants:
        return closest_restaurants
    else:
        return "restaurant info not found"


def define_cuisine_restaurant_airbnb_closeness(latitude, longitude, max_distance=5.0):
    closest_restaurants = []
    min_distance = float('inf')  # Initialize with positive infinity

    for idx in range(len(data_2)):
        listing_latitude = data_2["Latitude"][idx]
        listing_longitude = data_2["Longitude"][idx]
        restaurant_name = data_2["DBA"][idx]
        restaurant_cuisine = data_2["cuisine"][idx]

        # Calculate the distance between the given coordinates and the restaurant listing
        distance = haversine(latitude, longitude,
                             listing_latitude, listing_longitude)

        # If the distance is within the specified maximum distance, add the restaurant to the result
        if distance <= max_distance:
            closest_restaurants.append({
                "restaurant_name": restaurant_name,
                "restaurant_cuisine": restaurant_cuisine,
                "distance": distance
            })

    if closest_restaurants:
        return closest_restaurants
    else:
        return "restaurant info not found"


def define_cuisine_rating(cuisine: str):
    prox_data = []

    for idx, cuisine_type in enumerate(data_3["cuisine_type"].values()):
        cuisine_type = str(data_3["cuisine_type"][idx])
        rating = data_3["rating"][idx]

        if (
            str(cuisine_type.lower()) == str(cuisine.lower())
        ):
            data1 = {
                "cuisine_type": f"{str(cuisine_type)}",
                "rating": f"{str(rating)}"
            }
            prox_data.append(data1)

    return prox_data


def define_restaurants_by_rating(rating):
    prox_data = []

    for idx, restaurant_rating in enumerate(data_3["rating"].values()):
        restaurant_name = str(data_3["restaurant_name"][idx])
        restaurant_rating = data_3["rating"][idx]

        if (
            restaurant_rating == rating
        ):
            data1 = {
                "restaurant_name": f"{str(restaurant_name)}",
            }
            prox_data.append(data1)

    return prox_data


def define_neigh_by_rest(restaurant, neighborhood):
    prox_data = []

    for idx, restaurant_name in enumerate(data_2["DBA"].values()):
        restaurant_name = str(data_2["DBA"][idx])
        neighborhood_group = str(data_2["BORO"][idx])

        if (
            str(restaurant_name.lower()) == str(restaurant.lower()) and
            str(neighborhood_group.lower()) == str(neighborhood.lower())
        ):
            data1 = {
                "restaurant": f"{str(restaurant_name)}",
                "neighborhood_group": f"{str(neighborhood_group)}",
            }
            prox_data.append(data1)

    return prox_data


def define_airbnbs_with_max_reviews(popularity, neighbourhood_group, room_type, data):
    filtered_listings = []

    for idx in range(len(data['name'])):
        listing_neighbourhood = data["neighbourhood_group"][idx].lower()
        listing_room_type = data["room_type"][idx].lower()
        num_reviews = data["number_of_reviews"][idx]
        listing_name = data["name"][idx]
        latitude = data["latitude"][idx]
        longitude = data["longitude"][idx]

        if (
            listing_neighbourhood.lower() == neighbourhood_group.lower()
            and listing_room_type.lower() == room_type.lower()
        ):
            filtered_listings.append({
                "name": listing_name,
                "latitude": latitude,
                "longitude": longitude,
                "num_reviews": num_reviews
            })

    # Sort the filtered listings by the number of reviews in descending order
    sorted_listings = sorted(
        filtered_listings, key=lambda x: x["num_reviews"], reverse=True)

    # Get the top 'popularity' number of listings based on reviews
    top_entries = sorted_listings[:popularity]

    if top_entries:
        return top_entries
    else:
        return "No listings found"


def define_rating_by_restaurant_name(restaurant_name):
    name_data = []

    for idx, restaurant_name in enumerate(data_3["restaurant_name"]):
        restaurant_rating = data_3["rating"][idx]
        restaurant_name = data_3["restaurant_name"][idx]

        if (
            str(restaurant_name).lower() == str(restaurant_name).lower()
        ):
            name_data.append(data_3["rating"][idx])

    return name_data


def define_avg_costs_by_restaurant_name(restaurant_name, data_3):
    total_price = 0
    count = 0

    for idx in range(len(data_3['restaurant_name'])):
        cost = data_3["cost_of_the_order"][idx]
        restaurant = data_3["restaurant_name"][idx]

        if (
            restaurant.lower() == restaurant_name.lower()
        ):
            total_price += cost
            count += 1

    if count > 0:
        return total_price / count
    else:
        return "No restaurants found"


def define_avg_delivery_time_by_restaurant_name(restaurant_name, data_3):
    total_price = 0
    count = 0

    for idx in range(len(data_3['restaurant_name'])):
        delivery_time = data_3["delivery_time"][idx]
        restaurant = data_3["restaurant_name"][idx]

        if (
            restaurant.lower() == restaurant_name.lower()
        ):
            total_price += delivery_time
            count += 1

    if count > 0:
        return total_price / count
    else:
        return "No restaurants found"


def define_avg_prep_time_by_restaurant_name(restaurant_name, data_3):
    total_price = 0
    count = 0

    for idx in range(len(data_3['restaurant_name'])):
        prep_time = data_3["food_preparation_time"][idx]
        restaurant = data_3["restaurant_name"][idx]

        if (
            restaurant.lower() == restaurant_name.lower()
        ):
            total_price += prep_time
            count += 1

    if count > 0:
        return total_price / count
    else:
        return "No restaurants found"


class TravelAndRestaurantFunctions():
    functions = set((define_airbnb_by_latitude_longitude,
                    define_airbnbs_with_max_reviews,
                    define_average_price_by_neighbourhood_group_room_type,
                    define_avg_costs_by_restaurant_name,
                    define_avg_delivery_time_by_restaurant_name,
                    define_avg_prep_time_by_restaurant_name,
                    define_borough,
                    define_closest_airbnb_address,
                    define_closest_restaurant_by_airbnb,
                    define_cuisine,
                    define_cuisine_rating,
                    define_cuisine_restaurant_airbnb_closeness,
                    define_info_by_restaurant_cuisine_borough_phone,
                    define_lat_long_by_listing,
                    define_lat_long_by_restaurant_street,
                    define_listings_by_frequency,
                    define_name,
                    define_name_by_date_review,
                    define_name_by_lower_price,
                    define_name_by_min_nights,
                    define_name_by_neighbourhood_group,
                    define_name_by_neighbourhood_group_room_type_and_date,
                    define_name_by_price,
                    define_name_by_price_and_neighbourhood_group,
                    define_name_by_price_min_nights_and_neighbourhood_group,
                    define_name_by_price_range_and_neighbourhood_group,
                    define_name_by_room_type,
                    define_neigh_by_rest,
                    define_neighbourhood_group,
                    define_nights,
                    define_nr_reviews,
                    define_phone_by_name_neighbourhood_cuisine,
                    define_popularity_by_neighbourhood_group_room_type,
                    define_price,
                    define_rating_by_restaurant_name,
                    define_restaurant_by_cuisine_borough,
                    define_restaurant_by_zipcode_cuisine_borough_phone,
                    define_restaurant_info_zipcode_street_building,
                    define_restaurant_lat_long_by_zipcode_cuisine_borough_phone,
                    define_restaurants_by_cuisine,
                    define_restaurants_by_rating,
                    get_min_cost_by_neighbourhood_group_room_type_min_nights,
                    haversine))
