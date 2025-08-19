import streamlit as st
from cryptography.fernet import Fernet
import pandas as pd
import os

# ---- CONFIG ----
KEY_FILE = "key.key"
DATA_FILE = "credentials.csv"

# ---- LOAD ENCRYPTION KEY ----
if not os.path.exists(KEY_FILE):
    st.error(f"Key file '{KEY_FILE}' not found. Please create one using Fernet.generate_key().")
    st.stop()

with open(KEY_FILE, "rb") as f:
    encryption_key = f.read()

encryption_fernet = Fernet(encryption_key)

# ---- UI HEADER ----
st.title("🔐 Encrypted Credential Manager")

# ---- ENCRYPTION SECTION ----
st.header("🔏 Save New Credentials")

with st.form("encrypt_form"):
    app_name = st.text_input("Application Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    save_btn = st.form_submit_button("Encrypt & Save")

if save_btn:
    if app_name and username and password:
        enc_user = encryption_fernet.encrypt(username.encode()).decode()
        enc_pass = encryption_fernet.encrypt(password.encode()).decode()

        new_entry = pd.DataFrame([[app_name, enc_user, enc_pass]],
                                 columns=["app_name", "encrypted_username", "encrypted_password"])
        
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            df = pd.concat([df, new_entry], ignore_index=True)
        else:
            df = new_entry

        df.to_csv(DATA_FILE, index=False)
        st.success(f"✅ Credentials for '{app_name}' saved.")
    else:
        st.warning("Please fill all fields before saving.")

# ---- DECRYPTION SECTION ----
st.header("🔓 Retrieve Stored Credentials")

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    app_list = df["app_name"].unique().tolist()
    
    selected_app = st.selectbox("Select Application", app_list)
    user_key_input = st.text_input("Enter Fernet Decryption Key", type="password")
    
    if st.button("Decrypt"):
        try:
            user_fernet = Fernet(user_key_input.encode())
            row = df[df["app_name"] == selected_app].iloc[0]
            
            decrypted_user = user_fernet.decrypt(row["encrypted_username"].encode()).decode()
            decrypted_pass = user_fernet.decrypt(row["encrypted_password"].encode()).decode()

            st.success("🔓 Successfully Decrypted!")
            st.write(f"**Username:** `{decrypted_user}`")
            st.write(f"**Password:** `{decrypted_pass}`")
        except Exception as e:
            st.error("❌ Invalid decryption key or data corrupted.")
else:
    st.info("No data available. Please add credentials first.")
