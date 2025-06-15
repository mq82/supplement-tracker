import streamlit as st
import pandas as pd
from datetime import datetime
import os

SUPPLEMENT_FILE = "supplements.csv"
LOG_FILE = "supplement_log.csv"

if os.path.exists(SUPPLEMENT_FILE):
    df = pd.read_csv(SUPPLEMENT_FILE)
else:
    df = pd.DataFrame(columns=["Name","Brand","Dosage","Suggested Time"])

supplements = {
    "Name": ["EPA 1000","硒镁VD3","Phosphatidyl Choline"],
    "Brand": ["Haim","蝴蝶舒","Now Foods"],
    "Dosage": ["1000 mg/calsule","","180 mg/capsule"],
    "Benefits": ["Anti-inflammation","Inmune support","Good to Renal Tubules"],
    "Suggested Time": ["Morning","Morning","Morning"],
    "Default Amount": ["2","3","2"]
    }

df = pd.DataFrame(supplements)

st.title("Supplement Tracker App v0.1")

st.subheader("📋 Supplement List")
st.dataframe(df)

st.subheader("➕ Add New Supplement")

with st.form("add_supplement_form"):
    name = st.text_input("Name")
    brand = st.text_input("Brand")
    dosage = st.text_input("Dosage")
    time = st.selectbox("Suggested Time", ["Morning", "Afternoon", "Evening","Bedtime"])
    submitted = st.form_submit_button("Add Supplement")

    if submitted:
        if name and brand and dosage:
            new_row = pd.DataFrame([{
                "Name": name,
                "Brand": brand,
                "Dosage": dosage,
                "Suggested Time": time
            }])
            df = pd.concat([df,new_row], ignore_index=True)
            df.to_csv(SUPPLEMENT_FILE, index=False)
            st.success(f"✅ Supplement '{name}' added!")
        else:
            st.warning("⚠️ Please fill in all required fields.")

st.subheader("✅ Daily Intake Tracker")
time_slots = ["Breakfast", "Lunch", "Dinner", "Bedtime"]
record = {}

for slot in time_slots:
    taken = st.checkbox(f"{slot} - Taken?", key=f"{slot}_checkbox")
    quantity = st.number_input(f"{slot} - Quantity",min_value=0, max_value=10, value=0, key=f"{slot}_qty")
    record[slot] = quantity if taken else 0

if st.botton("✅ Submit Record"):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    data_row = {
        "Date": date_str,
        "Time": time_str,
        **record
    }

    # Save to CSV
    csv_file = "supplement_log.csv"
    if os.path.exists(csv_file):
        existing_df = pd.read_csv(csv_file)
        updated_df = pd.concat([existing_df, pd.DataFrame([data_row])], ignore_index=True)
    else:
        updated_df = pd.DataFrame([data_row])

    updated_df.to_csv(csv_file, index=False)
    st.success("📦 Record saved successfully!")

st.write("💾 Saved Record:")
st.write(data_row)