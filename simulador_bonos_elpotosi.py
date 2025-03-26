# Simulador de Bonos El Potosí 2025 en Streamlit
import streamlit as st

st.set_page_config(page_title="Simulador de Bonos El Potosí 2025", layout="centered")
st.markdown("""
    <h1 style='text-align: center;'>Simulador de Bonos</h1>
    <h3 style='text-align: center;'>El Potosí 2025</h3>
""", unsafe_allow_html=True)

st.markdown("---")
nombre = st.text_input("👤 Nombre del Agente")

# Menú para seleccionar tipo de bono
tipo_bono = st.selectbox("Selecciona el tipo de bono a calcular:",
                         ["Selecciona...", "Autos", "Daños", "Vida Individual y Venta Masiva", "Vida Grupo y Accidentes"])

# Función para formato de moneda
def formato_pesos(valor):
    return f"${valor:,.2f}" if valor else "$0.00"

# Variables comunes
resultados = []
total_bono = 0

# -------------------------- BLOQUE DE AUTOS --------------------------
if tipo_bono == "Autos":
    prod_autos = st.number_input("Producción 2025 (Autos)", min_value=0.0, step=1000.0, format="%.2f")
    siniestralidad_autos = st.number_input("Siniestralidad % (Autos)", min_value=0.0, max_value=100.0, step=0.1)
    prod_2024_autos = st.number_input("Producción 2024 (Autos)", min_value=0.0, step=1000.0, format="%.2f")
    agente_nuevo_autos = st.checkbox("Agente nuevo en Autos (alta en 2025 o < $300,000 en 2024)")
    num_polizas_web_autos = st.number_input("Número de pólizas Autos emitidas por portal web", min_value=0, step=1)

    if st.button("Calcular Bonos"):
        resultados = []
        total_bono = 0

        # Bono de Producción
        niveles_autos = [(5500000, 7.5), (4750000, 6.5), (3800000, 5.5), (2750000, 4.5), (1800000, 3.5),
                         (975000, 2.5), (500000, 1.5), (375000, 1.0)]
        bono_autos = 0
        explicacion_autos = ""
        for monto, porcentaje in niveles_autos:
            if prod_autos >= monto:
                bono_autos = prod_autos * (porcentaje / 100)
                explicacion_autos = f"Nivel alcanzado: {porcentaje}%"
                break
        if siniestralidad_autos > 80:
            bono_autos = 0
            explicacion_autos += " | Siniestralidad mayor al 80%, bono no aplica. ❌"
        elif siniestralidad_autos > 70:
            bono_autos *= 0.5
            explicacion_autos += " | Siniestralidad entre 70%-80%, aplica el 50%."
        elif siniestralidad_autos > 60:
            bono_autos *= 0.6
            explicacion_autos += " | Siniestralidad entre 60%-70%, aplica el 60%."
        resultados.append(("🚗 Bono Producción Autos", bono_autos, explicacion_autos))
        total_bono += bono_autos

        # Bono de Crecimiento
        if not agente_nuevo_autos and prod_2024_autos >= 300000:
            crecimiento = ((prod_autos - prod_2024_autos) / prod_2024_autos) * 100 if prod_2024_autos > 0 else 0
            if crecimiento >= 30:
                bono_crec_autos = prod_autos * 0.03
                resultados.append(("🚗 Bono Crecimiento Autos", bono_crec_autos, f"Crecimiento de {crecimiento:.2f}%, aplica 3%. ✅"))
                total_bono += bono_crec_autos
            else:
                resultados.append(("🚗 Bono Crecimiento Autos", 0, f"Crecimiento de {crecimiento:.2f}%, no aplica. ❌"))

        # Bono Agente Novel
        if agente_nuevo_autos and prod_autos >= 375000:
            bono_novel = prod_autos * 0.02
            resultados.append(("🚗 Bono Producción Agente Novel", bono_novel, "Agente nuevo con producción ≥ $375,000. ✅"))
            total_bono += bono_novel
        elif agente_nuevo_autos:
            resultados.append(("🚗 Bono Producción Agente Novel", 0, "Producción insuficiente para bono de agente novel. ❌"))

        # Bono Utilidad Anual
        if prod_autos >= 1500000:
            sin = siniestralidad_autos
            utilidad = [(0, 20, 0.12), (20.01, 25, 0.10), (25.01, 30, 0.08), (30.01, 35, 0.06),
                        (35.01, 40, 0.05), (40.01, 45, 0.04), (45.01, 50, 0.03), (50.01, 55, 0.02),
                        (55.01, 60, 0.01), (60.01, 65, 0.005)]
            bono_utilidad = 0
            for minimo, maximo, porcentaje in utilidad:
                if minimo <= sin <= maximo:
                    bono_utilidad = prod_autos * porcentaje
                    resultados.append(("🚗 Bono Utilidad Anual Autos", bono_utilidad, f"Siniestralidad {sin:.2f}%, aplica {porcentaje*100:.1f}%. ✅"))
                    total_bono += bono_utilidad
                    break

        # Bono Emisión Web
        bono_web = num_polizas_web_autos * 100
        resultados.append(("🚗 Bono Emisión Web Autos", bono_web, f"{num_polizas_web_autos} pólizas emitidas. ✅"))
        total_bono += bono_web

        # Mostrar resultados
        st.markdown("---")
        st.subheader(f"Resultados para {nombre}:")
        for concepto, monto, nota in resultados:
            st.write(f"**{concepto}**: {formato_pesos(monto)}")
            st.caption(f"{nota}")

        st.success(f"💰 Total Bono Acumulado: {formato_pesos(total_bono)}")
        st.caption("📌 Aplican restricciones y condiciones conforme al cuaderno oficial de Seguros El Potosí 2025.")

