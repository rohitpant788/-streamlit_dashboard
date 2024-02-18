import streamlit as st
import api
import csv
import os

st.sidebar.title('Options')
option = st.sidebar.selectbox(
    'Which Dashboard',
    ('stocktwits', 'twitter', 'wallstreetbets', 'charts', 'pattern')
)

st.header(option)

# Function to read symbols from CSV file
def read_symbols_from_csv(filename='options.csv'):
    symbols = []
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            symbols = [row[0] for row in reader]
    return symbols

# Function to write symbols to CSV file
def write_symbols_to_csv(symbols, filename='options.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for symbol in symbols:
            writer.writerow([symbol])

# Function to remove symbol from CSV file
def remove_symbol_from_csv(symbol, filename='options.csv'):
    symbols = read_symbols_from_csv(filename)
    if symbol in symbols:
        symbols.remove(symbol)
        write_symbols_to_csv(symbols, filename)

if option == 'stocktwits':
    symbol_input = st.sidebar.text_input("Enter a Symbol", value='TCNSBRANDS.NSE', max_chars=20)

    # Read symbols from CSV file
    symbol_options = read_symbols_from_csv()

    # If symbol_input is not in symbol_options, add it if it's a valid symbol
    if symbol_input and symbol_input not in symbol_options:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        url = f'https://api.stocktwits.com/api/2/streams/symbol/{symbol_input}.json'
        data, error = api.get_data_from_api(url, headers=headers)

        if data:
            symbol_options.append(symbol_input)
            # Write the symbol to CSV file
            write_symbols_to_csv(symbol_options)
        elif error:
            st.write(error)

    # Display select box with symbol_options
    selected_symbols = st.sidebar.multiselect("Select Symbol(s) to Display", symbol_options)

    # Display delete button next to each symbol
    for symbol in selected_symbols:
        if st.sidebar.button(f"Delete {symbol}"):
            remove_symbol_from_csv(symbol)
            selected_symbols.remove(symbol)

    # Fetch data for selected symbols
    for selected_symbol in selected_symbols:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        url = f'https://api.stocktwits.com/api/2/streams/symbol/{selected_symbol}.json'
        data, error = api.get_data_from_api(url, headers=headers)

        if error:
            st.write(error)
        elif data:
            for message in data['messages']:
                st.image(message['user']['avatar_url'])
                st.write(f"{message['user']['name']} (Followers: {message['user']['followers']})")
                st.write(message['created_at'])
                st.write(message['body'])

elif option == 'twitter':
    st.subheader('twitter dashboard logic.')
elif option == 'wallstreetbets':
    st.subheader('wallstreetbets dashboard logic.')
elif option == 'charts':
    st.subheader('charts dashboard logic.')
elif option == 'pattern':
    st.subheader('pattern dashboard logic.')
else:
    st.write('You selected Option does not exist')
