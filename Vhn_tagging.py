from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://vahan.parivahan.gov.in/vltdmaker/vahan/welcome.xhtml")
    
    user_id = page.get_by_placeholder("User ID")
    user_id.fill("vltd_gupta")
    pass_fill = page.get_by_placeholder("Password")
    pass_fill.fill("Watsoo@2024")
    input("Enter after login ")
    lgn = page.get_by_role("button", name="Login").click()
    Tag = page.get_by_role("link", name="Add/Remove VLTD").click()
    checkbox = page.get_by_role('radio', name='rb').click()
    input("enter to close")
    # search = page.get_by_role("button", name=)
    browser.close()