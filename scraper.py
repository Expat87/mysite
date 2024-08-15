from bs4 import BeautifulSoup
import csv

def parse_html_table(file_path):
    # Read the HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the table
    table = soup.find('table', id='locations-table')
    
    # Prepare to store results
    data = []
    
    # Iterate over rows in the table body
    for row in table.find('tbody').find_all('tr'):
        # Extract cells
        cells = row.find_all('td')
        
        if len(cells) < 6:
            continue  # Skip rows that don't have enough cells
        
        # Extract the required information
        name = cells[2].get_text(strip=True)
        category = cells[3].get_text(strip=True)
        region = cells[4].get_text(strip=True)
        info = cells[5].get_text(strip=True)
        
        # Append to the data list as a dictionary
        data.append({
            'Name': name,
            'Category': category,
            'Region': region,
            'Info': info
        })
    
    return data


def tx_csv(data_list):
    # Open the CSV file in write mode
    with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the column headings
        writer.writerow(['Name', 'Category', 'Region', 'Info'])
        
        # Write the data rows
        for item in data_list:
            writer.writerow([item['Name'], item['Category'], item['Region'], item['Info']])

# Example usage
file_path = 'ZTotK_html.txt'
data = parse_html_table(file_path)


tx_csv(data)
# Print the extracted data
#for item in data:
#    print(item)
