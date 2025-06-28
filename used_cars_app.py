
import streamlit as st
import pandas as pd
import plotly.express as px
import zipfile

st.markdown("<h1 style='text-align: center; color: cyan;'>🚗 Used Cars Explorer</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Analyze, Filter & Visualize cleaned dataset easily</h4>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def load_data():
    with zipfile.ZipFile('cleaned_df.zip') as z:
        with z.open('cleaned_df.csv') as f:
            df = pd.read_csv(f, index_col=0)
            df['car_age'] = 2025 - df['yearOfRegistration']
            return df

df = load_data()

# --- Sidebar filters ---
st.sidebar.header("🔧 Filter Options")

brands = sorted(df['brand'].dropna().unique())
selected_brand = st.sidebar.selectbox("Select Brand", options=["All"] + brands)
if selected_brand != "All":
    df = df[df['brand'] == selected_brand]

fuel_types = sorted(df['fuelType'].dropna().unique())
selected_fuel = st.sidebar.multiselect("Select Fuel Type(s)", fuel_types, default=fuel_types)
df = df[df['fuelType'].isin(selected_fuel)]

age_range = st.sidebar.slider("Select Car Age", min_value=int(df['car_age'].min()), max_value=int(df['car_age'].max()), value=(0, 30))
df = df[df['car_age'].between(age_range[0], age_range[1])]

st.subheader("🔍 Preview of Filtered Data")
st.dataframe(df.head(10))

st.subheader("📊 Summary Statistics")
st.write(df.describe().T)

st.subheader("📈 Price Distribution")
fig_price = px.histogram(df, x='price', nbins=50, color_discrete_sequence=['#00BFC4'])
st.plotly_chart(fig_price)

st.subheader("🚘 Price by Vehicle Type")
fig_box = px.box(df, x='vehicleType', y='price', color='vehicleType', title="Boxplot by Vehicle Type")
st.plotly_chart(fig_box)

df_scatter = df.dropna(subset=['car_age', 'price', 'gearbox', 'powerPS'])

df_scatter = df.dropna(subset=['car_age', 'price', 'gearbox', 'powerPS'])

st.subheader("🏷️ Most Common Car Models")
model_counts = df['model'].value_counts().head(10)
st.bar_chart(model_counts)

st.subheader("⛽ Fuel Type Distribution")
fuel_counts = df['fuelType'].value_counts()
fig_fuel = px.pie(values=fuel_counts.values, names=fuel_counts.index, title="Fuel Type Share")
st.plotly_chart(fig_fuel)

# Remove rows with non-positive or unrealistic powerPS
df_scatter = df_scatter[df_scatter['powerPS'] > 0]

st.subheader("📉 Price vs. Car Age")
fig_scatter = px.scatter(
    df_scatter,
    x='car_age',
    y='price',
    color='gearbox',
    size='powerPS',
    title="Price vs. Car Age (colored by gearbox, sized by powerPS)",
    opacity=0.6
)
st.plotly_chart(fig_scatter)


st.markdown("---")
st.caption("Made by Abdalla Gamal | Streamlit App for Cleaned Used Cars Dataset 🚗")
