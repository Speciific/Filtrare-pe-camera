import cv2

def aplica_blur(frame, kernel_size):
    if kernel_size == 0: kernel_size + 1
    return cv2.blur(frame, (kernel_size, kernel_size))

def aplica_gaussian_blur(frame, kernel_size):
    kernel_size = kernel_size if kernel_size % 2 != 0 else kernel_size + 1
    return cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)

def aplica_filtru_median(frame, kernel_size):
    kernel_size = kernel_size if kernel_size % 2 != 0 else kernel_size + 1
    if kernel_size == 0: kernel_size + 1
    return cv2.medianBlur(frame, kernel_size)

def aplica_sobel(frame, orientare):
    grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if orientare == 'vertical':
        return cv2.Sobel(grayscale_frame, cv2.CV_64F, 0, 1, ksize=5)
    elif orientare == 'orizontal':
        return cv2.Sobel(grayscale_frame, cv2.CV_64F, 1, 0, ksize=5)

def main():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Eroare la deschiderea camerei")
        return

    cv2.namedWindow('Control Utilizator', cv2.WINDOW_NORMAL)

    cv2.createTrackbar('Blur si Median', 'Control Utilizator', 1, 30, lambda x: x)
    cv2.createTrackbar('Gaussian Blur', 'Control Utilizator', 1, 30, lambda x: x)
    cv2.createTrackbar('Diametru', 'Control Utilizator', 1, 100, lambda x: x)
    cv2.createTrackbar('Sigma Color', 'Control Utilizator', 1, 100, lambda x: x)
    cv2.createTrackbar('Sigma Space', 'Control Utilizator', 1, 200, lambda x: x)

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Eroare la citirea frame-ului")
            break

        kernel_size = cv2.getTrackbarPos('Blur si Median', 'Control Utilizator')
        kernel_size2 = cv2.getTrackbarPos('Gaussian Blur', 'Control Utilizator')
        diametru = cv2.getTrackbarPos('Diametru', 'Control Utilizator')
        sigma_color = cv2.getTrackbarPos('Sigma Color', 'Control Utilizator')
        sigma_space = cv2.getTrackbarPos('Sigma Space', 'Control Utilizator')

        frame_blur = aplica_blur(frame, kernel_size)
        frame_gaussian_blur = aplica_gaussian_blur(frame, kernel_size2)
        frame_median = aplica_filtru_median(frame, kernel_size)
        frame_sobel_vertical = aplica_sobel(frame, 'vertical')
        frame_sobel_orizontal = aplica_sobel(frame, 'orizontal')
        frame_bilateral = cv2.bilateralFilter(frame, diametru, sigma_color, sigma_space)

        noua_dimensiune = (320, 240)

        frame = cv2.resize(frame, noua_dimensiune)
        cv2.imshow('Original', frame)
        cv2.moveWindow('Original', 970, 0)

        frame_blur = cv2.resize(frame_blur, noua_dimensiune)
        cv2.imshow('Blur', frame_blur)
        cv2.moveWindow('Blur', 0, 0)

        frame_gaussian_blur = cv2.resize(frame_gaussian_blur, noua_dimensiune)
        cv2.imshow('Gaussian Blur', frame_gaussian_blur)
        cv2.moveWindow('Gaussian Blur', 321, 0)

        frame_median = cv2.resize(frame_median, noua_dimensiune)
        cv2.imshow('Filtru Median', frame_median)
        cv2.moveWindow('Filtru Median', 642, 0)

        frame_sobel_vertical = cv2.resize(frame_sobel_vertical, noua_dimensiune)
        cv2.imshow('Sobel Vertical', frame_sobel_vertical)
        cv2.moveWindow('Sobel Vertical', 0, 275)

        frame_sobel_orizontal = cv2.resize(frame_sobel_orizontal, noua_dimensiune)
        cv2.imshow('Sobel Orizontal', frame_sobel_orizontal)
        cv2.moveWindow('Sobel Orizontal', 321, 275)

        frame_bilateral = cv2.resize(frame_bilateral, noua_dimensiune)
        cv2.imshow('Filtru Bilateral', frame_bilateral)
        cv2.moveWindow('Filtru Bilateral', 642, 275)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
