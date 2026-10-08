import streamlit as st
import MetaTrader5 as mt5
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date, time, timezone, timedelta
import calendar


# ============================================================
# Global Settings
# ============================================================

BULLISH_CANDLE_COLOR = "#26A69A"
BEARISH_CANDLE_COLOR = "#EF5350"

LINE_1_COLOR = "#2196F3"
LINE_2_COLOR = "#FF9800"

CHART_BACKGROUND_COLOR = "#10151D"
GRID_COLOR = "#29313D"
TEXT_COLOR = "#B8C0CC"


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="MT5 / CSV Chart",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# MT5 Initialization
# ============================================================

if not mt5.initialize():

    st.error(
        f"MT5 initialization failed: {mt5.last_error()}"
    )

    st.stop()


# ============================================================
# Get Available Symbols
# ============================================================

symbols = mt5.symbols_get()

if symbols is None:

    st.error(
        f"Failed to retrieve symbols from MetaTrader 5: "
        f"{mt5.last_error()}"
    )

    mt5.shutdown()
    st.stop()


symbol_names = sorted(
    [symbol.name for symbol in symbols]
)


if not symbol_names:

    st.error(
        "No symbols were found in MetaTrader 5."
    )

    mt5.shutdown()
    st.stop()


# ============================================================
# Timeframe Mapping
# ============================================================

timeframe_map = {

    "M1": mt5.TIMEFRAME_M1,
    "M2": mt5.TIMEFRAME_M2,
    "M3": mt5.TIMEFRAME_M3,
    "M4": mt5.TIMEFRAME_M4,
    "M5": mt5.TIMEFRAME_M5,
    "M6": mt5.TIMEFRAME_M6,
    "M10": mt5.TIMEFRAME_M10,
    "M12": mt5.TIMEFRAME_M12,
    "M15": mt5.TIMEFRAME_M15,
    "M20": mt5.TIMEFRAME_M20,
    "M30": mt5.TIMEFRAME_M30,
    "H1": mt5.TIMEFRAME_H1,
    "H2": mt5.TIMEFRAME_H2,
    "H3": mt5.TIMEFRAME_H3,
    "H4": mt5.TIMEFRAME_H4,
    "H6": mt5.TIMEFRAME_H6,
    "H8": mt5.TIMEFRAME_H8,
    "H12": mt5.TIMEFRAME_H12,
    "D1": mt5.TIMEFRAME_D1,
    "W1": mt5.TIMEFRAME_W1,
    "MN1": mt5.TIMEFRAME_MN1

}


# ============================================================
# Gregorian Date Selector
# ============================================================

def gregorian_date_selector(
    label,
    key_prefix
):

    today = date.today()

    years = list(
        range(
            2000,
            2031
        )
    )

    default_year = today.year

    if default_year not in years:

        default_year = years[-1]


    months = list(
        range(
            1,
            13
        )
    )


    month_names = {

        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"

    }


    st.write(
        f"**{label}**"
    )


    col1, col2, col3 = st.columns(3)


    # --------------------------------------------------------
    # Year
    # --------------------------------------------------------

    with col1:

        selected_year = st.selectbox(

            "Year",

            years,

            index=years.index(
                default_year
            ),

            key=f"{key_prefix}_year"

        )


    # --------------------------------------------------------
    # Month
    # --------------------------------------------------------

    with col2:

        selected_month = st.selectbox(

            "Month",

            months,

            index=today.month - 1,

            format_func=lambda x:
                month_names[x],

            key=f"{key_prefix}_month"

        )


    # --------------------------------------------------------
    # Days in Month
    # --------------------------------------------------------

    days_in_month = calendar.monthrange(
        selected_year,
        selected_month
    )[1]


    days = list(
        range(
            1,
            days_in_month + 1
        )
    )


    default_day = min(
        today.day,
        days_in_month
    )


    # --------------------------------------------------------
    # Day
    # --------------------------------------------------------

    with col3:

        selected_day = st.selectbox(

            "Day",

            days,

            index=default_day - 1,

            key=f"{key_prefix}_day"

        )


    # --------------------------------------------------------
    # Return Gregorian Date
    # --------------------------------------------------------

    return date(
        selected_year,
        selected_month,
        selected_day
    )


