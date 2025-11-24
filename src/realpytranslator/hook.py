# blocking but stable
import requests

response = requests.get(
    f"http://127.0.0.1:8080/translate?content={what}&source=英文&target=简体中文"
)
if response.ok:
    what = response.json()["translation"]

# non blocking but not that stable
_origin_key = "_origin"
if kwargs.get(_origin_key, True):

    def _translate():
        import requests

        response = requests.get(
            f"http://127.0.0.1:8080/translate?content={what}&source=英文&target=简体中文"
        )
        if response.ok:
            kwargs[_origin_key] = False
            say(who, response.json()["translation"], *args, **kwargs)

    t = threading.Thread(target=_translate)
    t.start()
