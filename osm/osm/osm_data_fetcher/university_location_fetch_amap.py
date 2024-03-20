import json
import requests


# Define the search query parameters
search_query = 'colleges in Beijing'
api_url = 'https://restapi.amap.com/v3/place/text?types=141201&region=北京市&key=f4e0a0d57c05463b57ad9a9c262d3949'

# Send a GET request to the Google Places API
response = requests.get(api_url)


# Check if the request was successful
if response.status_code == 200:
    output_file = "beijing_university.json"
    with open(output_file, 'w') as f: 
    # Parse the JSON response
        results = response.json()['pois']
        # Iterate over the results and print the names and locations of colleges
        for result in results:
            name = result['name']
            location = result['location']
            data = ({
                "name": name,
                "location": location
            })
            f.write(f"{json.dumps(data, ensure_ascii=False)},\n")        
    
else:
    print(f"Error: Unable to fetch data from Amaps API (Status Code: {response.status_code})")