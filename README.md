# AI Real Estate Valuation (in progress)

## Introduction
The purpose of this project is to predict the current value of unlisted properties in the Toronto region based on a 30+ variable multilayer percepitron. The intention is then to visualize this on a web-application like a Python-Flask with react flask where you would be able to type in an address or postal code, and our pre-trained model would spit out a value.


## Data
The data for this project was retrieved using a Puppeteer webscrapper taking data primarily from zolo.com with over 14,000 properties in data pulled and which will be stored in a MySQL database. The geolocational data was then found by using a latlong.net where the Puppeteer scrapper simulates human behavior to the long, lat data.

### Variables
There were a variety of variables as mentioned taken into consideration for the MLP model:
* location
* type of property
* nearby amenities (i.e. nearest distance to schools, grocery stores etc.)
* Rankings of nearest schools

#### Location
This was a unique variable to take into consideration. Basically what was done here was each individual area code was given a new exponential function for how important close data points or properties are in affecting property value. I.e. in some area codes, houses slightly outside of the neighborhood affect the current property value.
All of these unique exponetial funcitons are calculated using a secondary model.




