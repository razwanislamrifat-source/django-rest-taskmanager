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


@pytest.mark.django_db
def test_filter_by_priority(auth_client, user):
    Task.objects.create(owner=user, title='High priority', status='todo', priority='high')
    Task.objects.create(owner=user, title='Low priority', status='todo', priority='low')
    Task.objects.create(owner=user, title='Medium priority', status='todo', priority='medium')

    response = auth_client.get('/api/tasks/?priority=high')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['priority'] == 'high'


@pytest.mark.django_db
def test_summary_endpoint_mixed_status_priority(auth_client, user):
    Task.objects.create(owner=user, title='Task 1', status='todo', priority='high')
    Task.objects.create(owner=user, title='Task 2', status='in_progress', priority='medium')
    Task.objects.create(owner=user, title='Task 3', status='done', priority='high')
    Task.objects.create(owner=user, title='Task 4', status='done', priority='low')

    response = auth_client.get('/api/tasks/summary/')
    assert response.status_code == 200
    assert response.data['by_status']['todo'] == 1
    assert response.data['by_status']['in_progress'] == 1
    assert response.data['by_status']['done'] == 2
    assert response.data['by_priority']['high'] == 2
    assert response.data['by_priority']['medium'] == 1
    assert response.data['by_priority']['low'] == 1


@pytest.mark.django_db
def test_summary_endpoint_excludes_other_users_tasks(auth_client, user, other_user):
    Task.objects.create(owner=user, title='My task', status='todo', priority='high')
    Task.objects.create(owner=other_user, title='Their task', status='todo', priority='high')

    response = auth_client.get('/api/tasks/summary/')
    assert response.status_code == 200
    assert response.data['by_status']['todo'] == 1
    assert response.data['by_priority']['high'] == 1
