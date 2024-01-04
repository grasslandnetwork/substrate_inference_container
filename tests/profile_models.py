# import torch
# torch.manual_seed(0)
# torch.use_deterministic_algorithms(True)
# torch.backends.cudnn.benchmark = False
# torch.backends.cudnn.deterministic = True

import cv2 as cv


from depth import Depth
#initialize depth model
depth = Depth()

rgb = 'app/example_photo.jpg'


depth_map = depth.run(rgb)
