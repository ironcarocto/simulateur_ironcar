1) Put images in folder ground

# Contribuer au projet

1. créer un environnement virtuel

```
virtualenv venv -p python3
```

2. installer les dépendances de développement

```bash
. venv/bin/activate; pip install -e .[dev]
```

3. exécuter les tests

```bash
. venv/bin/activate; pytest
```