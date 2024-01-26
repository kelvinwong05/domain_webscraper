# Domain.com Web Scraping

#### Video Demo:  <URL HERE>

#### Description:

Hello! My name is Kelvin Wong, a student who has a passion for the CS50 series and computer science. I am excited to share with you my final project for CS50P, Introduction to Programming with Python – my second CS50 course.

In this project, I primarily utilized the popular web scraping library called "Beautiful Soup." This lightweight tool, in my opinion, is more approachable than Scrapy. I used it to parse properties listed on Domain.com, a major real estate website in Australia. In CS50x (Introduction to Computer Science), I gained foundational web programming knowledge. With the understanding of how Python empowers data processing, I was able to develop and present this project.


## Installation

To install the dependencies of the project, run this in your text editor:

```bash
pip install -r requirements.txt
```

## Usage/Examples

To run the program, follow these steps:

* Open a terminal or command prompt.
* Navigate to the directory where the script is located.


```bash
python project.py
```

* Follow the prompts to enter the required information when prompted.

Example:

    Postcode: 2000
    Output Filename (exclud. extension): results


This will output a "results.csv" file containing data for all properties listed within the area with the postcode 2000.

The data fields include price per week, address, no. of bedrooms and bathrooms, parking slots, property type, url to view the property and more.
## Code Structure

### 1. `parse_page(url, data)`

The main function of the program is `parse_page(url, data)`, which takes a list-type `data` and `url` as inputs. It retrieves the HTML file of the webpage and extracts information of interest using BeautifulSoup. The function includes logic checks for non-existent pages or missing information.

The extracted data is then cleansed using simple Python string methods and Regular Expressions. If the extracted data is `None`, it is caught by exceptions or value checks, and "N/A" is returned.

After data cleansing, the data is stored as key-value pairs in a dictionary with respect to one property. Each property is appended to the data, and the updated data list is returned.

### 2. `next_page(url, current_page)`

This boolean function looks for pagination elements within the HTML document of `url` and supports parsing multiple pages. The function checks if there is any pagination number that exceeds the `current_page` number, implying that the next page exists. If all pagination elements are exhausted and the numbers are all smaller than `current_page`, the function returns `False`.

### 3. `check_postcode(postcode)`

This function validates the user-inputted postcode and exits the program with a warning message if it is not a 4-digit code. It prevents the program from proceeding to page parsing, which could trigger request issues. Further functionalities can be added to this program, such as validating from an exhaustive list of postcodes.

### 4. `is_valid_page(url)`

This function serves as a defensive mechanism to filter out unsupported URLs that might raise unhandled errors. It ensures that the provided URL is valid and can be used for subsequent page parsing.




## Running Tests

A pytest file has been created for run logic checks of functions inside the main Python file.

To run tests, run the following command

```bash
  pytest test_project.py
```


## Roadmap

- Additional support for sale properties

- Add more information for property profile, such as transaction history


## 🛠 Skills

This project demonstrates proficiency in the following technologies and skills:

- **Python:** Utilized for scripting, data cleansing, and CSV writing.
- **Web Scraping:** Leveraged Beautiful Soup and requests for web scraping tasks.
- **Basic Understanding of HTML DOM:** Used to navigate and extract information from HTML documents.
- **Dependency Management:** Managed project dependencies using a `requirements.txt` file.


## Author

- [@kelvinwong05](https://www.github.com/kelvinwong05)


## License

[MIT](https://choosealicense.com/licenses/mit/)


