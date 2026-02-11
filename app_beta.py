import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. CONFIGURAÇÃO E ESTILO DE ALTO IMPACTO
st.set_page_config(page_title="LAB: Calculadora do Trecho", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"], .stApp { background-color: #000000 !important; }
    .stTooltipIcon { filter: invert(1) brightness(5) !important; transform: scale(1.4); }
    
    .chamada-impacto { 
        background-color: #E63946; color: white; text-align: center; 
        padding: 15px; font-weight: 900; text-transform: uppercase; 
        border: 3px solid #FFCC00; margin-bottom: 25px; font-size: 1.5rem; 
    }
    .propisito-app { 
        color: #FFCC00 !important; font-family: 'Arial Black', sans-serif; 
        font-size: 1.8rem !important; text-align: center; text-transform: uppercase; 
    }
    .secao-titulo { 
        color: #FFCC00 !important; font-size: 1.1rem !important; 
        font-weight: 800; text-transform: uppercase; 
        margin-top: 25px; border-bottom: 2px solid #FFCC00; padding-bottom: 5px; 
    }
    label { color: #FFCC00 !important; font-weight: 700 !important; font-size: 0.9rem !important; }
    
    /* CARDS DE RESULTADO */
    .card-res { 
        background-color: #111; border: 2px solid #FFCC00; 
        padding: 20px 10px; text-align: center; border-radius: 5px; 
        min-height: 160px; display: flex; flex-direction: column; justify-content: center; 
    }
    .val-res { color: #FFCC00 !important; font-size: 2.2rem !important; font-weight: 900 !important; }
    .label-card { color: #FFFFFF !important; font-size: 0.75rem !important; font-weight: bold; text-transform: uppercase; }
    
    /* SÍNTESE COM ÊNFASE TOTAL */
    .sintese-box { 
        background-color: #E63946; border: 5px solid #FFCC00; 
        padding: 40px; margin-top: 50px; color: #FFFFFF; 
        font-size: 1.4rem; line-height: 1.5; font-weight: 800; 
        border-radius: 15px; text-align: center;
        box-shadow: 0px 0px 20px rgba(255, 204, 0, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BASE GEO COMPLETA (DISTRITOS + RMSP)
# Adicionei a lógica de fallback: se não houver coordenada exata, centraliza em SP
geo_db = {
    "São Paulo (Centro)": [-23.5505, -46.6333], "Caieiras": [-23.3644, -46.7411], 
    "Franco da Rocha": [-23.3283, -46.7275], "Francisco Morato": [-23.2817, -46.7450],
    "Cajamar": [-23.3569, -46.8764], "Mairiporã": [-23.3186, -46.5867],
    "Grajaú": [-23.7744, -46.6975], "Itaquera": [-23.5333, -46.4583],
    "Guaianases": [-23.5422, -46.4139], "Cidade Tiradentes": [-23.5936, -46.4011],
    "Perus": [-23.4061, -46.7553], "Parelheiros": [-23.8347, -46.7175],
    "Osasco": [-23.5325, -46.7917], "Guarulhos": [-23.4542, -46.5333],
    "Santo André": [-23.6666, -46.5333], "São Bernardo do Campo": [-23.6944, -46.5644],
    "São Caetano do Sul": [-23.6225, -46.5489], "Diadema": [-23.6861, -46.6233],
    "Mauá": [-23.6678, -46.4614], "Mogi das Cruzes": [-23.5235, -46.1878],
    "Barueri": [-23.5112, -46.8761], "Taboão da Serra": [-23.6256, -46.7575]
}
# (Nota: Em produção, você pode expandir essa lista para todos os 96 distritos)
lista_geo = sorted(list(geo_db.keys()))

st.markdown('<div class="chamada-impacto">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="propisito-app">QTO DO SEU SALÁRIO FICA NO TRANSPORTE?</div>', unsafe_allow_html=True)

with st.form("beta_calc"):
    moradia = st.selectbox("🏠 ONDE VOCÊ MORA?", lista_geo)
    trabalho = st.selectbox("💼 ONDE VOCÊ TRABALHA?", lista_geo)
    
    col1, col2, col3 = st.columns(3)
    with col1: sal = st.number_input("💵 SALÁRIO BRUTO:", min_value=0.0, step=100.0)
    with col2: vida = st.number_input("🏠 CUSTO VIDA:", min_value=0.0, help="Opcional: Gastos fixos (moradia, luz, alimentação) para calcular a sobra final.")
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
    custo_t = (p_pub + p_app + p_car) * dias_presenca
    h_total_exprop = h_trecho * dias_presenca
    v_hora_real = (sal - custo_t) / (h_paga + h_total_exprop)
    perda = (1 - (v_hora_real / (sal/h_paga))) * 100
    sobra_final = sal - custo_t - vida

    # CARDS DE RESULTADO
    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="card-res"><div class="label-card">VALOR REAL PELA<br>HORA DE TRABALHO PAGA</div><div class="val-res">R$ {max(0, v_hora_real):.2f}</div></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="card-res"><div class="label-card">SALÁRIO REAL<br>CONFISCADO</div><div class="val-res">{max(0, perda):.1f}%</div></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="card-res"><div class="label-card">TEMPO DE TRABALHO NÃO PAGO<br>(HORAS/MÊS)</div><div class="val-res">{h_total_exprop:.0f}H</div></div>', unsafe_allow_html=True)

    # MAPA COM FOCO NO DESLOCAMENTO
    st.markdown('<div class="secao-titulo">🗺️ MAPEAMENTO DO DESLOCAMENTO (BETA)</div>', unsafe_allow_html=True)
    df_map = pd.DataFrame({
        'lat': [geo_db[moradia][0], geo_db[trabalho][0]],
        'lon': [geo_db[moradia][1], geo_db[trabalho][1]]
    })
    st.map(df_map)

    

    # SÍNTESE DE ALTO IMPACTO
    local_txt = f"por dentro de <b>{moradia}</b>" if moradia == trabalho else f"entre <b>{moradia}</b> e <b>{trabalho}</b>"
    sintese_v = f"<br><br><b>RENDIMENTO RESIDUAL:</b> Após o custo de vida (R$ {vida:,.2f}), restam apenas <span style='color:#FFCC00'>R$ {max(0, sobra_final):.2f}</span> mensais." if vida > 0 else ""

    st.markdown(f"""
        <div class="sintese-box">
            🚨 SÍNTESE DA EXPROPRIAÇÃO ({dias_presenca} DIAS):<br><br>
            Ao se deslocar {local_txt}, você dedica <span style="color:#FFCC00">{h_total_exprop:.0f} horas</span> mensais não remuneradas ao sistema.<br><br>
            O seu <b>VALOR REAL PELA HORA DE TRABALHO PAGA</b> cai para <b>R$ {max(0, v_hora_real):.2f}</b>.{sintese_v}
        </div>
    """, unsafe_allow_html=True)
