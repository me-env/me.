# *me.*

me. purpose is to let you choose where and how you store your data as well as who access it. We have full control over it.

## Vision 

me. want to allow you to store your data the way you want.

This data that you store allow you to run plugins developped by *me.* and the community.

### Storage

Your data can be stored in different **storage locations** (non-exhaustive) 

- NAS
    - at your home
    - at your friend’s home ... (can have different NAS if you want redundancy without using cloud providers)
- AWS
- GCP
- Azure

### Plugins

These **plugins** could be 

- me Photo (sync the photos you take)
    - From your phone
    - From a camera
    - On your computer ...
- me Drive (sync folders on your computers)
- me-ssage
    - Message app that stores conversation on *me.*
- me Mails
    - Mail app that stores mails on *me.*
- Plugins for domotic purposes
    - Why would companies implement *me.* tools ?
        
        In a world in which your data is stored in *me.* Then all your preferences would be in there. Some plugins would implement your life routines and so on .. All tools that you allow to access your data in order to run programs on it could offer you a personnalized exeperience without ever owning your data.
        
- Plugins to rent your data to others companies that implement tools based on IA.
    
    You can see it as if you were paid for allowing google to access your location history
    
- Restaurant / Activity recommander
- me Pay
    - Bank information stored in me would allow you to do this.
    - About transactions
        Allow you to see your bank transaction from all banks and work with them
        - Categorize
        - Aggregate
        - Check if that match your plans
        - Do placement / risk prediction ...
- Autofill tool that would fill information on formular websites
    - passwords
    - id information
        - Name
        - Phone
        - Age
        - Gender ...
    - living place
- me Calendar
- me Assistant
    - I dream of an vocal assitant connected to all my data 💭❤️
- me News
    - Such as google news
- me Health
    - Such as samsung Health
- Detailed shopping information about what to buy to reach your weight goal related to what sport you pratice ...

As you may have noticed, a lot of applications are copied from what google does. Actually that’s the goal. If we could have an open source tool that would centralize all tools based on your data such as what google does with a“central” point being *myself / me.* instead of google that would be perfect 🙂

Also for a more technical part, this plugins are divided into 3 distincts categories.

- DataSource
    Import data from anything to *me.*    
- Service
    Programs / Apps that use your data
- Both (Service & DataSource)

### Data

This **data** could be (non-exhaustive)

- Photos / Videos
- Documents
- Password
- Messages
- Mails
- History
    - Internet Navigation
    - Location
    - Places you visited
    - Activity you have done
- Id information
- Tastes / What you like
    - Restaurant
    - Activities
    - Topics / Subject
- Calendar
- What you buy

> You get the idea, every software you use today owning data on you that you would prefer have control on, can be rebuilt in an opensource way, where you choose how your data is stored.


## Installation instructions (tested on Windows 11 only)

These tutos helped me with the installation in case you are facing some troubles : 
- https://phoenixnap.com/kb/install-spark-on-windows-10
- https://sparkbyexamples.com/pyspark-tutorial/
- https://www.youtube.com/watch?v=WQErwxRTiW0&ab_channel=ArdianUmam
- https://flutterq.com/encountering-warn-procfsmetricsgetter-exception-when-trying-to-compute-pagesize-error-when-running-spark/

The following information are complement to these tutorials.

### Spark

https://spark.apache.org/downloads.html : 3.2.0 -> Pre-built for Apache Hadoop 3.3 abd later

### Java

Java 8

### HADOOP

https://github.com/cdarlint/winutils
find the correct version, it depends on your spark version, then set the right env variable (example later)

### Config file

$Env:SPARK_HOME\conf\spark-defaults.conf

````
spark.eventLog.enabled           true
spark.eventLog.dir               file:///c:/tmp/spark-events
spark.history.fs.logDirectory    file:///c:/tmp/spark-events
spark.executor.processTreeMetrics.enabled false
````

### Mongodb

Mongodb databases configuration files have to contain all possible fields in the "required" section. Otherwise the schema returned by Collection at some point may not be correct.

### Environnement variables

Sso this is my own configuration, please adapt it with your paths

````yaml
# Apache Spark :
HADOOP_HOME: D:\Program Files\Hadoop\winutils\hadoop-3.2.2
JAVA_HOME: D:\Program Files\Java\jre1.8.0_202
SPARK_HOME: D:\Program Files\Spark\spark-3.2.0-bin-hadoop3.2
PYSPARK_PYTHON: C:\Users\cypri\anaconda3\python.exe
PYTHONPATH: %SPARK_HOME%\python;%SPARK_HOME%\python\lib\py4j-0.10.9.2-src.zip;%PYTHONPATH%
SCALA_HOME: C:\Program Files (x86)\sbt\bin

# MOGODB
MONGO_USER: cyprien
MONGO_PWD: pwd

# For Tink : 
CLIENT_ID: c5db78c20d154d5a979648f12ac7182b
CLIENT_SECRET: client_secret
EXTERNAL_USER_ID: cyprien_ricque
````

### history

Run history server on windows
````powershell
D:\'Program Files'\Spark\spark-3.2.0-bin-hadoop3.2\bin\spark-class.cmd org.apache.spark.deploy.history.HistoryServer
````
