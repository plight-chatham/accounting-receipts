# Accounting Receipts Project
## Scenario
You are a project manager at a construction company in the Pittsburgh Area. 

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
