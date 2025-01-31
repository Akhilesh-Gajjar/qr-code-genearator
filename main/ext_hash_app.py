import streamlit as st
import requests

BASE_API_URL = "http://127.0.0.1:8000"

def fetch_directory():
    response = requests.get(f"{BASE_API_URL}/directory")
    return response.json()

def add_value(new_value):
    response = requests.post(f"{BASE_API_URL}/insert", json={"value": new_value})
    return response.json()

def remove_value(target_value):
    response = requests.post(f"{BASE_API_URL}/delete", json={"value": target_value})
    return response.json()

def reset_storage():
    response = requests.post(f"{BASE_API_URL}/clear")
    return response.json()

# Fetch the directory data
directory_info = fetch_directory()

st.write(f"### Extensible hashing: current global depth: {directory_info['global_depth']}")

directory_structure = directory_info["directory"]

input_value = st.text_input("Enter value:")

column_one, column_two, column_three = st.columns(3)
with column_one:
    if st.button("Insert"):
        if input_value.isdigit():
            response = add_value(int(input_value))  
            st.success(response['message'])
            st.experimental_rerun()  
        else:
            st.error("Please enter a valid integer.")

with column_two:
    if st.button("Delete"):
        if input_value.isdigit():
            response = remove_value(int(input_value))  
            st.success(response['message'])
            st.experimental_rerun()  
        else:
            st.error("Please enter a valid integer.")

with column_three:
    if st.button("Clear All"):
        response = reset_storage()
        st.success(response['message'])
        st.experimental_rerun()  

for bucket_key, bucket_values in directory_structure.items():
    current_depth = len(bucket_values)  
    bucket_display = f"""
        <div style='border: 2px solid #2205fa; padding: 10px; margin: 10px; border-radius: 10px;'>
            <div style='font-size:20px; font-weight: bold;'>Bucket {bucket_key}</div>
            <div>Current local depth: {current_depth}</div>
            <div style='font-size:18px; margin-top: 10px;'>Values: {', '.join(map(str, bucket_values)) if bucket_values else 'None'}</div>
        </div>
    """
    st.markdown(bucket_display, unsafe_allow_html=True)
