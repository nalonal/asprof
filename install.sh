sudo apt update
sudo apt install lsb-release ca-certificates apt-transport-https software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
git config --global user.name "nalonal"
git config --global user.email "rionaldyrizqy@gmail.com"
wget -nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -f ./google-chrome-stable_current_amd64.deb -y
sudo apt install python3-pip -y
sudo apt install docker-ce -y
mkdir -p ~/.docker/cli-plugins/
curl -SL https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose
sudo chmod 666 /var/run/docker.sock
pip3 install -r requirements.txt
sudo apt-get install tor -y
sudo sh -c 'echo "ControlPort 9051" >> /etc/tor/torrc'
sudo sh -c 'echo "CookieAuthentication 1" >> /etc/tor/torrc'
sudo sh -c 'echo "$(echo "HashedControlPassword ")$(sudo tor --hash-password asprof | tail -n1)" >> /etc/tor/torrc'
sudo service tor restart
docker compose up -d
wget https://dl.minio.io/server/minio/release/linux-amd64/minio
chmod +x minio
