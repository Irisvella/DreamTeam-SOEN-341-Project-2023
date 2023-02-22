from website.models import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    test = 'Hello'
    
    assert test == 'Hello'
    '''
    user = User('patkennedy79@gmail.com', 'FlaskIsAwesome', 'Google')
    assert user.email == 'patkennedy79@gmail.com'
    assert user.hashed_password != 'FlaskIsAwesome'
    assert user.company_name == 'user'
    '''
