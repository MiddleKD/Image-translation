import numpy as np
import easyocr
from PIL import Image, ImageDraw

def call_easyocr(language:list, model_dir=None):
    return easyocr.Reader(language, model_storage_directory=model_dir)

def inference(image, model, conf_threshold=0.5, mask_rank=None, return_mask_mode="one"):
    image_np = np.array(image)
    ocr_results = model.readtext(image_np, width_ths=0.7, min_size=50)
    
    text_and_coords = []
    for cur in ocr_results:
        confidence = cur[2]

        if confidence < conf_threshold:
            continue
        
        coords = cur[0]
        text = cur[1]
        text_and_coords.append([coords, text, confidence])
    text_and_coords = sorted(text_and_coords, key=lambda x:x[2], reverse=True)
    text_and_coords = text_and_coords[:mask_rank]
    
    mask_images = []
    if return_mask_mode=="list":
        for box in text_and_coords[:mask_rank] if mask_rank is not None else text_and_coords:
            mask_image = Image.new('L', image.size, 0)
            draw = ImageDraw.Draw(mask_image)
            coords = [tuple(point) for point in box[0]]
            draw.polygon(coords, fill=255)
            mask_images.append(mask_image)
        return [cur[1] for cur in text_and_coords], mask_images
    elif return_mask_mode=="one":
        mask_image = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask_image)
        for box in text_and_coords[:mask_rank] if mask_rank is not None else text_and_coords:
            coords = [tuple(point) for point in box[0]]
            draw.polygon(coords, fill=255)
        return [cur[1] for cur in text_and_coords], mask_image
    elif return_mask_mode=="all":
        concated_mask_image = Image.new('L', image.size, 0)
        cated_mask_draw = ImageDraw.Draw(concated_mask_image)
        for box in text_and_coords[:mask_rank] if mask_rank is not None else text_and_coords:
            coords = [tuple(point) for point in box[0]]
            cated_mask_draw.polygon(coords, fill=255)

            mask_image = Image.new('L', image.size, 0)
            draw = ImageDraw.Draw(mask_image)
            draw.polygon(coords, fill=255)
            mask_images.append(mask_image)
            
        return [cur[1] for cur in text_and_coords], [concated_mask_image, mask_images]

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    img = Image.open("")
    model = call_easyocr(["ko","en"], os.getenv("OCR_MODEL_PATH"))
    output, mask = inference(img, model, conf_threshold=0.0, mask_rank=1)