# ============================================================
# Page Title
# ============================================================

st.title(
    "📊 MT5 / CSV Candlestick Chart"
)


# ============================================================
# Symbol, Timeframe and Display Type
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    default_symbol = (

        "XAUUSD_o"

        if "XAUUSD_o" in symbol_names

        else symbol_names[0]

    )


    symbol = st.selectbox(

        "Symbol",

        symbol_names,

        index=symbol_names.index(
            default_symbol
        )

    )


with col2:

    timeframe_name = st.selectbox(

        "Timeframe",

        list(
            timeframe_map.keys()
        ),

        index=4

    )


with col3:

    display_type = st.selectbox(

        "Display Type",

        [
            "Candlestick",
            "Line"
        ]

    )


# ============================================================
# Two Time Ranges - Always Enabled
# ============================================================

st.subheader(
    "Time Range Comparison"
)


range_col_1, range_col_2 = st.columns(
    2,
    gap="medium"
)


# ============================================================
# First Time Range
# ============================================================

with range_col_1:

    st.markdown(
        "### Chart 1"
    )


    # --------------------------------------------------------
    # Data Source
    # --------------------------------------------------------

    source_1 = st.selectbox(

        "Data Source",

        [
            "MetaTrader 5",
            "CSV File"
        ],

        key="source_1"

    )


    # --------------------------------------------------------
    # Gregorian Date
    # --------------------------------------------------------

    selected_date_1 = gregorian_date_selector(

        "Date (Gregorian)",

        "date_1"

    )


    # --------------------------------------------------------
    # Start / End Time
    # --------------------------------------------------------

    time_col_1, time_col_2 = st.columns(2)


    with time_col_1:

        start_time_1 = st.time_input(

            "Start Time",

            value=time(
                4,
                0,
                0
            ),

            key="start_time_1"

        )


    with time_col_2:

        end_time_1 = st.time_input(

            "End Time",

            value=time(
                8,
                0,
                0
            ),

            key="end_time_1"

        )


# ============================================================
# Second Time Range
# ============================================================

with range_col_2:

    st.markdown(
        "### Chart 2"
    )


    # --------------------------------------------------------
    # Data Source
    # --------------------------------------------------------

    source_2 = st.selectbox(

        "Data Source",

        [
            "MetaTrader 5",
            "CSV File"
        ],

        key="source_2"

    )


    # --------------------------------------------------------
    # Gregorian Date
    # --------------------------------------------------------

    selected_date_2 = gregorian_date_selector(

        "Date (Gregorian)",

        "date_2"

    )


    # --------------------------------------------------------
    # Start / End Time
    # --------------------------------------------------------

    time_col_1, time_col_2 = st.columns(2)


    with time_col_1:

        start_time_2 = st.time_input(

            "Start Time",

            value=time(
                4,
                0,
                0
            ),

            key="start_time_2"

        )


    with time_col_2:

        end_time_2 = st.time_input(

            "End Time",

            value=time(
                8,
                0,
                0
            ),

            key="end_time_2"

        )


# ============================================================
# CSV File Upload
# ============================================================

csv_file = None


if (
    source_1 == "CSV File"
    or source_2 == "CSV File"
):

    st.subheader(
        "CSV Data"
    )


    csv_file = st.file_uploader(

        "Upload CSV File",

        type=[
            "csv"
        ],

        key="csv_uploader",

        help=(
            "CSV must contain the following columns: "
            "Date, Open, High, Low, Close"
        )

    )


# ============================================================
# Broker Timezone
# ============================================================

