# Clarity Code Test

Hi :wave:!

This files explains how to set up everything you need to run the code test scripts.
The scripts that execute the logic are written in Python :snake: and the scripts that orchestrate them are written in bash :penguin:.


## Requirements :memo:

Next requirements are needed in order to be able to run the tasks:

 * Any **Linux** :penguin: distribution, Mac os :apple: probably works just fine but I have not tested it, Windows should be avoided as we will leverage some hard work to the os.
 * **Python 3.7** :snake: (I use **Python 3.7.6** but any 3.7 version should works fine).
 * **virtualenv** (just if you don't want to mess up your installed Python).
 * **Docker** :whale:


## First steps

Beyond this point I'll assume that you are under a Linux distro. If you are not have in mind that some commands may change.

### Software installation

#### Python
First check your Python version, run the command `python` in a terminal. It should output something like this:

```bash
Python 3.7.6 (default, Jan 30 2020, 09:44:41)
[GCC 9.2.1 20190827 (Red Hat 9.2.1-1)] on linux
Type "help", "copyright", "credits" or "license" for more information.
```
If the output indicates that you are using Python 2 try `python3` and check the version again, as your `symlink` may be pointing to python 2. If you don't have python 3 install it with your default package manager or check [this guide](https://realpython.com/installing-python/). Again make sure you have python 3.6 installed.

#### virtualenv
Check if you have virtualenv installed. Run the following command `virtualenv --version`. If you don't have it just install it with `pip install virtualenv`. If your default python version is python2 run this command instead `python3 -m pip install virtualenv`. If you don't have `pip` follow [this guide](https://pip.pypa.io/en/stable/installing/).

#### docker
Make sure you have docker and docker-compose installed:
 *  `docker --version`
 * `docker-compose --version`

If you don't have it is it best to follow the [official installation guide](https://docs.docker.com/install/).

### Setting it up

Once you have installed all the requirements lets set the environment. First uncompress the file with all the contents `tar -xvzf name-of-archive.tar.gz -C /destination`. It should create a directory with the next structure:
```
 clarity
  ├── exercise_one.sh
  ├── exercise_two.sh
  ├── infrastructure
  ├── input-file-10000.txt
  ├── logs
  ├── parser
  ├── unlimited
  ├── config.ini
  ├── requirements.txt
```
 * `exercise_one.sh` and `exercise_two.sh` are the scripts that you will run.
 * `infrastructure` is a directory with the `docker-compose.yaml` that will create the database.
 * `logs` is the directory where logs will be saved.
 * `parser` contains the scripts that `exercise_one.sh` uses.
 * `unlimited` contains the scripts that `exercise_two.sh` will run.
 * `config.ini` is the configuration file for `exercise_two.sh`.
 * `requirements.txt`, python external libraries specification.

Change directory to the newly created one as the next steps are explained as if you are there.

#### Create a virtualenv

First create a virtual environment and install all the requirements.
 * `virtualenv clarity_env`
 * `source clarity_env/bin/activate`
 * `pip install -r requirements.txt`

Once you finish with the execution run `deactivate` to deactivate environment.

#### Set up docker
Just run the docker-compose file:
 * `docker-compose -f infrastructure/docker-compose.yaml up -d`
This will create a container with a Mongodb and a volume to store the data.

Once you have finished run:
 * `docker-compose -f docker-compose.yaml down`

### Run the scripts
As I mentioned before some hard work will be leveraged to the os. That's why the scripts are run in `bash`. Make sure you have permissions to run the scripts. `chmod +X script_name`. In this case `exercise_one.sh` and `exercise_two.sh`.

#### Exercise One
The tool given a file with a specific structure prints a list of hostnames connected to the given host during the given period.

Run the script as follows:
 * `./exercise_one.sh -f [file with data] -b [start of the period] -e [end of the period] -h [hostname]`

 There is not a specific order for the parameters, but everyone must be preceded by  it's flag either the sort or the long one. The next flags are provided:
  * `-f, --file` - file to be processed
  * `-h, --host` - hostname to match against.
  * `-b, --beggining` - start of the time period
  * `-e, --end` - end of the period.

The period must be in the next form `1582137623826` (epoch with miliseconds). You can create these epochs form [here](https://currentmillis.com/).

Example:
 * `./exercise_one.sh --file-name input-file-10000.txt --host Cerena --beggining 1565647200000 --end 1565650800000`

 The output is printed in the terminal. If you also want to store the result in a file just run it as follows:
 * `./exercise_one.sh --file-name input-file-10000.txt --host Cerena --beggining 1565647200000 --end 1565650800000 | tee file_name`

 If just want the output store in a file:
 * `./exercise_one.sh --file-name input-file-10000.txt --host Cerena --beggining 1565647200000 --end 1565650800000 > file_name`

##### How it works? :confounded:
Internally the script just runs a pipe:
 * `cat file | python map [hostname] | python reduce [start_time] [end_time]`.

 The first python script just filter the lines by a given hostname while the second filters by timestamp range. It is a simple map reduce that leverage the message passing to the os.

#### Exercise two
The tool should both parse previously written log files and terminate or collect input from a new log file while it's being written and run indefinitely. It will output, once every hour:
 * a list of hostnames connected to a given (configurable) host during the last hour
 * a list of hostnames received connections from a given (configurable) host during the last hour
 * the hostname that generated most connections in the last hour

 A file called `config.ini` is provided to configure the hostnames you want to track. The file has the following format:
 ```ini
 destination=some_destination
 source=some_source

 ```
 __It is very important that the file ends with an empty line. Otherwise the sh script won't be able to read it :cold_sweat:.__

 The variable `destination` is the name of the hostname you want the list of hostnames connected to.

 The variable `source` is the name of the hostname you want the list of hostnames received connections from.

Again you just have to run a sh script. But first make sure the docker container is up as the data will be loaded in a database. Run `docker-compose -f infrastructure/docker-compose.yaml up -d`.

Run:
 * `./exercise_two.sh -c [config file]  -l [input-file] -f [optional]`

 Again there's not a specific order for the parameters (this time there's not long format :cry:). But `-c` and `-f` must be followed by each file name.
  * `-c` - config file.
  * `-l` - input file.
  * `-f` - optional (just if you want the script to run forever).

Example:
 * `./exercise_two.sh -c config.ini -l input-file-10000.txt`

 This execution will end as the input file is processed. If you want the script to run forever add the `-f` flag:
 * `./exercise_two.sh -c config.ini -l input-file-10000.txt -f`

 This script will save some logs in the `/logs` directory that you can check. As in exercise one you want the output in terminal and in a file run:
 * `./exercise_two.sh -c config.ini -l input-file-10000.txt | tee file_name`
 If just want the output in a file:
 * `./exercise_two.sh -c config.ini -l input-file-10000.txt > file_name`

##### How it works? :confounded:
Internally the script run two processes. First one process the file and store the data in the db. The process either finish once it reads the file or stays alive listening to new lines. This process is executed as follows:
 * Process file and ends:
  * `tail -n +1 input-file-10000.txt | python unlimited/load_data.py | tee -a logs/load_data.log`
 * Process file and stays alive:
  * `tail -n +1 -f input-file-10000.txt | python unlimited/load_data.py | tee -a logs/load_data.log &`

 If the pipe is decomposed:
  * `tail -n +1` reads the file and pass it to next step. Note that one of the two differences between the executions is the `-f` flag in tail. This flag makes tail to keep alive listening for new changes. While `-n +1` indicates the precessing starting line.
  * `python unlimited/load_data.py` executes the python script that saves the data in a `Mongodb` database.
  * `tee` writes all the output to a file in /logs directory.
  * Note the `&` at the end in the endless execution. This tells the so to run it in the background.

The second process is executed every `3600 seconds` and queries the database to retrieve the results. This execution is as follows:
 * `python unlimited/hourly.py ${config[destination]} ${config[source]} | tee -a logs/hourly.log`

 If the pipe is decomposed:
  * `python unlimited/hourly.py ${config[destination]} ${config[source]}` executes the logic of the mongo queries. The arguments ${config[destination]} ${config[source]} are read from `config.ini` by the sh script.
  * `tee -a logs/hourly.log` saves the output to a file in the /logs directory.

### End

Make sure to deactivate everything before you leave.

 * `deactivate` for `virtualenv`
 * `docker-compose -f docker-compose.yaml down`

By by! :wave: :wave:
