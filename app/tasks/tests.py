import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from tasks.models import Task


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser', password='testpass123', email='test@test.com'
    )


@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        username='otheruser', password='testpass123'
    )


@pytest.fixture
def auth_client(client, user):
    response = client.post('/api/auth/token/', {
        'username': 'testuser',
        'password': 'testpass123'
    })
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


@pytest.mark.django_db
def test_unauthenticated_returns_401(client):
    response = client.get('/api/tasks/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_task_returns_201(auth_client):
    response = auth_client.post('/api/tasks/', {
        'title': 'Buy groceries',
        'status': 'todo',
        'priority': 'high'
    })
    assert response.status_code == 201
    assert response.data['title'] == 'Buy groceries'
    assert response.data['owner'] == 'testuser'


@pytest.mark.django_db
def test_user_only_sees_own_tasks(auth_client, user, other_user):
    Task.objects.create(owner=user, title='My task', status='todo', priority='low')
    Task.objects.create(owner=other_user, title='Their task', status='todo', priority='low')

    response = auth_client.get('/api/tasks/')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['title'] == 'My task'


@pytest.mark.django_db
def test_filter_by_status(auth_client, user):
    Task.objects.create(owner=user, title='Todo task', status='todo', priority='low')
    Task.objects.create(owner=user, title='Done task', status='done', priority='low')

    response = auth_client.get('/api/tasks/?status=todo')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['status'] == 'todo'
