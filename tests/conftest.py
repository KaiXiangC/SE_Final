import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True  # 啟用測試模式
    app.config['WTF_CSRF_ENABLED'] = False  # 禁用 CSRF（方便測試）
    return app

@pytest.fixture
def client(app):
    return app.test_client()
