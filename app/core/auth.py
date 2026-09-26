import os
import requests
from dotenv import load_dotenv
import streamlit as st

# Load environment variables (from .env or st.secrets)
load_dotenv()

def get_config():
    api_key = os.getenv("FIREBASE_API_KEY")
    project_id = os.getenv("FIREBASE_PROJECT_ID")
    google_client_id = os.getenv("GOOGLE_CLIENT_ID")
    google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

    try:
        if not api_key and hasattr(st, "secrets") and "FIREBASE_API_KEY" in st.secrets:
            api_key = st.secrets["FIREBASE_API_KEY"]
        if not project_id and hasattr(st, "secrets") and "FIREBASE_PROJECT_ID" in st.secrets:
            project_id = st.secrets["FIREBASE_PROJECT_ID"]
        if not google_client_id and hasattr(st, "secrets") and "GOOGLE_CLIENT_ID" in st.secrets:
            google_client_id = st.secrets["GOOGLE_CLIENT_ID"]
        if not google_client_secret and hasattr(st, "secrets") and "GOOGLE_CLIENT_SECRET" in st.secrets:
            google_client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
    except Exception:
        pass

    return {
        "api_key": api_key,
        "project_id": project_id,
        "google_client_id": google_client_id,
        "google_client_secret": google_client_secret
    }

def sign_up_with_email_password(email, password, display_name=""):
    config = get_config()
    api_key = config.get("api_key")
    if not api_key:
        raise ValueError("Firebase API Key is not configured.")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    resp = requests.post(url, json=data)
    result = resp.json()

    if "error" in result:
        error_message = result["error"].get("message", "Unknown error")
        raise Exception(error_message)

    id_token = result["idToken"]

    # Set display name if provided
    if display_name:
        update_url = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={api_key}"
        update_data = {
            "idToken": id_token,
            "displayName": display_name,
            "returnSecureToken": True
        }
        update_resp = requests.post(update_url, json=update_data)
        update_result = update_resp.json()
        if "error" not in update_result:
            result["displayName"] = update_result.get("displayName", "")

    return result

def sign_in_with_email_password(email, password):
    config = get_config()
    api_key = config.get("api_key")
    if not api_key:
        raise ValueError("Firebase API Key is not configured.")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    resp = requests.post(url, json=data)
    result = resp.json()

    if "error" in result:
        error_message = result["error"].get("message", "Unknown error")
        raise Exception(error_message)

    return result

def send_password_reset_email(email):
    config = get_config()
    api_key = config.get("api_key")
    if not api_key:
        raise ValueError("Firebase API Key is not configured.")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}"
    data = {
        "requestType": "PASSWORD_RESET",
        "email": email
    }

    resp = requests.post(url, json=data)
    result = resp.json()

    if "error" in result:
        error_message = result["error"].get("message", "Unknown error")
        raise Exception(error_message)

    return True

def get_google_auth_url(redirect_uri="http://localhost:8505"):
    config = get_config()
    client_id = config.get("google_client_id")
    if not client_id:
        return None

    url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"scope=email%20profile%20openid&"
        f"access_type=offline&"
        f"prompt=select_account"
    )
    return url

def exchange_google_code_for_firebase_token(code, redirect_uri="http://localhost:8505"):
    config = get_config()
    client_id = config.get("google_client_id")
    client_secret = config.get("google_client_secret")
    api_key = config.get("api_key")

    if not client_id or not client_secret or not api_key:
        raise ValueError("Google OAuth or Firebase credentials are not fully configured.")

    # 1. Exchange code for Google ID token
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }

    token_resp = requests.post(token_url, data=token_data)
    token_result = token_resp.json()

    if "error" in token_result:
        raise Exception(f"Google OAuth Error: {token_result.get('error_description', token_result.get('error'))}")

    google_id_token = token_result.get("id_token")
    if not google_id_token:
        raise Exception("Failed to retrieve ID token from Google.")

    # 2. Exchange Google ID token for Firebase token
    fb_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={api_key}"
    fb_data = {
        "postBody": f"id_token={google_id_token}&providerId=google.com",
        "requestUri": redirect_uri,
        "returnIdpCredential": True,
        "returnSecureToken": True
    }

    fb_resp = requests.post(fb_url, json=fb_data)
    fb_result = fb_resp.json()

    if "error" in fb_result:
        raise Exception(f"Firebase Identity Toolkit Error: {fb_result['error'].get('message', 'Unknown error')}")

    return fb_result
