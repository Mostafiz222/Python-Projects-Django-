import cv2
import numpy as np
import os



def count_coins(image_path):

    # -------------------------
    # Step 1 — Load Image
    # -------------------------

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Image could not be loaded")


    img_rgb = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2RGB
    )


    # -------------------------
    # Step 2 — Convert to Gray
    # -------------------------

    gray = cv2.cvtColor(
        img_rgb,
        cv2.COLOR_RGB2GRAY
    )


    # -------------------------
    # Step 3 — Blur
    # -------------------------

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )


    # -------------------------
    # Step 4 — Otsu Threshold
    # -------------------------

    _, thresh = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )


    # -------------------------
    # Step 5 — Morphology
    # -------------------------

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (5, 5)
    )


    opening = cv2.morphologyEx(
        thresh,
        cv2.MORPH_OPEN,
        kernel
    )


    # -------------------------
    # Step 6 — Find Contours
    # -------------------------

    contours, _ = cv2.findContours(
        opening,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )


    # Convert back to BGR for OpenCV drawing
    result = img.copy()


    # Keep only valid coins

    valid_contours = [
        cnt for cnt in contours
        if cv2.contourArea(cnt) >= 2000
    ]


    num_coins = len(valid_contours)

    areas = []

    count = 1


    # -------------------------
    # Step 7 — Draw Detection
    # -------------------------

    for cnt in valid_contours:

        area = cv2.contourArea(cnt)

        areas.append(area)


        # Generate unique color

        hue = int(
            (count - 1) *
            (180 / max(num_coins, 1))
        ) % 180


        hsv_pixel = np.uint8(
            [[[hue, 255, 255]]]
        )


        rgb_pixel = cv2.cvtColor(
            hsv_pixel,
            cv2.COLOR_HSV2RGB
        )[0][0]


        color_rgb = (
            int(rgb_pixel[0]),
            int(rgb_pixel[1]),
            int(rgb_pixel[2])
        )


        # Convert RGB to BGR for OpenCV

        color = (
            color_rgb[2],
            color_rgb[1],
            color_rgb[0]
        )


        # Enclosing circle

        (x_c, y_c), radius = cv2.minEnclosingCircle(cnt)


        center = (
            int(x_c),
            int(y_c)
        )


        cv2.circle(
            result,
            center,
            int(radius),
            color,
            2
        )


        # Bounding rectangle

        x, y, w, h = cv2.boundingRect(cnt)


        cv2.rectangle(
            result,
            (x, y),
            (x+w, y+h),
            color,
            2
        )


        # Label

        cv2.putText(
            result,
            f"Coin {count}",
            center,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )


        count += 1



    # -------------------------
    # Step 8 — Statistics
    # -------------------------

    if areas:

        statistics = {

            "total_coins": len(areas),

            "average_area":
                round(
                    sum(areas) / len(areas),
                    2
                ),

            "largest_coin":
                round(
                    max(areas),
                    2
                ),

            "smallest_coin":
                round(
                    min(areas),
                    2
                )
        }


    else:

        statistics = {

            "total_coins": 0,

            "average_area": 0,

            "largest_coin": 0,

            "smallest_coin": 0
        }



    # -------------------------
    # Step 9 — Save Result
    # -------------------------

    os.makedirs(
        "outputs",
        exist_ok=True
    )


    output_path = (
        "outputs/result.jpg"
    )


    cv2.imwrite(
        output_path,
        result
    )


    return {

        "count":
            len(areas),

        "areas":
            areas,

        "statistics":
            statistics,

        "image":
            output_path
    }