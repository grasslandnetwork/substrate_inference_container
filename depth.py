import numpy as np
import os
import torch
# import utilio
import cv2
from torchvision.transforms import Compose

from dpt.models import DPTDepthModel
from dpt.transforms import Resize, NormalizeImage, PrepareForNet
import time


# make a class for depth model
class Depth:
    # initialize the model
    def __init__(self, optimize=True):
        self.optimize = optimize
        print("initialize depth model")

        # select device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print("device: %s" % self.device)


        #model_type == "dpt_hybrid_nyu":
        net_w = 640
        net_h = 480

        self.model = DPTDepthModel(
            path="weights/dpt_hybrid_nyu-2ce69ec7.pt",
            scale=0.000305,
            shift=0.1378,
            invert=True,
            backbone="vitb_rn50_384",
            non_negative=True,
            enable_attention_hooks=False,
        )

        normalization = NormalizeImage(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])


        self.transform = Compose(
            [
                Resize(
                    net_w,
                    net_h,
                    resize_target=None,
                    keep_aspect_ratio=True,
                    ensure_multiple_of=32,
                    resize_method="minimal",
                    image_interpolation_method=cv2.INTER_CUBIC,
                ),
                normalization,
                PrepareForNet(),
            ]
        )

        self.model.eval()

        if self.optimize == True and self.device == torch.device("cuda"):
            self.model = self.model.to(memory_format=torch.channels_last)
            self.model = self.model.half()

        self.model.to(self.device)

    

    def run(self, frame):
        """Run MonoDepthNN to compute depth maps.

        Args:
            frame (str): path to input image
           
        """

        frame = cv2.imread(frame)

        start_time = time.perf_counter()
        
        print("start processing {} )".format(frame))

        if frame.ndim == 2:
            print("ndim")
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)


        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) / 255.0


        frame_trnsf = self.transform({"image": frame})["image"]

        print("frame_trnsf")
        print(frame_trnsf)

        # compute
        with torch.no_grad():
            sample = torch.from_numpy(frame_trnsf).to(self.device).unsqueeze(0)

            if self.optimize == True and self.device == torch.device("cuda"):
                sample = sample.to(memory_format=torch.channels_last)
                sample = sample.half()

            prediction = self.model.forward(sample)
            prediction = (
                torch.nn.functional.interpolate(
                    prediction.unsqueeze(1),
                    size=frame.shape[:2],
                    mode="bicubic",
                    align_corners=False,
                )
                .squeeze()
                .cpu()
                .numpy()
            )




            # prediction *= 1000.0
            # print("prediction", prediction)
            # utilio.write_depth("depthmap", prediction, bits=2)

            end_time = time.perf_counter()
            elapsed_time_ms = (end_time - start_time) * 1000
            print(f"Depth Map Perf.: {elapsed_time_ms:.2f} ms")
            return prediction





