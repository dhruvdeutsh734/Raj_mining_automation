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
    Tag = page.get_by_text("Tag/Untag VLTD").click()
    add_remove = page.get_by_text("Add/Remove VLTD")
    add_remove.wait_for(state="visible", timeout=5000)
    add_remove.click()
    # checkbox = page.get_by_role('radio', name='rb').check()
    radio_wrapper = page.locator('div.ui-radiobutton').filter(
    has=page.locator('input[value="A"]')) 
    radio_wrapper.locator('.ui-radiobutton-box').click()
    input("wait")

    select_vltd_maker = page.get_by_text("Select VLTD Maker").click()
    wat_exp = page.get_by_role('option',name="WATSOO EXPRESS PVT LTD").click()
    input("wait")
    select_vltd_model = page.get_by_text("Select VLTD Model").click()
    model= input("Enter 2g or 4g").upper()
    if (model=="2G"):
        Model_2g= page.get_by_role('option',name="PRITHIVI 140").click()
    else:
        Model_4g= page.get_by_role('option',name="PRITHVI 140 4G").click()

    input("enter to close")
    # search = page.get_by_role("button", name=)
    browser.close()