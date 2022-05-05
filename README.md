![image](https://user-images.githubusercontent.com/25375373/163279746-14d7902b-98ed-4fcf-a4e3-f27d4bcbd339.png)

# MedPerf

MedPerf is an open benchmarking platform for medical artificial intelligence using Federated Evaluation. MedPerf focuses on broadening data access during AI model evaluation to ensure accurate and reliable assessment of model generalization and improve clinician and patient confidence in AI. Furthermore, MedPerf provides the opportunity for the medical and technical community to establish benchmarks and related best practices for medical AI solutions.

## Benchmarks

A benchmark enables quantitative measurement of the performance of AI models for specific clinical tasks, and consists of the following components:
- Specifications: The task on which trained AI models are evaluated, and further details about the methodology
- Dataset Preparation: The process of preparing datasets for use in evaluation, and evaluation of these datasets
- Registered Datasets: A list of prepared and approved datasets 
- Reference Implementation: An example benchmark submission consisting of example model, evaluation and publicly available or synthetic data
- Registered Models: A list of registered models to run this benchmark
- Evaluation Metrics: The implementation of the evaluation metrics to be applied on the output of the model
- Documentation: To make the benchmark more understandable and usable.

## MLCubes

Multiple MedPerf benchmark components make use of [MLCubes](https://mlcommons.github.io/mlcube/). MLCubes are software containers with standard metadata and a consistent file-system level interface. MLCubes ensure that models are easily portable and reproducible by allowing the infrastructure software to easily interact with models implemented using different approaches or frameworks and more. 
MLCubes are for example used in Dataset preparation, Evaluation Metrics and the Registered Models.

## Datasets

MedPerf uses multiple datasets for each of the benchmarks. A Dataset can be registered by a Data Owner with the MedPerf server. To register their dataset, the data owner must first download the benchmark pipeline, which includes the data preparation MLCube. The Data Owner then follows the constructions given by the benchmark on how to prepare the data and process it with the data preparation MLCube. At the end of this process, the Data Preparation MLCube will output a Dataset registration file which contains the results of the data sanity-checks and summary statistics required by the benchmark.

## MedPerf platform
The benchmarks described above can be ran on the MedPerf platform.
MedPerf consists out of three important components.
-	A server, which uses a database to store the information necessary to coordinate experiments and support user management. For example, how to get, verify and run MLCubes, what private datasets are available to and compatible with a given benchmark and which models have been evaluated against which datasets under which metrics. No code is stored on the server.
-	The client, that can use this server to carry out experiments. To interact with the client, the CLI (Command Line Interface) can be used.
-	The cloud file servers and container repositories, hosting MLCubes, e.g. dockerHub.

## Workflow
To describe how the benchmarks are developed on the MedPerf platform, here we give an end-to-end workflow example.
- A benchmark is registered by a benchmark owner using the MedPerf client. The benchmark owner uploads the data preparation, reference model and evaluation metrics MLCubes to a container repository, and then registers them using the MedPerf server. The benchmark owner then submits the benchmark registration including required benchmark metadata.
- The model owner uploads the model MLCubes to a container repository, then registers them with the MedPerf Server. The model owner may then request inclusion of models in compatible benchmarks.
- The data owner downloads the metadata for the data preparation, reference model and evaluation metrics MLCubes from the MedPerf server. The MedPerf client uses these metadata to download and verify the corresponding MLCubes. The data owner then runs the data preparation steps and submits the registration output by the data preparation MLCube to the MedPerf server.
- To execute the benchmark, the data owner downloads the metadata for the model MLCubes used in the benchmark. The MedPerf client uses these metadata to download and verify the corresponding MLCubes. For each model, the data owner executes the model -> evaluation metrics pipeline and uploads the results files output by the evaluation metrics MLCube to the MedPerf server.

## How to run
In order to run MedPerf locally, you must host the server in your machine, and install the CLI.

1. ## Install dependencies
   MedPerf has some dependencies that must be installed by the user before being able to run. This are [mlcube](https://mlcommons.github.io/mlcube/) and the required runners (right now there's docker and singularity runners). Depending on the runner you're going to use, you also need to download the runner engine. For this demo, we will be using Docker, so make sure to get the [Docker Engine](https://docs.docker.com/get-docker/)

   ```
   pip install mlcube mlcube-docker mlcube-singularity
   ```
2. ## Host the server
   To access the MedPerf server, please follow the instructions inside the [`server/README.md`](server/README.md) file. The MedPerf server is used to access the datasets, run and implement MLCubes and obtain information about models.

3. ## Install the CLI:
   To install the CLI, please follow the instructions inside the [`cli/README.md`](cli/README.md) file. The CLI allows the user to specify commands through a command prompt.

## MedPerf usage
There are various things the user can do on the MedPerf platform. Here, an explanation is given of some of the common actions.

### Implementing MLCubes
To develop a benchmark, three MLCubes have to be implemented:
- Data Preparator MLCube
- Reference Model MLCube
- Evaluator MLCube
What these MLCubes are and how they are build can be found [here](https://github.com/aristizabal95/mlcube_examples/tree/medperf-examples/medperf/data_preparator)

To store the implemented MLCube, we expect the following to be present:
- The MLCube manifest (mlcube.yaml) and the parameters file (parameters.yaml)
- The MLCube image must be publicly available through docker hub.
- Additional files (those contained inside the mlcube/workspace/additional_files directory) must be compressed as a .tar.gz file and publicly hosted somewhere on the internet.

### Developing datasets
To test the implemented MLCubes, a dataset should be hosted. It is up to the user what the content of this dataset is.
Demo datasets must be compressed as a .tar.gz file, and at the root there should be a paths.yaml file with the following structure:

```
data_path: <DATA_PATH>
labels_path: <LABELS_PATH>
```
Where:
data_path: path relative to the location of the paths.yaml file that should be used as data_path input for the Data Preparator MLCube
labels_path: path relative to the location of the paths.yaml file that should be used as labels_path input for the Data Preparator MLCube


### Test your implemenetation
You can test your benchmark workflow before submitting anything to the platform. To do this, run the following command:
```
medperf test -p path/to/data_preparator/mlcube -m path/to/model/mlcube -e path/to/evaluator/mlcube -d <demo_dataset hash>
```

### Submit MLCubes
In order to submit your MLCubes to the MedPerf platform, run the following command:
```
medperf mlcube submit
```
Through the command prompt, you will be asked several questions regarding the MLCube.

### Submit benchmark
To submit your benchmark to the MedPerf platform, run the command:
```
medperf benchmark submit
```
Again, you will be asked several questions regarding the submission of the benchmark via the command prompt. The platform will run compatibility tests to ensure all requested information is correct.

### Adding new models
Models can be added for comparison on different benchmarks.
A new MLCube must be created, that follows the expected I/O of the benchmark, to do this. 
To test whether the model does this, the following command can be ran:
```
medperf test -b <benchmark_uid> -m <path/to/model/mlcube>
```
When the test passed, the model can be submitted to the MedPerf platform. An association to the benchmark can be created as follows:
```
	medperf [benchmark|mlcube] associate -m <mlcube_uid> -b <benchmark_uid>
```
Once an association is created, the other user must approve it. If the association is between two assets that you own, then it will be automatically approved and you can start using the model with your benchmark.

### Preparing datasets
To prepare a dataset for use in a benchmark, run the following command:
```
medperf dataset create -b <benchmark_uid> -d <path/to/data> -l <path/to/labels>
```
This command will execute the data preparation step with the data provided, and additionally will ask if you want to submit and associate the dataset with the benchmark. 

### Approving associations
For both adding a model or a dataset to a benchmark, an association must be created and approved by the benchmark owner and the other asset owner. If the owner of all assets is the same user, then approval is done automatically. 
You can see all your associations with the following command:
```
medperf association ls
```
Additionally, you may filter associations by their approval status
```
medperf association ls [pending | approved | rejected]
```

If you have any pending associations created by other users, you can approve/reject them with:
```
medperf association [approve|reject] -b <benchmark_uid> [-m <model_uid> | -d <dataset_uid>]
```

### Obtaining the reuslts
You can obtain metrics for a given benchmark, dataset and model with the following command:
```
medperf result create -b <benchmark_uid> -d <dataset_uid> -m <model_uid>
```
Both the dataset and the model must have an approved association with the benchmark.
This command will additionally try to submit the results under the user’s approval. If submissions is canceled by the user, it can always be done again with:
```
medperf result submit -b <benchmark_uid> -d <dataset_uid> -m <model_uid>
```

You can get information about your results with:
```
medperf result ls
```

## Demo
The server comes with prepared users and cubes for demonstration purposes. A toy benchmark was created beforehand for benchmarking XRay models. To execute it you need to:
1. ## Get the data
   The toy benchmark uses the [TorchXRayVision]() library behind the curtain for both data preparation and model implementations. To run the benchmark, you need to have a compatible dataset. The supported dataset formats are:
   - RSNA_Pneumonia
   - CheX
   - NIH
   - NIH_Google
   - PC
   - COVID19
   - SIIM_Pneumothorax
   - VinBrain
   - NLMTB

   As an example, we're going to use the CheXpert Dataset for the rest of this guide. You can get it [here](https://stanfordmlgroup.github.io/competitions/chexpert/). Even though you could use any version of the dataset, we're going to be using the downsample version for this demo. Once you retrieve it, keep track of where it is located on your system. For this demonstration, we're going to assume the dataset was unpacked to this location: 
   
   ```
   ~/CheXpert-v1.0-small
   ```
   We're going to be using the validation split
2. ## Authenticate the CLI
   If you followed the server hosting instructions, then your instance of the server already has some toy users to play with. The CLI needs to be authenticated with a user to be able to execute commands and interact with the server. For this, you can run:
   ```
   medperf login
   ```
   And provide `testdataowner` as user and `test` as password. You only need to authenticate once. All following commands will be authenticated with that user.
3. ## Run the data preparation step
   Benchmarks will usually require a data owner to generate a new version of the dataset that has been preprocessed for a specific benchmark. The command to do that has the following structure
   ```
   medperf dataset create -b <BENCHMARK_UID> -d <PATH_TO_DATASET> -l <PATH_TO_LABELS>
   ```
   for the CheXpert dataset, this would be the command to execute:
   ```
   medperf dataset create -b 1 -d ~/CheXpert-v1.0-small -l ~/CheXpert-v1.0-small
   ```
   Where we're executing the benchmark with UID `1`, since is the first and only benchmark in the server. By doing this, the CLI retrieves the data preparation cube from the benchmark and processes the raw dataset. You will be prompted for additional information and confirmations for the dataset to be prepared and registered onto the server.
4. ## Run the benchmark execution step
   Once the dataset is prepared and registered, you can execute the benchmark with a given model mlcube. The command to do this has the following structure
   ```
   medperf run -b <BENCHMARK_UID> -d <DATA_UID> -m <MODEL_UID>
   ```
   For this demonstration, you would execute the following command:
   ```
   medperf run -b 1 -d 63a -m 2
   ```
   Given that the prepared dataset was assigned the UID of 63a. You can find out what UID your prepared dataset has with the following command:
   ```
   medperf dataset ls
   ```
   Additional models have been provided to the benchmark, this is the list of models you can execute:
   - 2: CheXpert DenseNet Model
   - 4: ResNet Model
   - 5: NIH DenseNet Model

    During model execution, you will be asked for confirmation of uploading the metrics results to the server.

## Automated Test
A `test.sh` script is provided for automatically running the whole demo on a public mock dataset.

### Requirements for running the test
- It is assumed that the `medperf` command is already installed (See instructions on `cli/README.md`) and that all dependencies for the server are also installed (See instructions on `server/README.md`).
- `mlcube` command is also required (See instructions on `cli/README.md`)
- The docker engine must be running
- A connection to internet is required for retrieving the demo dataset and mlcubes

Once all the requirements are met, running `sh test.sh` will:
- cleanup any leftover medperf-related files (WARNING! Running this will delete the medperf workspace, along with prepared datasets, cubes and results!)
- Instantiate and seed the server using `server/seed.py`
- Retrieve the demo dataset
- Run the CLI demo using `cli/cli.sh`
- cleanup temporary files
  
## Pilots
In order to validate MedPerf we performed a series of pilot experiments with academic groups that are involved in multi-institutional collaborations for the purposes of research and development of medical AI models. The experiments were intentionally designed to include a diversity of domains and modalities in order to test MedPerf’s infrastructure adaptance. The experiments included public and private data highlighting the technical capabilities of MedPerf to operate on private data. We also asked participating teams to provide feedback on their experience with MedPerf (e.g., limitations, issues). 

**Data sources**

The figure below displays the data provider locations used in all pilot experiments. 🟢: Pilot 1 - Brain Tumor Segmentation Pilot Experiment; 🔴: Pilot 2 - Pancreas Segmentation Pilot Experiment. 🔵: Pilot 3 - Surgical Workflow Phase Recognition Pilot Experiment. Pilot 4 - Cloud Experiments, used data and processes from Pilot 1 and 2.

![image](https://user-images.githubusercontent.com/25375373/163238058-6cf16f00-5238-4c80-8b58-d86f291a5bcf.png)

### Pilot 1 - Brain Tumor Segmentation

**Participating institutions**

- University of Pennsylvania, Philadelphia, USA
- Perelman School of Medicine, Philadelphia, USA

**Task**

Gliomas are highly heterogeneous across their molecular, phenotypical, and radiological landscape. Their radiological appearance is described by different sub-regions comprising 1) the “enhancing tumor” (ET), 2) the gross tumor, also known as the “tumor core” (TC), and 3) the complete tumor extent also referred to as the “whole tumor” (WT). ET is described by areas that show hyper-intensity in T1Gd when compared to T1, but also when compared to ”healthy” white matter in T1Gd. The TC describes the bulk of the tumor, which is what is typically resected. The TC entails the ET, as well as the necrotic (fluid-filled) parts of the tumor. The appearance of the necrotic (NCR) tumor core is typically hypo-intense in T1Gd when compared to T1. The WT describes the complete extent of the disease, as it entails the TC and the peritumoral edematous/invaded tissue (ED), which is typically depicted by hyper-intense signal in T2-FLAIR.
These scans, with accompanying manually approved labels by expert neuroradiologists for these sub-regions, are provided in the International Brain Tumor Segmentation (BraTS) challenge data.

**Data**

The BraTS 2020 challenge dataset is a retrospective collection of 2,640 brain glioma multi-parametric magnetic resonance imaging (mpMRI) scans, from 660 patients, acquired at 23 geographically-distinct institutions under routine clinical conditions, i.e., with varying equipment and acquisition protocols.The exact mpMRI scans included in the BraTS challenge dataset are a) native (T1) and b) post-contrast T1-weighted (T1Gd), c) T2-weighted (T2), and d) T2-weighted Fluid Attenuated Inversion Recovery (T2-FLAIR). Notably, the BraTS 2020 dataset was utilized in the first ever federated learning challenge, namely the Federated Tumor Segmentation (FeTS) 2021 challenge (https://miccai.fets.ai/) that ran in conjunction with the Medical Image Computing and Computer Assisted Interventions (MICCAI) conference. Standardized pre-processing has been applied to all the BraTS mpMRI scans. This includes conversion of the DICOM files to the NIfTI file format, co-registration to the same anatomical template (SRI24), resampling to a uniform isotropic resolution (1mm3), and finally skull-stripping. The pre-processing pipeline is publicly available through the Cancer Imaging Phenomics Toolkit (CaPTk).

**Code**

[github.com/mlcommons/medperf/tree/main/examples/BraTS](https://github.com/mlcommons/medperf/tree/main/examples/BraTS)

### Pilot 2 - Pancreas Segmentation

**Participating institutions**

- Harvard School of Public Health, Boston, USA
- Dana-Farber Cancer Institute, Boston, USA

**Task**

Precise organ segmentation using computed tomography (CT) images is an important step for medical image analysis and treatment planning. Pancreas Segmentation involves immense challenge due to the small volume and irregular shapes. Our goal is to perform federated evaluation across different sites using MedPerf for the task of pancreas segmentation.

**Data**

We utilized two separate datasets for the pilot experiment. The first of which is the Multi-Atlas Labeling Beyond the Cranial Vault (BTCV) dataset. This dataset is publicly available through synapse platform. Abdominal CT images from the metastatic liver cancer patients and the postoperative ventral hernia patients were acquired at the Vanderbilt University Medical Center. Voxel size for images was 0.6 to 0.9 mm in the anterior-posterior (AP) and left-right (LR) axis and 1.5 to 7.0 mm in the inferior-superior (IS) axis were the image acquisition parameters. Abdominal CT images were registered using NiftyReg. A total of 3719 images were obtained from 40 subjects for the task. 3719 images were randomly distributed into 2916 images for training, and 803 images for testing. The data distribution was done in a subject-wise manner to avoid data leakage between the training and the testing dataset. Due to the inconsistency in the image orientation, all the images were re-oriented to a standard orientation for further analysis.
In addition to the BTCV dataset, we also included another publicly available dataset from The Cancer Imaging Archives (TCIA). The National Institute of Health Clinical Center curated the dataset with 82 abdominal scans, from 53 male and 27 female subjects. Of which 17 patients had known kidney donations that confirmed healthy abdominal regions, and the remaining patients were selected after examination confirmed that the patients had neither pancreatic lesions nor any other significant abdominal abnormalities. These scans varied between 1.5 - 2.5 mm, with 512 x 512 pixel resolution, generating 18782 individual scans.

**Code**

[github.com/mlcommons/medperf/tree/main/examples/DFCI](https://github.com/mlcommons/medperf/tree/main/examples/DFCI)

### Pilot 3 - Surgical Workflow Phase Recognition

**Participating institutions**

- CNRS, France
- IHU Strasbourg, France

**Task**

Surgical phase recognition is a classification task of each video frame from a recorded surgery to one of some predefined phases that give a coarse description of the surgical workflow. This task is a building block for context-aware systems that help in assisting surgeons for better Operating Room (OR) safety.

**Data**

The data we used corresponds to Multichole2022; a multicentric dataset comprising videos of recorded laparoscopic cholecystectomy surgeries, annotated for the task of surgical phase recognition. The dataset consists of 180 videos in total, of which 56 videos were used in our pilot experiment and the rest of the videos (i.e., 124) were used to train the model. The videos were taken from five (5) different hospitals: 32 videos from the University Hospital of Strasbourg, France; which are part of the public dataset Cholec80, and 6 videos were taken from each of the following Italian hospitals: Policlinico Universitario Agostino Gemelli, Rome; Azienda Ospedaliero-Universitaria Sant’Andrea, Rome; Fondazione IRCCS Ca’ Granda Ospedale Maggiore Policlinico, Milan; and Monaldi Hospital, Naples. The data is still private for now. Videos are annotated according to the Multichole2022 annotation protocol, with 6 surgical phases: Preparation, Hepatocytic Triangle Dissection, Clipping and Cutting, Gallbladder Dissection, Gallbladder Packaging, and Cleaning / Coagulation

**Code**

[github.com/mlcommons/medperf/tree/main/examples/SurgMLCube](https://github.com/mlcommons/medperf/tree/main/examples/SurgMLCube)

### Pilot 4 - Cloud Experiments

**Task**

We proceeded to further validate MedPerf on the cloud. Towards this, we executed various parts of the MedPerf architecture across different cloud providers. Google Cloud Platform (GCP) was used across all experiments for hosting the server. The Brain Tumor Segmentation (BraTS) Benchmark (Pilot 1), as well as part of the Pancreas Segmentation Benchmark (Pilot 2), were executed inside a GCP Virtual Machine with 128GB of RAM and an Nvidia T4.
Lastly, we created a Chest X-Ray Pathology Classification Benchmark to demonstrate the feasibility of running federated evaluation across different cloud providers. For this, the CheXpert 40 small validation dataset was partitioned into 4 splits, and executed inside Virtual Machines provided by AWS, Alibaba, Azure, and IBM. All results were retrieved by the MedPerf server, hosted on GCP. The figure below shows which cloud provider each MedPerf component (i.e., server, client) and dataset was executed on.

**Data**

Here we used data and processes from Pilot #1 and #2.

**Code**

[github.com/mlcommons/medperf/tree/main/examples/Chest XRay](https://github.com/mlcommons/medperf/tree/main/examples/Chest%20XRay)

**Architecture**

![image](https://user-images.githubusercontent.com/25375373/163241596-464aa465-e517-41cd-b2c0-d698047c1ed2.png)