# -------------------------- BLOQUE DE DAÑOS --------------------------
if tipo_bono == "Daños":
    prod_danos = st.number_input("Producción 2025 (Daños)", min_value=0.0, step=1000.0, format="%.2f")
    siniestralidad_danos = st.number_input("Siniestralidad % (Daños)", min_value=0.0, max_value=100.0, step=0.1)
    prod_2024_danos = st.number_input("Producción 2024 (Daños)", min_value=0.0, step=1000.0, format="%.2f")
    prod_casa_web = st.number_input("Producción CASA emitida por Web", min_value=0.0, step=1000.0, format="%.2f")

    if st.button("Calcular Bonos"):
        resultados = []
        total_bono = 0

        # Bono Producción Daños
        niveles_danos = [(2100000, 7), (1750000, 6), (1500000, 5), (1250000, 4), (900000, 3), (700000, 2), (300000, 1)]
        bono_danos = 0
        for monto, porcentaje in niveles_danos:
            if prod_danos >= monto:
                bono_danos = prod_danos * (porcentaje / 100)
                resultados.append(("🏠 Bono Producción Daños", bono_danos, f"Nivel alcanzado: {porcentaje}%. ✅"))
                break
        if bono_danos == 0:
            resultados.append(("🏠 Bono Producción Daños", 0, "Producción insuficiente. ❌"))
        total_bono += bono_danos

        # Bono Crecimiento Daños
        bono_crec_danos = 0
        if prod_2024_danos > 0:
            crecimiento = ((prod_danos - prod_2024_danos) / prod_2024_danos) * 100
            if crecimiento >= 40:
                bono_crec_danos = (prod_danos - prod_2024_danos) * 0.09
            elif crecimiento >= 30:
                bono_crec_danos = (prod_danos - prod_2024_danos) * 0.06
            elif crecimiento >= 20:
                bono_crec_danos = (prod_danos - prod_2024_danos) * 0.03
            if bono_crec_danos > 0:
                resultados.append(("📈 Bono Crecimiento Daños", bono_crec_danos, f"Crecimiento {crecimiento:.2f}%, aplica. ✅"))
                total_bono += bono_crec_danos
            else:
                resultados.append(("📈 Bono Crecimiento Daños", 0, f"Crecimiento {crecimiento:.2f}%, no aplica. ❌"))

        # Bono Casa Web
        bono_casa_web = 0
        if prod_casa_web >= 150000:
            bono_casa_web = prod_casa_web * 0.08
        elif prod_casa_web >= 75000:
            bono_casa_web = prod_casa_web * 0.06
        elif prod_casa_web >= 30000:
            bono_casa_web = prod_casa_web * 0.04
        if bono_casa_web > 0:
            resultados.append(("🌐 Bono Casa Web", bono_casa_web, "Producción CASA emitida por Web. ✅"))
            total_bono += bono_casa_web
        else:
            resultados.append(("🌐 Bono Casa Web", 0, "Producción insuficiente para bono CASA Web. ❌"))

        # Mostrar resultados
        st.markdown("---")
        st.subheader(f"Resultados para {nombre}:")
        for concepto, monto, nota in resultados:
            st.write(f"**{concepto}**: {formato_pesos(monto)}")
            st.caption(f"{nota}")

        st.success(f"💰 Total Bono Acumulado: {formato_pesos(total_bono)}")
        st.caption("📌 Aplican restricciones y condiciones conforme al cuaderno oficial de Seguros El Potosí 2025.")

