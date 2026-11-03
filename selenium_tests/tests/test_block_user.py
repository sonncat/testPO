
# Тест на блок учетки опенбмс
def test_block_user(page):
    page.base.open_url()

    # вводим 5 раз кривой пароль
    for i in range(5):
        page.login.fill_login("root")
        page.login.fill_password("0penBmc1")
        page.login.click_login_button()
        assert page.login.check_login_alert() == 'Invalid username or password', 'Неправильно всё вообще'

    # вводим корректный пароль
    page.login.fill_password("0penBmc")
    page.login.click_login_button()

    try:
        page.main.get_username_profile()
    except Exception as e:
        success_test = True
        assert success_test
    else:
        faild = False
        assert faild, 'Блокировка не прошла'    