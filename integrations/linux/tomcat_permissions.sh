# This file will add "tomcat" to the sudoers file.
# "tomcat" is the Jenkins user name by default on Bitnami Jenkins machines

# To become tomcat from a different user, use the following:
# sudo su tomcat
# bash

sudo sh -c "echo \"%tomcat ALL=(ALL:ALL) ALL\" >> /etc/sudoers"
sudo sh -c "echo \"%tomcat ALL=(ALL) NOPASSWD: ALL\" >> /etc/sudoers"
sudo sh -c "echo \"tomcat ALL=NOPASSWD: ALL\" >> /etc/sudoers"
