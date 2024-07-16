#  Copyright (c) 2024. @Aiseed
#  Author: Andrew Lee

from datetime import datetime


def generate_latest_device_report(device_data, device_title="Sensord Device"):
    num_devices = len(device_data)
    html_div = []
    # generate tables for each device (1 table per device)
    for device_name in device_data:
        device_section_str = f"""
                <div class="device-section">
                <div class="device-header">
                    <h2>Sensor Device: {device_name}</h2>
                </div>
                <div class="icon-grid">
                    """
        # if device_name has "Datetime" key, change this name to be "LastResponse"
        if "Sensor Device" in device_title and "Datetime" in device_data.get(device_name):
            device_data.get(device_name)["LastResponse"] = device_data.get(device_name).pop("Datetime")

        # Generate rows
        for key in device_data.get(device_name):
            if "humidity" in key.lower():
                device_section_str += f"""
                        <div class="icon-box humidity">
                            <i class="fas fa-tint"></i>
                            <div class="value">{str(round(device_data.get(device_name)[key], 2)) + "%" if device_data.get(device_name)[key] is not None else "None"}</div>
                            <div class="label">💧 Humidity</div>
                        </div>
                        """
            elif "sun" in key.lower():
                device_section_str += f"""
                        <div class="icon-box sun">
                            <i class="fas fa-sun"></i>
                            <div class="value">{str(round(device_data.get(device_name)[key], 2)) if device_data.get(device_name)[key] is not None else "None"}</div>
                            <div class="label">☀️ {key}</div>
                        </div>
                        """
            elif "ec" in key.lower():
                device_section_str += f"""
                        <div class="icon-box ec">
                            <i class="fas fa-flask"></i>
                            <div class="value">{str(round(device_data.get(device_name)[key], 2)) if device_data.get(device_name)[key] is not None else "None"}</div>
                            <div class="label">💧 EC</div>
                        </div>
                        """
            elif "ph" in key.lower():
                device_section_str += f"""
                        <div class="icon-box ph">
                            <i class="fas fa-vial"></i>
                            <div class="value">{str(round(device_data.get(device_name)[key], 2)) if device_data.get(device_name)[key] is not None else "None"}</div>
                            <div class="label">🧪 pH</div>
                        </div>
                        """
            elif "solid_temp" in key.lower():
                device_section_str += f"""
                        <div class="icon-box solid-temp">
                            <i class="fas fa-thermometer-half"></i>
                            <div class="value">{str(round(device_data.get(device_name)[key], 2)) + "°C" if device_data.get(device_name)[key] is not None else "None"}</div>
                            <div class="label">🌡️ Solid Temperature</div>
                        </div>
                        """
            elif "co2" in key.lower():
                device_section_str += f"""
                        <div class="icon-box co2">
                            <i class="fas fa-cloud"></i>
                            <div class="value">{str(round(device_data.get(device_name)[key], 2)) + "ppm" if device_data.get(device_name)[key] is not None else "None"}</div>
                            <div class="label">🌬️ CO2</div>
                        </div>
                        """
            elif "solid_moisture" in key.lower():
                device_section_str += f"""
                        <div class="icon-box solid-moisture">
                            <i class="fas fa-water"></i>
                            <div class="value">{str(round(device_data.get(device_name)[key], 2)) + "%" if device_data.get(device_name)[key] is not None else "None"}</div>
                            <div class="label">💦 Solid Moisture</div>
                        </div>
                        """
            elif "temp" in key.lower():
                device_section_str += f"""
                        <div class="icon-box temp">
                            <i class="fas fa-temperature-low"></i>
                            <div class="value">{str(round(device_data.get(device_name)[key], 2)) + "°C" if device_data.get(device_name)[key] is not None else "None"}</div>
                            <div class="label">🌡️ Temperature</div>
                        </div>
                        """
            elif "lastresponse" in key.lower():
                device_section_str += f"""
                        <div class="icon-box last-response">
                            <i class="fas fa-clock"></i>
                            <div class="value">{device_data.get(device_name)[key].strftime("%Y-%m-%d %H:%M:%S")}</div>
                            <div class="label">⏰ Last Response</div>
                        </div>
                        """
            elif "ip" in key.lower():
                device_section_str += f"""
                        <div class="icon-box ip">
                            <i class="fas fa-globe"></i>
                            <div class="value">{device_data.get(device_name)[key]}</div>
                            <div class="label">🌎 IP</div>
                        </div>
                        """
            elif "datetime" in key.lower():
                device_section_str += f"""
                        <div class="icon-box datetime">
                            <i class="fas fa-calendar"></i>
                            <div class="value">{device_data.get(device_name)[key].strftime("%Y-%m-%d %H:%M:%S")}</div>
                            <div class="label">📅 Datetime</div>
                        </div>
                        """

        device_section_str += "</div>"
        html_div.append(device_section_str)
    html_block = f"""{"".join(html_div)} """
    return html_block


def generate_report(farm_name, sensor_data, edge_data, title="AISeed Report"):
    html_header_str = """
           <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AISeed Report</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
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
                    position: relative;
                }
                .header .icon {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    font-size: 4em;
                    opacity: 0.2;
                }
                .header h1 {
                    position: relative;
                    z-index: 1;
                }
                .content {
                    padding: 30px 60px;
                }
                .content h1 {
                    color: #333;
                }
                .content p {
                    color: #555;
                }
                .device-section {
                    margin-bottom: 20px;
                }
                .device-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 10px;
                }
                .device-header h2 {
                    margin: 0;
                    color: #47349b;
                }
                .icon-grid {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 20px;
                }
                .icon-box {
                    background: #fff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    text-align: center;
                }
                .icon-box i {
                    font-size: 2em;
                    margin-bottom: 10px;
                    color: #00A4BD;
                }
                .icon-box .value {
                    font-size: 1.5em;
                    font-weight: bold;
                }
                .icon-box .label {
                    color: #777;
                }
                .humidity .value {
                    color: #3498db;
                }
                .sun .value {
                    color: #f39c12;
                }
                .ec .value {
                    color: #1abc9c;
                }
                .ph .value {
                    color: #8e44ad;
                }
                .solid-temp .value {
                    color: #e74c3c;
                }
                .temp .value {
                    color: #e67e22;
                }
                .co2 .value {
                    color: #2c3e50;
                }
                .solid-moisture .value {
                    color: #16a085;
                }
                .last-response .value {
                    color: #7f8c8d;
                }
                .ip .value {
                    color: #2980b9;
                }
                .datetime .value {
                    color: #d35400;
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
                        <h1>AISeed Report</h1>
                        <i class="fas fa-seedling icon"></i>
                    </div>
                    <div class="content">
                        <h1>Smart Farm Name: {farm_name}</h1>
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
