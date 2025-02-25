import tensorflow as tf
import os
from tensorflow.examples.tutorials.mnist import input_data
import inference
import numpy as np

BATCH_SIZE = 50
LEARNING_RATE_BASE = 0.8
LEARNING_RATE_DECAY = 0.99
REGULARIZATION_RATE = 0.0001
TRAINING_STEPS = 3000
MOVING_AVERAGE_DECAY = 0.99

MODEL_SAVE_PATH = 'model/'
MODEL_NAME = 'model.ckpt'

def my_l2_regularization(data):
    return tf.nn.l2_loss(data) * REGULARIZATION_RATE

def train(mnist):
    x = tf.placeholder(tf.float32, [BATCH_SIZE,
                                    inference.IMAGE_SIZE,
                                    inference.IMAGE_SIZE,
                                    inference.NUM_CHANNELS],
                       name='x-input')


    y_ = tf.placeholder(tf.int32, name='y-input')
    global_step = tf.Variable(0, trainable=False)

    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    variable_averages_op = variable_averages.apply(tf.trainable_variables())

    regularizer = my_l2_regularization
    y = inference.inference(x, True, regularizer)

    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=y_)
    cross_entropy_mean = tf.reduce_mean(cross_entropy)

    loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))
    learning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE, global_step,
                                               mnist.train.num_examples/BATCH_SIZE,
                                               LEARNING_RATE_DECAY)

    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
    with tf.control_dependencies([train_step, variable_averages_op]):
        train_op = tf.no_op(name='train')

    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for i in range(TRAINING_STEPS):
            xs, ys = mnist.train.next_batch(BATCH_SIZE)
            reshape_xs = np.reshape(xs, [BATCH_SIZE, inference.IMAGE_SIZE, inference.IMAGE_SIZE, inference.NUM_CHANNELS])
            _,loss_value,step = sess.run([train_op, loss, global_step], feed_dict={x:reshape_xs, y_: ys})

            if i%100 == 0:
                print('after %d training steps, loss on training batch is %f.'%(step, loss_value))
                saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)


def main(argv=None):
    mnist = input_data.read_data_sets(os.environ['HOME'] +
                                      '/Downloads/github/MachineLearningDemo/tensorflowStudy/projects/'
                                      'simpleTest/mnist/MNIST_data/')
    train(mnist)
    return 1

if __name__ == '__main__':
    tf.app.run()















