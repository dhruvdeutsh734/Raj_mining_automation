from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    def wait():
        page.wait_for_load_state("networkidle")
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://aisadmin.watsoo.com/")
    page.get_by_placeholder("Enter your email").fill("aisadmin@watsoo.com")
    page.get_by_placeholder("Enter your password").fill("Admin@2023#")
    sign_In = page.get_by_role("button", name="sign in")
    wait()
    sign_In.click()
    print("sign in clicked")
    wait()
    Vehicle_management = page.get_by_role("button", name="Vehicle management")
    Vehicle_management.click()
    print("Vehicle management clicked")
    input("akjdhfajhd")
    browser.close()