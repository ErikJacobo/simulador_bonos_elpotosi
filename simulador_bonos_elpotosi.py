# Simulador de Bonos El Potosí 2025 en Streamlit
import streamlit as st

st.set_page_config(page_title="Simulador de Bonos El Potosí 2025", layout="centered")
st.title("Simulador de Bonos")
st.subheader("El Potosí 2025")

st.markdown("---")
nombre = st.text_input("👤 Nombre del Agente")

# Menú para seleccionar tipo de bono
tipo_bono = st.selectbox("Selecciona el tipo de bono a calcular:",
                         ["Selecciona...", "Autos", "Daños", "Vida Individual y Venta Masiva", "Vida Grupo y Accidentes"])

st.markdown("---")

# Función para formato de moneda
def formato_pesos(valor):
    return f"${valor:,.2f}" if valor else "$0.00"

resultados = []
total_bono = 0

# Mostrar solo los campos relacionados con el tipo seleccionado
def calcular_bonos_autos():
    prod_autos = st.number_input("Producción 2025 (Autos)", min_value=0.0, step=1000.0, format="%.2f", key="prod_autos")
    siniestralidad_autos = st.number_input("Siniestralidad % (Autos)", min_value=0.0, max_value=100.0, step=0.1, key="siniestralidad_autos")
    prod_2024_autos = st.number_input("Producción 2024 (Autos)", min_value=0.0, step=1000.0, format="%.2f", key="prod_2024_autos")
    agente_nuevo_autos = st.checkbox("Agente nuevo en Autos (alta en 2025 o < $300,000 en 2024)", key="agente_nuevo_autos")
    num_polizas_web_autos = st.number_input("Número de pólizas Autos emitidas por portal web", min_value=0, step=1, key="num_polizas_web_autos")

    resultados = []
    total_bono = 0

    # Bono de producción
    niveles_autos = [(5500000, 7.5), (4750000, 6.5), (3800000, 5.5), (2750000, 4.5), (1800000, 3.5),
                     (975000, 2.5), (500000, 1.5), (375000, 1.0)]
    bono_autos = 0
    explicacion_autos = ""
    for monto, porcentaje in niveles_autos:
        if prod_autos >= monto:
            bono_autos = prod_autos * (porcentaje / 100)
            explicacion_autos = f"Nivel alcanzado: {porcentaje}%."
            break
    if siniestralidad_autos > 80:
        bono_autos = 0
        explicacion_autos += " Siniestralidad mayor al 80%, bono no aplica. ❌"
    elif siniestralidad_autos > 70:
        bono_autos *= 0.5
        explicacion_autos += " Siniestralidad entre 70%-80%, aplica el 50%."
    elif siniestralidad_autos > 60:
        bono_autos *= 0.6
        explicacion_autos += " Siniestralidad entre 60%-70%, aplica el 60%."
    resultados.append(("🚗 Bono Producción Autos", bono_autos, explicacion_autos))
    total_bono += bono_autos

    # Bono crecimiento
    bono_crec_autos = 0
    if not agente_nuevo_autos and prod_2024_autos >= 300000:
        crecimiento = ((prod_autos - prod_2024_autos) / prod_2024_autos) * 100 if prod_2024_autos > 0 else 0
        if crecimiento >= 30:
            bono_crec_autos = prod_autos * 0.03
            resultados.append(("🚗 Bono Crecimiento Autos", bono_crec_autos, f"Crecimiento de {crecimiento:.2f}%, aplica 3%. ✅"))
            total_bono += bono_crec_autos

    # Bono novel
    if agente_nuevo_autos and prod_autos >= 375000:
        bono_novel_autos = prod_autos * 0.02
        resultados.append(("🚗 Bono Producción Agente Novel Autos", bono_novel_autos, "Agente nuevo con producción ≥ $375,000, aplica 2%. ✅"))
        total_bono += bono_novel_autos

    # Bono utilidad
    if prod_autos >= 1500000:
        sin = siniestralidad_autos
        niveles_utilidad = [(0, 20, 0.12), (20.01, 25, 0.10), (25.01, 30, 0.08), (30.01, 35, 0.06),
                            (35.01, 40, 0.05), (40.01, 45, 0.04), (45.01, 50, 0.03),
                            (50.01, 55, 0.02), (55.01, 60, 0.01), (60.01, 65, 0.005)]
        for min_sin, max_sin, porc in niveles_utilidad:
            if min_sin <= sin <= max_sin:
                bono_utilidad = prod_autos * porc
                resultados.append(("🚗 Bono Utilidad Anual Autos", bono_utilidad, f"Siniestralidad {sin:.2f}%, aplica {porc*100:.1f}%. ✅"))
                total_bono += bono_utilidad
                break

    # Bono web
    bono_web_autos = num_polizas_web_autos * 100
    resultados.append(("🚗 Bono Emisión Web Autos", bono_web_autos, f"{num_polizas_web_autos} pólizas emitidas. ✅"))
    total_bono += bono_web_autos

    return resultados, total_bono

