def test_sanity_check_endpoint(client):
    response = client.get("/healthcheck")
    assert response.data == b'Success'
    assert response.status_code == 200
