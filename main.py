# Import necessary libraries
import cv2  # OpenCV for computer vision operations
from ultralytics import YOLO  # YOLO model for object detection
# from deep_sort_realtime.deepsort_tracker import DeepSort  # DeepSORT tracker (commented out)
from Database import cursor, db  # Database connection for logging
from datetime import datetime  # For timestamp operations
from collections import defaultdict  # Dictionary with default values

# Global variables for ROI (Region of Interest) selection
roi_selected = False  # Flag to check if ROI is selected
roi_points = []  # List to store ROI corner points
roi_x1, roi_y1, roi_x2, roi_y2 = 0, 0, 0, 0  # ROI corner coordinates

# Mouse callback function for ROI selection
def mouse_callback(event, x, y, flags, param):
    # Access global variables
    global roi_points, roi_selected, roi_x1, roi_y1, roi_x2, roi_y2
    
    # When left mouse button is pressed down
    if event == cv2.EVENT_LBUTTONDOWN:
        roi_points = [(x, y)]  # Store first corner point
        roi_selected = False  # Reset selection flag
    
    # When left mouse button is released
    elif event == cv2.EVENT_LBUTTONUP:
        roi_points.append((x, y))  # Add second corner point
        roi_x1, roi_y1 = roi_points[0]  # Get first corner coordinates
        roi_x2, roi_y2 = roi_points[1]  # Get second corner coordinates
        
        # Ensure x1 < x2 and y1 < y2 (normalize coordinates)
        if roi_x1 > roi_x2:
            roi_x1, roi_x2 = roi_x2, roi_x1  # Swap x coordinates if needed
        if roi_y1 > roi_y2:
            roi_y1, roi_y2 = roi_y2, roi_y1  # Swap y coordinates if needed
            
        roi_selected = True  # Set ROI as selected
        print(f"ROI selected: ({roi_x1}, {roi_y1}) to ({roi_x2}, {roi_y2})")  # Print ROI coordinates

# Load YOLOv8 model from specified path
model = YOLO(r'C:\Users\user\OneDrive\Documents\Computer Vision\Advance_Projects\Real-Time Object Detection and Tracking with Analytics Dashboard\train\weights\best.pt')

# Initialize DeepSORT tracker (commented out - not used)
# tracker = DeepSort(max_age=30, max_cosine_distance=0.4)

# Capture video from specified file path
cap = cv2.VideoCapture(r"C:\Users\user\OneDrive\Documents\Computer Vision\Advance_Projects\Real-Time Object Detection and Tracking with Analytics Dashboard\videos\vaccines_bottles5.mp4")

# Define custom classes for detection (currently only vaccine is active)
custom_classes = {
    "vaccine": {0: "vaccine"},  # Vaccine detection class
    # Other classes are commented out for this specific use case
}

# Define colors for each class in BGR format
class_colors = {
    "vaccine": (0, 0, 64),  # Dark red color for vaccine class
    # Other color definitions are commented out
}

# Create display window and set mouse callback
cv2.namedWindow('YOLOv11 + DeepSORT')  # Create named window
cv2.setMouseCallback('YOLOv11 + DeepSORT', mouse_callback)  # Set mouse callback function

# Print instructions for user
print("Click and drag to select Region of Interest (ROI)")
print("Press 'r' to reset ROI")
print("Press 'q' to quit")

# Main video processing loop
while cap.isOpened():  # Continue while video is open
    ret, frame = cap.read()  # Read next frame from video
    if not ret:  # If no frame is read
        break  # Exit loop
    
    # Draw ROI rectangle if it's selected
    if roi_selected:
        # Draw blue rectangle around ROI
        cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), (255, 0, 0), 2)
        # Add "ROI" label above the rectangle
        cv2.putText(frame, "ROI", (roi_x1, roi_y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    
    # Detect objects in the current frame
    results = model(frame)  # Run YOLO detection
    detections = []  # List to store detections
    class_counts = defaultdict(int)  # Count of each class in frame
    roi_class_counts = defaultdict(int)  # Count only objects in ROI
    
    # Process each detected object
    for box in results[0].boxes:
        # Extract bounding box coordinates
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        # Get confidence score
        conf = box.conf.item()
        # Get class ID
        cls = int(box.cls.item())
        # Get class name from model
        class_name = model.names[cls]
        
        # Always draw bounding boxes (both inside and outside ROI)
        color = class_colors.get(class_name, (0, 255, 0))  # Get color or default to green
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)  # Draw bounding box
        # Add class name and confidence label
        cv2.putText(frame, f'{class_name}: {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Check if detection is within ROI for counting
        if roi_selected:
            # Calculate center point of bounding box
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            
            # Check if center point is within ROI boundaries
            if roi_x1 <= center_x <= roi_x2 and roi_y1 <= center_y <= roi_y2:
                # Object is inside ROI - count it
                detections.append(([x1, y1, x2 - x1, y2 - y1], conf, cls))  # Add to detections
                class_counts[class_name] += 1  # Increment total count
                roi_class_counts[class_name] += 1  # Increment ROI count
        else:
            # No ROI selected - count all objects
            detections.append(([x1, y1, x2 - x1, y2 - y1], conf, cls))  # Add to detections
            class_counts[class_name] += 1  # Increment total count
    
    # Display count within ROI if ROI is selected and objects are detected
    if roi_selected and roi_class_counts:
        y_offset = 30  # Initial vertical offset for text
        # Display count for each class detected in ROI
        for class_name, count in roi_class_counts.items():
            count_text = f"{class_name}: {count}"  # Format count text
            # Draw count text in white inside ROI
            cv2.putText(frame, count_text, (roi_x1 + 10, roi_y1 + y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            y_offset += 25  # Move down for next line
    
    # Log detections to database (only objects in ROI)
    now = datetime.now()  # Get current timestamp
    Currents_date = now.date()  # Extract date (YYYY-MM-DD)
    Currents_time = now.strftime('%H:%M:%S')  # Format time as 24-hour (HH:MM:SS)
    
    # Insert count for each class into database
    for class_name, count in class_counts.items():
        # Execute SQL insert statement
        cursor.execute(
            "INSERT INTO detection_vaccineslog (class_name, count, Currents_date, Currents_time) VALUES (%s, %s, %s, %s)",
            (class_name, count, Currents_date, Currents_time)
        )
    db.commit()  # Commit changes to database
    
    # DeepSORT tracking code (commented out)
    # tracks = tracker.update_tracks(detections, frame=frame)
    
    # DeepSORT visualization code (commented out)
    # for track in tracks:
    #     if not track.is_confirmed():
    #         continue
    #     track_id = track.track_id
    #     ltrb = track.to_ltrb()
    #     x1, y1, x2, y2 = map(int, ltrb)
    #     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
    #     cv2.putText(frame, f'ID: {track_id}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    # Display the processed frame
    cv2.imshow('YOLOv11 + DeepSORT', frame)
    
    # Handle keyboard input
    key = cv2.waitKey(1) & 0xFF  # Wait for key press (1ms timeout)
    if key == ord('q'):  # If 'q' is pressed
        break  # Exit main loop
    elif key == ord('r'):  # If 'r' is pressed
        # Reset ROI selection
        roi_selected = False  # Reset selection flag
        roi_points = []  # Clear ROI points
        print("ROI reset")  # Print confirmation

# Cleanup operations
cap.release()  # Release video capture object
cv2.destroyAllWindows()  # Close all OpenCV windows
db.close()  # Close database connection

# Print completion message
print("Video_Finished")