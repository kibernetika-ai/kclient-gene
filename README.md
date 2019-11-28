# KClient generator

## Prepare openapi

Read openapi from https://dev.kibernetika.io/docs/apidocs.json and save prepared data to `prepared.json`:
```bash
python prepare.py
```

Another source can be set with `--source`, it can be local file or URL.
Target file also can be set with `--output`. For example:

```bash
python prepare.py --source source.json --output output.json
```

## Swagger Codegen

### Download

Latest [Swagger Codegen](https://github.com/swagger-api/swagger-codegen) can be downloaded with the following command:
```bash
wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.4.10/swagger-codegen-cli-2.4.10.jar -O swagger-codegen-cli.jar

java -jar swagger-codegen-cli.jar help
```
The latest version at the moment is 2.4.10, actual version can be found [here](https://github.com/swagger-api/swagger-codegen#prerequisites).

### Generate

Get available languages list:

```bash
java -jar swagger-codegen-cli.jar langs
```

Generate python package from `prepared.json` in directory `out/python`:

```bash
java -jar swagger-codegen-cli.jar generate -i prepared.json -l python -o out/python
```
