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
		sudo yum install epel-release -y &> /dev/null
	  sudo yum -y install python-pip &> /dev/null ;
    fi ;
	else
		echo "pip installed, moving on"
  fi
	Pip_req
}

Pip_req(){
	pip install nexmo &> /dev/null
	pip install requests &> /dev/null
  pip install bs4 &> /dev/null
}


Initialize(){
  read -p "Enter name : " name
	mkdir ~/.$name
  cp phone_number.py ~/.$name/
  cp set_initials.py ~/.$name/
  cp main.py ~/.$name/


  cd ~/.$name
	chmod +x phone_number.py
	chmod +x set_initials.py

	./phone_number.py
  ./set_initials.py && echo "phone number verified"
  echo  "* * * * * /usr/bin/env python2.7 $(pwd)/main.py" > mycron
  crontab mycron
  rm mycron
  echo 0 > callnum.txt


}



Verify_Pip
Initialize
