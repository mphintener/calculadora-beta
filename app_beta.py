import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pydeck as pdk

st.set_page_config(page_title="LAB: Calculadora do Trecho", layout="centered")

# CSS: ESTILO DE ALTO IMPACTO E SÍNTESE ENFÁTICA
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    .stTooltipIcon { filter: invert(1) brightness(5) !important; transform: scale(1.4); }
    .chamada-impacto { background-color: #E63946; color: white; text-align: center; padding: 15px; font-weight: 900; text-transform: uppercase; border: 3px solid #FFCC00; margin-bottom: 25px; font-size: 1.5rem; }
    .propisito-app { color: #FFCC00 !important; font-family: 'Arial Black', sans-serif; font-size: 1.8rem !important; text-align: center; text-transform: uppercase; }
    .secao-titulo { color: #FFCC00 !important; font-size: 1.1rem !important; font-weight: 800; text-transform: uppercase; margin-top: 25px; border-bottom: 2px solid #FFCC00; padding-bottom: 5px; }
    label { color: #FFCC00 !important; font-weight: 700 !important; font-size: 0.9rem !important; }
    .card-res { background-color: #111; border: 2px solid #FFCC00; padding: 20px 10px; text-align: center; border-radius: 5px; min-height: 160px; display: flex; flex-direction: column; justify-content: center; }
    .val-res { color: #FFCC00 !important; font-size: 2.2rem !important; font-weight: 900 !important; }
    .label-card { color: #FFFFFF !important; font-size: 0.75rem !important; font-weight: bold; text-transform: uppercase; }
    .sintese-box { background-color: #E63946; border: 5px solid #FFCC00; padding: 40px; margin-top: 50px; color: #FFFFFF; font-size: 1.4rem; line-height: 1.5; font-weight: 800; border-radius: 15px; text-align: center; box-shadow: 0px 0px 20px rgba(255, 204, 0, 0.3); }
    </style>
    """, unsafe_allow_html=True)

# 1. BASE GEOGRÁFICA COMPLETA (DISTRITOS + RMSP)
geo_db = {
    "São Paulo (Centro)": [-23.5505, -46.6333], "Água Rasa": [-23.55, -46.58], "Alto de Pinheiros": [-23.55, -46.70], "Anhanguera": [-23.43, -46.78], "Aricanduva": [-23.58, -46.51], "Artur Alvim": [-23.53, -46.48], "Barra Funda": [-23.5255, -46.6669], "Bela Vista": [-23.56, -46.64], "Belém": [-23.54, -46.59], "Bom Retiro": [-23.52, -46.63], "Brasilândia": [-23.46, -46.68], "Butantã": [-23.57, -46.70], "Cachoeirinha": [-23.47, -46.65], "Cambuci": [-23.56, -46.62], "Campo Belo": [-23.62, -46.66], "Campo Grande": [-23.67, -46.68], "Campo Limpo": [-23.64, -46.75], "Cangaíba": [-23.50, -46.52], "Capão Redondo": [-23.66, -46.76], "Carrão": [-23.55, -46.54], "Casa Verde": [-23.50, -46.65], "Cidade Ademar": [-23.67, -46.65], "Cidade Dutra": [-23.70, -46.69], "Cidade Líder": [-23.56, -46.49], "Cidade Tiradentes": [-23.59, -46.40], "Consolação": [-23.55, -46.65], "Ermelino Matarazzo": [-23.49, -46.48], "Freguesia do Ó": [-23.50, -46.69], "Grajaú": [-23.77, -46.69], "Guaianases": [-23.54, -46.42], "Ipiranga": [-23.59, -46.60], "Itaim Bibi": [-23.58, -46.67], "Itaim Paulista": [-23.49, -46.39], "Itaquera": [-23.53, -46.45], "Jabaquara": [-23.64, -46.64], "Jaçanã": [-23.46, -46.59], "Jaguara": [-23.50, -46.75], "Jaguaré": [-23.54, -46.74], "Jaraguá": [-23.44, -46.74], "Jardim Ângela": [-23.71, -46.77], "Jardim Helena": [-23.48, -46.41], "Jardim Paulista": [-23.57, -46.66], "Lapa": [-23.52, -46.70], "Liberdade": [-23.56, -46.63], "Limão": [-23.51, -46.67], "Mandaqui": [-23.47, -46.63], "Marsilac": [-23.89, -46.67], "Moema": [-23.59, -46.66], "Mooca": [-23.55, -46.60], "Morumbi": [-23.59, -46.72], "Parelheiros": [-23.83, -46.71], "Pari": [-23.53, -46.61], "Parque do Carmo": [-23.57, -46.47], "Pedreira": [-23.69, -46.63], "Penha": [-23.52, -46.54], "Perdizes": [-23.53, -46.67], "Perus": [-23.40, -46.75], "Pinheiros": [-23.5611, -46.7011], "Pirituba": [-23.48, -46.72], "Ponte Rasa": [-23.51, -46.50], "Raposo Tavares": [-23.58, -46.78], "República": [-23.54, -46.64], "Rio Pequeno": [-23.57, -46.75], "Sacomã": [-23.61, -46.59], "Santa Cecília": [-23.53, -46.64], "Santana": [-23.50, -46.62], "Santo Amaro": [-23.64, -46.70], "São Domingos": [-23.49, -46.74], "São Lucas": [-23.58, -46.55], "São Mateus": [-23.60, -46.47], "São Miguel": [-23.49, -46.44], "São Rafael": [-23.61, -46.45], "Sapopemba": [-23.60, -46.51], "Saúde": [-23.61, -46.64], "Sé": [-23.54, -46.63], "Socorro": [-23.69, -46.70], "Tatuapé": [-23.54, -46.57], "Tremembé": [-23.45, -46.61], "Tucuruvi": [-23.48, -46.60], "Vila Andrade": [-23.63, -46.72], "Vila Curuçá": [-23.49, -46.41], "Vila Formosa": [-23.57, -46.55], "Vila Guilherme": [-23.51, -46.59], "Vila Jacuí": [-23.49, -46.46], "Vila Leopoldina": [-23.52, -46.73], "Vila Maria": [-23.51, -46.57], "Vila Mariana": [-23.58, -46.63], "Vila Matilde": [-23.54, -46.52], "Vila Medeiros": [-23.49, -46.58], "Vila Prudente": [-23.58, -46.58], "Vila Sônia": [-23.59, -46.73],
    "Arujá": [-23.39, -46.32], "Barueri": [-23.51, -46.87], "Caieiras": [-23.36, -46.74], "Cajamar": [-23.35, -46.87], "Carapicuíba": [-23.52, -46.83], "Diadema": [-23.68, -46.62], "Franco da Rocha": [-23.32, -46.72], "Guarulhos": [-23.45, -46.53], "Osasco": [-23.53, -46.79], "Santo André": [-23.66, -46.53], "São Bernardo do Campo": [-23.69, -46.56], "São Caetano do Sul": [-23.62, -46.57], "Taboão da Serra": [-23.62, -46.75]
}
lista_geo = sorted(list(geo_db.keys()))

st.markdown('<div class="chamada-impacto">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="propisito-app">QTO DO SEU SALÁRIO FICA NO TRANSPORTE?</div>', unsafe_allow_html=True)

with st.form("beta_calc"):
    moradia = st.selectbox("🏠 ONDE VOCÊ MORA?", lista_geo)
    trabalho = st.selectbox("💼 ONDE VOCÊ TRABALHA?", lista_geo)
    
    col1, col2, col3 = st.columns(3)
    with col1: sal = st.number_input("💵 SALÁRIO BRUTO:", min_value=0.0, step=100.0)
    with col2: vida = st.number_input("🏠 CUSTO VIDA:", min_value=0.0)
    with col3: dias_presenca = st.number_input("📅 DIAS NO TRECHO/MÊS:", min_value=1, max_value=31, value=22)
    
    st.markdown('<div class="secao-titulo">🚌 GASTOS DIÁRIOS (IDA+VOLTA)</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 PÚBLICO (R$)", min_value=0.0)
    with g2: p_app = st.number_input("📱 APP (R$)", min_value=0.0)
    with g3: p_car = st.number_input("🚗 PRIVADO (R$)", min_value=0.0)
    
    st.markdown('<div class="secao-titulo">⏱️ TEMPO DE DESLOCAMENTO</div>', unsafe_allow_html=True)
    h_trecho = st.slider("HORAS NO TRECHO POR DIA (IDA+VOLTA):", 0.5, 12.0, 2.0, step=0.5)
    
    btn = st.form_submit_button("EFETUAR CÁLCULO DE IMPACTO")

if btn and sal > 0:
    h_paga = 176
    custo_t_mensal = (p_pub + p_app + p_car) * dias_presenca
    h_total_exprop = h_trecho * dias_presenca
    v_hora_real = (sal - custo_t_mensal) / (h_paga + h_total_exprop)
    perda = (1 - (v_hora_real / (sal/h_paga))) * 100
    sobra_final = sal - custo_t_mensal - vida

    # CARDS
    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="card-res"><div class="label-card">VALOR REAL PELA<br>HORA DE TRABALHO PAGA</div><div class="val-res">R$ {max(0, v_hora_real):.2f}</div></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="card-res"><div class="label-card">SALÁRIO REAL<br>CONFISCADO</div><div class="val-res">{max(0, perda):.1f}%</div></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="card-res"><div class="label-card">TEMPO DE TRABALHO NÃO PAGO<br>(HORAS/MÊS)</div><div class="val-res">{h_total_exprop:.0f}H</div></div>', unsafe_allow_html=True)

    # MAPA COM FLUXO DINÂMICO (GLOW EFFECT)
    st.markdown('<div class="secao-titulo">🗺️ FLUXO DE EXPROPRIAÇÃO ESPACIAL</div>', unsafe_allow_html=True)
    
    # Criando múltiplas camadas para o efeito "Glow"
    point_data = pd.DataFrame([
        {"pos": [geo_db[moradia][1], geo_db[moradia][0]], "color": [255, 204, 0, 255], "radius": 200},
        {"pos": [geo_db[trabalho][1], geo_db[trabalho][0]], "color": [230, 57, 70, 255], "radius": 200}
    ])

    line_data = pd.DataFrame([{
        "source": [geo_db[moradia][1], geo_db[moradia][0]],
        "target": [geo_db[trabalho][1], geo_db[trabalho][0]]
    }])

    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=(geo_db[moradia][0] + geo_db[trabalho][0]) / 2,
            longitude=(geo_db[moradia][1] + geo_db[trabalho][1]) / 2,
            zoom=11, pitch=0
        ),
        layers=[
            # Linha Principal (O Fluxo)
            pdk.Layer(
                "LineLayer", data=line_data, get_source_position="source", get_target_position="target",
                get_color=[255, 204, 0, 150], get_width=10, highlight_color=[255, 255, 255], picking=True
            ),
            # Brilho Externo (Glow)
            pdk.Layer(
                "ScatterplotLayer", data=point_data, get_position="pos", get_color="color",
                get_radius=500, opacity=0.3
            ),
            # Núcleo do Ponto
            pdk.Layer(
                "ScatterplotLayer", data=point_data, get_position="pos", get_color="color",
                get_radius=200, opacity=1
            )
        ]
    ))

    

    # SÍNTESE
    local_txt = f"por dentro de <b>{moradia}</b>" if moradia == trabalho else f"entre <b>{moradia}</b> e <b>{trabalho}</b>"
    sintese_v = f"<br><br><b>RENDIMENTO RESIDUAL:</b> Após despesas básicas (R$ {vida:,.2f}), restam apenas <span style='color:#FFCC00'>R$ {max(0, sobra_final):.2f}</span> mensais." if vida > 0 else ""

    st.markdown(f"""
        <div class="sintese-box">
            🚨 SÍNTESE DA EXPROPRIAÇÃO ({dias_presenca} DIAS):<br><br>
            Ao se deslocar {local_txt}, você gasta <span style="color:#FFCC00">R$ {custo_t_mensal:,.2f}</span> mensais com transporte e dedica <span style="color:#FFCC00">{h_total_exprop:.0f} horas</span> não remuneradas ao sistema.<br><br>
            O seu <b>VALOR REAL PELA HORA DE TRABALHO PAGA</b> cai para <b>R$ {max(0, v_hora_real):.2f}</b>.{sintese_v}
        </div>
    """, unsafe_allow_html=True)
