# Simulador de Bonos El Potosí 2025 en Streamlit
import streamlit as st

st.set_page_config(page_title="Simulador de Bonos El Potosí 2025", layout="centered")

col1, col2 = st.columns([0.85, 0.15])
with col1:
    st.markdown("""
        <h1 style='text-align: left;'>Simulador de Bonos</h1>
        <h3 style='text-align: left;'>El Potosí 2025</h3>
    """, unsafe_allow_html=True)
with col2:
    st.image("link logo.jpg", width=90)

st.markdown("---")
nombre = st.text_input("👤 Nombre del Agente")
tipo_bono = st.selectbox("Selecciona el tipo de bono a calcular:",
                         ["Selecciona...", "Autos", "Daños", "Vida Individual y Venta Masiva", "Vida Grupo y Accidentes"])

def formato_pesos(valor):
    return f"${valor:,.2f}" if valor else "$0.00"

# -------------------------- BLOQUE DE AUTOS --------------------------
if tipo_bono == "Autos":
    prod_2024_autos = st.number_input("Producción 2024 Autos", min_value=0.0, step=1000.0, format="%.2f", key="autos_prod_2024")
    prod_autos = st.number_input("Producción 2025 Autos", min_value=0.0, step=1000.0, format="%.2f", key="autos_prod_2025")
    siniestralidad_autos = st.number_input("Siniestralidad % Autos", min_value=0.0, max_value=100.0, step=0.1, key="autos_sin")
    num_polizas_web_autos = st.number_input("Número de pólizas emitidas por portal web", min_value=0, step=1, key="autos_web")
    agente_nuevo_autos = st.checkbox("Agente nuevo en Autos", key="autos_nuevo")

    if st.button("Calcular Bonos", key="btn_autos"):
        resultados = []
        total_bono = 0

        # Bono Producción Autos
        niveles_autos = [(5500000, 7.5), (4750000, 6.5), (3800000, 5.5), (2750000, 4.5), (1800000, 3.5),
                         (975000, 2.5), (500000, 1.5), (375000, 1.0)]
        bono_autos = 0
        explicacion_autos = ""
        for monto, porcentaje in niveles_autos:
            if prod_autos >= monto:
                bono_autos = prod_autos * (porcentaje / 100)
                explicacion_autos = f"🔹 Bono de Producción: {porcentaje:.2f}% ➜ {formato_pesos(bono_autos)}\n✅ Aplica según tabla con siniestralidad del {siniestralidad_autos:.2f}%."
                break
        if siniestralidad_autos > 80:
            bono_autos = 0
            explicacion_autos += "\n❌ Siniestralidad mayor al 80%, bono anulado."
        elif siniestralidad_autos > 70:
            bono_autos *= 0.5
            explicacion_autos += "\n⚠️ Siniestralidad entre 70%-80%, bono al 50%."
        elif siniestralidad_autos > 60:
            bono_autos *= 0.6
            explicacion_autos += "\n⚠️ Siniestralidad entre 60%-70%, bono al 60%."
        if bono_autos == 0:
            explicacion_autos = f"❌ Producción insuficiente o siniestralidad alta."
        resultados.append(("🔹 Bono de Producción", bono_autos, explicacion_autos))
        total_bono += bono_autos

        # Bono Crecimiento Autos
        bono_crec_autos = 0
        crecimiento = ((prod_autos - prod_2024_autos) / prod_2024_autos) * 100 if prod_2024_autos > 0 else 0
        if not agente_nuevo_autos and prod_2024_autos >= 300000 and crecimiento >= 30:
            bono_crec_autos = prod_autos * 0.03
            resultados.append(("🚀 Bono de Crecimiento", bono_crec_autos, f"✅ Crecimiento del {crecimiento:.2f}% ➜ {formato_pesos(bono_crec_autos)}"))
            total_bono += bono_crec_autos
        elif not agente_nuevo_autos:
            resultados.append(("🚀 Bono de Crecimiento", 0, f"❌ Crecimiento del {crecimiento:.2f}%, no aplica."))

        # Bono Agente Novel Autos
        if agente_nuevo_autos and prod_autos >= 375000:
            bono_novel = prod_autos * 0.02
            resultados.append(("🆕 Bono Agente Novel", bono_novel, "✅ Producción ≥ $375,000. Aplica 2% adicional."))
            total_bono += bono_novel
        elif agente_nuevo_autos:
            resultados.append(("🆕 Bono Agente Novel", 0, "❌ Producción insuficiente para aplicar bono novel."))

        # Bono Utilidad Autos
        if prod_autos >= 1500000:
            utilidad = [(0, 20, 0.12), (20.01, 25, 0.10), (25.01, 30, 0.08), (30.01, 35, 0.06),
                        (35.01, 40, 0.05), (40.01, 45, 0.04), (45.01, 50, 0.03), (50.01, 55, 0.02),
                        (55.01, 60, 0.01), (60.01, 65, 0.005)]
            for minimo, maximo, porcentaje in utilidad:
                if minimo <= siniestralidad_autos <= maximo:
                    bono_utilidad = prod_autos * porcentaje
                    resultados.append(("📊 Bono Utilidad Anual", bono_utilidad, f"✅ Siniestralidad {siniestralidad_autos:.1f}% en rango {minimo}-{maximo}%, aplica {porcentaje*100:.1f}%."))
                    total_bono += bono_utilidad
                    break

        # Bono Emisión Web
        bono_web = num_polizas_web_autos * 100
        resultados.append(("🌐 Bono Emisión Web", bono_web, f"✅ {num_polizas_web_autos} pólizas x $100 ➜ {formato_pesos(bono_web)}"))
        total_bono += bono_web

        # Mostrar resultados
        st.markdown("---")
        st.subheader(f"📋 Resultado para {nombre}:")

        st.markdown("### 📊 Datos Ingresados:")
        st.markdown(f"- Producción 2024: {formato_pesos(prod_2024_autos)}")
        st.markdown(f"- Producción 2025: {formato_pesos(prod_autos)}")
        st.markdown(f"- Siniestralidad: {siniestralidad_autos:.2f}%")
        st.markdown(f"- Unidades Emitidas: {num_polizas_web_autos}")

        st.markdown("### 💵 Resultados de Bono:")
        for concepto, monto, nota in resultados:
            st.markdown(f"**{concepto}**: {formato_pesos(monto)}")
            st.caption(nota)

        st.markdown(f"### 🧾 Total del Bono Autos: **{formato_pesos(total_bono)}**")
        st.caption("📌 Aplican restricciones y condiciones conforme al cuaderno oficial de Seguros El Potosí 2025.")
