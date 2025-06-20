
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Title & Header ---
st.markdown("<h1 style='text-align: center; color: cyan;'>🚗 Used Cars Explorer</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Analyze, Filter & Visualize cleaned dataset easily</h4>", unsafe_allow_html=True)
st.markdown("---")

# --- Load cleaned data ---
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_df.csv', index_col=0)
    df['car_age'] = 2025 - df['yearOfRegistration']
    return df

df = load_data()

# --- Sidebar filters ---
st.sidebar.header("🔧 Filter Options")

# Filter by brand
brands = sorted(df['brand'].dropna().unique())
selected_brand = st.sidebar.selectbox("Select Brand", options=["All"] + brands)
if selected_brand != "All":
    df = df[df['brand'] == selected_brand]

# Filter by fuel type
fuel_types = sorted(df['fuelType'].dropna().unique())
selected_fuel = st.sidebar.multiselect("Select Fuel Type(s)", fuel_types, default=fuel_types)
df = df[df['fuelType'].isin(selected_fuel)]

# Filter by car age
age_range = st.sidebar.slider("Select Car Age", min_value=int(df['car_age'].min()), max_value=int(df['car_age'].max()), value=(0, 30))
df = df[df['car_age'].between(age_range[0], age_range[1])]


# --- Main Area ---

# 1. Data Overview
st.subheader("🔍 Preview of Filtered Data")
st.dataframe(df.head(10))

# 2. Summary Stats
st.subheader("📊 Summary Statistics")
st.write(df.describe().T)

# 3. Price Distribution Plot
st.subheader("📈 Price Distribution")
fig_price = px.histogram(df, x='price', nbins=50, color_discrete_sequence=['#00BFC4'])
st.plotly_chart(fig_price)

# 4. Price by Vehicle Type
st.subheader("🚘 Price by Vehicle Type")
fig_box = px.box(df, x='vehicleType', y='price', color='vehicleType', title="Boxplot by Vehicle Type")
st.plotly_chart(fig_box)

# 5. Price vs. Car Age
st.subheader("📉 Price vs. Car Age")
fig_scatter = px.scatter(df, x='car_age', y='price', color='gearbox', size='powerPS',
                         title="Price vs. Car Age (colored by gearbox, sized by powerPS)", opacity=0.6)
st.plotly_chart(fig_scatter)

# 6. Most Common Models
st.subheader("🏷️ Most Common Car Models")
model_counts = df['model'].value_counts().head(10)
st.bar_chart(model_counts)

# 7. Vehicle Count by Fuel Type
st.subheader("⛽ Fuel Type Distribution")
fuel_counts = df['fuelType'].value_counts()
fig_fuel = px.pie(values=fuel_counts.values, names=fuel_counts.index, title="Fuel Type Share")
st.plotly_chart(fig_fuel)

# Footer
st.markdown("---")
st.caption("Made by Abdalla Gamal | Streamlit App for Cleaned Used Cars Dataset 🚗")
