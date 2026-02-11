import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pydeck as pdk

st.set_page_config(page_title="LAB: Calculadora do Trecho", layout="centered")

# CSS: IDENTIDADE VISUAL MANTIDA
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    .stTooltipIcon { filter: invert(1) brightness(5) !important; transform: scale(1.4); }
    .chamada-impacto { background-color: #E63946; color: white; text-align: center; padding: 12px; font-weight: 900; text-transform: uppercase; border: 2px solid #FFCC00; margin-bottom: 20px; }
    .propisito-app { color: #FFCC00 !important; font-family: 'Arial Black', sans-serif; font-size: 1.8rem !important; text-align: center; text-transform: uppercase; margin-bottom: 5px; }
    .secao-titulo { color: #FFCC00 !important; font-size: 1.1rem !important; font-weight: 800; text-transform: uppercase; margin-top: 25px; border-bottom: 2px solid #FFCC00; padding-bottom: 5px; }
    label { color: #FFCC00 !important; font-weight: 700 !important; font-size: 0.9rem !important; }
    .card-res { background-color: #111; border: 2px solid #FFCC00; padding: 20px 10px; text-align: center; border-radius: 5px; min-height: 140px; }
    .val-res { color: #FFCC00 !important; font-size: 1.8rem !important; font-weight: 900 !important; }
    .label-card { color: #FFFFFF !important; font-size: 0.65rem !important; font-weight: bold; text-transform: uppercase; }
    .sintese-box { background-color: #111; border-left: 10px solid #E63946; padding: 25px; margin-top: 30px; color: #FFFFFF; font-size: 1.1rem; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# BASE DE DADOS GEO (DISTRITOS + MUNICÍPIOS)
geo_db = {
    "São Paulo (Centro)": [-23.5505, -46.6333], "Caieiras": [-23.3644, -46.7411], 
    "Franco da Rocha": [-23.3283, -46.7275], "Grajaú": [-23.7744, -46.6975], 
    "Itaquera": [-23.5333, -46.4583], "Osasco": [-23.5325, -46.7917], 
    "Guarulhos": [-23.4542, -46.5333], "Santo André": [-23.6666, -46.5333], 
    "São Bernardo": [-23.6944, -46.5644], "Barueri": [-23.5112, -46.8761], 
    "Cajamar": [-23.3569, -46.8764], "Mogi das Cruzes": [-23.5235, -46.1878],
    "Perus": [-23.4000, -46.7500], "Lapa": [-23.5222, -46.7028], 
    "Pinheiros": [-23.5611, -46.7011], "Capão Redondo": [-23.6600, -46.7600]
}
lista_geo = sorted(list(geo_db.keys()))

st.markdown('<div class="chamada-impacto">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="propisito-app">QTO DO SEU SALÁRIO FICA NO TRANSPORTE?</div>', unsafe_allow_html=True)

with st.form("beta_calc"):
    moradia = st.selectbox("🏠 ONDE VOCÊ MORA?", lista_geo)
    trabalho = st.selectbox("💼 ONDE VOCÊ TRABALHA?", lista_geo)
    
    col1, col2, col3 = st.columns(3)
    with col1: sal = st.number_input("💵 SALÁRIO BRUTO:", min_value=0.0, step=100.0)
    with col2: vida = st.number_input("🏠 CUSTO VIDA:", min_value=0.0, help="Preenchimento Opcional: Moradia, alimentação e contas fixas.")
    with col3: dias_presenca = st.number_input("📅 DIAS NO TRECHO/MÊS:", min_value=1, max_value=31, value=22)
    
    st.markdown('<div class="secao-titulo">🚌 GASTOS DIÁRIOS (IDA+VOLTA)</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1: p_pub = st.number_input("🚆 PÚBLICO (R$)", min_value=0.0)
    with g2: p_app = st.number_input("📱 APP (R$)", min_value=0.0)
    with g3: p_car = st.number_input("🚗 PRIVADO (R$)", min_value=0.0)
    
    st.markdown('<div class="secao-titulo">⏱️ TEMPO DE DESLOCAMENTO</div>', unsafe_allow_html=True)
    h_trecho = st.slider("TOTAL DE HORAS NO TRECHO POR DIA:", 0.5, 12.0, 2.0, step=0.5)
    
    btn = st.form_submit_button("EFETUAR CÁLCULO AVANÇADO")

if btn and sal > 0:
    h_paga = 176
    custo_t = (p_pub + p_app + p_car) * dias_presenca
    h_total_exprop = h_trecho * dias_presenca
    v_hora_real = (sal - custo_t) / (h_paga + h_total_exprop)
    perda = (1 - (v_hora_real / (sal/h_paga))) * 100
    sobra_final = sal - custo_t - vida

    # RESULTADOS
    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="card-res"><div class="label-card">VALOR REAL PELA<br>HORA DE TRABALHO PAGA</div><div class="val-res">R$ {max(0, v_hora_real):.2f}</div></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="card-res"><div class="label-card">SALÁRIO REAL<br>CONFISCADO</div><div class="val-res">{max(0, perda):.1f}%</div></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="card-res"><div class="label-card">TEMPO DE TRABALHO NÃO PAGO<br>(HORAS/MÊS)</div><div class="val-res">{h_total_exprop:.0f}H</div></div>', unsafe_allow_html=True)

    # VISUALIZAÇÃO PYDECK (ARCO 3D)
    st.markdown('<div class="secao-titulo">🗺️ ARCO DE EXPROPRIAÇÃO ESPACIAL</div>', unsafe_allow_html=True)
    
    arc_data = pd.DataFrame([{
        "start_lat": geo_db[moradia][0], "start_lon": geo_db[moradia][1],
        "end_lat": geo_db[trabalho][0], "end_lon": geo_db[trabalho][1],
        "name": "Fluxo de Trabalho"
    }])

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v9',
        initial_view_state=pdk.ViewState(
            latitude=geo_db[moradia][0], longitude=geo_db[moradia][1],
            zoom=10, pitch=45,
        ),
        layers=[
            pdk.Layer(
                "ArcLayer", data=arc_data, get_source_position=["start_lon", "start_lat"],
                get_target_position=["end_lon", "end_lat"],
                get_source_color=[255, 204, 0], get_target_color=[230, 57, 70],
                get_width=5,
            ),
        ],
    ))

    # GRÁFICO (MANTIDO)
    st.markdown('<div class="secao-titulo">📊 ANÁLISE DA EXPROPRIAÇÃO DO TEMPO</div>', unsafe_allow_html=True)
    fig = go.Figure(data=[go.Pie(labels=['Tempo Remunerado', 'Tempo de Trajeto'], values=[h_paga, h_total_exprop], hole=.4, marker_colors=['#FFCC00', '#E63946'], textinfo='percent+label')])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white', height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    local_txt = f"por dentro de <b>{moradia}</b>" if moradia == trabalho else f"entre <b>{moradia}</b> e <b>{trabalho}</b>"
    sintese_v = f"<br><br><b>RENDIMENTO RESIDUAL:</b> Após o custo de vida (R$ {vida:,.2f}), restam apenas <span style='color:#FFCC00'>R$ {max(0, sobra_final):.2f}</span> mensais." if vida > 0 else ""

    st.markdown(f"""
        <div class="sintese-box">
            <b>SÍNTESE DA EXPROPRIAÇÃO ({dias_presenca} DIAS):</b><br>
            Ao se deslocar {local_txt}, você dedica <span style="color:#FFCC00">{h_total_exprop:.0f} horas</span> mensais não remuneradas ao sistema. 
            Na prática, seu <b>valor real pela hora de trabalho paga</b> é de <b>R$ {max(0, v_hora_real):.2f}</b>.{sintese_v}
        </div>
    """, unsafe_allow_html=True)