broker_utc_offset = st.number_input(

    "Broker UTC Offset",

    min_value=-12.0,

    max_value=14.0,

    value=3.0,

    step=0.5,

    help=(
        "Enter the UTC offset of your broker server time."
    )

)


# ============================================================
# Validate First Time Range
# ============================================================

if start_time_1 >= end_time_1:

    st.error(
        "Start time of Chart 1 must be earlier than end time."
    )

    mt5.shutdown()
    st.stop()


# ============================================================
# Validate Second Time Range
# ============================================================

if start_time_2 >= end_time_2:

    st.error(
        "Start time of Chart 2 must be earlier than end time."
    )

    mt5.shutdown()
    st.stop()


# ============================================================
# Validate CSV File
# ============================================================

if (
    source_1 == "CSV File"
    or source_2 == "CSV File"
):

    if csv_file is None:

        st.info(
            "Please upload a CSV file to display data from the CSV source."
        )

        mt5.shutdown()
        st.stop()


# ============================================================
# Load CSV Data
# ============================================================

csv_data = None


if csv_file is not None:

    try:

        csv_data = pd.read_csv(

            csv_file,

            sep=None,

            engine="python"

        )


        # ----------------------------------------------------
        # Clean Column Names
        # ----------------------------------------------------

        csv_data.columns = [

            str(column).strip()

            for column in csv_data.columns

        ]


        # ----------------------------------------------------
        # Required Columns
        # ----------------------------------------------------

        required_columns = [

            "Date",
            "Open",
            "High",
            "Low",
            "Close"

        ]


        missing_columns = [

            column

            for column in required_columns

            if column not in csv_data.columns

        ]


        if missing_columns:

            st.error(

                "The CSV file is missing the following required "
                f"columns: {', '.join(missing_columns)}"

            )

            mt5.shutdown()
            st.stop()


        # ----------------------------------------------------
        # Parse Date
        # ----------------------------------------------------

        csv_data["Date"] = pd.to_datetime(

            csv_data["Date"],

            errors="coerce"

        )


        # ----------------------------------------------------
        # Convert OHLC to Numeric
        # ----------------------------------------------------

        for column in [

            "Open",
            "High",
            "Low",
            "Close"

        ]:

            csv_data[column] = pd.to_numeric(

                csv_data[column],

                errors="coerce"

            )


        # ----------------------------------------------------
        # Remove Invalid Rows
        # ----------------------------------------------------

        csv_data = csv_data.dropna(

            subset=[

                "Date",
                "Open",
                "High",
                "Low",
                "Close"

            ]

        ).copy()


        # ----------------------------------------------------
        # Sort by Date
        # ----------------------------------------------------

        csv_data = csv_data.sort_values(

            "Date"

        ).reset_index(

            drop=True

        )


        if csv_data.empty:

            st.error(
                "The CSV file does not contain valid OHLC data."
            )

            mt5.shutdown()
            st.stop()


    except Exception as e:

        st.error(
            f"Failed to read the CSV file: {e}"
        )

        mt5.shutdown()
        st.stop()


# ============================================================
# Select Symbol in MT5
# ============================================================

symbol_info = mt5.symbol_info(
    symbol
)


if symbol_info is None:

    st.error(
        f"Symbol '{symbol}' was not found."
    )

    mt5.shutdown()
    st.stop()


if not symbol_info.visible:

    if not mt5.symbol_select(
        symbol,
        True
    ):

        st.error(
            f"Failed to select symbol '{symbol}'."
        )

        mt5.shutdown()
        st.stop()


# ============================================================
# Broker Server Time
# ============================================================

broker_timezone = timezone(

    timedelta(
        hours=broker_utc_offset
    )

)


# ============================================================
# Function: Get MT5 Data
# ============================================================

