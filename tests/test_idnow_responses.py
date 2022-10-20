def test_basic(pytester):
    # create a temporary pytest test file
    pytester.makepyfile(
        """
        import requests

        def test_service(idnow_responses):
            company_id = "yourcompany"

            # Create ident
            url = f"https://gateway.test.idnow.de/api/v1/{company_id}/identifications/foo-123-ab/start"
            response = requests.post(url)
            assert response.status_code == 200
            assert response.json() == {'id': 'foo-123-ab'}

            # Get ident
            url = f"https://gateway.test.idnow.de/api/v1/{company_id}/identifications/foo-123-ab"
            response = requests.get(url)
            assert response.status_code == 200
            assert response.json() == {'id': 'foo-123-ab'}

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
