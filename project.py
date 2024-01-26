from bs4 import BeautifulSoup
import requests
import csv
import re
import sys


def main():
    # Get legitimate postcode
    postcode = input("Postcode: ")
    check_postcode(postcode)

    # Initalize dataset and page no.
    data = []
    n = 1

    # Parse every page of listings and store in data
    while True:
        url = f"https://www.domain.com.au/rent/?postcode={postcode}&page={n}"
        if is_valid_page(url):
            print(f"Scraping: {url}")
            data = parse_page(url, data)
            if not next_page(url, n):
                break
            n += 1

    # Output the csv file
    filename = input("Output Filename (exclud. extension): ")
    with open(f"{filename}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def check_postcode(postcode):
    if re.search(r"^\d{4}$", postcode):
        return postcode
    sys.exit("Error: Non 4-digit postcode")


def next_page(url, current_page):
    fake_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=fake_headers).text
    soup = BeautifulSoup(response, "lxml")  # Using lxml parser to replace "html.parser"
    pages = soup.findAll("a", {"data-testid": "paginator-page-button"})
    for page in pages:
        if int(page.text) > current_page:
            return True
    return False


def is_valid_page(url):
    # Check if page exists
    fake_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=fake_headers)
    if response.status_code == 200:
        return True
    return False


def parse_page(url, data):
    fake_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=fake_headers).text

    # Using lxml parser instead of html for fast parsing
    soup = BeautifulSoup(response, "lxml")

    listings = soup.find("ul", {"data-testid": "results"}, class_="css-8tedj6")
    try:
        properties = listings.findAll("li", class_="css-1qp9106")
    except AttributeError:
        sys.exit("Invalid postcode")

    # Store property data in an array of dictionaries, each dict represent a property
    for property in properties:
        # Initialize dictionary for parsing
        row = {}

        # 1.1 Get rental price and address lines
        price = property.find("p", {"data-testid": "listing-card-price"}).text
        if address_line_1 := property.find("span", {"data-testid": "address-line1"}):
            address_line_1 = address_line_1.text
        else:
            address_line_1 = "N/A"
        if address_line_2 := property.find("span", {"data-testid": "address-line2"}):
            address_line_2 = address_line_2.text
        else:
            address_line_1 = "N/A"

        # 1.2 Clean up and store data
        price = price.lower().strip()
        price = price.replace(" pw", "")
        price = price.replace(" per week", "")
        row["Price/week"] = price
        row["Address1"] = address_line_1.strip()
        row["Address2"] = address_line_2.strip()

        # 2.1 Get property features
        features = property.findAll(
            "span", {"data-testid": "property-features-text-container"}
        )

        # 2.2 Clean up and store data
        for feature in features:
            if "Bed" in feature.text:
                beds = feature.text.strip(" Bed")
                beds = beds.strip(" Beds")
                try:
                    int(beds)
                    row["Bedrooms"] = beds
                except ValueError:
                    row["Bedrooms"] = 0
            elif "Bath" in feature.text:
                bath = feature.text.strip(" Bath")
                bath = feature.text.strip(" Baths")
                try:
                    int(bath)
                    row["Bathrooms"] = bath
                except ValueError:
                    row["Bathrooms"] = 0
            elif "Parking" in feature.text:
                parkings = feature.text.strip(" Parking")
                parkings = parkings.strip(" Parkings")
                try:
                    int(parkings)
                    row["Parkings"] = parkings
                except ValueError:
                    row["Parkings"] = 0

        # 3.1 Get property url, id and category (e.g. apartment / house)
        property_url = property.find("a")["href"]
        category = property.find(class_="css-693528").text
        id = property.attrs["data-testid"]

        # 3.2 Store data
        row["Url"] = property_url
        row["Category"] = category
        row["property_id"] = id.strip("listing-")

        # 4.1 Check and record if the property is newly advertised or updated
        if label := property.find(class_="css-1b64g3l"):
            label = label.text
        else:
            label = "N/A"
        row["Label"] = label

        # 5.1 Check and record if the property has inspection
        if inspection := property.find("span", class_="css-hwihpw"):
            date, time = inspection.text.split(",")
        else:
            date = "N/A"
            time = "N/A"
        row["Inspection Date"] = date
        row["Inspection Time"] = time.strip()

        # 6. Sort the row with keys in alphabetical order (optional)
        # row = dict(sorted(row.items()))
        data.append(row)

    return data


if __name__ == "__main__":
    main()
