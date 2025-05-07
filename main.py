import streamlit as st
import graphviz
import os
from PIL import Image
import base64
from io import BytesIO
#from pyvis.network import Network
import streamlit.components.v1 as components
from ancestrais import ancestrais, formatar_info_ancestral

def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def display_image(file_path):
    if file_path.lower().endswith('.pdf'):
        st.warning("PDF files cannot be displayed directly. Please convert to image format.")
        return
    
    try:
        image = Image.open(file_path)
        st.image(image, use_container_width =True)
    except Exception as e:
        st.error(f"Error displaying image: {str(e)}")

def arvore_com_links_e_imagens():
    # Criar um novo grafo direcionado
    dot = graphviz.Digraph(comment='Árvore Genealógica')
    
    # Configurar o estilo do grafo
    dot.attr(rankdir='TB')  # Top to Bottom
    dot.attr(bgcolor='black')  # Fundo preto
    dot.attr('node', shape='box', style='filled,rounded', fontcolor='black')  # Caixas com cantos arredondados
    dot.attr('edge', dir='none', color='white', penwidth='2')  # Linhas contínuas sem setas
    dot.attr(fontcolor='white')  # Texto branco
    dot.attr(splines='True')  # Linhas com dobras de 90 graus
    
    # Criar nós baseado no dicionário de ancestrais
    for geracao, individuos in ancestrais.items():
        for id_individuo, dados in individuos.items():
            # Definir cor baseada no sexo
            cor = 'lightblue' if dados['sexo'] == 'M' else 'lightpink'
            
            # Criar o nó com as informações formatadas
            dot.node(id_individuo, 
                    f"{dados['nome']}\n({dados['nascimento'].split('/')[-1]})",
                    tooltip=formatar_info_ancestral(dados),
                    fillcolor=cor)
    
    # Adicionar nó invisível para o casal
    dot.node('casal_3', '', shape='point', style='invis')
    dot.node('child_3', '', shape='point', style='invis')
    
    # Adicionar arestas (conexões)
    # Conexão entre gerações
    dot.edge('individuo1', 'individuo2')  # Bisavô -> Avô
    dot.edge('individuo2', 'individuo3_1')  # Avô -> Pai
    
    # Criar subgrafo para a conexão Pai-Mãe-Você
    with dot.subgraph() as s:
        s.attr(rank='same')  # Manter Pai e Mãe no mesmo nível
        s.edge('individuo3_1', 'casal_3')  # Pai -> casal       
        s.edge('casal_3', 'individuo3_2')  # casal -> Mãe
    
    dot.edge('casal_3', 'child_3')
    
    # Conexões para os filhos chegando em cima dos nós
    dot.edge('child_3', 'individuo4_1', constraint='true', headport='n')  # n = north (topo)
    dot.edge('child_3', 'individuo4_2', constraint='true', headport='n')  # n = north (topo)
    dot.edge('child_3', 'individuo4_3', constraint='true', headport='n')  # n = north (topo)
    dot.edge('child_3', 'individuo4_4', constraint='true', headport='n')  # n = north (topo)
    
    # Exibir o grafo no Streamlit
    st.graphviz_chart(dot)

def main():
    st.title("Árvore Genealógica da Família Pohren")
    
    # Criar as abas
    tab1, tab2 = st.tabs(["Árvore Genealógica", "Visualizar Arquivos"])
    
    with tab1:
        arvore_com_links_e_imagens()
    
    with tab2:
        # Listar arquivos na pasta "arquivos"
        arquivos = []
        if os.path.exists("arquivos"):
            arquivos = [f for f in os.listdir("arquivos") if f.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf'))]
        
        if not arquivos:
            st.info("Nenhum arquivo encontrado na pasta 'arquivos'. Adicione arquivos para visualizá-los aqui.")
        else:
            arquivo_selecionado = st.selectbox(
                "Selecione um arquivo para visualizar:",
                arquivos,
                format_func=lambda x: x
            )
            
            if arquivo_selecionado:
                file_path = os.path.join("arquivos", arquivo_selecionado)
                display_image(file_path)

if __name__ == "__main__":
    main()