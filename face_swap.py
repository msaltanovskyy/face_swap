import cv2
import dlib
import numpy as np

# Инициализация детектора и предиктора dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


def get_landmarks(image):
    """Получение ключевых точек лица из изображения."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    landmarks = []

    for face in faces:
        shape = predictor(gray, face)
        shape_np = np.zeros((68, 2), dtype=int)
        for i in range(68):
            shape_np[i] = (shape.part(i).x, shape.part(i).y)
        landmarks.append(shape_np)

    return landmarks


def apply_color_correction(src_face, dst_face):
    """Применение цветокоррекции для улучшения соответствия цвета."""
    src_face_lab = cv2.cvtColor(src_face, cv2.COLOR_BGR2Lab)
    dst_face_lab = cv2.cvtColor(dst_face, cv2.COLOR_BGR2Lab)

    src_mean, src_std = cv2.meanStdDev(src_face_lab)
    dst_mean, dst_std = cv2.meanStdDev(dst_face_lab)

    src_mean = src_mean.flatten()
    src_std = src_std.flatten()
    dst_mean = dst_mean.flatten()
    dst_std = dst_std.flatten()

    corrected_src_lab = (src_face_lab - src_mean) * (dst_std / (src_std + 1e-5)) + dst_mean
    corrected_src_lab = np.clip(corrected_src_lab, 0, 255).astype(np.uint8)
    corrected_src = cv2.cvtColor(corrected_src_lab, cv2.COLOR_Lab2BGR)

    return corrected_src


def warp_image(image, src_landmarks, dst_landmarks, size):
    """Warp изображение из исходных ключевых точек в целевые."""
    src_pts = np.float32(src_landmarks)
    dst_pts = np.float32(dst_landmarks)
    M, _ = cv2.findHomography(src_pts, dst_pts)
    warped_image = cv2.warpPerspective(image, M, size, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return warped_image


def create_smooth_mask(image, landmarks):
    """Создание плавной маски для смешивания лиц."""
    mask = np.zeros_like(image[:, :, 0], dtype=np.uint8)
    landmarks = np.array(landmarks, dtype=np.int32)

    if len(landmarks) > 0:
        hull = cv2.convexHull(landmarks)
        if len(hull) > 0:
            cv2.fillConvexPoly(mask, hull, 255)

            # Создание плавного перехода для маски
            mask = cv2.GaussianBlur(mask, (15, 15), 0)
            # Убедимся, что маска находится в пределах границ изображения
            mask = np.clip(mask, 0, 255)
        else:
            print("Error: Convex hull is empty.")
    else:
        print("Error: No landmarks to create mask.")

    return mask


def blend_faces(src_img, dst_img, mask):
    """Смешивание двух изображений на основе маски с плавным переходом."""
    alpha = mask / 255.0
    alpha = np.stack([alpha] * 3, axis=-1)

    # Смешивание с применением маски
    blended = alpha * src_img + (1 - alpha) * dst_img

    return blended


def swap_faces(src_img, dst_img, color_correction=True, face_size_scale=1.0):
    """Замена лиц на изображениях с опциональной цветокоррекцией и масштабированием лица."""
    src_landmarks = get_landmarks(src_img)
    dst_landmarks = get_landmarks(dst_img)

    if not src_landmarks or not dst_landmarks:
        raise ValueError("No faces detected in one of the images.")

    src_landmarks = src_landmarks[0]
    dst_landmarks = dst_landmarks[0]

    # Применение масштабирования размера лица, если требуется
    if face_size_scale != 1.0:
        src_face_size = np.linalg.norm(src_landmarks[16] - src_landmarks[0])
        dst_face_size = np.linalg.norm(dst_landmarks[16] - dst_landmarks[0])
        scale_factor = dst_face_size / (src_face_size * face_size_scale)

        src_img = cv2.resize(src_img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

        # Пересчитываем ключевые точки после изменения масштаба
        src_landmarks = get_landmarks(src_img)[0]

    size = (dst_img.shape[1], dst_img.shape[0])
    warped_src_img = warp_image(src_img, src_landmarks, dst_landmarks, size)

    if color_correction:
        corrected_src_img = apply_color_correction(warped_src_img, dst_img)
    else:
        corrected_src_img = warped_src_img

    mask = create_smooth_mask(dst_img, dst_landmarks)

    result_img = blend_faces(corrected_src_img, dst_img, mask)

    result_img = np.clip(result_img, 0, 255).astype(np.uint8)
    return result_img

# Пример использования:
# src_img = cv2.imread('source.jpg')
# dst_img = cv2.imread('destination.jpg')
# result_img = swap_faces(src_img, dst_img, color_correction=True)
# cv2.imwrite('result.jpg', result_img)
