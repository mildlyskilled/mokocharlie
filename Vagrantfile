# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "private_network", ip: "192.168.33.10"
  config.vm.synced_folder ".", "/home/vagrant"
  config.vm.hostname = "mokocharlie.dev"
  config.vm.provider "virtualbox" do |v|
    v.name = "moko"
  end
  config.vm.provision :shell, path: "vagrant_bootstrap.sh"
  config.ssh.insert_key = true
end
