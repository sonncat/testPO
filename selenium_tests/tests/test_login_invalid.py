
# Тест не успешной авторизации
def test_login_invalid(page):
    page.base.open_url()
    page.login.fill_login("root1")
    page.login.fill_password("0penBmc1")
    page.login.click_login_button()

    assert page.login.check_login_alert() == 'Invalid username or password', 'Неправильно всё вообще'
 