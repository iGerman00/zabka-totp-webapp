# zabka-totp-webapp
Use the QR code without visiting the bloated store app

## Why this exists
The official Żappka mobile app includes multiple dozens of tracking requests just on startup. This simple alternative generates your QR code without any tracking or privacy concerns.
Since a recent update also disabled the static widget functionality, this page provides a convenient alternative that even works offline.

## Technical details
* Your secrets are stored locally using the Web Storage API
* You can use ?secrets=<URL_ENCODED_SECRETS> in the URL to pre-populate secrets
* This page is not affiliated with Żappka
* TOTP implementation based on [TehFridge's Zappka3DS](https://github.com/TehFridge/Zappka3DS)

## Notka Prawna (Polski)
Ta aplikacja jest projektem open source, która korzysta z API aplikacji Żappka, należącej do Żabka Group S.A. Aplikacja została stworzona wyłącznie w celach edukacyjnych i nie jest powiązana z Żabka Group S.A. Twórca aplikacji nie jest w żaden sposób związany z Żabka Group S.A. i nie czerpie żadnych korzyści finansowych z tego projektu. Wszystkie znaki towarowe, nazwy handlowe i logotypy są własnością odpowiednich właścicieli. Użytkownicy korzystają z aplikacji na własne ryzyko.

## Legal Notice (English)
This application is an open-source project that utilizes the API of the Żappka app, owned by Żabka Group S.A. The application was created solely for educational purposes and is not affiliated with Żabka Group S.A. The creator of the application is not in any way connected to Żabka Group S.A. and does not derive any financial benefits from this project. All trademarks, trade names, and logos are the property of their respective owners. Users use the application at their own risk.