# -------------------------- BLOQUE DE VIDA INDIVIDUAL Y VENTA MASIVA --------------------------
if tipo_bono == "Vida Individual y Venta Masiva":
    prod_vida = st.number_input("Producción 2025 Vida (Primer Año)", min_value=0.0, step=1000.0, format="%.2f")
    conservacion = st.number_input("Índice de Conservación %", min_value=0.0, max_value=100.0, step=0.1)
    num_negocios = st.number_input("Número de Negocios", min_value=0, step=1)
    agente_novel_vida = st.checkbox("Agente nuevo en Vida")

    if st.button("Calcular Bonos"):
        resultados = []
        total_bono = 0

        # Bono Producción Vida
        tabla_vida = [(2700000, 0.34), (2100000, 0.32), (1600000, 0.28), (1300000, 0.24), (920000, 0.18),
                      (600000, 0.14), (300000, 0.085), (160000, 0.065)]
        bono_vida = 0
        for prod_min, porc in tabla_vida:
            if prod_vida >= prod_min and conservacion >= 95 and num_negocios >= 4:
                bono_vida = prod_vida * porc
                resultados.append(("💼 Bono Producción Vida", bono_vida, f"Nivel {porc*100:.1f}%, conservación {conservacion}%, {num_negocios} negocios. ✅"))
                total_bono += bono_vida
                break
        if bono_vida == 0:
            resultados.append(("💼 Bono Producción Vida", 0, "No cumple con los requisitos de conservación o número de negocios. ❌"))

        # Bono Agente Novel Vida (extra adicional)
        if agente_novel_vida and num_negocios >= 4:
            adicional = 0.0
            if prod_vida >= 2700000:
                adicional = 0.40
            elif prod_vida >= 2100000:
                adicional = 0.35
            elif prod_vida >= 1600000:
                adicional = 0.30
            elif prod_vida >= 1300000:
                adicional = 0.30
            elif prod_vida >= 920000:
                adicional = 0.25
            elif prod_vida >= 600000:
                adicional = 0.25
            elif prod_vida >= 300000:
                adicional = 0.20
            elif prod_vida >= 160000:
                adicional = 0.20
            bono_extra = prod_vida * adicional
            resultados.append(("💼 Bono Extra Agente Novel Vida", bono_extra, f"Agente novel con adicional del {adicional*100:.0f}%. ✅"))
            total_bono += bono_extra
        elif agente_novel_vida:
            resultados.append(("💼 Bono Extra Agente Novel Vida", 0, "Producción insuficiente o < 4 negocios para bono adicional novel. ❌"))

        # Mostrar resultados
        st.markdown("---")
        st.subheader(f"Resultados para {nombre}:")
        for concepto, monto, nota in resultados:
            st.write(f"**{concepto}**: {formato_pesos(monto)}")
            st.caption(f"{nota}")

        st.success(f"💰 Total Bono Acumulado: {formato_pesos(total_bono)}")
        st.caption("📌 Aplican restricciones y condiciones conforme al cuaderno oficial de Seguros El Potosí 2025.")

# -------------------------- BLOQUE DE VIDA INDIVIDUAL Y VENTA MASIVA --------------------------
if tipo_bono == "Vida Individual y Venta Masiva":
    prod_vida = st.number_input("Producción 2025 Vida (Primer Año)", min_value=0.0, step=1000.0, format="%.2f")
    conservacion = st.number_input("Índice de Conservación %", min_value=0.0, max_value=100.0, step=0.1)
    num_negocios = st.number_input("Número de Negocios", min_value=0, step=1)
    agente_novel_vida = st.checkbox("Agente nuevo en Vida")

    if st.button("Calcular Bonos"):
        resultados = []
        total_bono = 0

        # Bono Producción Vida
        tabla_vida = [(2700000, 0.34), (2100000, 0.32), (1600000, 0.28), (1300000, 0.24), (920000, 0.18),
                      (600000, 0.14), (300000, 0.085), (160000, 0.065)]
        bono_vida = 0
        for prod_min, porc in tabla_vida:
            if prod_vida >= prod_min and conservacion >= 95 and num_negocios >= 4:
                bono_vida = prod_vida * porc
                resultados.append(("💼 Bono Producción Vida", bono_vida, f"Nivel {porc*100:.1f}%, conservación {conservacion}%, {num_negocios} negocios. ✅"))
                total_bono += bono_vida
                break
        if bono_vida == 0:
            resultados.append(("💼 Bono Producción Vida", 0, "No cumple con los requisitos de conservación o número de negocios. ❌"))

        # Bono Agente Novel Vida (extra adicional)
        if agente_novel_vida and num_negocios >= 4:
            adicional = 0.0
            if prod_vida >= 2700000:
                adicional = 0.40
            elif prod_vida >= 2100000:
                adicional = 0.35
            elif prod_vida >= 1600000:
                adicional = 0.30
            elif prod_vida >= 1300000:
                adicional = 0.30
            elif prod_vida >= 920000:
                adicional = 0.25
            elif prod_vida >= 600000:
                adicional = 0.25
            elif prod_vida >= 300000:
                adicional = 0.20
            elif prod_vida >= 160000:
                adicional = 0.20
            bono_extra = prod_vida * adicional
            resultados.append(("💼 Bono Extra Agente Novel Vida", bono_extra, f"Agente novel con adicional del {adicional*100:.0f}%. ✅"))
            total_bono += bono_extra
        elif agente_novel_vida:
            resultados.append(("💼 Bono Extra Agente Novel Vida", 0, "Producción insuficiente o < 4 negocios para bono adicional novel. ❌"))

        # Mostrar resultados
        st.markdown("---")
        st.subheader(f"Resultados para {nombre}:")
        for concepto, monto, nota in resultados:
            st.write(f"**{concepto}**: {formato_pesos(monto)}")
            st.caption(f"{nota}")

        st.success(f"💰 Total Bono Acumulado: {formato_pesos(total_bono)}")
        st.caption("📌 Aplican restricciones y condiciones conforme al cuaderno oficial de Seguros El Potosí 2025.")

