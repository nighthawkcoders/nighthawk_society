IntelliJ IDEA Python Development
-------------

# Walruses README
### Project Checkpoint Week 2
- [Ridhima's Ticket](https://github.com/nighthawkcoders/nighthawk_society/issues/23#issue-915876084): I worked on finishing the filtering process within the projectdata.py. I also created a projectclass.py where I created a Project class that had created the self.filter option as well. I made sure to contribute more with the backend aspect especially dealing with the python end. 
-  [Isai's Ticket](https://github.com/nighthawkcoders/nighthawk_society/issues/20#issue-909195031): I worked on connecting the HTML to the database prtion, however, I faced the issue of persistent storage, which is the same issue I faced with WASC website. This means the comments were not being stored in a database or some storage mechanism so that when the user refreshes the page it will stay there. I researched various scripts that would solve this issue and found HTML box, which takes care of the persistent storage mechanism. I will have to see if the CSS can be changed or not for this comment feature. 
-  [Sriya's Ticket](https://github.com/nighthawkcoders/nighthawk_society/issues/15): I worked on the HTML cards and connecting them to the backend projectdata.py file. I added the variables from each project dictionary into the HTML file so that I do not have to hardcode each. I also worked on the backend by helping Ridhima create the Project class and the blueprint app route on projectapp.py. Next week, I will work on the projectdetail.html page and get it up and running. I will also work with Ridhima on getting the images up on the cards.
-  [Grace's Ticket](https://github.com/nighthawkcoders/nighthawk_society/issues/21): I worked on building a search filter for the project cards. I added javascript in the html and tried to create a function that would search through each key word. My work is still in progress and I am filtering out all the projects. I took a simple example and I added more to the function to allow a search function. I will work this week try and get the search filter up and running.
### Project Checkpoint Week 1
- [Sriya's Ticket](https://github.com/nighthawkcoders/nighthawk_society/issues/14): I worked on creating the **frontend** for the project menu based on our [project plan](https://docs.google.com/presentation/d/1CFiTaqvGOJBBHy6SLb8dqiXlm94fUvoZnKz5r99-06Y/edit#slide=id.gd3dc9efc7b_0_107). I utilized **Bootstrap** to create the cards and edited **CSS** to ensure that the cards would be in 4 columns. [Next week](https://github.com/nighthawkcoders/nighthawk_society/issues/16), I will be working with Iniyaa on the frontend and backend of the chat feature. Once the backend of the filtering is near complete (dictionaries are created for each project), I will use a **for loop** to replace the current text for the project name, scrum team, developers, and image, just like Sophie's project so that we can shave off excess HTML & CSS.
- [Iniyaa's Ticket](https://github.com/nighthawkcoders/nighthawk_society/issues/18): I worked on starting the backend for the chat feature. I used flask forms and the method POST. Currently, it is not connected to a database that will update based on the comments that are submitted - my next goal is to create this database and make sure it updates based on what is input to the website. 
- [Ridhima's Ticket](https://github.com/nighthawkcoders/nighthawk_society/projects/1#card-62301064): I worked on starting to create the backend for the filteration process. I did this by creating a function for each of the projects and then creating unanimous variables under each of the functions. Then I created another function that took those function's attributes and appended them into a common filtering dictionary.
- [Isai's Ticket](https://github.com/nighthawkcoders/nighthawk_society/projects/1#card-62301760): I worked on the backend for the comment/chat funtion where users input their opinions of the projects. I used POST to get the user inputs in main.py. In comment.py, I created the function (storecom) that creates a table and stores the values into the database "walrus.db". I called this function in main.py after establishing a connection to the database. Additionally, the user inputs were passed as parameters into the function "storecom". 
- [Grace's Ticket](https://github.com/nighthawkcoders/nighthawk_society/projects/1#card-62353746): I worked on both frontend and backend of code. My goal was to create a functional search bar and filter for the user to find specific projects. I wanted the user to type in a project title or team name, so that specific card would pull up. Using html, python and json, I was able to create a functional search bar.

# How to develop code for this Project
## This project was developed using IntelliJ IDEA with Python Plugin.  Following are tool requirements.

    Install IntelliJ IDEA  [Download](https://www.jetbrains.com/idea/)
    Install Python [Download](https://www.python.org/downloads/release/python-390/)
    Install Git [Download](https://git-scm.com/downloads) </li>
    Run IntelliJ, on main screen "Configure" search for and install Python Plugin
    Returning to main screen "Get from Version Control" the URL of this Github project
    To start web service look for run symbol in wsgi.py
    Dependencies are in requirements.txt
    Imports are in views.py and typically a hover of any red underlined object will enable import



Flask/Python Webserver Deployment
-------------

# How to initially deploy a Production Web Site on Raspberry Pi or Ubuntu
```diff
+ As a biginner this should take approximately 1 hour, just 15 minutes as you acquire experience  
```
## Visual overview: [Visuals of Deployment](https://padlet.com/jmortensen7/flaskdeploy)
## References used: [Digital Ocean article](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04)

## An application is typically written using a developer-friendly framework, this project is using Flask. The application code does not care about anything except being able to process single requests.  Thus, when we scale up to the Web we add small services to handle problems that are the same across most web applications.  A Python Web Server Gateway Interface (WSGI) is a way to make sure that web servers and python web applications can talk to each other. So somewhere inside your application (usually a wsgi.py file) an object is defined which can be invoked by Gunicorn (app).

## Gunicorn takes care of everything which happens in-between the web server and a the Flask web application. This way, when coding up a Flask application we don’t need to find your own solutions for:
<ol>
  <li>Communicating with multiple web servers</li>
  <li>Reacting to lots of web requests at once and distributing the load</li>
  <li>Keepiung multiple processes of the web application running</li>
</ol>

## Nginx is the web server:  it accepts requests, takes care of general domain logic and takes care of handling https connections. Only requests which are meant to arrive at the application are passed on toward the application server (Gunicorn) and the application itself (Flask). 

## Setup Virtual environment, clone code from GitHub, and get a Test Server running
#### In console/terminal (first time only: setup environment)...

pi@raspberrypi:~ $  ``` sudo apt update; sudo apt upgrade```

pi@raspberrypi:~ $  ``` sudo apt install python3-pip nginx```

pi@raspberrypi:~ $  ``` sudo pip3 install virtualenv```

#### Get code and move into your project directory (clone is 1st time only; after you use pull in project directory...

pi@raspberrypi:~ $  ``` cd ~; git clone https://github.com/nighthawkcoders/nighthawk_society```

pi@raspberrypi:~ $  ``` cd ~/nighthawk_society```

#### Create virtualenv environment (virtualenv create is first time only: test for python3)...

pi@raspberrypi:~/nighthawk_society $ ```virtualenv -p /usr/bin/python3 nighthawk``` 

pi@raspberrypi:~/nighthawk_society $ ```source nighthawk/bin/activate```

(nighthawk) pi@raspberrypi:~/nighthawk_society $   ``` python -V```

#### Install dependencies...

(nighthawk) pi@raspberrypi:~/nighthawk_society $ ``` pip install gunicorn```

(nighthawk) pi@raspberrypi:~/fnighthawk_society $ ```  sudo pip install -r requirements.txt```

#### Start an application test server, same as we do on development machine

(nighthawk) pi@raspberrypi:~/nighthawk_society $ ``` python main.py ``` 

in your browser ...

http://localhost:8080/ 

stop test server by typing control-c in terminal

(nighthawk) pi@raspberrypi:~/nighthawk_society $ ``` ^c ``` 

#### Leave project environemnt and return to home directory...

(nighthawk) pi@raspberrypi:~/nighthawk_society $ ``` deactivate```

pi@raspberrypi:~/nighthawk_society $  ``` cd```

pi@raspberrypi:~/


### Build Gunicorn configuration file.  Interesting bits...
<ol>
<li> 'ExecStart' start statement looks into main.py for app (main:app) and starts unix sock as defined in file. </li>
<li> 'ExecStart' -workers 3 starts thread processes that are listening for connections, this ties into load balancing. </li>
</ol>

```diff
- project specific information changes: nighhawk, nighthawk_society, main:app 
+ REPLACE with your project name and information
```

#### In console/terminal with nano, vi, or other text editor (setup Gunicorn configuration file)...

pi@raspberrypi:~ $  ``` sudo nano /etc/systemd/system/nighthawk.service```

    [Unit]
    Description=Gunicorn instance to serve nighthawk web project
    After=network.target

    [Service]
    User=pi
    Group=www-data
    WorkingDirectory=/home/pi/nighthawk_society
    Environment="PATH=/home/pi/nighthawk_society/nighthawk/bin"
    ExecStart=/home/pi/nighthawk_society/nighthawk/bin/gunicorn --workers 3 --bind unix:nighthawk.sock -m 007 main:app

    [Install]
    WantedBy=multi-user.target

### Build Nginx configuration file.  Requirements [Internet Domain](https://docs.google.com/document/d/1nODveWp0jBzj4ZpFLgWCWTOXzLAHAPUhAQYmZJ4LhyU/edit), Host IP address, [Internet IP address](http://127.0.0.1:8080/pi/portforward).
<ol>
  <li> Obtain your own 'server_name' values; these VALUES WILL NOT WORK for your environment</li>
  <li> 'listen' is the port for nginx, this port will be used when you port forward </li>
  <li> 'proxy_pass' is passing connect along to gunicorn server </li>
</ol>

```diff
- THESE server_name values MUST CHANGE to match your solution:  
- nighthawkcoders.cf
+ REPLACE with yourdomain.com
```
#### In console/terminal with nano, vi, or other text editor (first time only: setup Nginx configuration file)...

pi@raspberrypi:~ $  ``` sudo nano /etc/nginx/sites-available/homesite```

    server {
        listen 80;
        server_name nighthawkcoders.cf;

        location / {
            include proxy_params;
            proxy_pass http://unix:/home/pi/nighthawk_society/nighthawk.sock;
        }
    }


## Prepare for Gunicorn usage and verify
#### In console/terminal test Gunicorn test Server and virify (first time only: gunicor exectuion)...

(nighthawk) pi@raspberrypi:~/nighthawk_society $ ```nighthawk/bin/gunicorn --bind 0.0.0.0:8080 main:app```

in your browser ...

http://localhost:8080/ 

(nighthawk) pi@raspberrypi:~/nighthawk_society $ ``` ^c ``` 


## Validate Gunicorn configuration file and enable service permanently
#### In console/terminal start Gunicorn

pi@raspberrypi:~ $ ```sudo systemctl start nighthawk.service```

pi@raspberrypi:~ $ ```sudo systemctl enable nighthawk.service```
 
check the status...

pi@raspberrypi:~ $ ```sudo systemctl status nighthawk.service```

stop status by typing q in terminal


## Validate Nginx configuration file and enable service permanently
#### In console/terminal start Nginx

link file...

pi@raspberrypi:~ $ ```sudo ln -s /etc/nginx/sites-available/nighthawk /etc/nginx/sites-enabled```

test for errors...

pi@raspberrypi:~ $ ```sudo nginx -t```

start the web server...

pi@raspberrypi:~ $ ```sudo systemctl restart nginx```

check nginx status...

pi@raspberrypi:~ $ ```sudo systemctl status nginx```

stop status by typing q in terminal

in address bar of browser on another device in LAN type IP address of this Nginx server ...

```diff
- This IP address MUST CHANGE to match your Raspberry Pi 
+ REPLACE with yourpi-ip
```
http://192.168.1.245/

reboot to verify Nginx server config is permanent ...

next task is port forward Nginx server via public IP address on the internet ...



Flask/Python Webserver Update (aka Refresh)
-------------

# How to update Production Web Site on Raspberry Pi after initial setup
```diff
+ 5 minutes to do an update; if you have good branch managment this could be auto sceduled with crontab  
```
## Pull code from Github and update packages
#### In console/terminal (every update: pull code and check package dependencies)...

pi@raspberrypi:~ $  ``` sudo apt update; sudo apt upgrade```

pi@raspberrypi:~ $  ``` cd ~/nighthawk_society```

pi@raspberrypi:~/nighthawk_society $ ```  git pull```

pi@raspberrypi:~/nighthawk_society $ ```  source nighthawk/bin/activate```

#### In console/terminal with virtualenv activitate (every time: check and update packages)...

(nighthawk) pi@raspberrypi:~/nighthawk_society $ ```  sudo pip install -r requirements.txt```

#### In console/terminal (every time AFTER initial setup: restart gunicorn)...

pi@raspberrypi:~ $ ```sudo systemctl restart nighthawk.service```



Raspberry Pi Purchase
-------------

# Instruction on purchasing a Raspberry Pi and preparing for Webserver deployment
Raspberry Pi 4 specification
<OL> 
<li> Raspberry Pi 4 4GB Model B with 1.5GHz 64-bit quad-core CPU (4GB RAM) </li>
<li> 32GB Samsung EVO+ Micro SD Card (Class 10) Pre-loaded with NOOBS, USB MicroSD Card Reader </li>
<li> Raspberry Pi 4 Case </li>
<li> 3.5A USB-C Raspberry Pi 4 Power Supply (US Plug) with Noise Filter</li>
<li> Set of Heat Sinks </li>
<li> Micro HDMI to HDMI Cable - 6 foot (Supports up to 4K 60p) </li>
<li> USB-C PiSwitch (On/Off Power Switch for Raspberry Pi 4) </li>
</OL> 

Purchase Notes:  Keyboard, Mouse, Monitor are optional.  RPi advantages over AWS: 1. One time cost  2. All kinds of tinker projects in IOT realm can be performed using GPIO pins.  As for purchase options, CanaKit (my prefered) has options on Amazon that meet the bulleted list of requirements. There is a new option on raspberrypi.org that describes RPi as built into a keybaord (could be bulky in my use cases).

Webserver deployment preparation: RPi with NOOBS installed on SSD is very simple.  At boot select Raspberry Pi OS and you are on your way.  Since this will be private IP host on your home network, Port Forwarding is required to make your website visible on the Internet.

Runtime Notes: Mostly I use VNC Viewer to connect to the RPi.  This is a full desktop remote display tool.  RealVNC lets you share full desktop with cohorts.  If you reboot RPi, you need a monitor connected at reboot to maintain VNC screen share functionality.  Reboot will cause screen buffer not to be recognized unless HDMI is present.  There may be a dummy (mini) HDMI plug that could overcomee this issue.  Otherwise, after setup your RPi could be headless.



AWS EC2 Setup
-------------

# Instruction on preparing AWS EC2 instance for Webserver deployment
Login into your AWS IAM user, search for EC2.

To get started, launch an Amazon EC2 instance, which is a virtual server in the cloud.

![Launch EC2 instance](assets/ec2launch.png)

## Step 1: Choose an Amazon Machine Image (AMI)Cancel and Exit
An AMI is a template that contains the software configuration (operating system, application server, and applications) required to launch your instance. Pick Ubuntu free tier operating system that uses the Linux kernel.  Note, this is very compatible Raspberry Pi's OS.

![Select EC2 OS](assets/ec2os.png)

## Step 2: Choose an Instance Type
Amazon EC2 provides a wide selection of instance types optimized to fit different use cases. Instances have varying combinations of CPU, memory, storage, and networking capacity.   Stick with Free Tier options, as of this writing t2.mico with free tier designation is suggested.

## No action on Steps #3 through #4
Step 3: Configure Instance Details
Stick with default.  Your will launch a single instance of the AMI by using defaults

Step 4: Add Storage
Stick with default.  Your instance will be launched with 8gb of storage.

## Step 5: Add Tags
Tag your Amazon EC2 resources.  This is not required but you could name your volume for future identification.

![Tag EC2](assets/ec2tags.png)

## Step 6: Configure Security Group
A security group is a set of firewall rules that control the traffic for your instance. On this page, you can add rules to allow specific traffic to reach your instance. In this example, a web server is setup to allow Internet traffic to reach EC2 instance, this allows unrestricted access to the HTTP and HTTPS ports.  Also, this example restricts SSH from my IP.

![Select EC2 OS](assets/ec2security.png)

## Step 7: Review Instance Launch
Review your instance launch details. Click Launch to assign a key pair to your instance and complete the launch process.

![Build EC2 Keypair](assets/ec2keypair.png)

## Before you leave your ADMIN session on AWS go to EC2 running instances and find your IPV4 address.

![Find EC2 IPv4](assets/ec2ipv4.png)

# Start a terminal session on you localhost.



MacOS and AWS Ubuntu
-------------

## MacOS SSH (secure shell) and FTP (file transfer protocol) to your EC2 Ubuntu machine

### MacOS login into the EC2 instance using SSH

Manage your PEM file, rename and move to SSH configuration directory, setting permission on my PEM file to protect it:

MacBook-Pro-2:~ johnmortensen$ ``` sudo mv ~/Downloads/ec2ubuntu.pem ~/.ssh/ec2ubuntu.pem ```

MacBook-Pro-2:~ johnmortensen$ ``` sudo chmod 400 .ssh/ec2ubuntu.pem ```

SSH command

MacBook-Pro-2:~ johnmortensen$ ``` sudo ssh -i ~/.ssh/ec2ubuntu.pem ubuntu@52.34.146.159 ```

This should lead you to a NEW terminal prompt on ubuntu:

ubuntu@ip-172-31-30-21:~$

### Move JAR file to your deployment host with sftp (secure file transfer protocol).  This procedure shows a file from MacOS to Ubuntu on AWS.  

MacBook-Pro-2:~ ``` sftp -i ~/.ssh/ec2spring.pem ubuntu@52.34.146.159 ```

Connected to ubuntu@52.34.146.159.

sftp> ``` put serving-web-content-0.0.1-SNAPSHOT.jar ```

Uploading serving-web-content-0.0.1-SNAPSHOT.jar to /home/ubuntu/serving-web-content-0.0.1-SNAPSHOT.jar

serving-web-content-0.0.1-SNAPSHOT.jar        100%   18MB   1.8MB/s   00:09  

## Window puTTY (popular SSH and telnet client) and SCP (secure copy) to your EC2 Ubuntu machine



Windows and AWS Ubuntu
-------------

### Windoss login into ECW using SSH using puTTY
To SSH on a windows machine you will need to use [puTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html). (Download correct bit installer and keep default settings).

Add your EC2 instance ip into the putTTY IP bar and keep the port set as 22 (The standard SSH port)

![](https://github.com/nighthawkcoders/spring-idea/blob/master/assets/putty.png)

Open the puTTYgen app, (not puTTY), select "RSA: at the bottom and then click "load". Choose the .pem file downloaded from AWS earlier. Click "save private key" and click yes if you get a warning. Save this new .ppk file safely.

![](https://github.com/nighthawkcoders/spring-idea/blob/master/assets/puttygen.png)

In the navigation bar at the left, expand "SSH" and select "Auth". Under "private Key File for authentication" click browse change the setting to search for all files and select the .pem file downloaded from AWS in the previous step. Click Open to start the connection, if you get a warning message just click yes. Log in as "ec2-user". Now you have access to the ubuntu machine.

![](https://github.com/nighthawkcoders/spring-idea/blob/master/assets/puttyauth.png)


### If you are using windows you can transfer files from your computer to your AWS ubuntu machine using [WinSCP](https://winscp.net/eng/index.php). Download and install the version for your computer. Once the program opens, click the "New Session" button. Put your IPV4 address in the hostname box and "ubuntu" as the username.

Download and install the version for your computer. Once the program opens, click the "New Session" button. Put your IPV4 address in the hostname box and "ubuntu" as the username.

![](https://github.com/nighthawkcoders/spring-idea/blob/master/assets/winscp.png)

To load your private key click "Advanced" then open the "SSH" dropdown and choose "Authentication". Choose your private key here...

![](https://github.com/nighthawkcoders/spring-idea/blob/master/assets/advancedppk.png)

Then click "Login" to start the SFTP server connection. Your files will be on the left and your virtual machines files will be on the right. Drag your JAR file from your desktop into the your ubuntu machine.

![](https://github.com/nighthawkcoders/spring-idea/blob/master/assets/jarupload.png)

