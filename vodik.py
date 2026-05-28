
import streamlit as st
st.markdown("""
<style>
.stApp {
    background-color: #0b1020;
    color: #f5f7fb;
}


}

h1, h2, h3, p, label, span, div {
    color: #f5f7fb !important;
}

[data-testid="stMetricValue"] {
    color: #93c5fd !important;
}

[data-testid="stMetricLabel"] {
    color: #d1d5db !important;
}

.stAlert {
    background-color: #1f2937;
}
</style>
""", unsafe_allow_html=True)
st.set_page_config(
    page_title="Vodíkový stratég ČR",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Vodíkový stratég ČR")
st.subheader("Jednoduchá simulační hra pro rozvoj vodíku v Česku")

st.write("Nastav politické a tržní podmínky a sleduj, zda Česko splní vodíkový cíl.")

# postranní panel
st.sidebar.header("Nastavení politik")

povolovani = st.sidebar.slider("Rychlost povolování", 0.0, 1.0, 0.4)
dotace = st.sidebar.slider("Dotace", 0.0, 1.0, 0.5)
infrastruktura = st.sidebar.slider("Infrastruktura", 0.0, 1.0, 0.3)
podpora_prumyslu = st.sidebar.slider("Podpora průmyslu", 0.0, 1.0, 0.5)
cena_elektriny = st.sidebar.slider("Dostupnost levné elektřiny", 0.0, 1.0, 0.4)

# výpočet
policy_index = (
    povolovani
    + dotace
    + infrastruktura
    + podpora_prumyslu
    + cena_elektriny
) / 5

zakladni_vykon_GW = 1.0
provozni_hodiny = 4000
spotreba_el_na_kg = 55
cil_H2_tis_tun = 100

skutecny_vykon_GW = zakladni_vykon_GW * (0.5 + policy_index)

vyroba_H2_tis_tun = (
    skutecny_vykon_GW * 1000 * provozni_hodiny / spotreba_el_na_kg / 1000
)

chybi_H2 = max(0, cil_H2_tis_tun - vyroba_H2_tis_tun)

# výsledky
col1, col2, col3 = st.columns(3)

col1.metric("Policy index", round(policy_index, 2))
col2.metric("Výkon elektrolyzérů", f"{skutecny_vykon_GW:.2f} GW")
col3.metric("Výroba vodíku", f"{vyroba_H2_tis_tun:.1f} tis. tun H₂")

st.divider()

if vyroba_H2_tis_tun >= cil_H2_tis_tun:
    st.success("✅ Cíl strategie je splněn.")
else:
    st.error("❌ Cíl strategie není splněn.")
    st.write(f"Chybí ještě **{chybi_H2:.1f} tis. tun H₂**.")

st.progress(min(vyroba_H2_tis_tun / cil_H2_tis_tun, 1.0))

st.caption("Zdroj: vlastní modelový prototyp. Vstupní hodnoty jsou pracovní scénář.")
