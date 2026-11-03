
# Тест логов
def test_logs(page):
    page.login.full_login_root()
    assert page.main.get_username_profile() == 'root', "Авторизация прошла не под root" 

    page.logs.open_logs_page()
    assert page.logs.check_logs_is_none_in_table(), 'Таблица пустая или локатор изменился'
