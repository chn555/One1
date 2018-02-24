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


InitializeSMS(){
  read -p "Enter name : " name
	mkdir ~/.One1/$name -p
  cp phone_number.py ~/.One1/$name
  cp set_initials.py ~/.One1/$name
  cp main.py ~/.One1/$name

  read -p "Please enter your nexmo key : " key
  read -p "Please enter your nexmo secret key : " secret
  read -p "Please enter your gmail username : " gusr
  read -p "Please enter your gmail app password : " gpwd


  cd ~/.One1/$name
	chmod +x phone_number.py
	chmod +x set_initials.py

	./phone_number.py
  ./set_initials.py -$key -$secret && echo "phone number verified"
  touch run.sh
  echo "#!/bin/bash" > run.sh
  echo "cd $(pwd)" > run.sh
  echo "/usr/bin/env python2.7 main.py -$key -$secret -$gusr -$gpwd" >> run.sh
  chmod +x run.sh

  echo  "* * * * * bash $(pwd)/run.sh" > mycron
  crontab -l >> mycron
  crontab mycron
  rm mycron
  echo 0 > callnum.txt


}

InitializeEMAIL(){
  read -p "Enter name : " name
	mkdir ~/.One1/$name -p
  cp phone_number.py ~/.One1/$name
  cp set_initials_email.py ~/.One1/$name
  cp mainEmail.py ~/.One1/$name

  read -p "Please enter your email address : " email
  read -p "Please enter your gmail username : " gusr
  read -p "Please enter your gmail app password : " gpwd


  cd ~/.One1/$name
    echo $email > email.txt
	chmod +x phone_number.py
	chmod +x set_initials_email.py

	./phone_number.py
  ./set_initials_email.py  && echo "phone number verified"
  touch run.sh
  echo "#!/bin/bash" > run.sh
  echo "cd $(pwd)" > run.sh
  echo "/usr/bin/env python2.7 mainEmail.py -$key -$secret -$gusr -$gpwd" >> run.sh
  chmod +x run.sh

  echo  "* * * * * bash $(pwd)/run.sh" > mycron
  crontab -l >> mycron
  crontab mycron
  rm mycron
  echo 0 > callnum.txt


}

menu (){

echo "     Select the version you want to use "
echo " 1. Use the SMS version, this uses nexmo and costs money"
echo " 2. Use the EMAIL version, this uses gmail and is free "

read choise
case $choise in
    1) InitializeSMS
    ;;

    2) InitializeEMAIL
       ;;

    *) echo "Invalid output, please try again"
        menu
        ;;
esac
}
Verify_Pip
menu
