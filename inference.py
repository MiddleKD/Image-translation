from simple_lama_inpainting import SimpleLama
from PIL import Image

def load_lama_remover(model_path, device):
    remover = SimpleLama(model_path, device)
    return remover

def inferene(image, mask_image, model):
    image = image.convert("RGB")
    mask_image = mask_image.convert("L")

    result_image = model(image, mask_image)
    return result_image

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    remover = load_lama_remover(
        model_path=os.getenv("LAMA_MODEL_PATH"),
        device="cuda"
    )

    image = Image.open("")
    mask_image = Image.open("")
    
    result_image = inferene(image, mask_image, remover)
    result_image.show()
