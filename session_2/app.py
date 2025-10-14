import streamlit as st
import time
from plyer import notification
import platform

st.set_page_config(page_title="Push Notification Demo", layout="centered")

st.title("Desktop Push Notification Demo")

st.info(
    "This app sends a **desktop notification** to the computer running the app "
    "after a specified delay. It simulates a backend push notification trigger."
)

# A form to gather user input
with st.form("notification_form"):
    st.write("### Configure Your Notification")

    delay_seconds = st.number_input(
        "Delay before sending (seconds)",
        min_value=0,
        max_value=60,
        value=5,
        step=1
    )

    notification_title = st.text_input(
        "Notification Title",
        value="Reminder"
    )

    notification_message = st.text_area(
        "Notification Message",
        value="This is your scheduled notification!"
    )

    submitted = st.form_submit_button("Schedule Notification")

if submitted:
    if platform.system() == "Linux":
        st.warning(
            "On Linux, you may need to install a notification backend.\n\n"
            "For Debian/Ubuntu: `sudo apt-get install libnotify-bin`\n\n"
            "For Fedora: `sudo dnf install libnotify`",
            icon="🐧"
        )

    with st.spinner(f"Waiting for {delay_seconds} seconds to send notification..."):
        time.sleep(delay_seconds)

    try:
        notification.notify(
            title=notification_title,
            message=notification_message,
            app_name='Streamlit Notifier',
            timeout=10  # Notification will disappear after 10 seconds
        )
        st.success("✅ Notification sent successfully!")
        st.balloons()
    except Exception as e:
        st.error(f"Error sending notification: {e}")
        st.error(
            "Could not send notification. Please ensure you have a notification "
            "system installed and configured on your machine."
        )
