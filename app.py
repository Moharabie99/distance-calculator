import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Distance Calculator",
    page_icon="🗺️",
    layout="wide"
)

# Fixed points dictionary
SET_POINTS = {
    'Katameya': {'lat': 29.968090, 'lng': 31.347392},
    'Abou Rawash': {'lat': 30.04505223454618, 'lng': 31.095009339862553},
    'Asyut': {'lat': 27.18421, 'lng': 31.12678},
    'Beni Suef': {'lat': 29.03483, 'lng': 31.03717},
    'Luxor': {'lat': 25.6973, 'lng': 32.70985},
    'Minya': {'lat': 28.09237, 'lng': 30.80671},
    'Alex seiouf': {'lat': 31.239224, 'lng': 29.990279},
    'Alex Semoha': {'lat': 31.2065725, 'lng': 29.9564813},
    'Behera': {'lat': 30.997523, 'lng': 30.498518},
    'Mansuora': {'lat': 31.06637, 'lng': 31.416747},
    'Sharkeya': {'lat': 30.570121, 'lng': 31.564327},
    'Menofeya': {'lat': 30.542717, 'lng': 31.133244},
    'Tanta': {'lat': 30.758889, 'lng': 31.023436},
    'Ismailia SD': {'lat': 30.6121456, 'lng': 32.2197934},
    'Kafr El Shiekh': {'lat': 31.16529, 'lng': 30.876114}
}

