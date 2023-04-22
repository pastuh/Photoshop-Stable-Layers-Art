import webuiapi
from IPython.display import clear_output
import os
import time
import numbers
from psd_tools import PSDImage
from psd_tools.constants import Tag

api_sampler = 'Euler a'
api_steps = 20
api_seed = 666999
api_cfg = 6
api_denoise = 0.50
api = webuiapi.WebUIApi(sampler=api_sampler, steps=api_steps)

file_base = "stable_art.psd"
f_base_new = 0

while True:
    f_base = os.path.getmtime(file_base)

    if f_base == f_base_new:
        time.sleep(0.5)
    else:
        f_base_new = f_base

        psd = PSDImage.open(file_base)
        image_width, image_height = psd.size

        positive_prompt = ""
        positive_prompt_list = []
        negative_prompt = ""
        negative_prompt_list = []
        real_image = ""

        #Test
        #masks_in_layers = []
        #art_in_layers = []

        def process_layers(layer, target_list):
            #Prompts with "functions" multiplied by the weight. Default: (x:1.0) Modified: ((x:1.0):1.0)
            if (layer.is_visible() and layer.kind != "group"):
                #Prompt opacity reduce weight by 0.1
                opacity_value = int(layer.opacity * 100)
                opacity_ratio = round(opacity_value / 255) / 100
                #Prompt with effect increase weight by 1.0
                if(len(layer.effects) > 0):
                    opacity_ratio += len(layer.effects)
                quality_prompt = f"({layer.name}:{opacity_ratio:.2f})"
                #Locked Prompt activates AND
                if (layer.tagged_blocks.get_data(Tag.PROTECTED_SETTING) > 0):
                    target_list.append(f"({quality_prompt} AND {quality_prompt})")
                else:
                    target_list.append(f"{quality_prompt}")

        for layer in psd:
            if (layer.kind == "group" and "OPTIONS" in layer.name):
                #Read Settings if Options NOT-Locked, Can be active only one
                for options in layer:
                    if options.tagged_blocks.get_data(Tag.PROTECTED_SETTING) == 0:
                        if "Denoise" in options.name:
                            for settings in options:
                                if settings.is_visible() and isinstance(float(settings.name), numbers.Number):
                                    api_denoise = settings.name
                                    break

                        if "Cfg" in options.name:
                            for settings in options:
                                if settings.is_visible() and isinstance(float(settings.name), numbers.Number):
                                    api_cfg = settings.name
                                    break

                        if "Seed" in options.name:
                            for settings in options:
                                if settings.is_visible() and (settings.name.isdigit() or settings.name == '-1'):
                                    api_seed = settings.name
                                    break

                        if "Steps" in options.name:
                            for settings in options:
                                if settings.is_visible() and settings.name.isdigit():
                                    api_steps = settings.name
                                    break

                        if "Sampler" in options.name:
                            for settings in options:
                                if settings.is_visible():
                                    api_sampler = settings.name
                                    break

            if (layer.kind == "group" and "POSITIVE" in layer.name):
                for positive_group in layer:
                    process_layers(positive_group, positive_prompt_list)
                    if (positive_group.is_group()):
                        for positive_default in positive_group:
                            process_layers(positive_default, positive_prompt_list)

            if (layer.kind == "group" and "NEGATIVE" in layer.name):
                for negative_group in layer:
                    process_layers(negative_group, negative_prompt_list)
                    if (negative_group.is_group()):
                        for negative_default in negative_group:
                            process_layers(negative_default, negative_prompt_list)
            
            #Test
            # if layer.is_visible() and layer.has_pixels():
            #     if layer.has_mask():
            #         #print('Layer with mask:', layer.name)
            #         #print('Appends:', layer.mask)
            #         #print('////////////////////')
            #         masks_in_layers.append(layer.mask)
            #     if layer.has_clip_layers():
            #         art_in_layers.append(layer)
            #         for clip_layer in layer.clip_layers:
            #             if clip_layer.is_visible() and clip_layer.clipping_layer:
            #                 #print('Layer with clip:', layer.name)
            #                 #print('Appends:', clip_layer)
            #                 #print('////////////////////')
            #                 art_in_layers.append(clip_layer)
            #     else:
            #         if not layer.clipping_layer:
            #             #print('Simple layer:', layer.name)
            #             #print('////////////////////')
            #             art_in_layers.append(layer)

        positive_prompt = ",".join(positive_prompt_list).replace(', ', ',')
        negative_prompt = ",".join(negative_prompt_list).replace(', ', ',')
        #print("+", positive_prompt)
        #print("-", negative_prompt)
        
        #Test
        # print('------------------------')
        # print('MASKS:', len(masks_in_layers), masks_in_layers)
        # print('LAYERS:', len(art_in_layers), art_in_layers)
        # print('------------------------')
        # Composite the layers with mask into one image
        # real_image_mask = psd.composite(layer_filter=lambda layer: layer in masks_in_layers).convert('RGBA')
        # art_in_layers = psd.composite(layer_filter=lambda layer: layer in art_in_layers).convert('RGBA')
        # real_image = Image.alpha_composite(real_image_mask, art_in_layers)

        real_image = psd.composite()

        result2 = api.img2img(
            sampler_name=api_sampler,
            images=[real_image],
            prompt=positive_prompt, 
            negative_prompt=negative_prompt,
            steps=api_steps,
            styles=[],
            seed=api_seed, 
            cfg_scale=api_cfg, 
            width=image_width,
            height=image_height,
            denoising_strength=api_denoise)
        clear_output(wait=False)

        display(result2.image)