#!/bin/bash
#
#installs the One1 script and adds it to cron
#written by chn555


Verify_Pip(){

  if [ "" == "`command -v pip`" ]; then
	  echo "pip Not Found";
	  if [ -n "`command -v apt-get`" ]; then
		echo "Installing pip, please wait"
	  sudo apt-get -y install python-pip &> /dev/null ;
    elif [ -n "`command -v yum`" ]; then
		echo "Installing pip, please wait"
		sudo yum install epel-release -y
	  sudo yum -y install python-tools &> /dev/null ;
    fi ;
	else
		echo "pip installed, moving on"
  fi
	Pip_req
}

Pip_req(){
	pip install nexmo
	pip install requests
}


Initialize(){
	mkdir ~/.One1
	chmod +x phone_number.py
	chmod +x set_initials.py
	./phone_number.py
  ./set_initials.py && echo "phone number verified"

}



Verify_Pip
Initialize
