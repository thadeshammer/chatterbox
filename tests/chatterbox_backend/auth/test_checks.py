from chatterbox_backend.entities.models import UserRole


def test_role_comparison():
    assert UserRole.SUPER_ADMIN > UserRole.ADMIN
    assert UserRole.SUPER_ADMIN >= UserRole.ADMIN
    assert UserRole.SUPER_ADMIN >= UserRole.SUPER_ADMIN

    assert UserRole.ADMIN > UserRole.MODERATOR
    assert UserRole.ADMIN >= UserRole.MODERATOR
    assert UserRole.ADMIN >= UserRole.ADMIN

    assert UserRole.MODERATOR > UserRole.USER
    assert UserRole.MODERATOR >= UserRole.USER
    assert UserRole.MODERATOR >= UserRole.MODERATOR

    assert UserRole.USER <= UserRole.USER
    assert UserRole.USER <= UserRole.MODERATOR
