# Discussion #8410: Is there any detection model trained with negative samples? How to calculate the anchors shapes targeting nodules < 3 and >=3 mm ?
**Repository:** Project-MONAI/MONAI
**Author:** abhishekmarkad
**Created At:** 2025-04-04T06:09:59Z

## Description
I am using the script/config from https://monai.io/model-zoo.html to train retinanet detector,
While we put 10% negative samples in training data we had some problems. The Monai forum had a solution,followed it and made the changes,and were able to start training with custom data. Did experiments.Each experiment differs in terms of the nature of training data.
**Changes done to include Negative samples in training**
 * Reference : [https://github.com/Project-MONAI/tutorials/pull/1256/](https://github.com/Project-MONAI/tutorials/pull/1256/files) 
 * Added  “StandardizedEmptyBoxd” transform in train.preprocessing_trasform in config/train.json obtained from https://monai.io/model-zoo.html ( Lung nodule CT detection )
![Screenshot from 2025-04-02 14-54-41](https://github.com/user-attachments/assets/4a475db1-9e95-42d9-8a7f-02d71c039953)

 
**Experiments**
 * Experiment 1 (positive + negative samples)
   - Nature of Training data : scans with nodules ranging from 2 mm onwards and 10% negative samples
   - Problem : The validation accuracy was zero till 115 epochs.
![Screenshot from 2025-04-02 15-24-12](https://github.com/user-attachments/assets/aa90ab49-97fc-45bf-b529-554bad1fe142)

 * Experiment 2 (positive + negative samples)
   - Nature of Training data  : scans with nodules >=3 mm and negative samples
   - Problem : The validation accuracy was zero .
![Screenshot from 2025-04-03 10-54-15](https://github.com/user-attachments/assets/5928d5e8-d3bc-4d67-9408-93ac243922ea)

 * I observe following output on console with Experiment 1 and 2.
     ![Screenshot from 2025-04-02 14-31-07](https://github.com/user-attachments/assets/6fbd75e0-648d-443b-8ffe-bb382655edd8)

 * Experiment 3 (positive samples)
   - Nature of Training data : positive samples  with nodules <3 mm & >=3mm
   - Problem : The validation accuracy increasing after 80+ epochs.
![Screenshot from 2025-04-02 15-26-34](https://github.com/user-attachments/assets/44c1928a-5c39-476c-b1e8-04dec3481173)

 * Experiment 4 (positive samples)
   - Nature of Training data :  Positive samples with nodules >=3 mm
   - Everything looks fine
![Screenshot from 2025-03-28 19-34-42](https://github.com/user-attachments/assets/2e8303b5-6b2a-4c85-b80c-5ac102179fd3)


**Questions**
 1. Is it having anything with the size of nodules,I am wondering do i need to change the base anchors shape in config/train.json ?
 2. Am I doing anything wrong while including negative samples ? Is there any model trained with negative samples ?
  Any help will be appriciated.

## Comments
### Comment by abhishekmarkad at 2025-04-22T12:13:51Z
Hello Monai Team, any thought ?
