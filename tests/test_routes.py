def test_home(client):
    response = client.get('/')  # 根路由
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response.get_data(as_text=True)}"

def test_index(client):
    response = client.get('/index')  # /index 路由
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response.get_data(as_text=True)}"

def test_show_users(client):
    response = client.get('/test/users')  # Blueprint 路由
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response: {response.get_data(as_text=True)}"
