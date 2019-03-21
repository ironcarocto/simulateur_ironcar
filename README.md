[![Build Status](https://travis-ci.org/ironcarocto/simulateur_ironcar.svg?branch=master)](https://travis-ci.org/ironcarocto/simulateur_ironcar)

Ce simulateur permet de générer un dataset préqualifié d'images de
route tel que la verrait la caméra d'une **ironcar** associées à la commande de direction pour l'ironcar.

[Ironcar](http://ironcar.org/) est un championnat de courses de voitures
autonomes en modèle réduit !

__2 exemples de sortie de simulateur_ironcar__

![Banner](docs/images/21_cmd_0.png)![Banner](docs/images/155_cmd_2.png)

## Dernière version du code source de ce programme

```bash
git clone https://github.com/Cnstant/simulateur_ironcar
```

## Contribuer au projet

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
