import requests
import json
from app.core.auth import get_config

def get_firestore_url(collection_path, document_id=None):
    config = get_config()
    project_id = config.get("project_id")
    if not project_id:
        raise ValueError("Firebase Project ID is not configured.")

    base_url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents"

    if document_id:
        return f"{base_url}/{collection_path}/{document_id}"
    return f"{base_url}/{collection_path}"

def _dict_to_firestore(data):
    """Simple converter for dict to Firestore document format."""
    fields = {}
    for key, value in data.items():
        if isinstance(value, str):
            fields[key] = {"stringValue": value}
        elif isinstance(value, bool):
            fields[key] = {"booleanValue": value}
        elif isinstance(value, int):
            fields[key] = {"integerValue": str(value)}
        elif isinstance(value, float):
            fields[key] = {"doubleValue": value}
        elif isinstance(value, dict):
            fields[key] = {"mapValue": {"fields": _dict_to_firestore(value)}}
        elif value is None:
            fields[key] = {"nullValue": None}
    return fields

def _firestore_to_dict(document):
    """Simple converter for Firestore document to dict."""
    if "fields" not in document:
        return {}

    result = {}
    for key, value_dict in document["fields"].items():
        if "stringValue" in value_dict:
            result[key] = value_dict["stringValue"]
        elif "booleanValue" in value_dict:
            result[key] = value_dict["booleanValue"]
        elif "integerValue" in value_dict:
            result[key] = int(value_dict["integerValue"])
        elif "doubleValue" in value_dict:
            result[key] = float(value_dict["doubleValue"])
        elif "mapValue" in value_dict:
            result[key] = _firestore_to_dict(value_dict["mapValue"])
        elif "nullValue" in value_dict:
            result[key] = None
    return result

def create_document(id_token, collection_path, document_id, data):
    url = get_firestore_url(collection_path)
    # Using documentId query param to specify the ID
    params = {"documentId": document_id}
    headers = {"Authorization": f"Bearer {id_token}"}

    payload = {"fields": _dict_to_firestore(data)}

    resp = requests.post(url, headers=headers, params=params, json=payload)
    result = resp.json()

    if "error" in result:
        raise Exception(f"Firestore Error: {result['error'].get('message', 'Unknown error')}")

    return _firestore_to_dict(result)

def update_document(id_token, collection_path, document_id, data):
    url = get_firestore_url(collection_path, document_id)
    headers = {"Authorization": f"Bearer {id_token}"}

    # In Firestore REST API, PATCH updates the document.
    # We need to specify updateMask for partial updates, or just send the full document fields.
    payload = {"fields": _dict_to_firestore(data)}

    # For a simple partial update, we must list the fields in the updateMask
    params = []
    for key in data.keys():
        params.append(f"updateMask.fieldPaths={key}")

    query_string = "&".join(params)
    full_url = f"{url}?{query_string}"

    resp = requests.patch(full_url, headers=headers, json=payload)
    result = resp.json()

    if "error" in result:
        raise Exception(f"Firestore Error: {result['error'].get('message', 'Unknown error')}")

    return _firestore_to_dict(result)

def get_document(id_token, collection_path, document_id):
    url = get_firestore_url(collection_path, document_id)
    headers = {"Authorization": f"Bearer {id_token}"}

    resp = requests.get(url, headers=headers)

    if resp.status_code == 404:
        return None

    result = resp.json()
    if "error" in result:
        raise Exception(f"Firestore Error: {result['error'].get('message', 'Unknown error')}")

    return _firestore_to_dict(result)

def list_documents(id_token, collection_path):
    url = get_firestore_url(collection_path)
    headers = {"Authorization": f"Bearer {id_token}"}

    resp = requests.get(url, headers=headers)
    result = resp.json()

    if "error" in result:
        raise Exception(f"Firestore Error: {result['error'].get('message', 'Unknown error')}")

    documents = []
    for doc in result.get("documents", []):
        parsed = _firestore_to_dict(doc)
        # Extract the document ID from the full path 'name'
        doc_id = doc["name"].split("/")[-1]
        parsed["_id"] = doc_id
        documents.append(parsed)

    return documents