def get_mt5_data(

    symbol,
    timeframe_name,
    selected_date,
    start_time,
    end_time,
    broker_timezone

):

    broker_start_datetime = datetime.combine(

        selected_date,
        start_time

    )


    broker_end_datetime = datetime.combine(

        selected_date,
        end_time

    )


    # --------------------------------------------------------
    # Convert Broker Time to UTC
    # --------------------------------------------------------

    start_datetime_utc = (

        broker_start_datetime

        .replace(
            tzinfo=broker_timezone
        )

        .astimezone(
            timezone.utc
        )

    )


    end_datetime_utc = (

        broker_end_datetime

        .replace(
            tzinfo=broker_timezone
        )

        .astimezone(
            timezone.utc
        )

    )


    # --------------------------------------------------------
    # Get Data From MT5
    # --------------------------------------------------------

    rates = mt5.copy_rates_range(

        symbol,

        timeframe_map[
            timeframe_name
        ],

        start_datetime_utc,

        end_datetime_utc

    )


    if rates is None:

        return None, (

            f"Failed to retrieve candle data: "
            f"{mt5.last_error()}"

        )


    if len(rates) == 0:

        return pd.DataFrame(), (

            f"No candle data was found for {symbol} "
            f"between {start_time.strftime('%H:%M:%S')} and "
            f"{end_time.strftime('%H:%M:%S')} "
            f"on {selected_date}."

        )


    # --------------------------------------------------------
    # Create DataFrame
    # --------------------------------------------------------

    df = pd.DataFrame(
        rates
    )


    # --------------------------------------------------------
    # Convert MT5 UTC Time to Broker Time
    # --------------------------------------------------------

    df["time"] = (

        pd.to_datetime(

            df["time"],

            unit="s",

            utc=True

        )

        .dt

        .tz_convert(
            broker_timezone
        )

    )


    # --------------------------------------------------------
    # Remove Timezone Information
    # --------------------------------------------------------

    df["time"] = (
        df["time"]
        .dt
        .tz_localize(None)
    )


    # --------------------------------------------------------
    # Filter Exact Broker Time Range
    # --------------------------------------------------------

    df = df[

        (df["time"] >= broker_start_datetime)

        &

        (df["time"] <= broker_end_datetime)

    ].copy()


    if df.empty:

        return pd.DataFrame(), (

            f"No candle data was found for {symbol} "
            f"between {start_time.strftime('%H:%M:%S')} and "
            f"{end_time.strftime('%H:%M:%S')} "
            f"on {selected_date}."

        )


    return df, None


# ============================================================
# Function: Get CSV Data
# ============================================================

def get_csv_data(

    csv_data,
    selected_date,
    start_time,
    end_time

):

    start_datetime = datetime.combine(

        selected_date,
        start_time

    )


    end_datetime = datetime.combine(

        selected_date,
        end_time

    )


    # --------------------------------------------------------
    # Filter CSV Data
    # --------------------------------------------------------

    df = csv_data[

        (csv_data["Date"] >= start_datetime)

        &

        (csv_data["Date"] <= end_datetime)

    ].copy()


    if df.empty:

        return pd.DataFrame(), (

            f"No CSV candle data was found between "
            f"{start_time.strftime('%H:%M:%S')} and "
            f"{end_time.strftime('%H:%M:%S')} "
            f"on {selected_date}."

        )


    # --------------------------------------------------------
    # Rename Date
    # --------------------------------------------------------

    df = df.rename(

        columns={
            "Date": "time"
        }

    )


    # --------------------------------------------------------
    # Keep Required Columns
    # --------------------------------------------------------

    df = df[

        [
            "time",
            "Open",
            "High",
            "Low",
            "Close"
        ]

    ].copy()


    # --------------------------------------------------------
    # Rename OHLC Columns
    # --------------------------------------------------------

    df = df.rename(

        columns={

            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close"

        }

    )


    # --------------------------------------------------------
    # Sort Data
    # --------------------------------------------------------

    df = df.sort_values(

        "time"

    ).reset_index(

        drop=True

    )


    return df, None


