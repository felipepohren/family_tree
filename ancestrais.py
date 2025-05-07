# Dicionário com informações dos ancestrais
# Estrutura: {geração: {nome: {dados}}}

ancestrais = {
    1: {  # Primeira geração (mais antiga)
        "individuo1": {
            "nome": "Frederico Aloysio Pohren",
            "nascimento": "05/03/1891",
            "falecimento": "03/06/1954",
            "sexo": "M",
            "info": "Variações de nome: Frederico Luiz Pohren, Aloysio Pohren"
        }
    },
    2: {  # Segunda geração
        "individuo2": {
            "nome": "Isidorio Reinaldo Pohren",
            "nascimento": "28/01/1933",
            "falecimento": "-",
            "sexo": "M",
            "info": "Residente em Mato Fino"
        }
    },
    3: {  # Terceira geração
        "individuo3_1": {
            "nome": "João Batista pohren",
            "nascimento": "02/11/1962",
            "falecimento": None,  # None se ainda estiver vivo
            "sexo": "M",
            "info": " "
        },
        "individuo3_2": {
            "nome": "Ariane Fischborn Pohren",
            "nascimento": "18/05/1962",
            "falecimento": None,  # None se ainda estiver viva
            "sexo": "F",
            "info": " "
        }
    },
    4: {  # Quarta geração (atual)
        "individuo4_1": {
            "nome": "Felipe Fischborn Pohren",
            "nascimento": "29/02/1984",
            "falecimento": None,
            "sexo": "M",
            "info": " "
        },
        "individuo4_2": {
            "nome": "Natália Fischborn Pohren",
            "nascimento": "08/08/1987",
            "falecimento": None,
            "sexo": "F",
            "info": " "
        },
        
        "individuo4_3": {
            "nome": "Gabriela Fischborn Pohren",
            "nascimento": "23/12/1988",
            "falecimento": None,
            "sexo": "F",
            "info": " "
        },
        
        "individuo4_4": {
            "nome": "Gustavo Fischborn Pohren",
            "nascimento": "31/01/1990",
            "falecimento": None,
            "sexo": "M",
            "info": " "
        }
    }
}

# Função auxiliar para formatar as informações de um ancestral
def formatar_info_ancestral(ancestral):
    info = f"Nome: {ancestral['nome']}\n"
    info += f"Nascimento: {ancestral['nascimento']}\n"
    if ancestral['falecimento']:
        info += f"Falecimento: {ancestral['falecimento']}\n"
    info += f"Sexo: {ancestral['sexo']}\n"
    info += f"\n{ancestral['info']}"
    return info

# Exemplo de uso:
# Para obter informações formatadas de um ancestral:
# info_individuo1 = formatar_info_ancestral(ancestrais[1]["individuo1"]) 