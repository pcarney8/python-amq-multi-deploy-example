# Setup 


# Run Unit Tests
```bash
pipenv install --dev
pipenv run behave 
pipenv run pytest
```

By default, `behave` will skip integration tests, which
require the AMQ broker.

# Run Integration Tests
These test require the AMQ broker running

## Start AMQ broker

You will need deploy and start the AMQ Broker.  Use
the [amq-broker-deployment](https://github.com/pcarney8/amq-broker-deployment/)
project to deploy the broker to OpenShift

Before running the deployer, follow the instructions for deploying to your own namespace,
and add the test queues by editing the file
[amq-broker.yml](https://github.com/pcarney8/amq-broker-deployment/src/master/inventory/host_vars/amq-broker.yml),
and modifying this line:

```
AMQ_QUEUES: test.queue
```

to

```
AMQ_QUEUES: test_1.queue,test_2.queue
```

### Set local environment variables 
```bash
export ACTIVEMQ_ADDRESS=127.0.0.1:5672;
export QUEUE_1=test_1.queue; 
export QUEUE_2=test_2.queue;
```

### Set up port forward to the AMQ broker on OCP

Log into OCP
```bash
oc login https://console.patrick.rht-labs.com:443
```
Ensure correct project 
```bash
oc project <your namespace>
```
Run port forward to the amq broker pod (Note: Forward will time out)
```bash
oc port-forward <amq-broker pod name> 5672 
```

### Run tests 
Run only integration tests
```bash
pipenv run behave -t integration
```
Run all tests 
```bash
pipenv run behave -t integration,~integration
```


