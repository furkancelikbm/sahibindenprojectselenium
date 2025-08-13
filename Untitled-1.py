import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# ---------- User Agent Ayarları ----------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0"
]

# ---------- Selenium Driver Oluştur ----------
def create_driver():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    driver = uc.Chrome(options=options)
    return driver

# ---------- Ana Fonksiyon ----------
def main():
    driver = create_driver()
    
    try:
        # 1️⃣ Ana sayfaya git ve doğrulama için bekle
        driver.get("https://www.sahibinden.com")
        print("✅ Ana sayfa açıldı")
        time.sleep(random.uniform(3, 6))  # Sayfanın tamamen yüklenmesi için bekle

        # 2️⃣ Satılık ilanlar sayfasına git
        driver.get("https://www.sahibinden.com/satilik")
        print("✅ Satılık sayfası açıldı")
        time.sleep(random.uniform(3, 6))

        # 3️⃣ İlan başlıklarını ve fiyatlarını çek
        listings = driver.find_elements(By.CSS_SELECTOR, "tr.searchResultsItem")
        for listing in listings:
            try:
                title = listing.find_element(By.CSS_SELECTOR, "a.classifiedTitle").text
                price = listing.find_element(By.CSS_SELECTOR, "td.searchResultsPriceValue span").text
                print(f"📌 Başlık: {title} | Fiyat: {price}")
            except:
                continue

    finally:
        driver.quit()
        print("🔒 Tarayıcı kapatıldı")

if __name__ == "__main__":
    main()
