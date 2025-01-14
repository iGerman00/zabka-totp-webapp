# Żappka bez klopot

Use the QR code without visiting the bloated store app, from your browser  
[Click here to access the web app →](https://zaba.igerman.cc)

| <img src="https://github.com/user-attachments/assets/69fefd04-1d1e-41cd-a329-58f80fd41ac4" width="300" alt="Normal UI"> | <img src="https://github.com/user-attachments/assets/d3f29fbc-44ed-43ea-8409-f79f1fdb16d3" width="300" alt="Alternate"> |
|:--:|:--:|
| Normal UI | Alternate |

## Usage
1. Clone the repository:
```sh
git clone https://github.com/iGerman00/zabka-totp-webapp
```
2. Using `python` (3.8+), run the `login-for-secrets.py` script:
```sh
python login-for-secrets.py
```
You will be prompted to enter your phone number registered with the official app, after which, a verification code will be sent to your number. You will then be prompted to input your code.
Afterwards, you will be presented with something like this:

```sh
-----------------------------
COPY THE FOLLOWING LINE TO THE WEB BROWSER:

{"secret":"2db76449a55d59f1f9420b809edb1beb19dfa434ddb5dbf331f01aec35956e35","ployId":"123456789012"}
```
You should do what it says and copy the line containing the secrets to the Web App

> ⚠️ **WARNING**: The Python script contacts the app's servers. I am not responsible for any action they take against your account. All requests and credentials remain on your machine.

### Using the web app
1. Open the web app (https://zaba.igerman.cc)
2. Input the afforementioned secrets line, hit <kbd>Enter</kbd>
3. Profit!

## Why this exists
The official Żappka mobile app includes multiple dozens of tracking requests just on startup. This simple alternative generates your QR code without any tracking or privacy concerns.
Since a recent update also disabled the static widget functionality, this page provides a convenient alternative that even works offline.

## Technical details
* Your secrets are stored locally using the Web Storage API
* You can use `?secrets=<URL_ENCODED_SECRETS>` in the URL to pre-populate secrets
* You can use `?alternate` in the URL to use the alternate design
* This page is not affiliated with Żappka
* TOTP implementation based on [TehFridge's Zappka3DS](https://github.com/TehFridge/Zappka3DS)

## Notka Prawna (Polski)
Ta aplikacja jest projektem open source, która korzysta z API aplikacji Żappka, należącej do Żabka Group S.A. Aplikacja została stworzona wyłącznie w celach edukacyjnych i nie jest powiązana z Żabka Group S.A. Twórca aplikacji nie jest w żaden sposób związany z Żabka Group S.A. i nie czerpie żadnych korzyści finansowych z tego projektu. Wszystkie znaki towarowe, nazwy handlowe i logotypy są własnością odpowiednich właścicieli. Użytkownicy korzystają z aplikacji na własne ryzyko.

## Legal Notice (English)
This application is an open-source project that utilizes the API of the Żappka app, owned by Żabka Group S.A. The application was created solely for educational purposes and is not affiliated with Żabka Group S.A. The creator of the application is not in any way connected to Żabka Group S.A. and does not derive any financial benefits from this project. All trademarks, trade names, and logos are the property of their respective owners. Users use the application at their own risk.