# -------------------------- BLOQUE DE DAÑOS --------------------------
if tipo_bono == "Daños":
    prod_2024_danos = st.number_input("Producción 2024 Daños", min_value=0.0, step=1000.0, format="%.2f", key="danos_prod_2024")
    prod_danos = st.number_input("Producción 2025 Daños", min_value=0.0, step=1000.0, format="%.2f", key="danos_prod_2025")
    siniestralidad_danos = st.number_input("Siniestralidad % Daños", min_value=0.0, max_value=100.0, step=0.1, key="danos_sin")
    prod_casa_web = st.number_input("Producción CASA emitida por Web", min_value=0.0, step=1000.0, format="%.2f", key="danos_web")

    if st.button("Calcular Bonos", key="btn_danos"):
        resultados = []
        total_bono = 0

        # Bono Producción Daños
        niveles_danos = [(2100000, 7), (1750000, 6), (1500000, 5), (1250000, 4), (900000, 3), (700000, 2), (300000, 1)]
        bono_danos = 0
        for monto, porcentaje in niveles_danos:
            if prod_danos >= monto:
                bono_danos = prod_danos * (porcentaje / 100)
                resultados.append(("🏢 Bono Producción Daños", bono_danos, f"✅ Producción ${prod_danos:,.0f} ≥ ${monto:,.0f}, aplica {porcentaje}%."))
                break
        if bono_danos == 0:
            resultados.append(("🏢 Bono Producción Daños", 0, f"❌ Producción ${prod_danos:,.0f} no alcanza mínimo de $300,000."))
        total_bono += bono_danos

        # Bono Crecimiento Daños
        bono_crec_danos = 0
        crecimiento = ((prod_danos - prod_2024_danos) / prod_2024_danos) * 100 if prod_2024_danos > 0 else 0
        nota_crec = ""
        if crecimiento >= 40:
            bono_crec_danos = (prod_danos - prod_2024_danos) * 0.09
            nota_crec = f"✅ Crecimiento del {crecimiento:.2f}%, aplica 9%."
        elif crecimiento >= 30:
            bono_crec_danos = (prod_danos - prod_2024_danos) * 0.06
            nota_crec = f"✅ Crecimiento del {crecimiento:.2f}%, aplica 6%."
        elif crecimiento >= 20:
            bono_crec_danos = (prod_danos - prod_2024_danos) * 0.03
            nota_crec = f"✅ Crecimiento del {crecimiento:.2f}%, aplica 3%."
        else:
            nota_crec = f"❌ Crecimiento del {crecimiento:.2f}%, no alcanza mínimo de 20%."
        resultados.append(("📈 Bono Crecimiento Daños", bono_crec_danos, nota_crec))
        total_bono += bono_crec_danos

        # Bono CASA Web
        bono_casa_web = 0
        if prod_casa_web >= 150000:
            bono_casa_web = prod_casa_web * 0.08
            nota_web = "✅ Producción CASA Web ≥ $150,000, aplica 8%."
        elif prod_casa_web >= 75000:
            bono_casa_web = prod_casa_web * 0.06
            nota_web = "✅ Producción CASA Web ≥ $75,000, aplica 6%."
        elif prod_casa_web >= 30000:
            bono_casa_web = prod_casa_web * 0.04
            nota_web = "✅ Producción CASA Web ≥ $30,000, aplica 4%."
        else:
            nota_web = "❌ Producción insuficiente para bono CASA Web."
        resultados.append(("🌐 Bono CASA Web", bono_casa_web, nota_web))
        total_bono += bono_casa_web

        # Mostrar resultados
        st.markdown("---")
        st.subheader(f"📋 Resultado para {nombre}:")

        st.markdown("### 📊 Datos Ingresados:")
        st.markdown(f"- Producción 2024: {formato_pesos(prod_2024_danos)}")
        st.markdown(f"- Producción 2025: {formato_pesos(prod_danos)}")
        st.markdown(f"- Siniestralidad: {siniestralidad_danos:.2f}%")
        st.markdown(f"- Producción CASA Web: {formato_pesos(prod_casa_web)}")

        st.markdown("### 💵 Resultados de Bono:")
        for concepto, monto, nota in resultados:
            st.markdown(f"**{concepto}**: {formato_pesos(monto)}")
            st.caption(nota)

        st.markdown(f"### 🧾 Total del Bono Daños: **{formato_pesos(total_bono)}**")
        st.caption("📌 Aplican restricciones y condiciones conforme al cuaderno oficial de Seguros El Potosí 2025.")
