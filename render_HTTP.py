#  Copyright (c) 2024. @Aiseed
#  Author: Andrew Lee

def generate_html(farm_name, sensor_data, camera_data):
    html_header_str = """
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Smartfarm Daily Report</title>
                <style>
                    body {
                        background-color: #F5F8FA;
                        width: 100%;
                        font-family: Lato, sans-serif;
                        font-size: 18px;
                        margin: 0;
                        padding: 0;
                    }
                    #email {
                        width: 100%;
                    }
                    .header {
                        background-color: #00A4BD;
                        color: white;
                        text-align: center;
                        padding: 20px 0;
                    }
                    .content {
                        padding: 30px 60px;
                    }
                    .content h2 {
                        color: #333;
                    }
                    .content p {
                        color: #555;
                    }
                    .report-table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 20px;
                    }
                    .report-table th, .report-table td {
                        border: 1px solid #ddd;
                        padding: 10px;
                        text-align: left;
                    }
                    .report-table th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
        """

    num_devices = len(sensor_data)
    html_table = []
    # generate tables for each device (1 table per device)
    for device_name in sensor_data:
        table_str = f"""
                <h3>Device: {device_name}</h3>
                <table class="report-table">
                    <thead>
                        <tr>
                """
        # Generate table headers
        for key in sensor_data.get(device_name):
            table_str += f"<th>{key}</th>"
        table_str += "</tr>"
        table_str += "</thead>"
        table_str += "<tbody>"
        table_str += "<tr>"
        # Generate table rows
        for key in sensor_data.get(device_name):
            if key == "Datetime":
                table_str += f"<td>{sensor_data.get(device_name)[key].strftime("%Y-%m-%d %H:%M:%S")}</td>"
            else:
                table_str += f"<td>{str(sensor_data.get(device_name)[key])}</td>"
        table_str += "</tr>"
        table_str += "</tbody>"
        table_str += "</table>"
        html_table.append(table_str)

    # generate html body
    html_body_str = f"""
            <body>
                <div id="email">
                    <div class="header">
                        <h1>AISeed Daily Report</h1>
                    </div>
                    <div class="content">
                        <h2>Smartfarm Name: {farm_name}</h2>
                        <p>Number of devices: {num_devices}</p>
                        <h2>Sensor Data:</h2>
                        {"".join(html_table)}
                    </div>
                </div>
            </body>
        """

    html_string = f"""
        <!DOCTYPE html>
        <html lang="en">
            {html_header_str}
            {html_body_str}
        </html>
    """

    return html_string
