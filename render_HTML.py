#  Copyright (c) 2024. @Aiseed
#  Author: Andrew Lee

from datetime import datetime


def generate_latest_device_report(device_data, device_title="Sensord Device"):
    num_devices = len(device_data)
    html_table = []
    # generate tables for each device (1 table per device)
    for device_name in device_data:
        table_str = f"""
                 <li><h3 style="font-size: 17px;">Device: {device_name}</h3></li>
                    <table class="report-table">
                        <thead>
                            <tr>
                    """
        # if device_name has "Datetime" key, change this name to be "LastResponse"
        if "Datetime" in device_data.get(device_name):
            device_data.get(device_name)["LastResponse"] = device_data.get(device_name).pop("Datetime")
        # Generate table headers
        for key in device_data.get(device_name):
            table_str += f"<th>{key}</th>"
        table_str += "</tr>"
        table_str += "</thead>"
        table_str += "<tbody>"
        table_str += "<tr>"
        # Generate table rows
        for key in device_data.get(device_name):
            if key == "LastResponse":
                table_str += f"<td>{device_data.get(device_name)[key].strftime("%Y-%m-%d %H:%M:%S")}</td>"
            else:
                table_str += f"<td>{str(device_data.get(device_name)[key])}</td>"
        table_str += "</tr>"
        table_str += "</tbody>"
        table_str += "</table>"
        html_table.append(table_str)
    html_block = f"""
                    <h3>{device_title}:</h3>
                    <p>Number of devices: {num_devices}</p>
                    <ol>
                    {"".join(html_table)}
                    </ol>
                    """
    return html_block


def generate_report(farm_name, sensor_data, edge_data, title="AISeed Report"):
    html_header_str = """
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{title}</title>
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

    # generate sensor device report
    sensor_device_block = generate_latest_device_report(sensor_data, device_title="Sensor Device")
    # generate edge device report
    edge_device_block = generate_latest_device_report(edge_data, device_title="Edge Device")

    # generate html body
    html_body_str = f"""
            <body>
                <div id="email">
                    <div class="header">
                        <h1>{title}</h1>
                    </div>
                    <div class="content">
                        <h2>Smart Farm Name: {farm_name}</h2>
                        <p> <i> Report generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  </i> </p>
                        {"".join(sensor_device_block)}
                        <br>
                        {"".join(edge_device_block)}
                    </div>
                </div>
            </body>
        """

    html_string = f"""
            <!DOCTYPE html>
            <html lang="en">
                {html_header_str.replace("{title}", title)}
                {html_body_str}
            </html>
        """

    return html_string
