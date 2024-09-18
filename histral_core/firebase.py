import os
import firebase_admin
import logging as Logger

from enum import Enum
from typing import Dict, List
from firebase_admin import credentials, firestore


# Config for custom logging
Logger.basicConfig(
    level=Logger.INFO,
    format="[%(levelname)s] (%(asctime)s) -> %(message)s",
    handlers=[
        Logger.StreamHandler(),
    ],
)


class Category(Enum):
    """
    Enum for news categories.
    """

    BHARAT = "bharat"
    CRICKET = "cricket"
    TECHNOLOGY = "tech"
    USA = "usa"
    BUSINESS = "business"


class OutletCode(Enum):
    """
    Enum for news outlet codes.
    """

    FP = "fp"
    NDTV = "ndtv"
    HINDU = "hindu"
    ISN = "isn"
    YS = "ys"


class _FirebaseOptions(Enum):
    """
    Enum for firebase credentials and env variables
    """

    FIREBASE_TYPE = "FIREBASE_TYPE"
    FIREBASE_UNIVERSE_DOMAIN = "FIREBASE_UNIVERSE_DOMAIN"
    FIREBASE_AUTH_URI = "FIREBASE_AUTH_URI"
    FIREBASE_TOKEN_URI = "FIREBASE_TOKEN_URI"
    FIREBASE_AUTH_PROVIDER_X509_CERT_URL = "FIREBASE_AUTH_PROVIDER_X509_CERT_URL"
    FIREBASE_PROJECT_ID = "FIREBASE_PROJECT_ID"
    FIREBASE_CLIENT_ID = "FIREBASE_CLIENT_ID"
    FIREBASE_CLIENT_EMAIL = "FIREBASE_CLIENT_EMAIL"
    FIREBASE_PRIVATE_KEY_ID = "FIREBASE_PRIVATE_KEY_ID"
    FIREBASE_PRIVATE_KEY = "FIREBASE_PRIVATE_KEY"
    FIREBASE_CLIENT_X509_CERT_URL = "FIREBASE_CLIENT_X509_CERT_URL"


def _get_firestore_db():
    """
    Initialize the Firestore database using Firebase credentials from environment variables.

    **Returns**: `firestore.client`: _The Firestore client instance._

    **Raises**: `Exception`: _If initialization of Firebase fails._
    """

    try:
        firebase_credentials = {
            "type": (
                os.getenv(_FirebaseOptions.FIREBASE_TYPE.value)
                if os.getenv(_FirebaseOptions.FIREBASE_TYPE.value)
                else "service_account"
            ),
            "universe_domain": (
                os.getenv(_FirebaseOptions.FIREBASE_UNIVERSE_DOMAIN.value)
                if os.getenv(_FirebaseOptions.FIREBASE_UNIVERSE_DOMAIN.value)
                else "googleapis.com"
            ),
            "auth_uri": (
                os.getenv(_FirebaseOptions.FIREBASE_AUTH_URI.value)
                if os.getenv(_FirebaseOptions.FIREBASE_AUTH_URI.value)
                else "https://accounts.google.com/o/oauth2/auth"
            ),
            "token_uri": (
                os.getenv(_FirebaseOptions.FIREBASE_TOKEN_URI.value)
                if os.getenv(_FirebaseOptions.FIREBASE_TOKEN_URI.value)
                else "https://oauth2.googleapis.com/token"
            ),
            "auth_provider_x509_cert_url": (
                os.getenv(_FirebaseOptions.FIREBASE_AUTH_PROVIDER_X509_CERT_URL.value)
                if os.getenv(
                    _FirebaseOptions.FIREBASE_AUTH_PROVIDER_X509_CERT_URL.value
                )
                else "https://www.googleapis.com/oauth2/v1/certs"
            ),
            "project_id": os.getenv(_FirebaseOptions.FIREBASE_PROJECT_ID.value),
            "client_id": os.getenv(_FirebaseOptions.FIREBASE_CLIENT_ID.value),
            "client_email": os.getenv(_FirebaseOptions.FIREBASE_CLIENT_EMAIL.value),
            "private_key_id": os.getenv(_FirebaseOptions.FIREBASE_PRIVATE_KEY_ID.value),
            "private_key": os.getenv(
                _FirebaseOptions.FIREBASE_PRIVATE_KEY.value
            ).replace("\\n", "\n"),
            "client_x509_cert_url": os.getenv(
                _FirebaseOptions.FIREBASE_CLIENT_X509_CERT_URL.value
            ),
        }

        cred = credentials.Certificate(firebase_credentials)
        firebase_admin.initialize_app(cred)
        database = firestore.client()

        Logger.info("TRACE: Successfully initialized Firebase client.")

        return database
    except Exception as e:
        Logger.error(f"ERROR: An error occurred while initializing Firebase: {e}")
        raise


def post_news_list(
    DATA: List,
    current_date,
    category: Category,
    outlet_code: OutletCode,
):
    """
    Upload news data to Firestore. If the document exists, it updates the data;
    otherwise, it creates a new entry.

    **Args**:
        `DATA (List)`: _List of news articles._
        `current_date (datetime)`: _Current date for document ID generation._
        `category (Category)`: _Category of news (Enum)._
        `outlet_code (OutletCode)`: _News outlet code (Enum)._

    **Returns**: `None`

    **Raises**: `Exception` _If an error occurs during data upload to Firestore._
    """

    try:
        DB = _get_firestore_db()
        doc_id = f"{current_date.day}-{current_date.month}-{current_date.year}"
        doc_ref = DB.collection(category.value).document(doc_id)
        data = {outlet_code.value: DATA}

        try:
            # Try to get the document
            doc = doc_ref.get()
            if doc.exists:
                # Update the document if it exists
                doc_ref.update(data)

                Logger.info(
                    f"INFO: Stored ({category.value}:{len(DATA)}) news in firestore"
                )
            else:
                # Document doesn't exist, create a new one
                doc_ref.set(data)

                Logger.warning("WARN: New entry created as document was not found.")
                Logger.info(
                    f"INFO: Updated ({category.value}:{len(DATA)}) news in firestore"
                )
        except Exception as e:
            Logger.error(f"ERROR: Failed to update or create Firestore document: {e}")
            raise

    except Exception as e:
        Logger.error(f"ERROR: Unable to upload news list to Firestore: {e}")
        raise


def fetch_news_list(
    current_date,
    category: Category,
) -> Dict:
    """
    Retrieve news data from Firestore for a given category and date.

    **Args**:
        `current_date (datetime)`: _The date for which to retrieve news data._
        `category (Category)`: _Category of news (Enum)._

    **Returns**: `Dict` _Dictionary containing the news data_

    **Raises**:
        `ValueError`: _If no data is found for the specified document._
        `Exception`: _If an error occurs during Firestore data retrieval._
    """

    try:
        DB = _get_firestore_db()
        doc_id = f"{current_date.day}-{current_date.month}-{current_date.year}"
        doc_ref = DB.collection(category.value).document(doc_id)

        # Fetch the document from Firestore
        doc_data = doc_ref.get()

        # Check if data exists
        if doc_data.exists:
            data_dict = doc_data.to_dict()

            Logger.info(f"INFO: Data retrieved for {doc_ref.path}")
            Logger.info(f"INFO: Retrieved news for {len(data_dict)} outlets")

            return data_dict
        else:
            Logger.error(f"FATAL: No data found for document {doc_ref.path}")
            raise ValueError(f"No data found in {doc_ref.path}")

    except Exception as e:
        Logger.error(f"FATAL: Unable to read news from Firestore: {e}")
        raise
