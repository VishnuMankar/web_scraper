import requests
from bs4 import BeautifulSoup
import pandas

oyo_url = "https://www.oyorooms.com/hotels-in-mumbai/?page="
page_num_Max = 5
scraped_info_list = []

for page_num in range(1,page_num_Max):

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    req = requests.get(oyo_url + str(page_num), headers = headers)
    content = req.content
    soup = BeautifulSoup(content, "html.parser")
    all_hotels = soup.find_all("div", {"class" : "hotelCardListing"})
    
    for hotel in all_hotels :
        hotel_dict = {}
        hotel_dict["name"] = hotel.find("h3", {"class" : "listingHotelDescription__hotelName"}).text
        hotel_dict["address"] = hotel.find("span", {"itemprop" : "streetAddress"}).text
        hotel_dict["price"] = hotel.find("span", {"class" : "listingPrice__finalPrice"}).text
        
        try:
            hotel_dict["rating"] = hotel.find("span", {"class" : "hotelRating__ratingSummary"}).text
        except AttributeError:
            hotel_dict["rating"] = None

        parent_amenities_element = hotel.find("div", {"class" : "amenityWrapper"})

        amenity_list = []
        try:
            for amenity in parent_amenities_element.find_all("div", {"class" : "amenityWrapper__amenity"}):
                amenity_list.append(amenity.find("span", {"class" : "d-body-sm"}).text.strip())
        except AttributeError:
            amenity_list.append(None)

        hotel_dict["amenity"] = ", ".join(amenity_list[:-1])

        scraped_info_list.append(hotel_dict)

dataFrame = pandas.DataFrame(scraped_info_list)
dataFrame.to_csv("Oyo.csv")