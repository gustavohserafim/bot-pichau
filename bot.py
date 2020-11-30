from selenium import webdriver
from selenium.webdriver.common.by import By
from twilio.rest import Client

def send_whatsapp(nome, preco):
    account_sid = 'ACb311d3c21c97e9c99a7930da30014112'
    auth_token = 'c00e07fc79c615b1a38c3d12072e7229'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='Produto {} com o preço de R$ {} foi encontrado na Pichau.'.format(nome, preco),
        to='whatsapp:+5511942831079')
    print(message.sid)

options = webdriver.ChromeOptions()

prefs = {}
options.add_experimental_option("prefs", prefs)
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)

driver.get("https://www.pichau.com.br/dailydeal/?catid=4")

table = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[1]/div[3]/div/div/div/table")
rows = table.find_elements(By.TAG_NAME, "tr")

lista_produtos = []
lista_precos = []

for row in rows:
    precos = row.find_elements(By.TAG_NAME, "td")[0]
    produtos = row.find_elements(By.TAG_NAME, "td")[1]
    precos_filtrados = precos.text.split("R$")

    if not produtos.text.startswith("APENAS") and not produtos.text.startswith("ÚLTIMAS"):
        produto_atual = produtos.text
        lista_produtos.append(produto_atual)
    if len(precos_filtrados) > 1:
        preco_atual = precos_filtrados[2][:-29].strip()
        lista_precos.append(preco_atual)

ofertas = []

for i, p in enumerate(lista_produtos):
    ofertas.append({"nome": p, "preco": float(lista_precos[i].replace(".", "").replace(",", "."))})

for o in ofertas:
    if "SSD" in o["nome"] and "1TB" in o["nome"] and o["preco"] <= 1000:
        send_whatsapp(o["nome"], o["preco"])

# pprint(lista_produtos)
# pprint(lista_precos)