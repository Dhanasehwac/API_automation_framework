def assert_json_content_type(response):
    assert response.headers.get("content-type", "").startswith("application/json")
