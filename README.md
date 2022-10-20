# idnow_responses
A third-party pytest plugin that provides a fixture to mock the IdNow identification service.

## Installation

```
pip install idnow-responses
```

## Usage

This plugin makes the `idnow_responses` fixture available. Typically the request
to IdNow would be within the tested code and not within the test. For
simplicity, it's here in the request:


```python
import requests
import idnow_responses

idnow_responses.company_id = "Mandala"


def test_service(idnow_responses):
    company_id = "Mandala"

    # Create ident
    url = f"https://gateway.test.idnow.de/api/v1/{company_id}/identifications/foo-123-ab/start"
    response = requests.post(url)
    assert response.status_code == 200
    assert response.json() == {"id": "foo-123-ab"}

    # Get ident
    url = (
        f"https://gateway.test.idnow.de/api/v1/{company_id}/identifications/foo-123-ab"
    )
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == {"id": "foo-123-ab"}

    # Get unknown ident
    url = f"https://gateway.test.idnow.de/api/v1/{company_id}/identifications/unknown-tx-id"
    response = requests.get(url)
    assert response.status_code == 404
    assert response.json() == {"errors": [{"cause": "OBJECT_NOT_FOUND"}]}
```
