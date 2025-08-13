import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium_stealth import stealth

# ---------- Ayarlar ----------
HEADLESS = False  # False yaparsan tarayıcı görünür çalışır
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0"
]

# ---------- Driver Oluştur ----------
def create_driver():
    options = uc.ChromeOptions()

    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")

    driver = uc.Chrome(options=options)

    # Selenium Stealth ile tespit önleme
    stealth(
        driver,
        languages=["tr-TR", "tr"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True
    )

    return driver

# ---------- Ana Fonksiyon ----------
def main():
    driver = create_driver()
    
    try:
        # 1️⃣ Ana sayfa
        driver.get("https://www.sahibinden.com")
        print("✅ Ana sayfa açıldı")

        # Cloudflare doğrulama ekranı varsa bekle
        while "cf-browser-verification" in driver.page_source or "Just a moment..." in driver.page_source:
            print("⏳ Cloudflare doğrulaması bekleniyor...")
            time.sleep(1)

        time.sleep(random.uniform(8, 12))  # Ek bekleme

        # 2️⃣ Satılık ilanlar
        driver.get("https://www.sahibinden.com/satilik")
        print("✅ Satılık sayfası açıldı")
        time.sleep(random.uniform(5, 8))

        # 3️⃣ İlan başlıkları ve fiyatlar
        listings = driver.find_elements(By.CSS_SELECTOR, "tr.searchResultsItem")
        for listing in listings:
            try:
                title = listing.find_element(By.CSS_SELECTOR, "a.classifiedTitle").text.strip()
                price = listing.find_element(By.CSS_SELECTOR, "td.searchResultsPriceValue span").text.strip()
                print(f"📌 Başlık: {title} | Fiyat: {price}")
            except:
                continue

    finally:
        driver.quit()
        print("🔒 Tarayıcı kapatıldı")

if __name__ == "__main__":
    main()
