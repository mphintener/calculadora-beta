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
    "São Paulo (Centro)": [-23.5505, -46.6333], "Barra Funda": [-23.525, -46.666], "Pinheiros": [-23.561, -46.701], 
    "Água Rasa": [-23.559, -46.583], "Alto de Pinheiros": [-23.558, -46.705], "Anhanguera": [-23.434, -46.784], 
    "Aricanduva": [-23.581, -46.511], "Artur Alvim": [-23.535, -46.484], "Bela Vista": [-23.561, -46.641], 
    "Belém": [-23.542, -46.591], "Bom Retiro": [-23.526, -46.635], "Brasilândia": [-23.463, -46.685], 
    "Butantã": [-23.571, -46.708], "Cachoeirinha": [-23.473, -46.657], "Cambuci": [-23.567, -46.621], 
    "Campo Belo": [-23.628, -46.666], "Campo Grande": [-23.679, -46.689], "Campo Limpo": [-23.647, -46.756], 
    "Cangaíba": [-23.501, -46.521], "Capão Redondo": [-23.660, -46.760], "Carrão": [-23.559, -46.541], 
    "Casa Verde": [-23.507, -46.653], "Cidade Ademar": [-23.675, -46.655], "Cidade Dutra": [-23.708, -46.697], 
    "Cidade Líder": [-23.568, -46.495], "Cidade Tiradentes": [-23.593, -46.401], "Consolação": [-23.554, -46.657], 
    "Ermelino Matarazzo": [-23.495, -46.484], "Freguesia do Ó": [-23.503, -46.699], "Grajaú": [-23.774, -46.697], 
    "Guaianases": [-23.542, -46.413], "Ipiranga": [-23.591, -46.603], "Itaim Bibi": [-23.583, -46.683], 
    "Itaim Paulista": [-23.492, -46.391], "Itaquera": [-23.533, -46.458], "Jabaquara": [-23.645, -46.641], 
    "Jaçanã": [-23.461, -46.594], "Jaguara": [-23.507, -46.755], "Jaguaré": [-23.544, -46.745], 
    "Jaraguá": [-23.447, -46.744], "Jardim Ângela": [-23.717, -46.776], "Jardim Helena": [-23.483, -46.411], 
    "Jardim Paulista": [-23.571, -46.666], "Lapa": [-23.522, -46.702], "Liberdade": [-23.566, -46.635], 
    "Limão": [-23.511, -46.673], "Mandaqui": [-23.475, -46.634], "Moema": [-23.595, -46.661], 
    "Mooca": [-23.553, -46.603], "Morumbi": [-23.591, -46.721], "Parelheiros": [-23.834, -46.717], 
    "Penha": [-23.521, -46.543], "Perdizes": [-23.535, -46.671], "Perus": [-23.406, -46.755], 
    "Pirituba": [-23.487, -46.723], "Santana": [-23.501, -46.623], "Santo Amaro": [-23.647, -46.701], 
    "Sé": [-23.548, -46.633], "Tatuapé": [-23.541, -46.571], "Vila Mariana": [-23.581, -46.633], 
    "Arujá": [-23.391, -46.321], "Barueri": [-23.511, -46.876], "Caieiras": [-23.364, -46.741], 
    "Cajamar": [-23.356, -46.876], "Carapicuíba": [-23.523, -46.835], "Diadema": [-23.686, -46.623], 
    "Francisco Morato": [-23.281, -46.745], "Franco da Rocha": [-23.328, -46.727], "Guarulhos": [-23.454, -46.533], 
    "Mauá": [-23.667, -46.461], "Osasco": [-23.532, -46.791], "Pirapora do Bom Jesus": [-23.391, -46.991], 
    "Santo André": [-23.666, -46.533], "São Bernardo do Campo": [-23.694, -46.564], "São Caetano do Sul": [-23.622, -46.548], 
    "Taboão da Serra": [-23.625, -46.757]
}
lista_geo = sorted(list(geo_db.keys()))

st.markdown('<div class="chamada-impacto">ALERTA DE EXPROPRIAÇÃO MENSAL</div>', unsafe_allow_html=True)
st.markdown('<div class="propisito-app">QTO DO SEU SALÁRIO FICA NO TRANSPORTE?</div>', unsafe_allow_html=True)

with st.form("beta_calc"):
    moradia = st.selectbox("🏠 ONDE VOCÊ MORA?", lista_geo)
    trabalho = st.selectbox("💼 ONDE VOCÊ TRABALHA?", lista_geo)
    
    col1, col2, col3 = st.columns(3)
    with col1: sal = st.number_input("💵 SALÁRIO BRUTO:", min_value=0.0, step=100.0)
    with col2: 
        vida = st.number_input("🏠 CUSTO VIDA:", min_value=0.0, help="Preenchimento Opcional: Aluguel, contas e comida para calcular a sobra final.")
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

    # MAPA COM MARCADOR DE IMPACTO (SEM EFEITO FÓSFORO)
    st.markdown('<div class="secao-titulo">🗺️ MAPEAMENTO DO FLUXO PENDULAR</div>', unsafe_allow_html=True)
    
    line_df = pd.DataFrame([{
        "source": [geo_db[moradia][1], geo_db[moradia][0]],
        "target": [geo_db[trabalho][1], geo_db[trabalho][0]]
    }])
    
    point_df = pd.DataFrame([
        {"pos": [geo_db[moradia][1], geo_db[moradia][0]], "color": [255, 204, 0]},
        {"pos": [geo_db[trabalho][1], geo_db[trabalho][0]], "color": [230, 57, 70]}
    ])

    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=(geo_db[moradia][0] + geo_db[trabalho][0]) / 2,
            longitude=(geo_db[moradia][1] + geo_db[trabalho][1]) / 2,
            zoom=11.5, pitch=0
        ),
        layers=[
            pdk.Layer(
                "LineLayer", data=line_df, get_source_position="source", get_target_position="target",
                get_color=[255, 204, 0, 100], get_width=12
            ),
            pdk.Layer(
                "ScatterplotLayer", data=point_df, get_position="pos", get_color="color",
                get_radius=500, opacity=0.4, stroked=True, line_width_min_pixels=3
            ),
            pdk.Layer(
                "ScatterplotLayer", data=point_df, get_position="pos", get_color="color",
                get_radius=150, opacity=1
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
