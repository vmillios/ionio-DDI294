import streamlit as st
import logging
import sys

# --- OpenTelemetry Imports ---
# NOTE: To run this, you must install the following packages:
# pip install streamlit opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc opentelemetry-instrumentation-logging
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
# from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OtlpGrpcLogExporter
# from opentelemetry.exporter.otlp.proto.grpc.exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.logging import LoggingInstrumentor

# --- Global Logger Setup ---
# Use a global flag to prevent re-initializing OTEL on every Streamlit rerun
if 'otel_setup_done' not in st.session_state:
    st.session_state.otel_setup_done = False

# --- OpenTelemetry Logging Setup Function ---
def setup_opentelemetry_logging():
    """Configures OpenTelemetry for logging and sets up standard Python logging."""
    if st.session_state.otel_setup_done:
        return

    st.session_state.otel_setup_done = True
    st.info("Configuring OpenTelemetry Logging...")
    
    # 1. Define Resource: Identifies the service in the observability backend
    resource = Resource.create({
        "service.name": "streamlit-boilerplate-app",
        "service.version": "1.0.0",
        "environment": "development"
    })

    # 2. Configure Logger Provider
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)

    # 3. Configure OTLP Exporter (sends logs to an OpenTelemetry Collector)
    otlp_exporter = OTLPLogExporter(
        endpoint="opentelemetry:4317",
        insecure=True
    )

    # 4. Attach Processor: Logs are batched before being sent
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_exporter))

    # 5. Instrument Python's Built-in Logging
    LoggingInstrumentor().instrument(set_logging_format=True)

    # 6. Optional: Add a standard Python console handler for visibility
    # Note: OTEL instrumentation handles the formatting if set_logging_format=True
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        "%(levelname)s [%(name)s] [%(asctime)s] - %(message)s"
    ))
    logging.root.addHandler(handler)
    logging.root.setLevel(logging.INFO)
    
    st.success("OpenTelemetry Logging is active. Logs are sent to OTLP and console.")

# Execute the setup function
setup_opentelemetry_logging()

# Get the standard Python logger
logger = logging.getLogger(__name__)

# --- Configuration and Page Setup ---
st.set_page_config(
    page_title="Streamlit Boilerplate App (OTEL)",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Header Section ---
logger.info("Application starting or refreshing.")
st.title("🔭 Streamlit with OpenTelemetry Logging")
st.markdown("""
A basic structure with integrated Python logging instrumented by OpenTelemetry.
Check your console/collector for logs related to interactions below.
""")
st.divider()

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("⚙️ App Controls")
    
    # Text Input
    user_name = st.text_input("Enter your name", "Guest")
    logger.info(f"User input received: Name set to '{user_name}'")

    # Slider Input
    slider_value = st.slider(
        "Select a value",
        min_value=0,
        max_value=100,
        value=50,
        step=5
    )
    logger.debug(f"Slider value is {slider_value}")
    
    st.info("The application logic below generates log records.")

# --- Main Content/Logic ---

st.header("📈 Application Output")

# Display current inputs
st.metric(label="Selected Value", value=slider_value)
st.metric(label="Current User", value=user_name)

# Conditional Output based on inputs
if slider_value > 75:
    logger.warning(f"High threshold reached: Slider value is {slider_value}")
    st.warning("The value is high! Consider scaling back.")
elif slider_value < 25:
    logger.info(f"Low threshold reached: Slider value is {slider_value}")
    st.success("The value is quite low. Everything is optimal.")
else:
    logger.info(f"Moderate range: Slider value is {slider_value}")
    st.info("Value is within the moderate range.")

st.divider()

# --- Button Triggered Action ---
st.subheader("Action Trigger")
# A button that only executes its logic when clicked
if st.button("Process Data"):
    logger.info(f"Processing data triggered by user: {user_name}")
    st.balloons()
    
    try:
        result = slider_value * 2
        st.success(f"Processing complete! Doubled value is: **{result}**")
        logger.info(f"Data processed successfully. Result: {result}")
        
        st.dataframe({
            'Parameter': ['Value A', 'Value B', 'Value C'],
            'Result': [result, result / 2, result * 1.5]
        })
    except Exception as e:
        logger.error(f"Error during data processing: {e}", exc_info=True)
        st.error("An error occurred during processing.")

st.caption("Application powered by Streamlit and instrumented with OpenTelemetry.")