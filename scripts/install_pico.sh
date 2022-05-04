sudo apt-get install libpopt-dev
git clone https://github.com/naggety/picotts
cd picotts/pico
./autogen.sh
./configure
make
sudo make install
cd ../..

