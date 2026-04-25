import streamlit as st
import os
import subprocess
from engine.shadow_engine import shadow_redact

# 1. Page Setup
st.set_page_config(page_title="ShadowVault Pro", page_icon="🛡️", layout="wide")

# 2. State Initialization
if 'vault_password' not in st.session_state:
    st.session_state['vault_password'] = None
if 'file_sealed' not in st.session_state:
    st.session_state['file_sealed'] = False

# 3. Sidebar - Custom Username & Reset
with st.sidebar:
    st.header("👤 User Profile")
    current_user = st.text_input("Enter your Name", value="Guest User")
    st.write("---")
    if st.button("Reset Session"):
        st.session_state.clear()
        if os.path.exists("data/sensitive_raw.txt"):
            os.remove("data/sensitive_raw.txt")
        st.rerun()

# 4. Main UI
st.title("🛡️ ShadowVault AI")

# --- STEP A: PASSWORD INITIALIZATION ---
# This ONLY shows if no password exists
if st.session_state['vault_password'] is None:
    st.subheader("🔑 Initialize Master Vault")
    new_pass = st.text_input("Create your Master Passcode", type="password", help="This will be used to unlock all future records.")
    if st.button("Set Passcode"):
        if new_pass:
            st.session_state['vault_password'] = new_pass
            st.success("Passcode Established!")
            st.rerun()
        else:
            st.error("Please enter a valid passcode.")
    st.stop() # Stops the rest of the app from loading until password is set

# --- STEP B: FILE UPLOADER & REDACTION ---
uploaded_file = st.file_uploader("Upload Document", type=["txt"])

if uploaded_file:
    # If a new file is uploaded, we reset the 'sealed' status
    # This prevents unlocking old data for a new file
    content = uploaded_file.read().decode("utf-8")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Source")
        st.info(content)
    with col2:
        st.subheader("AI Redacted")
        redacted = shadow_redact(content)
        st.success(redacted)

    # --- STEP C: SEALING LOGIC ---
    if st.button("🔒 Seal in Java Vault"):
        # We pass the content AND the current_user to the bridge
        with open("data/sensitive_raw.txt", "w") as f:
            f.write(f"{current_user}\n{content}") # Store username on line 1
        
        try:
            subprocess.run(["java", "vault.VaultManager"], check=True)
            st.session_state['file_sealed'] = True
            st.balloons()
            st.toast("Encrypted and Saved!")
        except:
            st.error("Vault Connection Failed.")

# --- STEP D: THE MANAGER ACCESS ---
with st.expander("🔓 Unlock Secure Records"):
    if not st.session_state['file_sealed']:
        st.info("The vault is empty. Please 'Seal' a document above first.")
    else:
        # We wrap this in a form so the 'Enter' key works!
        with st.form("unlock_form", clear_on_submit=False):
            check_pass = st.text_input("Verify Master Passcode", type="password", autocomplete="one-time-code")
            submit_button = st.form_submit_button("Decrypt")
            
            if submit_button:
                if check_pass == st.session_state['vault_password']:
                    st.success("Access Granted!")
                    try:
                        # Ensure you are calling the compiled class
                        result = subprocess.check_output(["java", "vault.VaultUnlocker"], text=True)
                        st.code(result, language="text")
                    except Exception as e:
                        st.error(f"Could not access vault: {e}")
                else:
                    # This will now strictly show 'Incorrect Password'
                    st.error("❌ Incorrect Password. Please try again.")