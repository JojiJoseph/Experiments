import numpy as np
import cv2


control_points = [(50, 50), (50, 300), (450, 50), (450, 300)]
control_points_original_position = [(50, 50), (50, 300), (450, 50), (450, 300)]
selected_cp = None
# create some points between the control points
# points = np.random.randint(0, 500, (100, 2)).tolist()
# Sample points in a grid
x = np.linspace(0, 500, 20)
y = np.linspace(0, 500, 20)
xx, yy = np.meshgrid(x, y)
points = np.vstack([xx.ravel(), yy.ravel()]).T.astype(np.int32).tolist()
# Sample points in a circle around the center of the control points
# center = ((control_points[0][0] + control_points[1][0]) // 2, (control_points[0][1] + control_points[1][1]) // 2)
center = (250, 175)
radius = 150
angles = np.linspace(0, 2 * np.pi, 100)
circle_points = [(int(center[0] + radius * np.cos(a)), int(center[1] + radius * np.sin(a))) for a in angles]
# points = circle_points
img = np.ones((600, 600, 3), dtype=np.uint8) * 255
def callback(event, x, y, flags, param):
    global points, control_points, selected_cp
    if event == cv2.EVENT_LBUTTONDOWN:
        # Check if we clicked on a control point
        for i, cp in enumerate(control_points):
            if abs(cp[0] - x) < 10 and abs(cp[1] - y) < 10:
                # control_points[i] = (x, y)
                selected_cp = i
    if event == cv2.EVENT_LBUTTONUP:
        selected_cp = None
    if event == cv2.EVENT_MOUSEMOVE:
        if selected_cp is not None:
            control_points[selected_cp] = (x, y)

def transform_points(points, control_points):
    points_new = np.array(points)
    control_points_delta = np.array(control_points) - np.array(control_points_original_position)
    points_new = points_new + weights @ control_points_delta
    return points_new.astype(np.int32)


# dist_to_cp = lambda p, cp: np.sqrt((p[0] - cp[0])**2 + (p[1] - cp[1])**2)
# dist = dist_to_cp(points[0], control_points[0])
# Create (N,2) matrix of distances to each control point
distances = np.array([[np.sqrt((p[0] - cp[0])**2 + (p[1] - cp[1])**2) for cp in control_points] for p in points])
print(distances.shape)
weights = 1 / (distances**1.5 + 1e-6)
weights = weights / np.sum(weights, axis=1, keepdims=True)
print(weights.shape)
# exit()


cv2.namedWindow("image")
cv2.setMouseCallback("image", callback)

while True:
    points_transormed = transform_points(points, control_points)
    for p in points_transormed:
        cv2.circle(img, p, 3, (0, 0, 255), -1)
    for cp in control_points:
        cv2.circle(img, cp, 5, (255, 0, 0), -1)
    cv2.imshow("image", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    img = np.ones((600, 600, 3), dtype=np.uint8) * 255