# 🧠 Histral Core

[![Unit Tests for HistralCore](https://github.com/histral/histral_core/actions/workflows/unit_tests.yml/badge.svg)](https://github.com/histral/histral_core/actions/workflows/unit_tests.yml)

Set of modules used in various **Histral** repositories.

## Installation

Run fallowing command to add `histral-core` to your project,

```bash
pip install git+https://github.com/histral/histral_core.git@master
```

## Environment Variables

The package requires fallowing `env` variables to update and read data from
firebase firestore.

```txt
FIREBASE_TYPE (Optional)
FIREBASE_UNIVERSE_DOMAIN (Optional)
FIREBASE_AUTH_URI (Optional)
FIREBASE_TOKEN_URI (Optional)
FIREBASE_AUTH_PROVIDER_X509_CERT_URL (Optional)
FIREBASE_PROJECT_ID
FIREBASE_CLIENT_ID
FIREBASE_CLIENT_EMAIL
FIREBASE_PRIVATE_KEY_ID
FIREBASE_PRIVATE_KEY
FIREBASE_CLIENT_X509_CERT_URL
```

## Linting

Run fallowing commands to ensure proper linting and formatting

```py
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

```py
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --ignore=W293,W503
```
