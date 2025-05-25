import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.special import erfc
import pandas as pd

# Set up the Streamlit page
st.set_page_config(page_title="Contaminant Transport Simulator", layout="centered")

st.title("💧 Contaminant Transport in Subsurface Layers")

st.markdown("""
This interactive simulator visualizes the transport of contaminants through a landfill or subsurface layers.
It includes features such as dispersion, sorption, and biodegradation.
""")

# User Inputs
C0 = st.slider("Initial Concentration C₀ (mg/L)", 10, 500, 100)
D = st.slider("Dispersion Coefficient D (cm²/day)", 1, 100, 10)
z_values = st.multiselect("Select Depths z (cm)", [10, 30, 50, 70, 90], default=[10, 50, 90])
t_max = st.slider("Simulation Time (days)", 10, 300, 100)
k = st.slider("Sorption/Decay Coefficient k (1/day)", 0.0, 0.2, 0.01)

# Time array
t = np.linspace(1, t_max, 200)

# Function to calculate concentration with sorption/decay

def concentration_profile(C0, D, z, t, k):
    return C0 * erfc(z / (2 * np.sqrt(D * t))) * np.exp(-k * t)

# Plotting
fig, ax = plt.subplots()
data_dict = {"Time (days)": t}
for z in z_values:
    C_t = concentration_profile(C0, D, z, t, k)
    ax.plot(t, C_t, label=f"Depth {z} cm")
    data_dict[f"Depth {z} cm"] = C_t

ax.set_title("Contaminant Concentration vs. Time")
ax.set_xlabel("Time (days)")
ax.set_ylabel("Concentration (mg/L)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# Data export option
df = pd.DataFrame(data_dict)
st.markdown("### 📥 Export Concentration Data")
st.download_button(
    label="Download Data as CSV",
    data=df.to_csv(index=False),
    file_name="contaminant_concentration.csv",
    mime="text/csv"
)

# Explanation Section
st.markdown("""
### 📘 Equation and Theory:
The model is based on the classical solution to 1D advection-dispersion with decay:

\[
C(z, t) = C_0 \cdot \text{erfc}\left(\frac{z}{2\sqrt{Dt}}\right) \cdot e^{-kt}
\]

Where:
- \( C_0 \): Initial concentration (mg/L)
- \( D \): Dispersion coefficient (cm²/day)
- \( z \): Depth (cm)
- \( t \): Time (days)
- \( k \): Sorption/decay coefficient (1/day)
- \( \text{erfc} \): Complementary error function

The exponential term models loss due to biodegradation or sorption.
""")
