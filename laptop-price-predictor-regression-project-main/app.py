import streamlit as st
import pandas as pd
import numpy as np
import pickle
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Load the trained model and data
@st.cache_resource
def load_model():
    try:
        df = pickle.load(open('df.pkl', 'rb'))
        pipe = pickle.load(open('pipe.pkl', 'rb'))
        return df, pipe
    except FileNotFoundError:
        st.error("Model files not found. Please run main.py first to train the model.")
        return None, None

def create_price_comparison_chart(predicted_price, specs):
    """Create a price comparison chart"""
    # Sample market prices for comparison (you can replace with actual data)
    market_prices = {
        'Budget': predicted_price * 0.6,
        'Your Prediction': predicted_price,
        'Premium': predicted_price * 1.4,
        'Market Average': predicted_price * 1.1
    }
    
    fig = go.Figure(data=[
        go.Bar(x=list(market_prices.keys()), 
               y=list(market_prices.values()),
               marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
    ])
    
    fig.update_layout(
        title="Price Comparison with Market Segments",
        xaxis_title="Category",
        yaxis_title="Price (Rs)",
        template="plotly_white"
    )
    
    return fig

def create_feature_importance_plot():
    """Create a feature importance visualization"""
    # This is a placeholder - you would need to extract feature importance from your model
    features = ['RAM', 'SSD', 'CPU Brand', 'GPU Brand', 'Screen PPI', 'Brand', 'Type', 'Weight']
    importance = [25, 20, 15, 12, 10, 8, 6, 4]  # Example values
    
    fig = px.bar(x=importance, y=features, orientation='h',
                 title="Feature Importance in Price Prediction",
                 labels={'x': 'Importance (%)', 'y': 'Features'})
    
    fig.update_traces(marker_color='#4ECDC4')
    fig.update_layout(template="plotly_white")
    
    return fig

def get_price_category(price):
    """Categorize the predicted price"""
    if price < 500:
        return "💰 Budget", "#27AE60"
    elif price < 1000:
        return "💼 Mid-Range", "#3498DB"
    elif price < 2000:
        return "🚀 High-End", "#9B59B6"
    else:
        return "🎯 Premium", "#E74C3C"

def get_recommendations(specs, predicted_price):
    """Generate recommendations based on specifications and predicted price"""
    recommendations = []
    
    if specs['RAM'] < 8:
        recommendations.append("💡 Consider upgrading to at least 8GB RAM for better performance")
    
    if specs['SSD'] == 0:
        recommendations.append("💡 Adding an SSD would significantly improve system responsiveness")
    
    if specs['PPI'] < 120:
        recommendations.append("💡 Higher PPI display would provide better visual experience")
    
    if predicted_price > 1500 and specs['CPU'].startswith('Intel Core i3'):
        recommendations.append("💡 For this price range, consider Intel Core i5 or i7 for better value")
    
    if not recommendations:
        recommendations.append("✅ Your configuration looks well-balanced!")
    
    return recommendations

def main():
    st.set_page_config(
        page_title="Laptop Price Predictor",
        page_icon="💻",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS with enhanced styling
    st.markdown("""
        <style>
        .main-header {
            font-size: 3.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 1rem;
            font-weight: bold;
            background: linear-gradient(45deg, #1f77b4, #4ECDC4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .prediction-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2.5rem;
            border-radius: 15px;
            margin: 2rem 0;
            color: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .specs-box {
            background-color: #ffa;
            padding: 1.5rem;
            color: #333;
            border-radius: 10px;
            border-left: 5px solid #4ECDC4;
            margin: 1rem 0;
        }
        .recommendation-box {
            background-color: #e8f8;
            padding: 1rem;
            border-radius: 10px;
            border-left: 5px solid #3498DB;
            margin: 0.5rem 0;
        }
        
        
        
        </style>
    """, unsafe_allow_html=True)
    
    # Header with enhanced design
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="main-header">💻 Laptop Price Predictor</h1>', unsafe_allow_html=True)
        st.markdown("### *Smart Price Estimation Using Machine Learning Made by Subhadip 🔥*")
    
    # Load model
    df, pipe = load_model()
    
    if df is None or pipe is None:
        st.warning("Please run the training script first to generate the model files.")
        return
    
    # Create tabs for better organization
    tab1, = st.tabs(["🎯 Price Prediction"])
    
    with tab1:
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.header("Specify Your Laptop")
            
            # Organized input sections
            with st.expander("🏢 Basic Information", expanded=True):
                company = st.selectbox('Brand', df['Company'].unique(), 
                                     help="Select the laptop manufacturer")
                type_name = st.selectbox('Type', df['TypeName'].unique(),
                                       help="Choose the laptop type/category")
            
            with st.expander("⚡ Performance", expanded=True):
                col1_perf, col2_perf = st.columns(2)
                with col1_perf:
                    ram = st.selectbox('RAM (GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64],
                                     index=3, help="System memory size")
                    cpu_brand = st.selectbox('CPU Brand', df['Cpu brand'].unique(),
                                           help="Processor manufacturer and series")
                with col2_perf:
                    ssd = st.selectbox('SSD Storage (GB)', [0, 128, 256, 512, 1024, 2048],
                                     index=2, help="Solid State Drive capacity")
                    hdd = st.selectbox('HDD Storage (GB)', [0, 128, 256, 512, 1024, 2048],
                                     index=0, help="Hard Disk Drive capacity")
            
            with st.expander("🖥️ Display", expanded=True):
                col1_disp, col2_disp = st.columns(2)
                with col1_disp:
                    touchscreen = st.selectbox('Touchscreen', ['No', 'Yes'],
                                             help="Touchscreen capability")
                    ips = st.selectbox('IPS Display', ['No', 'Yes'],
                                     help="IPS panel for better viewing angles")
                with col2_disp:
                    ppi = st.slider('Screen PPI', min_value=50, max_value=400, value=150,
                                  help="Pixels Per Inch - display sharpness")
            
            with st.expander("🔧 Additional Features", expanded=True):
                col1_add, col2_add = st.columns(2)
                with col1_add:
                    gpu_brand = st.selectbox('GPU Brand', df['Gpu brand'].unique(),
                                           help="Graphics card manufacturer")
                    os = st.selectbox('Operating System', df['os'].unique(),
                                    help="Pre-installed operating system")
                with col2_add:
                    weight = st.number_input('Weight (kg)', min_value=0.5, max_value=5.0, 
                                           value=2.0, step=0.1, help="Laptop weight")
        
        with col2:
            st.header("Price Prediction")
            
            # Prediction button with enhanced styling
            if st.button('🚀 Predict Laptop Price', type='primary', use_container_width=True):
                # Convert categorical inputs to numerical
                touchscreen_num = 1 if touchscreen == 'Yes' else 0
                ips_num = 1 if ips == 'Yes' else 0
                
                # Create query array
                query = np.array([company, type_name, ram, weight, touchscreen_num, ips_num, 
                                ppi, cpu_brand, hdd, ssd, gpu_brand, os])
                query = query.reshape(1, -1)
                
                # Create DataFrame with correct column names
                columns = ['Company', 'TypeName', 'Ram', 'Weight', 'Touchscreen', 'Ips', 'ppi', 
                          'Cpu brand', 'HDD', 'SSD', 'Gpu brand', 'os']
                query_df = pd.DataFrame(query, columns=columns)
                
                # Ensure correct data types
                query_df['Ram'] = query_df['Ram'].astype('int32')
                query_df['Weight'] = query_df['Weight'].astype('float32')
                query_df['Touchscreen'] = query_df['Touchscreen'].astype('int32')
                query_df['Ips'] = query_df['Ips'].astype('int32')
                query_df['ppi'] = query_df['ppi'].astype('float32')
                query_df['HDD'] = query_df['HDD'].astype('int32')
                query_df['SSD'] = query_df['SSD'].astype('int32')
                
                # Predict
                try:
                    predicted_log_price = pipe.predict(query_df)[0]
                    predicted_price = np.exp(predicted_log_price)
                    
                    # Get price category
                    price_category, color = get_price_category(predicted_price)
                    
                    # Display prediction with enhanced styling
                    st.markdown(f"""
                    <div class="prediction-box">
                        <h4 style="color: white; margin-bottom: 1rem;">Predicted Price</h4>
                        <h4 style="color: white; font-size: 3rem; margin: 0;">Rs {predicted_price:,.2f}</h4>
                        <div style="background-color: {color}; padding: 0.5rem 1rem; border-radius: 20px; display: inline-block; margin-top: 1rem;">
                            <strong style="color: white;">{price_category}</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Specifications summary
                    st.subheader("📋 Configuration Summary")
                    
                    specs_data = {
                        'Brand': company,
                        'Type': type_name,
                        'RAM': f"{ram} GB",
                        'CPU': cpu_brand,
                        'GPU': gpu_brand,
                        'SSD': f"{ssd} GB" if ssd > 0 else "None",
                        'HDD': f"{hdd} GB" if hdd > 0 else "None",
                        'Display': f"{ppi} PPI, IPS: {ips}, Touch: {touchscreen}",
                        'OS': os,
                        'Weight': f"{weight} kg"
                    }
                    
                    # Display specs in a nice layout
                    col_spec1, col_spec2 = st.columns(2)
                    for i, (key, value) in enumerate(specs_data.items()):
                        with col_spec1 if i % 2 == 0 else col_spec2:
                            st.markdown(f"""
                            <div class="specs-box">
                                <strong>{key}:</strong> {value}
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Recommendations
                    st.subheader("💡 Recommendations")
                    specs_for_rec = {'RAM': ram, 'SSD': ssd, 'PPI': ppi, 'CPU': cpu_brand}
                    recommendations = get_recommendations(specs_for_rec, predicted_price)
                    
                    for rec in recommendations:
                        st.markdown(f"""
                        <div class="recommendation-box">
                            {rec}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Price comparison chart
                    st.subheader("📊 Price Comparison")
                    fig = create_price_comparison_chart(predicted_price, specs_data)
                    st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"❌ Error in prediction: {str(e)}")
                    st.info("Please check if all fields are filled correctly.")
            
            # Placeholder when no prediction is made
            else:
                st.info("👆 Configure your laptop specifications on the left and click 'Predict Laptop Price' to see the estimated price.")
                
                # Feature importance visualization
                st.subheader("🔍 What Affects Laptop Prices?")
                fig_importance = create_feature_importance_plot()
                st.plotly_chart(fig_importance, use_container_width=True)

   
    

if __name__ == '__main__':
    main()