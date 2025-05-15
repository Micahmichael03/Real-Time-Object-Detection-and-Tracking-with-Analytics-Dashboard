# Real-Time Object Detection and Tracking with Analytics Dashboard

![Project Demo](assets/demo.gif)

## Overview

This project implements a real-time object detection and tracking system with an analytics dashboard, designed specifically for manufacturing industry applications. The system allows for accurate identification, counting, and tracking of objects within a specified Region of Interest (ROI), while storing detection data for analytics purposes.

When objects are detected within the defined ROI, the system automatically logs this data to a MySQL database in real-time. The database architecture is optimized for analytics workloads, with carefully designed tables that capture object classes, counts, timestamps, and other relevant metrics. This data pipeline enables seamless integration with Power BI, which connects directly to the MySQL server to create live, interactive dashboards that visualize object detection metrics in real-time. The end-to-end solution provides manufacturing managers with actionable insights into production flows, quality control processes, and operational efficiency without any manual data entry or processing delays.

## Features

- **Real-time object detection** using YOLOv8 models
- **ROI (Region of Interest) selection** for focused monitoring
- **Object counting** within the selected ROI
- **Database integration** for detection analytics and historical data
- **Power BI dashboards** with real-time visualization of detection metrics
- **Customizable for various manufacturing objects** including products, components, and quality control
- **Visual feedback** with bounding boxes and object labels

## Screenshots

![Dashboard View](assets/dashboard.png)

## Technologies Used

- **Computer Vision**: OpenCV, Ultralytics YOLO
- **Database**: MySQL
- **Data Processing**: Python
- **Object Tracking**: Custom implementation based on YOLO detection

## Requirements

- Python 3.7+
- OpenCV
- Ultralytics YOLO
- MySQL
- Required Python packages (see installation section)

## Installation

1. **Clone the repository**
   ```
   git clone https://github.com/yourusername/real-time-object-detection.git
   cd real-time-object-detection
   ```

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Set up the MySQL database**
   - Create a new database named `object_detection`
   - Run the SQL scripts in the `sql_files` folder:
     ```
     mysql -u username -p object_detection < sql_files/creating_OD_db.sql
     ```

4. **Configure database connection**
   - Update the MySQL connection parameters in `Database.py` with your credentials:
     ```python
     db = mysql.connector.connect(
         host="localhost",
         user="your_username",
         password="your_password",
         database="object_detection"
     )
     ```

5. **Prepare your YOLO model**
   - Place your trained YOLO model in the `train/weights/` directory
   - The default path is set to `train/weights/best.pt`

## Usage

1. **Run the main application**
   ```
   python main.py
   ```

2. **Select a Region of Interest (ROI)**
   - Click and drag on the video frame to select a rectangular ROI
   - Objects will be counted only when they appear within this ROI

3. **Keyboard controls**
   - Press 'r' to reset the ROI selection
   - Press 'q' to quit the application

4. **View detection data**
   - Detection counts are stored in the MySQL database
   - You can use the included SQL queries in the `sql_files` folder to analyze detection data

## Customization

### For Different Manufacturing Objects

The system can be customized to detect different manufacturing objects by:

1. Training a custom YOLO model on your specific objects
2. Updating the `custom_classes` dictionary in `main.py`
3. Adjusting the `class_colors` dictionary to assign unique colors to each class

### For Different Video Sources

To use a different video source:

1. Update the `VideoCapture` path in `main.py`:
   ```python
   cap = cv2.VideoCapture("path/to/your/video.mp4")
   ```
2. To use a webcam, change to:
   ```python
   cap = cv2.VideoCapture(0)  # 0 for default webcam
   ```

## Database Schema

The system stores detection data in the following format:
- Object class name
- Count
- Date
- Time

This data can be used for:
- Production metrics
- Quality control statistics
- Throughput analysis
- Process optimization

## Analytics Dashboard

The project features a robust analytics solution powered by Power BI, which connects directly to the MySQL database for real-time visualization and analysis:

- **Live Connection**: Power BI establishes a direct query connection to the MySQL server, ensuring all visualizations reflect the most current detection data
- **Interactive Dashboards**: Custom-built dashboards provide multiple views of the detection data, including:
  - Real-time object counts with temporal filtering
  - Production line efficiency metrics
  - Anomaly detection for quality control
  - Trend analysis across different time periods
- **KPI Monitoring**: Key performance indicators are visualized through gauges, cards, and other intuitive visuals
- **Drill-Through Capabilities**: Users can drill down from summary metrics to detailed views of specific detection events
- **Automated Refresh**: The dashboard is configured to refresh at customizable intervals, ensuring manufacturing managers always have access to current data

![Analytics Dashboard](assets/analytics_dashboard.png)

The integration of computer vision, database technology, and business intelligence creates a comprehensive solution that transforms raw detection data into actionable manufacturing insights.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please contact [makoflash05@gmail.com]. 