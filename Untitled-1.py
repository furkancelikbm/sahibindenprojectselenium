import undetected_chromedriver as uc
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def create_undetected_driver():
    """Undetected Chrome driver oluştur"""
    options = uc.ChromeOptions()
    
    # Temel ayarlar
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Gerçek kullanıcı simülasyonu
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    try:
        driver = uc.Chrome(options=options, version_main=None)
        
        # Rastgele viewport boyutu
        sizes = [(1920, 1080), (1366, 768), (1536, 864)]
        width, height = random.choice(sizes)
        driver.set_window_size(width, height)
        
        print(f"✅ Undetected Chrome başlatıldı ({width}x{height})")
        return driver
        
    except Exception as e:
        print(f"❌ Undetected Chrome başlatılamadı: {e}")
        return None

def human_behavior(driver):
    """İnsan benzeri davranış"""
    try:
        # Rastgele mouse hareketleri
        actions = ActionChains(driver)
        for _ in range(random.randint(2, 4)):
            x_offset = random.randint(-100, 100)
            y_offset = random.randint(-100, 100)
            actions.move_by_offset(x_offset, y_offset).perform()
            time.sleep(random.uniform(0.5, 1.5))
        
        # Rastgele scroll
        for _ in range(random.randint(1, 3)):
            scroll_amount = random.randint(-300, 300)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
            time.sleep(random.uniform(1, 2))
            
    except Exception as e:
        print(f"Davranış simülasyonu hatası: {e}")

def main_undetected():
    """Ana fonksiyon - Undetected Chrome"""
    print("🔧 Undetected Chrome Driver ile deneme...")
    
    driver = create_undetected_driver()
    if not driver:
        return
    
    try:
        urls = [
            "https://www.sahibinden.com/",
            "https://www.sahibinden.com/kategori/emlak",
            "https://www.sahibinden.com/satilik-daire"
        ]
        
        for url in urls:
            print(f"\n🎯 Deneniyor: {url}")
            driver.get(url)
            
            # İnsan benzeri bekleme
            time.sleep(random.uniform(3, 7))
            
            # İnsan davranışı simülasyonu
            human_behavior(driver)
            
            # Sayfa başlığı kontrol
            title = driver.title
            print(f"📄 Başlık: {title}")
            
            if "Just a moment" not in title and "sahibinden" in driver.current_url:
                print("✅ Başarıyla erişildi!")
                
                # Kısa bir analiz
                body_text = driver.find_element(By.TAG_NAME, "body").text
                print(f"📊 Sayfa içerik uzunluğu: {len(body_text)} karakter")
                
                # İlan arama
                try:
                    listings = driver.find_elements(By.XPATH, "//a[contains(@href, '/ilan/')]")
                    print(f"🏠 Bulunan ilan linki: {len(listings)} adet")
                except:
                    print("🔍 İlan araması yapılamadı")
                
                input("\n📝 İncelemek için Enter'a basın...")
                break
            else:
                print("❌ Cloudflare bypass yapılamadı")
        
    except Exception as e:
        print(f"💥 Hata: {e}")
    
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    main_undetected()