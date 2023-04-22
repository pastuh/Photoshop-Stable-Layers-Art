# Photoshop Stable Layers Art

## Description

This project enables users to paint directly in **Photoshop**, generate an image using the **Stable Diffusion** server, and view the updated image in a **Jupyter Lab** window. Change prompts by editing layer names and special options. Knowledge of **Stable Diffusion** basics is required.

## Installation

To use this project, you will need to install the following:

- [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [Jupyter Lab](https://jupyter.org/install)
- [Photoshop](https://www.adobe.com/products/photoshop.html)

*(+additional packages required to use .py script)*


## Usage

To use this project, follow these steps:

1. Open a **Photoshop** `.psd` file **`(use example file)`** and start painting.
2. `Save .psd file` and generate the image using the **Stable Diffusion** API.
3. View the updated image in a **Jupyter Lab** window.


## More detailed explanation

`(.psd file contains 3 groups which are necessary for proper operation)`

By default, each group is locked (meaning the settings cannot be changed). Each group already has samples that you can edit or delete.


###### OPTIONS group
1. Unlock any group, set `Activate` for existing layer, or create a new one.
2. Save `.psd` file, after that, an image will be generated with new settings.
3. Lock the group if you do not plan to change the settings again.

*(*You can leave unlocked, but the computer will process all layers each time you save your image)*


###### NEGATIVE / POSITIVE group
This is where you `control the prompts` that decide how your art will look.
Rename each layer to describe the style, objects, or actions. You can separate each line with a comma or simply create a new layer.
* `Activate` *(eye icon)* allows to enable or disable prompt

In each group, you can control image generation [WEIGHT]
* `Opacity` controls [Weight] by 0.1.
* `Effect layer` increases [Weight] by 1.0.
* `Lock` adds [AND] into the prompt *(reduces image generation speed)*.


###### DREAM group
The main group where you `create your art`.
You can create, edit, and paint on any layer.
* This group doesn't have any prompt settings.
* You can name layers as you want (they don't influence prompt generation).


## Credits

This project was inspired by the [Unleashing the Creative Power of Stable Diffusion](https://openai.art/study/unleashing-creative-power-of-stable-diffusion-showcase/) showcase by **OpenAI**.

Information on how to name layers [Some detailed notes](https://www.reddit.com/r/StableDiffusionInfo/comments/ylp6ep/some_detailed_notes_on_automatic1111_prompts_as/).