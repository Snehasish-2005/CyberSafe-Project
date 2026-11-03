
import streamlit as st
from urllib.parse import urlparse
import ipaddress

# Page settings
st.set_page_config(
    page_title="CyberSafe - URL Checker",
    page_icon="🛡️",
    layout="centered"
)

# Website heading
st.title("🛡️ CyberSafe")
st.subheader("Phishing Awareness and URL Checker")

st.write(
    "Check a website URL for common suspicious signs "
    "and learn how to stay safe online."
)

st.warning(
    "Educational tool only. This checker uses basic rules. "
    "It does not connect to live threat databases."
)

# URL input
url_input = st.text_input(
    "Enter a website URL:",
    placeholder="example.com"
)

# Check button
if st.button("Check URL", type="primary"):

    if not url_input.strip():
        st.error("Please enter a website URL.")

    else:
        # Add HTTPS if no protocol is provided
        url = url_input.strip()

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        parsed_url = urlparse(url)
        hostname = parsed_url.hostname or ""

        score = 0
        reasons = []

        # Check HTTPS
        if parsed_url.scheme == "http":
            score += 2
            reasons.append("Website uses HTTP instead of HTTPS.")

        # Check IP address
        try:
            ipaddress.ip_address(hostname)
            score += 3
            reasons.append("Website uses an IP address instead of a domain name.")
        except ValueError:
            pass

        # Check suspicious words
        suspicious_words = [
            "login",
            "verify",
            "update",
            "secure",
            "account",
            "password",
            "banking",
            "confirm",
            "wallet",
            "signin"
        ]

        found_words = [
            word for word in suspicious_words
            if word in url.lower()
        ]

        if found_words:
            score += min(len(found_words), 3)
            reasons.append(
                "Suspicious words found: " + ", ".join(found_words)
            )

        # Check URL length
        if len(url) > 100:
            score += 2
            reasons.append("URL is unusually long.")

        # Display results
        st.divider()
        st.subheader("🔍 Scan Results")

        if score <= 1:
            st.success("🟢 LOW RISK")
            risk_level = "LOW"

        elif score <= 4:
            st.warning("🟡 MEDIUM RISK")
            risk_level = "MEDIUM"

        else:
            st.error("🔴 HIGH RISK")
            risk_level = "HIGH"

        st.write("**Website URL:**", url)
        st.write("**Risk score:**", score)
        st.write("**Risk level:**", risk_level)

        if reasons:
            st.write("### ⚠️ Warning Signs")

            for reason in reasons:
                st.write("- " + reason)

        else:
            st.info("No common suspicious signs were detected.")

        st.caption(
            "Important: LOW RISK does not mean a website is guaranteed safe."
        )

# Safety tips
st.divider()
st.subheader("🔐 Phishing Safety Tips")

st.write("1. Never share your passwords or OTP with anyone.")
st.write("2. Always check the website address before logging in.")
st.write("3. Avoid clicking unknown links in emails and messages.")
st.write("4. Use strong and unique passwords.")
st.write("5. Enable two-factor authentication (2FA).")

st.divider()

st.caption("CyberSafe | Student Minor Project | Cybersecurity Awareness")
