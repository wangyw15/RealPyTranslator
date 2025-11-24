import requests

response = requests.get(
    f"http://127.0.0.1:8080/translate?content={what}&source=英文&target=简体中文"
) # type: ignore
if response.ok:
    what = response.json()["translation"]
