import datetime
import glob
import os
import random

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import metrics
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier

st = datetime.datetime.now()

SIZE = 128


def array_population_train(main_directory, file_path, images_array, labels_array):
    for directory_path in glob.glob(main_directory):
        label = directory_path.split("\\")[-1]

        for img_path in glob.glob(os.path.join(directory_path, file_path)):
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            img = cv2.resize(img, (SIZE, SIZE))
            images_array.append(img)
            labels_array.append(label)


train_images = []
train_labels = []

array_population_train("dataset/train/*", "*/ears*.jp*", train_images, train_labels)
array_population_train("dataset/train/*", "*/eyes*.jp*", train_images, train_labels)
array_population_train("dataset/train/*", "*/muzzle*.jp*", train_images, train_labels)

train_images = np.array(train_images)
train_labels = np.array(train_labels)

test_images = []
test_labels = []

array_population_train("dataset/test/*", "*/ears*.jp*", test_images, test_labels)
array_population_train("dataset/test/*", "*/eyes*.jp*", test_images, test_labels)
array_population_train("dataset/test/*", "*/muzzle*.jp*", test_images, test_labels)

test_images = np.array(test_images)
test_labels = np.array(test_labels)

le = preprocessing.LabelEncoder()
le.fit(test_labels)
test_labels_encoded = le.transform(test_labels)
le.fit(train_labels)
train_labels_encoded = le.transform(train_labels)

x_train, y_train, x_test, y_test = train_images, train_labels_encoded, test_images, test_labels_encoded

x_train, x_test = x_train / 255.0, x_test / 255.0


# Feature Extractor Method

def feature_extractor(dataset):
    x_train = dataset
    image_dataset = pd.DataFrame()
    for image in range(x_train.shape[0]):
        df = pd.DataFrame()
        input_img = x_train[image, :, :, :]
        img = input_img

        # Adding data to the dataframe

        # Feature 1: add pixel values
        pixel_values = img.reshape(-1)
        df['Pixel_Value'] = pixel_values

        # Feature 2: Gabor Filters
        num = 1
        kernels = []
        for theta in range(2):
            theta = theta / 4 * np.pi
            for sigma in (1, 3):
                lamda = np.pi / 4
                gamma = 0.5
                gabor_label = 'Gabor' + str(num)
                ksize = 9
                kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lamda, gamma, 0, ktype=cv2.CV_32F)
                kernels.append(kernel)
                fimg = cv2.filter2D(img, cv2.CV_8UC3, kernel)
                filtered_img = fimg.reshape(-1)
                df[gabor_label] = filtered_img
                # print(gabor_label, ': theta=', theta, ': sigma=', sigma, ': lamda=', lamda, ': gamma=', gamma)
                num += 1

        image_dataset = image_dataset.append(df)

    return image_dataset


##############################################################

image_features = feature_extractor(x_train)

n_features = image_features.shape[1]
image_features = np.expand_dims(image_features, axis=0)
X_for_RF = np.reshape(image_features, (x_train.shape[0], -1))

RF_model = RandomForestClassifier(n_estimators=50, random_state=42)

# Fit model on training data

RF_model.fit(X_for_RF, y_train)

test_features = feature_extractor(x_test)
test_features = np.expand_dims(test_features, axis=0)
test_for_RF = np.reshape(test_features, (x_test.shape[0], -1))

test_prediction = RF_model.predict(test_for_RF)
test_prediction = le.inverse_transform(test_prediction)

et = datetime.datetime.now()
elapsed_time = et - st
print('Execution time:', elapsed_time)

print('Accuracy = ', metrics.accuracy_score(test_labels, test_prediction))

cm = confusion_matrix(test_labels, test_prediction)

fig, ax = plt.subplots(figsize=(6, 6))
sns.set(font_scale=1.6)
sns.heatmap(cm, annot=True, ax=ax)
plt.show()

n = random.randint(0, x_test.shape[0] - 1)
img = x_test[n]
plt.imshow(img)
plt.show()

input_img = np.expand_dims(img, axis=0)
input_img_features = feature_extractor(input_img)
input_img_features = np.expand_dims(input_img_features, axis=0)
input_img_for_RF = np.reshape(input_img_features, (input_img.shape[0], -1))

img_prediction = RF_model.predict(input_img_for_RF)
img_prediction = le.inverse_transform(img_prediction)
print("The prediction for this image is: ", img_prediction)
print("The actual label for this image is: ", test_labels[n])
