import argparse
import json
import os

import requests


def find_ref(prop, listB):
    # print (properties)
    list = listB
    if 'properties' in prop:
        properties = prop['properties']
        for p in properties.keys():
            ref = False
            if '$ref' in properties[p]:
                ref = properties[p]['$ref']
            if 'items' in properties[p] and '$ref' in properties[p]['items']:
                ref = properties[p]['items']['$ref']
            if ref:
                m = ref.replace('#/definitions/', '')
                # print(m)
                # print(list)
                if m not in list:
                    list[m] = True

    # print(list)
    return list


def add_def(def_name, definitions, ful_def):
    if not def_name in definitions:
        definitions[def_name] = ful_def[def_name]


def prepare(source, output):
    if source.startswith('http://') or source.startswith('https://'):
        response = requests.get(source)
        data = json.loads(response.text)
    elif os.path.isfile(source):
        with open('api.json') as f:
            data = json.load(f)
    else:
        raise RuntimeError(f'Unreachable source {source}')

    paths_list = [
        '/api/v0.2/workspace/{workspace}/serving/{serving}',
        '/api/v0.2/workspace/{workspace}/serving/{serving}/disable',
        '/api/v0.2/workspace/{workspace}/serving/{serving}/enable',
        '/api/v0.2/workspace/{workspace}/inference/{inference}/versions/{version}',
        '/api/v0.2/workspace/{workspace}/inference/{inference}/versions/{version}/start',
        '/api/v0.2/workspace/{workspace}/serving/{serving}/tfproxy/{port}/{model}',
        '/api/v0.2/workspace/{workspace}/serving/{serving}/tfproxy/{port}/{model}/{signature}',
        '/api/v0.2/workspace/{workspace}/serving/{serving}/tfproxy/{port}/{model}/{signature}/{version}',
    ]
    model_list = {
        'models.Serving': True,
        'mlapp.Serving': True,
        'models.InferenceVersion': True,
        'inference.RunServingRequest': True,
    }

    paths = {}
    for i in paths_list:
        paths[i] = data['paths'][i]

    definitions = {}

    while True:
        # ml = len(modelList.keys())
        # definitions = {}
        ml_keys = list(model_list.keys())
        for i in ml_keys:
            definitions[i] = data['definitions'][i]
            model_list = find_ref(data['definitions'][i], model_list)

        # print(len(definitions.keys()))
        # print(len(model_list.keys()))
        if len(definitions.keys()) == len(model_list.keys()):
            break
        # print (modelList)

    for i in model_list.keys():
        definitions[i] = data['definitions'][i]

    for key_path in paths.keys():
        for key_m in paths[key_path].keys():
            # print(key_m)
            if 'tags' in paths[key_path][key_m] and len(paths[key_path][key_m]['tags']) > 1:
                paths[key_path][key_m]['tags'].remove('Workspace')

            paths[key_path][key_m]['security'] = [
                {'bearerAuth': []}
                , {'Bearer': []}
            ]

    data['definitions'] = definitions
    data['paths'] = paths
    data['host'] = 'dev.kibernetika.io'
    data['securityDefinitions'] = {
        # "bearerAuth": {
        #   "type": "http",
        #   "scheme": "bearer",
        #   "bearerFormat": "JWT"
        # },
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "prefix": 'Bearer ',
        }
    }

    with open(output, 'w') as json_file:
        json.dump(data, json_file, indent='  ')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--source',
        type=str,
        default='https://dev.kibernetika.io/docs/apidocs.json',
        help='Kibernetika open-api source',
    )
    parser.add_argument(
        '--output',
        type=str,
        default='prepared.json',
        help='Processed shorten Kibernetika open-api',
    )

    args = parser.parse_args()
    kwargs = vars(args)
    kwargs['show_image'] = False

    prepare(source=args.source, output=args.output)
