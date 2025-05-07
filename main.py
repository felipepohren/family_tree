import streamlit as st
import graphviz
from streamlit_image_zoom import image_zoom
import os
from PIL import Image
import base64
from io import BytesIO
#from pyvis.network import Network
import streamlit.components.v1 as components
from ancestrais import ancestrais, formatar_info_ancestral

version = '1.01'

def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def display_image(file_path):
    if file_path.lower().endswith('.pdf'):
        st.warning("PDF files cannot be displayed directly. Please convert to image format.")
        return
    
    try:
        with Image.open(file_path) as img:
            st.image(img, use_container_width =True)
        
        #with Image.open(file_path) as img:
        #   image_zoom(img, zoom_factor=5, mode="both",keep_resolution = True)  # zoom com mouse e scroll
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
                    fillcolor=cor,
                    image = "flags/ger_bra.jpg")
    
    # Adicionar nó invisível para o casal

    dot.node('child_1', '', shape='point', style='invis')

    
    # Adicionar arestas (conexões)
    # Conexão entre gerações
   
   #heptavo
    with dot.subgraph() as s:
        s.attr(rank='same')  # Manter Pai e Mãe no mesmo nível
        s.edge('heptavo', 'heptavoh')  # Pai -> casal  
    dot.edge('heptavo', 'hexavo')  # Avô -> Pai
   #hexavo
   
    with dot.subgraph() as s:
        s.attr(rank='same')  # Manter Pai e Mãe no mesmo nível
        s.edge('hexavo', 'hexavoh')  # Pai -> casal  
    dot.edge('hexavo', 'pentavo')  # Avô -> Pai
   #pentavo

    with dot.subgraph() as s:
        s.attr(rank='same')  # Manter Pai e Mãe no mesmo nível
        s.edge('pentavo', 'pentavoh')  # Pai -> casal  
    dot.edge('pentavo', 'tetravo')  # Avô -> Pai
   #tataravo

    with dot.subgraph() as s:
        s.attr(rank='same')  # Manter Pai e Mãe no mesmo nível
        s.edge('tetravo', 'tetravoh')  # Pai -> casal  
    dot.edge('tetravo', 'trisavo')  # Avô -> Pai
   #Trizavo 

    with dot.subgraph() as s:
        s.attr(rank='same')  # Manter Pai e Mãe no mesmo nível
        s.edge('trisavo', 'trisavoh')  # Pai -> casal  
    dot.edge('trisavo', 'bizavo')  # Avô -> Pai
   #bizavo
    with dot.subgraph() as s:
        s.attr(rank='same')  # Manter Pai e Mãe no mesmo nível
        s.edge('bizavo', 'bisavoh')  # Pai -> casal    
    dot.edge('bizavo', 'avo')  # Avô -> Pai

    
    with dot.subgraph() as s:
        s.attr(rank='same')  # Manter Pai e Mãe no mesmo nível
        s.edge('avo', 'avoh')  # Pai -> casal              
    dot.edge('avo', 'pai')  # Avô -> Pai
    # Criar subgrafo para a conexão Pai-Mãe-Você
    with dot.subgraph() as s:
        s.attr(rank='same')  # Manter Pai e Mãe no mesmo nível
        s.edge('pai', 'mae')  # Pai -> casal       
        #s.edge('pai', 'casal_1')  # Pai -> casal       
        #s.edge('casal_1', 'mae')  # casal -> Mãe
    
    dot.edge('pai', 'child_1')
    
    # Conexões para os filhos chegando em cima dos nós
    dot.edge('child_1', 'eu', constraint='true', headport='n')  # n = north (topo)
    dot.edge('child_1', 'irmao_1', constraint='true', headport='n')  # n = north (topo)
    dot.edge('child_1', 'irmao_2', constraint='true', headport='n')  # n = north (topo)
    dot.edge('child_1', 'irmao_3', constraint='true', headport='n')  # n = north (topo)
    
    # Exibir o grafo no Streamlit
    st.graphviz_chart(dot,use_container_width = True)
    

def main():
    st.title("Família Pohren")
    
    # Criar as abas
    tab1, tab2, tab3 = st.tabs(["Árvore Genealógica", "Imigração","Registros Históricos"])
    
    with tab1:
        st.markdown("[Arvore completa](https://www.familysearch.org/en/tree/pedigree/portrait/PSZH-YDG)")
        arvore_com_links_e_imagens()
        st.markdown("---")  # Linha horizontal
        st.markdown("### Fontes:")        
        st.markdown("1. [familysearch](https://www.familysearch.org)")
        st.markdown("2. [geni](https://www.geni.com/home)")
        st.markdown("3. [geneanet](https://pt.geneanet.org)")
        st.markdown("---")  # Linha horizontal
        st.write("By: Felipe Fischborn pohren")
        st.write(f"version {version}")

    with tab2:
        st.markdown("""- O navio Olbers trouxe o maior número de imigrantes alemães numa viagem
transatlântica para o Brasil.\n
- O veleiro Olbers também foi o maior dos navios que até aquela data haviam
efetuado o transporte de imigrantes ao Brasil.\n
- O Olbers partiu do porto de Bremen sob o comando do Capitão Gerard Clausen (segundo Hunsche) no dia 03/10/1828
(no dia 26/09/1828 de Bremenhaven, segundo Mathias Franzen) e chegou ao Rio de \
Janeiro em 17/12/1828, em 75 dias.
- Navio especialmente preparado para o transporte de pessoas, transportou 874 passageiros, entre eles muitas famílias \
que se radicaram na Colônia Alemã de São Leopoldo no Rio Grande do Sul (Hunsche, Quadriênio).""")
    
    with tab3:
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
                
                # Link de download com o nome do arquivo especificado
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="📥 Baixar imagem",
                        data=f,
                        file_name=arquivo_selecionado,
                        mime="image/png"
                    )
                display_image(file_path)
                
    
                
               # with Image.open(file_path) as img:
               #     image_zoom(img, mode="scroll",increment=0.5)
                

if __name__ == "__main__":
    main()