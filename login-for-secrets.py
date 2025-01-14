import requests
import json
import hmac
import hashlib
import struct
import time
import re

# --- Configuration (User-specific) ---
FIREBASE_API_KEY = "AIzaSyByV8PCH4umClqDWZRMy2nSm7DXjQOWt1U"

# --- Constants ---
IDENTITY_TOOLKIT_URL = "https://www.googleapis.com/identitytoolkit/v3/relyingparty"
SUPER_ACCOUNT_URL = "https://super-account.spapp.zabka.pl/"
API_URL = "https://api.spapp.zabka.pl/"
CLIENT_TYPE = "CLIENT_TYPE_IOS"
CLIENT_VERSION = "iOS/FirebaseSDK/10.26.0/FirebaseCore-iOS"
IOS_BUNDLE_IDENTIFIER = "pl.zabka.apb2c"
GMPID = "1:123456789012:ios:e7e7e7e7e7e7e7e7e7e7e7"

def generate_totp(secret_hex, time_step=30):
    """Generates a TOTP code."""
    secret = bytes.fromhex(secret_hex)
    ts = int(time.time()) // time_step
    msg = struct.pack(">Q", ts)
    hmac_result = hmac.new(secret, msg, hashlib.sha1).digest()
    offset = hmac_result[-1] & 0x0F
    truncated_hash = struct.unpack(">I", hmac_result[offset:offset + 4])[0] & 0x7FFFFFFF
    totp = truncated_hash % 1000000
    return "{:06d}".format(totp)

def generate_qr_code_url(secret, user_id, time_step=30):
    """Generates a TOTP code."""
    totp = generate_totp(secret, time_step)
    return f"https://srln.pl/view/dashboard?ploy={user_id}&loyal={totp}"

