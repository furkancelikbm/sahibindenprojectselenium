import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# --- Ayarlar ---
# Tarayıcıyı arka planda çalıştırır. (Daha hızlı ve görünmezdir.)
HEADLESS = True

# --- WebDriver Oluşturma Fonksiyonu ---
def create_undetected_driver():
    """
    Bot algılama sistemlerini atlamak için özel olarak yapılandırılmış
    undetected_chromedriver örneği oluşturur.
    """
    options = uc.ChromeOptions()
    
    if HEADLESS:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
    
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # En stabil versiyonu kullanır ve bot algılamayı atlar.
    driver = uc.Chrome(options=options)
    
    # JavaScript ile 'webdriver' özelliğini gizleyerek bot izlerini silme.
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
        },
    )
    
    return driver

# --- İlan Bilgilerini Çekme Fonksiyonu ---
def get_property_listings(driver):
    """
    Sayfadaki emlak ilanlarını bulur, başlık ve fiyat bilgilerini ekrana yazdırır.
    """
    try:
        print("⏳ İlan listesinin yüklenmesi bekleniyor...")
        # İlan kartlarını belirten CSS seçicisi ile tüm ilanları bul.
        listings = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.styles_listingWrapper__I0H_l > div[data-index]"))
        )
        print(f"✅ Sayfada {len(listings)} adet ilan bulundu.")
        
        for i, listing in enumerate(listings, 1):
            # Proje ilanları, normal ilanlardan farklıdır ve atlanır.
            if "styles_projectBadgeCard__JTaKm" in listing.get_attribute("innerHTML"):
                continue

            try:
                # Başlık ve fiyat elementlerini bulun ve metinlerini alın.
                title = listing.find_element(By.CSS_SELECTOR, "h3.styles_title__CN_n3").text.strip()
                price = listing.find_element(By.CSS_SELECTOR, "span.styles_price__8Z_OS").text.strip()
                
                print(f"📌 İlan {i}: {title} | Fiyat: {price}")
            except NoSuchElementException:
                print(f"❗ İlan {i} için başlık veya fiyat bilgisi alınamadı, atlanıyor.")
                continue
    except TimeoutException:
        print("❌ İlanlar 20 saniye içinde yüklenemedi. Program sonlandırılıyor.")
    except Exception as e:
        print(f"❌ İlanları çekerken beklenmedik bir hata oluştu: {e}")

# --- Ana Program Akışı ---
def main():
    driver = None
    try:
        driver = create_undetected_driver()
        
        # Doğrudan satılık konutlar sayfasına git.
        print("✅ Emlakjet.com'a gidiliyor...")
        driver.get("https://www.emlakjet.com/satilik-konut")

        # Çerez pop-up'ını kapat (eğer varsa).
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            ).click()
            print("✅ Çerez bildirimi kapatıldı.")
        except TimeoutException:
            print("❗ Çerez bildirimi bulunamadı veya kendiliğinden kapandı. Devam ediliyor.")
        
        # İlanları çekme fonksiyonunu çağır.
        get_property_listings(driver)

    except WebDriverException as e:
        print(f"❌ WebDriver hatası oluştu: {e}")
    except Exception as e:
        print(f"❌ Programın ana akışında beklenmedik bir hata oluştu: {e}")
    finally:
        if driver:
            driver.quit()
            print("🔒 Tarayıcı başarıyla kapatıldı.")

if __name__ == "__main__":
    main()