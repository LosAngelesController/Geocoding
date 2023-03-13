import csv
import googlemaps
from tqdm import tqdm

# Set your Google Cloud API key
GOOGLE_MAPS_API_KEY = 'API_KEY'

# Define the number of subsets
num_subsets = 100

# Process each subset
for i in range(num_subsets):
    # Construct the file paths for the input and output CSV files
    input_file_path = f'2018.csv'
    output_file_path = f'2018_geocodes_addresses_{i+1}.csv'

    # Initialize the Google Maps client
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

    with open(input_file_path, newline='') as infile:
        reader = csv.DictReader(infile)
        header = reader.fieldnames

        # Add new fields to header for Latitude and Longitude
        header.extend(['Latitude', 'Longitude'])

        # Open the output file for  writing
        with open(output_file_path, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=header)
            writer.writeheader()

            # Add tqdm progress bar to loop
            for row in tqdm(reader):
                address = row['Full Address']
                
                #  the Google Cloud Places API to geocode the address
                try:
                    geocode_result = gmaps.geocode(address)[0]
                    location = geocode_result['geometry']['location']
                    row['Latitude'] = location['lat']
                    row['Longitude'] = location['lng']
                    writer.writerow(row)
                except IndexError:
                    print(f'Failed to geocode address "{address}"')
