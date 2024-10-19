from diffusers import StableDiffusionInpaintPipeline,UNet2DConditionModel
import torch
from PIL import Image 
import numpy as np 

model_path = "/home/shenjing/in_out_painting/code/VIP/examples/mv_ours/C_T_S/checkpoint-9000"
unet = UNet2DConditionModel.from_pretrained(model_path + "/unet", torch_dtype=torch.float16)


pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "/home/shenjing/in_out_painting/pretrained/stabilityai/stable-diffusion-2-inpainting",
    # unet = unet,
    torch_dtype=torch.float16,
)
pipe.to("cuda:0")
prompt = "indoor scene"
# prompt = [ "Face of a yellow cat", "high resolution", "sitting on a park bench"]

# image_path = "/home/shenjing/in_out_painting/code/overture-creations-5sI6fQgYIuo.png"  
# mask_image_path = "/home/shenjing/in_out_painting/code/overture-creations-5sI6fQgYIuo_mask.png"  


image_path = '/home/shenjing/in_out_painting/code/code/mydiffuser/mp3d_skyboxall7.5_warp.png'
mask_image_path = "/home/shenjing/in_out_painting/code/code/mydiffuser/overlap_mask1.png"
prompt = "indoor scene."



image = Image.open(image_path).convert("RGB").resize((256, 256))  # 确保图像是RGB格式  
mask_image = Image.open(mask_image_path).convert("RGB").resize((256, 256))  # 掩码图像转换为灰度图（单通道）  

# mask_image_inverted = Image.fromarray(255 - np.array(mask_image))
# mask_image_inverted.save('/home/shenjing/in_out_painting/code/code/mydiffuser/overlap_mask1.png')

num = 7.5
#image and mask_image should be PIL images.
#The mask structure is white for inpainting and black for keeping as is
image = pipe(prompt=prompt, image=image, mask_image=mask_image,guidance_scale=num).images[0]
image.save("./mp3d_skyboxall{}3-666.png".format(num))





# image_path = 
# image = Image.open(image_path).convert("RGB").resize((512, 512))
# mask_image = np.zeros((image.size[1], image.size[0], 3), dtype=np.uint8) 
# mask_image[:, 256:, :] = 255
# mask_image_pil = Image.fromarray(mask_image)  
# mask_image_pil.save("/home/shenjing/in_out_painting/code/overture_mask.png")  