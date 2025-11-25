init python:
    import requests
    import threading

    class RealPyTranslatorClient:
        def __init__(self):
            pass

        def translate(self, content):
            response = requests.get(
                f"http://127.0.0.1:8080/translate?name={config.name}&content={content}&source=英文&target=简体中文"
            )
            if response.ok:
                return response.json()["translation"]
            return ""
            
        def log(self, content):
            response = requests.get(
                f"http://127.0.0.1:8080/log?name={config.name}&content={content}"
            )
            return response.ok

        def character_callback(self, event, **kwargs):
            if event != "show_done":
                return
            if kwargs.get("translated", False):
                return

            screen_say = renpy.get_screen("say")
            widget_who = screen_say.widgets.get("who", None)
            widget_what = screen_say.widgets.get("what", None)

            who = " ".join(widget_who.text) if widget_who else ""
            what = " ".join(widget_what.text) if widget_what else ""

            def _translate_thread():
                if who:
                    translated_who = self.translate(who) or who
                if what:
                    translated_what = self.translate(what) or what

                if who:
                    widget_who.set_text(translated_who)
                if what:
                    widget_what.set_text(translated_what)
            
            t = threading.Thread(target=_translate_thread)
            t.start()

    translator = RealPyTranslatorClient()
    try:
        config.all_character_callbacks.append(translator.character_callback)
    except e:
        translator.log(str(e))
