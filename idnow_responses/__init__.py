"""
https://www.idnow.io/docs/api/IDnow_API_Latest.pdf
"""

import json
import re

import pytest
import responses

__version__ = "0.0.1"


seen_idents = {}
base = "https://gateway.test.idnow.de"
company_id = "yourcompany"

_RE_POST = re.compile(
    f"{base}/api/v1/{company_id}/identifications/(?P<txnumber>.*)/start"
)
_RE_GET = re.compile(f"{base}/api/v1/{company_id}/identifications/(?P<txnumber>.*)")


def post_identification_callback(request):
    global seen_idents
    headers = {"request-id": "uuid"}
    matches = _RE_POST.match(request.url)
    body = {"id": matches.groupdict()["txnumber"]}
    seen_idents[body["id"]] = body
    return (200, headers, json.dumps(body))


def get_identification_callback(request):
    global seen_idents
    matches = _RE_GET.match(request.url)
    txnumber = matches.groupdict()["txnumber"]
    headers = {"request-id": "uuid"}
    if txnumber not in seen_idents:
        return (404, headers, json.dumps({"errors": [{"cause": "OBJECT_NOT_FOUND"}]}))
    return (200, headers, json.dumps(seen_idents[txnumber]))


@pytest.fixture
def idnow_responses(request=None):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add_callback(
            responses.POST,
            _RE_POST,
            callback=post_identification_callback,
            content_type="application/json",
        )

        rsps.add_callback(
            responses.GET,
            _RE_GET,
            callback=get_identification_callback,
            content_type="application/json",
        )

        yield rsps