# ============================================================
# Function: Prepare Time Axis
# ============================================================

def add_time_label(df):

    if df is None or df.empty:

        return df


    df = df.copy()


    df["time_label"] = (
        df["time"]
        .dt
        .strftime("%H:%M")
    )


    return df


# ============================================================
# Function: Convert Close to Percentage Change
# ============================================================

def normalize_to_first_close(df):

    if df is None or df.empty:

        return df


    df = df.copy()


    first_close = (
        df["close"].iloc[0]
    )


    if first_close == 0:

        df["close"] = 0.0

        return df


    df["close"] = (

        (

            df["close"]
            /
            first_close

        )

        - 1.0

    ) * 100.0


    return df


# ============================================================
# Function: Calculate Pearson Correlation
# ============================================================

def calculate_pearson_correlation(

    df_1,
    df_2

):

    if df_1 is None or df_2 is None:

        return None


    if df_1.empty or df_2.empty:

        return None


    series_1 = (

        normalize_to_first_close(
            df_1
        )

        ["close"]

        .reset_index(
            drop=True
        )

    )


    series_2 = (

        normalize_to_first_close(
            df_2
        )

        ["close"]

        .reset_index(
            drop=True
        )

    )


    common_length = min(

        len(series_1),
        len(series_2)

    )


    if common_length < 2:

        return None


    series_1 = series_1.iloc[
        :common_length
    ]


    series_2 = series_2.iloc[
        :common_length
    ]


    correlation = series_1.corr(

        series_2,

        method="pearson"

    )


    if pd.isna(correlation):

        return None


    return float(
        correlation
    )


# ============================================================
# Function: Create Candlestick Chart
# ============================================================

def create_candlestick_chart(

    df,
    symbol,
    timeframe_name,
    selected_date,
    start_time,
    end_time,
    data_source,
    chart_number=None

):

    df = add_time_label(
        df
    )


    fig = go.Figure()


    # --------------------------------------------------------
    # Candlestick
    # --------------------------------------------------------

    fig.add_trace(

        go.Candlestick(

            x=df["time_label"],

            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],

            increasing=dict(

                line=dict(

                    color=BULLISH_CANDLE_COLOR,

                    width=1

                ),

                fillcolor=BULLISH_CANDLE_COLOR

            ),

            decreasing=dict(

                line=dict(

                    color=BEARISH_CANDLE_COLOR,

                    width=1

                ),

                fillcolor=BEARISH_CANDLE_COLOR

            ),

            name=data_source

        )

    )


    # --------------------------------------------------------
    # Chart Title
    # --------------------------------------------------------

    if chart_number is not None:

        chart_title = (

            f"{chart_number} - "
            f"{data_source} - "
            f"{symbol} - "
            f"{timeframe_name} - "
            f"{selected_date} - "
            f"{start_time.strftime('%H:%M:%S')} to "
            f"{end_time.strftime('%H:%M:%S')}"

        )

    else:

        chart_title = (

            f"{data_source} - "
            f"{symbol} - "
            f"{timeframe_name} - "
            f"{selected_date} - "
            f"{start_time.strftime('%H:%M:%S')} to "
            f"{end_time.strftime('%H:%M:%S')}"

        )


    # --------------------------------------------------------
    # Chart Layout
    # --------------------------------------------------------

    fig.update_layout(

        title=chart_title,

        xaxis_title="Time",

        yaxis_title="",

        xaxis_rangeslider_visible=False,

        height=360,

        margin=dict(

            l=20,
            r=20,
            t=45,
            b=20

        ),

        plot_bgcolor=CHART_BACKGROUND_COLOR,

        paper_bgcolor=CHART_BACKGROUND_COLOR,

        font=dict(

            color=TEXT_COLOR

        ),

        xaxis=dict(

            type="category",

            showgrid=True,

            gridcolor=GRID_COLOR,

            gridwidth=1,

            zeroline=False

        ),

        yaxis=dict(

            showgrid=True,

            gridcolor=GRID_COLOR,

            gridwidth=1,

            zeroline=False

        ),

        hovermode="x unified"

    )


    return fig