# Puedes replicar esta función y lógica para daños, vida y grupo también

if tipo_bono == "Autos" and st.button("Calcular Bonos"):
    resultados, total_bono = calcular_bonos_autos()
    st.markdown("---")
    st.subheader(f"Resultados para {nombre}:")
    for concepto, monto, nota in resultados:
        st.write(f"**{concepto}**: {formato_pesos(monto)}")
        st.caption(f"{nota}")
    st.success(f"💰 Total Bono Acumulado: {formato_pesos(total_bono)}")
    st.caption("📌 Aplican restricciones y condiciones conforme al Cuaderno de Incentivos El Potosí 2025.")
    
# -------------------------------- DAÑOS --------------------------------
def calcular_bonos_danos():
    prod_danos = st.number_input("Producción 2025 (Daños)", min_value=0.0, step=1000.0, format="%.2f", key="prod_danos")
    siniestralidad_danos = st.number_input("Siniestralidad % (Daños)", min_value=0.0, max_value=100.0, step=0.1, key="siniestralidad_danos")
    prod_2024_danos = st.number_input("Producción 2024 (Daños)", min_value=0.0, step=1000.0, format="%.2f", key="prod_2024_danos")
    prod_casa_web = st.number_input("Producción CASA Web", min_value=0.0, step=1000.0, format="%.2f", key="prod_casa_web")

    resultados = []
    total_bono = 0

    # Bono de producción daños
    niveles_danos = [(2100000, 7), (1750000, 6), (1500000, 5), (1250000, 4), (900000, 3), (700000, 2), (300000, 1)]
    bono_danos = 0
    for monto, porcentaje in niveles_danos:
        if prod_danos >= monto:
            bono_danos = prod_danos * (porcentaje / 100)
            resultados.append(("🏠 Bono Producción Daños", bono_danos, f"Nivel alcanzado: {porcentaje}%. ✅"))
            break
    total_bono += bono_danos

    # Bono crecimiento daños
    bono_crec_danos = 0
    if prod_2024_danos > 0:
        crecimiento = ((prod_danos - prod_2024_danos) / prod_2024_danos) * 100
        if crecimiento >= 40:
            bono_crec_danos = (prod_danos - prod_2024_danos) * 0.09
        elif crecimiento >= 30:
            bono_crec_danos = (prod_danos - prod_2024_danos) * 0.06
        elif crecimiento >= 20:
            bono_crec_danos = (prod_danos - prod_2024_danos) * 0.03
        if bono_crec_danos:
            resultados.append(("📈 Bono Crecimiento Daños", bono_crec_danos, f"Crecimiento {crecimiento:.2f}%, aplica. ✅"))
            total_bono += bono_crec_danos

    # Bono CASA Web
    bono_casa_web = 0
    if prod_casa_web >= 150000:
        bono_casa_web = prod_casa_web * 0.08
    elif prod_casa_web >= 75000:
        bono_casa_web = prod_casa_web * 0.06
    elif prod_casa_web >= 30000:
        bono_casa_web = prod_casa_web * 0.04
    if bono_casa_web:
        resultados.append(("🌐 Bono CASA Web", bono_casa_web, "Producción CASA emitida por portal web. ✅"))
        total_bono += bono_casa_web

    return resultados, total_bono

if tipo_bono == "Daños" and st.button("Calcular Bonos"):
    resultados, total_bono = calcular_bonos_danos()
    st.markdown("---")
    st.subheader(f"Resultados para {nombre}:")
    for concepto, monto, nota in resultados:
        st.write(f"**{concepto}**: {formato_pesos(monto)}")
        st.caption(f"{nota}")
    st.success(f"💰 Total Bono Acumulado: {formato_pesos(total_bono)}")
    st.caption("📌 Aplican restricciones y condiciones conforme al Cuaderno de Incentivos El Potosí 2025.")

