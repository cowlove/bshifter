apt-get install firefox-geckodriver
pip3 install octoprint-cli
# add ~/.local/bin/ to path 

git clone https://github.com/AllwineDesigns/stl_cmd.git
cd stl_cmd
make
make install # will install to /usr/local/bin by default
