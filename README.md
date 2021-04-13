# *🧬 Auto Face verification 💻*

---

## Table of Contents

- [Description](#description)
- [Demo](#demo)
- [Further Enhancement](#further-enchancement)
- [Help](#help)

---

## Description

This is a face verification web app which can verify your identity.
This web app uses computer vision to verify the identity of the user.When user enters the app he/she is asked to hold their card according to the guide given,
and the card must be clearly visible and user's hand should not block the card.A Mild lighting condition is ideal.The user is Verfied if the face of the user and
the face in the ID card matches.

Acceptable ID forms
- Driver’s Licence
- Passport
- Aadhar card
- PAN card

Technologies Used
- Python
- Deep Learning
- Flask
- HTML,CSS
- Javascript

## Demo

<p align="center">
  <img src="testing/demo.gif"/>
</p>

## Further Enhancement

### Areas Needed Enhancement

#### Card Verification:
For card verification a image similarity model is used. This can be further enhanced using a SVM classifier or other ml or dl models

#### Card Detection:
For now , User is asked to place the card in a particular location for card verification. This can be automated by using a state of art object detection models
          like yolo, resnet etc..The models can be trained using transfer learning and can be used for detection
