import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pydeck as pdk

st.set_page_config(page_title="LAB: Calculadora do Trecho", layout="centered")

# CSS: ESTILO TÉCNICO E DE ALTO IMPACTO
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    .stTooltipIcon { filter: invert(1) brightness(5) !important; transform: scale(1.4); }
    .chamada-impacto { background-color: #E63946; color: white; text-align: center; padding: 15px; font-weight: 900; text-transform: uppercase; border: 3px solid #FFCC00; margin-bottom: 25px; font-size: 1.5rem; }
    .propisito-app { color: #FFCC00 !important; font-family: 'Arial Black', sans-serif; font-size: 1.8rem !important; text-align: center; text-transform: uppercase; }
    .secao-titulo { color: #FFCC00 !important; font-size: 1.1rem !important; font-weight: 800; text-transform: uppercase; margin-top: 25px; border-bottom: 2px solid #FFCC00; padding-bottom: 5px; }
    label { color: #FFCC00 !important; font-weight: 700 !important; font-size: 0.9rem !important; }
    .card-res { background-color: #111; border: 1px solid #333; padding: 20px 10px; text-align: center; border-radius: 5px; min-height: 160px; display: flex; flex-direction: column; justify-content: center; }
    .val-res { color: #FFCC00 !important; font-size: 2.2rem !important; font-weight: 900 !important; }
    .label-card { color: #FFFFFF !important; font-size: 0.75rem !important; font-weight: bold; text-transform: uppercase; }
    .sintese-box { background-color: #111; border-left: 10px solid #E63946; padding: 40px; margin-top: 50px; color: #FFFFFF; font-size: 1.4rem; line-height: 1.5; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

# 1. BASE GEOGRÁFICA INTEGRAL (DISTRITOS + RMSP)
geo_db = {
    # DISTRITOS SÃO PAULO
    "São Paulo (Centro)": [-23.5505, -46.6333], "Água Rasa": [-23.559, -46.583], "Alto de Pinheiros": [-23.558, -46.705], 
    "Anhanguera": [-23.434, -46.784], "Aricanduva": [-23.581, -46.511], "Artur Alvim": [-23.535, -46.484], 
    "Barra Funda": [-23.525, -46.666], "Bela Vista": [-23.561, -46.641], "Belém": [-23.542, -46.591], 
    "Bom Retiro": [-23.526, -46.635], "Brasilândia": [-23.463, -46.685], "Butantã": [-23.571, -46.708], 
    "Cachoeirinha": [-23.473, -46.657], "Cambuci": [-23.567, -46.621], "Campo Belo": [-23.628, -46.666], 
    "Campo Grande": [-23.679, -46.689], "Campo Limpo": [-23.647, -46.756], "Cangaíba": [-23.501, -46.521], 
    "Capão Redondo": [-23.660, -46.760], "Carrão": [-23.559, -46.541], "Casa Verde": [-23.507, -46.653], 
    "Cidade Ademar": [-23.675, -46.655], "Cidade Dutra": [-23.708, -46.697], "Cidade Líder": [-23.568, -46.495], 
    "Cidade Tiradentes": [-23.593, -46.401], "Consolação": [-23.554, -46.657], "Ermelino Matarazzo": [-23.495, -46.484], 
    "Freguesia do Ó": [-23.503, -46.699], "Grajaú": [-23.774, -46.697], "Guaianases": [-23.542, -46.413], 
    "Ipiranga": [-23.591, -46.603], "Itaim Bibi": [-23.583, -46.683], "Itaim Paulista": [-23.492, -46.391], 
    "Itaquera": [-23.533, -46.458], "Jabaquara": [-23.645, -46.641], "Jaçanã": [-23.461, -46.594], 
    "Jaguara": [-23.507, -46.755], "Jaguaré": [-23.544, -46.745], "Jaraguá": [-23.447, -46.744], 
    "Jardim Ângela": [-23.717, -46.776], "Jardim Helena": [-23.483, -46.411], "Jardim Paulista": [-23.571, -46.666], 
    "Lapa": [-23.522, -46.702], "Liberdade": [-23.566, -46.635], "Limão": [-23.511, -46.673], 
    "Mandaqui": [-23.475, -46.634], "Marsilac": [-23.896, -46.671], "Moema": [-23.595, -46.661], 
    "Mooca": [-23.553, -46.603], "Morumbi": [-23.591, -46.721], "Parelheiros": [-23.834, -46.717], 
    "Pari": [-23.533, -46.611], "Parque do Carmo": [-23.571, -46.471], "Pedreira": [-23.693, -46.634], 
    "Penha": [-23.521, -46.543], "Perdizes": [-23.535, -46.671], "Perus": [-23.406, -46.755], 
    "Pinheiros": [-23.561, -46.701], "Pirituba": [-23.487, -46.723], "Ponte Rasa": [-23.513, -46.501], 
    "Raposo Tavares": [-23.581, -46.781], "República": [-23.541, -46.643], "Rio Pequeno": [-23.572, -46.757], 
    "Sacomã": [-23.611, -46.591], "Santa Cecília": [-23.535, -46.645], "Santana": [-23.501, -46.623], 
    "Santo Amaro": [-23.647, -46.701], "São Domingos": [-23.491, -46.741], "São Lucas": [-23.589, -46.551], 
    "São Mateus": [-23.601, -46.471], "São Miguel": [-23.491, -46.441], "São Rafael": [-23.611, -46.451], 
    "Sapopemba": [-23.603, -46.513], "Saúde": [-23.611, -46.643], "Sé": [-23.548, -46.633], 
    "Socorro": [-23.691, -46.703], "Tatuapé": [-23.541, -46.571], "Tremembé": [-23.453, -46.611], 
    "Tucuruvi": [-23.483, -46.603], "Vila Andrade": [-23.633, -46.721], "Vila Curuçá": [-23.491, -46.411], 
    "Vila Formosa": [-23.571, -46.551], "Vila Guilherme": [-23.513, -46.591], "Vila Jacuí": [-23.491, -46.461], 
    "Vila Leopoldina": [-23.523, -46.733], "Vila Maria": [-23.515, -46.573], "Vila Mariana": [-23.581, -46.633], 
    "Vila Matilde": [-23.543, -46.521], "Vila Medeiros": [-23.495, -46.581], "Vila Prudente": [-23.585, -46.581], 
    "Vila Sônia": [-23.591, -46.733],
    # MUNICÍPIOS RMSP
    "Arujá": [-23.391, -46.321], "Barueri": [-23.511, -46.876], "Biritiba-Mirim": [-23.571, -45.881], 
    "Caieiras": [-23.364, -46.741], "Cajamar": [-23.356, -46.876], "Carapicuíba": [-23.523, -46.835], 
    "Cotia": [-23.601, -46.911], "Diadema": [-23.686, -46.623], "Embu das Artes": [-23.647, -46.851], 
    "Embu-Guaçu": [-23.831, -46.811], "Ferraz de Vasconcelos": [-23.542, -46.363], "Francisco Morato": [-23.281, -46.745], 
    "Franco da Rocha": [-23.328, -46.727], "Guararema": [-23.411, -46.031], "Guarulhos": [-23.454, -46.533], 
    "Itapecerica da Serra": [-23.711, -46.841], "Itapevi": [-23.548, -46.932], "Itaquaquecetuba": [-23.483, -46.341], 
    "Jandira": [-23.527, -46.902], "Juquitiba": [-23.931, -47.071], "Mairiporã": [-23.318, -46.586], 
    "Mauá": [-23.667, -46.461], "Mogi das Cruzes": [-23.523, -46.187], "Osasco": [-23.532, -46.791], 
    "Pirapora do Bom Jesus": [-23.391, -46.991
