import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="LAB: Calculadora do Trecho", layout="centered")

# Mantendo a Identidade Visual de Alto Contraste
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    .stTooltipIcon { filter: invert(1) brightness(5) !important; transform: scale(1.4); }
    .chamada-impacto { background-color: #E63946; color: white; text-align: center; padding: 12px; font-weight: 900; text-transform: uppercase; border: 2px solid #FFCC00; margin-bottom: 20px; }
    .propisito-app { color: #FFCC00 !important; font-family: 'Arial Black', sans-serif; font-size: 1.8rem !important; text-align: center; text-transform: uppercase; margin-bottom: 5px; }
    .secao-titulo { color: #FFCC00 !important; font-size: 1.1rem !important; font-weight: 800; text-transform: uppercase; margin-top: 25px; border-bottom: 2px solid #FFCC00; padding-bottom: 5px; }
    label { color: #FFCC00 !important; font-weight: 700 !important; font-size: 0.9rem !important; }
    .card-res { background-color: #111; border: 2px solid #FFCC00; padding: 20px 10px; text-align: center; border-radius: 5px; }
    .val-res { color: #FFCC00 !important; font-size: 1.8rem !important; font-weight: 900 !important; }
    .label-card { color: #FFFFFF !important; font-size: 0.75rem !important; font-weight: bold; text-transform: uppercase; }
    .sintese-box { background-color: #111; border-left: 10px solid #E63946; padding: 25px; margin-top: 30px; color: #FFFFFF; font-size: 1.1rem; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# Coordenadas Básicas para Teste do Mapa (LAB)
coords = {
    "Caieiras": [-23.3644, -46.7411],
    "Franco da Rocha": [-23.3283, -46.7275],
    "São Paulo (Centro)": [-23.5505, -46.6333],
    "Grajaú": [-23.7744, -46.6975],
    "Itaquera": [-23.5333, -46.4583],
    "Osasco": [-23.5325, -46.7917],
    "Guarulhos": [-23.4542, -46.5333]
}
lista_geo = sorted(list(coords.keys()))

st.markdown('<div class="chamada-impacto">LABORATÓRIO DE TESTES - VERSÃO BETA</div>', unsafe_allow_html=True)
st.markdown('<div class="propisito-app">MODELAGEM DE IMPACTO GEOGRÁFICO</div>', unsafe_allow_html=True)

with st.form("beta_calc"):
    moradia = st.selectbox("🏠 ONDE VOCÊ MORA?", lista_geo)
    trabalho = st.selectbox("💼 ONDE VOCÊ TRABALHA?", lista_geo)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        sal = st.number_input("💵 SALÁRIO BRUTO:", min_value=0.0, step=100.0)
    with col2:
        vida = st.number_input("🏠 CUSTO VIDA:", min_value=0.0)
    with col3:
        # ATENDENDO À SUGESTÃO: TRABALHO HÍBRIDO
        dias_trecho = st.number_input("📅 DIAS NO TRECHO/MÊS:", min_value=1, max_value=31, value=22, help="Quantos dias por mês você efetivamente faz o trajeto?")
    
    st.markdown('<div class="secao-titulo">🚌 GASTOS E TEMPO NO TRECHO</div>', unsafe_allow_html=True)
    gasto_dia = st.number_input("GASTO TOTAL DIÁRIO (IDA+VOLTA R$):", min_value=0.0)
    h_trecho = st.slider("TOTAL DE HORAS NO TRECHO POR DIA:", 0.5, 12.0, 2.0, step=0.5)
    
    btn = st.form_submit_button("SIMULAR IMPACTO NO LAB")

if btn and sal > 0:
    h_paga_mes = 176
    custo_t_total = gasto_dia * dias_trecho
    h_total_exprop = h_trecho * dias_trecho
    
    v_hora_real = (sal - custo_t_total) / (h_paga_mes + h_total_exprop)
    perda = (1 - (v_hora_real / (sal/h_paga_mes))) * 100
    sobra_final = sal - custo_t_total - vida

    # RESULTADOS EM CARDS
    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="card-res"><div class="label-card">VALOR HORA REAL<br>(MODELO BETA)</div><div class="val-res">R$ {max(0, v_hora_real):.2f}</div></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="card-res"><div class="label-card">CONFISCO<br>REAL</div><div class="val-res">{max(0, perda):.1f}%</div></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="card-res"><div class="label-card">EXPROPRIAÇÃO<br>MENSAL</div><div class="val-res">{h_total_exprop:.0f}H</div></div>', unsafe_allow_html=True)

    # MAPA COM PONTOS REAIS
    st.markdown('<div class="secao-titulo">🗺️ MAPEAMENTO DO DESLOCAMENTO</div>', unsafe_allow_html=True)
    df_map = pd.DataFrame({
        'lat': [coords[moradia][0], coords[trabalho][0]],
        'lon': [coords[moradia][1], coords[trabalho][1]]
    })
    st.map(df_map)

    [Image of a geographical map of the Metropolitan Region of São Paulo showing commuting patterns between the periphery and the center]

    st.markdown(f"""
        <div class="sintese-box">
            <b>SÍNTESE DO EXPERIMENTO:</b><br>
            Considerando <b>{dias_trecho} dias</b> presenciais, sua expropriação temporal é de <b>{h_total_exprop:.0f} horas</b>. 
            O mapa acima ilustra a distância que separa sua residência da fonte de renda, um espaço geográfico onde ocorre o <b>confisco silencioso</b> do seu rendimento.
        </div>
    """, unsafe_allow_html=True)
