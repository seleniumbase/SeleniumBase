# Desired capabilities example file for Selenoid Grid
#
# The same result can be achieved on the command-line with:
#     --cap-string='{"selenoid:options": {"enableVNC": true}}'

capabilities = {
    "screenResolution": "1280x1024x24",
    "selenoid:options": {
        "enableVNC": True,
        "enableVideo": False,
    },
}
