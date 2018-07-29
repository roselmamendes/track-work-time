docker run --rm -v "$PWD":/usr/src/app -w /usr/src/app -it track-work-time flake8 .

docker run --rm -v "$PWD":/usr/src/app -w /usr/src/app -it track-work-time bandit -r .

docker run --rm -v "$PWD":/usr/src/app -w /usr/src/app -it track-work-time python -m unittest
