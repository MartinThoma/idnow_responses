def test_basic(pytester):
    # create a temporary pytest test file
    pytester.makepyfile(
        """
        import requests
        import idnow_responses

        idnow_responses.company_id = "Mandala"

        def test_service(idnow_responses):
            company_id = "Mandala"

            # Create ident
            url = f"https://gateway.test.idnow.de/api/v1/{company_id}/identifications/foo-123-ab/start"
            response = requests.post(url)
            assert response.status_code == 200
            assert response.json() == {'id': 'foo-123-ab'}

            # Get ident
            url = f"https://gateway.test.idnow.de/api/v1/{company_id}/identifications/foo-123-ab"
            response = requests.get(url)
            assert response.status_code == 200
            actual = response.json()

            idprocess = {'agentname': 'JSMITH', 'companyid': 'foobar', 'filename': 'foo.zip', 'id': 'foo-123-ab', 'type': 'APP', 'result': 'SUCCESS'}
            userdata = {'birthday': {'status': 'NEW', 'value': actual['userdata']['birthday']['value']}}
            expected = {'identificationprocess': idprocess, 'userdata': userdata}
            assert actual == expected

            # Get unknown ident
            url = f"https://gateway.test.idnow.de/api/v1/{company_id}/identifications/unknown-tx-id"
            response = requests.get(url)
            assert response.status_code == 404
            assert response.json() == {'errors': [{'cause': 'OBJECT_NOT_FOUND'}]}
        """
    )

    # run all tests with pytest
    result = pytester.runpytest()

    # check that the test passed
    result.assert_outcomes(passed=1)
