import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException

# ---------- Ayarlar ----------
HEADLESS = False  # True: Başsız (arka planda), False: Görünür
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
]

# ---------- Driver Oluştur ----------
def create_driver():
    """
    Cloudflare'ı aşmak için optimize edilmiş, en güncel ayarlarla
    undetected_chromedriver'ı oluşturur.
    """
    options = uc.ChromeOptions()

    if HEADLESS:
        # Modern headless mod, eski metoda göre daha az tespit edilebilir.
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu") # Headless mod için gereklidir.
        options.add_argument("--window-size=1920,1080") # Ekran boyutunu belirlemek bot tespitini zorlaştırır.
        options.add_argument("--no-sandbox")

    # Bot tespitini önlemek için standart ve etkili argümanlar
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")

    # `uc.Chrome` başlatılırken spesifik bir Chrome versiyonu belirtmek stabiliteyi artırabilir.
    # Sisteminizdeki Chrome sürümü 139 olduğu için bu değeri kullandık.
    driver = uc.Chrome(options=options, version_main=139)

    # `navigator.webdriver` flag'ini gizlemek, en önemli bypass tekniklerinden biridir.
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        },
    )
    
    return driver

# ---------- İnsan Davranışı Simülasyonu ----------
def simulate_human_behavior(driver):
    """
    Sayfa üzerinde rastgele kaydırma ve fare hareketleri yaparak
    insan davranışını taklit eder. Riskli tıklamalardan kaçınır.
    """
    actions = ActionChains(driver)
    try:
        # 1. Yavaş ve rastgele kaydırma
        for _ in range(random.randint(1, 3)):
            scroll_amount = random.randint(200, 500)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.5, 1.5))

        # 2. Fareyi sayfanın farklı bölgelerine hareket ettirme
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(random.randint(2, 4)):
            x_offset = random.randint(1, driver.execute_script("return window.innerWidth;") -1)
            y_offset = random.randint(1, driver.execute_script("return window.innerHeight;") -1)
            actions.move_to_element_with_offset(body, x_offset, y_offset).pause(random.uniform(0.4, 1.2)).perform()
    except Exception as e:
        print(f"⚠️ İnsan simülasyonu sırasında bir hata oluştu: {e}")

# ---------- Ana Fonksiyon ----------
def main():
    driver = None
    try:
        driver = create_driver()

        # 1️⃣ Ana sayfa ve Cloudflare Doğrulaması
        print("✅ Ana sayfa açılıyor...")
        driver.get("https://www.sahibinden.com")

        try:
            print("⏳ Cloudflare doğrulaması bekleniyor...")
            wait = WebDriverWait(driver, 45) # Bekleme süresini 45 saniyeye çıkardık.
            wait.until(EC.presence_of_element_located((By.ID, "searchText")))
            print("✅ Cloudflare başarıyla aşıldı!")
        except TimeoutException:
            print("❌ Cloudflare 45 saniye içinde aşılamadı. Sayfa kaynağı kontrol ediliyor...")
            if "captcha" in driver.page_source.lower():
                print("❌ CAPTCHA tespit edildi. Headless modda bu aşılamaz. Kod durduruluyor.")
                return
            else:
                 print("⚠️ Sayfa yüklenemedi ancak CAPTCHA da yok. Devam ediliyor...")

        simulate_human_behavior(driver)
        time.sleep(random.uniform(2, 4))

        # 2️⃣ Satılık ilanlar
        print("✅ Satılık sayfasına gidiliyor...")
        driver.get("https://www.sahibinden.com/satilik")

        # İlan listesinin yüklenmesini bekle
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr.searchResultsItem")))
        print("✅ Satılık sayfası başarıyla açıldı.")

        simulate_human_behavior(driver)
        time.sleep(random.uniform(2, 5))

        # 3️⃣ İlan başlıkları ve fiyatlar
        listings = driver.find_elements(By.CSS_SELECTOR, "tr.searchResultsItem")

        if not listings:
            print("❗ Herhangi bir ilan bulunamadı.")
            return

        print(f"✅ Toplam {len(listings)} adet ilan bulundu.")
        for i, listing in enumerate(listings, 1):
            try:
                title = listing.find_element(By.CSS_SELECTOR, "a.classifiedTitle").text.strip()
                price = listing.find_element(By.CSS_SELECTOR, "td.searchResultsPriceValue span").text.strip()
                print(f"📌 İlan {i}: {title} | Fiyat: {price}")
            except Exception as e:
                print(f"❗ Bir ilan bilgisi alınırken hata oluştu: {e}")
                continue

    except Exception as e:
        print(f"❌ Program ana akışında beklenmedik bir hata oluştu: {e}")
    finally:
        if driver:
            driver.quit()
            print("🔒 Tarayıcı başarıyla kapatıldı.")

if __name__ == "__main__":
    main()