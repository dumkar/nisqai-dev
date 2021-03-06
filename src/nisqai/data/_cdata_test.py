#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from nisqai.data._cdata import CData, LabeledCData, random_data, get_iris_setosa_data, get_mnist_data
from numpy import array, array_equal, allclose


def test_basic_cdata():
    """Creates a CData object and makes sure the dimensions are correct."""
    data = array([[1, 0, 0], [0, 1, 0]])
    cdata = CData(data)
    assert cdata.num_features == 3
    assert cdata.num_samples == 2


def test_higher_dim_cdata():
    """Creates a (3x3x3) Cdata object and
    ensures dimnetions are correct."""
    data = array([[[0, 1, 2],
                   [3, 4, 5],
                   [6, 7, 8]],
                  [[9, 10, 11],
                   [12, 13, 14],
                   [15, 16, 17]],
                  [[18, 19, 20],
                   [21, 22, 23],
                   [24, 25, 26]]])
    cdata = CData(data)
    assert cdata.num_samples == 3
    assert cdata.num_features == 9


def test_basic_labeled_cdata():
    """Creates a LabeledCData object and makes sure the dimensions are correct."""
    data = array([[1, 0, 0], [0, 1, 0]])
    labels = array([1, 0])
    lcdata = LabeledCData(data, labels)
    assert lcdata.num_features == 3
    assert lcdata.num_samples == 2


def test_get_random_data_basic():
    """Tests to see if we can get random data."""
    cdata = random_data(num_features=2,
                        num_samples=4,
                        labels=None)
    assert cdata.num_features == 2
    assert cdata.num_samples == 4


def test_scale_features_min_max_norm():
    """Tests min-max norm method of scale_features."""
    data = array([[0.564, 20.661], [-18.512, 41.168], [-0.009, 20.440]])
    cdata = CData(data)
    # correct answer computed with Mathematica
    answer = array([[1, 0.0106619], [0, 1], [0.969962, 0]])

    # perform min-max norm scaling on features and check answer
    cdata.scale_features('min-max norm')
    assert allclose(answer, cdata.data)


def test_scale_features_mean_norm():
    """Tests mean norm method of scale_features."""
    data = array([[0.564, 20.661], [-18.512, 41.168], [-0.009, 20.440]])
    cdata = CData(data)

    # correct answer computed in Mathematica
    answer = array([[0.343346, -0.326225], [-0.656654, 0.663113], [0.313308, -0.336887]])

    # perform mean norm scaling on features and check answer
    cdata.scale_features('mean norm')
    assert allclose(answer, cdata.data)


def test_scale_features_standardize():
    """Tests standardization method of scale_features."""
    data = array([[0.564, 20.661], [-18.512, 41.168], [-0.009, 20.440]])
    cdata = CData(data)

    # correct answer computed in Mathematica
    answer = array([[0.60355, -0.568043], [-1.1543, 1.15465], [0.550748, -0.586608]])

    # perform standardization feature scaling and check answer
    cdata.scale_features('standardize')
    assert allclose(answer, cdata.data)


def test_scale_features_L2_norm():
    """Tests L2 norm method of scale_features."""
    data = array([[0.564, 20.661], [-18.512, 41.168], [-0.009, 20.440]])
    cdata = CData(data)

    # correct answer computed in Mathematica
    answer = array([[0.0304526, 0.409996], [-0.999536, 0.816936], [-0.000485946, 0.40561]])

    # perform L2 normalization and check answer
    cdata.scale_features('L2 norm')
    assert allclose(answer, cdata.data)


def test_scale_features_L1_norm():
    """Tests L1 norm method of scale_features."""
    data = array([[0.564, 20.661], [-18.512, 41.168], [-0.009, 20.440]])
    cdata = CData(data)

    # correct answer computed in Mathematica
    answer = array([[0.029552, 0.25114], [-0.969976, 0.500407], [-0.000471575, 0.248453]])

    # perform L1 normalization and check answer
    cdata.scale_features('L1 norm')
    assert allclose(answer, cdata.data)


def test_get_iris_setosa_data():
    """ Checks that iris setosa data set is of correct length
    """
    iris = get_iris_setosa_data()
    assert len(iris.data) == 150 and len(iris.labels) == 150


def test_get_mnist_data():
    """ Checks that mnist data set is of correct length
    """
    mnist = get_mnist_data()
    assert len(mnist.data) == 60000 and len(mnist.labels) == 60000


def test_basic_labeling():
    """ Ensures LabeledCData runs correctly with given input labels
    """
    # data with only 1 feature
    data = array([[-1], [1], [0.5], [0.25], [-0.33], [0]])
    # give 1 if feature value >= 0; otherwise 0
    labels = array([0, 1, 1, 1, 0, 1])
    cdata = LabeledCData(data, labels)

    # ensure that labelling is correct
    assert array_equal(cdata.labels, labels)


def test_func_labeling():
    """ Ensure data labelled with a basic fuction works.
    """
    def f(x):
        return 1 if x >= 0 else 0
    data = array([[500], [-17], [12], [0], [-.002], [.001]])
    labels = array([f(x) for x in data])
    cdata = LabeledCData(data, f)

    # ensure data is labelled correctly
    assert array_equal(labels, cdata.labels)


def test_data_splititng():
    """ Ensures that splitting data into training and test set works."""
    data = array([-1, 0, 1, 5, -2, 17, 8])
    labels = array([0, 1, 1, 1, -1, 1, 1])
    cdata = LabeledCData(data, labels)

    # split data into various sizes
    testdata, traindata = cdata.train_test_split(0.1)
    assert array_equal(data[:0], testdata)
    assert array_equal(data[1::], traindata)

    testdata, traindata = cdata.train_test_split(0.2)
    assert array_equal(data[:1], testdata)
    assert array_equal(data[2::], traindata)

    testdata, traindata = cdata.train_test_split(0.3)
    assert array_equal(data[:2], testdata)
    assert array_equal(data[3::], traindata)

    testdata, traindata = cdata.train_test_split(0.4)
    assert array_equal(data[:2], testdata)
    assert array_equal(data[3::], traindata)

    testdata, traindata = cdata.train_test_split(0.5)
    assert array_equal(data[:3], testdata)
    assert array_equal(data[4::], traindata)

    testdata, traindata = cdata.train_test_split(0.6)
    assert array_equal(data[:4], testdata)
    assert array_equal(data[5::], traindata)

    testdata, traindata = cdata.train_test_split(0.7)
    assert array_equal(data[:4], testdata)
    assert array_equal(data[5::], traindata)

    testdata, traindata = cdata.train_test_split(0.8)
    assert array_equal(data[:5], testdata)
    assert array_equal(data[6::], traindata)

    testdata, traindata = cdata.train_test_split(0.9)
    assert array_equal(data[:6], testdata)
    assert array_equal(data[7::], traindata)

    testdata, traindata = cdata.train_test_split(1)
    assert array_equal(data[:7], testdata)
    assert array_equal(data[8::], traindata)


if __name__ == "__main__":
    test_basic_cdata()
    test_higher_dim_cdata()
    test_basic_labeled_cdata()
    test_get_random_data_basic()
    test_scale_features_min_max_norm()
    test_scale_features_mean_norm()
    test_scale_features_standardize()
    test_scale_features_L2_norm()
    test_scale_features_L1_norm()
    test_get_iris_setosa_data()
    test_get_mnist_data()
    test_basic_labeling()
    test_func_labeling()
    test_data_splititng()
    print("All tests for CData passed.")
