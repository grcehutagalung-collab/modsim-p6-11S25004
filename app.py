"""
============================================================================
SIMULASI DISCRETE EVENT — PEMBAGIAN LEMBAR JAWABAN UJIAN
MODUL PRAKTIKUM 6 | VERIFICATION & VALIDATION (MODSIM)
============================================================================
Jalankan: streamlit run app_modsim_p6.py
============================================================================
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Simulasi Pembagian LJU", layout="wide")

st.title("📊 Simulasi Pembagian Lembar Jawaban Ujian")
st.write("Model: Single Server Queue (FIFO) — Discrete Event Simulation")

# =========================
# INPUT
# =========================
col1, col2 = st.columns(2)

with col1:
    N = st.number_input("Jumlah Mahasiswa", min_value=1, value=30)

with col2:
    seed = st.number_input("Random Seed", min_value=0, value=42)

# =========================
# SIMULASI
# =========================
np.random.seed(seed)

# waktu pelayanan (uniform 1-3 menit)
service_times = np.random.uniform(1, 3, N)

start_times = []
end_times = []
wait_times = []

current_time = 0

for i in range(N):
    start = current_time
    end = start + service_times[i]
    
    wait = start  # karena semua datang di waktu 0
    
    start_times.append(start)
    end_times.append(end)
    wait_times.append(wait)
    
    current_time = end

# =========================
# DATAFRAME
# =========================
df = pd.DataFrame({
    "Mahasiswa": range(1, N+1),
    "Waktu Pelayanan": service_times,
    "Mulai Dilayani": start_times,
    "Selesai Dilayani": end_times,
    "Waktu Tunggu": wait_times
})

# =========================
# METRICS
# =========================
total_time = end_times[-1]
avg_wait = np.mean(wait_times)
utilisasi = 100  # karena selalu sibuk

# =========================
# OUTPUT METRICS
# =========================
st.subheader("📌 Hasil Simulasi")

col1, col2, col3 = st.columns(3)

col1.metric("Total Waktu (menit)", f"{total_time:.2f}")
col2.metric("Rata-rata Waktu Tunggu", f"{avg_wait:.2f}")
col3.metric("Utilisasi Meja (%)", f"{utilisasi}")

# =========================
# TABEL
# =========================
st.subheader("📋 Detail Simulasi")
st.dataframe(df, use_container_width=True)

# =========================
# GANTT CHART
# =========================
st.subheader("📊 Visualisasi Proses (Gantt Chart)")

fig = go.Figure()

for i in range(N):
    fig.add_trace(go.Bar(
        x=[service_times[i]],
        y=[f"Mhs {i+1}"],
        base=[start_times[i]],
        orientation='h',
        name=f"Mhs {i+1}"
    ))

fig.update_layout(
    title="Timeline Pelayanan Mahasiswa",
    xaxis_title="Waktu (menit)",
    yaxis_title="Mahasiswa",
    barmode='stack',
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# HISTOGRAM
# =========================
st.subheader("📈 Distribusi Waktu Pelayanan")

fig2 = go.Figure()
fig2.add_trace(go.Histogram(x=service_times))

fig2.update_layout(
    title="Distribusi Waktu Pelayanan (Uniform 1–3 menit)",
    xaxis_title="Waktu",
    yaxis_title="Frekuensi"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# VERIFICATION CHECK
# =========================
st.subheader("✅ Verification Check")

if all(end_times[i] <= start_times[i+1] for i in range(N-1)):
    st.success("✔ Tidak ada overlap pelayanan (benar)")
else:
    st.error("❌ Ada kesalahan logika antrian")

if min(service_times) >= 1 and max(service_times) <= 3:
    st.success("✔ Distribusi waktu sesuai (1–3 menit)")
else:
    st.error("❌ Distribusi waktu tidak sesuai")

# =========================
# KESIMPULAN
# =========================
st.subheader("📌 Kesimpulan")

st.write(f"""
- Total waktu yang dibutuhkan: **{total_time:.2f} menit**
- Rata-rata waktu tunggu: **{avg_wait:.2f} menit**
- Sistem menunjukkan antrian FIFO dengan satu server
- Model telah memenuhi aspek **verification & validation sederhana**
""")