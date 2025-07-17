import streamlit as st
import numpy as np

# Chart yeast % values IDY
yeast_percents = np.array([
    0.006, 0.010, 0.016, 0.024, 0.032, 0.040,
    0.048, 0.056, 0.064, 0.096, 0.128, 0.160, 0.192, 0.224,
    0.256, 0.320
])

# Chart data (hours at given yeast %)
chart_data = {
    15.0: [139, 103, 71, 53, 43, 37, 32, 29, 26, 19, 16, 13, 12, 10, 9, 8],
    17.8: [98, 73, 50, 37, 30, 26, 23, 20, 18, 14, 11, 9, 8, 7, 7, 6],
    18.3: [92, 68, 47, 35, 28, 24, 21, 19, 17, 13, 10, 9, 8, 7, 6, 5],
    18.9: [86, 64, 44, 33, 27, 23, 20, 18, 16, 12, 10, 8, 7, 6, 6, 5],
    19.4: [80, 60, 41, 31, 25, 21, 19, 17, 15, 11, 9, 8, 7, 6, 5, 5],
    20.6: [66, 49, 34, 25, 20, 17, 15, 14, 12, 9, 7, 6, 6, 5, 4, 4],
    22.8: [46, 34, 24, 18, 14, 12, 11, 9, 9, 6, 5, 4, 4, 3, 3, 3],
    25.0: [34, 25, 17, 13, 10, 9, 8, 7, 6, 5, 4, 3, 3, 3, 2, 2],
    27.2: [26, 19, 13, 10, 8, 7, 6, 5, 5, 4, 3, 2, 2, 2, 2, 2],
    30.0: [19, 14, 10, 7, 6, 5, 4, 4, 4, 3, 2, 2, 2, 2, 2, 2]
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
    page_title="Pizza Dough Yeast Calculator",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🍕 Yeast Calculator")

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
    max_value=72.0,
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
