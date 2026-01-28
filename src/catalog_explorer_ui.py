"""Catalog Explorer UI Component for Streamlit."""
import streamlit as st
import pandas as pd
import altair as alt
from src.catalog_explorer import (
    list_catalogs,
    list_schemas,
    list_tables,
    preview_table,
    get_numeric_columns,
    get_categorical_columns,
    get_datetime_columns,
)


def clean_table_name(v: str) -> str:
    """Clean table name from qualified format."""
    if v is None:
        return ''
    s = str(v).strip()
    s = s.strip('`"')
    if '.' in s:
        s = s.split('.')[-1]
    return s


def render_catalog_explorer(location: str = "sidebar"):
    """Render Databricks Catalog Explorer UI.
    
    Args:
        location: "sidebar" or "main" - where to render the explorer
    
    Returns:
        tuple: (selected_catalog, selected_schema, selected_table, df) or (None, None, None, None) if not selected
    """
    
    # Create container based on location
    if location == "sidebar":
        container = st.sidebar
    else:
        container = st
    
    with container.expander("📊 Data Catalog Explorer", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Refresh Catalogs", key=f"refresh_catalogs_{location}"):
                # Clear cache when user refreshes
                st.cache_data.clear()
                st.rerun()
        
        with col2:
            if st.button("🧪 Test Connection", key=f"test_conn_{location}"):
                try:
                    catalogs_df = list_catalogs()
                    st.success(f"✅ Connected! Found {len(catalogs_df)} catalogs")
                except Exception as e:
                    st.error(f"❌ Connection failed: {e}")
        
        # Initialize session state for explorer
        if f"explorer_catalog_{location}" not in st.session_state:
            st.session_state[f"explorer_catalog_{location}"] = None
        if f"explorer_schema_{location}" not in st.session_state:
            st.session_state[f"explorer_schema_{location}"] = None
        if f"explorer_table_{location}" not in st.session_state:
            st.session_state[f"explorer_table_{location}"] = None
        
        # Load catalogs
        try:
            catalogs_df = list_catalogs()
            if catalogs_df.empty:
                catalogs = []
            else:
                for col_name in ("catalog_name", "catalog", "name", "catalogs"):
                    if col_name in catalogs_df.columns:
                        catalogs = catalogs_df[col_name].astype(str).tolist()
                        break
                else:
                    catalogs = catalogs_df.iloc[:, 0].astype(str).tolist()
        except Exception as e:
            st.error(f"Error loading catalogs: {e}")
            return None, None, None, None
        
        selected_catalog = st.selectbox(
            "📁 Catalog",
            options=catalogs,
            key=f"catalog_{location}",
            index=catalogs.index(st.session_state.get(f"explorer_catalog_{location}")) 
                  if st.session_state.get(f"explorer_catalog_{location}") in catalogs else 0
        )
        st.session_state[f"explorer_catalog_{location}"] = selected_catalog
        
        # Load schemas
        schemas = []
        if selected_catalog:
            try:
                schemas_df = list_schemas(selected_catalog)
                if not schemas_df.empty:
                    schema_col = 'namespace_name' if 'namespace_name' in schemas_df.columns else (
                        'name' if 'name' in schemas_df.columns else schemas_df.columns[0]
                    )
                    schemas = schemas_df[schema_col].astype(str).tolist()
            except Exception as e:
                st.error(f"Error loading schemas: {e}")
        
        selected_schema = st.selectbox(
            "📋 Schema",
            options=schemas,
            key=f"schema_{location}",
            index=schemas.index(st.session_state.get(f"explorer_schema_{location}")) 
                  if st.session_state.get(f"explorer_schema_{location}") in schemas else 0
        )
        st.session_state[f"explorer_schema_{location}"] = selected_schema
        
        # Load tables
        tables = []
        if selected_catalog and selected_schema:
            try:
                tables_df = list_tables(selected_catalog, selected_schema)
                if not tables_df.empty:
                    cols_lc = {c.lower(): c for c in tables_df.columns}
                    candidate_keys = ['tablename', 'table_name', 'name', 'table', 'displayname', 'identifier']
                    chosen_col = None
                    for key in candidate_keys:
                        if key in cols_lc:
                            chosen_col = cols_lc[key]
                            break
                    if not chosen_col:
                        chosen_col = tables_df.columns[0]
                    
                    tables = [clean_table_name(x) for x in tables_df[chosen_col].astype(str).tolist()]
                    seen = set()
                    tables = [t for t in tables if t and not (t in seen or seen.add(t))]
            except Exception as e:
                st.error(f"Error loading tables: {e}")
        
        selected_table = st.selectbox(
            "📊 Table",
            options=tables,
            key=f"table_{location}",
            index=tables.index(st.session_state.get(f"explorer_table_{location}")) 
                  if st.session_state.get(f"explorer_table_{location}") in tables else 0
        )
        st.session_state[f"explorer_table_{location}"] = selected_table
        
        # Load and preview table
        df = None
        if selected_catalog and selected_schema and selected_table:
            try:
                df = preview_table(selected_catalog, selected_schema, selected_table, limit=200)
                st.success(f"✅ Loaded {len(df)} rows × {len(df.columns)} columns")
            except Exception as e:
                st.error(f"Error loading table: {e}")
                return selected_catalog, selected_schema, selected_table, None
        
        return selected_catalog, selected_schema, selected_table, df


def render_data_preview(df: pd.DataFrame, key_prefix: str = ""):
    """Render data preview section with table view."""
    if df is None or df.empty:
        st.info("No data to preview")
        return
    
    st.write(f"**Rows:** {len(df)} | **Columns:** {len(df.columns)}")
    st.dataframe(df, use_container_width=True)


def render_charts(df: pd.DataFrame, key_prefix: str = ""):
    """Render interactive chart builder with multiple chart types."""
    if df is None or df.empty:
        return
    
    st.subheader("📈 Data Visualization")
    
    numeric_cols = get_numeric_columns(df)
    categorical_cols = get_categorical_columns(df)
    datetime_cols = get_datetime_columns(df)
    
    chart_type = st.selectbox(
        "Chart Type",
        ["Scatter", "Line", "Area", "Bar", "Histogram", "Box"],
        key=f"{key_prefix}_chart_type"
    )
    
    try:
        if chart_type in ("Scatter", "Line", "Area"):
            x_options = categorical_cols + datetime_cols
            y_options = numeric_cols
            
            if not x_options or not y_options:
                st.info("Need categorical/datetime X-axis and numeric Y-axis for this chart")
                return
            
            xcol = st.selectbox("X-axis", x_options, key=f"{key_prefix}_x")
            ycol = st.selectbox("Y-axis", y_options, key=f"{key_prefix}_y")
            color_col = st.selectbox("Color (optional)", [""] + categorical_cols, key=f"{key_prefix}_color")
            
            if chart_type == "Line":
                chart = alt.Chart(df).mark_line()
            elif chart_type == "Area":
                chart = alt.Chart(df).mark_area()
            else:
                chart = alt.Chart(df).mark_circle()
            
            enc = {
                'x': alt.X(f"{xcol}", type='temporal' if xcol in datetime_cols else 'quantitative'),
                'y': alt.Y(f"{ycol}", type='quantitative'),
            }
            
            if color_col:
                enc['color'] = alt.Color(f"{color_col}")
            
            chart = chart.encode(**enc, tooltip=list(df.columns)).interactive()
            st.altair_chart(chart, use_container_width=True)
        
        elif chart_type == "Bar":
            if not categorical_cols:
                st.info("Need at least one categorical column for bar charts")
                return
            
            xcol = st.selectbox("X-axis (category)", categorical_cols, key=f"{key_prefix}_bar_x")
            ycol = st.selectbox("Y-axis (numeric, optional)", [""] + numeric_cols, key=f"{key_prefix}_bar_y")
            agg = st.selectbox("Aggregation", ["count", "sum", "mean", "median"], key=f"{key_prefix}_bar_agg")
            
            if ycol:
                if agg == "count":
                    chart = alt.Chart(df).mark_bar().encode(x=f"{xcol}:N", y="count()", tooltip=list(df.columns))
                else:
                    chart = alt.Chart(df).mark_bar().encode(
                        x=f"{xcol}:N",
                        y=alt.Y(f"{ycol}:Q", aggregate=agg),
                        tooltip=list(df.columns)
                    )
            else:
                chart = alt.Chart(df).mark_bar().encode(x=f"{xcol}:N", y="count()", tooltip=list(df.columns))
            
            st.altair_chart(chart, use_container_width=True)
        
        elif chart_type == "Histogram":
            if not numeric_cols:
                st.info("No numeric columns available for histogram")
                return
            
            col = st.selectbox("Column", numeric_cols, key=f"{key_prefix}_hist_col")
            bins = st.slider("Bins", 5, 200, 30, key=f"{key_prefix}_hist_bins")
            
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(f"{col}:Q", bin=alt.Bin(maxbins=bins)),
                y="count()",
                tooltip=[alt.Tooltip(f"{col}:Q")]
            )
            st.altair_chart(chart, use_container_width=True)
        
        elif chart_type == "Box":
            if not numeric_cols:
                st.info("No numeric columns available for box plot")
                return
            
            ycol = st.selectbox("Numeric column", numeric_cols, key=f"{key_prefix}_box_y")
            xcol = st.selectbox("Group by (optional)", [""] + categorical_cols, key=f"{key_prefix}_box_x")
            
            if xcol:
                chart = alt.Chart(df).mark_boxplot().encode(
                    x=f"{xcol}:N",
                    y=alt.Y(f"{ycol}:Q"),
                    tooltip=list(df.columns)
                )
            else:
                chart = alt.Chart(df).mark_boxplot().encode(
                    y=alt.Y(f"{ycol}:Q"),
                    tooltip=list(df.columns)
                )
            
            st.altair_chart(chart, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error building chart: {e}")


def render_full_explorer(title: str = "📊 Databricks Catalog Explorer", location: str = "main"):
    """Render complete explorer with preview and charts."""
    if location == "main":
        st.header(title)
    
    # Use sidebar for selection if location is main, else inline
    if location == "main":
        with st.sidebar.expander("🔍 Select Data", expanded=True):
            catalog, schema, table, df = render_catalog_explorer("sidebar")
    else:
        catalog, schema, table, df = render_catalog_explorer("sidebar")
    
    if catalog and schema and table and df is not None:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Catalog", catalog)
        with col2:
            st.metric("Schema", schema)
        with col3:
            st.metric("Table", table)
        
        st.divider()
        
        tab1, tab2 = st.tabs(["📋 Data Preview", "📈 Visualization"])
        
        with tab1:
            render_data_preview(df, location)
        
        with tab2:
            render_charts(df, location)
    else:
        st.info("Select a catalog, schema, and table from the sidebar to explore data")
