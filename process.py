import numpy as np


# debug
def _calculate_mode(image):
    if len(image.shape) == 2:  # grayscale
        vals, counts = np.unique(image, return_counts=True)
        v = vals[np.argmax(counts)]
        return v

    num_channels = image.shape[-1]
    channels = np.split(image.astype(np.uint8), num_channels, axis=-1)
    merged_colors = np.zeros_like(channels[0], dtype=np.uint32)
    for ch in channels:  # rgb
        merged_colors = merged_colors << 8
        merged_colors += ch

    vals, counts = np.unique(merged_colors, return_counts=True)
    asort = np.argsort(counts)
    # print(counts[asort][::-1][:10])
    vals_sorted = vals[asort][::-1][:10]

    results = []
    for v in vals_sorted:
        result = []
        for _ in range(num_channels):  # bgr
            c = v & 0xFF
            v = v >> 8
            result.append(c)
        results.append(result[::-1])
    return np.array(results)


# debug
def _determine_dominate_color(image):
    mode = calculate_mode(image)
    res = ""
    for value in mode:
        if isinstance(value, np.uint8):
            value_str = f"({value},{value},{value})"
        else:
            value_str = ','.join(str(x) for x in value[:3])  # [:3] so the transparent result is visible
    # return f'<p style="color:rgb({value_str});">{value}</p>'
        s = f'<p style="background-color:rgb({value_str});">{value}</p>'
        res = res + s
    # return f'<p>{value}</p>'
    return res


def calculate_mode(image):
    if len(image.shape) == 2:  # grayscale
        vals, counts = np.unique(image, return_counts=True)
        v = vals[np.argmax(counts)]
        return v

    num_channels = image.shape[-1]
    channels = np.split(image.astype(np.uint8), num_channels, axis=-1)
    merged_colors = np.zeros_like(channels[0], dtype=np.uint32)
    for ch in channels:  # rgb
        merged_colors = merged_colors << 8
        merged_colors += ch
    vals, counts = np.unique(merged_colors, return_counts=True)
    v = vals[np.argmax(counts)]
    result = []
    for _ in range(num_channels):
        c = v & 0xFF
        v = v >> 8
        result.append(c)
    return np.array(result[::-1])


def determine_dominate_color(image):
    mode = calculate_mode(image)
    value = mode
    # if isinstance(value, np.uint8):
    #     value_str = f"({value},{value},{value})"
    # else:
    #     value_str = ','.join(str(x) for x in value[:3])  # [:3] so the transparent result is visible
    # return f'<p style="background-color:rgb({value_str});">{value}</p>'
    return value
