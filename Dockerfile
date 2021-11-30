FROM ufoym/deepo:pytorch-py36-cu100

RUN apt update && \
	apt install -y zip \
	htop screen \
	libgl1-mesa-glx 
RUN pip install --upgrade pip
RUN pip install -U seaborn \
	thop
RUN pip install -U absl-py==0.14.1 \
	cachetools==4.2.4 \
	certifi==2021.5.30 \
	charset-normalizer==2.0.6 \
	cloudpickle==1.2.1 \
	cycler==0.10.0 \
	Cython==0.29.13 \
	dataclasses==0.8 \
	enum34==1.1.6 \
	future==0.17.1 \
	google-auth==1.35.0 \
	google-auth-oauthlib==0.4.6 \
	grpcio==1.41.0 \
	idna==3.2 \
	importlib-metadata==4.8.1 \
	joblib==0.13.2 \
	kiwisolver==1.1.0 \
	Markdown==3.3.4 \
	matplotlib==3.3.4 \
	numpy==1.19.5 \
	oauthlib==3.1.1 \
	opencv-python==4.5.3.56 \
	pandas==0.25.0 \
	Pillow==8.3.2 \
	pip==21.2.4 \
	protobuf==3.9.1 \
	pyasn1==0.4.8 \
	pyasn1-modules==0.2.8 \
	pycocotools==2.0.0 \
	PyGObject==3.26.1 \
	pyparsing==2.4.2 \
	python-apt==1.6.4 \
	python-dateutil==2.8.0 \
	python-distutils-extra==2.39 \
	pytz==2019.2 \
	PyYAML==5.4.1 \
	requests==2.26.0 \
	requests-oauthlib==1.3.0 \
	rsa==4.7.2 \
	scikit-learn==0.21.3 \
	scipy==1.5.4 \
	seaborn==0.11.2 \
	setuptools==41.1.0 \
	six==1.12.0 \
	tensorboard==2.6.0 \
	tensorboard-data-server==0.6.1 \
	tensorboard-plugin-wit==1.8.0 \
	thop==0.0.31.post2005241907 \
	torch==1.7.0 \
	torch-nightly==1.2.0.dev20190805 \
	torchvision==0.8.1 \
	tqdm==4.62.3 \
	typing==3.7.4 \
	typing-extensions==3.10.0.2 \
	urllib3==1.26.7 \
	Werkzeug==2.0.1 \
	wheel==0.33.4 \
	zipp==3.6.0
RUN apt install -y libsm6 && \
	apt-get clean
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
	unzip awscliv2.zip && \
	./aws/install
ADD app/ /app/
RUN aws s3 cp s3://gln-inference-models/p6.pt /app/
WORKDIR /app/
ENTRYPOINT ["python", "detect.py"]
CMD ["--source", "rtsp://0.0.0.0:8554/live.stream", "--cfg", "cfg/p6.cfg", "--weights", "p6.pt", "--conf", "0.25", "--img-size", "1920", "--device", "0"]