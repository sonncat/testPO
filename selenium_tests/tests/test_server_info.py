def test_server_info(page):
    page.login.full_login_root()
    assert page.main.get_username_profile() == 'root', "Авторизация прошла не под root" 

    page.main.open_main_page()

    assert page.main.check_info_is_none(page.main.main_page_locators.xpath_model_server_inf) is False, 'Отсутвует информация о модели'
    assert page.main.check_info_is_none(page.main.main_page_locators.xpath_server_manufacturer_inf) is False, 'Отсутвует информация о производителе сервера'
    assert page.main.check_info_is_none(page.main.main_page_locators.xpath_serial_number_inf) is False, 'Отсутвует информация о серийном номере'



