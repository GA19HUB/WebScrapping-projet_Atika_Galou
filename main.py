from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time
import csv

options = Options()
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option(
    "prefs", {"profile.managed_default_content_settings.media_stream": 2}
)
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1200")
options.add_argument("--start-fullscreen")
options.add_argument("--mute-audio")
options.add_extension("./ublock.crx")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disable-notifications")
options.add_argument(
    "--disable-features=PreloadMediaEngagementData,MediaEngagementBypassAutoplayPolicies"
)
options.add_argument("--autoplay-policy=user-required")

ua = UserAgent()
user_agent = ua.random
options.add_argument(f"user-agent={user_agent}")

monpilote = webdriver.Chrome(options=options)
print("Démarrage de Chrome")

monpilote.get("https://www.amazon.fr/")
print("navigue")

# Cookies
monbouton = WebDriverWait(monpilote, 5).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="sp-cc-accept"]'))
)
time.sleep(0.5)
monbouton.click()
print("cookie cliqué")

# Formulaire de recherche
mazoneRecherche = WebDriverWait(monpilote, 5).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="nav-search-bar-form"]//input'))
)
article = "pantalon"
mazoneRecherche.send_keys(article)
mazoneRecherche.send_keys(Keys.ENTER)
print("recherche lancée")

# Liste globale — un bloc par produit (le [*] généralise)
listGlobale = WebDriverWait(monpilote, 5).until(
    EC.presence_of_all_elements_located(
        (By.XPATH, '//div[@data-component-type="s-search-result"][*]')
    )
)

# Construire la liste de listes appareillée
a = [["Produit", "Prix (€)"]]

for x in listGlobale:
    try:
        info1 = x.find_element(By.XPATH, ".//h2[@aria-label]").get_attribute(
            "aria-label"
        )
    except:
        info1 = "abs"
    try:
        info2 = x.find_element(By.XPATH, './/span[@class="a-price-whole"]').text
    except:
        info2 = "abs"
    r = [info1, info2]
    a.append(r)
    print(len(a), r)

print(a)

# Enregistrer en CSV
fichier = open("amazon_pantalon.csv", "w")
écrivain = csv.writer(fichier, delimiter=",")
écrivain.writerows(a)
fichier.close()

print("Fichier enregistré")
