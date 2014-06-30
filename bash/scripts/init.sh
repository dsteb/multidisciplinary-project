echo "PASSWORD_HERE" | sudo -Sv 
sudo apt-get -y install git
pushd ~/mdp
	wget https://bootstrap.pypa.io/get-pip.py
	sudo python get-pip.py
	sudo pip install beautifulsoup4
	sudo pip install futures
	git clone https://github.com/n43jl/mdp.git
popd


