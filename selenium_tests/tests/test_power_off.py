import time

def test_power_off(page):
    page.login.full_login_root()
    assert page.main.get_username_profile() == 'root', "Авторизация прошла не под root" 

    page.power_control.open_control_page()
    time.sleep(5)
    if page.power_control.power_control_status() == "Off":    
        page.base.click_element(page.power_control.power_control_locators.xpath_power_on_button)
        page.base.find_element(page.power_control.power_control_locators.xpath_alert_after_click_power)

    page.base.driver.refresh()
    page.power_control.shutdown_server()
    page.base.find_element(page.power_control.power_control_locators.xpath_alert_after_click_power)
    page.base.driver.refresh()
    status = page.power_control.power_control_status()
    
    assert status == "Off", f'Сервер не выключился, статус сервера - {status}'

    