# -------------------------- BLOQUE DE VIDA INDIVIDUAL Y VENTA MASIVA --------------------------
if tipo_bono == "Vida Individual y Venta Masiva":
    prod_vida_2024 = st.number_input("Producción 2024 Vida (Primer Año)", min_value=0.0, step=1000.0, format="%.2f", key="vida_prod_2024")
    prod_vida = st.number_input("Producción 2025 Vida (Primer Año)", min_value=0.0, step=1000.0, format="%.2f", key="vida_prod")
    conservacion = st.number_input("Índice de Conservación %", min_value=0.0, max_value=100.0, step=0.1, key="vida_cons")
    num_negocios = st.number_input("Número de Negocios", min_value=0, step=1, key="vida_neg")
    agente_novel_vida = st.checkbox("Agente nuevo en Vida", key="vida_novel")

    if st.button("Calcular Bonos", key="btn_vida"):
        resultados = []
        total_bono = 0

        # Bono Producción Vida
        tabla_vida = [(2700000, 0.34), (2100000, 0.32), (1600000, 0.28), (1300000, 0.24), (920000, 0.18),
                      (600000, 0.14), (300000, 0.085), (160000, 0.065)]
        bono_vida = 0
        explicacion_vida = ""
        for prod_min, porc in tabla_vida:
            if prod_vida >= prod_min:
                if conservacion >= 95 and num_negocios >= 4:
                    bono_vida = prod_vida * porc
                    explicacion_vida = f"✅ Producción ${prod_vida:,.0f} ≥ ${prod_min:,.0f}, conservación {conservacion:.1f}%, {num_negocios} negocios. Aplica {porc*100:.1f}%."
                else:
                    explicacion_vida = f"❌ Conservación {conservacion:.1f}% o número de negocios {num_negocios} no cumplen con requisitos."
                break
        if bono_vida == 0 and explicacion_vida == "":
            explicacion_vida = f"❌ Producción de ${prod_vida:,.0f} no alcanza el mínimo requerido (${tabla_vida[-1][0]:,.0f})."
        resultados.append(("💼 Bono Producción Vida", bono_vida, explicacion_vida))
        total_bono += bono_vida

        # Bono Agente Novel Vida (extra adicional)
        explicacion_novel = ""
        if agente_novel_vida and num_negocios >= 4:
            adicional = 0.0
            for prod_min, porc in tabla_vida:
                if prod_vida >= prod_min:
                    if prod_min >= 2100000:
                        adicional = 0.35 if prod_min == 2100000 else 0.40
                    elif prod_min >= 1300000:
                        adicional = 0.30
                    elif prod_min >= 600000:
                        adicional = 0.25
                    elif prod_min >= 160000:
                        adicional = 0.20
                    break
            if adicional > 0:
                bono_extra = prod_vida * adicional
                explicacion_novel = f"✅ Agente novel con producción ${prod_vida:,.0f} y {num_negocios} negocios. Aplica bono adicional del {adicional*100:.0f}%."
                resultados.append(("🎁 Bono Extra Agente Novel Vida", bono_extra, explicacion_novel))
                total_bono += bono_extra
            else:
                explicacion_novel = "❌ Producción insuficiente para bono adicional novel."
                resultados.append(("🎁 Bono Extra Agente Novel Vida", 0, explicacion_novel))
        elif agente_novel_vida:
            explicacion_novel = "❌ Agente novel con menos de 4 negocios."
            resultados.append(("🎁 Bono Extra Agente Novel Vida", 0, explicacion_novel))

        # Mostrar resultados
        st.markdown("---")
        st.subheader(f"📋 Resultado para {nombre}:")

        st.markdown("### 📊 Datos Ingresados:")
        st.markdown(f"- Producción 2024: {formato_pesos(prod_vida_2024)}")
        st.markdown(f"- Producción 2025: {formato_pesos(prod_vida)}")
        st.markdown(f"- Conservación: {conservacion:.1f}%")
        st.markdown(f"- Negocios: {num_negocios}")

        st.markdown("### 💵 Resultados de Bono:")
        for concepto, monto, nota in resultados:
            st.markdown(f"**{concepto}**: {formato_pesos(monto)}")
            st.caption(nota)

        st.markdown(f"### 🧾 Total del Bono Vida: **{formato_pesos(total_bono)}**")
        st.caption("📌 Aplican restricciones y condiciones conforme al cuaderno oficial de Seguros El Potosí 2025.")
