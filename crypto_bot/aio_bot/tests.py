import cv2
import numpy as np

def photo_edit(photo_path, crop_bottom_pixels):
    # Загрузка изображения
    img = cv2.imread(photo_path)

    if img is None:
        print("Ошибка: изображение не загружено. Проверьте путь к файлу.")
        return

    # Получение размеров изображения
    height, width = img.shape[:2]

    # Обрезка снизу
    cropped_img = img[:height - crop_bottom_pixels]

    # Применение изменений в яркости и контрастности
    alpha = 1.8  # коэффициент усиления контраста
    beta = -100  # сдвиг яркости
    new_img = alpha * img + beta

    new_img = np.clip(new_img, 0, 255).astype(np.uint8)

    new_img = cv2.convertScaleAbs(cropped_img, alpha=alpha, beta=beta)

    # Сохранение обработанного изображения
    cv2.imwrite(photo_path, new_img)
    print('Успех: изображение обработано и сохранено')

# Пример вызова функции, обрезаем нижние 50 пикселей
photo_edit("crypto_bot/media/file_13.jpg", 20)
