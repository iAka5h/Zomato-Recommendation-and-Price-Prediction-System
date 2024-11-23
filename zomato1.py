import base64
import numpy as np
import pandas as pd
import pickle
import streamlit as st
import pickle


#------------------------------------------------------------------------------------------

class Zomato:
    def __init__(self, mod_df, dec_df, dec_df1):
        self.mod_df=mod_df
        self.dec_df=dec_df
        self.dec_df1=dec_df1
        self.mappings={} #Initialize an empty dictionary for store mappings

    # Encoding with saved mappings
    def encode(self, cols):
        mappings = {} 
        for col in cols:
            self.dec_df[col], unique = self.dec_df[col].factorize()  # Factorize to encode each column
            self.mappings[col] = unique  # Store the mapping of original values to encoded integers
        return self.dec_df, self.mappings


    def prediction(self):
        #Creating dictionary for mapping string to integer
        rat_text_dict={'Not rated':0, 'Poor':1, 'Average':2, 'Good':3, 'Very Good':4, 'Excellent':5} 
        rat_color_dict={'5BA829':0, '3F7E00':1, 'FF7800':2, '9ACD32':3, 'CDD614':4, 'FFBA00':5,
        'CBCBC8':6, 'DE1D0F':7}
        rat_col_dict={'Apple Green':0,'Dark Olive Green':1,'Vivid Orange':2,'Yellow':3,'Olive Green':4,'Amber':5,
                    'Light Gray':6,'Red':7}
        table_dict={'No':0, 'Yes':1}
        country_dict={'India':0,'UAE':1,'Singapore':2,'Sri Lanka':3,'Tureky':4,'UK':5,'Qatar':6,'Philippines':7,'South Afria':8,
                'Brazil':9,'New Zealand':10,'Indonesia':11,'Canada':12,'USA':13,'Australia':14}
        
        #---------------------------------------------------------------------------------------------------
        #Options
        rat_text_option=['Not rated','Poor','Average','Good','Very Good','Excellent']
        rat_color_option=['Apple Green','Dark Olive Green','Vivid Orange','Yellow','Olive Green','Amber',
                    'Light Gray','Red']
        table_option=['No','Yes']
        country_option=['India','UAE','Singapore','Sri Lanka','Tureky','UK','Qatar','Philippines','South Afria',
                'Brazil','New Zealand','Indonesia','Canada','USA','Australia']
        
        #To get unique city from encoding
        unique_cities=self.mappings['City']
        unique_cuisines=self.mappings['Cuisines']

        country=st.selectbox('**Country**',options=country_option)
        filtered_country=self.dec_df1[self.dec_df1['Country']==country]

        unique_cities1=filtered_country['City'].unique()
        unique_cuisines1=filtered_country['Cuisines'].unique()

        #----------------------------------------------------------------------------------------

        #Sidebards
        price=st.sidebar.selectbox('**Price Range**',[i for i in range(1, 5)]) 
        rat_text=st.sidebar.selectbox('**Rating Text**',options=rat_text_option) 
        rat_color=st.sidebar.selectbox('**Color**', options=rat_color_option)
        votes=st.sidebar.number_input('**Votes**',min_value=0,max_value=10000)
        agg_rating=st.sidebar.number_input('**Rating out of 5**',min_value=0.0, max_value=5.0, format='%.1f') 
        table=st.sidebar.selectbox('**Table Booking**',options=table_option) #com

        col1,col2=st.columns(2)
        with col1:
            selected_city = st.selectbox('**City**', options=unique_cities1)
            # Get the encoded value for the selected city
            encoded_city_value = unique_cities.get_loc(selected_city)

        with col2:
            selected_cuisine = st.selectbox('**Cuisine**', options=unique_cuisines1)
            # Get the encoded value for the selected cuisine
            encoded_cuisine_value = unique_cuisines.get_loc(selected_cuisine)

        f=[country,encoded_city_value,price,rat_text,rat_color,encoded_cuisine_value,votes,agg_rating,table]
        if None not in f and st.button('**Predict**'):
            features1=[country_dict[country],encoded_city_value,price,rat_text_dict[rat_text],rat_col_dict[rat_color],
                      encoded_cuisine_value,votes,agg_rating,table_dict[table]]
            features=[price,rat_text_dict[rat_text],rat_col_dict[rat_color],np.sqrt(votes),np.sqrt(agg_rating),encoded_cuisine_value,
                      table_dict[table],encoded_city_value,country_dict[country]]
            Model=pickle.load(open('H:/zomato project final/Model1.pkl','rb'))
            pred=Model.predict([features])[0]
            pred=np.square(pred)
            st.subheader(f'Average Cost for two People : Rs.{pred:.2f}/-')

        st.caption(body='All Price in INR')     

#-----------------------------------------------------------------------------------------------


#Main Program

mod_df=pd.read_csv('Model1.csv')
dec_df=pd.read_csv('new_decoded_df.csv')
dec_df1=pd.read_csv('new_decoded_df.csv')

if __name__ == '__main__':
    # CSS to set background image for the header
    st.markdown(
        """
        <style>
        .header {
            background-image: url('https://img.freepik.com/premium-photo/colorful-various-herbs-spices-cooking-dark-background-copy-space-mock-up-banner-high-quality-photo_370312-404.jpg');
            background-size: cover;
            padding: 60px;
            text-align: center;
            color: white;
            font-size: 35px;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Adding the header text with background image
    st.markdown('<div class="header">MACHINE LEARNING</div>', unsafe_allow_html=True)

    st.title("Zomato ML Model to Predict the Average cost")
    st.sidebar.title('MACHINE LEARNING')

    zom=Zomato(mod_df, dec_df, dec_df1)
    cols_to_encode=['Cuisines','City']
    zom.encode(cols_to_encode)
    zom.prediction()

    # Custom CSS to add sidebar background image
    sidebar_bg = """
    <style>
    [data-testid="stSidebar"] {
        background: url("https://github.com/andfanilo/social-media-tutorials/blob/master/20220817-streamlit_css_background/image.jpg?raw=true") no-repeat center center fixed;
        background-size: cover;
    }
    [data-testid="stSidebar"]::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
    }
    </style>
    """

    # Apply the custom CSS to the sidebar
    st.markdown(sidebar_bg, unsafe_allow_html=True)

    def load_image(image_file):
        with open(image_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()

    # Load your local image file
    image_file = "home-banner3.jpg"  # Replace with your image filename
    image_data = load_image(image_file) 

    # Load custom CSS to set the background image
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpg;base64,{image_data});
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            height: 100vh;
        }}
        </style> 
        """,
        unsafe_allow_html=True
    )