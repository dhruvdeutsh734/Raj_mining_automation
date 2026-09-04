from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    def Login():
        page.goto("https://vahan.parivahan.gov.in/vltdmaker/vahan/welcome.xhtml")
        page.get_by_role("textbox", name="User ID").fill("fox6")
        page.get_by_role("textbox", name="Password").fill("Watsoo@4664")
        input("Enter after filling captcha and press login ")
    Login()
    add_rmv_vltd = page.get_by_title("Maker Master").click()

    input("wait")
    browser.close()