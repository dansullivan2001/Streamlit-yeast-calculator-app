import streamlit as st
import numpy as np

# Chart yeast % values
yeast_percents = np.array([
    0.003, 0.006, 0.010, 0.021, 0.031, 0.042,
    0.063, 0.094, 0.126, 0.168, 0.210, 0.252,
    0.294, 0.336, 0.420
])

# Chart data (hours at given yeast %)
chart_data = {
    17.8: [162, 105, 78, 50, 40, 32, 28, 24, 20, 15, 12, 10, 9, 8, 6],
    18.3: [152, 98, 68, 47, 37, 31, 25, 21, 18, 14, 12, 9, 8, 8, 6],
    19.4: [133, 80, 64, 41, 31, 25, 21, 17, 15, 11, 9, 8, 7, 6, 5],
    20.6: [109, 65, 52, 33, 25, 20, 17, 14, 12, 9, 8, 6, 5, 5, 4],
    22.8: [76, 50, 34, 21, 18, 14, 12, 10, 9, 7, 6, 5, 4, 4, 3],
    24.9: [56, 36, 27, 15, 12, 10, 8, 7, 6, 5, 4, 3, 3, 3, 2],
    27.2: [42, 28, 18, 12, 9, 7, 6, 5, 5, 4, 3, 3, 2, 2, 2],
    30.0: [32, 19, 14, 10, 7, 5, 5, 4, 4, 3, 3, 2, 2, 2, 2]
}

# Conversion factors
# relative to IDY = 1.0
yeast_types = {
    "Instant Dry Yeast (IDY)": 1.0,
    "Active Dry Yeast (ADY)": 1.25,
    "Fresh Yeast": 3.0
}

# --- Streamlit UI ---
st.set_page_config(
    page_title="Yeast Calculator (2D Interpolation)",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🍞 Yeast Calculator (2D Interpolation)")

st.markdown("""
This calculator:
- interpolates both **temperature** and **time**
- supports multiple yeast types

So you get precise yeast predictions for any dough!
""")

temp_input = st.slider(
    "Dough Temperature (°C)",
    min_value=17.0,
    max_value=30.0,
    step=0.1,
    value=18.3
)

target_hours = st.slider(
    "Desired Fermentation Time (hours)",
    min_value=2.0,
    max_value=168.0,
    step=1.0,
    value=24.0
)

flour_weight = st.slider(
    "Flour Weight (grams)",
    min_value=100.0,
    max_value=5000.0,
    step=50.0,
    value=1000.0
)

yeast_choice = st.selectbox(
    "Select Yeast Type",
    list(yeast_types.keys())
)

# --- Interpolation logic ---

temps_sorted = sorted(chart_data.keys())

if temp_input <= temps_sorted[0]:
    t_low = t_high = temps_sorted[0]
elif temp_input >= temps_sorted[-1]:
    t_low = t_high = temps_sorted[-1]
else:
    for i in range(len(temps_sorted)-1):
        if temps_sorted[i] <= temp_input <= temps_sorted[i+1]:
            t_low = temps_sorted[i]
            t_high = temps_sorted[i+1]
            break

if t_low == t_high:
    interp_hours = np.array(chart_data[t_low])
else:
    y_low = np.array(chart_data[t_low])
    y_high = np.array(chart_data[t_high])
    factor = (temp_input - t_low) / (t_high - t_low)
    interp_hours = y_low + (y_high - y_low) * factor

# interpolate across time
idx = np.searchsorted(interp_hours[::-1], target_hours, side='left')
idx = len(interp_hours) - idx

if idx <= 0:
    yeast_needed_idy = yeast_percents[0]
elif idx >= len(interp_hours):
    yeast_needed_idy = yeast_percents[-1]
else:
    h_low = interp_hours[idx-1]
    h_high = interp_hours[idx]
    y_low = yeast_percents[idx-1]
    y_high = yeast_percents[idx]
    
    if h_high == h_low:
        yeast_needed_idy = y_low
    else:
        yeast_needed_idy = y_low + (y_high - y_low) * (h_low - target_hours) / (h_low - h_high)

# adjust for chosen yeast type
factor = yeast_types[yeast_choice]
yeast_needed = yeast_needed_idy * factor

yeast_grams = yeast_needed / 100 * flour_weight

# --- Display results ---
st.success(f"**Interpolated fermentation times at {temp_input:.1f}°C:**\n" +
           ", ".join(f"{h:.1f}" for h in interp_hours))

st.info(f"**Estimated {yeast_choice} needed:** {yeast_needed*100:.3f}% baker's percentage")

st.write(f"👉 For {int(flour_weight)} g flour → **{yeast_grams:.2f} g {yeast_choice}**")

st.caption("""
Remember:
- ADY is ~25% weaker than IDY
- Fresh yeast is ~3× the weight of IDY
Always test and adjust for your flour and kitchen environment.
""")