# ============================================================
# Function: Create Line Chart
# ============================================================

def create_line_chart(

    df_1,
    df_2,
    symbol,
    timeframe_name,
    source_1,
    source_2=None

):

    fig = go.Figure()


    # ========================================================
    # Pearson Correlation
    # ========================================================

    pearson_correlation = None


    if (

        df_1 is not None

        and not df_1.empty

        and df_2 is not None

        and not df_2.empty

    ):

        pearson_correlation = (

            calculate_pearson_correlation(

                df_1,
                df_2

            )

        )


    # --------------------------------------------------------
    # Chart 1
    # --------------------------------------------------------

    if df_1 is not None and not df_1.empty:

        df_1 = normalize_to_first_close(
            df_1
        )


        df_1 = add_time_label(
            df_1
        )


        fig.add_trace(

            go.Scatter(

                x=df_1["time_label"],

                y=df_1["close"],

                mode="lines",

                name="Chart 1",

                line=dict(

                    color=LINE_1_COLOR,

                    width=2

                ),

                hovertemplate=(

                    "<b>Chart 1</b><br>"
                    "Time: %{x}<br>"
                    "Change: %{y:.2f}%"
                    "<extra></extra>"

                )

            )

        )


    # --------------------------------------------------------
    # Chart 2
    # --------------------------------------------------------

    if df_2 is not None and not df_2.empty:

        df_2 = normalize_to_first_close(
            df_2
        )


        df_2 = add_time_label(
            df_2
        )


        fig.add_trace(

            go.Scatter(

                x=df_2["time_label"],

                y=df_2["close"],

                mode="lines",

                name="Chart 2",

                line=dict(

                    color=LINE_2_COLOR,

                    width=2

                ),

                hovertemplate=(

                    "<b>Chart 2</b><br>"
                    "Time: %{x}<br>"
                    "Change: %{y:.2f}%"
                    "<extra></extra>"

                )

            )

        )


    # --------------------------------------------------------
    # Chart Title
    # --------------------------------------------------------

    chart_title = (

        f"{symbol} - {timeframe_name} - "
        f"Line Comparison"

    )


    # --------------------------------------------------------
    # Chart Layout
    # --------------------------------------------------------

    fig.update_layout(

        title=chart_title,

        xaxis_title="Time",

        yaxis_title="Change from First Close (%)",

        height=360,

        margin=dict(

            l=20,
            r=20,
            t=45,
            b=20

        ),

        plot_bgcolor=CHART_BACKGROUND_COLOR,

        paper_bgcolor=CHART_BACKGROUND_COLOR,

        font=dict(

            color=TEXT_COLOR

        ),

        xaxis=dict(

            type="category",

            showgrid=True,

            gridcolor=GRID_COLOR,

            gridwidth=1,

            zeroline=False

        ),

        yaxis=dict(

            showgrid=True,

            gridcolor=GRID_COLOR,

            gridwidth=1,

            zeroline=True,

            zerolinecolor=GRID_COLOR,

            zerolinewidth=1

        ),

        hovermode="x unified",

        legend=dict(

            orientation="h",

            yanchor="bottom",

            y=1.01,

            xanchor="right",

            x=1

        )

    )


    # ========================================================
    # Display Pearson Correlation
    # ========================================================

    if pearson_correlation is not None:

        fig.add_annotation(

            xref="paper",

            yref="paper",

            x=0.01,

            y=0.97,

            xanchor="left",

            yanchor="top",

            text=(

                f"Pearson Correlation: "
                f"{pearson_correlation:.2f}"

            ),

            showarrow=False,

            font=dict(

                color=TEXT_COLOR,

                size=14

            ),

            bgcolor=CHART_BACKGROUND_COLOR,

            bordercolor=GRID_COLOR,

            borderwidth=1,

            borderpad=5

        )


    return fig


