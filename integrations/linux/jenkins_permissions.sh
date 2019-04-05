# This file will add "jenkins" to the sudoers file.

# To become jenkins from a different user, use the following:
# sudo su jenkins
# bash

sudo sh -c "echo \"%jenkins ALL=(ALL:ALL) ALL\" >> /etc/sudoers"
sudo sh -c "echo \"%jenkins ALL=(ALL) NOPASSWD: ALL\" >> /etc/sudoers"
sudo sh -c "echo \"jenkins ALL=NOPASSWD: ALL\" >> /etc/sudoers"
