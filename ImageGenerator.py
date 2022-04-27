from pathlib import Path

from PIL import Image
import random
import json

# Each image is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%

background = ["Blue"]
background_weights = [100]

body = ["Black Coat"]
body_weights = [100]

faceAccessories = ["Beard"]
faceAccessories_weights = [100]

mouthAccessories = ["Chewing Gum"]
mouthAccessories_weights = [100]

eye = ["Blue Eye"]
eye_weights = [100]

eyeWear = ["Sun Glasses"]
eyeWear_weights = [100]

headWear = ["Snapback"]
headWear_weights = [100]

# Dictionary variable for each trait.
# Each trait corresponds to its file name

background_files = {
    "Blue": "BLUE"
}

body_files = {
    "Black Coat": "BLACK-COAT"
}

faceAccessories_files = {
    "Beard": "BEARD"
}

mouthAccessories_files = {
    "Chewing Gum": "CHEWING-GUM"
}

eye_files = {
    "Blue Eye": "BLUE-EYE"
}

eyeWear_files = {
    "Sun Glasses": "SUN-GLASSES"
}

headWear_files = {
    "Snapback": "SNAPBACK"
}

# Generate Traits
TOTAL_IMAGES = 1000  # Number of random unique images we want to generate
all_images = []


# A recursive function to generate unique image combinations
def create_new_image():
    new_image = {"Background": random.choices(background, background_weights)[0],
                 "Body": random.choices(body, body_weights)[0],
                 "Face Accessories": random.choices(faceAccessories, faceAccessories_weights)[0],
                 "Mouth Accessories": random.choices(mouthAccessories, mouthAccessories_weights)[0],
                 "Eyes": random.choices(eye, eye_weights)[0], "Eye Wear": random.choices(eyeWear, eyeWear_weights)[0],
                 "Head Wear": random.choices(headWear, headWear_weights)[0]}  #

    # For each trait category, select a random trait based on the weightings

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image


# Generate the unique combinations based on trait weightings
for i in range(TOTAL_IMAGES):
    new_trait_image = create_new_image()
    all_images.append(new_trait_image)


# Returns true if all images are unique
def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)


print("Are all images unique?", all_images_unique(all_images))
if not all_images_unique(all_images):
    raise SystemExit(0);

# Add token Id to each image
i = 1
for item in all_images:
    item["tokenId"] = i
    i = i + 1

# Get Trait Counts
background_count = {}
for item in background:
    background_count[item] = 0

body_count = {}
for item in body:
    body_count[item] = 0

faceAccessories_count = {}
for item in mouthAccessories:
    faceAccessories_count[item] = 0

mouthAccessories_count = {}
for item in mouthAccessories:
    mouthAccessories_count[item] = 0

eye_count = {}
for item in eye:
    eye_count[item] = 0

eyeWear_count = {}
for item in eyeWear:
    eyeWear_count[item] = 0

headWear_count = {}
for item in headWear:
    headWear_count[item] = 0

for image in all_images:
    background_count[image["Background"]] += 1
    body_count[image["Body"]] += 1
    faceAccessories_count[image["Face Accessories"]] += 1
    mouthAccessories_count[image["Mouth Accessories"]] += 1
    eye_count[image["Eyes"]] += 1
    eyeWear_count[image["Eye Wear"]] += 1
    headWear_count[image["Head Wear"]] += 1

# Create necessary directories
basePathFinalGen = r"C:\nftproject"
Path(fr"{basePathFinalGen}\final-gen\images").mkdir(parents=True, exist_ok=True)
Path(fr"{basePathFinalGen}\final-gen\metadata").mkdir(parents=True, exist_ok=True)

# Generate Metadata for all Traits
METADATA_FILE_NAME = fr'{basePathFinalGen}\final-gen/all-traits.json'
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)

basePath = r"C:\nftproject\Traits"

# Generate Images
for item in all_images:
    im1 = Image.open(f'{basePath}/7_backgrounds/{background_files[item["Background"]]}.png').convert('RGBA')
    im2 = Image.open(f'{basePath}/6_body/{body_files[item["Body"]]}.png').convert('RGBA')
    im3 = Image.open(f'{basePath}/5_face_accessories/{faceAccessories_files[item["Face Accessories"]]}.png').convert(
        'RGBA')
    im4 = Image.open(f'{basePath}/4_mouth_accessories/{mouthAccessories_files[item["Mouth Accessories"]]}.png').convert(
        'RGBA')
    im5 = Image.open(f'{basePath}/3_eyes/{eye_files[item["Eyes"]]}.png').convert('RGBA')
    im6 = Image.open(f'{basePath}/2_eyewear/{eyeWear_files[item["Eye Wear"]]}.png').convert('RGBA')
    im7 = Image.open(f'{basePath}/1_headwear/{headWear_files[item["Head Wear"]]}.png').convert('RGBA')

    # Create each composite
    com1 = Image.alpha_composite(im1, im2)
    com2 = Image.alpha_composite(com1, im3)
    com3 = Image.alpha_composite(com2, im4)
    com4 = Image.alpha_composite(com3, im5)
    com5 = Image.alpha_composite(com4, im6)
    com6 = Image.alpha_composite(com5, im7)

    rgb_im = com6.convert('RGB')
    file_name = str(item["tokenId"]) + ".png"
    rgb_im.save(fr"{basePath}\final-gen\images/" + file_name)

# Generate metadata

metadataFiles = open(fr"{basePath}\final-gen/all-traits.json")
data = json.load(metadataFiles)

imageBaseUri = "ipfs://REPLACE/"
projectName = "PROJECT_NAME"


def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value
    }


# Create metadata files
for i in data:
    token_id = i['tokenId']
    token = {
        "image": imageBaseUri + str(token_id) + '.png',
        "tokenId": token_id,
        "description": "",
        "name": projectName + ' #' + str(token_id),
        "attributes": []
    }
    token["attributes"].append(getAttribute("Background", item["Background"]))
    token["attributes"].append(getAttribute("Body", item["Body"]))
    token["attributes"].append(getAttribute("Face Accessories", item["Face Accessories"]))
    token["attributes"].append(getAttribute("Mouth Accessories", item["Mouth Accessories"]))
    token["attributes"].append(getAttribute("Eyes", item["Eyes"]))
    token["attributes"].append(getAttribute("Eye Wear", item["Eye Wear"]))
    token["attributes"].append(getAttribute("Head Wear", item["Head Wear"]))

    with open(fr"{basePath}\final-gen\metadata/" + str(token_id) + '.json',
              'w') as outfile:
        json.dump(token, outfile, indent=4)

# Dump Counts
imageCounts = {
    "Backgrounds": background_count,
    "Eyes": eye_count,
    "Eye Wear": eyeWear_count,
    "Face Accessories": faceAccessories_count,
    "Head Wear": headWear_count,
    "Mouth Accessories": mouthAccessories_count,
    "Body": body_count,
}
with open(fr"{basePath}\final-gen\trait-counts.json", 'w') as outfile:
    json.dump(imageCounts, outfile, indent=4)
