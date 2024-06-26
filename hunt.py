from flask import Flask, request, send_from_directory, jsonify
from datetime import datetime

app = Flask(__name__)

# Serve the static files from the mysite directory
@app.route('/')
def serve_index():
    return send_from_directory('mysite', 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('mysite', path)

# Endpoint to receive collected data from the client
@app.route('/collect', methods=['POST'])
def collect_data():
    data = request.json
    formatted_data = format_data(data)
    # Print the formatted data to the terminal
    print(formatted_data)
    # Save the formatted data to info.txt
    with open('info.txt', 'a') as f:
        f.write(formatted_data + '\n\n')  # Add two newline characters for separation
    return jsonify({"status": "success"}), 200

def format_data(data):
    formatted_data = (
        f"information\n"
        f"Date 📅: {datetime.now().strftime('%d %B %A %Y')} | Time ⏰: {datetime.now().strftime('%I:%M %p %Z')} 🌆\n"
        f"\n#######################################################\n"
        f"\nPublic IP Address         : {data.get('publicIpAddress', 'N/A')}\n"
        f"----------------------------------------------------------------------------------------------------------------------------\n"
        f"Private IP Address        : {data.get('privateIpAddress', 'N/A')}\n"
        f"----------------------------------------------------------------------------------------------------------------------------\n"
        f"Operating System          : {data.get('osName', 'N/A')}\n"
        f"----------------------------------------------------------------------------------------------------------------------------\n"
        f"CPU Architecture          : {data.get('cpuArchitecture', 'N/A')}\n"
        f"----------------------------------------------------------------------------------------------------------------------------\n"
        f"CPU Core                  : {data.get('cpuCore', 'N/A')}\n"
        f"----------------------------------------------------------------------------------------------------------------------------\n"
        f"GPU Vendor                : {data.get('gpuVendor', 'N/A')}\n"
        f"----------------------------------------------------------------------------------------------------------------------------\n"
        f"GPU Renderer              : {data.get('gpuRenderer', 'N/A')}\n"
        f"----------------------------------------------------------------------------------------------------------------------------\n"
        f"Device Manufacture/Brand  : {data.get('deviceVendor', 'N/A')}\n"
        f"----------------------------------------------------------------------------------------------------------------------------\n"
        f"Device Model              : {data.get('deviceModel', 'N/A')}\n"
        f"----------------------------------------------------------------------------------------------------------------------------\n"
        f"RAM                       : {data.get('ram', 'N/A')}\n"
        f"----------------------------------------------------------------------------------------------------------------------------\n"
        f"Browser Name              : {data.get('browserName', 'N/A')}\n"
        f"----------------------------------------------------------------------------------------------------------------------------\n"
        f"Browser Version           : {data.get('browserVersion', 'N/A')}\n"
        f"----------------------------------------------------------------------------------------------------------------------------\n"
        f"Engine                    : {data.get('engine', 'N/A')}\n"
        f"----------------------------------------------------------------------------------------------------------------------------\n"
        f"User Agent                : {data.get('userAgent', 'N/A')}\n"
        f"----------------------------------------------------------------------------------------------------------------------------\n"
        f"Language                  : {data.get('language', 'N/A')}\n"
        f"----------------------------------------------------------------------------------------------------------------------------\n"
        f"Time Zone                 : {data.get('timeZone', 'N/A')}\n"
        f"----------------------------------------------------------------------------------------------------------------------------\n"
        f"Battery : %?               : {data.get('battery', 'N/A')}\n"
        f"----------------------------------------------------------------------------------------------------------------------------\n"
        f"Charging.                 : {data.get('charging', 'N/A')}\n"
        f"\n#######################################################\n"
    )
    return formatted_data

if __name__ == '__main__':
    app.run(debug=True)