# -------------------------- BLOQUE DE VIDA GRUPO Y ACCIDENTES --------------------------
if tipo_bono == "Vida Grupo y Accidentes":
    prod_vida_grupo = st.number_input("Producción 2025 Vida Grupo (trimestral)", min_value=0.0, step=1000.0, format="%.2f", key="vg_prod")
    prod_accidentes = st.number_input("Producción 2025 Accidentes (trimestral)", min_value=0.0, step=1000.0, format="%.2f", key="acc_prod")
    siniestralidad = st.number_input("Siniestralidad % Vida Grupo / Accidentes", min_value=0.0, max_value=100.0, step=0.1, key="vg_sin")

    if st.button("Calcular Bonos", key="btn_vg_acc"):
        resultados = []
        total_bono = 0

        # Bono Vida Grupo Trimestral
        if prod_vida_grupo > 250000:
            bono_vg = prod_vida_grupo * 0.03
            resultados.append(("👥 Bono Trimestral Vida Grupo", bono_vg, f"✅ Producción ${prod_vida_grupo:,.0f} supera mínimo de $250,000. Aplica 3%."))
            total_bono += bono_vg
        else:
            resultados.append(("👥 Bono Trimestral Vida Grupo", 0, f"❌ Producción ${prod_vida_grupo:,.0f} no alcanza mínimo de $250,001."))

        # Bono Vida Grupo Anual
        if prod_vida_grupo >= 500000 and siniestralidad < 60:
            bono_vg_anual = prod_vida_grupo * 0.02
            resultados.append(("📅 Bono Anual Vida Grupo", bono_vg_anual, f"✅ Producción ${prod_vida_grupo:,.0f} ≥ $500,000 y siniestralidad {siniestralidad:.1f}% < 60%."))
            total_bono += bono_vg_anual
        else:
            nota = ""
            if prod_vida_grupo < 500000:
                nota += f"Producción insuficiente (${prod_vida_grupo:,.0f} < $500,000). "
            if siniestralidad >= 60:
                nota += f"Siniestralidad muy alta ({siniestralidad:.1f}% ≥ 60%)."
            resultados.append(("📅 Bono Anual Vida Grupo", 0, f"❌ {nota}"))

        # Bono Accidentes Trimestral
        bono_acc = 0
        nota_acc = ""
        if prod_accidentes >= 400000:
            bono_acc = prod_accidentes * 0.10
            nota_acc = "✅ Aplica bono del 10% por producción ≥ $400,000."
        elif prod_accidentes >= 300000:
            bono_acc = prod_accidentes * 0.06
            nota_acc = "✅ Aplica bono del 6% por producción ≥ $300,000."
        elif prod_accidentes >= 200000:
            bono_acc = prod_accidentes * 0.04
            nota_acc = "✅ Aplica bono del 4% por producción ≥ $200,000."
        else:
            nota_acc = f"❌ Producción de ${prod_accidentes:,.0f} no alcanza mínimo de $200,000."
        resultados.append(("🧯 Bono Trimestral Accidentes", bono_acc, nota_acc))
        total_bono += bono_acc

        # Bono Accidentes Anual
        if prod_accidentes >= 500000 and siniestralidad < 60:
            bono_acc_anual = prod_accidentes * 0.05
            resultados.append(("📅 Bono Anual Accidentes", bono_acc_anual, f"✅ Producción ${prod_accidentes:,.0f} ≥ $500,000 y siniestralidad {siniestralidad:.1f}% < 60%."))
            total_bono += bono_acc_anual
        else:
            nota = ""
            if prod_accidentes < 500000:
                nota += f"Producción insuficiente (${prod_accidentes:,.0f} < $500,000). "
            if siniestralidad >= 60:
                nota += f"Siniestralidad alta ({siniestralidad:.1f}% ≥ 60%)."
            resultados.append(("📅 Bono Anual Accidentes", 0, f"❌ {nota}"))

        # Mostrar resultados
        st.markdown("---")
        st.subheader(f"📋 Resultado para {nombre}:")

        st.markdown("### 📊 Datos Ingresados:")
        st.markdown(f"- Producción Trimestral Vida Grupo: {formato_pesos(prod_vida_grupo)}")
        st.markdown(f"- Producción Trimestral Accidentes: {formato_pesos(prod_accidentes)}")
        st.markdown(f"- Siniestralidad: {siniestralidad:.2f}%")

        st.markdown("### 💵 Resultados de Bono:")
        for concepto, monto, nota in resultados:
            st.markdown(f"**{concepto}**: {formato_pesos(monto)}")
            st.caption(nota)

        st.markdown(f"### 🧾 Total del Bono Vida Grupo y Accidentes: **{formato_pesos(total_bono)}**")
        st.caption("📌 Aplican restricciones y condiciones conforme al cuaderno oficial de Seguros El Potosí 2025.")

