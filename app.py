import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
from io import BytesIO
import folium
from streamlit_folium import folium_static

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

def create_excel_output(df):
    """Create Excel file from dataframe"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Results')
    output.seek(0)
    return output

# Initialize session state
if 'calculation_mode' not in st.session_state:
    st.session_state.calculation_mode = None
if 'results_df' not in st.session_state:
    st.session_state.results_df = None
if 'x_col' not in st.session_state:
    st.session_state.x_col = None
if 'y_col' not in st.session_state:
    st.session_state.y_col = None
if 'selected_fixed_point' not in st.session_state:
    st.session_state.selected_fixed_point = None
if 'route_geometries' not in st.session_state:
    st.session_state.route_geometries = None

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

def calculate_distance_osrm(lon1, lat1, lon2, lat2, retry=3, return_geometry=False):
    """
    Calculate distance and time using OSRM with actual road routes
    
    Returns:
        If return_geometry=False: (distance_km, duration_min)
        If return_geometry=True: (distance_km, duration_min, route_geometry)
    
    Note: This uses REAL ROAD ROUTING, not straight-line distance
    """
    # Use 'overview=full' to get the actual route geometry
    overview = 'full' if return_geometry else 'false'
    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview={overview}&geometries=geojson"
    
    for attempt in range(retry):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('routes'):
                    route = data['routes'][0]
                    distance_km = route['distance'] / 1000  # meters to km
                    duration_min = route['duration'] / 60    # seconds to minutes
                    
                    if return_geometry:
                        # Extract route coordinates
                        geometry = route['geometry']['coordinates']
                        # Convert from [lng, lat] to [lat, lng] for folium
                        route_coords = [[coord[1], coord[0]] for coord in geometry]
                        return distance_km, duration_min, route_coords
                    else:
                        return distance_km, duration_min
            elif response.status_code == 429:  # Rate limited
                time.sleep(1)  # Wait if rate limited
            else:
                time.sleep(0.2)
        except requests.exceptions.Timeout:
            if attempt < retry - 1:
                time.sleep(0.5)
            else:
                return (None, None, None) if return_geometry else (None, None)
        except Exception as e:
            if attempt == retry - 1:
                return (None, None, None) if return_geometry else (None, None)
            time.sleep(0.3)
    
    return (None, None, None) if return_geometry else (None, None)

def calculate_batch_distances(fixed_point, coordinates_list, progress_bar, status_text, return_routes=False):
    """Calculate distances from fixed point to multiple destinations"""
    results = []
    total = len(coordinates_list)
    failed_count = 0
    route_geometries = [] if return_routes else None
    
    for idx, (lng, lat, original_data) in enumerate(coordinates_list):
        status_text.text(f"Processing: {idx + 1}/{total} | Failed: {failed_count}")
        
        if return_routes:
            distance_km, duration_min, route_coords = calculate_distance_osrm(
                fixed_point['lng'], 
                fixed_point['lat'],
                lng,
                lat,
                return_geometry=True
            )
            if route_coords:
                route_geometries.append({
                    'route': route_coords,
                    'distance': distance_km,
                    'duration': duration_min
                })
        else:
            distance_km, duration_min = calculate_distance_osrm(
                fixed_point['lng'], 
                fixed_point['lat'],
                lng,
                lat
            )
        
        if distance_km is None:
            failed_count += 1
        
        result = original_data.copy()
        result['Distance_KM'] = round(distance_km, 2) if distance_km else 'Error'
        result['Time_Minutes'] = round(duration_min, 2) if duration_min else 'Error'
        result['Time_Hours'] = round(duration_min / 60, 2) if duration_min else 'Error'
        results.append(result)
        
        progress_bar.progress((idx + 1) / total)
        
        # Smart delay: only add minimal delay every 10 requests
        if (idx + 1) % 10 == 0:
            time.sleep(0.1)
    
    if return_routes:
        return results, failed_count, route_geometries
    return results, failed_count

def calculate_sequential_distances(coordinates_list, progress_bar, status_text, return_routes=False):
    """Calculate distances between consecutive points"""
    results = []
    total = len(coordinates_list) - 1
    failed_count = 0
    route_geometries = [] if return_routes else None
    
    for idx in range(len(coordinates_list) - 1):
        lng1, lat1, data1 = coordinates_list[idx]
        lng2, lat2, data2 = coordinates_list[idx + 1]
        
        status_text.text(f"Route {idx + 1}→{idx + 2} of {len(coordinates_list)} | Failed: {failed_count}")
        
        if return_routes:
            distance_km, duration_min, route_coords = calculate_distance_osrm(
                lng1, lat1, lng2, lat2, return_geometry=True
            )
            if route_coords:
                route_geometries.append({
                    'route': route_coords,
                    'distance': distance_km,
                    'duration': duration_min
                })
        else:
            distance_km, duration_min = calculate_distance_osrm(lng1, lat1, lng2, lat2)
        
        if distance_km is None:
            failed_count += 1
        
        result = {
            'From_Point': idx + 1,
            'To_Point': idx + 2,
            'Distance_KM': round(distance_km, 2) if distance_km else 'Error',
            'Time_Minutes': round(duration_min, 2) if duration_min else 'Error',
            'Time_Hours': round(duration_min / 60, 2) if duration_min else 'Error'
        }
        
        # Add original data from the starting point
        for key, value in data1.items():
            if key not in ['Distance_KM', 'Time_Minutes', 'Time_Hours']:
                result[f'From_{key}'] = value
        
        results.append(result)
        
        progress_bar.progress((idx + 1) / total)
        
        # Smart delay
        if (idx + 1) % 10 == 0:
            time.sleep(0.1)
    
    if return_routes:
        return results, failed_count, route_geometries
    return results, failed_count

def create_map_visualization(results_df, mode, route_geometries=None, fixed_point=None, x_col='X', y_col='Y'):
    """
    Create interactive map visualization with ACTUAL ROUTE PATHS
    
    route_geometries: List of actual route coordinates from OSRM
    """
    
    # Determine map center
    if mode == "fixed":
        center_lat = fixed_point['lat']
        center_lng = fixed_point['lng']
    else:
        # Use first point in sequential mode
        center_lat = results_df[f'From_{y_col}'].iloc[0] if f'From_{y_col}' in results_df.columns else 30.0444
        center_lng = results_df[f'From_{x_col}'].iloc[0] if f'From_{x_col}' in results_df.columns else 31.2357
    
    # Create map
    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    if mode == "fixed":
        # Add fixed point marker (big star)
        folium.Marker(
            location=[fixed_point['lat'], fixed_point['lng']],
            popup=f"<b>Fixed Point: {fixed_point.get('name', 'Start')}</b>",
            icon=folium.Icon(color='red', icon='star', prefix='fa'),
            tooltip="Starting Point"
        ).add_to(m)
        
        # Add destination markers and ACTUAL ROUTES
        for idx, row in results_df.iterrows():
            if y_col in row and x_col in row:
                try:
                    lat = float(row[y_col])
                    lng = float(row[x_col])
                    distance = row.get('Distance_KM', 'N/A')
                    time_min = row.get('Time_Minutes', 'N/A')
                    time_hrs = row.get('Time_Hours', 'N/A')
                    
                    # Determine marker color based on TIME (not distance)
                    if isinstance(time_min, (int, float)):
                        if time_min < 30:  # Less than 30 minutes
                            color = 'green'
                        elif time_min < 90:  # 30-90 minutes
                            color = 'orange'
                        else:  # More than 90 minutes
                            color = 'red'
                    else:
                        color = 'gray'
                    
                    popup_text = f"""
                    <b>Store {idx + 1}</b><br>
                    <b style="color: #4a0070;">⏱️ Time: {time_min} min ({time_hrs} hrs)</b><br>
                    📏 Distance: {distance} KM
                    """
                    
                    folium.CircleMarker(
                        location=[lat, lng],
                        radius=6,
                        popup=popup_text,
                        color=color,
                        fill=True,
                        fillColor=color,
                        fillOpacity=0.7,
                        tooltip=f"Store {idx + 1}: {time_min} min"
                    ).add_to(m)
                    
                    # Draw ACTUAL ROUTE if available
                    if route_geometries and idx < len(route_geometries):
                        route_data = route_geometries[idx]
                        if route_data and route_data.get('route'):
                            folium.PolyLine(
                                locations=route_data['route'],
                                color=color,
                                weight=3,
                                opacity=0.7,
                                popup=f"Route: {distance} KM, {time_min} min",
                                tooltip=f"Click for details"
                            ).add_to(m)
                    else:
                        # Fallback: straight line with warning
                        folium.PolyLine(
                            locations=[[fixed_point['lat'], fixed_point['lng']], [lat, lng]],
                            color=color,
                            weight=2,
                            opacity=0.3,
                            dash_array='5, 10',  # Dashed line to show it's not actual route
                            popup="⚠️ Straight line (not actual route)"
                        ).add_to(m)
                except:
                    continue
    
    else:  # Sequential mode
        # Add route markers and ACTUAL ROUTE PATHS
        for idx, row in results_df.iterrows():
            try:
                from_lat = float(row[f'From_{y_col}'])
                from_lng = float(row[f'From_{x_col}'])
                
                distance = row.get('Distance_KM', 'N/A')
                time_min = row.get('Time_Minutes', 'N/A')
                time_hrs = row.get('Time_Hours', 'N/A')
                
                # Add marker for starting point
                folium.CircleMarker(
                    location=[from_lat, from_lng],
                    radius=7,
                    popup=f"<b>Point {row['From_Point']}</b>",
                    color='blue',
                    fill=True,
                    fillColor='blue',
                    fillOpacity=0.8,
                    tooltip=f"Point {row['From_Point']}"
                ).add_to(m)
                
                # Draw ACTUAL ROUTE if available
                if route_geometries and idx < len(route_geometries):
                    route_data = route_geometries[idx]
                    if route_data and route_data.get('route'):
                        folium.PolyLine(
                            locations=route_data['route'],
                            color='blue',
                            weight=4,
                            opacity=0.8,
                            popup=f"<b>Segment {idx + 1}</b><br>⏱️ {time_min} min ({time_hrs} hrs)<br>📏 {distance} KM",
                            tooltip=f"Segment {idx + 1}: {time_min} min"
                        ).add_to(m)
                
            except:
                continue
    
    return m

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
                    
                    # Show validation info
                    st.info("🛣️ **ROUTE-BASED CALCULATION**: Using actual driving routes (not straight lines)")
                    
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
                        
                        start_time = time.time()
                        
                        # Calculate WITH route geometries for map
                        results, failed, route_geoms = calculate_batch_distances(
                            SET_POINTS[selected_point],
                            coordinates_list,
                            progress_bar,
                            status_text,
                            return_routes=True  # Get actual route paths
                        )
                        
                        elapsed_time = time.time() - start_time
                        
                        # Create results dataframe
                        results_df = pd.DataFrame(results)
                        st.session_state.results_df = results_df
                        st.session_state.x_col = x_col
                        st.session_state.y_col = y_col
                        st.session_state.route_geometries = route_geoms
                        st.session_state.selected_fixed_point = {
                            'name': selected_point,
                            'lat': SET_POINTS[selected_point]['lat'],
                            'lng': SET_POINTS[selected_point]['lng']
                        }
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        if failed > 0:
                            st.warning(f"⚠️ Calculation complete with {failed} failures out of {len(coordinates_list)} requests")
                        else:
                            st.success(f"✅ Route-based calculation complete in {elapsed_time:.1f} seconds!")
                        
                        st.info(f"⚡ Speed: {len(coordinates_list)/elapsed_time:.1f} routes/second")
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
                    
                    st.info("🛣️ **ROUTE-BASED CALCULATION**: Using actual driving routes (not straight lines)")
                    
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
                        
                        start_time = time.time()
                        
                        # Calculate WITH route geometries
                        results, failed, route_geoms = calculate_sequential_distances(
                            coordinates_list,
                            progress_bar,
                            status_text,
                            return_routes=True
                        )
                        
                        elapsed_time = time.time() - start_time
                        
                        # Create results dataframe
                        results_df = pd.DataFrame(results)
                        st.session_state.results_df = results_df
                        st.session_state.x_col = x_col
                        st.session_state.y_col = y_col
                        st.session_state.route_geometries = route_geoms
                        
                        progress_bar.empty()
                        status_text.empty()
                        
                        if failed > 0:
                            st.warning(f"⚠️ Route calculation complete with {failed} failures")
                        else:
                            st.success(f"✅ Route-based calculation complete in {elapsed_time:.1f} seconds!")
                        
                        st.info(f"⚡ Speed: {len(results)/elapsed_time:.1f} segments/second")
                    else:
                        st.error("❌ Need at least 2 points to calculate a route")
            else:
                st.error("❌ Could not find 'X' and 'Y' columns. Please ensure your file has columns named 'X' (longitude) and 'Y' (latitude).")
        
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

    st.divider()
    st.subheader("📊 Results")
    
    results_df = st.session_state.results_df
    
    # Important notice
    st.markdown("""
    <div class="info-box">
        <b>✅ VERIFIED: Route-Based Calculations</b><br>
        All distances and times are calculated using <b>actual driving routes</b> on real roads,
        NOT straight-line distances. Times are based on typical driving speeds without real-time traffic.
    </div>
    """, unsafe_allow_html=True)
    
    # Summary metrics - PRIORITIZE TIME
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📍 Total Routes", len(results_df))
    
    with col2:
        total_time = results_df['Time_Minutes'].apply(lambda x: x if isinstance(x, (int, float)) else 0).sum()
        st.metric("⏱️ Total Time", f"{total_time:.1f} min")
    
    with col3:
        total_time_hrs = total_time / 60
        st.metric("🕐 Total Time", f"{total_time_hrs:.1f} hrs")
    
    with col4:
        total_distance = results_df['Distance_KM'].apply(lambda x: x if isinstance(x, (int, float)) else 0).sum()
        st.metric("📏 Total Distance", f"{total_distance:.1f} KM")
    
    # Show results table
    st.dataframe(results_df, use_container_width=True)
    
    # Map Visualization
    st.markdown("### 🗺️ Map Visualization - ACTUAL DRIVING ROUTES")
    
    try:
        if st.session_state.calculation_mode == "fixed" and st.session_state.selected_fixed_point:
            map_obj = create_map_visualization(
                results_df, 
                "fixed",
                st.session_state.route_geometries,
                st.session_state.selected_fixed_point,
                st.session_state.x_col,
                st.session_state.y_col
            )
        elif st.session_state.calculation_mode == "sequential":
            map_obj = create_map_visualization(
                results_df, 
                "sequential",
                st.session_state.route_geometries,
                None,
                st.session_state.x_col,
                st.session_state.y_col
            )
        
        folium_static(map_obj, width=1200, height=600)
        
        st.markdown("""
        <div class="success-box">
            <b>🎨 Map Legend (Color based on TRAVEL TIME):</b><br>
            🟢 <b>Green</b> = Under 30 minutes | 
            🟠 <b>Orange</b> = 30-90 minutes | 
            🔴 <b>Red</b> = Over 90 minutes<br>
            <br>
            <b>✅ Routes shown are ACTUAL DRIVING PATHS</b> following real roads, not straight lines!
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not generate map: {str(e)}")
        st.info("Map visualization requires valid coordinates in the results")
    
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
