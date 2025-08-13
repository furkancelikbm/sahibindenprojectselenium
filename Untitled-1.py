import time
import random
import zipfile
import undetected_chromedriver as uc

# ---------- Proxy ve User Agent Ayarları ----------
ZYTE_API_KEY = "5df0e934e8f04dd398084f7c1d0db3dd"
ZYTE_PROXY = "proxy.zyte.com"
ZYTE_PORT = "8011"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0"
]

# ---------- Proxy Kullanımı (True = Açık, False = Kapalı) ----------
USE_PROXY = True  # 🔹 Proxy'yi kullanmak için True, kapatmak için False yap

# ---------- Proxy Uzantısı Oluştur ----------
def create_proxy_extension(proxy_host, proxy_port, proxy_user="", proxy_pass=""):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": ["proxy", "tabs", "unlimitedStorage", "storage", "<all_urls>", "webRequest", "webRequestBlocking"],
        "background": {"scripts": ["background.js"]}
    }
    """
    background_js = f"""
    var config = {{
        mode: "fixed_servers",
        rules: {{
            singleProxy: {{
                scheme: "http",
                host: "{proxy_host}",
                port: parseInt({proxy_port})
            }},
            bypassList: ["localhost"]
        }}
    }};
    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

    function callbackFn(details) {{
        return {{authCredentials: {{username: "{proxy_user}", password: "{proxy_pass}"}}}};
    }}

    chrome.webRequest.onAuthRequired.addListener(callbackFn, {{urls: ["<all_urls>"]}}, ['blocking']);
    """
    with zipfile.ZipFile("proxy_auth.zip", "w") as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return "proxy_auth.zip"

# ---------- Selenium Driver Oluştur ----------
def create_driver():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    
    if USE_PROXY:
        proxy_extension = create_proxy_extension(ZYTE_PROXY, ZYTE_PORT, ZYTE_API_KEY)
        options.add_extension(proxy_extension)
        print("🛡 Proxy etkinleştirildi")
    else:
        print("❌ Proxy kullanılmıyor")

    driver = uc.Chrome(options=options)
    return driver

# ---------- Ana Fonksiyon ----------
def main():
    driver = create_driver()
    
    try:
        driver.get("https://www.sahibinden.com")
        print("✅ Ana sayfa açıldı")
        time.sleep(random.uniform(3, 7))
        
        driver.get("https://www.sahibinden.com/satilik")
        print("✅ Satılık sayfası açıldı")
        time.sleep(random.uniform(3, 5))
        
        page_html = driver.page_source
        print("📄 Satılık sayfa HTML içeriği (ilk 5000 karakter):\n")
        print(page_html[:5000])
    
    finally:
        driver.quit()
        print("🔒 Tarayıcı kapatıldı")

if __name__ == "__main__":
    main()