# Custom CSS matching the previous app
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #e4d9f5 0%, #f0e8ff 50%, #e8f4f8 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    div[data-testid="stExpander"], .stTabs {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 25px rgba(74, 0, 112, 0.08);
        border: 1px solid rgba(74, 0, 112, 0.05);
        margin-bottom: 20px;
    }
    
    .success-box {
        padding: 1.2rem;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 5px solid #28a745;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.2);
    }
    
    .info-box {
        padding: 1.2rem;
        background: linear-gradient(135deg, #e4d9f5 0%, #d1ecf1 100%);
        border-left: 5px solid #4a0070;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(74, 0, 112, 0.2);
    }
    
    .warning-box {
        padding: 1.2rem;
        background: linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%);
        border-left: 5px solid #ffc107;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255, 193, 7, 0.2);
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #4a0070, #2c5282) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 8px 25px rgba(74, 0, 112, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #370052, #1a365d) !important;
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(74, 0, 112, 0.4) !important;
    }
    
    .stDownloadButton>button {
        background: linear-gradient(135deg, #28a745, #20c997) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 6px 20px rgba(40, 167, 69, 0.3) !important;
    }
    
    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #218838, #17a2b8) !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(40, 167, 69, 0.4) !important;
    }
    
    .stFileUploader {
        background: white;
        border-radius: 15px;
        padding: 20px;
        border: 2px dashed #4a0070;
        box-shadow: 0 4px 15px rgba(74, 0, 112, 0.1);
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #4a0070, #2c5282) !important;
    }
    
    .stSelectbox {
        background: white;
        border-radius: 10px;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #3d005e;
    }
    
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(74, 0, 112, 0.1);
    }
    
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #4a0070, transparent);
    }
    
    h1, h2, h3 {
        color: #3d005e;
        font-weight: 700;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .element-container {
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'calculation_mode' not in st.session_state:
    st.session_state.calculation_mode = None
if 'results_df' not in st.session_state:
    st.session_state.results_df = None

def detect_coordinate_columns(df):
    """Detect X and Y columns in the dataframe"""
    columns_lower = {col.lower(): col for col in df.columns}
    
    x_col = None
    y_col = None
    
    # Look for X column (longitude)
    for possible_x in ['x', 'lng', 'lon', 'longitude', 'long']:
        if possible_x in columns_lower:
            x_col = columns_lower[possible_x]
            break
    
    # Look for Y column (latitude)
    for possible_y in ['y', 'lat', 'latitude']:
        if possible_y in columns_lower:
            y_col = columns_lower[possible_y]
            break
    
    return x_col, y_col

def calculate_distance_osrm(lon1, lat1, lon2, lat2, retry=3):
    """Calculate distance and time using OSRM"""
    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
    
    for attempt in range(retry):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('routes'):
                    distance_km = data['routes'][0]['distance'] / 1000
                    duration_min = data['routes'][0]['duration'] / 60
                    return distance_km, duration_min
            time.sleep(0.5)  # Wait before retry
        except Exception as e:
            if attempt == retry - 1:
                return None, None
            time.sleep(1)
    
    return None, None

def calculate_batch_distances(fixed_point, coordinates_list, progress_bar, status_text):
    """Calculate distances from fixed point to multiple destinations"""
    results = []
    total = len(coordinates_list)
    
    for idx, (lng, lat, original_data) in enumerate(coordinates_list):
        status_text.text(f"Calculating distance {idx + 1} of {total}...")
        
        distance_km, duration_min = calculate_distance_osrm(
            fixed_point['lng'], 
            fixed_point['lat'],
            lng,
            lat
        )
        
        result = original_data.copy()
        result['Distance_KM'] = round(distance_km, 2) if distance_km else 'Error'
        result['Time_Minutes'] = round(duration_min, 2) if duration_min else 'Error'
        results.append(result)
        
        progress_bar.progress((idx + 1) / total)
        time.sleep(0.3)  # Be respectful to the free API
    
    return results

def calculate_sequential_distances(coordinates_list, progress_bar, status_text):
    """Calculate distances between consecutive points"""
    results = []
    total = len(coordinates_list) - 1
    
    for idx in range(len(coordinates_list) - 1):
        lng1, lat1, data1 = coordinates_list[idx]
        lng2, lat2, data2 = coordinates_list[idx + 1]
        
        status_text.text(f"Calculating route {idx + 1} to {idx + 2} of {len(coordinates_list)}...")
        
        distance_km, duration_min = calculate_distance_osrm(lng1, lat1, lng2, lat2)
        
        result = {
            'From_Point': idx + 1,
            'To_Point': idx + 2,
            'Distance_KM': round(distance_km, 2) if distance_km else 'Error',
            'Time_Minutes': round(duration_min, 2) if duration_min else 'Error'
        }
        
        # Add original data from the starting point
        for key, value in data1.items():
            if key not in ['Distance_KM', 'Time_Minutes']:
                result[f'From_{key}'] = value
        
        results.append(result)
        
        progress_bar.progress((idx + 1) / total)
        time.sleep(0.3)
    
    return results

def create_excel_output(df):
    """Create Excel file from dataframe"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Results')
    output.seek(0)
    return output

# Header
st.markdown("""
    <div style="
        display: flex;
        align-items: center;
        background: linear-gradient(135deg, #390856 0%, #4a0070 50%, #2c5282 100%);
        padding: 25px 40px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(74, 0, 112, 0.3);
        margin-bottom: 30px;
    ">
        <img src="https://iili.io/2c7elMQ.png" style="
            width: 90px;
            height: auto;
            margin-right: 25px;
            filter: drop-shadow(0 3px 6px rgba(255,255,255,0.1));
        ">
        <h1 style="
            font-size: 2.2rem;
            font-weight: 700;
            color: white;
            text-shadow: 0 3px 6px rgba(0,0,0,0.1);
            margin: 0;
        ">Distance Calculator</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="sub-header">Calculate distances and travel times using real road routes</div>', unsafe_allow_html=True)

# Mode Selection
st.subheader("Select Calculation Mode")

col1, col2 = st.columns(2)

with col1:
    if st.button("🎯 Fixed Point to Multiple Stores", use_container_width=True):
        st.session_state.calculation_mode = "fixed"
        st.session_state.results_df = None
        st.rerun()

with col2:
    if st.button("🔄 Sequential Route (Point to Point)", use_container_width=True):
        st.session_state.calculation_mode = "sequential"
        st.session_state.results_df = None
        st.rerun()

st.divider()

# Mode 1: Fixed Point to Multiple
if st.session_state.calculation_mode == "fixed":
    st.subheader("🎯 Fixed Point to Multiple Stores")
    st.markdown('<div class="info-box">Calculate distances from one fixed point to all stores in your Excel file</div>', unsafe_allow_html=True)
    
    # Select fixed point
    selected_point = st.selectbox(
        "Select Fixed Point",
        options=list(SET_POINTS.keys()),
        help="Choose the starting point for distance calculations"
    )
    
    st.caption(f"📍 Selected: {selected_point} (Lat: {SET_POINTS[selected_point]['lat']}, Lng: {SET_POINTS[selected_point]['lng']})")
    
    # Upload file
    uploaded_file = st.file_uploader(
        "Upload Excel file with store coordinates",
        type=['xlsx', 'xls', 'csv'],
        key="fixed_upload"
    )
    
    if uploaded_file:
        try:
            # Read file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.markdown(f'<div class="success-box">✅ File uploaded: {len(df)} rows</div>', unsafe_allow_html=True)
            
            # Detect coordinate columns
            x_col, y_col = detect_coordinate_columns(df)
            
            if x_col and y_col:
                st.markdown(f'<div class="success-box">✅ Detected coordinates: X = "{x_col}", Y = "{y_col}"</div>', unsafe_allow_html=True)
                
                # Show preview
                with st.expander("📋 Preview Data (first 10 rows)"):
                    st.dataframe(df.head(10), use_container_width=True)
                
                # Calculate button
                if st.button("🚀 Calculate Distances", type="primary"):
                    # Prepare data
                    coordinates_list = []
                    for idx, row in df.iterrows():
                        try:
                            lng = float(row[x_col])
                            lat = float(row[y_col])
                            original_data = row.to_dict()
                            coordinates_list.append((lng, lat, original_data))
                        except:
                            continue
                    
                    if coordinates_list:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Calculate
                        results = calculate_batch_distances(
                            SET_POINTS[selected_point],
                            coordinates_list,
                            progress_bar,
                            status_text
                        )
                        
                        # Create results dataframe
                        results_df = pd.DataFrame(results)
                        st.session_state.results_df = results_df
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        st.success("✅ Calculation complete!")
                    else:
                        st.error("❌ No valid coordinates found in the file")
            else:
                st.error("❌ Could not find 'X' and 'Y' columns. Please ensure your file has columns named 'X' (longitude) and 'Y' (latitude).")
        
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

# Mode 2: Sequential Route
elif st.session_state.calculation_mode == "sequential":
    st.subheader("🔄 Sequential Route (Point to Point)")
    st.markdown('<div class="info-box">Calculate distances between consecutive points in your file (row by row)</div>', unsafe_allow_html=True)
    
    # Upload file
    uploaded_file = st.file_uploader(
        "Upload Excel file with route points",
        type=['xlsx', 'xls', 'csv'],
        key="sequential_upload",
        help="Points will be processed in the order they appear in the file"
    )
    
    if uploaded_file:
        try:
            # Read file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.markdown(f'<div class="success-box">✅ File uploaded: {len(df)} points</div>', unsafe_allow_html=True)
            
            # Detect coordinate columns
            x_col, y_col = detect_coordinate_columns(df)
            
            if x_col and y_col:
                st.markdown(f'<div class="success-box">✅ Detected coordinates: X = "{x_col}", Y = "{y_col}"</div>', unsafe_allow_html=True)
                
                # Show preview
                with st.expander("📋 Preview Route (first 10 points)"):
                    st.dataframe(df.head(10), use_container_width=True)
                
                st.info(f"🛣️ This will calculate {len(df) - 1} route segments")
                
                # Calculate button
                if st.button("🚀 Calculate Route", type="primary"):
                    # Prepare data
                    coordinates_list = []
                    for idx, row in df.iterrows():
                        try:
                            lng = float(row[x_col])
                            lat = float(row[y_col])
                            original_data = row.to_dict()
                            coordinates_list.append((lng, lat, original_data))
                        except:
                            continue
                    
                    if len(coordinates_list) >= 2:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Calculate
                        results = calculate_sequential_distances(
                            coordinates_list,
                            progress_bar,
                            status_text
                        )
                        
                        # Create results dataframe
                        results_df = pd.DataFrame(results)
                        st.session_state.results_df = results_df
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        st.success("✅ Route calculation complete!")
                    else:
                        st.error("❌ Need at least 2 points to calculate a route")
            else:
                st.error("❌ Could not find 'X' and 'Y' columns. Please ensure your file has columns named 'X' (longitude) and 'Y' (latitude).")
        
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

# Display Results
if st.session_state.results_df is not None:
    st.divider()
    st.subheader("📊 Results")
    
    results_df = st.session_state.results_df
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Routes", len(results_df))
    
    with col2:
        total_distance = results_df['Distance_KM'].apply(lambda x: x if isinstance(x, (int, float)) else 0).sum()
        st.metric("Total Distance", f"{total_distance:.2f} KM")
    
    with col3:
        total_time = results_df['Time_Minutes'].apply(lambda x: x if isinstance(x, (int, float)) else 0).sum()
        st.metric("Total Time", f"{total_time:.2f} min")
    
    with col4:
        avg_distance = results_df['Distance_KM'].apply(lambda x: x if isinstance(x, (int, float)) else 0).mean()
        st.metric("Avg Distance", f"{avg_distance:.2f} KM")
    
    # Show results table
    st.dataframe(results_df, use_container_width=True)
    
    # Download button
    st.markdown("### 💾 Download Results")
    excel_data = create_excel_output(results_df)
    st.download_button(
        label="📥 Download Results as Excel",
        data=excel_data,
        file_name=f"distance_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# Footer
st.divider()
st.markdown("""
    <div style="
        text-align: center;
        padding: 30px 20px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        margin-top: 40px;
    ">
        <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">
            Distance Calculator | Powered by OSRM (OpenStreetMap Routing)
        </p>
    </div>
""", unsafe_allow_html=True)