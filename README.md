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
In main.py, the first code you will need to write is in [load_receipts_from_csv()](https://github.com/plight-chatham/accounting-receipts/blob/0dbe25569f06c69fe1ca5bfe3f4d61c2b1eb7f9b/main.py#L57).
  * If you scroll up, you'll see another function `load_projects_from_csv()`. The "load receipts" function will be very similar to "load projects."
  * However, you'll see that we're reading different columns of data out of the different csv files.
  * If you need to learn more about .csv files, you can read more on the [wikipedia page](https://en.wikipedia.org/wiki/Comma-separated_values).
  * Note that you'll be creating objects which are instances of the [receipt class](https://github.com/plight-chatham/accounting-receipts/blob/0dbe25569f06c69fe1ca5bfe3f4d61c2b1eb7f9b/receipt_classes.py#L57).
  * The `__init__` function for Receipt accepts 3 parameters: when the receipt was purchased, the [Vendor](https://github.com/plight-chatham/accounting-receipts/blob/0dbe25569f06c69fe1ca5bfe3f4d61c2b1eb7f9b/receipt_classes.py#L32) that it came from, and the amount on the receipt.
  * You will need to create a new `Vendor` object to make a `Receipt`.
  * Another problem you'll need to handle is that dates were formatted differently in projects.csv and receipts.csv. You can learn more about how to parse them by reading the [python documentation on datetime.strptime()](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior)

## Associating Receipts with Projects
Now that you have read in all the receipts to go along with the projects, it's time to start working on associating each receipt with a project.

1. Look at the code in `main()` which says "your code here". This is where you can add your processing of each receipt.
2. Consider using a loop to look at each receipt. Look at the loop in `print_summary_of_receipts` for an example.
3. Each receipt contains two important pieces of information:
   * The *date* of the transaction, which is called **when** in the `Receipt` class. Each project has a date range, defined by the *Contract date* and *Work Completion Date*. Workers would not be buying supplies for a project outside of these dates.
   * The *address* of the retailer where the supplies were purchased. Workers on the project are unlikely to travel all the way across the city, and would instead go to suppliers which are near the work site.
4. For each receipt, you'll want to consider each of the projects. Using the date and address information you have, do you think the project is a possible match? Do you think that it's likely?
5. Once your code makes a guess for each receipt, set the `receipt.client` field with the name of the project client.
6. Then, you'll want to write all of your results to a new .csv in the data folder. There is a function called [write_receipts](https://github.com/plight-chatham/accounting-receipts/blob/252b5ef2cc67de0430f8884acf8aba39d03f1237/data/receipt-generator.py#L204) in the script I used to generate the input file which does exactly this. You could consider copy/paste/modifying this code to work with the `Receipt` objects that you've loaded and updated.
7. Write your output to a file like `data/guesses.csv`
8. Compare it to [answer-key.csv](https://github.com/plight-chatham/accounting-receipts/blob/main/data/answer-key.csv) - how many of your guesses were correct?
9. If it wasn't very many, consider iterating on your logic in steps 3-4.

## Measuring Distances Between Two Addresses
In a "real world" project, we might consider using something like the [Google Maps python libraries](https://developers.google.com/maps/web-services/client-library) to measure distances between two addresses (such as vendor and project addresses.) However, getting this set up is more complicated than we need for this class. 

Therefore, I have provided a simple API (which stands for "Application Programming Interface") which will tell you the distance in km between any two addresses in our data set. You can call it as a function called `get_distance(address1, address2)` in [distance_api](https://github.com/plight-chatham/accounting-receipts/blob/main/distance_api.py). This is already available in your code with the variable name `dapi`. Look at the [test code](https://github.com/plight-chatham/accounting-receipts/blob/252b5ef2cc67de0430f8884acf8aba39d03f1237/distance_api.py#L48) to see how to use it.



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
