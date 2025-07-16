import streamlit as st

# Chart yeast % values
yeast_percents = [0.003, 0.006, 0.010, 0.021, 0.031, 0.042,
                  0.063, 0.094, 0.126, 0.168, 0.210, 0.252,
                  0.294, 0.336, 0.420]

# Chart data (partial sample — expand as desired!)
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

# --- Streamlit page config ---
st.set_page_config(
    page_title="Yeast Calculator",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- App UI ---
st.title("🍞 Instant Dry Yeast Calculator")

st.markdown("""
Enter your dough parameters to calculate how much Instant Dry Yeast (IDY) you need for your desired fermentation time.

Works great for cold fermentation planning!
""")

# Sliders for mobile-friendly input
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

# Find closest temp in chart
closest_temp = min(chart_data.keys(), key=lambda t: abs(t - temp_input))
row_hours = chart_data[closest_temp]

# Use mid yeast % as reference (≈0.100%)
mid_idx = len(row_hours) // 2
chart_hours = row_hours[mid_idx]
chart_yeast_pct = yeast_percents[mid_idx]

# Calculate required yeast %
yeast_pct_needed = chart_yeast_pct * (chart_hours / target_hours)
yeast_grams = yeast_pct_needed / 100 * flour_weight

# --- Display results ---
st.success(f"**Closest chart temperature:** {closest_temp} °C")
st.info(f"**Estimated IDY needed:** {yeast_pct_needed*100:.2f} % baker's percentage")
st.write(f"👉 For {int(flour_weight)} g flour → **{yeast_grams:.2f} g IDY**")

st.caption("Note: Based on partial fermentation chart. Always test and adjust for your flour, hydration, and conditions!")
