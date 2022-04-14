# Substrate version of the Grassland Inference Container

## Building the image

cd into the repo's root directory


```
docker build -t grassland_substrate_inference_container:0.1 .
```

## Running the container

Ensure that the Substrate version of the Grassland full node is running first. This inference container assumes that the node is listening for incoming WebSocket traffic on 127.0.0.1:9944

```
docker run -t --gpus all --rm --network=host grassland_substrate_inference_container:0.1
```

## Default URL's

The default RTSP URL that it reads from is "rtsp://0.0.0.0:8554/live.stream". Change the RTSP URL to whatever feed you're reading from by appending the following to the end of the "docker run...." command above.

```
--source [YOUR RTSP URL]
```

