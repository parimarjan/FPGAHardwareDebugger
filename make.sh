./bake clean
./bake
sudo kextunload -b com.apple.driver.AppleUSBFTDI
cd build
make upload
cd ..
# upload the driver again so we can do the stuff with ports
sudo kextload -b com.apple.driver.AppleUSBFTDI
