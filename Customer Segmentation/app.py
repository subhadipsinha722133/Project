import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Customer Segmentation App",
    page_icon="🛍️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .cluster-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 0.5rem 0;
    }
    .stPlot {
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)
st.sidebar.header("🛠️ Made By Subhadip")
# App title
st.markdown('<h1 class="main-header">🛍️ Mall Customer Segmentation Analysis</h1>', unsafe_allow_html=True)

# Load the dataset
@st.cache_data
def load_data():
    # Using the sample data structure you provided
    data = {
        'CustomerID': range(1, 201),
        'Gender': np.random.choice(['Male', 'Female'], 200),
        'Age': np.random.randint(18, 70, 200),
        'Annual Income (k$)': np.random.randint(15, 140, 200),
        'Spending Score (1-100)': np.random.randint(1, 100, 200)
    }
    return pd.DataFrame(data)

customer_data = load_data()

# Sidebar for parameters
with st.sidebar:
    st.header("⚙️ Clustering Parameters")
    n_clusters = st.slider("Number of clusters", min_value=2, max_value=10, value=5)
    random_state = st.number_input("Random state", min_value=0, value=42)
    
    st.header("📊 Visualization Settings")
    plot_size = st.slider("Plot size", min_value=6, max_value=12, value=8)
    show_centroids = st.checkbox("Show centroids", value=True)
    show_elbow = st.checkbox("Show elbow method", value=True)
    
    st.header("🔍 Data Selection")
    x_axis = st.selectbox(
        "X-axis feature",
        options=['Age', 'Annual Income (k$)', 'Spending Score (1-100)'],
        index=1
    )
    y_axis = st.selectbox(
        "Y-axis feature",
        options=['Age', 'Annual Income (k$)', 'Spending Score (1-100)'],
        index=2
    )

# Display data information
st.header("📊 Data Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Customers", len(customer_data))
with col2:
    gender_count = customer_data['Gender'].value_counts()
    st.metric("Gender Distribution", f"{gender_count['Female']}F, {gender_count['Male']}M")
with col3:
    st.metric("Average Age", f"{customer_data['Age'].mean():.1f} years")
with col4:
    st.metric("Average Income", f"${customer_data['Annual Income (k$)'].mean():.1f}k")

# Show data preview
st.subheader("Data Preview")
st.dataframe(customer_data.head(), use_container_width=True)

# Data information
st.subheader("Data Statistics")
st.write(customer_data.describe())

# Data preprocessing
X = customer_data[[x_axis, y_axis]].values

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Elbow method to find optimal clusters
if show_elbow:
    st.header("📈 Elbow Method Analysis")
    
    wcss = []
    max_clusters = min(11, len(customer_data))
    
    with st.spinner('Calculating optimal clusters...'):
        for i in range(1, max_clusters):
            kmeans = KMeans(n_clusters=i, init='k-means++', random_state=random_state)
            kmeans.fit(X_scaled)
            wcss.append(kmeans.inertia_)
    
    # Plot elbow graph
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(range(1, max_clusters), wcss, marker='o', linestyle='--')
    ax.set_xlabel('Number of Clusters')
    ax.set_ylabel('WCSS')
    ax.set_title('Elbow Method for Optimal Clusters')
    ax.grid(True)
    st.pyplot(fig)

# Perform K-means clustering
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=random_state)
y_kmeans = kmeans.fit_predict(X_scaled)

# Add cluster labels to the dataframe
customer_data['Cluster'] = y_kmeans

# Plot clusters
st.header("👥 Customer Clusters Visualization")

fig, ax = plt.subplots(figsize=(plot_size, plot_size))

# Define colors for clusters
colors = ['green', 'red', 'yellow', 'violet', 'blue', 'orange', 'purple', 'brown', 'pink', 'gray']

for i in range(n_clusters):
    ax.scatter(X[y_kmeans == i, 0], X[y_kmeans == i, 1], 
              s=50, c=colors[i % len(colors)], 
              label=f'Cluster {i+1}', alpha=0.7)

