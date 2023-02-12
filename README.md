# Chat App
![](https://github.com/AronKG/Group-1/actions/workflows/build.yml/badge.svg)

http://gagga.se

A group of five students organized and recorded on Canvas, have teamed up to create a project. The project is being tracked through git and hosted on GitHub. The GitHub repository has been shared with Tuwe (tuvelofstrom) and Rudy (rudymatela) and the repository link has been sent to both Tuwe and Rudy by email or Canvas.

## About the Project
The project aims to be a simple yet powerful chat app where users have a unique identifer which the user can share with others to connect and communicate with one another. Users will interact using a simple yet elegant user interface hosted on the local computer. The application uses websockets which uses the default HTTP ports so you dont have to open ports in the router. To start with, the application will only support ascii communication but will hopefully support utf-8 and VoIP future on. 

## Group Members

| Name             | Github handle     |
|------------------|-------------------|
| Johan Sollenius  | [11Johan11](https://github.com/11Johan11) | 
| Henrik Eriksson  | [HenrikEriksson1](https://github.com/HenrikEriksson1) |
| Mohamad Alkhaled | [Mohamadalkhaled](https://github.com/Mohamadalkhaled) | 
| Aron Kesete      | [AronKG](https://github.com/AronKG) | 
| Daniel Johansson | [danieljohansson94](https://github.com/danieljohansson94) |

## Declaration

Each of the group members have made an associated commit to this project. The following is a list of commits made by each student:

- I, Johan Sollenius, declare that I am the sole author of the content I add to this repository.
- I, Henrik Eriksson, declare that I am the sole author of the content I add to this repository.
- I, Mohamad Alkhaled, declare that I am the sole author of the content I add to this repository.
- I, Aron Kesete, declare that I am the sole author of the content I add to this repository.
- I, Daniel Johansson, declare that I am the sole author of the content I add to this repository.

## Plan

The project aims to implement a new feature that will improve the overall user experience. The new feature will work by allowing users to interact with the application in a more intuitive way. The project will have the following features:

- [ ] Peer-To-Peer
- [ ] RSA Encryption
- [x] WEB-Based using Flask
- [x] Websocket

The project will be developed using the following language(s):

- Python
- Html
- Javascript

The project will use the following build system:

- setuptools
- pip

You can track the progress of these tasks on our Kanban board: [Project chat-App board](https://github.com/users/AronKG/projects/3)

## Compilation and Running Instructions

To run this project, you will need to have Python 3 installed on your system.

1. Clone the repository to your local machine using the following command:

    ```git clone https://github.com/AronKG/Group-1.git```

2. Navigate to the project directory:

    ```cd Group-1```

3. Install the required packages:

    ```pip install -r requirements.txt```  
    
4. To run the server, open a terminal and execute the following command  

    ```python server.py --host 127.0.0.1 --port 80```
    
5. Navigate to the web with the specified ip&port and start chatting!

6. To stop the server, press `CTRL + C` on the terminal where the server is running.

Note: the above instructions are for running the code locally, you may want to adjust the host and ports according to your needs.

## Unit testing
Install the coverage.py library by running 

    pip install coverage

Run the test file with coverage by using the command 

    coverage run -m unittest 

Once the tests have been run, use the command 

    coverage report 
    
to view the coverage report. This will show the percentage of lines covered in your code.

You can also use pytest by running
    pytest

## Linter
Black can be installed by running 

    pip install black
    
It requires Python 3.7+ to run.
To run the black linter you simply write

    black {source_file_or_directory}
    
Further information [here](https://github.com/psf/black)

## Contribution

Each member of the group has made at least one commit to this project. We have agreed not to use force pushes to the master/main branch. If changes need to be undone, a new commit will be used instead.-

## Note

Please make sure that your name and email is set properly in your .gitconfig file, to ensure proper credit for your contributions.
