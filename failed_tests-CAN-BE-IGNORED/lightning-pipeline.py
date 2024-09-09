
# DOESN'T WORK FORGET IT
from lightning_sdk import Machine, Studio, JobsPlugin, MultiMachineTrainingPlugin


training_studio = Studio("training-studio", teamspace="jedha-educational-test-code", user="antoine")
#training_studio.stop()
#training_studio.start()
#training_studio.switch_machine(Machine.T4)
"""
training_studio.upload_file("requirements.txt")
training_studio.run("pip install -r requirements.txt")
training_studio.upload_file("train.py")
training_studio.upload_file("secrets.sh")
training_studio.run("source secrets.sh")
training_studio.run("echo 'secrets: ${APP_URI}'")
training_studio.run("python train.py")
training_studio.stop()
"""
#training_studio.run("mlflow run https://github.com/antoinekrajnc/mlflow_101 --build-image -A gpus=all")


description = training_studio.available_plugins['jobs']
plugin = JobsPlugin("jobs", description, training_studio)
plugin.run("mlflow run https://github.com/antoinekrajnc/mlflow_101 --build-image -A gpus=all", name="first-parameter-job")

#multi_machine_plugin= MultiMachineTrainingPlugin("jobs", description, training_studio)
#multi_machine_plugin.run("mlflow run https://github.com/antoinekrajnc/mlflow_101 --build-image -A gpus=all")