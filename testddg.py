from duckduckgo_search import DDGS

# Definir User-Agent para a requisição
with DDGS(headers={"User-Agent": "Mozilla/5.0"}) as ddgs:
    results = ddgs.text("python programming")
    resultados_lista = list(results)
    for resultado in resultados_lista:
        print(resultado)