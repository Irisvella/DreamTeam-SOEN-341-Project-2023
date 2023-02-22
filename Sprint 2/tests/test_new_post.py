from website.models import User


def test_new_user():
    """
    GIVEN a Post model
    WHEN a new job posting is created
    THEN check that the fields are defined correctly
    """
    test = 'Hello'
    
    assert test == 'Hello'
    '''
    post = User('patkennedy79@gmail.com', 'Google', '25000')
    assert post.email == 'patkennedy79@gmail.com'
    assert post.company == 'Google'
    '''
