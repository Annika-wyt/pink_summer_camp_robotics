# Instructions

## To send the path from your computer to the SVEA vehicle, there are 2 major components:
1. docker 
    - to run a "datastreamer" to connects your computer to the SVEA vehicle
2. python
    - to produce the path, which is then followed by the SVEA vehicle

Use these instructions to set up the FleetMQ datastreamer and Python scripts to communicate between your computer and a SVEA vehicle. Select your operating system to get started:

- [Linux](#linux)
- [Windows](#windows)
- [Mac](#mac)


## Linux

### We need to frist git clone the files we need from GitHub

1. Open a terminal by searching for `terminal` on the "show applications" page.
2. Type the following command: 

    ```
    git clone https://github.com/Annika-wyt/pink_summer_camp_robotics.git
    ```

3. On the same terminal, type 
    
    ```
    cd pink_summer_camp_robotics
    ```

    followed by 

    ```
    ls
    ```

    you will see output similar to

    ```
    datastreamer-linux                              pink.json
    datastreamer-mac                                python
    datastreamer-windows                            python_installation_instruction.pdf
    Information_pack_Robotics_And_AI_Camp_2025.pdf  README.md

    ```
You can now continue with the next part. If you do not see the above layout, let us know!

### To setup the docker part:
1. Make sure you have docker installed. On the same terminal, type: 
    ```
    docker-compose --version
    ```

    If you see something like `docker-compose version x.xx.xx`, then you can continue with step 2. Otherwise, check the [Information Pack](Information_pack_Robotics_And_AI_Camp_2025.pdf) we sent you for the instruction for installing docker.

2. On the same terminal, type:
    ```
    cd datastreamer-linux
    ```
    Then,
    ```
    docker compose -f datastreamer-linux-<groupName>.yml up
    ```

    If you see something like:

    ```
    DEBUG: Waiting for incoming message...
    ```

    , you can continue with the next part. Otherwise, let us know. 

### To setup the python part
1. Make sure you have python installed. Open a new terminal and type:
    ```
    python --version
    ```
    or
    ```
    python3 --version
    ```
    if you see `Python x.xx.xx` for either of the command, then you can continue with step 2. Otherwise, follow the [Python Installation Instruction](python_installation_instruction.pdf) on how to install python. 

    #### NOTES: 
    `python` and `python3` are commands you type before your scripts (like `python script.py`), not folder names.

    If `python --version` works, use `python` for all commands below.
    
    If only `python3 --version` works, use `python3` for all commands below.

    The cd command is always `cd python` (the folder is named python, not python3).

2. On the same terminal, go to the directory where you git cloned the folder, and then type: 
    ```
    cd python
    ```
    then 
    ```
    ls
    ```
    You should see something similar to:
    ```
    create_venv.py  fmq_connect.py  pathplanning.py  requirements.txt
    ```

3. On the same terminal, type:
    ```
    python create_venv.py
    ```
    or
    ```
    python3 create_venv.py
    ```    
    The virtual environment is created when you see:
    ```
    ✅ Done!
    To activate type in the terminal: source pinkenv/bin/activate
    ```
4. Follow the instruction on the terminal and (on the same terminal), type
    ```
    source pinkenv/bin/activate
    ```
    Once activated, you’ll see your prompt change to indicate the environment is active, e.g.: 
    ```
    (pinkenv) user@user:~/Users/pink_summer_camp_robotics/python$ 
    ```

    Now you are run our code on a contained environment without interfering with your python setup.

5. Now, you can start sending the path from pathplanning to our SVEA vehicle. On the same terminal, type: 
    ```
    python fmq_connect.py --end=1,2
    ```
    or
    ```
    python3 fmq_connect.py --end=1,2
    ```
    The command with `--end=1,2` specify the goal position of the vehicle, you can change the value of `1` and `2` to anything that are within the map boundary.

### Bonus
If you want to see the path planned by A*, you can go onto 
[Foxglove](https://app.foxglove.dev/). Then, after you have created an account, you can go to "Open connection..." (on upper left) and on the websocket URL, change localhost to `ip-address`, and press "open". Let us know when you are on this step, and we can show you the correct ip-address. 

Then, on upper right, look for the arrow to the right of "Layout", click it and selec "Import from file...", go to the directory where you did `git clone`, and go to select `pink.json`. 

Now on the website, you will be able to see a path planned by A*.

## Windows

### We need to frist git clone the files we need from GitHub

1. Open a terminal by searching for command prompt on the "start" page.
2. Type the following command: 

    ```
    git clone https://github.com/Annika-wyt/pink_summer_camp_robotics.git
    ```

3. On the same terminal, type 

    ```
    cd pink_summer_camp_robotics
    ```

    followed by 

    ```
    dir
    ```

    you will see output similar to

    ```
        Directory: C:\Users\YourName\pink_summer_camp_robotics

        Mode                LastWriteTime         Length Name
        ----                -------------         ------ ----
        -a----        2025-07-01     12:34                datastreamer-linux
        -a----        2025-07-01     12:34                datastreamer-mac
        -a----        2025-07-01     12:34                datastreamer-windows
        -a----        2025-07-01     12:34            456 pink.json
        d-----        2025-07-01     12:34                python
        -a----        2025-07-01     12:34           1024 python_installation_instruction.pdf
        -a----        2025-07-01     12:34           2048 Information_pack_Robotics_And_AI_Camp_2025.pdf
        -a----        2025-07-01     12:34            789 README.md
    ```

    You can now continue with the next part. If you do not see something similar to the above layout, let us know!
    
### To setup the docker part:
1. Make sure you have docker installed. On the same command prompt, type: 
    ```
    docker-compose version
    ```

    If you see something like ```docker-compose version x.xx.xx```, then you're good to go. Otherwise, check the [Information Pack](Information_pack_Robotics_And_AI_Camp_2025.pdf) we sent you for the instruction for installing docker.

2. On the same command prompt, type:
    ```
    cd datastreamer-windows
    ```
    Then, 
    ```
    docker compose -f datastreamer-windows-<groupName>.yml up
    ```

    If you see something like:

    ```
    DEBUG: Waiting for incoming message...
    ```

    , you can continue with the next part. Otherwise, let us know. 

### To setup the python part
1. Make sure you have python installed. Open a new command prompt and type:
    ```
    python --version
    ```
    or
    ```
    python3 --version
    ```
    if you see `Python x.xx.xx` for either of the command, then you can continue with step 2. Otherwise, follow the [Python Installation Instruction](python_installation_instruction.pdf)  on how to install python. 

    #### NOTES: 
    `python` and `python3` are commands you type before your scripts (like `python script.py`), not folder names.

    If `python --version` works, use `python` for all commands below.

    If only `python3 --version` works, use `python3` for all commands below.

    The cd command is always `cd python` (the folder is named python, not python3).

2. On the same command prompt, go to the directory where you git cloned the folder, and then type: 
    ```
    cd python
    ```
    then 
    ```
    dir
    ```
    You should see something like:
    ```
    Directory: C:\Users\YourName\pink_summer_camp_robotics\python

    Mode                LastWriteTime         Length Name
    ----                -------------         ------ ----
    -a----        2024-07-01     12:34            456 create_venv.py
    -a----        2024-07-01     12:34            789 fmq_connect.py
    -a----        2024-07-01     12:34            321 path_ planning.py
    -a----        2024-07-01     12:34             89 requirements.txt
    ```

3. On the same command prompt, type:
    ```
    python create_venv.py
    ```
    or
    ```
    python3 create_venv.py
    ```    
    The virtual environment is created when you see:
    ```
    ✅ Done!
    To activate type in the terminal: pinkenv\Scripts\activate.ps1
    ```
4. Follow the instruction on the command prompt and (on the same command prompt), type
    ```
    pinkenv\Scripts\activate.ps1
    ```
    
    Once activated, you’ll see your prompt change to indicate the environment is active, e.g.: 
    ```
    (pinkenv) PS C:\Users\YourName\pink_summer_camp_robotics\python>
    ```

    Now you are run our code on a contained environment without interfering with your python setup.

5. Now, you can start sending the path from pathplanning to our SVEA vehicle. On the same command prompt, type: 
    ```
    python fmq_connect.py --end=1,2
    ```
    or
    ```
    python3 fmq_connect.py --end=1,2
    ```
    The command with `--end=1,2` specify the goal position of the vehicle, you can change the value of `1` and `2` to anything that are within the map boundary.

### Bonus

If you want to see the path planned by A*, you can go onto [Foxglove](https://app.foxglove.dev/). Then, after you have created an account, you can go to "Open connection..." (on upper left) and on the websocket URL, change localhost to `ip-address`, and press "open". Let us know when you are on this step, and we can show you the correct ip-address. 

Then, on upper right, look for the arrow to the right of "Layout", click it and selec "Import from file...", go to the directory where you did `git clone`, and go to select `pink.json`. 

Now on the website, you will be able to see a path planned by A*.

## Mac

### We need to frist git clone the files we need from GitHub

1. Open a terminal by pressing command + space, and type terminal, and press enter.

2. Type the following command: 

    ```
    git clone https://github.com/Annika-wyt/pink_summer_camp_robotics.git
    ```

3. On the same terminal, type 
    
    ```
    cd pink_summer_camp_robotics
    ```

    followed by 

    ```
    ls
    ```

    you will see output similar to

    ```
    datastreamer-linux                              pink.json
    datastreamer-mac                                python
    datastreamer-windows                            python_installation_instruction.pdf
    Information_pack_Robotics_And_AI_Camp_2025.pdf  README.md
    ```
    
    You can now continue with the next part. If you do not see the above layout, let us know!

### To setup the docker part:
1. Make sure you have docker installed. On the same terminal, type: 
    ```
    docker compose version
    ```

    If you see something like ```docker compose version x.xx.xx```, then you're good to go. Otherwise, check the [Information Pack](Information_pack_Robotics_And_AI_Camp_2025.pdf) we sent you for the instruction for installing docker.

2. On the same terminal, type:
    ```
    cd datastreamer-mac
    ```
    Then, 
    ```
    docker compose -f datastreamer-mac-<groupName>.yml up
    ```

    If you see something like:

    ```
    DEBUG: Waiting for incoming message...
    ```

    , you can continue with the next part. Otherwise, let us know. 

### To setup the python part
1. Make sure you have python installed. Open a new terminal and type:
    ```
    python --version
    ```
    or
    ```
    python3 --version
    ```
    if you see `Python x.xx.xx` for either of the command, then you can continue with step 2. Otherwise, follow the [Python Installation Instruction](python_installation_instruction.pdf) on how to install python. 

    #### NOTES: 
    `python` and `python3` are commands you type before your scripts (like `python script.py`), not folder names.

    If `python --version` works, use `python` for all commands below.

    If only `python3 --version` works, use `python3` for all commands below.

    The cd command is always `cd python` (the folder is named python, not python3).

2. On the same terminal, go to the directory where you git cloned the folder, and then type: 
    ```
    cd python
    ```
    then 
    ```
    ls
    ```
    You should see something like:
    ```
    create_venv.py  fmq_connect.py  path_planning.py  requirements.txt
    ```

3. On the same terminal, type:
    ```
    python create_venv.py
    ```
    or
    ```
    python3 create_venv.py
    ```    
    The virtual environment is created when you see:
    ```
    ✅ Done!
    To activate type in the terminal: source pinkenv/bin/activate
    ```
4. Follow the instruction on the terminal and (on the same terminal), type
    ```
    source pinkenv/bin/activate
    ```
    
    Once activated, you’ll see your prompt change to indicate the environment is active, e.g.: 
    ```
    (pinkenv) MacBook-Pro:python yourusername$
    ```

    Now you are run our code on a contained environment without interfering with your python setup.

5. Now, you can start sending the path from pathplanning to our SVEA vehicle. On the same terminal, type: 
    ```
    python fmq_connect.py --end=1,2
    ```
    or
    ```
    python3 fmq_connect.py --end=1,2
    ```
    The command with `--end=1,2` specify the goal position of the vehicle, you can change the value of `1` and `2` to anything that are within the map boundary.

### Bonus

If you want to see the path planned by A*, you can go onto [Foxglove](https://app.foxglove.dev/). Then, after you have created an account, you can go to "Open connection..." (on upper left) and on the websocket URL, change localhost to `ip-address`, and press "open". Let us know when you are on this step, and we can show you the correct ip-address. 

Then, on upper right, look for the arrow to the right of "Layout", click it and selec "Import from file...", go to the directory where you did `git clone`, and go to select `pink.json`. 

Now on the website, you will be able to see a path planned by A*.