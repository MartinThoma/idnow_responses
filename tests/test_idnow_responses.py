def test_hello(pytester):
    # create a temporary pytest test file
    pytester.makepyfile(
        """
        import requests

        def test_service(idnow_responses):
            company_id = "yourcompany"
            url = f"https://gateway.test.idnow.de/api/v1/{company_id}/identifications/.*"
            response = requests.post(url)
            assert response.status_code == 200
            assert response.json() == {'id': 'new-idnow-id'}
        """
    )

    # run all tests with pytest
    result = pytester.runpytest()

    # check that the test passed
    result.assert_outcomes(passed=1)
