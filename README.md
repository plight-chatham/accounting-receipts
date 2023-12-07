# Accounting Receipts Project
## Scenario
You are a project manager at a construction company in the Pittsburgh Area. In 2022, your company worked on 5 [projects](https://github.com/plight-chatham/accounting-receipts/blob/f2152a86a58f2008982e26cdec5022053c994126/data/projects.csv#L1) in the region. (The names listed on those projects are made up, but the addresses are real.)

In the process of working on those projects, your crews needed to occasionally run out to get tools and supplies such as lumber. When they did, they drove to a hardware store near the job site and purchased what they needed. They dutifully saved and turned in their receipts using your company's accounting system.

Now it is tax time and you need to figure out the costs spent on each project. Unfortunately, your accounting system does not have any association between receipt and project, or the team members who entered the data didn't see the field, or the software lost it, or whatever. You are left with 500 receipts, and you need a way to come up with a reasonable guess about which project they are associated with.

## Getting Started
1. Download this repository as a .zip file (see the "<> Code" button above.)
2. Extract the .zip to a folder (preferably not your downloads folder, but it's your choice.)
3. You may run this code with any tool you like. I recommend [PyCharm](https://jetbrains.com/pycharm/download/)
4. Take a look at [main.py](https://github.com/plight-chatham/accounting-receipts/blob/main/main.py), [distance_api.py](https://github.com/plight-chatham/accounting-receipts/blob/main/distance_api.py). You can see what happens when you run either of them.
5. Look at [projects.csv](https://github.com/plight-chatham/accounting-receipts/blob/main/data/projects.csv) and [receipts.csv](https://github.com/plight-chatham/accounting-receipts/blob/main/data/receipts.csv). These contain the input data you will work with. Note the column names in those files.

## Reading in Receipts
1. In main.py, the first code you will need to write is in [load_receipts_from_csv()](https://github.com/plight-chatham/accounting-receipts/blob/0dbe25569f06c69fe1ca5bfe3f4d61c2b1eb7f9b/main.py#L57).
  * If you scroll up, you'll see another function `load_projects_from_csv()`. The "load receipts" function will be very similar to "load projects."
  * However, you'll see that we're reading different columns of data out of the different csv files.
  * If you need to learn more about .csv files, you can read more on the [wikipedia page](https://en.wikipedia.org/wiki/Comma-separated_values).
  * Note that you'll be creating objects which are instances of the [receipt class](https://github.com/plight-chatham/accounting-receipts/blob/0dbe25569f06c69fe1ca5bfe3f4d61c2b1eb7f9b/receipt_classes.py#L57).
  * The `__init__` function for Receipt accepts 3 parameters: when the receipt was purchased, the [Vendor](https://github.com/plight-chatham/accounting-receipts/blob/0dbe25569f06c69fe1ca5bfe3f4d61c2b1eb7f9b/receipt_classes.py#L32) that it came from, and the amount on the receipt.
  * You will need to create a new `Vendor` object to make a `Receipt`.



# About the Development of this Project (students can ignore this part)
A project for python students to use scripting to reconstitute missing data


This tool uses the Google Maps API.

I created a project using the Google Cloud Console:
https://console.cloud.google.com/google/maps-apis/

This required inputting my credit card, which I did, but plan to stay well under the $200/month credit.

I then enabled the Places API:
https://developers.google.com/maps/documentation#places

And I created an API Key. This documentation should describe the process, although I didn't actually use it:
https://console.cloud.google.com/welcome/new?walkthrough_id=maps--maps_enable_api&project=receipt-generator-399911

I downloaded the API key and saved it next to my script as apikey.txt

This is where I learned to make calls to the API.
https://github.com/googlemaps/google-maps-services-python/blob/master/tests/test_places.py

The script uses two calls to the API (so far):
gmaps.geocode (to figure out where the imaginary construction work site is)
gmaps.places_nearby (to find the hardware stores near this location.)

When looking at the location results which are returned from the API, it is handy to look at the sample-location.json file for reference. 
(the file is a python object, not JSON... sorry for the misleading name. The file's contents are spiritually closer to JSON than python.)
