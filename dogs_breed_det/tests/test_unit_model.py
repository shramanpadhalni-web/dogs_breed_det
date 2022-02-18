# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 08:47:51 2019

@author: Hem Chandra Padhalni
"""
import unittest
import numpy as np
import tensorflow as tf
import dogs_breed_det.models.deep_api as dog_model

from keras import backend as K

debug = True


class TestModelMethods(unittest.TestCase):
    def setUp(self):
        self.meta = dog_model.get_metadata()
        self.network = 'Resnet50'
        self.num_classes = 133

        print("[INFO] TensorFlow version: {}".format(tf.__version__))

    def test_model_metadata_type(self):
        """
        Test that get_metadata() returns list
        """
        self.assertTrue(type(self.meta) is dict)

    def test_model_metadata_values(self):
        """
        Test that get_metadata() returns
        right values (subset)
        """
        print("Meta:", self.meta)
        self.assertEqual(self.meta['name'].replace('-', '_').lower(),
                         'dogs_breed_det'.replace('-', '_').lower())
        self.assertEqual(self.meta['author'].lower(), 'V.Kozlov (KIT)'.lower())
        self.assertEqual(self.meta['author-email'].lower(),
                         'valentin.kozlov@kit.edu'.lower())

    def test_model_variables(self):
        print("[test_model_variables]")

        train_tensor = np.random.normal(size=(2, 1, 1, 2048))
        # train_tensor = np.random.normal(size=(2, 224, 224, 3))  # full ResNet
        label_tensor = np.random.normal(size=(2, self.num_classes))

        model = dog_model.build_model(self.network, self.num_classes)
        print(model.trainable_weights)

        before = K.get_session().run(model.trainable_weights)
        model.fit(train_tensor,
                  label_tensor,
                  epochs=1,
                  # need batch_size>=2, e.g. for the case of BatchNormalization
                  batch_size=2,
                  verbose=1)
        after = K.get_session().run(model.trainable_weights)

        # Make sure something changed.
        i = 0
        for b, a in zip(before, after):
            if debug:
                print("[DEBUG] {} : ".format(model.trainable_weights[i]))
                i += 1
                if (b != a).any() and debug:
                    print(" * ok, training (values are updated)")
                else:
                    print(" * !!! values didn't change, not training? !!!")
                    print(" * Before: {} : ".format(b))
                    print("")
                    print(" * After: {} : ".format(a))

            # Make sure something changed.
            assert (b != a).any()


# test_model_variables()

if __name__ == '__main__':
    unittest.main()
