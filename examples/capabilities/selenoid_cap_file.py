# Desired capabilities example file for Selenoid Grid
#
# The same result can be achieved on the command-line. Eg:
#     --cap-string='{"selenoid:options": {"enableVNC": true}}'

capabilities = {
    "acceptSslCerts": True,
    "acceptInsecureCerts": True,
    "screenResolution": "1920x1080x24",
    "selenoid:options": {
        "enableVNC": True,
        "enableVideo": False,
    },
}
