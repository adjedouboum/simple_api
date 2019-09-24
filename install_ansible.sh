#!/bin/bash
# script to install ansible to deploy some ressource using playbook  
sudo apt-add-repository ppa:ansible/ansible
sudo apt -y update
sudo apt -y install ansible
