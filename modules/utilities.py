# ********************************************************************************************
# Shamelessly stolen from Jeff Kassel by Mike Haggerty (2019)
# As of this publish there are no known public versions of this file I stole from Jeff
# I also do not know if this was shameless stolen from others by Jeff
# No known license from Jeff's work, but if there is, it would be presiding.
# ********************************************************************************************

import json


def render_template(search_key, **kwargs):
    json_data = open('templates/templates.json').read()
    template_data = json.loads(json_data)
    for key, val in template_data.items():
        if key == search_key:
            for word, translation in kwargs.items():
                val = (val.replace('{{ ' + word + ' }}', str(translation)))
            return val