def signup_new_user():
    """Signs up a new anonymous user."""
    url = f"{IDENTITY_TOOLKIT_URL}/signupNewUser?key={FIREBASE_API_KEY}"
    data = {
        "returnSecureToken": True,
        "clientType": CLIENT_TYPE
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": f"FirebaseAuth.iOS/10.26.0 {IOS_BUNDLE_IDENTIFIER}/4.2.0 iPhone/18.2 hw/iPhone16_1",
        "X-Client-Version": f"{CLIENT_VERSION}/FirebaseCore-iOS",
        "X-Ios-Bundle-Identifier": IOS_BUNDLE_IDENTIFIER,
        "X-Firebase-GMPID": GMPID
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def get_account_info(id_token):
    """Retrieves account info."""
    url = f"{IDENTITY_TOOLKIT_URL}/getAccountInfo?key={FIREBASE_API_KEY}"
    data = {
        "idToken": id_token
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": f"FirebaseAuth.iOS/10.26.0 {IOS_BUNDLE_IDENTIFIER}/4.2.0 iPhone/18.2 hw/iPhone16_1",
        "X-Client-Version": f"{CLIENT_VERSION}/FirebaseCore-iOS",
        "X-Ios-Bundle-Identifier": IOS_BUNDLE_IDENTIFIER,
        "X-Firebase-GMPID": GMPID
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def send_verification_code(id_token, phone_number):
    """Sends a verification code to the provided phone number."""
    url = SUPER_ACCOUNT_URL
    data = {
        "operationName": "SendCode",
        "query": "mutation SendCode($input: SendVerificationCodeInput!) { sendVerificationCode(input: $input) { __typename retryAfterSeconds } }",
        "variables": {
            "input": {
                "phoneNumber": {
                    "countryCode": "48",
                    "nationalNumber": phone_number
                }
            }
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": id_token,
        "User-Agent": "SuperApp/999 CFNetwork/1568.300.101 Darwin/24.2.0",
        "X-Client-Key": "l6u0R9biQcbEvZy5UybJxw",
        "apollographql-client-name": "pl.zabka.apb2c-apollo-ios",
        "apollographql-client-version": "4.2.0-999",
        "X-APOLLO-OPERATION-NAME": "SendCode",
        "X-APOLLO-OPERATION-TYPE": "mutation"
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def sign_in_with_phone(id_token, phone_number, verification_code):
    """Signs in using phone number and verification code."""
    url = SUPER_ACCOUNT_URL
    data = {
        "operationName": "SignIn",
        "query": "mutation SignIn($input: SignInInput!) { signIn(input: $input) { __typename customToken } }",
        "variables": {
            "input": {
                "phoneNumber": {
                    "countryCode": "48",
                    "nationalNumber": phone_number
                },
                "verificationCode": verification_code
            }
        }
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": id_token,
        "User-Agent": "SuperApp/999 CFNetwork/1568.300.101 Darwin/24.2.0",
        "X-Client-Key": "l6u0R9biQcbEvZy5UybJxw",
        "apollographql-client-name": "pl.zabka.apb2c-apollo-ios",
        "apollographql-client-version": "4.2.0-999",
        "X-APOLLO-OPERATION-NAME": "SignIn",
        "X-APOLLO-OPERATION-TYPE": "mutation"
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    custom_token = response.json()["data"]["signIn"]["customToken"]

    return verify_custom_token(custom_token)

def verify_custom_token(custom_token):
    """Verifies the custom token."""
    url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken?key={FIREBASE_API_KEY}"
    data = {
        "token": custom_token,
        "returnSecureToken": True
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def get_qr_code(bearer_token):
    """Retrieves the QR code secret and user ID."""
    url = API_URL
    data = {
        "operationName": "QRCode",
        "query": "query QRCode { qrCode { __typename loyalSecret paySecret ployId } }",
        "variables": {}
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "Zappka/999 (iOS; iPhone 15; 00000000-0000-4000-A000-000000000000) iOS/18.2",
        "X-APOLLO-OPERATION-NAME": "QRCode",
        "X-APOLLO-OPERATION-TYPE": "query",
        "apollographql-client-name": "pl.zabka.apb2c-apollo-ios",
        "apollographql-client-version": "4.2.0-999"
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def main():
    """Main function to handle the login flow and save secrets."""
    try:
        # if secrets.json exists, load it and skip the login flow
        try:
            with open("secrets.json") as f:
                secrets = json.load(f)
                if all(key in secrets for key in ["idToken", "refreshToken", "secret", "ployId"]):
                    print("Secrets loaded from secrets.json")
                    # print("Here's the current TOTP code (for testing):")
                    # print(generate_totp(secrets["secret"]))
                    # print("Here's the current QR Code URL (for testing):")
                    # print(generate_qr_code_url(secrets["secret"], secrets["ployId"]))
                    
                    print("\n\n-----------------------------")
                    print("COPY THE FOLLOWING LINE TO THE WEB BROWSER:\n")
                    print(f'{{"secret":"{secrets["secret"]}","ployId":"{secrets["ployId"]}"}}')
                    return
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        signup_response = signup_new_user()
        id_token = signup_response["idToken"]
        refresh_token = signup_response["refreshToken"]

        get_account_info_response = get_account_info(id_token)
        # print("Account Info:", get_account_info_response)

        phone_number = input("Enter your phone number (without country code): ")
        
        send_code_response = send_verification_code(id_token, phone_number)
        # print("Send Code Response:", send_code_response)

        verification_code = input("Enter the verification code: ")

        sign_in_response = sign_in_with_phone(id_token, phone_number, verification_code)
        # print("Sign In Response:", sign_in_response)

        bearer_token = sign_in_response["idToken"]

        qr_code_response = get_qr_code(bearer_token)
        secret = qr_code_response["data"]["qrCode"]["loyalSecret"]
        user_id = qr_code_response["data"]["qrCode"]["ployId"]

        with open("secrets.json", "w") as f:
            json.dump({
                "idToken": id_token,
                "refreshToken": refresh_token,
                "secret": secret,
                "ployId": user_id
            }, f)

        print("Secrets saved to secrets.json")
        # print("Here's the current TOTP code (for testing):")
        # print(generate_totp(secret))
        # print("Here's the current QR Code URL (for testing):")
        # print(generate_qr_code_url(secret, user_id))
        secrets = {
            "secret": secret,
            "ployId": user_id
        }
        
        print("\n\n-----------------------------")
        print("COPY THE FOLLOWING LINE TO THE WEB BROWSER:\n")
        print(f'{{"secret":"{secrets["secret"]}","ployId":"{secrets["ployId"]}"}}')

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()