# ============================================================
# Function: Get Data Based on Selected Source
# ============================================================

def get_range_data(

    data_source,
    symbol,
    timeframe_name,
    selected_date,
    start_time,
    end_time,
    broker_timezone,
    csv_data

):

    if data_source == "MetaTrader 5":

        return get_mt5_data(

            symbol,
            timeframe_name,
            selected_date,
            start_time,
            end_time,
            broker_timezone

        )


    elif data_source == "CSV File":

        return get_csv_data(

            csv_data,
            selected_date,
            start_time,
            end_time

        )


    return pd.DataFrame(), (
        "Unknown data source."
    )


# ============================================================
# Get First Range Data
# ============================================================

df_1, error_1 = get_range_data(

    source_1,

    symbol,

    timeframe_name,

    selected_date_1,

    start_time_1,

    end_time_1,

    broker_timezone,

    csv_data

)


# ============================================================
# Get Second Range Data
# ============================================================

df_2, error_2 = get_range_data(

    source_2,

    symbol,

    timeframe_name,

    selected_date_2,

    start_time_2,

    end_time_2,

    broker_timezone,

    csv_data

)


# ============================================================
# Display Charts
# ============================================================

if display_type == "Candlestick":

    # ========================================================
    # Chart 1
    # ========================================================

    if error_1 is not None:

        if df_1 is None:

            st.error(
                error_1
            )

        else:

            st.warning(
                error_1
            )

    else:

        fig_1 = create_candlestick_chart(

            df_1,

            symbol,

            timeframe_name,

            selected_date_1,

            start_time_1,

            end_time_1,

            source_1,

            chart_number="Chart 1"

        )


        st.plotly_chart(

            fig_1,

            use_container_width=True,

            config={

                "displayModeBar": True,

                "scrollZoom": True

            }

        )


    # ========================================================
    # Chart 2
    # ========================================================

    if error_2 is not None:

        if df_2 is None:

            st.error(
                error_2
            )

        else:

            st.warning(
                error_2
            )

    else:

        fig_2 = create_candlestick_chart(

            df_2,

            symbol,

            timeframe_name,

            selected_date_2,

            start_time_2,

            end_time_2,

            source_2,

            chart_number="Chart 2"

        )


        st.plotly_chart(

            fig_2,

            use_container_width=True,

            config={

                "displayModeBar": True,

                "scrollZoom": True

            }

        )


# ============================================================
# Line Display
# ============================================================

elif display_type == "Line":

    first_valid = (

        error_1 is None

        and df_1 is not None

        and not df_1.empty

    )


    second_valid = (

        error_2 is None

        and df_2 is not None

        and not df_2.empty

    )


    # --------------------------------------------------------
    # Show Errors
    # --------------------------------------------------------

    if error_1 is not None:

        if df_1 is None:

            st.error(
                error_1
            )

        else:

            st.warning(
                error_1
            )


    if error_2 is not None:

        if df_2 is None:

            st.error(
                error_2
            )

        else:

            st.warning(
                error_2
            )


    # --------------------------------------------------------
    # Create Combined Line Chart
    # --------------------------------------------------------

    if first_valid or second_valid:

        line_df_1 = (
            df_1
            if first_valid
            else None
        )


        line_df_2 = (
            df_2
            if second_valid
            else None
        )


        fig_line = create_line_chart(

            line_df_1,

            line_df_2,

            symbol,

            timeframe_name,

            source_1,

            source_2

        )


        st.plotly_chart(

            fig_line,

            use_container_width=True,

            config={

                "displayModeBar": True,

                "scrollZoom": True

            }

        )


# ============================================================
# Shutdown MT5
# ============================================================

mt5.shutdown()