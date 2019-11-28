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