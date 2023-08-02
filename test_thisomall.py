import argparse
import logging
import os

import cv2
import torch
import yt_dlp
from mivolo.data.data_reader import InputType, get_all_files, get_input_type
from mivolo.predictor import Predictor
from timm.utils import setup_default_logging
import glob

_logger = logging.getLogger("inference")



def get_parser():
    parser = argparse.ArgumentParser(description="PyTorch MiVOLO Inference")
    parser.add_argument("--input", type=str, default=None, required=True, help="image file or folder with images")
    parser.add_argument("--output", type=str, default=None, required=True, help="folder for output results")
    parser.add_argument("--detector-weights", type=str, default=None, required=True, help="Detector weights (YOLOv8).")
    parser.add_argument("--checkpoint", default="", type=str, required=True, help="path to mivolo checkpoint")

    parser.add_argument(
        "--with-persons", action="store_true", default=False, help="If set model will run with persons, if available"
    )
    parser.add_argument(
        "--disable-faces", action="store_true", default=False, help="If set model will use only persons if available"
    )

    parser.add_argument("--draw", action="store_true", default=False, help="If set, resulted images will be drawn")
    parser.add_argument("--device", default="cuda", type=str, help="Device (accelerator) to use.")
    parser.add_argument('--dir_json', type= str, default='./')
    parser.add_argument('--dir_image', type= str, default= './')
    return parser


def main():
    parser = get_parser()
    setup_default_logging()
    args = parser.parse_args()

    if torch.cuda.is_available():
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.benchmark = True
    os.makedirs(args.output, exist_ok=True)

    predictor = Predictor(args, verbose=True)
    image_files = list(glob.glob(f"{args.dir_path}/*"))
    
    for img_p in image_files:

        img = cv2.imread(img_p)
        detected_objects, out_im, ages, genders = predictor.recognize(img)

        if args.draw:
            bname = os.path.splitext(os.path.basename(img_p))[0]
            filename = os.path.join(args.output, f"out_{bname}.jpg")
            cv2.imwrite(filename, out_im)
            _logger.info(f"Saved result to {filename}")
        print(ages[0], genders[0])

if __name__ == "__main__":
    main()