# -------------------------- BLOQUE DE VIDA GRUPO Y ACCIDENTES --------------------------
if tipo_bono == "Vida Grupo y Accidentes":
    prod_vida_grupo = st.number_input("Producción Vida Grupo (trimestral)", min_value=0.0, step=1000.0, format="%.2f")
    prod_accidentes = st.number_input("Producción Accidentes (trimestral)", min_value=0.0, step=1000.0, format="%.2f")
    siniestralidad = st.number_input("Siniestralidad % Vida Grupo / Accidentes", min_value=0.0, max_value=100.0, step=0.1)

    if st.button("Calcular Bonos"):
        resultados = []
        total_bono = 0

        # Bono Vida Grupo (trimestral)
        if prod_vida_grupo > 250000:
            bono_vida_grupo = prod_vida_grupo * 0.03
            resultados.append(("👥 Bono Vida Grupo", bono_vida_grupo, "Primas > $250,000, bono 3%. ✅"))
            total_bono += bono_vida_grupo
        else:
            resultados.append(("👥 Bono Vida Grupo", 0, "No aplica. Requiere mínimo $250,001. ❌"))

        # Bono Vida Grupo Anual
        if prod_vida_grupo >= 500000 and siniestralidad < 60:
            bono_anual_vg = prod_vida_grupo * 0.02
            resultados.append(("📅 Bono Anual Vida Grupo", bono_anual_vg, "Producción ≥ $500,000 y siniestralidad < 60%. ✅"))
            total_bono += bono_anual_vg
        else:
            resultados.append(("📅 Bono Anual Vida Grupo", 0, "No aplica bono anual. ❌"))

        # Bono Accidentes
        bono_acc = 0
        if prod_accidentes >= 400000:
            bono_acc = prod_accidentes * 0.10
            nota = "Bono 10% por > $400,000. ✅"
        elif prod_accidentes >= 300000:
            bono_acc = prod_accidentes * 0.06
            nota = "Bono 6% por > $300,000. ✅"
        elif prod_accidentes >= 200000:
            bono_acc = prod_accidentes * 0.04
            nota = "Bono 4% por > $200,000. ✅"
        else:
            nota = "No alcanza mínimo de $200,000. ❌"
        resultados.append(("🧯 Bono Accidentes", bono_acc, nota))
        total_bono += bono_acc

        # Bono Anual Accidentes
        if prod_accidentes >= 500000 and siniestralidad < 60:
            bono_anual_acc = prod_accidentes * 0.05
            resultados.append(("📅 Bono Anual Accidentes", bono_anual_acc, "Producción ≥ $500,000 y siniestralidad < 60%. ✅"))
            total_bono += bono_anual_acc
        else:
            resultados.append(("📅 Bono Anual Accidentes", 0, "No aplica bono anual. ❌"))

        # Mostrar resultados
        st.markdown("---")
        st.subheader(f"Resultados para {nombre}:")
        for concepto, monto, nota in resultados:
            st.write(f"**{concepto}**: {formato_pesos(monto)}")
            st.caption(f"{nota}")

        st.success(f"💰 Total Bono Acumulado: {formato_pesos(total_bono)}")
        st.caption("📌 Aplican restricciones y condiciones conforme al cuaderno oficial de Seguros El Potosí 2025.")
