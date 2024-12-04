
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_about(client):
    response = client.get('/index')
    assert response.status_code == 200
