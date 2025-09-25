import string
import random
from pathlib import Path
from src.utils.meta_data.course_data import COURSES, INSTRUCTORS
from src.utils.meta_data.tp_data import TP_NAMES


#Fees/Rupees
def get_random_digits():
    return f"{random.choices(string.digits,k=5)}"

#Instructor Name
def get_random_instructor_name():
    return f"{random.choice(INSTRUCTORS)}"

#course name
def get_random_course_name():
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"COURSE {random.choice(COURSES)} - {suffix}"

#TP name
def get_random_tp_name():
    return f"{random.choice(TP_NAMES)}"

#field text
def get_random_data():
    suffix = "".join(random.choices(string.ascii_lowercase +string.digits, k=10))
    return f"{suffix}"

#Image
def get_random_image():
    project_root = Path(__file__).resolve().parents[3]
    images_dir = project_root / "resources" / "images"
    image_files = [f for f in images_dir.iterdir() if f.is_file() and f.suffix.lower() in (".jpg", ".jpeg", ".png")]
    if not image_files:
        raise FileNotFoundError(f"No images found in {images_dir}")
    return str(random.choice(image_files))

#fill same fields
async def fill_same_fields(page,locator):
    for i in range(1, 5):
        field_id = f"{locator}{i}"
        random_text = get_random_data()
        await page.fill(field_id,f"Learning Objective {i} "+random_text)
        print(f"Learning Objective {i} : {random_text}")
