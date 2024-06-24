import pandas as pd

def read_urls_excel(filename, sheet_name='Sheet1', column_name='URL'):
    """Read URLs from an Excel file and return a list."""
    df = pd.read_excel(filename, sheet_name=sheet_name)
    return df[column_name].dropna().tolist()

def read_scraped_data_excel(filename, sheet_name='First Sheet', url_column='URL', data_column='Data'):
    """Read scraped data from an Excel file and return a dictionary with URLs as keys."""
    df = pd.read_excel(filename, sheet_name=sheet_name)
    return df.set_index(url_column)[data_column].to_dict()

def match_and_order_data(urls, scraped_data):
    """Match and order scraped data according to the list of URLs."""
    ordered_data = []
    for url in urls:
        if url in scraped_data:
            ordered_data.append(scraped_data[url])
        else:
            ordered_data.append('No data scraped')  # Placeholder for missing data
    return ordered_data

def write_ordered_data_excel(filename, ordered_data, sheet_name='Sheet1', column_name='Data'):
    """Write the ordered data to an Excel file."""
    df = pd.DataFrame({column_name: ordered_data})
    df.to_excel(filename, index=False, sheet_name=sheet_name)

def main():
    urls = read_urls_excel('urls.xlsx')  # Input file with URLs
    scraped_data = read_scraped_data_excel('descriptions.xlsx')  # Input file with scraped data
    ordered_data = match_and_order_data(urls, scraped_data)
    write_ordered_data_excel('ordered_data.xlsx', ordered_data)  # Output file with ordered data
    print("Scraped data has been reordered and saved to 'ordered_data.xlsx'.")

if __name__ == '__main__':
    main()