# -------------------------------- VIDA INDIVIDUAL Y VENTA MASIVA --------------------------------
def calcular_bonos_vida():
    prod_vida = st.number_input("Producción 2025 Vida (Primer Año)", min_value=0.0, step=1000.0, format="%.2f", key="prod_vida")
    conservacion = st.number_input("Índice de Conservación %", min_value=0.0, max_value=100.0, step=0.1, key="conservacion")
    num_negocios = st.number_input("Número de Negocios", min_value=0, step=1, key="num_negocios")
    agente_novel = st.checkbox("Agente nuevo en Vida", key="agente_nuevo_vida")

    resultados = []
    total_bono = 0

    # Bono de producción principal
    tabla_vida = [(2700000, 0.34), (2100000, 0.32), (1600000, 0.28), (1300000, 0.24), (920000, 0.18), (600000, 0.14),
                  (300000, 0.085), (160000, 0.065)]
    for prod_min, porc in tabla_vida:
        if prod_vida >= prod_min and conservacion >= 95 and num_negocios >= 4:
            bono_vida = prod_vida * porc
            resultados.append(("💼 Bono Producción Vida", bono_vida, f"Nivel {porc*100:.1f}%, conservación {conservacion}%, {num_negocios} negocios. ✅"))
            total_bono += bono_vida
            break

    # Bono adicional agente novel
    if agente_novel and num_negocios >= 4:
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

    return resultados, total_bono

if tipo_bono == "Vida Individual y Venta Masiva" and st.button("Calcular Bonos"):
    resultados, total_bono = calcular_bonos_vida()
    st.markdown("---")
    st.subheader(f"Resultados para {nombre}:")
    for concepto, monto, nota in resultados:
        st.write(f"**{concepto}**: {formato_pesos(monto)}")
        st.caption(f"{nota}")
    st.success(f"💰 Total Bono Acumulado: {formato_pesos(total_bono)}")
    st.caption("📌 Aplican restricciones y condiciones conforme al Cuaderno de Incentivos El Potosí 2025.")

# -------------------------------- VIDA GRUPO Y ACCIDENTES --------------------------------
def calcular_bonos_vida_grupo_y_acc():
    prod_vida_grupo = st.number_input("Producción Vida Grupo (trimestral)", min_value=0.0, step=1000.0, format="%.2f", key="vida_grupo")
    prod_accidentes = st.number_input("Producción Accidentes (trimestral)", min_value=0.0, step=1000.0, format="%.2f", key="accidentes")
    siniestralidad = st.number_input("Siniestralidad % Vida Grupo / Accidentes", min_value=0.0, max_value=100.0, step=0.1, key="siniestralidad_grupo")

    resultados = []
    total_bono = 0

    # Bono Vida Grupo (trimestral)
    if prod_vida_grupo > 250000:
        bono_vida_grupo = prod_vida_grupo * 0.03
        resultados.append(("👥 Bono Vida Grupo", bono_vida_grupo, "Primas > $250,000, bono 3%. ✅"))
        total_bono += bono_vida_grupo
    else:
        resultados.append(("👥 Bono Vida Grupo", 0, "No aplica. Requiere mínimo $250,001. ❌"))

    # Bono Vida Grupo anual (si producción > $500,000 y siniestralidad < 60%)
    if prod_vida_grupo >= 500000 and siniestralidad < 60:
        bono_anual_vg = prod_vida_grupo * 0.02
        resultados.append(("📅 Bono Anual Vida Grupo", bono_anual_vg, "Producción ≥ $500,000 y siniestralidad < 60%. ✅"))
        total_bono += bono_anual_vg

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

    return resultados, total_bono

if tipo_bono == "Vida Grupo y Accidentes" and st.button("Calcular Bonos"):
    resultados, total_bono = calcular_bonos_vida_grupo_y_acc()
    st.markdown("---")
    st.subheader(f"Resultados para {nombre}:")
    for concepto, monto, nota in resultados:
        st.write(f"**{concepto}**: {formato_pesos(monto)}")
        st.caption(f"{nota}")
    st.success(f"💰 Total Bono Acumulado: {formato_pesos(total_bono)}")
    st.caption("📌 Aplican restricciones y condiciones conforme al Cuaderno de Incentivos El Potosí 2025.")
