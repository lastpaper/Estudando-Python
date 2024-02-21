import json
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore


init()
# Abre o arquivo JSON com os links
with open('links.json', 'r') as file:
    links = json.load(file)

print("\n"*20)
print("""

    \tLENIN - MARXITS.ORG
      
      """)
termo_pesquisa = input("[-] Escreva o termo a ser pesquisado: ").lower()

links_encontrados = []


# Faz um loop por cada link
for link in links:
    if link.endswith(".pdf"):
        print(f"{Fore.YELLOW} (PDF) arquivo ignorado: {link}")
        continue
    
    try:
        # Realiza a requisição HTTP para a página
        response = requests.get(link)
        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            html = response.content.decode('utf-8')
            soup = BeautifulSoup(html, "html.parser")

            # Encontrando todo o texto da página
            text = soup.get_text()
            # Convertendo tanto o texto quanto o termo de pesquisa para minúsculas
            text_lower = text.lower()

            # Verificando se o termo de pesquisa está presente no texto
            if termo_pesquisa in text_lower:
                print(f"{Fore.GREEN}\t\"{termo_pesquisa}\" >>>> foi encontrado em: {link}")
                links_encontrados.append(f"{soup.title.string} - {link}")
            else:
                print(f"{Fore.RED}\t\"{termo_pesquisa}\" ---- não foi encontrado em: {link}")
        else:
            print(f"<< STATUS CODE diferente de 200 >>  {link}")
    except Exception as e:
        print(f"Erro ao processar o link {link}: {str(e)}")

print("\n"*5)
print(f"{Fore.LIGHTCYAN_EX} Este foi o resultado da pesquisa '{termo_pesquisa}': \n\n")
for resultado in links_encontrados:
    print(f"[+] {resultado}")
