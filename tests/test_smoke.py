def test_sanity_check_endpoint(client):
    response = client.get("/sanityCheck")
    assert response.data == b'Success'
