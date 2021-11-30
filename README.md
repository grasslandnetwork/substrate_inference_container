# inference_container

## Building the image

cd into the repo's root directory


```
docker build -t 932200675199.dkr.ecr.ca-central-1.amazonaws.com/inference_container:1.0 . 
```

## Running the container

```
sudo docker run -t --gpus all --rm --network=host 932200675199.dkr.ecr.ca-central-1.amazonaws.com/inference_container:1.0
```

## Default URL's

The default RTSP URL that it reads from is below. Change the value to the output RTSP URL of the kinesis_to_rtsp container

```
--source rtsp://0.0.0.0:8554/live.stream 
```
## Default Output
Right now, a summary of the results is just printed to the terminal
