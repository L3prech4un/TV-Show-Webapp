def test_home_page(client):
    """Test that home page loads"""
    response = client.get('/')
    assert response.status_code == 200

def test_signup_page(client):
    """Test the signup page"""
    response = client.get('/signup')
    assert response.status_code == 200

def test_login_page(client):
    """Test the login page"""
    response = client.get('/login')
    assert response.status_code == 200

def test_profile_page(client):
    """Test the my_profile page"""
    response = client.get('/my_profile', follow_redirects=True)
    assert response.status_code == 200

def test_about_page(client):
    """Test the about page"""
    response = client.get('/about')
    assert response.status_code == 200

def test_my_feed_page(client):
    """Test the my_feed page"""
    response = client.get('/my_feed', follow_redirects=True)
    assert response.status_code == 200

def test_create_post_page(client):
    """Test the create_post page"""
    response = client.get('/create_post', follow_redirects=True)
    assert response.status_code == 200

def test_discover_page(client):
    """Test the discover page"""
    response = client.get('/discover', follow_redirects=True)
    assert response.status_code == 200

def test_add_to_watched_page(client):
    """Test the add_to_watched page"""
    response = client.post('/add_to_watched', data={'mediaid': '1'}, follow_redirects=True)
    assert response.status_code == 200

def test_remove_from_watched_page(client):
    """Test the removed_from_watched page"""
    response = client.post('/remove_from_watched', data={'title': 'Some Title'}, follow_redirects=True)
    assert response.status_code == 200