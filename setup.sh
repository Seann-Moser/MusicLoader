
if ! [ -x "$(command -v brew)" ]; then
  echo "installing homebrew"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  exit
fi


if ! [ -x "$(command -v ffmpeg)" ]; then
  echo "install ffmpeg"
  brew install ffmpeg
fi


if ! [ -x "$(command -v python3)" ]; then
  echo "install python"
  brew install python
fi

echo "install pip requirements"
pip3 install -r requirements.txt