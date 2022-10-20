"""
https://www.idnow.io/docs/api/IDnow_API_Latest.pdf
"""

import json
import re

import pytest
import responses
from faker import Faker

Faker.seed(0)
fake = Faker()

__version__ = "0.0.1"


seen_idents = {}
base = "https://gateway.test.idnow.de"
company_id = "yourcompany"

_RE_POST = "{base}/api/v1/{company_id}/identifications/(?P<txnumber>.*)/start"
_RE_GET = "{base}/api/v1/{company_id}/identifications/(?P<txnumber>.*)"


def post_identification_callback(request):
    global seen_idents
    headers = {"request-id": "uuid"}
    matches = re.compile(_RE_POST.format(base=base, company_id=company_id)).match(
        request.url
    )
    body = {"id": matches.groupdict()["txnumber"]}
    seen_idents[body["id"]] = {
        "birthday": {
            "status": "NEW",
            "value": f"{fake.date_of_birth(minimum_age=18, maximum_age=118):%Y-%m-%d}",
        }
    }
    return (200, headers, json.dumps({"id": body["id"]}))


def get_identification_callback(request):
    global seen_idents
    matches = re.compile(_RE_GET.format(base=base, company_id=company_id)).match(
        request.url
    )
    txnumber = matches.groupdict()["txnumber"]
    headers = {"request-id": "uuid"}
    if txnumber not in seen_idents:
        return (404, headers, json.dumps({"errors": [{"cause": "OBJECT_NOT_FOUND"}]}))
    return (
        200,
        headers,
        json.dumps(
            {
                "identificationprocess": {
                    "result": "SUCCESS",
                    "companyid": "foobar",
                    "filename": "foo.zip",
                    "agentname": "JSMITH",
                    "id": txnumber,
                    "type": "APP",
                },
                "userdata": seen_idents[txnumber],
            }
        ),
    )


@pytest.fixture
def idnow_responses(request=None):
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add_callback(
            responses.POST,
            re.compile(_RE_POST.format(base=base, company_id=company_id)),
            callback=post_identification_callback,
            content_type="application/json",
        )

        rsps.add_callback(
            responses.GET,
            re.compile(_RE_GET.format(base=base, company_id=company_id)),
            callback=get_identification_callback,
            content_type="application/json",
        )

        yield rsps
