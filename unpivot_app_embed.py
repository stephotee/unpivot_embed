import streamlit as st
import pandas as pd

def transform_data(input_df):
    # Unpivot the data
    melted_data = pd.melt(input_df, id_vars=["response_id"], 
                          value_vars=input_df.columns[1:],
                          var_name="Response Option",
                          value_name="Selected")
    
    # Convert to lowercase for case-insensitive matching
    melted_data['Selected'] = melted_data['Selected'].astype(str).str.lower()

    # Map the values
    value_mapping = {
        "yes": "Selected",
        "1": "Selected",
        "selected": "Selected",
        "true": "Selected",
        "no": "Not selected",
        "0": "Not selected",
        "not selected": "Not selected",
        "false": "Not selected",
        "": "Not selected",  # for blank strings
        "nan": "Not selected"  # for NaN values
    }
    
    melted_data['Selected'] = melted_data['Selected'].map(value_mapping).fillna("Not selected")
    
    return melted_data


st.title('Unpivot Multi-Select Survey Data')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    input_df = pd.read_csv(uploaded_file)
    transformed_data = transform_data(input_df)
    
    st.write("Transformed Data:")
    st.write(transformed_data)
    
    st.download_button(label="Download Transformed Data", data=transformed_data.to_csv(index=False), file_name='transformed_data.csv', mime='text/csv')
