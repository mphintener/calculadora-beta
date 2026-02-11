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
    .sintese-box { background-color: #E63946; border: 5px solid #FFCC00; padding: 40px; margin-top: 50px; color: #FFFFFF; font-size: 1.4rem; line-height: 1.5; font-weight: 800; border-radius: 15px; text-align: center; box-shadow: 0px 0px 20px rgba(255, 204, 0, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# 1. BASE GEOGRÁFICA MASSIVA (DISTRITOS + RMSP)
geo_db = {
    "São Paulo (Centro)": [-23.5505, -46.6333], "Barra Funda": [-23.5255, -46.6669], "Pinheiros": [-23.5611, -46.7011],
    "Caieiras": [-23.3644, -46.7411], "Franco da Rocha": [-23.3283, -46.7275], "Francisco Morato": [-23.2817, -46.7450],
    "Cajamar": [-23.3569, -46.8764], "Mairiporã": [-23.3186, -46.5867], "Osasco": [-23.5325, -46.7917],
    "Guarulhos": [-23.4542, -46.5333], "Santo André": [-23.6666, -46.5333], "São Bernardo do Campo": [-23.6944, -46.5644],
    "São Caetano do Sul": [-23.6225, -46.5489], "Diadema": [-23.6861, -46.6233], "Mauá": [-23.6678, -46.4614],
    "Barueri": [-23.5112, -46.8761], "Taboão da Serra": [-23.6256, -46.7575], "Carapicuíba": [-23.5233, -46.8350],
    "Itapevi": [-23.5489, -46.9325], "Jandira": [-23.5272, -46.9022], "Grajaú": [-23.7744, -46.6975],
    "Itaquera": [-23.5333, -46.4583], "Guaianases": [-23.5422, -46.4139], "Cidade Tiradentes": [-23.5936, -46.4011],
    "Perus": [-23.4061, -46.7553], "Parelheiros": [-23.8347, -46.7175], "Capão Redondo": [-23.6600, -46.7600]
}
# (Nota: Em produção definitiva, carregaremos todos os 96 distritos aqui)
lista_geo = sorted(list(geo_db.keys()))

st.markdown('<div class="chamada-impacto">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="propisito-app">QTO DO SEU SALÁRIO FICA NO TRANSPORTE?</div>', unsafe_allow_html=True)

with st.form("beta_calc"):
    moradia = st.selectbox("🏠 ONDE VOCÊ MORA?", lista_geo)
    trabalho = st.selectbox("💼 ONDE VOCÊ TRABALHA?", lista_geo)
    
    col1, col2, col3 = st.columns(3)
    with col1: sal = st.number_input("💵 SALÁRIO BRUTO:", min_value=0.0, step=100.0)
    with col2: 
        vida = st.number_input("🏠 CUSTO VIDA:", min_value=0.0, help="Preenchimento Opcional: Gastos fixos (moradia, alimentação, etc) para calcular o Rendimento Real Residual.")
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

    # MAPA COM MARCADORES PULSANTES (GLOW DINÂMICO)
    st.markdown('<div class="secao-titulo">🗺️ MAPEAMENTO DO FLUXO PENDULAR</div>', unsafe_allow_html=True)
    
    line_df = pd.DataFrame([{
        "source": [geo_db[moradia][1], geo_db[moradia][0]],
        "target": [geo_db[trabalho][1], geo_db[trabalho][0]]
    }])
    
    point_df = pd.DataFrame([
        {"pos": [geo_db[moradia][1], geo_db[moradia][0]], "color": [255, 255, 0], "label": "ORIGEM"},
        {"pos": [geo_db[trabalho][1], geo_db[trabalho][0]], "color": [230, 57, 70], "label": "DESTINO"}
    ])

    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=(geo_db[moradia][0] + geo_db[trabalho][0]) / 2,
            longitude=(geo_db[moradia][1] + geo_db[trabalho][1]) / 2,
            zoom=11, pitch=0
        ),
        layers=[
            # A Linha de Conexão (Suavizada)
            pdk.Layer(
                "LineLayer", data=line_df, get_source_position="source", get_target_position="target",
                get_color=[255, 204, 0, 150], get_width=15
            ),
            # O "Glow" Radiante (Círculo de impacto ao redor do ponto)
            pdk.Layer(
                "ScatterplotLayer", data=point_df, get_position="pos", get_color="color",
                get_radius=600, opacity=0.3
            ),
            # O Ponto Núcleo (Marcador sólido)
            pdk.Layer(
                "ScatterplotLayer", data=point_df, get_position="pos", get_color="color",
                get_radius=200, opacity=1
            )
        ]
    ))

    

    # SÍNTESE FINAL
    local_txt = f"por dentro de <b>{moradia}</b>" if moradia == trabalho else f"entre <b>{moradia}</b> e <b>{trabalho}</b>"
    sintese_v = f"<br><br><b>RENDIMENTO RESIDUAL:</b> Após despesas básicas (R$ {vida:,.2f}), restam apenas <span style='color:#FFCC00'>R$ {max(0, sobra_final):.2f}</span> mensais." if vida > 0 else ""

    st.markdown(f"""
        <div class="sintese-box">
            🚨 SÍNTESE DA EXPROPRIAÇÃO ({dias_presenca} DIAS):<br><br>
            Ao se deslocar {local_txt}, você gasta <span style="color:#FFCC00">R$ {custo_t_mensal:,.2f}</span> mensais com transporte e dedica <span style="color:#FFCC00">{h_total_exprop:.0f} horas</span> não remuneradas ao sistema.<br><br>
            O seu <b>VALOR REAL PELA HORA DE TRABALHO PAGA</b> cai para <b>R$ {max(0, v_hora_real):.2f}</b>.{sintese_v}
        </div>
    """, unsafe_allow_html=True)
