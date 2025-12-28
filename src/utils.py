def expand_bbox(x, y, w, h, img_w, img_h):
    pad_w = int(w * 0.1)
    pad_h = int(h * 0.15)

    nx = max(0, x - pad_w)
    ny = max(0, y - pad_h)
    nw = min(img_w, x + w + pad_w*2) - nx
    nh = min(img_h, y + h + pad_h*2) - ny

    return nx, ny, nw, nh