if show_centroids:
    # Transform centroids back to original scale for plotting
    centroids_original = scaler.inverse_transform(kmeans.cluster_centers_)
    ax.scatter(centroids_original[:, 0], centroids_original[:, 1], 
              s=200, c='black', marker='X', 
              label='Centroids', edgecolors='white')

ax.set_xlabel(x_axis)
ax.set_ylabel(y_axis)
ax.set_title('Customer Segments')
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Cluster analysis
st.header("📋 Cluster Analysis")

# Cluster statistics
cluster_stats = customer_data.groupby('Cluster').agg({
    'Age': 'mean',
    'Annual Income (k$)': 'mean',
    'Spending Score (1-100)': 'mean',
    'CustomerID': 'count'
}).rename(columns={'CustomerID': 'Count'})

cluster_stats['Age'] = cluster_stats['Age'].round(1)
cluster_stats['Annual Income (k$)'] = cluster_stats['Annual Income (k$)'].round(1)
cluster_stats['Spending Score (1-100)'] = cluster_stats['Spending Score (1-100)'].round(1)

st.subheader("Cluster Statistics")
st.dataframe(cluster_stats, use_container_width=True)

# Gender distribution per cluster
st.subheader("Gender Distribution per Cluster")
gender_cluster = pd.crosstab(customer_data['Cluster'], customer_data['Gender'])
st.dataframe(gender_cluster, use_container_width=True)

# Display customers by cluster
st.subheader("Customers by Cluster")
for cluster in range(n_clusters):
    with st.expander(f"Cluster {cluster + 1} - {len(customer_data[customer_data['Cluster'] == cluster])} customers"):
        cluster_data = customer_data[customer_data['Cluster'] == cluster]
        st.dataframe(cluster_data[['CustomerID', 'Gender', 'Age', 'Annual Income (k$)', 'Spending Score (1-100)']], 
                    use_container_width=True)

# Add 3D visualization for more advanced analysis
st.header("🔮 3D Cluster Visualization (Advanced)")

if st.checkbox("Show 3D clustering (may take a moment to load)"):
    from mpl_toolkits.mplot3d import Axes3D
    
    # Use three features for 3D clustering
    X_3d = customer_data[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']].values
    X_3d_scaled = StandardScaler().fit_transform(X_3d)
    
    # Perform K-means for 3D
    kmeans_3d = KMeans(n_clusters=n_clusters, init='k-means++', random_state=random_state)
    y_kmeans_3d = kmeans_3d.fit_predict(X_3d_scaled)
    
    # Create 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    for i in range(n_clusters):
        ax.scatter(X_3d[y_kmeans_3d == i, 0], X_3d[y_kmeans_3d == i, 1], X_3d[y_kmeans_3d == i, 2], 
                  s=50, c=colors[i % len(colors)], 
                  label=f'Cluster {i+1}', alpha=0.7)
    
    ax.set_xlabel('Age')
    ax.set_ylabel('Annual Income (k$)')
    ax.set_zlabel('Spending Score (1-100)')
    ax.set_title('3D Customer Segments')
    ax.legend()
    
    st.pyplot(fig)

# Download results
st.header("💾 Download Results")

csv = customer_data.to_csv(index=False)
st.download_button(
    label="Download segmented data as CSV",
    data=csv,
    file_name="customer_segmentation_results.csv",
    mime="text/csv"
)

# Add footer
st.markdown("---")
st.markdown("### 🎯 How to interpret the results:")
st.markdown("""
- **Elbow Method**: Look for the "elbow" point where the WCSS decrease slows down significantly
- **Clusters**: Each color represents a different customer segment
- **Centroids**: The black X marks show the center of each cluster
- **Cluster Statistics**: Understand the characteristics of each customer group
- **Use the results** to tailor marketing strategies for each customer segment
""")

st.markdown("### 📝 Cluster Characteristics Guide:")
st.markdown("""
- **High Income, High Spending**: Premium customers - target with luxury products
- **High Income, Low Spending**: Conservative spenders - convince with value propositions
- **Low Income, High Spending**: Budget-conscious but enthusiastic - offer deals and discounts
- **Low Income, Low Spending**: Minimalists - focus on essential products
- **Middle Income, Middle Spending**: Average customers - target with broad marketing
""")