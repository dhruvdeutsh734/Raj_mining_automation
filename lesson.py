from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser=p.chromium.launch(headless=False)
    page=browser.new_page()
    page.goto("https://google.com")
    searchbox = page.get_by_role("combobox", name ="Search")
    searchbox.fill("Dhruv kumar bhardwaj")
    # page.locator("textarea").fill("playwright")
    input("Enter to close ")
    
