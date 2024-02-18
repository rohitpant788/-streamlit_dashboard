import streamlit as st

import api

st.sidebar.title('Options')
option = st.sidebar.selectbox(
    'Which Dashboard',
    ('twitter', 'wallstreetbets', 'stocktwits','charts','pattern')
)

st.header(option)

if option == 'twitter':
    st.subheader('twitter dashboard logic.')
elif option == 'wallstreetbets':
    st.subheader('wallstreetbets dashboard logic.')
elif option == 'stocktwits':
    symbol = st.sidebar.text_input("Symbol",value='TCNSBRANDS.NSE', max_chars=20)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    url = f'https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json'
    data, error = api.get_data_from_api(url,headers=headers)

    if error:
        st.write(error)
    else:
        #st.write(data)
        for message in data['messages']:
            st.image(message['user']['avatar_url'])
            st.write(message['user']['username'])
            st.write(message['created_at'])
            st.write(message['body'])

elif option == 'charts':
    st.subheader('charts dashboard logic.')
elif option == 'pattern':
    st.subheader('pattern dashboard logic.')
else:
    st.write('You selected Option doesnot exists')
