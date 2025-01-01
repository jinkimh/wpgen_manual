import numpy as np
import matplotlib.pyplot as plt
import cv2
import csv
import yaml
from scipy.interpolate import CubicSpline

# 맵 초기화
def initialize_map(width, height):
    obs_dict = {}
    for i in range(width):
        for j in range(height):
            obs_dict[(i, j)] = False
    return obs_dict

# 이미지 기반 장애물 맵 생성 함수
def load_image_and_generate_map(image_path):
    o_x, o_y = [], []

    # 이미지 로드 및 이진화
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Error: Cannot load image at '{image_path}'. Check the file path or integrity.")

    height, width = img.shape  # 이미지 크기를 맵 크기로 설정
    obs_dict = initialize_map(width, height)
    _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    # 장애물 위치 기록
    for i in range(binary.shape[0]):
        for j in range(binary.shape[1]):
            if binary[i, j] == 255:  # 장애물로 간주
                obs_dict[(j, i)] = True
                o_x.append(j)
                o_y.append(i)

    return obs_dict, o_x, o_y, img, width, height

# Cubic Spline으로 경로 보간
def calc_cubic_spline_path(points, n_points=100):
    points = np.array(points)
    x, y = points[:, 0], points[:, 1]

    # Cubic Spline 생성
    cs_x = CubicSpline(np.linspace(0, 1, len(x)), x, bc_type='clamped')
    cs_y = CubicSpline(np.linspace(0, 1, len(y)), y, bc_type='clamped')

    # 보간된 경로 생성
    t = np.linspace(0, 1, n_points)
    path_x = cs_x(t)
    path_y = cs_y(t)

    return np.array(list(zip(path_x, path_y)))

# 마우스로 경로 점들을 설정하는 함수
class PointPicker:
    def __init__(self, img):
        self.img = img
        self.points = []

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 버튼 클릭
            self.points.append((x, y))
            print(f"Point selected: ({x}, {y})")
            cv2.circle(self.img, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow("Select Path Points", self.img)

    def select_points(self):
        print("Click on the image to select the path points (Press R to finish).")
        cv2.imshow("Select Path Points", self.img)
        cv2.setMouseCallback("Select Path Points", self.mouse_callback)
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('r'):
                break
        cv2.destroyAllWindows()
        return self.points

# 플립된 경로 좌표 계산 함수
def flip_points(points, height):
    return [(x, height - y) for x, y in points]

# 경로를 CSV로 저장 (YAML 정보를 반영하여 변환)
def save_path_to_csv(path, filename, resolution, origin):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["x", "y"])
        for x, y in path:
            world_x = x * resolution + origin[0]
            world_y = y * resolution + origin[1]
            writer.writerow([world_x, world_y])

# YAML 파일 로드
def load_yaml(yaml_path):
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
    return data['resolution'], data['origin']

# 메인 함수
def main():
    image_path = './map/ict_3rd_floor.png'  # 입력 이미지 파일 경로
    yaml_path = image_path.replace('.png', '.yaml')  # 입력 YAML 파일 경로

    # YAML 파일에서 맵 정보 로드
    resolution, origin = load_yaml(yaml_path)

    # 이미지 기반 장애물 맵 생성
    obs_dict, o_x, o_y, img, width, height = load_image_and_generate_map(image_path)

    # 마우스로 경로 점 선택
    picker = PointPicker(cv2.cvtColor(img, cv2.COLOR_GRAY2BGR))
    points = picker.select_points()
    print("Selected points:", points)

    # 경로 점을 이미지 상하 플립
    flipped_points = flip_points(points, height)
    print("Flipped points:", flipped_points)

    # 시작점과 끝점 연결
    if len(flipped_points) > 1 and flipped_points[0] != flipped_points[-1]:
        flipped_points.append(flipped_points[0])

    # Cubic Spline 보간
    if len(flipped_points) > 1:
        smoothed_path = calc_cubic_spline_path(flipped_points, n_points=500)
        csv_filename = image_path.split('/')[-1].replace('.png', '.csv')  # CSV 파일 이름 생성
        save_path_to_csv(smoothed_path, csv_filename, resolution, origin)
        print(f"Path saved to {csv_filename}")

        # 시각화
        flipped_img = cv2.flip(img, 0)  # 이미지 상하 플립
        plt.figure(figsize=(width / 300, height / 300))  # Figure 크기 조정
        plt.imshow(cv2.cvtColor(flipped_img, cv2.COLOR_GRAY2RGB), interpolation='nearest')
        plt.plot(o_x, [height - y for y in o_y], ".k", markersize=1, label="Obstacles")  # 점 크기 축소
        px, py = zip(*smoothed_path)
        plt.plot(px, py, "-r", linewidth=1, label="Smoothed Path")  # 선 두께 조정
        plt.grid(False)
        plt.legend()
        plt.title("Flipped Image with Path")
        plt.show()
    else:
        print("Not enough points to calculate a path.")

if __name__ == "__main__":
    main()
