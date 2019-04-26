import json


def render_template(search_key, **kwargs):
    json_data = open('templates/templates.json').read()
    template_data = json.loads(json_data)
    for key, val in template_data.items():
        if key == search_key:
            for word, translation in kwargs.items():
                val = (val.replace('{{ ' + word + ' }}', str(translation)))
            return val
