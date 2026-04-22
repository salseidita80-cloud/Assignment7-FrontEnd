import streamlit as st
import requests

API_BASE = "https://myapi1-pz44.onrender.com"

st.title("President SCRUD App")

try:
    response = requests.get(f"{API_BASE}/presidents")
    data = response.json()
except:
    st.error("Error connecting to API")
    data = []

st.header("Search Presidents")

search = st.text_input("Enter name to search")

if search:
    filtered = []
    for p in data:
        if search.lower() in p["firstname"].lower() or search.lower() in p["lastname"].lower():
            filtered.append(p)
else:
    filtered = data

for p in filtered:
    st.write(f'ID: {p["id"]} | {p["firstname"]} {p["lastname"]}')

st.header("Retrieve by ID")

rid = st.number_input("Enter ID", min_value=1, step=1)

if st.button("Get President"):
    res = requests.get(f"{API_BASE}/presidents/{rid}")
    if res.status_code == 200:
        st.json(res.json())
    else:
        st.error("Not found")

st.header("Create President")

c_first = st.text_input("First Name")
c_last = st.text_input("Last Name")
c_birth = st.text_input("Birthdate")

if st.button("Create"):
    payload = {
        "firstname": c_first,
        "lastname": c_last,
        "birthdate": c_birth
    }
    res = requests.post(f"{API_BASE}/presidents", json=payload)
    if res.status_code in [200, 201]:
        st.success("Created!")
        st.json(res.json())
    else:
        st.error("Error creating")

st.header("Update President")

u_id = st.number_input("ID to update", min_value=1, step=1, key="u")
u_first = st.text_input("New First Name")
u_last = st.text_input("New Last Name")
u_birth = st.text_input("New Birthdate")

if st.button("Update"):
    payload = {
        "firstname": u_first,
        "lastname": u_last,
        "birthdate": u_birth
    }
    res = requests.patch(f"{API_BASE}/presidents/{u_id}", json=payload)
    if res.status_code == 200:
        st.success("Updated!")
        st.json(res.json())
    else:
        st.error("Error updating")

st.header("Delete President")

d_id = st.number_input("ID to delete", min_value=1, step=1, key="d")

if st.button("Delete"):
    res = requests.delete(f"{API_BASE}/presidents/{d_id}")
    if res.status_code == 200:
        st.success("Deleted!")
    else:
        st.error("Error deleting")
