def test_pocessor_inventory_item(page):
    page.login.full_login_root()
    assert page.main.get_username_profile() == 'root', "Авторизация прошла не под root" 

    page.inventory.open_inventory_page()
    assert page.inventory.count_item_processor() > 0, 'Процессоров нет - все пронейрослопили'