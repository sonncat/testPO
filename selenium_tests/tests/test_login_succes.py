
# Тест успешной авторизации
def test_login_success(page):
    page.base.open_url()
    page.login.fill_login("root")
    page.login.fill_password("0penBmc")
    page.login.click_login_button()
    assert page.main.get_username_profile() == 'root', "Авторизация прошла не под root" 

