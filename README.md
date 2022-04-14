# Substrate version of the Grassland Inference Container

## Building the image

cd into the repo's root directory


```
docker build -t grassland_substrate_inference_container:0.1 .
```

## Running the container

Ensure that the Substrate version of the Grassland full node is running first. This inference container assumes that the node is listening for incoming WebSocket traffic on 127.0.0.1:9944

```
sudo docker run -t --gpus all --rm --network=host grassland_substrate_inference_container:0.1
```

## Default URL's

The default RTSP URL that it reads from is below. Change the value to the output RTSP URL of the kinesis_to_rtsp container

```
--source rtsp://0.0.0.0:8554/live.stream 
```

